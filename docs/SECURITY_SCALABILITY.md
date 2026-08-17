# Security and Scalability Safeguards — EcoInfraMind AI

## 1. Security Architecture

### 1.1 Local-Only Design
- Zero network connections to external services after installation.
- No telemetry, analytics, or usage reporting.
- All data (knowledge base, conversation history, uploaded documents) stored locally.
- The application is designed for single-user operation on a personal machine.

### 1.2 API Security
- The FastAPI server listens on localhost (127.0.0.1:8432) only.
- No authentication is implemented (not required for local-only single-user operation).
- No HTTPS (not required for localhost-only traffic).
- CORS is restricted in the middleware but localhost-origin requests are inherently trusted.

### 1.3 Input Validation
- All user inputs are validated before processing:
  - Calculator inputs are type-checked and range-checked.
  - File uploads are restricted to PDF, DOCX, TXT, MD (configurable).
  - File size is limited to prevent resource exhaustion.
  - Chat messages are truncated to prevent prompt injection via excessive length.

### 1.4 Prompt Injection Mitigation
- System prompts are hardcoded and override user instructions.
- User input is clearly delimited with ChatML tags (`<|im_start|>user`).
- The RAG pipeline limits context window to prevent context overflow attacks.
- Output post-processing (`clean_text()`) strips formatting characters that could be used for injection.

### 1.5 File Upload Safety
- Uploaded files are processed in-memory where possible; temporary files are cleaned up immediately.
- Only text extraction is performed; no macro execution or embedded content rendering.
- File type is verified by extension AND content inspection (where possible).
- Very large files (>10 MB) are rejected at the endpoint level.

## 2. Operational Safeguards

### 2.1 Resource Limits
- RAM usage capped at 5.5 GB via `settings.py` `max_ram_gb` parameter.
- LLM context window limited to 1024 tokens prevents unbounded memory growth.
- Response generation limited to 768 tokens maximum.
- ChromaDB retrieval limited to top-2 results (configurable).
- Knowledge chunk size fixed at 256 characters to bound embedding and retrieval cost.

### 2.2 Error Handling
- All endpoints use try-except blocks with structured error responses.
- LLM generation errors return partial results where possible.
- ChromaDB connection failures fall back to LLM-only responses.
- Calculator errors return descriptive messages identifying the invalid parameter.
- Unhandled exceptions return HTTP 500 with a generic error message (no stack trace leakage).

### 2.3 Graceful Degradation
- If the embedding model fails to load, vector search is skipped and LLM responds from context alone.
- If the LLM model fails to load, the health endpoint reports `model_loaded: false` and chat endpoints return an error.
- If ChromaDB is corrupted or absent, the system recreates the database automatically.
- If a calculator receives invalid inputs, it returns a clear error message without crashing.

### 2.4 Concurrency Protection
- LLM inference is a blocking, single-threaded call to `llama-cpp-python`.
- Concurrent chat requests are queued (the second request waits for the first to complete).
- Non-LLM endpoints (health, metrics, calculators, knowledge stats) run in parallel without blocking.
- The embedding model can be called concurrently with LLM inference since it uses a separate model instance.

## 3. Data Protection

### 3.1 Knowledge Base Integrity
- ChromaDB uses persistent SQLite storage with transactional writes.
- Indexing operations are atomic per document; partial failures do not corrupt the collection.
- The `clear` endpoint truncates the collection and recreates it cleanly.

### 3.2 Conversation Privacy
- No conversation logs are persisted to disk (in-memory only during session).
- The response cache is in-memory and lost on server restart.
- Users who require privacy should restart the server between sessions to clear the cache.

### 3.3 Model File Security
- GGUF model files are read-only after download.
- No executable code is loaded from model files (llama-cpp-python loads weights only).
- The embedding model GGUF is similarly read-only.

## 4. Scalability Design

### 4.1 Current Architecture (Single-User)
- Single FastAPI process with uvicorn.
- Single LLM model instance loaded in memory.
- Single ChromaDB client connection.
- Maximum throughput: ~2.7 tokens/s on i5-12450H CPU.

### 4.2 Bottleneck Analysis

| Bottleneck | Current Capacity | Limitation |
|------------|-----------------|------------|
| LLM inference | ~2.7 tokens/s | CPU-bound, single-threaded inference |
| Knowledge retrieval | ~5 ms per query | ChromaDB cosine similarity scan |
| Calculator | ~2-15 ms per call | CPU-bound arithmetic |
| File upload/indexing | ~500 ms per document | Embedding generation |
| HTTP/ASGI overhead | ~50-100 ms per request | Uvicorn on Windows |

### 4.3 Scaling Strategies (Future)

#### 4.3.1 Vertical Scaling
- Upgrade CPU: Core i7/i9 with more cores and AVX512 support (up to 2x inference speedup).
- Increase RAM to 16 GB: Allows larger models (7B-13B) with better reasoning quality.
- NVMe SSD: Reduces model load time from ~5s to ~1s.

#### 4.3.2 Horizontal Scaling (Multi-User)
- Deploy behind Nginx reverse proxy for load balancing.
- Run multiple uvicorn workers behind a process manager.
- Each worker loads its own LLM model instance (RAM scales linearly).
- Use Redis for shared response cache across workers.

#### 4.3.3 Inference Optimization
- GPU acceleration (CUDA/Metal): 10-50x inference speedup.
- Model quantization (Q2_K): Reduces RAM but degrades quality.
- Speculative decoding: ~2x speedup with a draft model.
- KV-cache optimization: Reduces per-token computation.

#### 4.3.4 Knowledge Base Scaling
- Database partitioning: Split by engineering domain (civil, structural, environmental).
- Embedding caching: Avoid redundant embedding computations.
- Hybrid search: BM25 + vector search for improved retrieval.
- Incremental indexing: Index new documents without full re-index.

### 4.4 High-Availability Configuration (Future)

```
                      +---------+
                      |  Nginx  |
                      | :8432   |
                      +----+----+
                           |
              +------------+------------+
              |            |            |
         +----v---+  +----v---+  +----v---+
         | Worker |  | Worker |  | Worker |
         | 1:8433 |  | 2:8434 |  | 3:8435 |
         +--------+  +--------+  +--------+
              |            |            |
         +----v------------v------------v---+
         |         Redis Cache              |
         +----------------------------------+
              |            |
         +----v------------v----+
         |  ChromaDB (shared)   |
         +----------------------+
         |  Knowledge Files     |
         +----------------------+
```

## 5. Monitoring (Current)

### 5.1 Health Check
- `GET /api/v1/health`: Returns `status: "healthy"` and model load state.
- Non-LLM endpoints respond within ~50-100 ms, confirming server availability.
- If LLM model fails to load, health reports `model_loaded: false`.

### 5.2 Live Metrics
- `GET /api/v1/metrics`: Returns CPU%, RAM GB, model name, cache hits, cache misses, knowledge stats.
- Frontend displays these metrics in a real-time panel.
- No external monitoring integration (log-based only).

## 6. Backup and Recovery

- Knowledge base (ChromaDB) can be backed up by copying the `database/` directory.
- Model files can be re-downloaded from Hugging Face if corrupted.
- Configuration is stored in `config/settings.py` (back up this file).
- To recover from corruption: delete `database/` and re-index via `/api/v1/knowledge/index-all`.
