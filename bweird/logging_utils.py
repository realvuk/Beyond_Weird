"""Shared logging and CLI plumbing for all pipeline stage scripts."""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Callable
from pathlib import Path

from bweird.errors import BweirdError

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: str = "INFO", log_file: Path | None = None) -> None:
    """Configure root logging: stderr always, plus an optional mirror file."""
    numeric_level = logging.getLevelName(level.upper())
    if not isinstance(numeric_level, int):
        raise ValueError(f"Unknown log level: {level!r}")

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=numeric_level,
        format=_FORMAT,
        datefmt=_DATE_FORMAT,
        handlers=handlers,
        force=True,
    )
    # Third-party HTTP libraries are noisy at INFO/DEBUG.
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


def run_stage(
    parser: argparse.ArgumentParser,
    run: Callable[[argparse.Namespace], int],
    argv: list[str] | None = None,
) -> int:
    """Add the shared logging flags, parse, set up logging, and run one stage.

    Returns the stage's exit code, or 2 on a fatal :class:`BweirdError`.
    """
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    parser.add_argument("--log-file", type=Path, default=None, help="Optional log file")
    args = parser.parse_args(argv)
    setup_logging(args.log_level, args.log_file)
    try:
        return run(args)
    except BweirdError as exc:
        logging.getLogger("bweird").error("Fatal: %s", exc)
        return 2
