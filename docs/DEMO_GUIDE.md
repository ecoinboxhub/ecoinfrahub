# EcoInfraMind AI — Competition Demo Guide (ADTC 2026)

## Purpose
This document describes how to present EcoInfraMind AI to judges at the Africa Deep Tech Challenge. Follow the script sequentially for a 20-minute demonstration.

## Requirements Before Demo

1. Server running on port 8432:
   ```powershell
   python run_api.py
   ```
2. Knowledge base indexed:
   ```powershell
   curl -X POST http://localhost:8432/api/v1/knowledge/index-all
   ```
3. Browser open to `http://localhost:8432`

## Live Demo Script (Judges)

### Part 1: System Overview (2 min)
Show the browser window. Point out:
- **Sidebar**: Status indicator (green = online, model loaded), calculator buttons, metrics panel
- **Chat area**: Clean interface, type your question, streaming responses
- **Theme toggle**: Click the sun/moon icon in the sidebar header to switch light/dark mode

### Part 2: Engineering Q&A (10 min)
Ask 3-4 questions from the benchmark set, demonstrating:
- **Streaming**: Tokens appear one by one with a progress bar showing tokens/sec
- **Sources**: Source document badges appear below each answer
- **Context memory**: Follow-up questions retain conversation context
- **Calculator**: Open a calculator (e.g., Pavement Thickness), enter values, see instant result

Suggested demo questions (choose based on judge interest):

| Question | Domain | What to Highlight |
|----------|--------|-------------------|
| "What is the standard pavement structure for a rural road in Nigeria?" | Highway Engineering | Knowledge base retrieval, source badges |
| "Explain the Rational Method for stormwater drainage design" | Drainage Engineering | Technical accuracy, formula explanation |
| "What climate adaptation measures should be considered for roads in flood-prone areas?" | Climate Adaptation | Cross-domain knowledge, practical recommendations |
| "Calculate the pavement thickness for CBR=15, traffic ESA=5,000,000, reliability=90%" | Calculator | Instant computation, no internet needed |

### Part 3: Document Upload (3 min)
1. Show the upload endpoint in action:
   ```powershell
   curl -X POST http://localhost:8432/api/v1/upload -F "file=@knowledge/01_nigerian_highway_manual.md"
   ```
2. Ask a question about the uploaded content
3. Point out the knowledge stats increment in the sidebar

### Part 4: Technical Deep Dive (3 min)
Discuss architecture highlights:
- 100% offline: No cloud calls, all models local
- CPU-only: Runs on any Core i5 laptop, no GPU needed
- RAM: Peak ~3.5 GB, well under the 6 GB competition limit
- Speed: ~1.5-7 tokens/sec on i5-12450H, ~20-120s for detailed answers
- Knowledge base: 104 chunks from 46 engineering documents

### Part 5: Code Walkthrough (2 min)
Quickly show key files:
- `app/backend/rag.py` — RAG pipeline (retrieval, context building, prompt formatting)
- `app/backend/engine.py` — LLM wrapper (single model instance, streaming generation)
- `app/api/routes.py` — 18 API endpoints including SSE streaming
- `frontend/src/App.jsx` — Chat UI with real-time streaming display

## Automated Demo Script

To run the full automated benchmark:
```powershell
powershell -ExecutionPolicy Bypass -File demo.ps1
```

This executes:
- System health verification
- 10 engineering benchmark questions
- 5 calculator validation tests
- Expert assistant mode test
- Cache performance test

Expected duration: ~15 minutes for all 10 questions.

## Scoring Metrics for Judges

| Metric | Measurement | Target |
|--------|-------------|--------|
| Response quality | Keyword coverage in 10 questions | 6/10 keywords per question |
| Response length | Tokens per response | 50+ tokens per answer |
| Response time | Seconds per query | Under 180s per query |
| RAM usage | GB during inference | Under 4 GB |
| Calculator accuracy | Correct results for 5 tests | 100% pass rate |
| Offline operation | No internet calls | 100% verified |

## Troubleshooting During Demo

| Issue | Recovery |
|-------|----------|
| Server not responding | Run `python run_api.py` in a new terminal |
| Empty responses | Check `config/settings.py` max_tokens=512, n_ctx=4096 |
| Model not loading | Verify `model/ecoinframind-ai-model.gguf` exists |
| Knowledge base empty | Run `/api/v1/knowledge/index-all` via curl or browser |
| Browser shows blank page | Clear browser cache, reload at `http://localhost:8432` |
