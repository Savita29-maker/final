"""
Sample data initialization script
Run this to populate the database with sample doctors and demonstrate the system
"""

import requests
import json
from datetime import date, timedelta

API_URL = "http://localhost:8000/api"


def create_sample_doctors():
    """Create sample doctors"""
    doctors = [
        {
            "name": "Dr. Sarah Johnson",
            "specialization": "General Practitioner",
            "avg_consultation_time": 15.0
        },
        {
            "name": "Dr. Rajesh Kumar",
            "specialization": "Cardiologist",
            "avg_consultation_time": 20.0
        },
        {
            "name": "Dr. Emma Wilson",
            "specialization": "Pediatrician",
            "avg_consultation_time": 12.0
        },
        {
            "name": "Dr. Michael Chen",
            "specialization": "Orthopedic Surgeon",
            "avg_consultation_time": 25.0
        }
    ]

    print("\n🏥 Creating Sample Doctors...")
    for doctor in doctors:
        try:
            response = requests.post(
                f"{API_URL}/admin/doctors",
                params=doctor,
                timeout=10
            )
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Created: {result['doctor_name']} ({result['specialization']})")
            else:
                print(f"❌ Failed to create {doctor['name']}: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")


def create_sample_patient_and_appointment():
    """Create a sample patient and appointment"""
    print("\n👤 Creating Sample Patient...")

    patient_data = {
        "name": "Raj Patel",
        "age": 35,
        "phone": "9876543210",
        "email": "raj.patel@email.com",
        "symptoms": "Common cold and mild fever",
        "priority_score": 30
    }

    try:
        # Create patient
        patient_response = requests.post(f"{API_URL}/patients", json=patient_data, timeout=10)
        if patient_response.status_code == 201:
            patient = patient_response.json()
            print(f"✅ Created patient: {patient['name']} (ID: {patient['id']})")

            # Book appointment
            appointment_data = {
                "patient_id": patient['id'],
                "doctor_id": 1,
                "appointment_date": str(date.today()),
                "appointment_type": "scheduled"
            }

            apt_response = requests.post(
                f"{API_URL}/patients/appointments",
                json=appointment_data,
                timeout=10
            )

            if apt_response.status_code == 201:
                apt = apt_response.json()
                print(f"✅ Booked appointment: Token #{apt['token_number']}")
                print(f"   Queue Position: {apt['queue_position']}")
            else:
                print(f"❌ Failed to book appointment: {apt_response.text}")

        else:
            print(f"❌ Failed to create patient: {patient_response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")


def test_prediction():
    """Test ML prediction"""
    print("\n🔮 Testing Wait Time Prediction...")

    prediction_data = {
        "queue_length": 5,
        "priority_score": 50,
        "doctor_avg_time": 15.0
    }

    try:
        response = requests.post(
            f"{API_URL}/predict-wait-time",
            json=prediction_data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction Success!")
            print(f"   Queue Length: {result['queue_length']}")
            print(f"   Priority Score: {result['priority_score']}")
            print(f"   Predicted Wait Time: {result['predicted_wait_time']:.1f} minutes")
        else:
            print(f"❌ Prediction failed: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function"""
    print("\n" + "="*60)
    print("  Smart Patient Queue - Sample Data Generator")
    print("="*60)

    # Check if backend is running
    try:
        health = requests.get("http://localhost:8000/health", timeout=5)
        if health.status_code == 200:
            print("\n✅ Backend is running!\n")
        else:
            print("\n❌ Backend health check failed\n")
            return
    except Exception as e:
        print(f"\n❌ Cannot connect to backend: {e}")
        print("Make sure the backend is running on http://localhost:8000\n")
        return

    # Create sample data
    create_sample_doctors()
    create_sample_patient_and_appointment()
    test_prediction()

    print("\n" + "="*60)
    print("  ✅ Sample data created successfully!")
    print("="*60)
    print("\n📱 Now you can:")
    print("   1. Open Streamlit: http://localhost:8501")
    print("   2. Try the Doctor Portal to see the queue")
    print("   3. Book more appointments in Patient Portal")
    print("   4. Check Admin Dashboard for analytics\n")


if __name__ == "__main__":
    main()
