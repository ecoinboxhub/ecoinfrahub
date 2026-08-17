# System Architecture — EcoInfraMind AI

## 1. High-Level Architecture

```
+------------------------------------------------------------------+
|                        USER BROWSER                               |
|              React 18 + Vite 6 (port 8501)                        |
|           Chat UI / Calculator / Metrics Panel                    |
+-------------------------------|----------------------------------+
                                | HTTP/SSE
                                | localhost:8432
+-------------------------------|----------------------------------+
|                       FASTAPI SERVER (uvicorn)                     |
|                              port 8432                             |
|                                                                    |
|  +------------------+  +------------------+  +------------------+  |
|  |  REST Endpoints  |  |  SSE Streaming   |  |  Static Files    |  |
|  |  /api/v1/*       |  |  /chat/stream    |  |  (built React)   |  |
|  +--------+---------+  +--------+---------+  +--------+---------+  |
|           |                     |                       |           |
|  +--------v---------------------v-----------------------v---------+ |
|  |                    ROUTING LAYER (routes.py)                    | |
|  |          orjson serialization, clean_text(), CORS              | |
|  +--------+---------------------+------------------+--------------+ |
|           |                     |                  |                |
|  +--------v--------+   +--------v--------+   +-----v----------+    |
|  |   LLM ENGINE    |   |  EMBEDDING      |   |   CALCULATORS  |    |
|  |  (engine.py)    |   |  ENGINE         |   |  (calculators  |    |
|  |  Qwen2.5-3B     |   |  (embeddings.py)|   |   .py)         |    |
|  |  llama-cpp      |   |  MiniLM-L6-v2   |   |  11 calculators|    |
|  +--------+--------+   +--------+--------+   +-------+--------+    |
|           |                     |                     |             |
|  +--------v---------------------v---------------------v----------+ |
|  |                    RAG PIPELINE (rag.py)                        | |
|  |   Prompt formatting, context retrieval, cache, assistants      | |
|  +-------------------------------+-------------------------------+ |
|                                  |                                 |
|  +-------------------------------v-------------------------------+ |
|  |                    CHROMADB VECTOR STORE                        | |
|  |           Collection: ecoinframind_knowledge                    | |
|  |           313 chunks indexed, cosine similarity                 | |
|  +---------------------------------------------------------------+ |
|                                  |                                 |
|  +-------------------------------v-------------------------------+ |
|  |                    KNOWLEDGE DIRECTORY (knowledge/)            | |
|  |           36 engineering documents (PDF, DOCX, TXT, MD)       | |
|  +---------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

## 2. Component Descriptions

### 2.1 Frontend (React 18 + Vite 6)
- **Location**: `frontend/`
- **Port**: 8501 (Vite dev server or production build served by FastAPI)
- **Key files**: `App.jsx`, `api.js`
- **State management**: React useState hooks
- **Streaming**: EventSource-like SSE consumption via fetch + ReadableStream
- **Build output**: Static files served from FastAPI `/` root

### 2.2 API Layer (FastAPI)
- **Location**: `app/api/main.py`, `app/api/routes.py`
- **Port**: 8432
- **18 endpoints** covering chat, streaming, knowledge, calculators, metrics
- **CORS**: Custom `@app.middleware("http")` adding headers to all responses
- **Serialization**: `orjson.dumps()` for sub-millisecond payload generation
- **Startup**: Pre-loads LLM and embedding models in lifespan handler

### 2.3 LLM Engine
- **Location**: `app/backend/engine.py`
- **Model**: `qwen2.5-3b-instruct-q4_k_m.gguf` (1.96 GB)
- **Framework**: `llama-cpp-python` (CPU build, no AVX512)
- **Parameters**: n_ctx=1024, max_tokens=768, n_threads=8, temperature=0.5
- **Performance**: ~375 ms/token, ~2.7 tokens/s on Core i5-12450H
- **Singleton**: Single instance loaded at startup, persistent across requests

### 2.4 Embedding Engine
- **Location**: `app/backend/embeddings.py`
- **Primary model**: all-MiniLM-L6-v2 (sentence-transformers)
- **Lazy loading**: Loads on first embedding request, persists thereafter

### 2.5 RAG Pipeline
- **Location**: `app/backend/rag.py`
- **Retrieval**: ChromaDB cosine similarity search, top-K=6, rerank top 5
- **Context limit**: 600 characters from retrieved chunks
- **Memory**: Last 4 messages preserved in conversation history
- **Cache**: In-memory response cache with 1-hour TTL
- **Prompt format**: ChatML (`<|im_start|>`, `<|im_end|>`)

### 2.6 Vector Store
- **Database**: ChromaDB with SQLite backend
- **Location**: `database/`
- **Collection**: `ecoinframind_knowledge`
- **Capacity**: 313 chunks from 36 source documents
- **Chunking**: 256 characters with 32-character overlap

### 2.7 Calculators Module
- **Location**: `app/backend/calculators.py`
- **10 calculators**: concrete_mix, traffic_volume, aadt, pavement_thickness, earthwork, drainage, unit_conversion, bearing_capacity, area, volume, slope
- **Input validation**: Pydantic-style manual validation
- **Response time**: 2-15ms per calculation

### 2.8 Expert Assistants
- **Location**: `app/backend/assistants.py`
- **4 modes**: engineering, climate, proposal, research
- Each mode has a dedicated system prompt stored in the module
- Selected via the `expert_type` parameter in `/api/v1/expert`

## 3. Data Flow Diagrams

### 3.1 Chat Flow (Streaming)
```
User Message
    |
    v
