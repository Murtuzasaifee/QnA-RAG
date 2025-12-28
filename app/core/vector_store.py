from functools import lru_cache
from typing import Any
from uuid import uuid4

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.exceptions import UnexpectedResponse
from app.utils.logger import get_logger
from omegaconf import DictConfig
from app.core.embeddings import get_embeddings

logger = get_logger(__name__)

@lru_cache
def get_qdrant_client(cfg: DictConfig) -> QdrantClient:
    """Get cached Qdrant client instance.

    Returns:
        Configured QdrantClient instance
    """
    logger.info(f"Connecting to Qdrant at: {cfg.qdrant.url}")

    client = QdrantClient(
        url=cfg.qdrant.url,
        api_key=cfg.qdrant.api_key,
    )

    logger.info("Qdrant client connected successfully")
    return client


class VectorStoreService:

    def __init__(self, cfg: DictConfig, collection_name: str | None = None):
        self.cfg = cfg
        self.client = get_qdrant_client(cfg)
        self.collection_name = collection_name or cfg.collection.name
        self.embedding = get_embeddings(cfg)

        # Ensure collection exists
        self._ensure_collection()

        # Initialize LangChain Qdrant vector store
        self.vector_store = QdrantVectorStore(
            client = self.client,
            collection_name = self.collection_name,
            embedding = self.embedding
        )

        logger.info(f"VectorStoreService initialized for collection: {self.collection_name}")



    def _ensure_collection(self) -> None:
        """Ensure the collection exists, create if not."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(
                f"Collection '{self.collection_name}' exists with "
                f"{collection_info.points_count} points"
            )
        except UnexpectedResponse:
            logger.info(f"Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.cfg.collection.embedding_dimension,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")


    
    def add_documents(self, documents: list[Document]) -> None:
        """Add documents to the vector store.

        Args:
            documents: List of Document objects to add

        Returns:
            List of document IDs
        """

        if not documents:
            logger.warning("No Documents to add")
            return []

        logger.info(f"Adding {len(documents)} documents to collection")

        # Generate unique IDs for each documents
        ids = [str(uuid4()) for _ in documents]

        # Add to vector store
        self.vector_store.add_documents(documents, ids=ids)

        logger.info(f"Added {len(documents)} documents to collection")
        return ids  


    def search(self, query: str, k: int = 4) -> list[Document]:
        """Search for similar documents in the vector store.

        Args:
            query: Query string
            k: Number of similar documents to retrieve

        Returns:
            List of similar Document objects
        """

        k = k or self.cfg.retrieval.k

        logger.info(f"Searching for similar documents to query: {query}")

        results = self.vector_store.similarity_search(query, k=k)

        logger.info(f"Found {len(results)} similar documents")  
        return results


    def search_with_scores(
        self,
        query : str,
        k : int | None = None
    ) -> list[tuple[Document, float]]:
        """Search for similar documents with relevance scores.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of (Document, score) tuples
        """

        k = k or self.cfg.retrieval.k

        logger.info(f"Searching with scores to query: {query}")

        results = self.vector_store.similarity_search_with_score(query, k=k)

        logger.info(f"Found {len(results)} similar documents with scores")  
        return results


    def get_retriever(self, k : int | None = None) -> Any:
        
        """Get a retriever for the vector store.

        Args:
            k: Number of documents to retrieve

        Returns:
            LangChain retriever object
        """

        k = k or self.cfg.retrieval.k

        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k,
            }
        )

    def delete_collection(self) -> None:
        """Delete the entire collection."""
        logger.warning(f"Deleting collection: {self.collection_name}")
        self.client.delete_collection(self.collection_name)
        logger.info(f"Collection '{self.collection_name}' deleted")


    def get_collection_info(self) -> dict:
        """Get information about the collection.

        Returns:
            Dictionary with collection statistics
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "indexed_vectors_count": info.indexed_vectors_count,
                "status": info.status.value,
            }
        except UnexpectedResponse:
            return {
                "name": self.collection_name,
                "points_count": 0,
                "indexed_vectors_count": 0,
                "status": "not_found",
            }

    def health_check(self) -> bool:
        """Check if vector store is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Vector store health check failed: {e}")
            return False
