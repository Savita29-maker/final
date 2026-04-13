# 🎓 User Workflows & Usage Guide

Complete step-by-step guides for each user role in the Smart Patient Queue system.

---

## 👤 Patient Workflow

### Scenario: John Doe books an appointment

#### Step 1: Open Patient Portal
```
URL: http://localhost:8501
Role Selection: 👤 Patient
Tab: 📅 Book Appointment
```

#### Step 2: Fill Appointment Form
```
Full Name:        John Doe
Age:              35
Phone Number:     +91-9876543210
Email:            john.doe@email.com
Symptoms:         Migraine and fever
Priority:         40/100 (Normal)
Select Doctor:    Dr. Sarah Johnson (General Practitioner)
Date:             2024-01-15 (Today)
Time:             10:30 AM
```

#### Step 3: Submit & Confirmation
```
✅ Success Message:
"Your appointment is confirmed. Token Number: 5"

📱 Notifications Sent:
SMS:   "Your appointment is confirmed. Token: 5. Please arrive 10 min early."
Email: "Your appointment is confirmed. Token: 5. Please arrive 10 min early."
```

#### Step 4: Check Current Status (10 minutes later)
```
Tab: 📍 Current Status
Enter Phone: 9876543210

Response:
├─ Token #: 5
├─ Queue Position: 2
├─ Status: Waiting
└─ Predicted Wait: 15 minutes
```

#### Step 5: Patient Called by Doctor
```
Notification Received:
📱 SMS: "Please come now, it's your turn! Token: 5. Doctor is waiting."

Dashboard Update:
├─ Status: IN PROGRESS  (badge turns red)
├─ Queue Position: -  (moved to consultation)
└─ Coming Soon: "You're being treated"
```

#### Step 6: Consultation Complete
```
Notification Received:
📧 Email: "Your consultation is complete. Please proceed to billing counter."

Appointment Status: COMPLETED
├─ Wait Time: 12 minutes
├─ Consultation Duration: 18 minutes
└─ Can now book next appointment if needed
```

#### Step 7: Cancel Appointment (Alternative)
```
Tab: ❌ Cancel Appointment
Enter Phone: 9876543210

Find Appointment:
├─ Token #5
├─ Date: 2024-01-15
└─ Status: WAITING

Click Cancel Button

✅ Confirmation:
"Appointment cancelled"

📱 Notification:
SMS: "Your appointment has been cancelled. Please book a new appointment."

Queue Auto-Reorder:
├─ Token #5 Removed
├─ Remaining queue: [6] [7] [8]
└─ No position change for other patients
```

---

## 👨‍⚕️ Doctor Workflow

### Scenario: Dr. Sarah Johnson manages her queue

#### Step 1: Login to Doctor Portal
```
URL: http://localhost:8501
Role Selection: 👨‍⚕️ Doctor
Select Doctor: Dr. Sarah Johnson
```

#### Step 2: View Current Queue
```
Current Queue - 4 patients

| Token | Position | Patient Name     | Priority | Status  |
|-------|----------|------------------|----------|---------|
| 5     | 1        | John Doe         | 40       | waiting |
| 6     | 2        | Jane Smith       | 80       | waiting |
| 7     | 3        | Raj Patel        | 30       | waiting |
| 8     | 4        | Emily Johnson    | 50       | waiting |

Note: Queue is sorted by:
1. Priority DESC (Jane #6 has higher priority than John #5)
2. FIFO (Within same priority: first come = first served)

Today's Stats:
├─ Completed: 5
├─ Avg Wait: 12.3 min
└─ Avg Consultation: 16.5 min
```

#### Step 3: Call Next Patient
```
Button: 📢 Call Next Patient
Click ↓

System Action:
├─ Selects highest priority patient (Jane #6, priority 80)
├─ Updates status: waiting → in_progress
├─ Logs arrival time for analytics
└─ Triggers notification

Notification to Jane:
📱 SMS: "Please come now, it's your turn! Token: 6. Doctor is waiting."

Doctor's View:
┌─────────────────────────────┐
│ PATIENT CALLED              │
├─────────────────────────────┤
│ Patient: Jane Smith         │
│ Token: 6                    │
│ Priority: 80 (High)         │
│ Phone: +91-9876543201       │
└─────────────────────────────┘
```

