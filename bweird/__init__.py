"""bweird: Beyond WEIRD -- perspective-coverage benchmarking pipeline.

Shared building blocks for the six-stage pipeline. The stage scripts in
``pipeline/`` are thin, argument-parsing wrappers around this package;
``analysis`` is the live analysis core that stages 3-6 import.
See the README for the pipeline DAG.
"""

from __future__ import annotations

__version__ = "1.0.0"
