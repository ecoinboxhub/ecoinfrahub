# EcoInfraMind AI — Quick Start Guide

## Requirements

- Windows 10/11 64-bit
- Intel Core i5 or equivalent x86-64 CPU (AVX2 support required)
- 8 GB RAM (4 GB free after OS)
- 4 GB free disk space
- Python 3.12+
- Node.js 18+ (only needed for frontend development)

## Installation

### 1. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

Note: If you encounter an `0xc000001d` illegal instruction error when importing `llama-cpp-python`, rebuild it from source:

```powershell
set CMAKE_ARGS=-DLLAMA_NO_AVX512=ON -DLLAMA_AVX2=ON -DLLAMA_F16C=ON
pip install llama-cpp-python --no-cache-dir --force-reinstall --no-binary llama-cpp-python
```

### 2. Download the LLM Model

Place the GGUF model in the `model/` directory:

```powershell
mkdir -p model
# Download: ecoinframind-ai-model.gguf (~2.1 GB)
# from hugging face: Qwen/Qwen2.5-3B-Instruct-GGUF
```

### 3. Install Frontend Dependencies (Development)

```powershell
cd frontend
npm install
cd ..
```

## Running

### Production Mode (Recommended)

Double-click `start.bat` or run:

```powershell
python run_api.py
```

This launches the FastAPI server on port 8432, serving the pre-built frontend at `http://localhost:8432`.

### Development Mode (Frontend Hot Reload)

1. Start the backend:
   ```powershell
   python run_api.py
   ```

2. In another terminal, start the frontend dev server:
   ```powershell
   cd frontend
   npm run dev
   ```

3. Open `http://localhost:8501` in your browser.

## First-Time Setup

On first launch, the knowledge base is empty. Index the provided engineering documents:

1. Open the app in your browser.
2. The side panel shows status: Online, Model Loaded.
3. Knowledge stats will show 0 chunks if not yet indexed.
4. To index all documents, send a POST request:
   ```powershell
   curl -X POST http://localhost:8432/api/v1/knowledge/index-all
   ```
   This processes all files in `knowledge/` and populates the ChromaDB vector store.
5. After indexing, knowledge stats should show 104 chunks. You can now query engineering topics.

## Features

### Chat
- Type an engineering question and press Enter.
- Responses stream token-by-token with a progress bar showing tokens/sec.
- Conversation history is preserved within the session.
- Sources used for the response are shown as badges below each answer.

### Engineering Calculators
Click any calculator button in the sidebar to open the calculator panel.
- Concrete Mix Ratio
- Pavement Thickness (AASHTO)
- Drainage Flow (Rational Method)
- Bearing Capacity (Terzaghi)
- Traffic Volume / AADT
- Earthwork Volume
- Unit Conversion (length, area, volume, pressure, mass, temperature)
- Area / Volume calculations
- Slope calculation

### Expert Assistants
The system supports four expert modes (select via API):
- Engineering: General civil/structural/transportation
- Climate: Flood risk, drainage, sustainability
- Proposal: BOQs, method statements, risk registers
- Research: Papers, literature reviews, abstracts

### Document Upload
Upload your own documents to extend the knowledge base:
```powershell
curl -X POST http://localhost:8432/api/v1/upload -F "file=@document.pdf"
```

Supported formats: PDF, DOCX, TXT, MD.

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root info |
| `/api/v1/health` | GET | System health (model loaded, CPU%, RAM) |
| `/api/v1/chat` | POST | Non-streaming chat |
| `/api/v1/chat/stream` | POST | Streaming chat (SSE) |
| `/api/v1/expert` | POST | Expert assistant chat |
| `/api/v1/calculator` | POST | Engineering calculation |
| `/api/v1/experts` | GET | List available expert types |
| `/api/v1/knowledge/stats` | GET | Knowledge base statistics |
| `/api/v1/knowledge/clear` | POST | Clear knowledge base |
| `/api/v1/knowledge/index-all` | POST | Re-index all knowledge documents |
| `/api/v1/upload` | POST | Upload and index a document |
| `/api/v1/metrics` | GET | Detailed system metrics |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `0xc000001d` crash on import | Rebuild llama-cpp-python with `LLAMA_NO_AVX512=ON` |
| Knowledge base shows 0 chunks | Run `/api/v1/knowledge/index-all` via curl |
| Frontend shows "Connecting..." | Ensure `python run_api.py` is running on port 8432 |
| Server won't start / port in use | Change port in `config/settings.py` or kill the process on port 8432 |
| Out of memory | Reduce `n_ctx` in `config/settings.py` (e.g., to 512) |
| Model not loading | Verify `ecoinframind-ai-model.gguf` exists in `model/` |
| Slow responses | Expected: ~1.5-7 tokens/sec (20-120s per query) on Core i5 CPU |
| Blank responses | Check that max_tokens is sufficient in `config/settings.py` |
| CORS errors in browser console | The standard CORSMiddleware allows Vite dev-server origins (localhost:8501); production is same-origin on port 8432 |
| Chrome extension errors in console | Ignore `chrome-extension://invalid/` — these are from browser extensions |

## Keyboard Shortcuts

- Enter: Send message
- Shift+Enter: New line in input
- App runs in system tray when using the batch file

## Configuration

All tunable parameters are in `config/settings.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| n_ctx | 4096 | LLM context window size |
| max_tokens | 512 | Maximum response tokens |
| n_threads | 8 | CPU threads for LLM |
| temperature | 0.3 | Generation temperature (0-1) |
| chunk_size | 1500 | Document chunk size (characters) |
| max_retrieved | 5 | Documents retrieved per query |
| cache_ttl | 3600 | Response cache TTL (seconds) |
| api_port | 8432 | Server port |
