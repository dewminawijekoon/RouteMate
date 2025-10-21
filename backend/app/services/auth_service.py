"""Authentication service using Supabase Auth"""
from supabase import Client
from fastapi import HTTPException, status
from app.schemas.auth import UserSignUp, UserSignIn, TokenResponse, UserResponse, PasswordReset
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Handle authentication operations with Supabase"""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    async def sign_up(self, user_data: UserSignUp) -> TokenResponse:
        """
        Register a new user
        
        Args:
            user_data: User registration information
            
        Returns:
            TokenResponse with access token and user info
            
        Raises:
            HTTPException: If user already exists or registration fails
        """
        try:
            # Sign up with Supabase Auth
            response = self.supabase.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password,
                "options": {
                    "data": {
                        "full_name": user_data.full_name,
                        "phone": user_data.phone
                    }
                }
            })
            
            if not response.user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create user. Email may already be registered."
                )
            
            # Check if session exists (if email confirmation is disabled, session will exist)
            if response.session:
                return TokenResponse(
                    access_token=response.session.access_token,
                    token_type="bearer",
                    expires_in=response.session.expires_in,
                    refresh_token=response.session.refresh_token,
                    user={
                        "id": response.user.id,
                        "email": response.user.email,
                        "full_name": user_data.full_name,
                        "phone": user_data.phone
                    }
                )
            else:
                # Email confirmation is enabled - return user info without session
                raise HTTPException(
                    status_code=status.HTTP_201_CREATED,
                    detail={
                        "message": "Registration successful! Please check your email to confirm your account.",
                        "email": user_data.email,
                        "user_id": response.user.id
                    }
                )
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Sign up error: {str(e)}")
            error_message = str(e).lower()
            
            # Provide helpful error messages
            if "already" in error_message or "duplicate" in error_message or "unique" in error_message:
                detail = f"Email '{user_data.email}' is already registered. Please sign in instead at /api/auth/signin"
            elif "invalid" in error_message and "email" in error_message:
                detail = "Invalid email format. Please provide a valid email address."
            elif "password" in error_message:
                detail = "Password does not meet requirements. Must be at least 6 characters."
            else:
                detail = f"Registration failed: {str(e)}"
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )
    
    async def sign_in(self, credentials: UserSignIn) -> TokenResponse:
        """
        Authenticate user and return tokens
        
        Args:
            credentials: User login credentials
            
        Returns:
            TokenResponse with access token and user info
            
        Raises:
            HTTPException: If credentials are invalid or user doesn't exist
        """
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": credentials.email,
                "password": credentials.password
            })
            
            if not response.user or not response.session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password. Please check your credentials or sign up first."
                )
            
            return TokenResponse(
                access_token=response.session.access_token,
                token_type="bearer",
                expires_in=response.session.expires_in,
                refresh_token=response.session.refresh_token,
                user={
                    "id": response.user.id,
                    "email": response.user.email,
                    "full_name": response.user.user_metadata.get("full_name"),
                    "phone": response.user.user_metadata.get("phone")
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Sign in error: {str(e)}")
            error_message = str(e).lower()
            
            # Provide helpful error messages based on the error
            if "invalid login credentials" in error_message or "invalid" in error_message:
                detail = "Invalid email or password. Please check your credentials or sign up first at /api/auth/signup"
            elif "email not confirmed" in error_message or "email confirmation" in error_message:
                detail = "Please verify your email address before signing in. Check your inbox for the confirmation link."
            elif "user not found" in error_message or "not found" in error_message:
                detail = "User not found. Please sign up first at /api/auth/signup"
            elif "password" in error_message and "weak" in error_message:
                detail = "Password is too weak. Please use a stronger password."
            else:
                # Show actual error for debugging
                detail = f"Sign in failed: {str(e)}"
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail
            )
    
    async def sign_out(self, access_token: str) -> dict:
        """
        Sign out user and invalidate token
        
        Args:
            access_token: User's access token
            
        Returns:
            Success message
        """
        try:
            self.supabase.auth.sign_out()
            return {"message": "Successfully signed out"}
        except Exception as e:
            logger.error(f"Sign out error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to sign out: {str(e)}"
            )
    
    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: User's refresh token
            
        Returns:
            New TokenResponse with refreshed tokens
        """
        try:
            response = self.supabase.auth.refresh_session(refresh_token)
            
            if not response.session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired refresh token"
                )
            
            return TokenResponse(
                access_token=response.session.access_token,
                token_type="bearer",
                expires_in=response.session.expires_in,
                refresh_token=response.session.refresh_token,
                user={
                    "id": response.user.id,
                    "email": response.user.email
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Refresh token error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
    
    async def get_current_user(self, access_token: str) -> UserResponse:
        """
        Get current user information from token
        
        Args:
            access_token: User's access token
            
        Returns:
            UserResponse with user information
        """
        try:
            response = self.supabase.auth.get_user(access_token)
            
            if not response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )
            
            return UserResponse(
                id=response.user.id,
                email=response.user.email,
                full_name=response.user.user_metadata.get("full_name"),
                phone=response.user.user_metadata.get("phone"),
                created_at=response.user.created_at,
                email_confirmed_at=response.user.email_confirmed_at
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Get user error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
    
    async def reset_password(self, email: str) -> dict:
        """
        Send password reset email
        
        Args:
            email: User's email address
            
        Returns:
            Success message
        """
        try:
            self.supabase.auth.reset_password_email(email)
            return {
                "message": "Password reset email sent. Please check your inbox."
            }
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            # Don't reveal if email exists or not for security
            return {
                "message": "If the email exists, a password reset link has been sent."
            }
    
    async def update_password(self, access_token: str, new_password: str) -> dict:
        """
        Update user password
        
        Args:
            access_token: User's access token
            new_password: New password
            
        Returns:
            Success message
        """
        try:
            self.supabase.auth.update_user({
                "password": new_password
            })
            return {"message": "Password updated successfully"}
        except Exception as e:
            logger.error(f"Update password error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update password: {str(e)}"
            )
