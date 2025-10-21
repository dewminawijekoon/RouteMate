# 🔑 Authentication Quick Reference

## Quick Start Checklist

### 1. Supabase Setup (5 minutes)
- [ ] Go to https://supabase.com/dashboard
- [ ] Select your project
- [ ] Settings → API → Copy `SUPABASE_URL` and `SUPABASE_KEY`
- [ ] Authentication → Providers → Enable **Email**
- [ ] Update your `.env` file with correct values

### 2. Test Authentication (2 minutes)
- [ ] Start server: `uv run uvicorn main:app --reload`
- [ ] Open: http://127.0.0.1:8000/docs
- [ ] Try POST `/api/auth/signup` with test email
- [ ] Copy `access_token` from response
- [ ] Click 🔒 **Authorize** button → Paste token
- [ ] Try GET `/api/auth/me` - should work!

---

## Essential API Endpoints

### Sign Up (Register)
```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

### Sign In (Login)
```http
POST /api/auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Access Protected Endpoint
```http
GET /api/auth/me
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

---

## Files Created

```
backend/
├── app/
│   ├── api/
│   │   └── auth.py                 # ✅ Auth endpoints
│   ├── schemas/
│   │   └── auth.py                 # ✅ Request/Response models
│   ├── services/
│   │   └── auth_service.py         # ✅ Auth business logic
│   └── core/
│       └── security.py             # ✅ Auth dependencies
└── AUTHENTICATION_GUIDE.md         # ✅ Detailed guide
```

---

## Common Commands

### Test with cURL
```bash
# Sign up
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Sign in
curl -X POST http://127.0.0.1:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Get user (with token)
curl -X GET http://127.0.0.1:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Protection Levels

### Public (No auth needed)
```python
@router.get("/buses/")
async def get_buses():
    return {"buses": []}
```

### Protected (Auth required)
```python
from app.core.security import get_current_user

@router.get("/buses/")
async def get_buses(current_user = Depends(get_current_user)):
    return {"buses": [], "user": current_user.email}
```

### Optional Auth
```python
from app.core.security import get_current_user_optional

@router.get("/buses/")
async def get_buses(current_user = Depends(get_current_user_optional)):
    if current_user:
        return {"buses": [], "authenticated": True}
    return {"buses": [], "authenticated": False}
```

---

## Token Flow

1. **Sign Up/Sign In** → Get `access_token` + `refresh_token`
2. **Use access_token** → Access protected endpoints (valid 1 hour)
3. **Token expires** → Use `refresh_token` to get new `access_token`
4. **Refresh token** → POST `/api/auth/refresh` with refresh token

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| "Email already registered" | User exists, use sign in |
| "Invalid credentials" | Wrong email/password |
| "Could not validate credentials" | Token expired or invalid, sign in again |
| "Email not confirmed" | Check email or disable confirmations in Supabase |

---

## Next: Read Full Guide
See `AUTHENTICATION_GUIDE.md` for complete documentation!
