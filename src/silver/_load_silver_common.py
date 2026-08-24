"""Load silver_common from the module directory (always fresh on Databricks)."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def load_silver_common() -> ModuleType:
    module_path = Path(__file__).resolve().parent / "silver_common.py"
    spec = importlib.util.spec_from_file_location("silver_common", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load silver_common from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