#### Step 4: Consultation Ongoing
```
Doctor performs consultation with Jane Smith for ~20 minutes

System shows:
├─ Jane's status: IN PROGRESS
├─ Jane's symptoms: Chest pain (chest pain, shortness of breath)
└─ Can't call next patient until consultation is complete
```

#### Step 5: Mark Consultation as Complete
```
Button: ✅ Complete Consultation
Click ↓

System Action:
├─ Updates consultation status: in_progress → completed
├─ Calculates & logs:
│   ├─ Wait time: 13 minutes (arrival → start)
│   ├─ Consultation time: 20 minutes (start → end)
│   └─ Total time: 33 minutes
├─ Auto-triggers next patient call (Optional in actual system)
└─ Saves analytics data

Confirmation:
✅ Consultation completed
├─ Wait Time: 13 minutes
├─ Consultation Time: 20 minutes
└─ [Next patient auto-called]
```

#### Step 6: Refresh & Continue
```
Button: 🔄 Refresh Queue
Click ↓

Updated Queue - 3 patients (Jane removed, next in line: John)

| Token | Position | Patient Name     | Priority | Status  |
|-------|----------|------------------|----------|---------|
| 5     | 1        | John Doe         | 40       | waiting |
| 7     | 2        | Raj Patel        | 30       | waiting |
| 8     | 3        | Emily Johnson    | 50       | waiting |

Repeat: Call Next Patient → Consultation → Mark Complete
```

#### Step 7: End of Day Summary
```
After consultation with all patients:

Today's Statistics:
├─ Total Appointments: 5
├─ Completed: 5
├─ Average Wait Time: 12.3 minutes
├─ Average Consultation: 17.4 minutes
└─ Patient Throughput: 5 patients/90 minutes
```

---

## ⚙️ Admin Workflow

### Scenario: Hospital Administrator reviews system

#### Step 1: Access Admin Dashboard
```
URL: http://localhost:8501
Role Selection: ⚙️ Admin
Tab: 📊 Dashboard
```

#### Step 2: View System Overview
```
Dashboard Stats:
┌────────────────────────────────────┐
│ SYSTEM OVERVIEW                    │
├────────────────────────────────────┤
│ Total Patients: 156                │
│ Total Doctors: 4                   │
│ Total Appointments: 487            │
│ Current Queue: 8 patients          │
└────────────────────────────────────┘

Today's Stats:
┌────────────────────────────────────┐
│ TODAY (2024-01-15)                 │
├────────────────────────────────────┤
│ Appointments Booked: 14            │
│ Completed: 10                      │
│ Cancelled: 1                       │
│ Notifications Sent: 25             │
└────────────────────────────────────┘
```

#### Step 3: View Detailed Analytics
```
Tab: 📈 Analytics

Appointment Status Breakdown:
├─ Waiting: 5
├─ In Progress: 1
├─ Completed: 10
└─ Cancelled: 1

Appointment Types:
├─ Scheduled: 13
└─ Walk-in: 2

Doctor Performance (Today):
┌─────────────────────────────────────────────────────┐
│ Doctor Name  │ Completed │ Avg Wait │ Avg Consult │
├─────────────────────────────────────────────────────┤
│ Dr. Sarah    │ 5         │ 12.3 min │ 15.2 min    │
│ Dr. Rajesh   │ 3         │ 18.5 min │ 22.1 min    │
│ Dr. Emma     │ 4         │ 10.2 min │ 12.5 min    │
│ Dr. Michael  │ 2         │ 15.8 min │ 28.3 min    │
└─────────────────────────────────────────────────────┘
```

#### Step 4: Add New Doctor
```
Tab: 👨‍⚕️ Manage Doctors

Form:
├─ Doctor Name: Dr. Lisa Patel
├─ Specialization: Dermatologist
└─ Avg Consultation Time: 18 minutes

Button: ➕ Add Doctor
Click ↓

✅ Success:
"Doctor added successfully"
├─ Doctor ID: 5
├─ Name: Dr. Lisa Patel
└─ Specialization: Dermatologist
```

