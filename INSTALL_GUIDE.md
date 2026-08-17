# EcoInfraMind AI — Installation Guide

Step-by-step instructions to install and run EcoInfraMind AI on your PC from GitHub.

## Prerequisites

1. **Windows 10/11** (64-bit)
2. **Python 3.12+** — tick "Add to PATH" during installation
3. **Node.js 18+**
4. **Intel Core i5** or equivalent x86-64 CPU with **AVX2 support** (required)
5. **8 GB RAM**
6. **4 GB free disk space**

## Step 1 — Get the code

Open Command Prompt or PowerShell:

```
git clone https://github.com/ecoinboxhub/ecoinfrahub.git
cd ecoinfrahub
```

## Step 2 — Set up Python

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

If the app crashes with **`0xc000001d`** on startup, your CPU lacks AVX512 — rebuild the library:

```
set CMAKE_ARGS=-DLLAMA_NO_AVX512=ON -DLLAMA_AVX2=ON -DLLAMA_F16C=ON
pip install llama-cpp-python --no-cache-dir --force-reinstall --no-binary llama-cpp-python
```

## Step 3 — Download the model (~2 GB)

The model file is not stored on GitHub, so create the folder and add it:

```
mkdir model
curl -L -o model\ecoinframind-ai-model.gguf https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf
```

> Prefer the app's own script? If Git Bash is installed: `bash download_model.sh` (it creates `model/` automatically).

## Step 4 — Build the web interface

The built frontend is not on GitHub either, so build it once:

```
cd frontend
npm install
npm run build
cd ..
```

## Step 5 — Start the app

```
python run_api.py
```

## Step 6 — Open it

Go to **http://localhost:8432** in your browser. The sidebar should show **Online · Model Loaded**.

## Step 7 — Load the knowledge base (first time only)

```
curl -X POST http://localhost:8432/api/v1/knowledge/index-all
```

The sidebar should show **104 chunks**.

## Done

Ask engineering questions in the chat (answers stream in with source badges), or use the 11 calculators in the sidebar.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `0xc000001d` crash on import | Rebuild `llama-cpp-python` with `LLAMA_NO_AVX512=ON` (Step 2) |
| Knowledge base shows 0 chunks | Run `/api/v1/knowledge/index-all` via curl (Step 7) |
| Frontend shows "Connecting..." | Ensure `python run_api.py` is running on port 8432 |
| Model not loading | Verify `ecoinframind-ai-model.gguf` exists in `model/` |
| Out of memory | Reduce `n_ctx` in `config/settings.py` (e.g., to 512) |
| Port 8432 already in use | Change port in `config/settings.py` or kill the process using it |
| Slow responses | Expected: ~1.5-7 tokens/sec (20-120s per query) on Core i5 CPU |