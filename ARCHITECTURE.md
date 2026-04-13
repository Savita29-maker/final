# Smart Patient Queue - Architecture & APIs

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│         (Patient | Doctor | Admin Interfaces)               │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP Requests
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Routes Layer                                          │   │
│  │ - patients.py    (Patient management)                │   │
│  │ - doctors.py     (Doctor management)                 │   │
│  │ - predictions.py (ML predictions)                    │   │
│  │ - admin.py       (Admin functions)                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                       ▲                                      │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────────┐   │
│  │ Services Layer (Business Logic)                       │   │
│  │ ┌──────────────────────────────────────────────────┐ │   │
│  │ │ queue_service.py      (Priority queue)          │ │   │
│  │ ├──────────────────────────────────────────────────┤ │   │
│  │ │ notification_service.py (SMS/Email)             │ │   │
│  │ ├──────────────────────────────────────────────────┤ │   │
│  │ │ prediction_service.py  (Analytics & ML)         │ │   │
│  │ ├──────────────────────────────────────────────────┤ │   │
│  │ │ ml_model.py           (XGBoost)                 │ │   │
│  │ └──────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
│                       ▲                                      │
│                       │ SQL                                 │
└───────────────────────┼───────────────────────────────────┘
                        │
         ┌──────────────▼─────────────────┐
         │   PostgreSQL Database           │
         │                                 │
         │ - patients                      │
         │ - doctors                       │
         │ - appointments                  │
         │ - queue                         │
         │ - queue_logs                    │
         │ - notifications                 │
         └─────────────────────────────────┘
```

## 📊 Data Flow Diagram

### Appointment Booking Flow
```
Patient Portal Form
     ▼
Create Patient Record
     ▼
Book Appointment
     ▼
Generate Token & Queue Position
     ▼
Insert into Queue Table
     ▼
Trigger Notification Service
     ▼
Send SMS + Email
     ▼
Return Confirmation to Patient
```

### Queue Management Flow
```
Doctor Portal
     ▼
Click "Next Patient"
     ▼
QueueService.call_next_patient()
     ├─ Sort by priority DESC
     ├─ Then by created_at ASC (FIFO)
     ├─ Update Queue status → in_progress
     ├─ Update Appointment status → in_progress
     └─ Log arrival time
     ▼
Trigger Notification (Patient Called)
     ▼
Show Patient Details to Doctor
```

### Consultation Flow
```
Doctor Finishes Consultation
     ▼
Click "Complete Consultation"
     ▼
QueueService.complete_consultation()
     ├─ Update Appointment status → completed
     ├─ Update Queue status → completed
     └─ Calculate wait & consultation times
     ▼
Log to queue_logs table
     ▼
Auto-call next patient
```

## 🔄 Queue Algorithm

### Priority-Based FIFO Queue

```python
# Sorting Logic
ORDER BY:
    1. priority_score DESC    (Higher priority first)
    2. created_at ASC         (Earlier booking first within same priority)

