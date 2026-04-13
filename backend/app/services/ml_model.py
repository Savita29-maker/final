"""
XGBoost ML Model Service
Predicts wait time based on queue parameters
"""
import pickle
import os
import numpy as np
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')


class MLModelService:
    """Service for wait time prediction using XGBoost"""

    def __init__(self):
        """Initialize ML model"""
        self.model_path = "backend/app/services/wait_time_model.pkl"
        self.scaler_path = "backend/app/services/scaler.pkl"
        self.model = None
        self.scaler = None
        self.feature_names = ['queue_length', 'priority_score', 'doctor_avg_time']
        self.load_or_train_model()

    def load_or_train_model(self):
        """Load model if exists, otherwise train on synthetic data"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            # Load existing model
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            print("✅ ML Model loaded successfully")
        else:
            # Train new model
            self.train_model()

    def train_model(self):
        """Train XGBoost model on synthetic data"""
        print("🔄 Training ML Model on synthetic data...")

        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 1000

        # Features
        queue_lengths = np.random.randint(0, 30, n_samples)  # 0-30 patients in queue
        priority_scores = np.random.randint(0, 101, n_samples)  # 0-100 priority
        doctor_avg_times = np.random.uniform(10, 30, n_samples)  # 10-30 min avg consultation

        X = np.column_stack([queue_lengths, priority_scores, doctor_avg_times])

        # Target: wait_time in minutes
        # Logic: wait_time = queue_length * doctor_avg_time - (priority_score influence)
        wait_times = (queue_lengths * 0.8 * doctor_avg_times / 15) - (priority_scores / 10) + np.random.normal(0, 2, n_samples)
        wait_times = np.maximum(wait_times, 0)  # No negative wait times

        # Standardize features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        # Train XGBoost model
        self.model = XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            verbosity=0
        )
        self.model.fit(X_scaled, wait_times)

        # Save model and scaler
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)

        print("✅ ML Model trained and saved")

    def predict_wait_time(self, queue_length: int, priority_score: int, doctor_avg_time: float) -> float:
        """
        Predict wait time for a patient
        
        Args:
            queue_length: Number of patients in queue
            priority_score: Patient priority (0-100)
            doctor_avg_time: Average consultation time in minutes
            
        Returns:
            Predicted wait time in minutes
        """
        if self.model is None or self.scaler is None:
            return 0.0

        # Prepare input
        X = np.array([[queue_length, priority_score, doctor_avg_time]])
        X_scaled = self.scaler.transform(X)

        # Predict
        predicted_wait = self.model.predict(X_scaled)[0]

        # Ensure non-negative prediction
        return float(max(predicted_wait, 0))

    def batch_predict(self, samples: list) -> list:
        """Predict wait times for multiple patients"""
        predictions = []
        for sample in samples:
            wait_time = self.predict_wait_time(
                sample['queue_length'],
                sample['priority_score'],
                sample['doctor_avg_time']
            )
            predictions.append(wait_time)
        return predictions


# Global instance
ml_service = MLModelService()


def predict_wait_time(queue_length: int, priority_score: int, doctor_avg_time: float) -> float:
    """Convenience function for wait time prediction"""
    return ml_service.predict_wait_time(queue_length, priority_score, doctor_avg_time)
