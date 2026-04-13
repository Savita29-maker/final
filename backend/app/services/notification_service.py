"""
Notification service for SMS and Email
Sends simulated notifications by default.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Notification, Patient, Appointment
from ..schemas import NotificationCreate

class NotificationService:
    """Service for sending notifications"""

    @staticmethod
    def send_sms(phone: str, message: str) -> bool:
        """
        Simulate sending SMS notification.
        """
        try:
            print(f"\n📱 SMS SIMULATED")
            print(f"   To: {phone}")
            print(f"   Message: {message}")
            print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            return True
        except Exception as e:
            print(f"\n❌ SMS FAILED")
            print(f"   To: {phone}")
            print(f"   Error: {str(e)}\n")
            return False

    @staticmethod
    def send_email(email: str, message: str, subject: str = "Hospital Appointment") -> bool:
        """
        Send Email notification (currently simulated)
        In production, integrate with SendGrid, AWS SES, etc.
        """
        print(f"\n📧 EMAIL SENT")
        print(f"   To: {email}")
        print(f"   Subject: {subject}")
        print(f"   Message: {message}")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        return True

    @staticmethod
    def notify_appointment_booked(db: Session, patient_id: int, appointment_id: int, token_number: int):
        """Notify patient when appointment is booked"""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return False

        message = f"Your appointment is confirmed. Token Number: {token_number}. Please arrive 10 minutes early."
        subject = "Appointment Confirmation"

        # Send SMS
        NotificationService.send_sms(patient.phone, message)

        # Send Email
        NotificationService.send_email(patient.email, message, subject)

        # Log notification
        notification = Notification(
            patient_id=patient_id,
            appointment_id=appointment_id,
            message=message,
            notification_type="booking",
            status="sent"
        )
        db.add(notification)
        db.commit()

        return True

    @staticmethod
    def notify_patient_called(db: Session, patient_id: int, appointment_id: int, token_number: int):
        """Notify patient when doctor calls them"""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return False

        message = f"Please come now, it's your turn! Token: {token_number}. Doctor is waiting."
        subject = "It's Your Turn!"

        # Send SMS (most important for immediate notification)
        NotificationService.send_sms(patient.phone, message)

        # Send Email
        NotificationService.send_email(patient.email, message, subject)

        # Log notification
        notification = Notification(
            patient_id=patient_id,
            appointment_id=appointment_id,
            message=message,
            notification_type="call",
            status="sent"
        )
        db.add(notification)
        db.commit()

        return True

    @staticmethod
    def notify_appointment_cancelled(db: Session, patient_id: int, appointment_id: int):
        """Notify patient when appointment is cancelled"""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return False

        message = "Your appointment has been cancelled. Please book a new appointment at your convenience."
        subject = "Appointment Cancelled"

        # Send SMS
        NotificationService.send_sms(patient.phone, message)

        # Send Email
        NotificationService.send_email(patient.email, message, subject)

        # Log notification
        notification = Notification(
            patient_id=patient_id,
            appointment_id=appointment_id,
            message=message,
            notification_type="cancel",
            status="sent"
        )
        db.add(notification)
        db.commit()

        return True

    @staticmethod
    def send_consultation_fee_notification(db: Session, patient_id: int, fee: float):
        """Notify patient about consultation fee"""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return False

        message = f"Your consultation is complete. Please proceed to billing counter. Estimated fee: ${fee}"
        subject = "Consultation Complete - Billing"

        # Send SMS
        NotificationService.send_sms(patient.phone, message)

        # Send Email
        NotificationService.send_email(patient.email, message, subject)

        return True
