# Smart Patient Queue & Appointment Predictor

## 🏥 Project Overview

A comprehensive full-stack hospital management system with:
- **Real-time patient queue management** with priority-based ordering
- **AI-powered wait-time prediction** using XGBoost
- **Automated SMS/Email notifications** for appointments
- **Doctor consultation tracking** with analytics
- **Admin dashboard** for system overview

## 🏗️ Architecture

```
Smart Patient Queue/
├── backend/              # FastAPI backend
│   └── app/
│       ├── main.py      # FastAPI app entry point
│       ├── models.py    # SQLAlchemy models
│       ├── schemas.py   # Pydantic schemas
│       ├── database.py  # Database connection
│       ├── routes/      # API endpoints
│       │   ├── patients.py
│       │   ├── doctors.py
│       │   ├── predictions.py
│       │   └── admin.py
│       └── services/    # Business logic
│           ├── queue_service.py
│           ├── notification_service.py
│           ├── prediction_service.py
│           └── ml_model.py
├── frontend/            # Streamlit frontend
│   └── app.py
├── database/            # Database schema
│   └── schema.sql
└── requirements.txt     # Python dependencies
```

## 📋 Features

### 1. **Patient Portal**
- Book appointments with doctor selection
- View real-time queue status and wait time prediction
- Cancel appointments (if waiting)
- Receive SMS/Email notifications

### 2. **Doctor Portal**
- View patient queue (sorted by priority, then FIFO)
- Call next patient
- Mark consultation as completed
- View daily performance statistics

### 3. **Admin Dashboard**
- System overview (total patients, doctors, appointments)
- Appointment analytics (status breakdown)
- Doctor performance metrics
- Manage doctors
- View all patients

### 4. **Queue Management**
- **Automatic Token Generation**: Each appointment gets a unique token
- **Priority-Based Ordering**: High-priority patients move ahead in queue
- **FIFO Within Priority**: Same-priority patients served in booking order
- **Automatic Reordering**: Queue reorders when patients cancel
- **Queue Analytics**: Track wait times and consultation times

### 5. **AI-Powered Predictions**
- XGBoost model predicts wait times
- Features: queue_length, priority_score, doctor_avg_time
- Real-time predictions for patients

### 6. **Notification System**
- SMS and Email notifications (simulated with print())
- Triggered on: appointment booking, doctor calling, cancellation
- Production-ready structure for SMS/Email APIs

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- pip or conda

### Step 1: Clone & Setup Environment

```bash
cd c:\smart_patient_queue

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Setup

**Option A: Use PostgreSQL Locally**

```bash
# Create database
createdb smart_patient_queue

# Load schema
psql -U postgres -d smart_patient_queue -f database/schema.sql
```

**Option B: Use Docker (if PostgreSQL not installed)**

```bash
# Run PostgreSQL container (needs Docker)
docker run -d --name postgres_hospital -e POSTGRES_PASSWORD=password -e POSTGRES_DB=smart_patient_queue -p 5432:5432 postgres:15
```

### Step 3: Set Environment Variables

Create `.env` file in project root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_patient_queue
API_URL=http://localhost:8000/api
```

Or set directly in code (default uses localhost credentials).

### Step 4: Start Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

**API Documentation**: http://localhost:8000/docs (Swagger UI)

### Step 5: Start Frontend

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

Frontend will be available at: http://localhost:8501

## 📊 API Endpoints

### Patient APIs
- `POST /api/patients` - Register new patient
- `POST /api/patients/appointments` - Book appointment
- `GET /api/patients/{id}/current-status` - Get queue status
- `GET /api/patients/{id}/appointments` - View all appointments
- `POST /api/patients/cancel/{appointment_id}` - Cancel appointment

### Doctor APIs
- `POST /api/doctors` - Add doctor (admin)
- `GET /api/doctors/{id}/queue` - View queue
- `POST /api/doctors/{id}/next-patient` - Call next patient
- `POST /api/doctors/{id}/complete/{appointment_id}` - Mark completed
- `GET /api/doctors/{id}/today-stats` - View statistics

### ML Prediction APIs
- `POST /api/predict-wait-time` - Predict wait time
- `GET /api/queue-analytics/{doctor_id}` - Queue analytics

### Admin APIs
- `GET /api/admin/dashboard` - System dashboard
- `GET /api/admin/appointments-analytics` - Appointment analytics
- `GET /api/admin/doctor-performance` - Doctor performance
- `GET /api/admin/patients-list` - All patients

## 💡 Sample Usage Workflow

### 1. Patient Books Appointment

```
Patient Portal → Fill form → Select Doctor → Book Appointment
↓
Token generated: #123
Queue Position: 2
Notification sent (SMS + Email)
```

### 2. Doctor Calls Patients

```
Doctor Portal → View Queue (sorted by priority, then FIFO)
↓
Click "Call Next Patient"
↓
Patient #123 (High Priority) is called
SMS sent: "Please come, it's your turn!"
Queue updates automatically
```

### 3. Doctor Completes Consultation

```
Click "Complete Consultation"
↓
System logs:
- Wait time: 12 minutes
- Consultation time: 18 minutes
↓
Next patient automatically becomes active
```

### 4. Patient Checks Queue Status

```
Patient Portal → Check Status → Enters Phone
↓
Current Position: 1
Predicted Wait: 15 minutes
Status: In Queue
```

### 5. Patient Cancels

```
Patient Portal → Cancel → Confirm
↓
Status changed to "cancelled"
Queue reordered automatically
Cancellation notification sent
```

