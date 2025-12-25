"""Hydra configuration utilities and helpers."""

from functools import lru_cache
from pathlib import Path

from hydra import compose, initialize_config_dir
from omegaconf import DictConfig, OmegaConf

from app.dto.config import AppConfig, register_configs


@lru_cache
def get_config(overrides: tuple[str, ...] = ()) -> DictConfig:
    """
    Get Hydra configuration.

    Args:
        overrides: Tuple of override strings (e.g., ("model.llm_model=gpt-4",))

    Returns:
        DictConfig: Hydra configuration object

    Example:
        >>> cfg = get_config()
        >>> print(cfg.openai.api_key)
        >>> cfg = get_config(overrides=("model.llm_model=gpt-4",))
    """
    register_configs()
    config_dir = str(Path(__file__).parent.parent / "conf")

    with initialize_config_dir(config_dir=config_dir, version_base="1.3"):
        cfg = compose(config_name="config", overrides=list(overrides))

    return cfg



def print_config(cfg: DictConfig | AppConfig | None = None) -> None:
    """
    Pretty print configuration.

    Args:
        cfg: Configuration object to print (defaults to current config)
    """
    if cfg is None:
        cfg = get_config()

    if isinstance(cfg, DictConfig):
        print(OmegaConf.to_yaml(cfg))
    else:
        dict_cfg = OmegaConf.structured(cfg)
        print(OmegaConf.to_yaml(dict_cfg))
