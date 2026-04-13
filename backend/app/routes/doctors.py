"""
Doctor routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import Date, cast, func
from datetime import datetime
from ..database import get_db
from ..models import Doctor, Appointment, Queue, QueueLog
from ..schemas import (
    DoctorCreate, DoctorResponse, NextPatientResponse, QueueDetailResponse
)
from ..services.queue_service import QueueService
from ..services.notification_service import NotificationService

router = APIRouter(prefix="/api/doctors", tags=["doctors"])


@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    """
    Add a new doctor to the system
    
    - **name**: Doctor name
    - **specialization**: Medical specialization
    - **avg_consultation_time**: Average consultation time in minutes
    """
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)

    return db_doctor


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Get doctor details"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor


@router.get("", response_model=list[DoctorResponse])
def list_doctors(db: Session = Depends(get_db)):
    """List all doctors"""
    doctors = db.query(Doctor).all()
    return [DoctorResponse.model_validate(d) for d in doctors]


@router.get("/{doctor_id}/queue", response_model=dict)
def get_doctor_queue(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get current queue for a doctor
    Ordered by priority (highest first) then FIFO
    """
    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Get queue
    queue_list = QueueService.get_doctor_queue(db, doctor_id)

    return {
        "doctor_id": doctor_id,
        "doctor_name": doctor.name,
        "specialization": doctor.specialization,
        "queue_count": len(queue_list),
        "queue": queue_list
    }


@router.post("/{doctor_id}/next-patient", response_model=dict)
def call_next_patient(doctor_id: int, db: Session = Depends(get_db)):
    """
    Call next patient in queue
    - Selects patient with highest priority, then FIFO
    - Updates status to "in_progress"
    - Sends SMS notification to patient
    """
    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Get next patient
    result = QueueService.call_next_patient(db, doctor_id)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    # Send notification to patient
    NotificationService.notify_patient_called(
        db,
        db.query(Appointment).filter(
            Appointment.id == result["appointment_id"]
        ).first().patient_id,
        result["appointment_id"],
        result["token_number"]
    )

    return {
        "success": True,
        "appointment_id": result["appointment_id"],
        "patient_name": result["patient_name"],
        "patient_phone": result["patient_phone"],
        "token_number": result["token_number"],
        "priority_score": result["priority_score"],
        "message": f"Patient {result['patient_name']} (Token: {result['token_number']}) is now being called"
    }


@router.post("/{doctor_id}/complete/{appointment_id}", response_model=dict)
def complete_consultation(
    doctor_id: int,
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark consultation as completed
    - Updates appointment status to "completed"
    - Records consultation time in queue_logs
    """
    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Verify appointment belongs to doctor
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment or appointment.doctor_id != doctor_id:
        raise HTTPException(status_code=404, detail="Appointment not found for this doctor")

    # Complete consultation
    result = QueueService.complete_consultation(db, appointment_id, doctor_id)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    # Get consultation details
    queue_log = db.query(QueueLog).filter(QueueLog.appointment_id == appointment_id).first()

    return {
        "success": True,
        "appointment_id": appointment_id,
        "consultation_time_minutes": queue_log.consultation_time_minutes if queue_log else 0,
        "wait_time_minutes": queue_log.wait_time_minutes if queue_log else 0,
        "message": "Consultation marked as completed"
    }


@router.get("/{doctor_id}/today-stats", response_model=dict)
def get_today_statistics(doctor_id: int, db: Session = Depends(get_db)):
    """Get today's statistics for a doctor"""
    from datetime import date
    from sqlalchemy import func

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    today = date.today()

    # Completed appointments today
    completed = db.query(func.count(Appointment.id)).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status == "completed",
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    # Wait time statistics
    logs = db.query(QueueLog).filter(
        QueueLog.appointment_id.in_(
            db.query(Appointment.id).filter(
                Appointment.doctor_id == doctor_id,
                cast(Appointment.appointment_date, Date) == today
            )
        )
    ).all()

    avg_wait = 0
    avg_consultation = 0
    if logs:
        wait_times = [log.wait_time_minutes for log in logs if log.wait_time_minutes]
        consultation_times = [log.consultation_time_minutes for log in logs if log.consultation_time_minutes]
        avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0
        avg_consultation = sum(consultation_times) / len(consultation_times) if consultation_times else 0

    return {
        "doctor_id": doctor_id,
        "doctor_name": doctor.name,
        "date": str(today),
        "appointments_completed": completed,
        "average_wait_time_minutes": round(avg_wait, 2),
        "average_consultation_time_minutes": round(avg_consultation, 2),
        "total_logs": len(logs)
    }
