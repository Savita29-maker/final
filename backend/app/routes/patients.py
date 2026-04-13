"""
Patient routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from ..database import get_db
from ..models import Patient, Appointment, Queue
from ..schemas import (
    PatientCreate, PatientResponse, AppointmentCreate, AppointmentResponse,
    QueueResponse
)
from ..services.notification_service import NotificationService
from ..services.queue_service import QueueService
from ..services.prediction_service import PredictionService

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """
    Create a new patient
    
    - **name**: Patient name
    - **age**: Patient age
    - **phone**: Phone number (unique)
    - **email**: Email address
    - **symptoms**: Health symptoms
    - **priority_score**: Priority (0-100)
    """
    # Check if patient already exists
    existing = db.query(Patient).filter(Patient.phone == patient.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get patient details"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


@router.post("/appointments", response_model=dict, status_code=status.HTTP_201_CREATED)
def book_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    """
    Book an appointment for a patient
    
    - **patient_id**: Patient ID
    - **doctor_id**: Doctor ID
    - **appointment_date**: Date of appointment
    - **appointment_time**: Time of appointment (optional)
    - **appointment_type**: "scheduled" or "walk-in"
    """
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Create appointment
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.flush()

    # Add to queue
    queue_entry = QueueService.add_to_queue(
        db,
        db_appointment.id,
        appointment.doctor_id,
        patient.priority_score
    )

    db.commit()

    # Send notification
    NotificationService.notify_appointment_booked(
        db,
        appointment.patient_id,
        db_appointment.id,
        queue_entry.token_number
    )

    return {
        "success": True,
        "appointment_id": db_appointment.id,
        "token_number": queue_entry.token_number,
        "queue_position": queue_entry.queue_position,
        "message": f"Appointment booked successfully. Your token number is {queue_entry.token_number}"
    }


@router.get("/{patient_id}/appointments", response_model=list)
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    """Get all appointments for a patient"""
    appointments = db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).order_by(Appointment.created_at.desc()).all()

    result = []
    for apt in appointments:
        queue = db.query(Queue).filter(Queue.appointment_id == apt.id).first()
        result.append({
            "appointment_id": apt.id,
            "doctor_id": apt.doctor_id,
            "appointment_date": apt.appointment_date,
            "appointment_time": apt.appointment_time,
            "status": apt.status,
            "token_number": queue.token_number if queue else None,
            "queue_position": queue.queue_position if queue else None,
            "priority_score": queue.priority_score if queue else None
        })

    return result


@router.post("/cancel/{appointment_id}", response_model=dict)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Cancel an appointment
    Can only cancel if status is "waiting"
    """
    # Verify appointment exists
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Cancel through queue service
    result = QueueService.cancel_appointment(db, appointment_id)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    # Send cancellation notification
    NotificationService.notify_appointment_cancelled(db, appointment.patient_id, appointment_id)

    return result


@router.get("/{patient_id}/current-status", response_model=dict)
def get_patient_current_status(patient_id: int, db: Session = Depends(get_db)):
    """Get current queue status for patient's current appointment"""
    # Get latest appointment
    appointment = db.query(Appointment).filter(
        Appointment.patient_id == patient_id,
        Appointment.status.in_(["waiting", "in_progress"])
    ).order_by(Appointment.created_at.desc()).first()

    if not appointment:
        return {
            "status": "no_active_appointment",
            "message": "No active appointment found"
        }

    # Get queue entry
    queue = db.query(Queue).filter(Queue.appointment_id == appointment.id).first()

    # Predict wait time
    wait_time = PredictionService.predict_patient_wait_time(
        db,
        patient_id,
        appointment.doctor_id,
        queue.priority_score
    )

    return {
        "appointment_id": appointment.id,
        "status": appointment.status,
        "token_number": queue.token_number,
        "queue_position": queue.queue_position,
        "predicted_wait_time_minutes": wait_time,
        "priority_score": queue.priority_score
    }
