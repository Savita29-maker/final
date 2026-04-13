-- PostgreSQL Schema for Smart Patient Queue System

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    symptoms TEXT,
    priority_score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    specialization VARCHAR(255) NOT NULL,
    avg_consultation_time FLOAT DEFAULT 15.0,  -- minutes
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(id),
    doctor_id INT NOT NULL REFERENCES doctors(id),
    appointment_date DATE NOT NULL,
    appointment_time TIME,
    status VARCHAR(50) DEFAULT 'waiting',  -- waiting, in_progress, completed, cancelled
    appointment_type VARCHAR(50) DEFAULT 'scheduled',  -- scheduled, walk-in
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create queue table
CREATE TABLE IF NOT EXISTS queue (
    id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL REFERENCES appointments(id),
    token_number INT NOT NULL,
    queue_position INT NOT NULL,
    priority_score INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'waiting',  -- waiting, in_progress, completed, cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(appointment_id)
);

-- Create queue_logs table for analytics
CREATE TABLE IF NOT EXISTS queue_logs (
    id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL REFERENCES appointments(id),
    arrival_time TIMESTAMP NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    wait_time_minutes INT,
    consultation_time_minutes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(id),
    appointment_id INT REFERENCES appointments(id),
    message TEXT NOT NULL,
    notification_type VARCHAR(50),  -- booking, call, cancel
    status VARCHAR(50) DEFAULT 'sent',  -- sent, failed
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster queries
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_queue_appointment ON queue(appointment_id);
CREATE INDEX idx_queue_status ON queue(status);
CREATE INDEX idx_queue_priority ON queue(priority_score DESC);
CREATE INDEX idx_notifications_patient ON notifications(patient_id);
