"""Route repository for route-related database operations"""
from typing import List, Optional, Dict, Any
from supabase import Client
from app.repositories.base import BaseRepository


class RouteRepository(BaseRepository):
    """Repository for route data operations"""
    
    def __init__(self, supabase: Client):
        """
        Initialize route repository.
        
        Args:
            supabase: Supabase client instance
        """
        super().__init__(supabase, "routes")
    
    async def get_by_route_number(self, route_number: str) -> Optional[Dict[str, Any]]:
        """
        Get route by route number.
        
        Args:
            route_number: The route number (e.g., "138")
            
        Returns:
            Route record or None if not found
        """
        response = self.table.select("*").eq("route_number", route_number).execute()
        return response.data[0] if response.data else None
    
    async def get_routes_with_buses(self) -> List[Dict[str, Any]]:
        """
        Get all routes with their associated buses.
        
        Returns:
            List of routes with bus data
        """
        response = (
            self.table
            .select("*, buses(*)")
            .execute()
        )
        return response.data
    
    async def search_routes(
        self, 
        start_location: Optional[str] = None,
        end_location: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search routes by start and/or end location.
        
        Args:
            start_location: Starting location to search for
            end_location: Ending location to search for
            
        Returns:
            List of matching routes
        """
        query = self.table.select("*")
        
        if start_location:
            query = query.ilike("start_location", f"%{start_location}%")
        if end_location:
            query = query.ilike("end_location", f"%{end_location}%")
            
        response = query.execute()
        return response.data
    
    async def get_routes_by_stops(self, stop_name: str) -> List[Dict[str, Any]]:
        """
        Get routes that include a specific stop.
        
        Args:
            stop_name: Name of the stop to search for
            
        Returns:
            List of routes containing the stop
        """
        # Assuming stops is a JSONB array field
        response = (
            self.table
            .select("*")
            .contains("stops", [{"name": stop_name}])
            .execute()
        )
        return response.data
    
    async def get_popular_routes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most popular routes (by usage count or rating).
        
        Args:
            limit: Maximum number of routes to return
            
        Returns:
            List of popular routes
        """
        response = (
            self.table
            .select("*")
            .order("usage_count", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data
