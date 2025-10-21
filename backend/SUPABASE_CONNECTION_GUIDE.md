# 🔍 How to Check Supabase Connection

## ✅ Your Connection Status: **WORKING!**

Based on the test results:
- ✅ Environment variables loaded correctly
- ✅ Supabase client initialized successfully  
- ✅ Database connection established
- ✅ Authentication service accessible
- ✅ Project URL: `https://nrjmbfxcgutbghtccept.supabase.co`

---

## 🧪 Method 1: Run the Connection Test Script (Fastest)

```powershell
cd c:\Users\Ranuga\Routemate\RouteMate\backend
uv run python test_supabase_connection.py
```

**What it checks:**
- ✅ Environment variables (.env file)
- ✅ Supabase client initialization
- ✅ Database connectivity
- ✅ Authentication service

---

## 🌐 Method 2: Test via API Endpoints

### Step 1: Make sure server is running
```powershell
cd c:\Users\Ranuga\Routemate\RouteMate\backend
uv run uvicorn main:app --reload
```

### Step 2: Test Health Endpoint
```powershell
# PowerShell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/health/"

# Or visit in browser:
http://127.0.0.1:8000/api/health/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-21T...",
  "version": "0.1.0"
}
```

### Step 3: Test Authentication (Sign Up)
```powershell
$signup = @{
    email = "test@example.com"
    password = "test123"
    full_name = "Test User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/signup" `
    -Method Post `
    -ContentType "application/json" `
    -Body $signup
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "...",
  "user": {
    "id": "uuid-here",
    "email": "test@example.com",
    "full_name": "Test User"
  }
}
```

✅ **If you get a token response = Supabase is working perfectly!**

---

## 📊 Method 3: Check in Supabase Dashboard

### Step 1: Open Supabase Dashboard
1. Go to: https://supabase.com/dashboard
2. Select your project: **nrjmbfxcgutbghtccept**

### Step 2: Verify Project Settings
1. Go to **Settings** → **API**
2. Verify these match your `.env` file:
   - **Project URL**: `https://nrjmbfxcgutbghtccept.supabase.co` ✅
   - **anon public key**: Check against your `SUPABASE_KEY`

### Step 3: Check Authentication
1. Go to **Authentication** → **Providers**
2. Verify **Email** is enabled ✅

### Step 4: Test Users
1. Sign up a test user via your API
2. Go to **Authentication** → **Users**
3. You should see your test users appear here!

---

## 🎯 Method 4: Interactive Test in Swagger UI

### Step 1: Open Swagger Documentation
```
http://127.0.0.1:8000/docs
```

### Step 2: Test Authentication Flow
1. **Sign Up:**
   - Find `POST /api/auth/signup`
   - Click "Try it out"
   - Enter:
     ```json
     {
       "email": "mytest@example.com",
       "password": "secure123",
       "full_name": "My Name"
     }
     ```
   - Click "Execute"
   - ✅ If you get `access_token` → **Connection works!**

2. **Verify in Supabase:**
   - Go to Supabase Dashboard
   - Authentication → Users
   - Your new user should appear!

---

## 🔧 Method 5: Check Configuration Files

### Verify .env file
```powershell
Get-Content .env
```

**Should contain:**
```env
SUPABASE_URL=https://nrjmbfxcgutbghtccept.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SECRET_KEY=your-secret-key
```

### Verify pyproject.toml dependencies
```powershell
Get-Content pyproject.toml | Select-String "supabase"
```

**Should show:**
```toml
"supabase>=2.0.0",
```

---

## ✅ Connection Checklist

Use this checklist to verify everything:

- [ ] `.env` file exists with correct values
- [ ] `SUPABASE_URL` points to your project
- [ ] `SUPABASE_KEY` is the anon/public key
- [ ] `SECRET_KEY` is set (any random string)
- [ ] Run `test_supabase_connection.py` successfully
- [ ] Server starts without errors
- [ ] Health endpoint responds: `http://127.0.0.1:8000/api/health/`
- [ ] Can sign up a test user
- [ ] User appears in Supabase Dashboard
- [ ] Email provider is enabled in Supabase

---

## 🐛 Troubleshooting

### Issue: "Could not connect to Supabase"
**Solution:**
1. Check your internet connection
2. Verify `SUPABASE_URL` in `.env` is correct
3. Make sure it starts with `https://`

### Issue: "Invalid API key"
**Solution:**
1. Go to Supabase Dashboard → Settings → API
2. Copy the **anon public** key (not the service_role key!)
3. Update `SUPABASE_KEY` in `.env`
4. Restart the server

### Issue: "Email already registered"
**Solution:**
- User already exists! This is good - it means Supabase is working!
- Either sign in instead, or use a different email

### Issue: "Table does not exist"
**Solution:**
- This is normal! You haven't created tables yet
- Authentication works without tables
- You can create tables later in Supabase Dashboard

### Issue: "Authentication service unavailable"
**Solution:**
1. Go to Supabase Dashboard
2. Authentication → Providers
3. Enable **Email** provider
4. Save changes

---

## 🎯 Quick Verification Commands

### One-Line Connection Test
```powershell
uv run python test_supabase_connection.py
```

### One-Line Health Check
```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health/
```

### One-Line Auth Test
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/signup" -Method Post -ContentType "application/json" -Body '{"email":"quick@test.com","password":"test123"}'
```

---

## ✨ Your Current Status

Based on the test results:

```
🟢 SUPABASE CONNECTION: ACTIVE
🟢 Environment Variables: ✅ Loaded
🟢 Supabase Client: ✅ Initialized
🟢 Database: ✅ Connected
🟢 Authentication: ✅ Ready
🟢 API Server: ✅ Running

Project: nrjmbfxcgutbghtccept.supabase.co
```

**You're all set! Your backend is properly connected to Supabase! 🎉**

---

## 📚 Additional Resources

- **Supabase Dashboard**: https://supabase.com/dashboard
- **API Docs**: http://127.0.0.1:8000/docs
- **Auth Guide**: `AUTHENTICATION_GUIDE.md`
- **Quick Start**: `AUTH_QUICK_START.md`

---

## 🎉 Next Steps

Now that your connection is verified:

1. ✅ Test user registration in Swagger UI
2. ✅ Create some test users
3. ✅ Check users appear in Supabase Dashboard
4. 🔄 Create your database tables (buses, routes, etc.)
5. 🔄 Implement your business logic
6. 🔄 Build your frontend!

**Your Supabase backend is ready to use!** 🚀
