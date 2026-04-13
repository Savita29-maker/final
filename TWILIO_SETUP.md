# 📱 Twilio SMS Notifications Setup

Your system is now **ready to send real SMS notifications** via Twilio! 

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Twilio Account
1. Go to: https://www.twilio.com/console
2. Sign up for **FREE** (creates trial account with $15 credit)
3. Verify your phone number

### Step 2: Get Your Credentials
After signing up, you'll see your **Twilio Console Dashboard**:
- **Account SID**: Copy from the "Account SID" field
- **Auth Token**: Copy from the "Auth Token" field
- **Phone Number**: You'll receive a test phone number (format: +1XXXXXXXXXX)

### Step 3: Update `.env` File
Edit `C:\smart_patient_queue\.env` and add:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

Example:
```
TWILIO_ACCOUNT_SID=AC1234567890abcdef
TWILIO_AUTH_TOKEN=abcdefghijk123456789
TWILIO_PHONE_NUMBER=+12025551234
```

### Step 4: Restart Backend
Stop and restart the backend for changes to take effect:
```powershell
# Terminal 1 - Stop: Press Ctrl+C
# Then run:
cd C:\smart_patient_queue\backend
python -m uvicorn app.main:app --reload --port 8000
```

## ✅ Testing SMS Notifications

1. **Open Frontend**: http://localhost:8501
2. **Login as Patient** with credentials from database
3. **Book an Appointment**
4. **Check Backend Console** - You'll see:
   ```
   ✅ SMS SENT VIA TWILIO
      To: 9876543210
      Message: Your appointment is confirmed...
      SID: SM1234567890abcdef
   ```

## 💬 Twilio Free Trial Information

- ✅ **Free Credits**: $15 (enough for ~150 SMS)
- ✅ **Verified Recipients**: Can send SMS to numbers you verify
- ✅ **Test Phone Numbers**: Receive one free test number
- ⚠️ **Limitations**: Trial accounts can only send to verified numbers

## 🔄 Upgrade to Production (After Trial)

When ready to scale:
1. **Upgrade account** to remove verification limits
2. **SMS costs**: ~$0.0075 per SMS
3. **No code changes needed** - just different credentials

## 📧 Email Notifications (Optional)

Currently email is simulated. To enable real email:

1. **Sign up for SendGrid**: https://sendgrid.com
2. **Install library**:
   ```powershell
   pip install sendgrid
   ```
3. **Update `.env`**:
   ```
   SENDGRID_API_KEY=your_api_key
   SENDGRID_FROM_EMAIL=noreply@yourhospital.com
   ```
4. **Update notification_service.py** with SendGrid integration

## 🆘 Troubleshooting

### SMS Not Sending?
- ✅ Check `.env` file has correct credentials
- ✅ Verify `TWILIO_PHONE_NUMBER` format: `+1234567890`
- ✅ Restart backend service
- ✅ Check backend console for error messages

### Error: "Invalid phone number"?
- Phone must be in international format: `+1234567890`
- Patient phone numbers in database need area code

### "Account suspended"?
- Trial accounts are limited
- Upgrade to production account

## 📞 Phone Number Format

- **International**: `+1` + 10-digit number (USA)
- **Examples**:
  - USA: `+12025551234`
  - India: `+919876543210`  ← Current test data uses this format
  - UK: `+442071838750`

## 🎯 Current System Status

- ✅ SMS Integration: **READY**
- ✅ Twilio Library: **INSTALLED** (pip install twilio)
- ✅ .env File: **CREATED**
- ⏳ Twilio Account: **PENDING** (your setup)
- ⏳ Twilio Credentials: **PENDING** (your input)

---

**Next**: Sign up for Twilio, get credentials, update `.env`, restart backend, and you're done! 🎉
