# EcoInfraMind AI - PowerShell Setup & Launch
# Run: .\start.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EcoInfraMind AI - Setup & Launch" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python not found. Install Python 3.12+ and add to PATH." -ForegroundColor Red
    exit 1
}

# Check Node
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Node.js not found. Install Node.js 18+ and add to PATH." -ForegroundColor Red
    exit 1
}

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate venv
& "$Root\venv\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q

# Download model if not present
$modelPath = "model\ecoinframind-ai-model.gguf"
if (-not (Test-Path $modelPath)) {
    Write-Host ""
    Write-Host "Downloading model (~2 GB)..." -ForegroundColor Yellow
    if (Test-Path "download_model.sh") {
        bash download_model.sh
    } else {
        Write-Host "WARNING: download_model.sh not found. Download model manually." -ForegroundColor Yellow
        Write-Host "Place qwen2.5-3b-instruct-q4_k_m.gguf in model/" -ForegroundColor Yellow
    }
}

# Install frontend dependencies
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location frontend
    npm install --silent
    Pop-Location
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting EcoInfraMind AI..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start backend
Write-Host "Starting backend on port 8432..." -ForegroundColor Green
Start-Process -FilePath "cmd" -ArgumentList "/k", "title EcoInfraMind-Backend && venv\Scripts\activate.bat && python run_api.py" -WorkingDirectory $Root

# Wait for backend
Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 12

# Start frontend
Write-Host "Starting frontend on port 8501..." -ForegroundColor Green
Start-Process -FilePath "cmd" -ArgumentList "/k", "title EcoInfraMind-Frontend && cd frontend && npm run dev" -WorkingDirectory $Root

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EcoInfraMind AI is running!" -ForegroundColor Green
Write-Host ""
Write-Host "  Frontend:  http://localhost:8501" -ForegroundColor White
Write-Host "  Backend:   http://localhost:8432" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8432/docs" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Close this window. Backend and frontend are running in separate windows." -ForegroundColor Gray
Read-Host "Press Enter to exit"
