
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

class EvaluationScores(BaseModel):
    """RAGAS evaluation scores."""

    faithfulness: float | None = Field(
        None,
        ge=0.0,
        description="Faithfulness score (0-1): measures factual consistency with sources",
        le=1.0,
    )
    answer_relevancy: float | None = Field(
        None,
        description="Answer relevancy score (0-1): measures relevance to question",
        ge=0.0,
        le=1.0,
    )
    evaluation_time_ms: float | None = Field(
        None,
        description="Time taken for evaluation in milliseconds",
    )
    error: str | None = Field(
        None,
        description="Error message if evaluation failed",
    )