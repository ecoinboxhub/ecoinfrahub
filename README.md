# EcoInfraMind AI — ADTC 2026 Submission

Offline infrastructure and environmental engineering AI assistant for Africa.
Runs on CPU-only consumer hardware with no cloud dependencies.

## Submission Checklist

- [x] `model/.gitkeep` — model weight placeholder
- [x] `.gitignore` — excludes model files, caches, local profiler output
- [x] `LICENSE` — GNU General Public License v3
- [x] `README.md` — this file
- [x] `REPORT.md` — problem, design, constraints, benchmarks
- [x] `metadata.json` — ADTC competition metadata
- [x] `download_model.sh` — idempotent model download script

## Required Folder Structure

```
.
├── model/
│   └── .gitkeep
├── app/
├── config/
├── frontend/
├── knowledge/
├── tests/
├── utils/
├── .gitignore
├── LICENSE
├── README.md
├── REPORT.md
├── download_model.sh
├── metadata.json
├── run_api.py
├── requirements.txt
├── start.bat
└── demo.ps1
```

## metadata.json

Contains competition metadata:

```json
{
  "team_id": "team-ecoinfrahub",
  "email": "ibrahim5322022@gmail.com",
  "github_username": "ecoinboxhub",
  "model_name": "Qwen2.5-3B-Instruct",
  "model_path": "model/ecoinframind-ai-model.gguf",
  "runtime": "llama-cpp-python",
  "quantization": "Q4_K_M",
  "context_length": 4096,
  "max_tokens": 512,
  "test_prompts": [...]
}
```

Edit `metadata.json` with your actual team ID, email, and GitHub username before submission.

## download_model.sh

Downloads the GGUF model into `model/`:

```bash
bash download_model.sh
```

- Idempotent: skips download if file already exists
- Uses `curl` if available, falls back to `wget`
- Downloads to `model/ecoinframind-ai-model.gguf`
- Exits with error if both `curl` and `wget` are missing

## REPORT.md

Technical report covering:
- Problem statement and target users
- Design decisions and trade-offs
- Hardware and competition constraints
- Benchmarks (inference speed, memory usage, retrieval latency)

## Local Testing Instructions

### Prerequisites
- Python 3.12+
- 8 GB RAM
- Intel Core i5 or equivalent x86-64 CPU (AVX2 support)
- 4 GB free disk space

### Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\Activate       # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download model
bash download_model.sh

# 4. Index knowledge base
curl -X POST http://localhost:8432/api/v1/knowledge/index-all
```

### Run

```bash
python run_api.py
```

Open http://localhost:8432 in your browser.

### Run Tests

```bash
pytest tests/ -v
```

Test suite includes:
- 15 calculator unit tests
- 5 document processing tests
- 6 utility tests (cache, timer, monitor)
- 7 RAG engine tests
- 5 engine tests
- 5 embedding tests
- 6 assistant tests
- 11 API integration tests

### Run Demo Script

```bash
powershell -ExecutionPolicy Bypass -File demo.ps1
```

## Rules

- 100% offline — no cloud API calls
- CPU-only — no GPU required
- llama.cpp only for model inference (ADTC 2026 rule)
- All models in GGUF format
- No internet access at runtime

## Support

For issues or questions, open a GitHub issue or contact the development team.

## License

This project is licensed under the GNU General Public License v3.
See `LICENSE` for details.
