
from functools import lru_cache

from langchain_openai import OpenAIEmbeddings

from app.utils.logger import get_logger
from omegaconf import DictConfig

logger = get_logger(__name__)

@lru_cache
def get_embeddings(cfg: DictConfig) -> OpenAIEmbeddings:
    """Get cached OpenAI embeddings instance.

    Returns:
        Configured OpenAIEmbeddings instance
    """

    logger.info(f"Initializing embeddings model: {cfg.model.embedding_model}")

    embeddings = OpenAIEmbeddings(
        model=cfg.model.embedding_model,
        openai_api_key=cfg.openai.api_key,
    )
    
    logger.info("OpenAI embeddings initialized successfully")
    return embeddings


class EmbeddingService:
    """Service for generating embeddings."""

    def __init__(self, cfg: DictConfig):
        """Initialize embedding service."""
        self.embeddings = get_embeddings(cfg)
        self.model_name = cfg.model.embedding_model

    def embed_query(self, text: str) -> list[float]:
        """Generate embedding for a single query.

        Args:
            text: Query text

        Returns:
            Embedding vector as list of floats
        """
        logger.debug(f"Generating embedding for query: {text[:50]}...")
        return self.embeddings.embed_query(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple documents.

        Args:
            texts: List of document texts

        Returns:
            List of embedding vectors
        """
        logger.debug(f"Generating embeddings for {len(texts)} documents")
        return self.embeddings.embed_documents(texts)
