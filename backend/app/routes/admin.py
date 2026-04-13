"""Admin routes for system management"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, Date, cast
from datetime import date, datetime
from ..database import get_db
from ..models import Patient, Doctor, Appointment, Queue, QueueLog, Notification
from ..schemas import PatientResponse, DoctorResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard", response_model=dict)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get overall system statistics"""
    today = date.today()

    # Count totals
    total_patients = db.query(func.count(Patient.id)).scalar() or 0
    total_doctors = db.query(func.count(Doctor.id)).scalar() or 0
    total_appointments = db.query(func.count(Appointment.id)).scalar() or 0

    # Today's stats
    today_appointments = db.query(func.count(Appointment.id)).filter(
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    today_completed = db.query(func.count(Appointment.id)).filter(
        Appointment.status == "completed",
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    today_cancelled = db.query(func.count(Appointment.id)).filter(
        Appointment.status == "cancelled",
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    # Current queue
    current_queue = db.query(func.count(Queue.id)).filter(
        Queue.status.in_(["waiting", "in_progress"])
    ).scalar() or 0

    # Notifications sent today
    notifications_sent = db.query(func.count(Notification.id)).filter(
        cast(Notification.timestamp, Date) == today
    ).scalar() or 0

    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "today_date": str(today),
        "today_appointments": today_appointments,
        "today_completed": today_completed,
        "today_cancelled": today_cancelled,
        "current_queue_size": current_queue,
        "notifications_sent_today": notifications_sent
    }


@router.get("/appointments-analytics", response_model=dict)
def get_appointments_analytics(db: Session = Depends(get_db)):
    """Get detailed appointment analytics"""
    today = date.today()

    # Status breakdown
    waiting = db.query(func.count(Appointment.id)).filter(
        Appointment.status == "waiting",
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    in_progress = db.query(func.count(Appointment.id)).filter(
        Appointment.status == "in_progress",
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    completed = db.query(func.count(Appointment.id)).filter(
        Appointment.status == "completed",
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    cancelled = db.query(func.count(Appointment.id)).filter(
        Appointment.status == "cancelled",
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    # Type breakdown
    scheduled = db.query(func.count(Appointment.id)).filter(
        Appointment.appointment_type == "scheduled",
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    walk_in = db.query(func.count(Appointment.id)).filter(
        Appointment.appointment_type == "walk-in",
        cast(Appointment.appointment_date, Date) == today
    ).scalar() or 0

    return {
        "date": str(today),
        "status_breakdown": {
            "waiting": waiting,
            "in_progress": in_progress,
            "completed": completed,
            "cancelled": cancelled
        },
        "type_breakdown": {
            "scheduled": scheduled,
            "walk_in": walk_in
        },
        "total": waiting + in_progress + completed + cancelled
    }


@router.get("/doctor-performance", response_model=list)
def get_doctor_performance(db: Session = Depends(get_db)):
    """Get performance metrics for all doctors"""
    doctors = db.query(Doctor).all()
    today = date.today()

    performance = []
    for doctor in doctors:
        completed_today = db.query(func.count(Appointment.id)).filter(
            Appointment.doctor_id == doctor.id,
            Appointment.status == "completed",
            cast(Appointment.appointment_date, Date) == today
        ).scalar() or 0

        logs = db.query(QueueLog).filter(
            QueueLog.appointment_id.in_(
                db.query(Appointment.id).filter(
                    Appointment.doctor_id == doctor.id,
                    cast(Appointment.appointment_date, Date) == today
                )
            )
        ).all()

        avg_wait = 0
        avg_consult = 0
        if logs:
            waits = [l.wait_time_minutes for l in logs if l.wait_time_minutes]
            consults = [l.consultation_time_minutes for l in logs if l.consultation_time_minutes]
            avg_wait = sum(waits) / len(waits) if waits else 0
            avg_consult = sum(consults) / len(consults) if consults else 0

        performance.append({
            "doctor_id": doctor.id,
            "doctor_name": doctor.name,
            "specialization": doctor.specialization,
            "appointments_completed_today": completed_today,
            "avg_wait_time_minutes": round(avg_wait, 2),
            "avg_consultation_minutes": round(avg_consult, 2)
        })

    return performance


@router.post("/doctors", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_doctor(name: str, specialization: str, avg_consultation_time: float = 15.0, db: Session = Depends(get_db)):
    """Add a new doctor (admin function)"""
    from ..models import Doctor as DoctorModel

    doctor = DoctorModel(
        name=name,
        specialization=specialization,
        avg_consultation_time=avg_consultation_time
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return {
        "success": True,
        "doctor_id": doctor.id,
        "doctor_name": doctor.name,
        "specialization": doctor.specialization
    }


@router.get("/patients-list", response_model=list)
def get_all_patients(db: Session = Depends(get_db)):
    """Get list of all patients"""
    patients = db.query(Patient).order_by(Patient.created_at.desc()).all()
    return [
        {
            "patient_id": p.id,
            "name": p.name,
            "age": p.age,
            "phone": p.phone,
            "email": p.email,
            "priority_score": p.priority_score,
            "created_at": str(p.created_at)
        }
        for p in patients
    ]
