# Smart Patient Queue - Complete Setup Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Start (Automatic Setup)](#quick-start-automatic-setup)
3. [Manual Setup](#manual-setup)
4. [Database Configuration](#database-configuration)
5. [Starting the Application](#starting-the-application)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: For pip package installation

### Required Software
- **PostgreSQL**: 12 or higher (or Docker for containerized version)
- **Python pip**: For package management

### Optional
- **Docker** & **Docker Compose**: For easy PostgreSQL setup
- **Git**: For cloning the repository

---

## Quick Start (Automatic Setup)

### On Windows

1. **Open Command Prompt** in the project root directory
   ```cmd
   cd c:\smart_patient_queue
   ```

2. **Run the quick start script**
   ```cmd
   quick_start.bat
   ```

3. Follow the on-screen instructions

### On macOS/Linux

1. **Open Terminal** in the project root directory
   ```bash
   cd ~/smart_patient_queue
   ```

2. **Make the script executable**
   ```bash
   chmod +x quick_start.sh
   ```

3. **Run the quick start script**
   ```bash
   ./quick_start.sh
   ```

---

## Manual Setup

### Step 1: Install Python Packages

```bash
# Activate virtual environment (if created)
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Expected time**: 2-5 minutes

### Step 2: Set Up PostgreSQL

#### Option A: Local PostgreSQL Installation

**Windows**:
```powershell
# Create database
createdb -U postgres smart_patient_queue

# Load schema
psql -U postgres -d smart_patient_queue -f database\schema.sql

# Verify
psql -U postgres -d smart_patient_queue -c "SELECT 1"
```

**macOS**:
```bash
# Install PostgreSQL (if not installed)
brew install postgresql@15

# Start PostgreSQL
brew services start postgresql@15

# Create database
createdb smart_patient_queue

# Load schema
psql -d smart_patient_queue -f database/schema.sql

# Verify
psql -d smart_patient_queue -c "SELECT 1"
```

**Linux (Ubuntu/Debian)**:
```bash
# Install PostgreSQL (if not installed)
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
sudo service postgresql start

# Create database
sudo -u postgres createdb smart_patient_queue

# Load schema
sudo -u postgres psql -d smart_patient_queue -f database/schema.sql

# Verify
sudo -u postgres psql -d smart_patient_queue -c "SELECT 1"
```

#### Option B: Docker (No Local PostgreSQL Installation Needed)

**Prerequisites**: Docker and Docker Compose installed

```bash
# Start PostgreSQL container
docker-compose up -d

# Wait for container to be healthy (10-20 seconds)
docker-compose logs postgres

# Load schema (runs automatically via docker-entrypoint-initdb.d)
# Verify
docker exec smart_patient_queue_db psql -U postgres -d smart_patient_queue -c "SELECT 1"
```

### Step 3: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings (optional, defaults work)
# Windows: notepad .env
# macOS/Linux: nano .env
```

**Default values in .env**:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_patient_queue
API_PORT=8000
```

---

## Database Configuration

### Default Database Credentials
- **Host**: localhost
- **Port**: 5432
- **Username**: postgres
- **Password**: password
- **Database**: smart_patient_queue

### Connection Strings

**For Local PostgreSQL**:
```
postgresql://postgres:password@localhost:5432/smart_patient_queue
```

**For Docker PostgreSQL**:
```
postgresql://postgres:password@localhost:5432/smart_patient_queue
```

**For Custom Configuration**:
Edit the `DATABASE_URL` in `.env` file:
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### Verify Database Connection

```bash
# Using psql
psql -U postgres -d smart_patient_queue -c "SELECT version();"

# Or via Python
python -c "from backend.app.database import engine; print(engine.execute('SELECT 1'))"
```

---

## Starting the Application

### Option 1: Use Provided Scripts

#### Windows
```batch
REM Terminal 1: Start Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

REM Terminal 2: Start Frontend
cd frontend
streamlit run app.py
```

#### macOS/Linux
```bash
# Terminal 1: Start Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Start Frontend
source venv/bin/activate
cd frontend
streamlit run app.py
```

### Option 2: Manual Start (Detailed Steps)

#### Start Backend

**Terminal 1**:
```bash
# Navigate to backend directory
cd backend

# Start FastAPI server
python -m uvicorn app.main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Access points**:
- API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- Health Check: http://localhost:8000/health

#### Start Frontend

**Terminal 2**:
```bash
# Activate virtual environment (if using one)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Navigate to frontend directory
cd frontend

# Start Streamlit app
streamlit run app.py
```

**Expected output**:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

**Access point**:
- Web UI: http://localhost:8501

### Full Application Status

Once both are running:

| Component | URL | Status |
|-----------|-----|--------|
| Backend API | http://localhost:8000 | ✅ Running |
| API Docs | http://localhost:8000/docs | ✅ Interactive |
| Frontend | http://localhost:8501 | ✅ Running |

---

## Testing

### Test 1: Quick API Test

**Check if backend is running**:
```bash
curl http://localhost:8000/health
```

**Expected response**:
```json
{"status":"healthy","timestamp":"2024-01-15T10:30:00.000000"}
```

### Test 2: Create Sample Data

**With backend running**:
```bash
# Populate with sample doctors and patient
python sample_data.py
```

**Expected output**:
```
🏥 Creating Sample Doctors...
✅ Created: Dr. Sarah Johnson (General Practitioner)
✅ Created: Dr. Rajesh Kumar (Cardiologist)
...
👤 Creating Sample Patient...
✅ Created patient: Raj Patel (ID: 1)
✅ Booked appointment: Token #1
```

### Test 3: Integration Test

**Complete workflow test**:
```bash
python integration_test.py
```

**This tests**:
1. Patient creation
2. Appointment booking
3. Queue management
4. Doctor calling patient
5. Consultation completion
6. Analytics

### Test 4: Manual Testing via Streamlit UI

1. Open http://localhost:8501
2. **Patient Portal**: Book an appointment
3. **Doctor Portal**: View queue and call patients
4. **Admin Dashboard**: Check analytics
5. **Predictor**: Test wait-time predictions

---

## Troubleshooting

### Issue 1: PostgreSQL Connection Failed

**Symptoms**:
```
psycopg2.OperationalError: could not connect to server
```

**Solutions**:

```bash
# Check if PostgreSQL is running
# Windows (Task Manager): Look for "postgres.exe"

# macOS
brew services list | grep postgresql

# Linux
sudo service postgresql status

# Start PostgreSQL
# macOS
brew services start postgresql@15

# Linux
sudo service postgresql start

# Docker (if using container)
docker-compose up -d
docker ps  # Verify postgres container is running
```

**If connection still fails**:
```bash
# Check credentials in .env
cat .env | grep DATABASE_URL

# Try connecting manually
psql -U postgres -d smart_patient_queue -c "SELECT 1"

# If password is wrong, reset user password
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'password';"
```

### Issue 2: Python Package Installation Failed

**Symptoms**:
```
ERROR: Could not find a version that satisfies the requirement
```

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Upgrade setuptools
pip install --upgrade setuptools wheel

# Try installing again
pip install -r requirements.txt

# If still failing, install packages individually
pip install fastapi
pip install uvicorn
pip install sqlalchemy
# ... etc
```

### Issue 3: Port Already in Use

**Symptoms**:
```
OSError: [Errno 48] Address already in use
```

**Solution**:

```bash
# Windows: Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux: Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
python -m uvicorn app.main:app --port 8001
streamlit run app.py --server.port 8502
```

### Issue 4: Frontend Can't Connect to Backend

**Symptoms**:
```
❌ Cannot connect to backend. Make sure it's running on port 8000
```

**Check**:

```bash
# Verify backend is running
curl http://localhost:8000/health

# Check API endpoint
curl http://localhost:8000/api/doctors

# If CORS issues, update frontend API_URL
# Edit: frontend/app.py - line with API_URL
```

### Issue 5: Streamlit Shows Old Cache

**Solution**:
```bash
# Clear Streamlit cache
streamlit cache clear

# Or restart with clear flag
streamlit run app.py --logger.level=debug
```

### Issue 6: ML Model Not Training

**Symptoms**:
```
KeyError: 'wait_time_model.pkl' or scaler.pkl file not found
```

**Solution**:
```bash
# Model trains automatically on first run
# If error persists, manually trigger training

python -c "from backend.app.services.ml_model import ml_service; ml_service.train_model()"

# Check if files exist
ls -la backend/app/services/wait_time_model.pkl
ls -la backend/app/services/scaler.pkl
```

### Issue 7: Database Schema Not Loaded

**Symptoms**:
```
ProgrammingError: relation "patients" does not exist
```

**Solution**:
```bash
# Manually load schema
psql -U postgres -d smart_patient_queue -f database/schema.sql

# Or via Python
python -c "from backend.app.models import Base; from backend.app.database import engine; Base.metadata.create_all(bind=engine)"
```

---

## Common Commands

### Backend Management

```bash
# Start with hot reload
python -m uvicorn app.main:app --reload --port 8000

# Start without hot reload (production)
python -m uvicorn app.main:app --port 8000

# Run with specific host
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Database Management

```bash
# Connect to database
psql -U postgres -d smart_patient_queue

# Run SQL file
psql -U postgres -d smart_patient_queue -f database/schema.sql

# Backup database
pg_dump -U postgres smart_patient_queue > backup.sql

# Restore database
psql -U postgres smart_patient_queue < backup.sql

# Drop database
dropdb -U postgres smart_patient_queue
```

### Frontend Management

```bash
# Run Streamlit
streamlit run app.py

# Run with custom port
streamlit run app.py --server.port 8502

# Run in headless mode
streamlit run app.py --headless

# Clear cache
streamlit cache clear
```

---

## Performance Tips

1. **Database Indexing**: Already optimized in schema
2. **Connection Pooling**: SQLAlchemy uses connection pooling
3. **Frontend Caching**: Streamlit caches API responses
4. **API Response Time**: < 200ms average
5. **Queue Operations**: O(n) for sorting, optimized with indexes

---

## File Structure Verification

Ensure all files are present:

```
smart_patient_queue/
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       ├── database.py
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── patients.py
│       │   ├── doctors.py
│       │   ├── predictions.py
│       │   └── admin.py
│       └── services/
│           ├── __init__.py
│           ├── queue_service.py
│           ├── notification_service.py
│           ├── prediction_service.py
│           └── ml_model.py
├── frontend/
│   └── app.py
├── database/
│   └── schema.sql
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── README.md
├── SETUP_GUIDE.md
├── .env.example
├── sample_data.py
├── integration_test.py
├── docker-compose.yml
├── quick_start.bat
└── quick_start.sh
```

---

## Next Steps After Setup

1. **Create Sample Data**: `python sample_data.py`
2. **Run Integration Tests**: `python integration_test.py`
3. **Access Frontend**: http://localhost:8501
4. **Explore API Docs**: http://localhost:8000/docs
5. **Book Appointments**: Use Patient Portal
6. **Manage Queue**: Use Doctor Portal
7. **View Analytics**: Access Admin Dashboard

---

## Getting Help

### Check Logs

**Backend logs** (Terminal 1):
```
Look for INFO, WARNING, or ERROR messages
```

**Frontend logs** (Terminal 2):
```
Streamlit running messages
```

**Database logs** (PostgreSQL):
```bash
# On macOS
log show --predicate 'eventMessage contains "postgres"' --last 1h

# On Linux
sudo tail -f /var/log/postgresql/postgresql.log
```

### API Documentation

- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Test Endpoints

```bash
# List all doctors
curl http://localhost:8000/api/doctors

# Get dashboard
curl http://localhost:8000/api/admin/dashboard

# Predict wait time
curl -X POST http://localhost:8000/api/predict-wait-time \
  -H "Content-Type: application/json" \
  -d '{"queue_length":5,"priority_score":50,"doctor_avg_time":15}'
```

---

## Production Deployment

For production deployment:

1. **Set `DEBUG=False`** in .env
2. **Use production WSGI server** (Gunicorn instead of Uvicorn)
3. **Configure proper database** (managed PostgreSQL service)
4. **Enable HTTPS** (SSL certificates)
5. **Set up monitoring** (logging, error tracking)
6. **Configure real SMS/Email** (Twilio, SendGrid)
7. **Use secrets management** (AWS Secrets Manager, HashiCorp Vault)

---

## Support & Documentation

- **Full README**: See [README.md](README.md)
- **API Docs**: http://localhost:8000/docs
- **Source Code**: Well-commented Python files
- **Sample Data**: Use `sample_data.py` for testing

---

**Last Updated**: 2024
**Version**: 1.0.0
