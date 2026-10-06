"""Shared pytest fixtures: make the numeric-free ``pipeline`` modules importable.

``pipeline/`` has no ``__init__.py`` (it is a script directory, not a
library), so its non-numeric-prefixed modules (``adapter.py``) are only
importable if the repo root is on ``sys.path``.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
