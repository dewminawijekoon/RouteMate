"""User-related endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from app.db.supabase import get_supabase_client
from app.core.security import get_current_user
from app.schemas.auth import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current authenticated user profile
    
    Requires: Authentication (Bearer token)
    """
    return current_user


@router.get("/{user_id}")
async def get_user(
    user_id: str, 
    supabase: Client = Depends(get_supabase_client),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get user by ID
    
    Requires: Authentication (Bearer token)
    """
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user: {str(e)}"
        )
