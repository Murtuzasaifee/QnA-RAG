from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough


from app.core.vector_store import VectorStoreService
from app.utils.logger import get_logger
from omegaconf import DictConfig

logger = get_logger(__name__)

# RAG Prompt Template
RAG_PROMPT_TEMPLATE = """You are a helpful assistant. Answer the question based on the provided context.

If you cannot answer the question based on the context, say "I don't have enough information to answer that question."

Do not make up information. Only use the context provided.

Context:
{context}

Question: {question}

Answer:"""


def format_docs(docs: list[Document]) -> str:
    """Format documents into a single context string.

    Args:
        docs: List of Document objects

    Returns:
        Formatted context string
    """
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


class RagChain:

    """
    RAG Chain for QnA
    """

    def __init__(self, cfg: DictConfig, vector_store_service: VectorStoreService | None = None):
        
        """Initialize RAG chain.

        Args:
            vector_store_service: Optional VectorStoreService instance
        """
        self.cfg = cfg
        self.vector_store_service = vector_store_service or VectorStoreService(cfg)
        self.retriever = self.vector_store_service.get_retriever()

        self.llm = ChatOpenAI(
            model_name=cfg.model.llm_model,
            openai_api_key=cfg.openai.api_key,
            temperature=cfg.model.llm_temperature,
        )

        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        
        # Build the chain
        self.chain = (
            {
                "context" : self.retriever | format_docs,
                "question" : RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser() 
        )

        logger.info("RAG chain initialized successfully")
    

    def run(self, query: str) -> str:
        """Run the RAG chain.

        Args:
            query: Query string

        Returns:
            Answer string
        """

        try:
            answer = self.chain.invoke(query)
            logger.info("Query processed successfully")
            return answer
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

    
    def run_with_sources(self, query: str) -> dict:
        """Execute a RAG query and return sources.

        Args:
            question: User question

        Returns:
            Dictionary with answer and source documents
        """

        try:
            answer = self.chain.invoke(query)

            source_docs = self.retriever.invoke(query)

            sources = [
                {
                    "content": (
                        doc.page_content[:500] + "..."
                        if len(doc.page_content) > 500
                        else doc.page_content
                    ),
                    "metadata": doc.metadata
                }
                for doc in source_docs
            ]

            logger.info(f"Query processed successfully with {len(sources)} sources")

            return {
                "answer": answer,
                "sources": sources
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise   
            
