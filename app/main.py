"""FastAPI application entry point."""

# IMPORTANT: Load .env file FIRST, before any LangChain imports
# This ensures LangSmith environment variables are available for tracing
# ruff: noqa: E402, I001
from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from app import __version__
from app.api.routes import health, documents
from omegaconf import DictConfig
from app.utils.logger import get_logger, setup_logging
from app.utils.config_utils import with_config

@with_config
@asynccontextmanager
async def lifespan(cfg:DictConfig, app:FastAPI):
    """Application lifespan manager."""
    # Startup
    
    # store cfg globally on app.state
    app.state.cfg = cfg
    setup_logging(log_level=cfg.logging.level)
    logger = get_logger(__name__)
    logger.info(f"Starting {cfg.app_name} v{__version__}")
    logger.info(f"Log level: {cfg.logging.level}")

    yield

    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI Appliction
app = FastAPI(
    title="QnA RAG",
    description="""
    ## QnA RAG System API

    A Retrieval-Augmented Generation (RAG) question-answering system built with:
    - **FastAPI** for the API layer
    - **LangChain** for RAG orchestration
    - **Qdrant Cloud** for vector storage
    - **OpenAI** for embeddings and LLM

    ### Features
    - Upload PDF, TXT, and CSV documents
    - Ask questions and get AI-powered answers
    - View source documents for transparency
    - Streaming responses for real-time feedback
        """,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(documents.router)

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""

    cfg = app.state.cfg

    return {
        "message": f"Welcome to {cfg.app_name}",
        "version": __version__,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger = get_logger(__name__)
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
