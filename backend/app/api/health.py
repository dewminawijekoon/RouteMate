"""Health check endpoints"""
from fastapi import APIRouter
from datetime import datetime
from app.schemas.common import HealthCheck

router = APIRouter()


@router.get("/", response_model=HealthCheck)
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    return HealthCheck(
        status="healthy",
        message="RouteMate API is running",
        timestamp=datetime.utcnow()
    )
