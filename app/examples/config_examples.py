"""Example usage of Hydra configuration."""

import os

from app.utils.config_utils import get_config, print_config


def setup_test_env():
    """Set up test environment variables."""
    os.environ.setdefault("OPENAI_API_KEY", "sk-test-key-123")
    os.environ.setdefault("QDRANT_URL", "https://test.qdrant.io")
    os.environ.setdefault("QDRANT_API_KEY", "test-qdrant-key")
    os.environ.setdefault("COLLECTION_NAME", "test_collection")


def main():
    """Demonstrate Hydra configuration usage."""
    
    # Set up test environment
    setup_test_env()
    
    # Method 1: Get DictConfig (OmegaConf)
    print("=" * 60)
    print("Method 1: Using get_config() - Returns DictConfig")
    print("=" * 60)
    cfg = get_config()
    print(f"App Name: {cfg.app_name}")
    print(f"LLM Model: {cfg.model.llm_model}")
    print(f"Chunk Size: {cfg.document_processing.chunk_size}")
    print()

    # Method 2: Runtime overrides
    print("=" * 60)
    print("Method 2: Using overrides")
    print("=" * 60)
    # Clear cache to allow new config with overrides
    get_config.cache_clear()
    cfg_override = get_config(overrides=(
        "model.llm_model=gpt-4",
        "model.llm_temperature=0.7",
        "retrieval.k=10",
    ))
    print(f"LLM Model (overridden): {cfg_override.model.llm_model}")
    print(f"Temperature (overridden): {cfg_override.model.llm_temperature}")
    print(f"Retrieval K (overridden): {cfg_override.retrieval.k}")
    print()

    # Method 3: Print full config
    print("=" * 60)
    print("Method 3: Print full configuration")
    print("=" * 60)
    # Clear cache and get fresh config
    get_config.cache_clear()
    print_config()


if __name__ == "__main__":
    main()
