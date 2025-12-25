"""Example usage of Hydra configuration with decorators."""

import os

import hydra
from omegaconf import DictConfig

from app.dto.config import register_configs
from app.utils.config_utils import print_config, validate_config, with_config


def setup_test_env():
    """Set up test environment variables."""
    os.environ.setdefault("OPENAI_API_KEY", "sk-test-key-123456789")
    os.environ.setdefault("QDRANT_URL", "https://test.qdrant.io")
    os.environ.setdefault("QDRANT_API_KEY", "test-qdrant-key-123")
    os.environ.setdefault("COLLECTION_NAME", "test_collection")


# ============================================================================
# Example 1: Using @hydra.main decorator (Best for CLI applications)
# ============================================================================
@hydra.main(version_base="1.3", config_path="../conf", config_name="config")
def example_hydra_main(cfg: DictConfig) -> None:
    """
    Example using @hydra.main decorator.
    
    This is the recommended approach for CLI tools and main entry points.
    
    Benefits:
    - Automatic config loading from YAML
    - CLI overrides support (e.g., python script.py model.llm_model=gpt-4)
    - Config validation
    - Working directory management
    
    Usage:
        # Run with default config
        python -m app.examples.config_examples
        
        # Run with CLI overrides
        python -m app.examples.config_examples model.llm_model=gpt-4
        python -m app.examples.config_examples model.llm_model=gpt-4 retrieval.k=10
        
        # Show configuration
        python -m app.examples.config_examples --cfg job
    """
    print("=" * 70)
    print("Example 1: Using @hydra.main Decorator")
    print("=" * 70)
    print()
    
    # Validate configuration
    print("🔍 Validating configuration...")
    validate_config(cfg)
    print("✅ Configuration is valid!")
    print()
    
    # Access configuration values
    print("📋 Configuration Values:")
    print(f"  App Name: {cfg.app_name}")
    print(f"  App Version: {cfg.app_version}")
    print(f"  LLM Model: {cfg.model.llm_model}")
    print(f"  Embedding Model: {cfg.model.embedding_model}")
    print(f"  Temperature: {cfg.model.llm_temperature}")
    print(f"  Chunk Size: {cfg.document_processing.chunk_size}")
    print(f"  Chunk Overlap: {cfg.document_processing.chunk_overlap}")
    print(f"  Retrieval K: {cfg.retrieval.k}")
    print(f"  Collection: {cfg.collection.name}")
    print()
    
    # Access nested configuration
    print("🔐 API Configuration:")
    print(f"  OpenAI API Key: {cfg.openai.api_key[:20]}...")
    print(f"  Qdrant URL: {cfg.qdrant.url}")
    print(f"  Qdrant API Key: {cfg.qdrant.api_key[:20]}...")
    print()
    
    print("🌐 API Server Configuration:")
    print(f"  Host: {cfg.api.host}")
    print(f"  Port: {cfg.api.port}")
    print()
    
    print("📊 RAGAS Evaluation:")
    print(f"  Enabled: {cfg.ragas.enable_evaluation}")
    print(f"  Timeout: {cfg.ragas.timeout_seconds}s")
    print(f"  Log Results: {cfg.ragas.log_results}")
    print()


# ============================================================================
# Example 2: Using @with_config decorator (Best for internal functions)
# ============================================================================
@with_config
def example_with_config_decorator(cfg: DictConfig) -> None:
    """
    Example using custom @with_config decorator.
    
    This is useful for internal functions that need config but aren't entry points.
    
    Benefits:
    - Simpler than @hydra.main
    - No CLI overhead
    - Good for helper functions and utilities
    - Config is automatically injected
    """
    print("=" * 70)
    print("Example 2: Using @with_config Decorator")
    print("=" * 70)
    print()
    
    print("📋 Basic Configuration Access:")
    print(f"  App Name: {cfg.app_name}")
    print(f"  LLM Model: {cfg.model.llm_model}")
    print(f"  Temperature: {cfg.model.llm_temperature}")
    print(f"  Chunk Size: {cfg.document_processing.chunk_size}")
    print()


# ============================================================================
# Example 3: Using config in a class
# ============================================================================
class ConfigurableService:
    """Example service class that uses Hydra configuration."""
    
    def __init__(self, cfg: DictConfig):
        """Initialize service with configuration."""
        self.cfg = cfg
        self.llm_model = cfg.model.llm_model
        self.embedding_model = cfg.model.embedding_model
        self.chunk_size = cfg.document_processing.chunk_size
        self.retrieval_k = cfg.retrieval.k
    
    def get_info(self) -> dict:
        """Get service configuration info."""
        return {
            "llm_model": self.llm_model,
            "embedding_model": self.embedding_model,
            "chunk_size": self.chunk_size,
            "retrieval_k": self.retrieval_k,
        }


@with_config
def example_class_with_config(cfg: DictConfig) -> None:
    """Example showing how to use config with a class."""
    print("=" * 70)
    print("Example 3: Using Config in a Class")
    print("=" * 70)
    print()
    
    # Create service with config
    service = ConfigurableService(cfg)
    
    # Get service info
    info = service.get_info()
    
    print("🔧 Service Configuration:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()


# ============================================================================
# Example 4: Programmatic config access (without decorator)
# ============================================================================
def example_programmatic_access() -> None:
    """
    Example of programmatic config access without decorators.
    
    Useful for:
    - Testing with different configs
    - Dynamic config loading
    - When you need more control
    """
    from app.utils.config_utils import get_config
    
    print("=" * 70)
    print("Example 4: Programmatic Config Access")
    print("=" * 70)
    print()
    
    # Load config with overrides
    cfg = get_config(overrides=(
        "model.llm_model=gpt-4",
        "model.llm_temperature=0.7",
        "retrieval.k=10",
        "document_processing.chunk_size=500",
    ))
    
    print("🔄 Overridden Configuration:")
    print(f"  LLM Model: {cfg.model.llm_model}")
    print(f"  Temperature: {cfg.model.llm_temperature}")
    print(f"  Retrieval K: {cfg.retrieval.k}")
    print(f"  Chunk Size: {cfg.document_processing.chunk_size}")
    print()


# ============================================================================
# Example 5: Print full configuration
# ============================================================================
@with_config
def example_print_config(cfg: DictConfig) -> None:
    """Example showing how to print the full configuration."""
    print("=" * 70)
    print("Example 5: Print Full Configuration")
    print("=" * 70)
    print()
    print_config(cfg)


# ============================================================================
# Main entry point
# ============================================================================
if __name__ == "__main__":
    import sys
    
    # Set up test environment
    setup_test_env()
    
    # Register configs
    register_configs()
    
    # If CLI arguments are provided, use @hydra.main decorator
    # This allows CLI overrides like: python script.py model.llm_model=gpt-4
    if len(sys.argv) > 1:
        print("\n🚀 Running with @hydra.main (supports CLI overrides)\n")
        example_hydra_main()
    else:
        # Otherwise, run all examples
        print("\n🚀 Running All Hydra Configuration Examples\n")
        
        # Example 2: Custom decorator
        example_with_config_decorator()
        
        # Example 3: Class with config
        example_class_with_config()
        
        # Example 4: Programmatic access
        example_programmatic_access()
        
        # Example 5: Print full config
        example_print_config()
        
        print("=" * 70)
        print("✅ All examples completed!")
        print("=" * 70)
        print()
        print("💡 Try running with CLI overrides:")
        print("   python -m app.examples.config_examples model.llm_model=gpt-4")
        print("   python -m app.examples.config_examples model.llm_model=gpt-4 retrieval.k=10")
        print("   python -m app.examples.config_examples --cfg job")
        print()
