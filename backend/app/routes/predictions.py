"""
ML Prediction routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import PredictionRequest, PredictionResponse
from ..services.ml_model import predict_wait_time
from ..services.prediction_service import PredictionService

router = APIRouter(prefix="/api", tags=["predictions"])


@router.post("/predict-wait-time", response_model=PredictionResponse)
def get_wait_time_prediction(request: PredictionRequest):
    """
    Predict wait time for a patient
    
    - **queue_length**: Number of patients currently in queue
    - **priority_score**: Patient priority score (0-100, higher = more urgent)
    - **doctor_avg_time**: Average doctor consultation time in minutes
    
    Returns predicted wait time in minutes
    """
    predicted_wait = predict_wait_time(
        request.queue_length,
        request.priority_score,
        request.doctor_avg_time
    )

    return PredictionResponse(
        predicted_wait_time=round(predicted_wait, 2),
        queue_length=request.queue_length,
        priority_score=request.priority_score
    )


@router.get("/queue-analytics/{doctor_id}", response_model=dict)
def get_queue_analytics(doctor_id: int, db: Session = Depends(get_db)):
    """Get queue analytics for a specific doctor"""
    analytics = PredictionService.get_queue_analytics(db, doctor_id)
    return analytics
