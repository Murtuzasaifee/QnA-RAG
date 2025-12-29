from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):

    question: str = Field(
        ...,
        description="Question to ask",
        min_length=1,
        max_length=1000,
    )
    include_sources: bool = Field(
        default = True,
        description = "Include source documents in response",
    )
    enable_evaluation: bool = Field(
        default = False,
        description = "Enable RAGAS evaluation (faithfulnes, answer relevancy)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is RAG?",
                    "include_sources": True,
                }
            ]
        }
    }


class SourceDocument(BaseModel):
    """Source document information."""

    content: str = Field(..., description="Document content excerpt")
    metadata: dict[str, Any] = Field(..., description="Document metadata")


class QueryResponse(BaseModel):
    """Response for RAG query."""

    question: str = Field(..., description="Original question")
    answer: str = Field(..., description="Generated answer")
    sources: list[SourceDocument] | None = Field(
        None,
        description="Source documents used",
    )
    processing_time_ms: float = Field(
        ...,
        description="Query processing time in milliseconds",
    )
    