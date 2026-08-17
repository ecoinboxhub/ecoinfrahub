# Product Requirements Document — EcoInfraMind AI

## 1. Product Overview

EcoInfraMind AI is an offline, CPU-only artificial intelligence assistant for infrastructure and environmental engineering professionals in Africa. It provides engineering knowledge retrieval, technical calculations, and expert-guided responses using a locally hosted large language model with retrieval-augmented generation.

## 2. Problem Statement

Rural and peri-urban infrastructure projects in Africa face critical challenges: limited access to specialised engineering expertise, high cost of commercial engineering software, unreliable internet connectivity in remote areas, and insufficient localised technical reference materials. Engineers and technicians in the field require immediate access to engineering knowledge, standards, and computational tools without dependence on cloud services.

## 3. Target Users

- Civil and highway engineers working on rural road projects
- Environmental and sustainability consultants conducting EIAs
- Project managers preparing proposals and technical documents
- Engineering students and researchers in African universities
- Government agencies and contractors managing infrastructure projects
- Field technicians requiring quick reference calculations

## 4. Core Requirements

### 4.1 Functional Requirements

| ID | Requirement | Priority | Status |
|----|------------|----------|--------|
| F1 | Chat-based Q&A with LLM on engineering topics | P0 | Done |
| F2 | Retrieval-augmented generation from local knowledge base | P0 | Done |
| F3 | Streaming token-by-token responses | P0 | Done |
| F4 | Expert assistant modes (engineering, climate, proposal, research) | P1 | Done |
| F5 | Conversation history and context memory | P1 | Done |
| F6 | Engineering calculators (11 types) | P1 | Done |
| F7 | Document upload and indexing (PDF, DOCX, TXT, MD) | P1 | Done |
| F8 | Knowledge base management (view stats, clear, re-index) | P2 | Done |
| F9 | System health monitoring (CPU, RAM, model status) | P2 | Done |
| F10 | Response caching for repeated queries | P2 | Done |
| F11 | Plain text output without markdown or special characters | P1 | Done |
| F12 | Web-based user interface (React) | P0 | Done |
| F13 | REST API for third-party integration | P1 | Done |
| F14 | Pre-loading of LLM and embedding models at startup | P1 | Done |

### 4.2 Non-Functional Requirements

| ID | Requirement | Target | Status |
|----|------------|--------|--------|
| N1 | 100% offline operation after initial installation | No cloud calls | Done |
| N2 | CPU-only inference (no GPU required) | Core i5-12450H | Done |
| N3 | RAM usage under 6 GB during inference | Peak ~3.5 GB | Done |
| N4 | Response time under 120 seconds for typical queries | 19-80s | Done |
| N5 | Knowledge base capacity of 100+ indexed chunks | 104 chunks | Done |
| N6 | Support for concurrent users (local) | Single-user | Done |
| N7 | Plain text output (no emoji, markdown, or special chars) | All responses | Done |

## 5. Hardware Constraints

- Processor: Intel Core i5-12450H or equivalent x86-64 CPU
- RAM: 8 GB DDR4 (minimum), 16 GB recommended
- Storage: 4 GB free space (model + knowledge base + application)
- GPU: None required
- Network: None required after initial setup
- OS: Windows 10/11 64-bit

## 6. Software Dependencies

- Python 3.12+
- llama-cpp-python (CPU build, no AVX512)
- ChromaDB (local vector database)
- FastAPI + uvicorn (API server)
- Qwen2.5-3B-Instruct Q4_K_M GGUF model
- all-MiniLM-L6-v2 embedding model
- React 18 + Vite 6 (frontend)
- Node.js 18+ (frontend build tooling)

## 7. Use Cases

### UC1: Engineering Q&A
Engineer asks a technical question about road pavement design. System retrieves relevant context from knowledge base, augments the LLM prompt, and generates a detailed response referencing applicable standards.

### UC2: Environmental Impact Assessment
Consultant requests an EIA outline for a rural road project. System engages the proposal expert assistant to generate a structured EIA with all required sections.

### UC3: Technical Calculations
Field technician uses the built-in calculators for concrete mix design, pavement thickness, drainage flow, or bearing capacity without needing internet access.

### UC4: Document Research
User uploads a technical PDF. System processes and indexes the document into the knowledge base, making it retrievable for future queries.

## 8. Success Metrics

- Query response under 90 seconds for 90% of requests
- RAM consumption under 4 GB during normal operation
- Knowledge base accuracy (retrieved context relevance) above 80%
- Zero cloud API calls during operation
- All 60 unit tests passing
- Frontend page load under 3 seconds