POST /api/v1/chat/stream {message, history}
    |
    v
routes.py receives request
    |
    v
rag.py formats prompt with:
  - System prompt (plain-text instruction)
  - Conversation history (last 4 messages)
  - Retrieved context from ChromaDB (top 2 chunks)
  - User query
    |
    v
engine.py generates tokens via llama-cpp-python
    |
    v
SSE stream: {token} -> {token} -> ... -> {meta} -> [DONE]
    |
    v
Frontend renders tokens progressively with auto-scroll
```

### 3.2 Knowledge Upload Flow
```
User uploads file (PDF/DOCX/TXT/MD)
    |
    v
POST /api/v1/upload (multipart form)
    |
    v
documents.py processes file:
  - PDF: PyMuPDF extraction
  - DOCX: python-docx extraction
  - TXT/MD: direct text read
    |
    v
chunk_text() splits into 256-char chunks with 32-char overlap
    |
    v
Embedding engine generates vectors for each chunk
    |
    v
ChromaDB stores chunk text + vectors + metadata (source, page)
    |
    v
Response: {status: "indexed", chunks: N, document: name}
```

### 3.3 Calculator Flow
```
User selects calculator type and inputs parameters
    |
    v
POST /api/v1/calculator {calculator: "pavement_thickness", params: {...}}
    |
    v
routes.py routes to calculators.py based on type
    |
    v
Calculator function validates inputs and computes result
    |
    v
Response: {result: value, unit: "mm", params: {...}}
    |
    v
Frontend displays formatted result
```

## 4. Deployment Architecture

### 4.1 Directory Structure
```
EcoInfraMind-AI/
  app/
    __init__.py
    api/
      main.py          # FastAPI app, lifespan, CORS, model loading
      routes.py         # All 18 endpoints
    backend/
      __init__.py
      engine.py         # LLM wrapper (Qwen2.5-3B)
      embeddings.py     # Embedding model wrapper
      rag.py            # RAG pipeline (retrieval, prompt, cache)
      assistants.py     # Expert assistant prompts
      calculators.py    # 10 engineering calculators
      documents.py      # File processing, chunking, indexing
  config/
    settings.py         # All tunable parameters
  knowledge/            # 36 source documents
  database/             # ChromaDB persistent storage
  frontend/             # React source code
    src/
      App.jsx           # Main chat UI
      api.js            # API client with SSE streaming
  tests/
    test_calculators.py # 15 unit tests
  docs/                 # Documentation
  run_api.py            # Application entry point
  start.bat
  status.md
```

### 4.2 Startup Sequence
1. `run_api.py` launches `uvicorn` with `app.api.main:app`
2. FastAPI lifespan handler loads LLM model into memory
3. FastAPI lifespan handler sets up ChromaDB connection
4. Server begins listening on port 8432
5. Frontend (production build) is served as static files or run via Vite

### 4.3 Memory Allocation (peak ~3.5 GB)
- LLM model (Qwen2.5-3B Q4_K_M): ~2.1 GB
- Embedding model (all-MiniLM-L6-v2): ~0.4 GB
- ChromaDB + cache: ~0.3 GB
- Python runtime + dependencies: ~0.4 GB
- OS and other overhead: ~0.15 GB
