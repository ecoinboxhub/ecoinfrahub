# EcoInfraMind AI — Technical Report

## Problem

Infrastructure engineers across Africa face significant barriers to accessing technical knowledge and engineering computation tools. Rural and peri-urban projects in particular suffer from:

- Limited access to specialised engineering expertise
- High cost of commercial engineering software
- Unreliable or absent internet connectivity in remote areas
- Scarcity of localised technical reference materials (e.g., Nigerian Highway Manual, FERMA guidelines)
- Difficulty performing field calculations without specialised tools

**Target user (African context):** civil, highway, transportation, geotechnical, and environmental engineers; project managers preparing BOQs and method statements; field technicians needing quick on-site calculations; and engineering students or researchers. These users typically work on laptops with no GPU, limited RAM, and intermittent or no internet access.

**Solution:** EcoInfraMind AI is a fully offline, CPU-only AI assistant that delivers engineering knowledge retrieval, technical calculations, and expert-guided responses on any standard consumer laptop — no cloud, no GPU, no subscription.

## Design Decisions

### Base model
- **Qwen2.5-3B-Instruct Q4_K_M GGUF** is the foundation model. Qwen2.5-3B was chosen for its strong multilingual reasoning at 3B parameters, which is well suited to engineering tasks and to African-language technical terms.
- **Why Q4_K_M:** 4-bit quantization keeps the model at ~2.1 GB on disk and ~2.2–3.5 GB RAM during inference, comfortably inside the 8 GB budget while retaining good engineering reasoning quality. It is the standard CPU-efficient GGUF quantization.

### Alternatives evaluated
| Alternative | Why rejected |
|-------------|--------------|
| Phi-4 Mini (3.8B) | Excellent reasoning but not available as a stable GGUF at selection time |
| Qwen3-8B | Too much RAM for the 8 GB budget |
| Llama 3.2 3B | Comparable, but weaker multilingual support than Qwen2.5-3B |
| Gemma 3 2B | Faster but less engineering knowledge |
| TinyLlama 1.1B | Too small for reliable technical answers |
| Mistral 7B Q4 | ~5.5 GB RAM — too slow/heavy for an 8 GB CPU-only laptop |
| Fine-tuning | Rejected — no fine-tuning data, and hardware limits rule out training; inference-only of a pre-trained model is used instead |

### Architecture decisions
- **FastAPI** over Flask for native async/await, SSE streaming, and Pydantic validation
- **ChromaDB** over FAISS for persistent local vector storage with a simple API
- **llama-cpp-python** (llama.cpp) as the inference engine — required by the ADTC rule
- **React 18 + Vite 6** over Streamlit — reduces idle RAM by ~200 MB (50 MB vs 250 MB)
- Single-process **uvicorn**, static frontend served by the backend to eliminate CORS complexity

### RAG strategy
1. User question embedded via `all-MiniLM-L6-v2` (offline sentence-transformers)
2. ChromaDB retrieves top-k relevant chunks from indexed engineering documents
3. LLM receives system prompt + retrieved context + conversation history
4. Generates plain-text engineering response with source document badges

### Performance optimizations
| Optimization | Impact |
|-------------|--------|
| `orjson` for JSON serialization | ~1 us per response vs ~10 us (stdlib json) |
| Pre-load models at startup | Eliminates cold-start latency |
| Singleton embedding model | No reload penalty across requests |
| In-memory response cache (1h TTL) | Cache hits return in ~106ms |
| `n_ctx=4096` | Efficient context window for RAG prompts with history |
| `chunk_size=1500`, `chunk_overlap=128` | Balanced chunk size for meaningful retrieval |
| `len(text)//4` token counting | Eliminates ~1s overhead from llama-cpp-python tokenization |

## Constraints

### Hardware
| Component | Constraint | Actual Usage |
|-----------|------------|--------------|
| CPU | Intel Core i5 or equivalent x86-64 | i5-12450H, 8 threads (AVX2) |
| RAM | 8 GB total | Peak ~3.5 GB during inference |
| Storage | 4 GB free | ~2 GB (model) + ~100 MB (code) |
| GPU | None | Not required |
| Network | None at runtime | 100% offline |

### Connectivity
- No cloud APIs, no external model services, no telemetry
- All models loaded from local GGUF files in `model/`
- ChromaDB uses local SQLite persistence in `database/`
- Frontend served as static files from the backend
- No Python package index access at runtime

### Data
- Knowledge base limited to 46 local engineering documents (Markdown)
- No fine-tuning dataset; no OCR for scanned documents
- Indexed into 104 chunks via local embedding

### Competition (ADTC)
- llama.cpp only for model inference
- All models in GGUF format
- Maximum 8 GB RAM usage
- Single-file submission via GitHub

## Benchmarks

Measured on the development machine (Intel Core i5-12450H, 8 threads, n_ctx=4096, Qwen2.5-3B-Instruct Q4_K_M).

### Inference speed
| Metric | Value | Conditions |
|--------|-------|------------|
| Token generation | ~1.5-7 tok/s (~140-670ms/token) | 8 threads, n_ctx=4096, 3B model |
| Time to first token | 10-30s | Includes embedding + ChromaDB retrieval + 3B warmup |
| 50-token response | ~19-25s | Short prompts, no history |
| 300-token response | ~50-80s | Long prompts with RAG context |

### Memory usage
| Scenario | RAM | Notes |
|----------|-----|-------|
| Idle (both models loaded) | ~2.0 GB | 3B LLM + embedding resident |
| During inference | ~2.2-3.5 GB | Peak measured with 3B model |
| ChromaDB loaded | ~2.0 GB | With 104 indexed chunks |

### Endpoint latency
| Endpoint | Latency | Notes |
|----------|---------|-------|
| `GET /api/v1/health` | ~50-105ms | ASGI overhead floor on Windows |
| `GET /api/v1/metrics` | ~50-105ms | Same baseline |
| `GET /api/v1/knowledge/stats` | ~2.6ms | ChromaDB count query |
| `POST /api/v1/calculator` | ~2-15ms | CPU-bound arithmetic |
| `POST /api/v1/chat` (cache hit) | ~106ms | Identical query, HTTP round-trip only |
| `POST /api/v1/chat` (LLM) | 20-100s | Full inference with 3B model |

### Knowledge base
| Metric | Value |
|--------|-------|
| Source documents | 46 engineering files |
| Total chunks | 104 |
| Chunk size | 1500 characters |
| Chunk overlap | 128 characters |
| Embedding model | all-MiniLM-L6-v2 (sentence-transformers) |
| Vector database | ChromaDB (SQLite, cosine similarity) |
| Documents per retrieval | 5 |

### Tests
- **86/86 unit and integration tests pass** (pytest)
  - 15 calculator tests across all 11 calculators
  - 5 document processing tests
  - 6 utility tests (cache, timer, monitor)
  - 7 RAG pipeline tests
  - 6 assistant tests
  - 5 embedding tests
  - 5 engine tests
  - 11 API integration tests
- Integration verified end-to-end: health, streaming chat with RAG, expert modes, calculators, knowledge indexing and retrieval

## Known Gaps
- CPU-only inference is inherently slow (~1.5-7 tok/s for 3B model); no GPU alternative under ADTC rules
- No persistent conversation history (in-memory only, lost on restart)
- Single-user (LLM inference is blocking, concurrent requests queued)
- Windows ASGI overhead adds 50-105ms baseline per request
- No OCR for scanned PDFs