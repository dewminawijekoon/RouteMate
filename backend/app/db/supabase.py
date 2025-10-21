"""Supabase client initialization and management"""
from supabase import create_client, Client
from app.core.config import settings


def get_supabase_client() -> Client:
    """
    Create and return a Supabase client instance.
    
    Returns:
        Client: Authenticated Supabase client
    """
    supabase: Client = create_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_KEY
    )
    return supabase


def get_supabase_admin_client() -> Client:
    """
    Create and return a Supabase admin client with service role key.
    Use this for server-side operations that bypass RLS.
    
    Returns:
        Client: Authenticated Supabase admin client
    """
    if not settings.SUPABASE_SERVICE_KEY:
        raise ValueError("SUPABASE_SERVICE_KEY not configured")
    
    supabase: Client = create_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_SERVICE_KEY
    )
    return supabase
