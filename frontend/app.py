"""
Streamlit Frontend Application
Smart Patient Queue & Appointment Predictor
"""
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date, timedelta
import time

# Configure page
st.set_page_config(
    page_title="Smart Patient Queue",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
try:
    API_URL = st.secrets.get("api_url", "http://localhost:8000/api")
except FileNotFoundError:
    API_URL = "http://localhost:8000/api"

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.2em;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #28a745;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #17a2b8;
        color: #0c5460;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        color: #856404;
    }
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state"""
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "patient_id" not in st.session_state:
        st.session_state.patient_id = None
    if "doctor_id" not in st.session_state:
        st.session_state.doctor_id = None
    if "refresh_count" not in st.session_state:
        st.session_state.refresh_count = 0


def show_header():
    """Display application header"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center'>🏥 Smart Patient Queue</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center'>AI-Powered Hospital Management System</p>", unsafe_allow_html=True)



# ======================== LOGIN INTERFACE ========================

def login_page():
    """Login page for role selection and authentication"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center'>👤 User Login</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center'>Select your role to access the system</p>", unsafe_allow_html=True)
        
        st.write("")
        
        # Role selection
        selected_role = st.selectbox(
            "Select Your Role:",
            ["Choose a role...", "👤 Patient", "👨‍⚕️ Doctor", "⚙️ Admin", "📋 Receptionist"],
            key="role_selection"
        )
        
        st.write("")
        
        if selected_role == "Choose a role...":
            st.info("👉 Please select your role above")
        
        elif selected_role == "👤 Patient":
            st.subheader("Patient Login")
            patient_id = st.number_input("Patient ID", min_value=1, step=1, key="login_patient_id")
            patient_name = st.text_input("Your Name", key="login_patient_name")
            
            if st.button("🔓 Login as Patient", key="login_patient_btn"):
                if patient_name.strip():
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Patient"
                    st.session_state.user_id = patient_id
                    st.session_state.user_name = patient_name
                    st.success(f"✅ Welcome, {patient_name}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Please enter your name")
        
        elif selected_role == "👨‍⚕️ Doctor":
            st.subheader("Doctor Login")
            try:
                doctors_response = requests.get(f"{API_URL}/doctors", timeout=5)
                if doctors_response.status_code == 200:
                    doctors = doctors_response.json()
                    if doctors:
                        doctor_options = {f"{d['name']} ({d['specialization']})": d['id'] for d in doctors}
                        selected_doctor = st.selectbox("Select Your Profile", list(doctor_options.keys()), key="login_doctor_select")
                        doctor_id = doctor_options[selected_doctor]
                        doctor_name = selected_doctor.split(" (")[0]
                        
                        if st.button("🔓 Login as Doctor", key="login_doctor_btn"):
                            st.session_state.logged_in = True
                            st.session_state.user_role = "Doctor"
                            st.session_state.user_id = doctor_id
                            st.session_state.user_name = doctor_name
                            st.success(f"✅ Welcome, Dr. {doctor_name}!")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.warning("⚠️ No doctors found in the system")
                        st.info("Run: `python sample_data.py` to add sample data")
                else:
                    st.error("❌ Cannot connect to backend")
            except requests.exceptions.RequestException:
                st.error("❌ Cannot connect to backend. Ensure it's running on port 8000")
        
        elif selected_role == "⚙️ Admin":
            st.subheader("Admin Login")
            admin_password = st.text_input("Admin Password", type="password", key="login_admin_pass")
            
            if st.button("🔓 Login as Admin", key="login_admin_btn"):
                # Simple password check (in production, use proper authentication)
                if admin_password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Admin"
                    st.session_state.user_id = 0
                    st.session_state.user_name = "Administrator"
                    st.success("✅ Welcome, Administrator!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid password")
        
        elif selected_role == "📋 Receptionist":
            st.subheader("Receptionist Login")
            receptionist_id = st.number_input("Receptionist ID", min_value=1, step=1, key="login_receptionist_id")
            receptionist_name = st.text_input("Your Name", key="login_receptionist_name")
            
            if st.button("🔓 Login as Receptionist", key="login_receptionist_btn"):
                if receptionist_name.strip():
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Receptionist"
                    st.session_state.user_id = receptionist_id
                    st.session_state.user_name = receptionist_name
                    st.success(f"✅ Welcome, {receptionist_name}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Please enter your name")
        
        st.write("")
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Backend:** http://localhost:8000")
        with col2:
            st.markdown("**Database:** PostgreSQL")


# ======================== PATIENT INTERFACE ========================

def patient_interface():
    """Patient panel"""
    st.header("👤 Patient Portal")

    tab1, tab2, tab3 = st.tabs(["📅 Book Appointment", "📍 Current Status", "❌ Cancel Appointment"])

    # Tab 1: Book Appointment
    with tab1:
        st.subheader("Book a New Appointment")

        col1, col2 = st.columns(2)

        with col1:
            patient_name = st.text_input("Full Name", key="patient_name_book")
            patient_age = st.number_input("Age", min_value=1, max_value=120, key="patient_age_book")

        with col2:
            patient_phone = st.text_input("Phone Number", key="patient_phone_book")
            patient_email = st.text_input("Email", key="patient_email_book")

        patient_symptoms = st.text_area("Symptoms/Reason for Visit", key="patient_symptoms_book")

        col1, col2 = st.columns(2)

        with col1:
            priority_score = st.slider("Priority (0=low, 100=emergency)", 0, 100, 0, key="priority_book")

        with col2:
            # Fetch doctors
            try:
                doctors_response = requests.get(f"{API_URL}/doctors", timeout=5)
                if doctors_response.status_code == 200:
                    doctors = doctors_response.json()
                    if not doctors:
                        st.warning("⚠️ No doctors available. Please populate sample data first.")
                        st.info("Run: `python sample_data.py`")
                        selected_doctor_id = None
                    else:
                        doctor_options = {f"{d['name']} ({d['specialization']})": d['id'] for d in doctors}
                        selected_doctor = st.selectbox("Select Doctor", options=list(doctor_options.keys()))
                        selected_doctor_id = doctor_options[selected_doctor] if selected_doctor else None
                else:
                    st.error("Could not load doctors. Is the backend running?")
                    selected_doctor_id = None
            except requests.exceptions.RequestException:
                st.error("❌ Cannot connect to backend. Make sure it's running on port 8000")
                selected_doctor_id = None

        col1, col2 = st.columns(2)

        with col1:
            appointment_date = st.date_input("Appointment Date", min_value=date.today())

        with col2:
            appointment_time = st.time_input("Appointment Time (optional)", value=datetime.now().time())

        if st.button("✅ Book Appointment", key="book_apt_btn"):
            if not patient_name or not patient_phone or not patient_email:
                st.error("Please fill in all required fields")
            elif not selected_doctor_id:
                st.error("Please select a doctor")
            else:
                # Create patient
                patient_data = {
                    "name": patient_name,
                    "age": patient_age,
                    "phone": patient_phone,
                    "email": patient_email,
                    "symptoms": patient_symptoms,
                    "priority_score": priority_score
                }

                try:
                    patient_response = requests.post(f"{API_URL}/patients", json=patient_data, timeout=5)

                    if patient_response.status_code == 201:
                        patient_id = patient_response.json()["id"]

                        # Book appointment
                        apt_data = {
                            "patient_id": patient_id,
                            "doctor_id": selected_doctor_id,
                            "appointment_date": str(appointment_date),
                            "appointment_time": str(appointment_time),
                            "appointment_type": "scheduled"
                        }

                        apt_response = requests.post(
                            f"{API_URL}/patients/appointments",
                            json=apt_data,
                            timeout=5
                        )

                        if apt_response.status_code == 201:
                            result = apt_response.json()
                            st.success(f"✅ {result['message']}")
                            st.info(f"📋 Your Token Number: **{result['token_number']}**")
                            st.session_state.patient_id = patient_id
                        else:
                            st.error(f"Failed to book appointment: {apt_response.text}")
                    else:
                        st.error(f"Failed to create patient profile: {patient_response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {str(e)}")

    # Tab 2: Current Status
    with tab2:
        st.subheader("Your Current Queue Status")

        patient_phone_status = st.text_input("Enter your phone number", key="patient_phone_status")

        if st.button("🔍 Check Status", key="check_status_btn"):
            try:
                # Get all patients and find by phone
                patients_response = requests.get(f"{API_URL}/admin/patients-list", timeout=5)

                if patients_response.status_code == 200:
                    patients = patients_response.json()
                    patient = next((p for p in patients if p["phone"] == patient_phone_status), None)

                    if patient:
                        patient_id = patient["patient_id"]
                        status_response = requests.get(
                            f"{API_URL}/patients/{patient_id}/current-status",
                            timeout=5
                        )

                        if status_response.status_code == 200:
                            status = status_response.json()

                            if status["status"] == "no_active_appointment":
                                st.info("No active appointments at the moment")
                            else:
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.metric("Token #", status["token_number"])

                                with col2:
                                    st.metric("Queue Position", status["queue_position"])

                                with col3:
                                    st.metric("Predicted Wait", f"{status['predicted_wait_time_minutes']:.0f} min")

                                st.info(f"Status: **{status['status'].upper()}**")
                        else:
                            st.error("Could not fetch status")
                    else:
                        st.warning("Phone number not found")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")

    # Tab 3: Cancel Appointment
    with tab3:
        st.subheader("Cancel Your Appointment")

        patient_phone_cancel = st.text_input("Enter your phone number", key="patient_phone_cancel")

        if st.button("🔍 Find Appointment", key="find_cancel_btn"):
            try:
                patients_response = requests.get(f"{API_URL}/admin/patients-list", timeout=5)

                if patients_response.status_code == 200:
                    patients = patients_response.json()
                    patient = next((p for p in patients if p["phone"] == patient_phone_cancel), None)

                    if patient:
                        patient_id = patient["patient_id"]
                        apt_response = requests.get(
                            f"{API_URL}/patients/{patient_id}/appointments",
                            timeout=5
                        )

                        if apt_response.status_code == 200:
                            appointments = apt_response.json()
                            waiting_apts = [a for a in appointments if a["status"] == "waiting"]

                            if waiting_apts:
                                for apt in waiting_apts:
                                    col1, col2, col3 = st.columns([2, 1, 1])

                                    with col1:
                                        st.write(f"Token: {apt['token_number']} | Date: {apt['appointment_date']}")

                                    with col3:
                                        if st.button("❌ Cancel", key=f"cancel_{apt['appointment_id']}"):
                                            cancel_response = requests.post(
                                                f"{API_URL}/patients/cancel/{apt['appointment_id']}",
                                                timeout=5
                                            )

                                            if cancel_response.status_code == 200:
                                                st.success("✅ Appointment cancelled")
                                                st.rerun()
                                            else:
                                                st.error("Failed to cancel")
                            else:
                                st.info("No active appointments to cancel")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")


# ======================== DOCTOR INTERFACE ========================

def doctor_interface():
    """Doctor panel"""
    st.header("👨‍⚕️ Doctor Portal")

    # Select doctor
    try:
        doctors_response = requests.get(f"{API_URL}/doctors", timeout=5)
        if doctors_response.status_code == 200:
            doctors = doctors_response.json()
            
            if not doctors:
                st.warning("⚠️ No doctors found in the system. Please populate sample data first.")
                st.info("Run this command to add sample data: `python sample_data.py`")
                return
            
            doctor_options = {d['name']: d['id'] for d in doctors}

            selected_doctor_name = st.selectbox("Select Your Profile", options=list(doctor_options.keys()))
            if selected_doctor_name is None:
                return
            selected_doctor_id = doctor_options[selected_doctor_name]
        else:
            st.error("Could not load doctors")
            return
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to backend")
        return

    col1, col2 = st.columns([2, 1])

    with col2:
        if st.button("🔄 Refresh Queue", key="refresh_queue_btn"):
            st.session_state.refresh_count += 1
            st.rerun()

    # Get queue
    try:
        queue_response = requests.get(f"{API_URL}/doctors/{selected_doctor_id}/queue", timeout=5)

        if queue_response.status_code == 200:
            queue_data = queue_response.json()

            st.subheader(f"Current Queue - {queue_data['queue_count']} patients")

            if queue_data['queue_count'] > 0:
                # Display queue table
                queue_df = pd.DataFrame(queue_data['queue'])
                st.dataframe(
                    queue_df[['token_number', 'queue_position', 'patient_name', 'priority_score', 'status']],
                    use_container_width=True,
                    hide_index=True
                )

                # Call next patient button
                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    if st.button("📢 Call Next Patient", key="next_patient_btn"):
                        next_response = requests.post(
                            f"{API_URL}/doctors/{selected_doctor_id}/next-patient",
                            timeout=5
                        )

                        if next_response.status_code == 200:
                            result = next_response.json()
                            st.success(f"✅ {result['message']}")
                            st.info(f"Patient: **{result['patient_name']}** | Token: **{result['token_number']}**")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(next_response.json().get("detail", "Error"))

                # Complete consultation
                with col2:
                    st.write("---")
                    st.subheader("Mark Completed")

                    if st.button("✅ Complete Consultation", key="complete_btn"):
                        # Get current patient (first in progress)
                        in_progress = next((p for p in queue_data['queue'] if p['status'] == 'in_progress'), None)

                        if in_progress:
                            complete_response = requests.post(
                                f"{API_URL}/doctors/{selected_doctor_id}/complete/{in_progress['appointment_id']}",
                                timeout=5
                            )

                            if complete_response.status_code == 200:
                                result = complete_response.json()
                                st.success("✅ Consultation completed")
                                st.info(
                                    f"Wait Time: {result['wait_time_minutes']}m | "
                                    f"Consultation: {result['consultation_time_minutes']}m"
                                )
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Error completing consultation")
                        else:
                            st.warning("No patient in consultation")

                # Today's stats
                with col3:
                    stats_response = requests.get(f"{API_URL}/doctors/{selected_doctor_id}/today-stats", timeout=5)

                    if stats_response.status_code == 200:
                        stats = stats_response.json()
                        st.write("---")
                        st.subheader("Today's Statistics")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Completed", stats['appointments_completed'])

                        with col2:
                            st.metric("Avg Wait (min)", f"{stats['average_wait_time_minutes']:.1f}")

                        with col3:
                            st.metric("Avg Consult (min)", f"{stats['average_consultation_time_minutes']:.1f}")
            else:
                st.success("✅ No patients waiting - All done for now!")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")


# ======================== ADMIN INTERFACE ========================

def admin_interface():
    """Admin panel"""
    st.header("⚙️ Admin Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Analytics", "👨‍⚕️ Manage Doctors", "👥 Patients"])

    # Tab 1: Dashboard
    with tab1:
        try:
            dashboard_response = requests.get(f"{API_URL}/admin/dashboard", timeout=5)

            if dashboard_response.status_code == 200:
                data = dashboard_response.json()

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total Patients", data['total_patients'])

                with col2:
                    st.metric("Total Doctors", data['total_doctors'])

                with col3:
                    st.metric("Total Appointments", data['total_appointments'])

                with col4:
                    st.metric("Current Queue", data['current_queue_size'])

                st.write("---")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Today's Appts", data['today_appointments'])

                with col2:
                    st.metric("Completed", data['today_completed'])

                with col3:
                    st.metric("Cancelled", data['today_cancelled'])

                with col4:
                    st.metric("Notifications", data['notifications_sent_today'])

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")

    # Tab 2: Analytics
    with tab2:
        try:
            apt_analytics = requests.get(f"{API_URL}/admin/appointments-analytics", timeout=5).json()
            perf_data = requests.get(f"{API_URL}/admin/doctor-performance", timeout=5).json()

            st.subheader("Appointment Status Breakdown")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Waiting", apt_analytics['status_breakdown']['waiting'])

            with col2:
                st.metric("In Progress", apt_analytics['status_breakdown']['in_progress'])

            with col3:
                st.metric("Completed", apt_analytics['status_breakdown']['completed'])

            with col4:
                st.metric("Cancelled", apt_analytics['status_breakdown']['cancelled'])

            st.write("---")
            st.subheader("Doctor Performance")

            perf_df = pd.DataFrame(perf_data)
            st.dataframe(perf_df, use_container_width=True, hide_index=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")

    # Tab 3: Manage Doctors
    with tab3:
        st.subheader("Add New Doctor")

        col1, col2 = st.columns(2)

        with col1:
            doctor_name = st.text_input("Doctor Name", key="new_doctor_name")
            specialization = st.text_input("Specialization", key="new_specialization")

        with col2:
            avg_time = st.number_input("Avg Consultation Time (minutes)", min_value=5, value=15, key="new_avg_time")

        if st.button("➕ Add Doctor", key="add_doctor_btn"):
            if doctor_name and specialization:
                try:
                    add_response = requests.post(
                        f"{API_URL}/admin/doctors",
                        params={
                            "name": doctor_name,
                            "specialization": specialization,
                            "avg_consultation_time": avg_time
                        },
                        timeout=5
                    )

                    if add_response.status_code == 201:
                        st.success("✅ Doctor added successfully")
                        st.rerun()
                    else:
                        st.error("Failed to add doctor")

                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {str(e)}")
            else:
                st.error("Please fill in all fields")

    # Tab 4: Patients List
    with tab4:
        try:
            patients_response = requests.get(f"{API_URL}/admin/patients-list", timeout=5).json()
            patients_df = pd.DataFrame(patients_response)
            st.dataframe(patients_df, use_container_width=True, hide_index=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")


# ======================== WAIT TIME PREDICTION ========================

def prediction_interface():
    """Wait time prediction panel"""
    st.header("🔮 Wait Time Predictor")

    col1, col2, col3 = st.columns(3)

    with col1:
        queue_length = st.slider("Patients in Queue", 0, 50, 5)

    with col2:
        priority_score = st.slider("Priority Score (0-100)", 0, 100, 50)

    with col3:
        doctor_avg_time = st.slider("Doctor Avg Time (minutes)", 5.0, 60.0, 15.0)

    if st.button("🔍 Predict Wait Time", key="predict_btn"):
        try:
            prediction_data = {
                "queue_length": queue_length,
                "priority_score": priority_score,
                "doctor_avg_time": doctor_avg_time
            }

            prediction_response = requests.post(
                f"{API_URL}/predict-wait-time",
                json=prediction_data,
                timeout=5
            )

            if prediction_response.status_code == 200:
                result = prediction_response.json()

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Predicted Wait Time", f"{result['predicted_wait_time']:.1f} min")

                with col2:
                    st.metric("Queue Length", result['queue_length'])

                with col3:
                    st.metric("Priority Score", result['priority_score'])

                st.success("✅ Prediction complete! This estimate helps patients plan their visit.")

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")


# ======================== MAIN APPLICATION ========================

def main():
    """Main application logic"""
    init_session_state()

    show_header()

    # Initialize session state for login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_id = None
        st.session_state.user_name = None

    # Sidebar navigation
    st.sidebar.title("🏥 Navigation")

    if not st.session_state.logged_in:
        # Show login page
        login_page()
        return

    role = st.sidebar.radio(
        "Select Role",
        options=["👤 Patient", "👨‍⚕️ Doctor", "⚙️ Admin", "🔮 Predictor"],
        key="user_role_select"
    )

    st.sidebar.write("---")
    
    # Logout button
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.rerun()
    
    with col2:
        st.write(f"👤 {st.session_state.user_name}")

    st.sidebar.write("---")

    # Route to appropriate interface
    if role == "👤 Patient":
        patient_interface()

    elif role == "👨‍⚕️ Doctor":
        doctor_interface()

    elif role == "⚙️ Admin":
        admin_interface()

    elif role == "🔮 Predictor":
        prediction_interface()


if __name__ == "__main__":
    main()
