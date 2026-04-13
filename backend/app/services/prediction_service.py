"""
Prediction service for wait times and analytics
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from ..models import Queue, Appointment, Doctor
from .ml_model import predict_wait_time


class PredictionService:
    """Service for predicting wait times and queue analytics"""

    @staticmethod
    def get_queue_length(db: Session, doctor_id: int) -> int:
        """Get current queue length for a doctor"""
        queue_length = db.query(func.count(Queue.id)).filter(
            and_(
                Queue.appointment_id.in_(
                    db.query(Appointment.id).filter(Appointment.doctor_id == doctor_id)
                ),
                Queue.status.in_(["waiting", "in_progress"])
            )
        ).scalar()
        return queue_length or 0

    @staticmethod
    def predict_patient_wait_time(db: Session, patient_id: int, doctor_id: int, priority_score: int) -> float:
        """Predict wait time for a specific patient"""
        # Get queue length
        queue_length = PredictionService.get_queue_length(db, doctor_id)

        # Get doctor's average consultation time
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            return 0.0

        avg_time = doctor.avg_consultation_time

        # Predict
        predicted_wait = predict_wait_time(queue_length, priority_score, avg_time)

        return round(predicted_wait, 2)

    @staticmethod
    def get_queue_analytics(db: Session, doctor_id: int) -> dict:
        """Get analytics for doctor's queue"""
        # Current queue
        queue_length = PredictionService.get_queue_length(db, doctor_id)

        # Average priority
        avg_priority = db.query(func.avg(Queue.priority_score)).filter(
            and_(
                Queue.appointment_id.in_(
                    db.query(Appointment.id).filter(Appointment.doctor_id == doctor_id)
                ),
                Queue.status.in_(["waiting", "in_progress"])
            )
        ).scalar() or 0

        # Doctor info
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

        return {
            "doctor_id": doctor_id,
            "doctor_name": doctor.name if doctor else "Unknown",
            "current_queue_length": queue_length,
            "average_priority": round(avg_priority, 2),
            "doctor_avg_consultation_time": doctor.avg_consultation_time if doctor else 0
        }
