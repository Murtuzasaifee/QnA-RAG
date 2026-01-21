# QnA RAG

A Retrieval-Augmented Generation (RAG) system designed for efficient Question Answering over documents using LangChain, Qdrant, and OpenAI.

## Features

- **Document Ingestion**: Process PDF and DOCX documents with `pypdf` and `python-docx`.
- **Vector Storage**: High-performance vector search using Qdrant.
- **RAG Pipeline**: robust chain for context-aware answers with source tracking.
- **Evaluation**: Integration with RAGAS for pipeline performance metrics.
- **Configuration**: centralized configuration management using Hydra.

## Tech Stack

- **Core**: Python 3.13+, LangChain
- **Database**: Qdrant
- **API**: FastAPI (included dependencies)
- **Utilities**: UV (package management), Structlog (logging)

## Getting Started

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd qna-rag
   ```

2. **Install dependencies**
   ```bash
   uv sync
   # OR
   pip install .
   ```

3. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=sk-...
   QDRANT_URL=...
   QDRANT_API_KEY=...
   ```

### Usage

Run the main entry point to process documents and test the pipeline:

```bash
python main.py
```

Configuration defaults can be managed via Hydra config files or overridden via CLI.

## Configuration

This project adopts [Hydra](https://hydra.cc/) for configuration management to ensure scalability and flexibility.

**Why Hydra?**
- **Modular Design**: Settings are organized into logical groups (e.g., `openai`, `model`, `qdrant`), making the config easy to navigate.
- **Type Safety**: Works with dataclasses to provide autocomplete and catch errors early.
- **Runtime Flexibility**: Allows you to override any parameter via command line argument without changing code.

Key features:
- **Centralized Config**: All settings located in `app/conf/config.yaml`.
- **Environment Variables**: Seamless integration with `.env` files for secrets.
- **CLI Overrides**: Easily modify parameters at runtime (e.g., `model.llm_model=gpt-4`).

For a detailed guide on file structure, usage patterns, and troubleshooting, please refer to [HYDRA_CONFIG.md](./HYDRA_CONFIG.md).
