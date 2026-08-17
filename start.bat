@echo off
title EcoInfraMind AI
echo ========================================
echo   EcoInfraMind AI - Setup ^& Launch
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found. Install Python 3.12+ and add to PATH.
    pause
    exit /b 1
)

:: Check Node
node --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js not found. Install Node.js 18+ and add to PATH.
    pause
    exit /b 1
)

:: Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt -q

:: Download model if not present
if not exist "model\ecoinframind-ai-model.gguf" (
    echo.
    echo Downloading model (~2 GB)...
    if exist "download_model.sh" (
        bash download_model.sh
    ) else (
        echo WARNING: download_model.sh not found. Download model manually.
        echo Place qwen2.5-3b-instruct-q4_k_m.gguf in model/
    )
)

:: Install frontend dependencies
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    npm install --silent
    cd ..
)

echo.
echo ========================================
echo   Starting EcoInfraMind AI...
echo ========================================
echo.

:: Start backend
echo Starting backend on port 8432...
start "EcoInfraMind-Backend" cmd /k "venv\Scripts\activate.bat && python run_api.py"

:: Wait for backend to load
echo Waiting for backend to initialize...
timeout /t 12 /nobreak >nul

:: Start frontend
echo Starting frontend on port 8501...
start "EcoInfraMind-Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   EcoInfraMind AI is running!
echo.
echo   Frontend:  http://localhost:8501
echo   Backend:   http://localhost:8432
echo   API Docs:  http://localhost:8432/docs
echo ========================================
echo.
echo Close this window. Backend and frontend are running in separate windows.
pause
