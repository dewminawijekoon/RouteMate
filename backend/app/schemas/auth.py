"""Authentication schemas"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserSignUp(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserSignIn(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str
    user: dict


class UserResponse(BaseModel):
    """User information response"""
    id: str
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime
    email_confirmed_at: Optional[datetime] = None


class PasswordReset(BaseModel):
    """Password reset request"""
    email: EmailStr


class PasswordUpdate(BaseModel):
    """Update password"""
    new_password: str = Field(..., min_length=6)


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str
