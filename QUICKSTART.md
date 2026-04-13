# 🚀 Getting Started in 5 Minutes

**Quick start guide for the impatient!**

---

## ⚡ TL;DR

1. **Install packages**: `pip install -r requirements.txt`
2. **Setup database**: Create PostgreSQL database, run `psql -d smart_patient_queue -f database/schema.sql`
3. **Start backend**: `cd backend && python -m uvicorn app.main:app --reload --port 8000`
4. **Start frontend**: `cd frontend && streamlit run app.py`
5. **Open browser**: http://localhost:8501
6. **Add sample data** (optional): `python sample_data.py`

---

## 📦 Prerequisites (2 minutes)

```bash
# Check Python version
python --version  # Must be 3.9+

# Check PostgreSQL
psql --version  # Must be installed

# Verify PostgreSQL is running
psql -U postgres -c "SELECT 1"  # Should work
```

---

## ⚙️ Installation (3 minutes)

### Step 1: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database

**Create database**:
```bash
# PostgreSQL must be running!
createdb smart_patient_queue
```

**Load schema**:
```bash
psql -U postgres -d smart_patient_queue -f database/schema.sql
```

**Verify**:
```bash
psql -U postgres -d smart_patient_queue -c "SELECT COUNT(*) FROM patients;"
# Should return: count = 0 (empty table is OK)
```

---

## 🚀 Run Application

### Terminal 1: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start Frontend
```bash
cd frontend
streamlit run app.py
```

**Expected output**:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

## 🌐 Access Application

| Component | URL | Use |
|-----------|-----|-----|
| **Frontend** | http://localhost:8501 | Main app |
| **API** | http://localhost:8000 | Direct API calls |
| **API Docs** | http://localhost:8000/docs | Interactive API |
| **Health** | http://localhost:8000/health | Verify running |

---

## 📊 Quick Test

### 1. Check Backend is Running
```bash
curl http://localhost:8000/health
```

### 2. Create Sample Data (Optional)
```bash
python sample_data.py
```

### 3. Access Frontend
```
Open browser: http://localhost:8501
```

### 4. Try Features
- **Patient Portal**: Book an appointment
- **Doctor Portal**: View queue, call patients
- **Admin Dashboard**: See analytics
- **Predictor**: Try wait time prediction

---

## 🎯 First Steps

### Book Your First Appointment

1. Open http://localhost:8501
2. Select "👤 Patient" from sidebar
3. Click "📅 Book Appointment" tab
4. Fill in form:
   - Name: John Doe
   - Age: 30
   - Phone: 9876543210
   - Email: john@example.com
   - Symptoms: Headache
   - Priority: 50
   - Doctor: Any doctor (click dropdown)
5. Click "✅ Book Appointment"

**Result**:
```
✅ Appointment booked successfully. Token: 1
```

### View as Doctor

1. Select "👨‍⚕️ Doctor" from sidebar
2. Select a doctor from dropdown
3. See the queue with your patient
4. Click "📢 Call Next Patient"
5. Click "✅ Complete Consultation"

### Check Admin Dashboard

1. Select "⚙️ Admin" from sidebar
2. See dashboard with stats
3. View analytics
4. Try other tabs

---

## 🛠️ Common Commands

```bash
# Kill process on port 8000 (if stuck)
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8000
kill -9 <PID>

# Restart PostgreSQL
# Mac:
brew services restart postgresql@15

# Linux:
sudo service postgresql restart

# Clear Streamlit cache
streamlit cache clear
```

---

## ⚠️ Troubleshooting

### "Cannot connect to PostgreSQL"
```bash
# Check if running
psql -U postgres -c "SELECT 1"

# If not, start it:
# Mac: brew services start postgresql@15
# Linux: sudo service postgresql start

# Check credentials in code/env
```

### "Port 8000 already in use"
```bash
# Kill process using port 8000 (see commands above)
# Or use different port: --port 8001
```

### "Cannot connect to API from frontend"
```bash
# Verify backend is actually running
curl http://localhost:8000/health

# Check API_URL in frontend/app.py
```

### "ML model not found"
```bash
# Model trains on first backend start
# Restart backend, wait 30 seconds
```

---

## 📱 Quick Feature Demo

### Patient Flow
```
Book → Get Token → Check Status → Wait → See Queue Position → Called → Done
```

### Doctor Flow
```
View Queue → Call Patient → Consult → Complete → Next Patient
```

### Admin Flow
```
Dashboard → Analytics → Doctor Performance → Add Doctor
```

### Prediction Flow
```
Input Settings → Predict Wait Time → See Estimate
```

---

## 🧪 Run Tests

### Quick Integration Test
```bash
# Ensure backend & frontend are running
python integration_test.py
```

**Tests**:
1. ✅ Create patient
2. ✅ Book appointment
3. ✅ View queue
4. ✅ Call patient
5. ✅ Complete consultation
6. ✅ Predict wait time
7. ✅ Check admin dashboard
8. ✅ Full workflow

---

## 📚 Full Documentation

- **README.md** - Full project overview
- **SETUP_GUIDE.md** - Detailed installation
- **ARCHITECTURE.md** - System design & APIs
- **WORKFLOWS.md** - User workflows
- **VERIFICATION.md** - Checklist

---

## 🎉 That's It!

You now have a fully functional Smart Patient Queue system!

**Next steps**:
1. Explore the frontend at http://localhost:8501
2. Check API docs at http://localhost:8000/docs
3. Read full documentation for advanced features
4. Customize for your use case
5. Deploy to production (update README)

---

## 💡 Quick Tips

- **Add More Doctors**: Use Admin Portal → Manage Doctors
- **Generate Test Data**: `python sample_data.py`
- **Check Logs**: Look at terminal output
- **Real SMS/Email**: See README.md for integration
- **Authentication**: Add JWT (see ARCHITECTURE.md)
- **Deployment**: Use Docker & Gunicorn

---

## 🆘 Need Help?

1. **Setup Issue**: See SETUP_GUIDE.md troubleshooting
2. **API Issue**: Check http://localhost:8000/docs
3. **Feature Issue**: See WORKFLOWS.md
4. **Architecture**: Check ARCHITECTURE.md

---

**Total Time**: ~5 minutes to get started ⏱️
**Difficulty**: Easy ✅
**Status**: Ready to use 🚀
