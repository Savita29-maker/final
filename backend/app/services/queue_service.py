"""
Queue management service
Handles queue operations, token generation, and patient ordering
"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, Date, cast
from ..models import Queue, Appointment, Patient, QueueLog, Doctor
from ..schemas import QueueDetailResponse


class QueueService:
    """Service for managing patient queues"""

    @staticmethod
    def get_next_token_number(db: Session, doctor_id: int) -> int:
        """Get the next token number for a doctor"""
        # Get the maximum token number for this doctor today
        today = datetime.now().date()
        max_token = db.query(func.max(Queue.token_number)).filter(
            and_(
                Queue.appointment_id.in_(
                    db.query(Appointment.id).filter(
                        and_(
                            Appointment.doctor_id == doctor_id,
                            cast(Appointment.appointment_date, Date) == today
                        )
                    )
                )
            )
        ).scalar()

        return (max_token or 0) + 1

    @staticmethod
    def add_to_queue(db: Session, appointment_id: int, doctor_id: int, priority_score: int) -> Queue:
        """Add appointment to queue"""
        # Get next token number
        token_number = QueueService.get_next_token_number(db, doctor_id)

        # Get queue position
        queue_position = db.query(func.count(Queue.id)).filter(
            and_(
                Queue.appointment_id.in_(
                    db.query(Appointment.id).filter(
                        and_(
                            Appointment.doctor_id == doctor_id,
                            Appointment.status.in_(["waiting", "in_progress"])
                        )
                    )
                )
            )
        ).scalar() + 1

        # Create queue entry
        queue_entry = Queue(
            appointment_id=appointment_id,
            token_number=token_number,
            queue_position=queue_position,
            priority_score=priority_score,
            status="waiting"
        )
        db.add(queue_entry)
        db.commit()
        db.refresh(queue_entry)

        return queue_entry

    @staticmethod
    def get_next_patient(db: Session, doctor_id: int) -> Queue:
        """
        Get next patient to be called
        Sorting: highest priority first, then FIFO (earliest created_at)
        """
        next_patient = db.query(Queue).filter(
            and_(
                Queue.status == "waiting",
                Queue.appointment_id.in_(
                    db.query(Appointment.id).filter(Appointment.doctor_id == doctor_id)
                )
            )
        ).order_by(Queue.priority_score.desc(), Queue.created_at.asc()).first()

        return next_patient

    @staticmethod
    def call_next_patient(db: Session, doctor_id: int) -> dict:
        """
        Call next patient in queue
        Returns patient details and marks appointment as in_progress
        """
        next_patient = QueueService.get_next_patient(db, doctor_id)

        if not next_patient:
            return {"success": False, "message": "No patients waiting"}

        # Update queue status
        next_patient.status = "in_progress"

        # Update appointment status
        appointment = db.query(Appointment).filter(Appointment.id == next_patient.appointment_id).first()
        appointment.status = "in_progress"

        # Get patient details
        patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()

        # Create queue log entry for tracking
        queue_log = QueueLog(
            appointment_id=next_patient.appointment_id,
            arrival_time=next_patient.created_at,
            start_time=datetime.utcnow()
        )
        db.add(queue_log)
        db.commit()

        return {
            "success": True,
            "appointment_id": next_patient.appointment_id,
            "patient_name": patient.name,
            "patient_phone": patient.phone,
            "token_number": next_patient.token_number,
            "priority_score": next_patient.priority_score
        }

    @staticmethod
    def complete_consultation(db: Session, appointment_id: int, doctor_id: int) -> dict:
        """Mark consultation as completed"""
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

        if not appointment or appointment.doctor_id != doctor_id:
            return {"success": False, "message": "Appointment not found"}

        if appointment.status != "in_progress":
            return {"success": False, "message": "Appointment is not in progress"}

        # Update appointment status
        appointment.status = "completed"

        # Update queue status
        queue = db.query(Queue).filter(Queue.appointment_id == appointment_id).first()
        if queue:
            queue.status = "completed"

        # Update queue log
        queue_log = db.query(QueueLog).filter(QueueLog.appointment_id == appointment_id).first()
        if queue_log:
            queue_log.end_time = datetime.utcnow()
            if queue_log.start_time:
                consultation_minutes = int((queue_log.end_time - queue_log.start_time).total_seconds() / 60)
                queue_log.consultation_time_minutes = consultation_minutes
            if queue_log.arrival_time:
                wait_minutes = int((queue_log.start_time - queue_log.arrival_time).total_seconds() / 60)
                queue_log.wait_time_minutes = wait_minutes

        db.commit()

        return {
            "success": True,
            "appointment_id": appointment_id,
            "message": "Consultation marked as completed"
        }

    @staticmethod
    def get_doctor_queue(db: Session, doctor_id: int) -> list:
        """Get full queue for a doctor (sorted by priority and FIFO)"""
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            return []

        queue_entries = db.query(Queue).filter(
            and_(
                Queue.appointment_id.in_(
                    db.query(Appointment.id).filter(Appointment.doctor_id == doctor_id)
                ),
                Queue.status.in_(["waiting", "in_progress"])
            )
        ).order_by(Queue.priority_score.desc(), Queue.created_at.asc()).all()

        result = []
        for queue in queue_entries:
            appointment = db.query(Appointment).filter(Appointment.id == queue.appointment_id).first()
            patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()

            result.append({
                "appointment_id": queue.appointment_id,
                "patient_name": patient.name,
                "token_number": queue.token_number,
                "queue_position": queue.queue_position,
                "priority_score": queue.priority_score,
                "status": queue.status,
                "symptoms": patient.symptoms
            })

        return result

    @staticmethod
    def cancel_appointment(db: Session, appointment_id: int) -> dict:
        """Cancel appointment and remove from queue"""
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

        if not appointment:
            return {"success": False, "message": "Appointment not found"}

        if appointment.status != "waiting":
            return {"success": False, "message": "Can only cancel waiting appointments"}

        # Update appointment status
        appointment.status = "cancelled"

        # Update queue status
        queue = db.query(Queue).filter(Queue.appointment_id == appointment_id).first()
        if queue:
            queue.status = "cancelled"

        # Reorder remaining queue for this doctor
        QueueService.reorder_queue(db, appointment.doctor_id)

        db.commit()

        return {
            "success": True,
            "appointment_id": appointment_id,
            "message": "Appointment cancelled"
        }

    @staticmethod
    def reorder_queue(db: Session, doctor_id: int):
        """Reorder queue positions after cancellation"""
        queue_entries = db.query(Queue).filter(
            and_(
                Queue.appointment_id.in_(
                    db.query(Appointment.id).filter(Appointment.doctor_id == doctor_id)
                ),
                Queue.status.in_(["waiting", "in_progress"])
            )
        ).order_by(Queue.priority_score.desc(), Queue.created_at.asc()).all()

        for position, queue in enumerate(queue_entries, 1):
            queue.queue_position = position

        db.commit()
