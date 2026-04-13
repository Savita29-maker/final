@echo off
REM Smart Patient Queue - Quick Start Script for Windows

echo.
echo ========================================
echo  Smart Patient Queue & Appointment Predictor
echo  Windows Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if PostgreSQL is running
echo Checking PostgreSQL connection...
psql -U postgres -c "SELECT 1" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Cannot connect to PostgreSQL
    echo Please ensure PostgreSQL is running on localhost:5432
    echo.
    echo Default credentials expected:
    echo   Username: postgres
    echo   Password: password
    echo   Database: smart_patient_queue
    echo.
    pause
)

REM Create virtual environment if not exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing Python packages...
pip install -q -r requirements.txt

REM Create .env file if not exists
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Please update .env with your database credentials if needed
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. In this terminal, start the backend:
echo    cd backend
echo    python -m uvicorn app.main:app --reload --port 8000
echo.
echo 2. In a new terminal, start the frontend:
echo    cd frontend
echo    streamlit run app.py
echo.
echo 3. Optional: Populate with sample data:
echo    python sample_data.py
echo.
echo 4. Access the application:
echo    - Frontend: http://localhost:8501
echo    - Backend API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo.
pause
