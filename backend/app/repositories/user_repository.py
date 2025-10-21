"""User repository for user-related database operations"""
from typing import List, Optional, Dict, Any
from supabase import Client
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Repository for user data operations"""
    
    def __init__(self, supabase: Client):
        """
        Initialize user repository.
        
        Args:
            supabase: Supabase client instance
        """
        super().__init__(supabase, "users")
    
    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email address.
        
        Args:
            email: User's email address
            
        Returns:
            User record or None if not found
        """
        response = self.table.select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    
    async def create_user(self, email: str, name: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            email: User's email address
            name: User's full name
            **kwargs: Additional user fields
            
        Returns:
            Created user record
        """
        data = {
            "email": email,
            "name": name,
            **kwargs
        }
        return await self.create(data)
    
    async def update_profile(
        self, 
        user_id: str, 
        name: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Update user profile.
        
        Args:
            user_id: The ID of the user
            name: Updated name (optional)
            **kwargs: Additional fields to update
            
        Returns:
            Updated user record or None if not found
        """
        data = {}
        if name:
            data["name"] = name
        data.update(kwargs)
        
        return await self.update(user_id, data)
    
    async def get_user_favorites(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get user's favorite routes or buses.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of user's favorites
        """
        # Assuming there's a user_favorites table or relation
        response = (
            self.supabase
            .table("user_favorites")
            .select("*, routes(*), buses(*)")
            .eq("user_id", user_id)
            .execute()
        )
        return response.data
    
    async def add_favorite(
        self, 
        user_id: str, 
        favorite_type: str,
        favorite_id: str
    ) -> Dict[str, Any]:
        """
        Add a route or bus to user's favorites.
        
        Args:
            user_id: The ID of the user
            favorite_type: Type of favorite ('route' or 'bus')
            favorite_id: ID of the route or bus
            
        Returns:
            Created favorite record
        """
        data = {
            "user_id": user_id,
            "favorite_type": favorite_type,
            "favorite_id": favorite_id
        }
        response = self.supabase.table("user_favorites").insert(data).execute()
        return response.data[0]
    
    async def remove_favorite(
        self, 
        user_id: str, 
        favorite_id: str
    ) -> bool:
        """
        Remove a favorite from user's list.
        
        Args:
            user_id: The ID of the user
            favorite_id: ID of the favorite record
            
        Returns:
            True if removed, False if not found
        """
        response = (
            self.supabase
            .table("user_favorites")
            .delete()
            .eq("user_id", user_id)
            .eq("id", favorite_id)
            .execute()
        )
        return len(response.data) > 0
    
    async def get_users_by_role(self, role: str) -> List[Dict[str, Any]]:
        """
        Get all users with a specific role.
        
        Args:
            role: User role (e.g., 'admin', 'driver', 'user')
            
        Returns:
            List of users with the specified role
        """
        response = self.table.select("*").eq("role", role).execute()
        return response.data
