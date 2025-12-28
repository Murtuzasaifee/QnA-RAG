"""Health check endpoints."""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app import __version__
from app.dto.health_schema import HealthResponse, ReadinessResponse
from app.core.vector_store import VectorStoreService
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/health", tags=["Health"])

@router.get(
    "",
    response_model=HealthResponse,
    summary="Basic health check",
    description="Return basic health status of a service"
)
async def health_check() -> HealthResponse:
    """ Basic health check endpoint """

    logger.debug("Health check requested")
    return HealthResponse(
        status = "Healthy",
        timestamp= datetime.utcnow(),
        version = __version__
    )