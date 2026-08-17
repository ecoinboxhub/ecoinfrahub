# EcoInfraMind AI — Technical Report

## Problem

Infrastructure engineers across Africa face significant barriers to accessing technical knowledge and engineering computation tools. Rural and peri-urban projects suffer from:

- Limited access to specialised engineering expertise
- High cost of commercial engineering software
- Unreliable or absent internet connectivity in remote areas
- Scarcity of localised technical reference materials (e.g., Nigerian Highway Manual, FERMA guidelines)
- Difficulty performing field calculations without specialised tools

EcoInfraMind AI addresses these challenges by providing a fully offline, CPU-only AI assistant that delivers engineering knowledge retrieval, technical calculations, and expert-guided responses on any standard consumer laptop.

## Design Decisions

### Architecture
- **FastAPI** over Flask for native async/await, SSE streaming, and Pydantic validation
- **ChromaDB** over FAISS for persistent local vector storage with simple API
- Single-process **uvicorn** adequate for single-user deployment
- Static frontend served by backend to eliminate CORS complexity

### LLM Strategy
- **Qwen2.5-3B-Instruct Q4_K_M GGUF** as the foundation model — strong multilingual reasoning with 3B parameters for engineering tasks (Q4_K_M quantization for CPU efficiency; fits within 8 GB RAM budget)
- **No fine-tuning** — inference-only of pre-trained model due to hardware constraints (8 GB RAM, CPU-only, no GPU)
- **RAG (Retrieval-Augmented Generation)** layers domain knowledge on top of the foundation model:
  1. User question embedded via `all-MiniLM-L6-v2` (offline sentence-transformers model)
  2. ChromaDB retrieves top-k relevant chunks from indexed engineering documents
  3. LLM receives system prompt + retrieved context + conversation history
  4. Generates plain-text engineering response with source document badges
- **len(text)//4** token counting eliminates ~1s overhead from llama-cpp-python tokenization

### Performance Optimizations
| Optimization | Impact |
|-------------|--------|
| `orjson` for JSON serialization | ~1 us per response vs ~10 us (stdlib json) |
| Pre-load models at startup | Eliminates cold-start latency |
| Singleton embedding model | No reload penalty across requests |
| In-memory response cache (1h TTL) | Cache hits return in ~106ms |
| `n_ctx=4096` | Efficient context window for RAG prompts with conversation history |
| `chunk_size=1500`, `chunk_overlap=128` | Balanced chunk size for meaningful retrieval |

### Frontend
- **React 18 + Vite 6** over Streamlit — reduces idle RAM by ~200 MB (50 MB vs 250 MB)
- SSE streaming for real-time token-by-token output
- Dark/light theme with localStorage persistence
- Source document badges with relevance percentage
- Live progress bar with tokens/sec throughput during generation

### Model Loading
- `llama-cpp-python` rebuilt from source with `LLAMA_NO_AVX512=ON` because prebuilt wheels use AVX512 instructions not supported by the Core i5-12450H CPU
- Both LLM and embedding models loaded at startup via FastAPI startup handler
- Embedding model uses `all-MiniLM-L6-v2` (offline sentence-transformers) — no internet auth required

### Output Format
All LLM responses are plain natural language:
- System prompt explicitly instructs no markdown, no emoji, no special characters
- Post-processing `clean_text()` function strips any remaining formatting as a safety layer
- Source documents retrieved are displayed as clickable badges with relevance scores

## Constraints

### Hardware
| Component | Constraint | Actual Usage |
|-----------|------------|--------------|
| CPU | Intel Core i5 or equivalent x86-64 | i5-12450H, 8 threads |
| RAM | 8 GB total | Peak ~3.5 GB during inference |
| Storage | 4 GB free | ~2 GB (model) + ~100 MB (code) |
| GPU | None | Not required |
| Network | None at runtime | 100% offline |

### Competition (ADTC 2026)
- llama.cpp only for model inference
- No cloud APIs or external model services
- All models in GGUF format
- Single-file submission via GitHub
- Maximum 8 GB RAM usage

### Offline Requirements
- All models loaded from local GGUF files in `model/`
- ChromaDB uses local SQLite persistence in `database/`
- No telemetry, analytics, or external API calls
- Frontend served as static files from the backend
- No Python package index access at runtime

## Benchmarks

### Inference Speed
| Metric | Value | Conditions |
|--------|-------|------------|
| Token generation | ~1.5-7 tok/s (~140-670ms/token) | i5-12450H, 8 threads, n_ctx=4096, 3B model |
| Time to first token | 10-30s | Includes embedding + ChromaDB retrieval + 3B model warmup |
| 50-token response | ~19-25s | Short prompts, no history |
| 300-token response | ~50-80s | Long prompts with RAG context |

### Memory Usage
| Scenario | RAM | Notes |
|----------|-----|-------|
| Idle (both models loaded) | ~2.0 GB | 3B LLM + embedding resident |
| During inference | ~2.2-3.5 GB | Peak measured with 3B model |
| ChromaDB loaded | ~2.0 GB | With 104 indexed chunks |

### Endpoint Latency
| Endpoint | Latency | Notes |
|----------|---------|-------|
| `GET /api/v1/health` | ~50-105ms | ASGI overhead floor on Windows |
| `GET /api/v1/metrics` | ~50-105ms | Same baseline |
| `GET /api/v1/knowledge/stats` | ~2.6ms | ChromaDB count query |
| `POST /api/v1/calculator` | ~2-15ms | CPU-bound arithmetic |
| `POST /api/v1/chat` (cache hit) | ~106ms | Identical query, HTTP round-trip only |
| `POST /api/v1/chat` (LLM) | 20-100s | Full inference with 3B model |

### Knowledge Base
| Metric | Value |
|--------|-------|
| Source documents | 46 engineering files |
| Total chunks | 104 |
| Chunk size | 1500 characters |
| Chunk overlap | 128 characters |
| Embedding model | all-MiniLM-L6-v2 (sentence-transformers) |
| Vector database | ChromaDB (SQLite, cosine similarity) |
| Documents per retrieval | 5 |

### Calculator Tests
All 15 calculator unit tests pass across 11 calculators:
- Concrete mix, traffic volume, AADT, pavement thickness, earthwork, drainage, unit conversion, bearing capacity, area, volume, slope

### Unit Tests
60/60 tests pass (pytest):
- 15 calculator tests
- 5 document processing tests
- 6 utility tests (cache, timer, monitor)
- 7 RAG pipeline tests
- 6 assistant tests
- 5 embedding tests
- 5 engine tests
- 11 API integration tests

### Integration Tests
- API health endpoint returns model status
- Chat endpoint streams responses with RAG context
- Expert endpoint generates domain-specific responses
- Calculator endpoint performs engineering calculations
- Knowledge base indexing and retrieval works end-to-end

## Known Gaps
- CPU-only inference is inherently slow (~1.5-7 tok/s for 3B model); no GPU alternative under ADTC rules
- No persistent conversation history (in-memory only, lost on restart)
- Single-user (LLM inference is blocking, concurrent requests queued)
- Windows ASGI overhead adds 50-105ms baseline per request
- 3B model requires ~2.2-3.5GB RAM during inference (within 8GB constraint, leaves ample headroom)
