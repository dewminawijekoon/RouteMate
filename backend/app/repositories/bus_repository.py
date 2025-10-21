"""Bus repository for bus-related database operations"""
from typing import List, Optional, Dict, Any
from supabase import Client
from app.repositories.base import BaseRepository


class BusRepository(BaseRepository):
    """Repository for bus data operations"""
    
    def __init__(self, supabase: Client):
        """
        Initialize bus repository.
        
        Args:
            supabase: Supabase client instance
        """
        super().__init__(supabase, "buses")
    
    async def get_by_route(self, route_id: str) -> List[Dict[str, Any]]:
        """
        Get all buses for a specific route.
        
        Args:
            route_id: The ID of the route
            
        Returns:
            List of buses on the route
        """
        response = self.table.select("*").eq("route_id", route_id).execute()
        return response.data
    
    async def get_by_bus_number(self, bus_number: str) -> Optional[Dict[str, Any]]:
        """
        Get bus by bus number.
        
        Args:
            bus_number: The bus number (e.g., "138")
            
        Returns:
            Bus record or None if not found
        """
        response = self.table.select("*").eq("bus_number", bus_number).execute()
        return response.data[0] if response.data else None
    
    async def get_active_buses(self) -> List[Dict[str, Any]]:
        """
        Get all currently active buses.
        
        Returns:
            List of active buses
        """
        response = self.table.select("*").eq("status", "active").execute()
        return response.data
    
    async def update_location(
        self, 
        bus_id: str, 
        latitude: float, 
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        Update bus location.
        
        Args:
            bus_id: The ID of the bus
            latitude: GPS latitude
            longitude: GPS longitude
            
        Returns:
            Updated bus record or None if not found
        """
        data = {
            "current_location": f"POINT({longitude} {latitude})",
            "last_updated": "NOW()"
        }
        return await self.update(bus_id, data)
    
    async def search_buses(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search buses by number or route.
        
        Args:
            search_term: Search term to match against bus_number
            
        Returns:
            List of matching buses
        """
        response = self.table.select("*").ilike("bus_number", f"%{search_term}%").execute()
        return response.data
