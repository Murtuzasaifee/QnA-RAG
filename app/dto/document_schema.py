class DocumentUploadResponse(BaseModel):
    """Response after document upload."""

    message: str = Field(..., description="Status message")
    filename: str = Field(..., description="Uploaded filename")
    chunks_created: int = Field(..., description="Number of chunks created")
    document_ids: list[str] = Field(..., description="List of document IDs")


class DocumentInfo(BaseModel):
    """Document information."""

    source: str = Field(..., description="Document source/filename")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Document metadata",
    )


class DocumentListResponse(BaseModel):
    """Response for listing documents."""

    collection_name: str = Field(..., description="Collection name")
    total_documents: int = Field(..., description="Total document count")
    status: str = Field(..., description="Collection status")