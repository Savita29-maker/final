"""
FastAPI main application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from .database import engine
from .models import Base
from .routes import patients, doctors, predictions, admin

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Smart Patient Queue & Appointment Predictor",
    description="Hospital management system with AI-based wait-time prediction",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(predictions.router)
app.include_router(admin.router)


@app.get("/")
def read_root():
    """Health check and API info"""
    return {
        "status": "online",
        "application": "Smart Patient Queue & Appointment Predictor",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "patients": "POST /api/patients, GET /api/patients/{id}",
            "appointments": "POST /api/patients/appointments, GET /api/patients/{id}/appointments",
            "doctors": "POST /api/doctors, GET /api/doctors/{id}/queue",
            "queue": "POST /api/doctors/{id}/next-patient, POST /api/doctors/{id}/complete/{apt_id}",
            "predictions": "POST /api/predict-wait-time",
            "admin": "GET /api/admin/dashboard, GET /api/admin/doctor-performance",
            "docs": "/docs (Swagger UI)"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
