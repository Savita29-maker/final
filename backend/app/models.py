"""
Database models for Smart Patient Queue System
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Time, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Patient(Base):
    """Patient model"""
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False)
    symptoms = Column(Text)
    priority_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Doctor(Base):
    """Doctor model"""
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=False)
    avg_consultation_time = Column(Float, default=15.0)  # minutes
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Appointment(Base):
    """Appointment model"""
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time)
    status = Column(String(50), default="waiting", index=True)  # waiting, in_progress, completed, cancelled
    appointment_type = Column(String(50), default="scheduled")  # scheduled, walk-in
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Queue(Base):
    """Queue model"""
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False, index=True)
    token_number = Column(Integer, nullable=False)
    queue_position = Column(Integer, nullable=False)
    priority_score = Column(Integer, default=0, index=True)
    status = Column(String(50), default="waiting", index=True)  # waiting, in_progress, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QueueLog(Base):
    """Queue analytics log"""
    __tablename__ = "queue_logs"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    wait_time_minutes = Column(Integer)
    consultation_time_minutes = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    """Notification model"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    message = Column(Text, nullable=False)
    notification_type = Column(String(50))  # booking, call, cancel
    status = Column(String(50), default="sent")  # sent, failed
    timestamp = Column(DateTime, default=datetime.utcnow)
