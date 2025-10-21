"""API router aggregation"""
from fastapi import APIRouter
from app.api import health, auth, users

api_router = APIRouter()

# Include route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
