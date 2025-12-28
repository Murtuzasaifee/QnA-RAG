from app.core.document_processor import DocumentProcessor
from omegaconf import DictConfig
from app.utils.config_utils import with_config, print_config
from app.utils.logger import setup_logging
from app.core.vector_store import VectorStoreService
from app.core.rag_chain import RagChain
import asyncio  

from dotenv import load_dotenv

load_dotenv()

@with_config
def main(cfg: DictConfig):
    print_config(cfg)

    setup_logging(log_level=cfg.logging.level)

    # document_processor = DocumentProcessor(cfg)
    # documents = document_processor.process_file("test.pdf")

    # vector_store_service = VectorStoreService(cfg)
    # vector_store_service.add_documents(documents=documents)

    # search_results = vector_store_service.search("What is Docling?")
    # search_results = vector_store_service.search_with_scores("What is Docling?")
    # print(search_results)

    # print(vector_store_service.get_collection_info())
    # print(vector_store_service.health_check())

    rag_chain = RagChain(cfg)
    # answer = rag_chain.run("What is Muli Headed Attention?")
    # print(answer)

    # answer_with_sources = rag_chain.run_with_sources("What is Docling?")
    # print(answer_with_sources)


@with_config
async def amain(cfg: DictConfig):
    print_config(cfg)

    setup_logging(log_level=cfg.logging.level)

    rag_chain = RagChain(cfg)

    # answer = await rag_chain.arun("What is Muli Headed Attention?")
    # print(answer)

    answer = await rag_chain.arun_with_sources("What is Muli Headed Attention?")
    print(answer)


if __name__ == "__main__":
    # main()
    asyncio.run(amain())
