from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field



class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp",
    )
    version: str = Field(..., description="Application version")


class ReadinessResponse(BaseModel):
    """
    Readiness check response
    """

    status: str = Field(..., description="Service status")
    qdrant_connected: bool = Field(..., description="Qdrant connection status")
    collection_info: dict = Field(..., description="Collection info")