#### Step 5: View All Patients
```
Tab: 👥 Patients

Patients List:
┌──────────────────────────────────────────────────────┐
│ Name          │ Age │ Phone        │ Priority │ Date │
├──────────────────────────────────────────────────────┤
│ John Doe      │ 35  │ 9876543210   │ 40       │ ... │
│ Jane Smith    │ 28  │ 9876543211   │ 80       │ ... │
│ Raj Patel     │ 42  │ 9876543212   │ 30       │ ... │
│ Emily Johnson │ 31  │ 9876543213   │ 50       │ ... │
│ Sarah Wilson  │ 26  │ 9876543214   │ 20       │ ... │
└──────────────────────────────────────────────────────┘

Filters Available:
├─ Search by Name
├─ Filter by Priority
└─ Sort by Registration Date
```

#### Step 6: Generate Reports
```
Insights from Dashboard:
├─ Dr. Emma has lowest average wait time (10.2 min) - Most efficient
├─ Dr. Michael has highest consultation time (28.3 min) - Complex cases
├─ Walk-in ratio: 13% (good scheduling)
├─ Cancellation rate: 6.7% (within acceptable range)
└─ Peak hour: 10-11 AM (4 appointments)

Recommendations:
├─ Add more doctors during peak hours
├─ Consider training Dr. Rajesh on efficiency
└─ Allocate complex cases to Dr. Michael
```

---

## 🔮 Predictor Workflow

### Scenario: Testing Wait Time Predictions

#### Step 1: Access Predictor
```
URL: http://localhost:8501
Role Selection: 🔮 Predictor
```

#### Step 2: Input Parameters
```
Scenario 1: Busy Morning
├─ Patients in Queue: 10
├─ Patient Priority: 50 (Normal)
└─ Doctor Avg Time: 15 minutes

Click: 🔍 Predict Wait Time
↓

Result:
┌─────────────────────────────────────┐
│ Predicted Wait Time: 18.5 minutes   │
├─────────────────────────────────────┤
│ Queue Length: 10                    │
│ Priority Score: 50                  │
└─────────────────────────────────────┘

Interpretation:
Patient with ID asking "When will I see doctor?"
Answer: "Approximately 18-19 minutes based on current queue"
```

#### Step 3: Compare Different Scenarios
```
Scenario 2: High Priority Patient
├─ Queue Length: 15
├─ Priority: 90 (High/Emergency)
└─ Doctor Avg: 15 min

Predicted Wait: 8.2 minutes

Why Less?
├─ Will move ahead in queue (priority 90)
├─ Only need to wait for ~1-2 patients
└─ Even with 15 people, effective queue is smaller

vs.

Scenario 3: Low Priority, Busy Time
├─ Queue Length: 20
├─ Priority: 20 (Low)
└─ Doctor Avg: 15 min

Predicted Wait: 32.5 minutes

Why More?
├─ Will go to end of queue
├─ Must wait for ~18-19 high priority patients
└─ Plus longer average time per patient
```

#### Step 4: Use in Patient Communication
```
Patient asks: "How long will I wait?"

Doctor/Receptionist:
├─ Checks current queue via API
├─ Inputs: queue_length=5, priority=35, doctor_avg=15
├─ Gets prediction: 10.2 minutes
└─ Tells patient: "Approximately 10 minutes"

With notification:
"Predicted wait time: 10 minutes. You'll receive SMS when it's your turn."
```

---

## 🚗 Receptionist Workflow (Walk-in Patient)

### Scenario: Patient walks in without prior appointment

#### Step 1: Patient Arrives
```
Patient walks to reception desk
Receptionist asks:
├─ Name: Michael Brown
├─ Age: 45
├─ Phone: 9112121212
├─ Email: michael@email.com
├─ Symptoms: Sudden headache and dizziness
└─ Reason for visit: Walk-in

Receptionist selects preferred doctor: Dr. Emma Wilson (Pediatrician available)
```

#### Step 2: Book Walk-in Appointment
```
Receptionist uses Patient Portal in 📅 Book Appointment tab

Form:
├─ Name: Michael Brown
├─ Details: [filled]
├─ Appointment Type: walk-in  (selector available)
└─ Date: Today

Click: ✅ Book Appointment
↓

✅ Confirmation:
"Appointment booked successfully. Token Number: 12"
├─ Queue Position: 3
└─ Predicted Wait: 22 minutes

Send SMS to patient's phone:
"Your appointment is confirmed. Token: 12. Please wait in reception."
```

