from fastapi import Request
from omegaconf import DictConfig

def get_cfg(request: Request) -> DictConfig:
    return request.app.state.cfg