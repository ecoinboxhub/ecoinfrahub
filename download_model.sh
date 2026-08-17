#!/usr/bin/env bash
set -euo pipefail

# download_model.sh — Idempotent model download for ADTC 2026 submission
#
# Downloads Qwen2.5-3B-Instruct Q4_K_M GGUF into model/
# Skips if file already exists.
# Uses curl if available, falls back to wget.

MODEL_DIR="model"
MODEL_FILE="ecoinframind-ai-model.gguf"
MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf"

mkdir -p "$MODEL_DIR"

TARGET="$MODEL_DIR/$MODEL_FILE"

if [ -f "$TARGET" ]; then
    echo "Model already exists at $TARGET — skipping download."
    exit 0
fi

echo "Downloading $MODEL_FILE to $MODEL_DIR/ ..."

if command -v curl &> /dev/null; then
    echo "Using curl"
    curl -L -o "$TARGET" "$MODEL_URL"
elif command -v wget &> /dev/null; then
    echo "Using wget"
    wget -O "$TARGET" "$MODEL_URL"
else
    echo "Error: Neither curl nor wget found. Install one of them and try again." >&2
    exit 1
fi

echo "Download complete: $TARGET"
ls -lh "$TARGET"
