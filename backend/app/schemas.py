"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime, date, time
from typing import Optional, List


class PatientCreate(BaseModel):
    """Patient creation schema"""
    name: str
    age: int
    phone: str
    email: EmailStr
    symptoms: Optional[str] = None
    priority_score: int = 0


class PatientResponse(PatientCreate):
    """Patient response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DoctorCreate(BaseModel):
    """Doctor creation schema"""
    name: str
    specialization: str
    avg_consultation_time: float = 15.0


class DoctorResponse(DoctorCreate):
    """Doctor response schema"""
    id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AppointmentCreate(BaseModel):
    """Appointment creation schema"""
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: Optional[time] = None
    appointment_type: str = "scheduled"


class AppointmentResponse(AppointmentCreate):
    """Appointment response schema"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QueueCreate(BaseModel):
    """Queue creation schema"""
    appointment_id: int
    token_number: int
    queue_position: int
    priority_score: int = 0


class QueueResponse(QueueCreate):
    """Queue response schema"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QueueLogCreate(BaseModel):
    """Queue log creation schema"""
    appointment_id: int
    arrival_time: datetime
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    wait_time_minutes: Optional[int] = None
    consultation_time_minutes: Optional[int] = None


class QueueLogResponse(QueueLogCreate):
    """Queue log response schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationCreate(BaseModel):
    """Notification creation schema"""
    patient_id: int
    appointment_id: Optional[int] = None
    message: str
    notification_type: Optional[str] = None


class NotificationResponse(NotificationCreate):
    """Notification response schema"""
    id: int
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True


class NextPatientResponse(BaseModel):
    """Response for next patient call"""
    appointment_id: int
    patient_name: str
    token_number: int
    priority_score: int
    patient_phone: str


class PredictionRequest(BaseModel):
    """Wait time prediction request"""
    queue_length: int
    priority_score: int
    doctor_avg_time: float


class PredictionResponse(BaseModel):
    """Wait time prediction response"""
    predicted_wait_time: float
    queue_length: int
    priority_score: int


class QueueDetailResponse(BaseModel):
    """Detailed queue information"""
    appointment_id: int
    patient_name: str
    token_number: int
    queue_position: int
    priority_score: int
    status: str
    symptoms: Optional[str] = None
    wait_time_prediction: Optional[float] = None
