from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Error response."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: str | None = Field(None, description="Detailed error information")


class ValidationErrorResponse(BaseModel):
    """Validation error response."""

    error: str = Field(default="Validation Error", description="Error type")
    message: str = Field(..., description="Error message")
    errors: list[dict] = Field(..., description="Validation errors")
