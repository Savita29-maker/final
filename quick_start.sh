#!/bin/bash
# Smart Patient Queue - Quick Start Script for macOS/Linux

echo ""
echo "========================================"
echo " Smart Patient Queue & Appointment Predictor"
echo " macOS/Linux Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

# Check if PostgreSQL is running
echo "Checking PostgreSQL connection..."
psql -U postgres -c "SELECT 1" &>/dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: Cannot connect to PostgreSQL"
    echo "Please ensure PostgreSQL is running on localhost:5432"
    echo ""
    echo "To start PostgreSQL on macOS: brew services start postgresql"
    echo "To start PostgreSQL on Linux: sudo service postgresql start"
    echo ""
fi

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing Python packages..."
pip install -q -r requirements.txt

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please update .env with your database credentials if needed"
fi

echo ""
echo "========================================"
echo " Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. In this terminal, start the backend:"
echo "   cd backend"
echo "   python -m uvicorn app.main:app --reload --port 8000"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   source venv/bin/activate  # macOS/Linux"
echo "   cd frontend"
echo "   streamlit run app.py"
echo ""
echo "3. Optional: Populate with sample data:"
echo "   python sample_data.py"
echo ""
echo "4. Access the application:"
echo "   - Frontend: http://localhost:8501"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
