"""RouteMate Backend API - Main Application Entry Point"""
from fastapi import FastAPI
from app.core.config import settings
from app.middleware.cors import setup_cors
from app.api.router import api_router

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Community-driven bus tracker API for Sri Lankan transportation",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS middleware
setup_cors(app)

# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": settings.APP_NAME,
    }


@app.get("/health")
async def health():
    """Basic health check"""
    return {"status": "ok", "message": "RouteMate API is running"}