## 🧠 ML Model Details

### XGBoost Wait Time Predictor

**Training Data**: 1000 synthetic samples

**Features**:
- `queue_length`: Number of patients in queue (0-30)
- `priority_score`: Patient priority level (0-100)
- `doctor_avg_time`: Average consultation time (10-30 min)

**Target**:
- `wait_time`: Predicted wait time in minutes

**Model Configuration**:
- Algorithm: XGBRegressor
- Estimators: 100
- Max Depth: 5
- Learning Rate: 0.1

**Usage**:
```python
from backend.app.services.ml_model import predict_wait_time

wait_time = predict_wait_time(
    queue_length=5,
    priority_score=75,
    doctor_avg_time=15.0
)
# Returns: ~12.5 minutes
```

## 📱 Notification System

### Currently: Simulated (print-based)
```
SMS sent to 9876543210: Your appointment is confirmed. Token: 123
Email sent to user@example.com: Your appointment is confirmed. Token: 123
```

### Production Integration (Ready):
Replace `send_sms()` and `send_email()` in `services/notification_service.py` with:

**For SMS** (Twilio example):
```python
from twilio.rest import Client

def send_sms(phone, message):
    client = Client(account_sid, auth_token)
    client.messages.create(to=phone, from_="+1234567890", body=message)
```

**For Email** (SendGrid example):
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(email, message, subject):
    mail = Mail(from_email=SENDER, to_emails=email, subject=subject, html_content=message)
    SendGridAPIClient(SENDGRID_KEY).send(mail)
```

## 🔐 Priority Score Logic

The priority score determines queue position:

- **0-20**: Low (routine checkup)
- **21-50**: Normal (general illness)
- **51-80**: High (serious condition)
- **81-100**: Emergency (critical)

Higher priority patients move ahead in queue, but still respect FIFO within same priority.

## 📈 Database Schema

### patients
- id, name, age, phone (unique), email, symptoms, priority_score

### doctors
- id, name, specialization, avg_consultation_time, is_available

### appointments
- id, patient_id, doctor_id, date, time, status (waiting/in_progress/completed/cancelled), type

### queue
- id, appointment_id, token_number, queue_position, priority_score, status

### queue_logs
- id, appointment_id, arrival_time, start_time, end_time, wait_time_minutes, consultation_time_minutes

### notifications
- id, patient_id, appointment_id, message, type (booking/call/cancel), status (sent/failed)

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/smart_patient_queue
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend (.streamlit/secrets.toml)
```toml
api_url = "http://localhost:8000/api"
```

## ✅ Testing the System

### 1. Test Patient Registration & Booking
```bash
# Via Streamlit or API
curl -X POST http://localhost:8000/api/patients \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","age":30,"phone":"9876543210","email":"john@example.com","symptoms":"Flu","priority_score":30}'
```

### 2. Test Queue Operations
```bash
# Get queue for doctor 1
curl http://localhost:8000/api/doctors/1/queue

# Call next patient
curl -X POST http://localhost:8000/api/doctors/1/next-patient
```

### 3. Test Predictions
```bash
curl -X POST http://localhost:8000/api/predict-wait-time \
  -H "Content-Type: application/json" \
  -d '{"queue_length":5,"priority_score":50,"doctor_avg_time":15}'
```

## 📊 Sample Data

To populate with sample data, use the Streamlit interface:
1. Create 3-5 sample doctors through Admin Panel
2. Book 10-15 appointments as different patients
3. View analytics and predictions

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check PostgreSQL connection
psql -U postgres -d smart_patient_queue -c "SELECT 1"

# Check port 8000 is free
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Mac/Linux
```

### Streamlit can't connect
- Ensure backend is running at http://localhost:8000
- Check CORS is enabled (it is by default)
- Check API_URL in frontend code

### Database errors
- Ensure PostgreSQL is running
- Check credentials in DATABASE_URL
- Run `python -c "from sqlalchemy import create_engine; engine = create_engine(DATABASE_URL); print(engine.execute('SELECT 1'))"` to test connection

## 📚 Project Structure Details

### app/routes/
- **patients.py**: Patient registration, appointments, status, cancellation
- **doctors.py**: Doctor management, queue viewing, consultation actions
- **predictions.py**: AI-based wait time predictions
- **admin.py**: System analytics, doctor management, patient list

### app/services/
- **queue_service.py**: Queue logic (add, get_next, call, complete, cancel, reorder)
- **notification_service.py**: SMS/Email (simulated, ready for real APIs)
- **prediction_service.py**: Analytics and ML predictions
- **ml_model.py**: XGBoost model training and inference

## 🎯 Next Steps / Future Enhancements

1. **Real SMS/Email Integration**: Twilio, SendGrid
2. **Payment Integration**: Stripe for appointment fees
3. **Two-Factor Authentication**: OTP verification
4. **Appointment Reminders**: 24-hour pre-appointment SMS
5. **Mobile App**: React Native or Flutter
6. **Doctor Ratings**: Patient reviews and ratings
7. **Multiple Clinic Chains**: Multi-tenant support
8. **Advanced Analytics**: Dashboards, reports, graphs
9. **Appointment Reschedule**: Instead of cancel
10. **Video Consultation**: Integration with Jitsi/Zoom

## 📝 License

MIT License - Open source project

## 👥 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at http://localhost:8000/docs
3. Check Streamlit logs for frontend issues

---

**Built with ❤️ for better hospital management**
