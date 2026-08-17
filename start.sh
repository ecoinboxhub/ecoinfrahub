#!/usr/bin/env bash
set -euo pipefail

# EcoInfraMind AI - Bash Setup & Launch
# Run: bash start.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  EcoInfraMind AI - Setup & Launch${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}ERROR: Python not found. Install Python 3.12+.${NC}"
    exit 1
fi
PY=$(command -v python3 || command -v python)

# Check Node
if ! command -v node &> /dev/null; then
    echo -e "${RED}ERROR: Node.js not found. Install Node.js 18+.${NC}"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    $PY -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt -q

# Download model if not present
MODEL="model/ecoinframind-ai-model.gguf"
if [ ! -f "$MODEL" ]; then
    echo ""
    echo -e "${YELLOW}Downloading model (~2 GB)...${NC}"
    if [ -f "download_model.sh" ]; then
        bash download_model.sh
    else
        echo -e "${YELLOW}WARNING: download_model.sh not found. Download model manually.${NC}"
        echo -e "${YELLOW}Place qwen2.5-3b-instruct-q4_k_m.gguf in model/${NC}"
    fi
fi

# Install frontend dependencies
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    cd frontend
    npm install --silent
    cd ..
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Starting EcoInfraMind AI...${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Start backend
echo -e "${GREEN}Starting backend on port 8432...${NC}"
python run_api.py &
BACKEND_PID=$!

# Wait for backend
echo -e "${YELLOW}Waiting for backend to initialize...${NC}"
sleep 12

# Start frontend
echo -e "${GREEN}Starting frontend on port 8501...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}  EcoInfraMind AI is running!${NC}"
echo ""
echo -e "  Frontend:  http://localhost:8501"
echo -e "  Backend:   http://localhost:8432"
echo -e "  API Docs:  http://localhost:8432/docs"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "Press Ctrl+C to stop both servers."

# Trap Ctrl+C to kill both processes
trap "echo ''; echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

wait