#### Step 3: Patient Waits
```
Patient sits in waiting area
Display shows:
├─ Current Token in Consultation: 10
├─ Waiting Tokens: [11, 12, 13, ...]
├─ Michael's Estimated Time: 22 minutes
└─ Reminder: "You'll receive SMS when it's your turn"
```

#### Step 4: Patient Called
```
Doctor finishes consultation with previous patient
System automatically shows next patient on doctor's screen

Notification sent to Michael:
SMS: "Please come now, it's your turn! Token: 12. Doctor is waiting."

Patient walks into consultation room
```

---

## 🔄 Complete End-to-End Workflow

### Patient Journey: Day View

```
08:00 AM
─────────────────────────────────────
Patient (John) wakes up with fever
Decides to book appointment

08:15 AM
─────────────────────────────────────
Opens Streamlit app (Patient Portal)
Fills appointment form
Selects Dr. Sarah Johnson
Submits booking

✅ Gets Token #5
Queue Position: 2
SMS: "Appointment confirmed. Token: 5"

09:00 AM
─────────────────────────────────────
Patient arrives at hospital
Checks status on app
Token #3, #4 still in queue
Predicted Wait: 15 minutes

09:30 AM
─────────────────────────────────────
Patient in queue position 1
SMS: "You're next! Estimated 5 minutes"

09:40 AM
─────────────────────────────────────
Dr. Sarah finishes with Token #4
Calls next patient: Token #5 (John)

✅ SMS: "Please come, it's your turn! Token: 5"
John enters consultation room

10:00 AM
─────────────────────────────────────
Consultation complete
Dr. Sarah marks "Completed"
Duration: 18 minutes

System logs:
├─ Arrival Time: 09:30 AM
├─ Consultation Start: 09:42 AM
├─ Consultation End: 10:00 AM
├─ Wait Time: 12 minutes
└─ Consultation Duration: 18 minutes

✅ SMS: "Consultation complete. Please go to billing."

10:05 AM
─────────────────────────────────────
Patient receives bill, leaves happy
System analytics updated:
├─ Completed Appointments: +1
├─ Total Wait Time (in logs): +12 min
└─ Doctor Performance: Updated
```

---

## 📊 Data Tracking & Analytics

### What Gets Tracked

```
For Each Patient:
├─ Registration Time
├─ Appointment Booking Time
├─ Queue Entry Time
├─ Consultation Start Time
├─ Consultation End Time
├─ Total Wait Time
├─ Consultation Duration
├─ Priority Level
└─ Appointment Type

Generated Analytics:
├─ Average Wait Time (per doctor, per day)
├─ Average Consultation Time
├─ Patient Throughput
├─ Peak Hours
├─ Doctor Efficiency
├─ Cancellation Rate
└─ Priority Distribution
```

---

## 🎯 Key Interaction Patterns

### 1. Real-Time Queue Updates
```
Doctor marks patient complete
    ↓
Queue auto-refreshes
    ↓
Next patient automatically selected
    ↓
SMS notification sent immediately
    ↓
Doctor sees next patient on screen
```

### 2. Automatic Reordering
```
Patient cancels appointment
    ↓
Queue Service removes from queue
    ↓
Re-sorts remaining patients
    ↓
Updates queue_position for all
    ↓
Other patients unaffected
```

### 3. Smart Priority System
```
High priority (80+) arrives
    ↓
Moves ahead of lower priority
    ↓
Called before them
    ↓
Emergency cases: immediate
    ↓
Critical patients: priority 100
```

---

## 📲 Notification Triggers

### Automatic Notifications Sent

```
1. Appointment Booked
   └─→ SMS + Email: "Appointment confirmed. Token: X"

2. Doctor Calls Patient  
   └─→ SMS: "Please come, it's your turn! Token: X"

3. Appointment Cancelled
   └─→ SMS: "Your appointment has been cancelled"

4. Consultation Complete
   └─→ Email: "Consultation complete. Go to billing counter"

5. Reminder (Upcoming - Optional)
   └─→ SMS: "Appointment in 30 minutes. Please arrive early"
```

---

**This guide covers all major workflows and user interactions in the Smart Patient Queue system.**

For API details, see: [ARCHITECTURE.md](ARCHITECTURE.md)
For setup help, see: [SETUP_GUIDE.md](SETUP_GUIDE.md)
