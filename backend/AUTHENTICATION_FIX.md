# 🔧 Authentication Fix - Complete Guide

## ❌ Your Issue: "Invalid email or password"

### What Happened:
You tried to **sign in** (`/api/auth/signin`) with:
- Email: `dewmina@gmail.com`
- Password: `string`

**But this user doesn't exist yet!** You need to **sign up** first.

---

## ✅ Solution: Follow These Steps

### Step 1: Sign Up (Register) First

**Use this endpoint:** `POST /api/auth/signup`

**In Swagger UI (http://127.0.0.1:8000/docs):**

1. Find **POST /api/auth/signup**
2. Click **"Try it out"**
3. Use this JSON:
```json
{
  "email": "dewmina@gmail.com",
  "password": "string",
  "full_name": "Dewmina",
  "phone": "+94771234567"
}
```
4. Click **"Execute"**

**Expected Response (Success):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "v1.abc123...",
  "user": {
    "id": "uuid-here",
    "email": "dewmina@gmail.com",
    "full_name": "Dewmina",
    "phone": "+94771234567"
  }
}
```

✅ **Copy the `access_token`!** You'll need it.

---

### Step 2: Now You Can Sign In

After signing up, you can sign in:

**Use this endpoint:** `POST /api/auth/signin`

**Request:**
```json
{
  "email": "dewmina@gmail.com",
  "password": "string"
}
```

**Response (Same as sign up):**
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "...",
  "user": { ... }
}
```

---

### Step 3: Use the Token for Protected Endpoints

1. Click the **🔒 Authorize** button in Swagger UI
2. Enter: `Bearer YOUR_ACCESS_TOKEN_HERE`
3. Click **Authorize**
4. Now try protected endpoints like:
   - `GET /api/auth/me`
   - `GET /api/users/me`

---

## 🧪 Quick Test with PowerShell

### Sign Up:
```powershell
$signup = @{
    email = "dewmina@gmail.com"
    password = "string"
    full_name = "Dewmina"
    phone = "+94771234567"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/signup" `
    -Method Post `
    -ContentType "application/json" `
    -Body $signup

# Save the token
$token = $response.access_token
Write-Host "Access Token: $token"
```

### Sign In:
```powershell
$signin = @{
    email = "dewmina@gmail.com"
    password = "string"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/signin" `
    -Method Post `
    -ContentType "application/json" `
    -Body $signin

$token = $response.access_token
Write-Host "Signed in! Token: $token"
```

### Use Token:
```powershell
# Get current user
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/me" `
    -Headers @{Authorization="Bearer $token"}
```

---

## ✅ Improved Error Messages

I've updated the code to give you better error messages:

### Sign In Errors:
- ❌ **"Invalid email or password. Please check your credentials or sign up first."**
  - User doesn't exist → Go to `/api/auth/signup`
  - Wrong password → Check your password

- ❌ **"User not found. Please sign up first at /api/auth/signup"**
  - Account doesn't exist → Register first

- ❌ **"Please verify your email address before signing in."**
  - Check your email for confirmation link

### Sign Up Errors:
- ❌ **"Email 'example@email.com' is already registered. Please sign in instead at /api/auth/signin"**
  - User already exists → Use sign in instead

- ❌ **"Invalid email format. Please provide a valid email address."**
  - Fix your email format

- ❌ **"Password does not meet requirements. Must be at least 6 characters."**
  - Use a longer password (minimum 6 characters)

---

## 🔍 Verify in Supabase Dashboard

After signing up:

1. Go to: https://supabase.com/dashboard
2. Select your project: **nrjmbfxcgutbghtccept**
3. Go to **Authentication** → **Users**
4. You should see **dewmina@gmail.com** listed!

---

## 📋 Common Issues & Solutions

### Issue 1: "Email already registered"
**Solution:** 
- The user already exists!
- Use **sign in** instead: `POST /api/auth/signin`
- Or use a different email for testing

### Issue 2: "Invalid email or password" on sign in
**Causes:**
- User doesn't exist → **Sign up first**
- Wrong password → Check your password
- Email not confirmed → Check email for confirmation link

### Issue 3: "Please check your email to confirm"
**Solution:**
- Supabase requires email confirmation (default setting)
- Check your email inbox for confirmation link
- OR disable email confirmation in Supabase:
  1. Dashboard → Authentication → Email Templates
  2. Turn off "Email Confirmations"

### Issue 4: Not receiving confirmation emails
**Solution:**
- Check spam folder
- Supabase free tier has email limits
- Set up custom SMTP (see `AUTHENTICATION_GUIDE.md`)
- Or disable email confirmation for development

---

## 🎯 Complete Authentication Flow

```
1. Sign Up
   ↓
   POST /api/auth/signup
   ↓
   Get access_token & refresh_token
   ↓
2. (Optional) Confirm Email
   ↓
3. Access Protected Endpoints
   ↓
   Authorization: Bearer {access_token}
   ↓
4. Token Expires (after 1 hour)
   ↓
   POST /api/auth/refresh
   ↓
   Get new access_token
```

---

## 🚀 Your Next Steps

1. ✅ Use **POST /api/auth/signup** to register `dewmina@gmail.com`
2. ✅ Save the `access_token` from response
3. ✅ Click **🔒 Authorize** in Swagger UI
4. ✅ Test protected endpoints
5. ✅ Verify user appears in Supabase Dashboard
6. ✅ Try signing in with **POST /api/auth/signin**

---

## 📝 Test Checklist

- [ ] Sign up successful (get access_token)
- [ ] User appears in Supabase Dashboard
- [ ] Can authorize in Swagger UI
- [ ] Can access `/api/auth/me`
- [ ] Can access `/api/users/me`
- [ ] Can sign in with same credentials
- [ ] Can refresh token
- [ ] Can sign out

---

## 🎉 You're All Set!

The authentication system is now working with improved error messages. Follow the steps above and you'll be authenticated successfully!

**Need Help?**
- See `AUTHENTICATION_GUIDE.md` for full documentation
- See `AUTH_QUICK_START.md` for quick commands
- See `SUPABASE_CONNECTION_GUIDE.md` for connection info
