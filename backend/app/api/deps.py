"""App dependencies (e.g. model loader)."""
from __future__ import annotations

from typing import Any

# Set at startup via lifespan; read by get_model()
_model: Any = None


def set_model(model: Any) -> None:
    global _model
    _model = model


def get_model() -> Any:
    return _model
