# Software Requirements Specification — EcoInfraMind AI

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for EcoInfraMind AI, an offline engineering intelligence assistant delivering LLM-powered Q&A, RAG-based knowledge retrieval, and engineering calculations on consumer-grade CPU hardware.

### 1.2 Scope
The system comprises a Python/FastAPI backend serving REST and SSE streaming endpoints, a React/Vite frontend, a local vector database (ChromaDB), and a locally hosted LLM (Qwen2.5-3B) with an embedding model.

### 1.3 Definitions
- LLM: Large Language Model
- RAG: Retrieval-Augmented Generation
- SSE: Server-Sent Events
- GGUF: GPT-Generated Unified Format (model file format)
- ChromaDB: Open-source vector database
- EIA: Environmental Impact Assessment

## 2. System Architecture

The system follows a three-tier architecture:
- Presentation Tier: React+Vite browser application
- Application Tier: FastAPI backend with RAG and LLM engines
- Data Tier: ChromaDB vector store and local file system

## 3. Software Interfaces

### 3.1 API Endpoints

#### 3.1.1 System Endpoints

| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| `/` | GET | Root info | None | `{app, version, docs}` |
| `/api/v1/health` | GET | System health | None | `{status, model_loaded, cpu_percent, ram_gb}` |
| `/api/v1/metrics` | GET | Detailed metrics | None | `{cpu, ram, model, cache, knowledge}` |

#### 3.1.2 Chat Endpoints

| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| `/api/v1/chat` | POST | Non-streaming chat | `{message, history}` | `{response, tokens, cpu, ram, time}` |
| `/api/v1/chat/stream` | POST | Streaming chat (SSE) | `{message, history}` | SSE stream of `{token}` + `{meta}` + `[DONE]` |
| `/api/v1/expert` | POST | Expert-assistant chat | `{message, expert_type, history}` | `{response, expert_type, tokens, ...}` |

#### 3.1.3 Knowledge Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/knowledge/stats` | GET | Retrieve knowledge base statistics |
| `/api/v1/knowledge/clear` | POST | Clear the entire knowledge base |
| `/api/v1/knowledge/index-all` | POST | Re-index all documents from knowledge directory |
| `/api/v1/upload` | POST | Upload and index a new document |

#### 3.1.4 Calculator Endpoint

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/calculator` | POST | Execute an engineering calculation |

Supported calculators: concrete_mix, traffic_volume, aadt, pavement_thickness, earthwork, drainage, unit_conversion, bearing_capacity, area, volume, slope.

#### 3.1.5 Expert Endpoint

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/experts` | GET | List all available expert assistant types |

Expert types: engineering, climate, proposal, research.

### 3.2 Streaming Protocol
The `/api/v1/chat/stream` endpoint uses Server-Sent Events (SSE):
- Each token is sent as `data: {"token": "<text>"}\n\n`
- A heartbeat `data: {"status": "generating"}\n\n` is sent during LLM inference wait
- On completion: `data: {"meta": {"tokens": N, "time": T, "cpu": C, "ram": R}}\n\n`
- Final event: `data: [DONE]\n\n`

### 3.3 Data Formats
- All JSON serialization uses `orjson` (~1 us per response)
- Text output is cleaned of markdown formatting (`#`, `**`, `*`) via regex post-processing
- Timestamps are ISO 8601 format
- Numeric values use SI units throughout

## 4. Functional Modules

### 4.1 LLM Engine (app/backend/engine.py)
- Singleton pattern ensures single model instance
- Loads Qwen2.5-3B-Instruct Q4_K_M GGUF at startup
- Uses llama-cpp-python for inference
- Supports streaming and non-streaming generation
- Token counting: `len(text) // 4` estimation
- Stop tokens: `<|im_end|>`, `<|endoftext|>`

### 4.2 Embedding Engine (app/backend/embeddings.py)
- Primary: all-MiniLM-L6-v2
- Fallback: all-MiniLM-L6-v2
- Singleton with lazy loading
- Supports single and batch embedding

### 4.3 RAG Engine (app/backend/rag.py)
- ChromaDB with cosine similarity search
- Retrieval: top-K documents (K=6, rerank top 5)
- Context building from retrieved chunks
- ChatML prompt formatting (`<|im_start|>system|user|assistant`)
- Response caching (TTL: 1 hour)
- Conversation memory: last 4 messages

### 4.4 Document Processor (app/backend/documents.py)
- Supported formats: PDF, DOCX, TXT, MD
- Chunk size: 1500 characters, overlap: 128 characters
- Text cleaning and normalization

### 4.5 Calculators (app/backend/calculators.py)
11 engineering calculators with input validation.
- Concrete mix ratio calculation
- Traffic volume estimation
- Annual Average Daily Traffic (AADT)
- Pavement thickness (AASHTO method)
- Earthwork volume with swell factor
- Drainage flow (Rational method)
- Unit conversion (length, area, volume, pressure, mass, temperature)
- Bearing capacity (Terzaghi method)
- Area and volume calculations
- Slope calculation

### 4.6 Expert Assistants (app/backend/assistants.py)
Four specialized assistants with tailored system prompts:
- Engineering: Civil, structural, transportation, geotechnical
- Climate: Flood risk, drainage, sustainability
- Proposal: BOQs, method statements, risk registers
- Research: Papers, literature reviews, abstracts

### 4.7 Frontend (frontend/src/App.jsx)
- React 18 with functional components and hooks
- Chat interface with streaming token display
- Calculator panel with form inputs
- Live system metrics (CPU, RAM, model status)
- Auto-scroll on new messages
- CORS client connecting to port 8432

## 5. Performance Requirements

| Metric | Requirement | Measured |
|--------|-------------|----------|
| LLM time-to-first-token | < 30s | 10-25s |
| Average throughput | > 2 tokens/s | ~1.5-7 tokens/s |
| Knowledge retrieval | < 500ms | ~5ms |
| Calculator response | < 500ms | ~2-15ms |
| Non-LLM endpoint latency | < 200ms | ~50-105ms |
| Frontend initial load | < 5s | ~2s |
| API payload serialization | < 5ms | ~1us |

## 6. Configuration Parameters

All configurable via `config/settings.py`:
- n_ctx: 4096 (context window size)
- max_tokens: 512 (maximum generation length)
- n_threads: 8 (CPU threads for LLM)
- temperature: 0.3 (generation temperature)
- chunk_size: 1500 (document chunk size)
- max_retrieved: 5 (retrieved documents per query)
- cache_ttl: 3600 (response cache TTL in seconds)
- max_ram_gb: 5.5 (RAM usage limit)
- api_port: 8432 (server port)

## 7. Test Requirements

- Unit tests: 60 test cases across calculators, documents, utilities, RAG, engine, embeddings, assistants, and API
- Test framework: pytest
- All tests pass before release
- No external dependencies during testing
