# 🔐 Supabase Authentication Setup Guide

## Overview
Your FastAPI backend now has complete Supabase Authentication integration with:
- ✅ User registration (Sign up)
- ✅ User login (Sign in)
- ✅ Token refresh
- ✅ Password reset
- ✅ Protected endpoints
- ✅ JWT token validation

---

## 📋 What You Need to Provide from Supabase

### 1. **Supabase Project Configuration**

Go to your Supabase Dashboard: https://supabase.com/dashboard

#### Get Your API Keys:
1. Select your project
2. Go to **Settings** → **API**
3. Copy these values to your `.env` file:

```env
# Already in your .env - verify these are correct:
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here  # Optional but recommended
```

### 2. **Enable Email Authentication**

1. In Supabase Dashboard → **Authentication** → **Providers**
2. Make sure **Email** provider is **enabled**
3. Configure email settings:
   - **Enable email confirmations** (recommended for production)
   - **Enable email change confirmations** 
   - **Secure password reset**

### 3. **Configure Email Templates (Optional but Recommended)**

1. Go to **Authentication** → **Email Templates**
2. Customize these templates:
   - **Confirm signup** - Sent when users register
   - **Magic Link** - For passwordless login
   - **Change Email Address** - Email change confirmation
   - **Reset Password** - Password reset link

### 4. **SMTP Settings (For Production)**

By default, Supabase limits email sending. For production:

1. Go to **Settings** → **Authentication** → **SMTP Settings**
2. Configure your own SMTP server:
   - **Host**: smtp.gmail.com (or your provider)
   - **Port**: 587 (TLS) or 465 (SSL)
   - **Username**: your-email@gmail.com
   - **Password**: your-app-password
   - **Sender name**: RouteMate
   - **Sender email**: noreply@routemate.com

**Gmail SMTP Setup:**
- Enable 2FA on your Gmail
- Generate an "App Password" (not your regular password)
- Use that app password in SMTP settings

---

## 🚀 API Endpoints Available

### **Public Endpoints** (No authentication required)

#### 1. **Sign Up** - Register new user
```
POST /api/auth/signup
```
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "phone": "+94771234567"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "v1.MjM4NDU3ODk...",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone": "+94771234567"
  }
}
```

#### 2. **Sign In** - Login
```
POST /api/auth/signin
```
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** (Same as Sign Up)

#### 3. **Refresh Token** - Get new access token
```
POST /api/auth/refresh
```
**Request Body:**
```json
{
  "refresh_token": "v1.MjM4NDU3ODk..."
}
```

#### 4. **Password Reset Request**
```
POST /api/auth/password-reset
```
**Request Body:**
```json
{
  "email": "user@example.com"
}
```

---

### **Protected Endpoints** (Require authentication)

All protected endpoints need this header:
```
Authorization: Bearer your-access-token-here
```

#### 5. **Get Current User**
```
GET /api/auth/me
```
**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1...
```

**Response:**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+94771234567",
  "created_at": "2025-10-21T10:30:00Z",
  "email_confirmed_at": "2025-10-21T10:35:00Z"
}
```

#### 6. **Sign Out**
```
POST /api/auth/signout
```
**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1...
```

#### 7. **Update Password**
```
POST /api/auth/password-update
```
**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1...
```
**Request Body:**
```json
{
  "new_password": "newSecurePassword456"
}
```

#### 8. **Get User Profile**
```
GET /api/users/me
```
**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1...
```

---

## 🧪 Testing Authentication

### Using the Swagger UI (http://127.0.0.1:8000/docs)

1. **Sign Up a Test User:**
   - Go to `/api/auth/signup`
   - Click "Try it out"
   - Fill in the request body
   - Click "Execute"
   - Copy the `access_token` from response

2. **Authorize Your Session:**
   - Click the **🔒 Authorize** button at the top
   - Enter: `Bearer your-access-token-here`
   - Click "Authorize"
   - Click "Close"

3. **Test Protected Endpoints:**
   - Now try `/api/auth/me` or `/api/users/me`
   - They should work with your token!

### Using cURL

**Sign Up:**
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

**Sign In:**
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Access Protected Endpoint:**
```bash
curl -X GET "http://127.0.0.1:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🔒 How to Protect Your Endpoints

### Make an endpoint require authentication:

**Before (Public):**
```python
@router.get("/buses/")
async def get_buses():
    # Anyone can access
    return {"buses": []}
```

**After (Protected):**
```python
from app.core.security import get_current_user
from app.schemas.auth import UserResponse

@router.get("/buses/")
async def get_buses(current_user: UserResponse = Depends(get_current_user)):
    # Only authenticated users can access
    # current_user contains user info
    return {"buses": [], "requested_by": current_user.email}
```

### Optional Authentication (works with or without):
```python
from app.core.security import get_current_user_optional

@router.get("/buses/")
async def get_buses(current_user = Depends(get_current_user_optional)):
    if current_user:
        # User is logged in
        return {"buses": [], "user": current_user.email}
    else:
        # User is not logged in (public access)
        return {"buses": []}
```

---

## 📊 Verify in Supabase Dashboard

After users sign up, you can see them:

1. Go to **Authentication** → **Users**
2. You'll see all registered users
3. Click on a user to see details
4. You can manually:
   - Confirm email
   - Reset password
   - Delete user
   - View metadata

---

## 🛠️ Common Issues & Solutions

### Issue 1: "Email already registered"
**Solution:** User already exists. Either use sign in or register with different email.

### Issue 2: "Invalid email or password"
**Solution:** Check credentials. Passwords are case-sensitive.

### Issue 3: "Could not validate credentials"
**Solution:** 
- Token expired (default: 1 hour). Use refresh token.
- Token invalid. Sign in again.
- Check `Authorization: Bearer TOKEN` header format.

### Issue 4: "Email confirmation required"
**Solution:** 
- Check user's email for confirmation link
- Or disable email confirmation in Supabase settings (dev only!)

### Issue 5: "SMTP rate limit exceeded"
**Solution:** 
- Supabase free tier has email limits
- Set up custom SMTP
- Or wait for rate limit to reset

---

## 🔐 Security Best Practices

1. **Access Tokens:**
   - Short-lived (1 hour default)
   - Store in memory/localStorage (frontend)
   - Send in Authorization header

2. **Refresh Tokens:**
   - Long-lived (30 days default)
   - Store securely (httpOnly cookie recommended)
   - Use to get new access tokens

3. **Passwords:**
   - Minimum 6 characters (configured in schema)
   - Supabase handles hashing (bcrypt)
   - Never log or display passwords

4. **Environment Variables:**
   - Keep `.env` file secure
   - Never commit to git
   - Use different keys for dev/prod

5. **CORS:**
   - Already configured in your app
   - Update allowed origins for production

---

## 📝 Next Steps

1. ✅ Verify your Supabase credentials in `.env`
2. ✅ Enable Email provider in Supabase dashboard
3. ✅ Test sign up/sign in in Swagger UI
4. ✅ Check users appear in Supabase Authentication tab
5. ✅ Protect your important endpoints
6. 🔄 Set up custom SMTP for production (optional)
7. 🔄 Customize email templates (optional)
8. 🔄 Add role-based access control (if needed)

---

## 🎉 You're All Set!

Your authentication system is ready to use. Start testing at:
**http://127.0.0.1:8000/docs**

Need help? Check:
- Supabase Auth Docs: https://supabase.com/docs/guides/auth
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
