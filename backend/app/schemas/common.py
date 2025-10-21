"""Common schema models used across the application"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    message: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    status_code: int


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True
