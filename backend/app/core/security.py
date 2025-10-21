"""Security utilities and dependencies"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from app.db.supabase import get_supabase_client
from app.services.auth_service import AuthService
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# HTTP Bearer token scheme
security = HTTPBearer()


def get_auth_service(supabase: Client = Depends(get_supabase_client)) -> AuthService:
    """
    Dependency to get authentication service
    
    Args:
        supabase: Supabase client instance
        
    Returns:
        AuthService instance
    """
    return AuthService(supabase)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Dependency to get current authenticated user
    
    Args:
        credentials: HTTP Bearer token from request header
        auth_service: Authentication service instance
        
    Returns:
        Current user information
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        token = credentials.credentials
        user = await auth_service.get_current_user(token)
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Dependency to get current user if authenticated, None otherwise
    Useful for endpoints that work with or without authentication
    
    Args:
        credentials: HTTP Bearer token from request header (optional)
        auth_service: Authentication service instance
        
    Returns:
        Current user information or None
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        user = await auth_service.get_current_user(token)
        return user
    except Exception:
        return None


def require_roles(*required_roles: str):
    """
    Decorator factory for role-based access control
    
    Args:
        required_roles: Roles required to access the endpoint
        
    Returns:
        Dependency function that checks user roles
    """
    async def role_checker(current_user = Depends(get_current_user)):
        # Get user roles from user metadata or database
        # This is a placeholder - implement based on your role system
        user_roles = []  # TODO: Fetch from database or token
        
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    
    return role_checker
