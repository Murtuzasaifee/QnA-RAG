from app.core.document_processor import DocumentProcessor
import hydra
from omegaconf import DictConfig
from app.utils.config_utils import print_config, validate_config, with_config

@with_config
def main(cfg: DictConfig):
    print("Hello from qna-rag!")
    document_processor = DocumentProcessor(cfg)
    document_processor.process_file("test.pdf")


if __name__ == "__main__":
    main()
