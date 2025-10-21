"""Authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import (
    UserSignUp, 
    UserSignIn, 
    TokenResponse, 
    UserResponse,
    PasswordReset,
    PasswordUpdate,
    RefreshTokenRequest
)
from app.services.auth_service import AuthService
from app.core.security import get_auth_service, get_current_user

router = APIRouter()


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
    user_data: UserSignUp,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user
    
    - **email**: Valid email address
    - **password**: Minimum 6 characters
    - **full_name**: Optional full name
    - **phone**: Optional phone number
    """
    return await auth_service.sign_up(user_data)


@router.post("/signin", response_model=TokenResponse)
async def sign_in(
    credentials: UserSignIn,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate user and get access token
    
    - **email**: User's email address
    - **password**: User's password
    """
    return await auth_service.sign_in(credentials)


@router.post("/signout")
async def sign_out(
    current_user: UserResponse = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Sign out current user (invalidate token)
    
    Requires: Authentication
    """
    # The token is automatically passed through get_current_user
    return await auth_service.sign_out(current_user.id)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Valid refresh token from previous sign in
    """
    return await auth_service.refresh_token(refresh_data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Requires: Authentication (Bearer token)
    """
    return current_user


@router.post("/password-reset")
async def request_password_reset(
    reset_data: PasswordReset,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Request password reset email
    
    - **email**: User's email address
    """
    return await auth_service.reset_password(reset_data.email)


@router.post("/password-update")
async def update_password(
    password_data: PasswordUpdate,
    current_user: UserResponse = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Update user password
    
    Requires: Authentication
    
    - **new_password**: New password (minimum 6 characters)
    """
    # Extract token from dependency (this is simplified)
    return await auth_service.update_password(current_user.id, password_data.new_password)
