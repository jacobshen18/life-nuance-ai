from __future__ import annotations

import os
from pathlib import Path

from life_nuance_ai.training import TrainedRouter, load_router


DEFAULT_ROUTER_PATH = Path("artifacts/router_model.json")


def load_optional_router() -> TrainedRouter | None:
    path = Path(os.getenv("LIFE_NUANCE_ROUTER_MODEL", str(DEFAULT_ROUTER_PATH)))
    if not path.exists():
        return None
    return load_router(path)
