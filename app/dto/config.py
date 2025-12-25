"""Hydra configuration schemas using dataclasses."""

from dataclasses import dataclass
from typing import Optional

from hydra.core.config_store import ConfigStore


@dataclass
class OpenAIConfig:
    """OpenAI configuration."""
    api_key: str


@dataclass
class QdrantConfig:
    """Qdrant configuration."""
    url: str
    api_key: str


@dataclass
class CollectionConfig:
    """Collection configuration."""
    name: str = "ragit_documents"


@dataclass
class DocumentProcessingConfig:
    """Document processing configuration."""
    chunk_size: int = 1000
    chunk_overlap: int = 200


@dataclass
class ModelConfig:
    """Model configuration."""
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0


@dataclass
class RetrievalConfig:
    """Retrieval configuration."""
    k: int = 4


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"


@dataclass
class RagasConfig:
    """RAGAS evaluation configuration."""
    enable_evaluation: bool = True
    timeout_seconds: float = 30.0
    log_results: bool = True
    llm_model: Optional[str] = None
    llm_temperature: Optional[float] = None
    embedding_model: Optional[str] = None


@dataclass
class APIConfig:
    """API configuration."""
    host: str = "0.0.0.0"
    port: int = 8000


@dataclass
class AppConfig:
    """Main application configuration."""
    openai: OpenAIConfig
    qdrant: QdrantConfig
    collection: CollectionConfig
    document_processing: DocumentProcessingConfig
    model: ModelConfig
    retrieval: RetrievalConfig
    logging: LoggingConfig
    ragas: RagasConfig
    api: APIConfig
    app_name: str
    app_version: str


def register_configs() -> None:
    """Register configuration schema with Hydra ConfigStore."""
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=AppConfig)
