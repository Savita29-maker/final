"""
Integration test for the Smart Patient Queue system
Tests the complete workflow from appointment booking to completion
"""

import requests
import time
from datetime import date

API_URL = "http://localhost:8000/api"


def test_complete_workflow():
    """Test the complete patient queue workflow"""
    print("\n" + "="*70)
    print("  INTEGRATION TEST: Complete Patient Queue Workflow")
    print("="*70 + "\n")

    # Step 1: Create Patient
    print("STEP 1: Create Patient")
    print("-" * 70)
    patient_data = {
        "name": "Integration Test Patient",
        "age": 40,
        "phone": "9111111111",
        "email": "test@integration.com",
        "symptoms": "Test symptoms",
        "priority_score": 60
    }
    
    try:
        response = requests.post(f"{API_URL}/patients", json=patient_data, timeout=10)
        assert response.status_code == 201, f"Failed: {response.text}"
        patient = response.json()
        patient_id = patient["id"]
        print(f"✅ Patient created: {patient['name']} (ID: {patient_id})\n")
    except Exception as e:
        print(f"❌ FAILED: {e}\n")
        return False

    # Step 2: Get Doctors
    print("STEP 2: Get Available Doctors")
    print("-" * 70)
    try:
        response = requests.get(f"{API_URL}/doctors", timeout=10)
        assert response.status_code == 200, f"Failed: {response.text}"
        doctors = response.json()
        assert len(doctors) > 0, "No doctors available"
        doctor_id = doctors[0]["id"]
        print(f"✅ Found {len(doctors)} doctor(s)")
        print(f"   Selected: {doctors[0]['name']} ({doctors[0]['specialization']})\n")
    except Exception as e:
        print(f"❌ FAILED: {e}\n")
        return False

    # Step 3: Book Appointment
    print("STEP 3: Book Appointment")
    print("-" * 70)
    appointment_data = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": str(date.today()),
        "appointment_type": "scheduled"
    }
    
    try:
        response = requests.post(f"{API_URL}/patients/appointments", json=appointment_data, timeout=10)
        assert response.status_code == 201, f"Failed: {response.text}"
        appointment = response.json()
        appointment_id = None
        token_number = appointment["token_number"]
        queue_position = appointment["queue_position"]
        print(f"✅ Appointment booked!")
        print(f"   Token Number: {token_number}")
        print(f"   Queue Position: {queue_position}\n")
    except Exception as e:
        print(f"❌ FAILED: {e}\n")
        return False

    # Step 4: Get Queue
    print("STEP 4: View Doctor's Queue")
    print("-" * 70)
    try:
        response = requests.get(f"{API_URL}/doctors/{doctor_id}/queue", timeout=10)
        assert response.status_code == 200, f"Failed: {response.text}"
        queue = response.json()
        print(f"✅ Queue retrieved!")
        print(f"   Doctor: {queue['doctor_name']} ({queue['specialization']})")
        print(f"   Current Queue Count: {queue['queue_count']}")
        
        for patient_q in queue['queue']:
            if patient_q['token_number'] == token_number:
                appointment_id = patient_q['appointment_id']
                print(f"   Patient in queue: {patient_q['patient_name']} (Token: {patient_q['token_number']})\n")
    except Exception as e:
        print(f"❌ FAILED: {e}\n")
        return False

    # Step 5: Call Next Patient
    print("STEP 5: Doctor Calls Next Patient")
    print("-" * 70)
    try:
        response = requests.post(f"{API_URL}/doctors/{doctor_id}/next-patient", timeout=10)
        assert response.status_code == 200, f"Failed: {response.text}"
        result = response.json()
        print(f"✅ Next patient called!")
        print(f"   {result['message']}\n")
    except Exception as e:
        print(f"❌ FAILED: {e}\n")
        return False

    # Step 6: Get Patient Status
    print("STEP 6: Patient Checks Queue Status")
    print("-" * 70)
    try:
        response = requests.get(f"{API_URL}/patients/{patient_id}/current-status", timeout=10)
        assert response.status_code == 200, f"Failed: {response.text}"
        status = response.json()
        print(f"✅ Patient status retrieved!")
        print(f"   Status: {status['status']}")
        print(f"   Token: {status['token_number']}")
        print(f"   Predicted Wait: {status['predicted_wait_time_minutes']:.1f} minutes\n")
    except Exception as e:
        print(f"❌ FAILED: {e}\n")
        return False

    # Step 7: Test Prediction
    print("STEP 7: Test Wait Time Prediction")
    print("-" * 70)
    try:
        prediction_data = {
            "queue_length": 3,
            "priority_score": 50,
            "doctor_avg_time": 15.0
        }
        response = requests.post(f"{API_URL}/predict-wait-time", json=prediction_data, timeout=10)
        assert response.status_code == 200, f"Failed: {response.text}"
        pred = response.json()
        print(f"✅ Prediction successful!")
        print(f"   Predicted Wait Time: {pred['predicted_wait_time']:.1f} minutes\n")
    except Exception as e:
        print(f"❌ FAILED: {e}\n")
        return False

    # Step 8: Complete Consultation
    print("STEP 8: Doctor Completes Consultation")
    print("-" * 70)
    try:
        response = requests.post(
            f"{API_URL}/doctors/{doctor_id}/complete/{appointment_id}",
            timeout=10
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        result = response.json()
        print(f"✅ Consultation completed!")
        print(f"   Wait Time: {result['wait_time_minutes']} minutes")
        print(f"   Consultation Time: {result['consultation_time_minutes']} minutes\n")
    except Exception as e:
        print(f"❌ FAILED: {e}\n")
        return False

    # Step 9: Admin Dashboard
    print("STEP 9: Admin Views Dashboard")
    print("-" * 70)
    try:
        response = requests.get(f"{API_URL}/admin/dashboard", timeout=10)
        assert response.status_code == 200, f"Failed: {response.text}"
        dashboard = response.json()
        print(f"✅ Dashboard data retrieved!")
        print(f"   Total Patients: {dashboard['total_patients']}")
        print(f"   Total Doctors: {dashboard['total_doctors']}")
        print(f"   Today's Completed: {dashboard['today_completed']}\n")
    except Exception as e:
        print(f"❌ FAILED: {e}\n")
        return False

    print("="*70)
    print("  ✅ ALL TESTS PASSED!")
    print("="*70 + "\n")
    return True


if __name__ == "__main__":
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend health check failed")
            exit(1)
    except:
        print("❌ Cannot connect to backend on http://localhost:8000")
        print("Please start the backend first:")
        print("  cd backend")
        print("  python -m uvicorn app.main:app --reload --port 8000")
        exit(1)

    success = test_complete_workflow()
    exit(0 if success else 1)