# Example Queue:
Token #3 | Priority 100 | Created 09:00 ← First (Emergency)
Token #1 | Priority 50  | Created 08:00 ← Second (Earlier booking)
Token #2 | Priority 50  | Created 08:30 ← Third (Later booking)
Token #4 | Priority 20  | Created 09:30 ← Last (Low priority)
```

### Queue Reordering on Cancellation

```
Original Queue:
[Token #1] [Token #2] [Token #3] [Token #4]
     ▼
Patient #2 cancels
     ▼
QueueService.reorder_queue()
     ├─ Remove Token #2 from queue
     ├─ Re-sort remaining patients
     └─ Update queue_position values
     ▼
New Queue:
[Token #1] [Token #3] [Token #4]
```

## 🤖 ML Model Architecture

### XGBoost Wait Time Predictor

```
Input Features:
├─ queue_length (0-50)
├─ priority_score (0-100)
└─ doctor_avg_time (5-60 minutes)
        ▼
┌──────────────────────┐
│ StandardScaler       │ (Feature normalization)
└────────────┬─────────┘
             ▼
┌──────────────────────────────┐
│ XGBRegressor                 │
│ - n_estimators: 100          │
│ - max_depth: 5               │
│ - learning_rate: 0.1         │
└────────────┬─────────────────┘
             ▼
Output: predicted_wait_time (minutes)

Example:
Input: queue_length=5, priority=75, doctor_time=15
         ▼
Output: 12.5 minutes
```

## 📡 API Endpoints Reference

### Patient APIs

#### Create Patient
```http
POST /api/patients
Content-Type: application/json

{
  "name": "John Doe",
  "age": 30,
  "phone": "9876543210",
  "email": "john@example.com",
  "symptoms": "Headache and fever",
  "priority_score": 50
}

Response:
{
  "id": 1,
  "name": "John Doe",
  "age": 30,
  "phone": "9876543210",
  "email": "john@example.com",
  "symptoms": "Headache and fever",
  "priority_score": 50,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### Book Appointment
```http
POST /api/patients/appointments
Content-Type: application/json

{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2024-01-15",
  "appointment_time": "10:30:00",
  "appointment_type": "scheduled"
}

Response:
{
  "success": true,
  "appointment_id": 1,
  "token_number": 5,
  "queue_position": 2,
  "message": "Appointment booked successfully. Your token number is 5"
}
```

#### Get Current Status
```http
GET /api/patients/{patient_id}/current-status

Response:
{
  "appointment_id": 1,
  "status": "waiting",
  "token_number": 5,
  "queue_position": 2,
  "predicted_wait_time_minutes": 15.3,
  "priority_score": 50
}
```

#### Cancel Appointment
```http
POST /api/patients/cancel/{appointment_id}

Response:
{
  "success": true,
  "appointment_id": 1,
  "message": "Appointment cancelled"
}
```

### Doctor APIs

#### Get Doctor's Queue
```http
GET /api/doctors/{doctor_id}/queue

Response:
{
  "doctor_id": 1,
  "doctor_name": "Dr. Sarah Johnson",
  "specialization": "General Practitioner",
  "queue_count": 3,
  "queue": [
    {
      "appointment_id": 1,
      "patient_name": "John Doe",
      "token_number": 5,
      "queue_position": 1,
      "priority_score": 50,
      "status": "waiting",
      "symptoms": "Headache and fever"
    },
    {
      "appointment_id": 2,
      "patient_name": "Jane Smith",
      "token_number": 6,
      "queue_position": 2,
      "priority_score": 40,
      "status": "waiting",
      "symptoms": "Back pain"
    }
  ]
}
```

#### Call Next Patient
```http
POST /api/doctors/{doctor_id}/next-patient

Response:
{
  "success": true,
  "appointment_id": 1,
  "patient_name": "John Doe",
  "patient_phone": "9876543210",
  "token_number": 5,
  "priority_score": 50,
  "message": "Patient John Doe (Token: 5) is now being called"
}
```

#### Complete Consultation
```http
POST /api/doctors/{doctor_id}/complete/{appointment_id}

Response:
{
  "success": true,
  "appointment_id": 1,
  "consultation_time_minutes": 18,
  "wait_time_minutes": 12,
  "message": "Consultation marked as completed"
}
```

### Prediction APIs

#### Predict Wait Time
```http
POST /api/predict-wait-time
Content-Type: application/json

{
  "queue_length": 5,
  "priority_score": 50,
  "doctor_avg_time": 15.0
}

Response:
{
  "predicted_wait_time": 12.5,
  "queue_length": 5,
  "priority_score": 50
}
```

### Admin APIs

#### Get Dashboard Stats
```http
GET /api/admin/dashboard

Response:
{
  "total_patients": 25,
  "total_doctors": 4,
  "total_appointments": 150,
  "today_date": "2024-01-15",
  "today_appointments": 12,
  "today_completed": 8,
  "today_cancelled": 1,
  "current_queue_size": 3,
  "notifications_sent_today": 12
}
```

#### Get Analytics
```http
GET /api/admin/appointments-analytics

Response:
{
  "date": "2024-01-15",
  "status_breakdown": {
    "waiting": 3,
    "in_progress": 1,
    "completed": 8,
    "cancelled": 1
  },
  "type_breakdown": {
    "scheduled": 10,
    "walk_in": 2
  },
  "total": 13
}
```

#### Get Doctor Performance
```http
GET /api/admin/doctor-performance

Response:
[
  {
    "doctor_id": 1,
    "doctor_name": "Dr. Sarah Johnson",
    "specialization": "General Practitioner",
    "appointments_completed_today": 5,
    "avg_wait_time_minutes": 12.5,
    "avg_consultation_minutes": 15.2
  },
  {
    "doctor_id": 2,
    "doctor_name": "Dr. Rajesh Kumar",
    "specialization": "Cardiologist",
    "appointments_completed_today": 3,
    "avg_wait_time_minutes": 18.3,
    "avg_consultation_minutes": 22.1
  }
]
```

## 🗄️ Database Schema

### patients
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(255) | NOT NULL |
| age | INT | NOT NULL |
| phone | VARCHAR(20) | UNIQUE, NOT NULL |
| email | VARCHAR(255) | NOT NULL |
| symptoms | TEXT | |
| priority_score | INT | DEFAULT 0 |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

### queue
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| appointment_id | INT | FOREIGN KEY, UNIQUE |
| token_number | INT | NOT NULL |
| queue_position | INT | NOT NULL |
| priority_score | INT | DEFAULT 0 |
| status | VARCHAR(50) | DEFAULT 'waiting' |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

**Indexes**:
- `idx_queue_status`: ON status (fast filtering)
- `idx_queue_priority`: ON priority_score DESC (priority sorting)
- `idx_appointments_status`: ON appointments(status)

## 🔐 Authentication & Security (Future)

Current implementation uses no authentication. For production:

```python
# Add JWT authentication
from fastapi.security import HTTPBearer, HTTPAuthCredential

security = HTTPBearer()

@router.post("/patients")
async def create_patient(
    patient: PatientCreate,
    credentials: HTTPAuthCredential = Depends(security)
):
    # Verify JWT token
    # Check user permissions
    # Proceed with business logic
```

## 📈 Performance Considerations

### Query Optimization
- **Indexes on**: status, priority_score, doctor_id, patient_id
- **Connection Pooling**: SQLAlchemy default pooling
- **Query Caching**: Streamlit frontend caches responses

### Scaling Strategies
1. **Horizontal Scaling**: Multiple FastAPI instances behind load balancer
2. **Database Sharding**: Shard by doctor_id for multi-clinic support
3. **Redis Caching**: Cache doctor queue and predictions
4. **Message Queue**: Use Celery for async notifications

## 📋 Notification Flow

### SMS/Email Integration Points

```
Event: Appointment Booked
├─ Trigger: API /patients/appointments
├─ Service: NotificationService.notify_appointment_booked()
└─ Output: SMS + Email to patient

Event: Doctor Calls Patient
├─ Trigger: API /doctors/{id}/next-patient
├─ Service: NotificationService.notify_patient_called()
└─ Output: SMS + Email to patient

Event: Appointment Cancelled
├─ Trigger: API /patients/cancel/{apt_id}
├─ Service: NotificationService.notify_appointment_cancelled()
└─ Output: SMS + Email to patient
```

### Notification Service Structure

```python
# Current: Simulated (print-based)
def send_sms(phone, message):
    print(f"SMS sent to {phone}: {message}")

# Production: Real API
def send_sms(phone, message):
    from twilio.rest import Client
    client = Client(account_sid, auth_token)
    client.messages.create(to=phone, from_=TWILIO_NUMBER, body=message)
```

## 🐳 Docker Deployment

### Multi-container Setup

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: smart_patient_queue
    
  backend:
    image: python:3.11
    command: uvicorn app.main:app --port 8000
    
  frontend:
    image: streamlit/latest
    command: streamlit run app.py
```

---

**Version**: 1.0.0
**Last Updated**: 2024-01-15
