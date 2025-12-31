from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough


from app.core.vector_store import VectorStoreService
from app.core.rag_evalutator import RAGEvaluator

from app.core.rag_evalutator import evaluate
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
        self.evaluator = RAGEvaluator(cfg=cfg)

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
            
    async def arun(self, query: str) -> str:
        """Run the RAG chain.

        Args:
            query: Query string

        Returns:
            Answer string
        """

        try:
            answer = await self.chain.ainvoke(query)
            logger.info("Query processed successfully")
            return answer
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

    
    async def arun_with_sources(self, query: str) -> dict:
        """Execute a RAG query and return sources.

        Args:
            question: User question

        Returns:
            Dictionary with answer and source documents
        """

        try:
            answer = await self.chain.ainvoke(query)

            source_docs = await self.retriever.ainvoke(query)

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


    async def arun_with_evaluation(self, question: str, include_sources: bool = True) -> dict:
        """Execute async RAG query with RAGAS evaluation.

        Args:
            question: User question
            include_sources: Whether to include sources in response

        Returns:
            Dictionary with answer, sources, and evaluation scores
        """
        logger.info(f"Processing query with evaluation: {question[:100]}...")

        try:

            result = await self.arun_with_sources(question)
            answer = result["answer"]
            sources = result["sources"]

            contexts = [source["content"] for source in sources]

            try:
                evaluation = await self.evaluator.aevaluate(
                    question= question,
                    answer= answer,
                    contexts= contexts
                )
                logger.info(
                    f"Evaluation completed - "
                    f"faithfulness={evaluation.get('faithfulness', 'N/A')}, "
                    f"answer_relevancy={evaluation.get('answer_relevancy', 'N/A')}"
                )
            except Exception as e:
                logger.warning(f"Evaluation failed: {e}", exc_info=True)
                evaluation = {
                    "faithfulness": None,
                    "answer_relevancy": None,
                    "evaluation_time_ms": None,
                    "error": str(e),
                }

            return {"answer": answer, "sources": sources, "evaluation": evaluation}

        except Exception as e:
            logger.error(f"Error in query with evaluation: {e}")
            raise


    
    def stream(self, query: str):
        """Stream RAG response.

        Args:
            question: User question

        Yields:
            Response chunks
        """
        logger.info(f"Streaming query: {query[:100]}...")

        try:
            for chunk in self.chain.stream(query):
                yield chunk
        except Exception as e:
            logger.error(f"Error streaming query: {e}")
            raise
            

