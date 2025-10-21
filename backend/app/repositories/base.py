"""Base repository with common database operations"""
from typing import Any, Dict, List, Optional, TypeVar, Generic
from supabase import Client


T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Base repository class with common CRUD operations.
    
    All specific repositories should inherit from this class.
    """
    
    def __init__(self, supabase: Client, table_name: str):
        """
        Initialize repository with Supabase client and table name.
        
        Args:
            supabase: Supabase client instance
            table_name: Name of the database table
        """
        self.supabase = supabase
        self.table_name = table_name
        self.table = supabase.table(table_name)
    
    async def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all records from the table.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of records as dictionaries
        """
        query = self.table.select("*")
        
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
            
        response = query.execute()
        return response.data
    
    async def get_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single record by ID.
        
        Args:
            record_id: The ID of the record to retrieve
            
        Returns:
            Record as dictionary or None if not found
        """
        response = self.table.select("*").eq("id", record_id).execute()
        return response.data[0] if response.data else None
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new record.
        
        Args:
            data: Dictionary of field values
            
        Returns:
            Created record as dictionary
        """
        response = self.table.insert(data).execute()
        return response.data[0]
    
    async def update(self, record_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing record.
        
        Args:
            record_id: The ID of the record to update
            data: Dictionary of fields to update
            
        Returns:
            Updated record as dictionary or None if not found
        """
        response = self.table.update(data).eq("id", record_id).execute()
        return response.data[0] if response.data else None
    
    async def delete(self, record_id: str) -> bool:
        """
        Delete a record by ID.
        
        Args:
            record_id: The ID of the record to delete
            
        Returns:
            True if deleted, False if not found
        """
        response = self.table.delete().eq("id", record_id).execute()
        return len(response.data) > 0
    
    async def filter_by(self, **filters) -> List[Dict[str, Any]]:
        """
        Filter records by field values.
        
        Args:
            **filters: Field-value pairs to filter by
            
        Returns:
            List of matching records
        """
        query = self.table.select("*")
        
        for field, value in filters.items():
            query = query.eq(field, value)
            
        response = query.execute()
        return response.data
    
    async def count(self) -> int:
        """
        Count total records in the table.
        
        Returns:
            Total number of records
        """
        response = self.table.select("id", count="exact").execute()
        return response.count if hasattr(response, 'count') else len(response.data)
