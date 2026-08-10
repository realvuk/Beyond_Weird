"""Append-only JSON Lines checkpointing for resumable API stages.

Every API-driven stage writes one JSON object per completed unit of work to
a ``.jsonl`` file, flushing and fsyncing after each append. On restart the
stage reads the file, collects the set of completed keys, and skips them.
A truncated final line (from a crash mid-write) is tolerated and skipped
with a warning; the unit it belonged to is simply redone.
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class JsonlCheckpoint:
    """Append-only JSONL store keyed by a unique string per record."""

    def __init__(self, path: Path, key_field: str = "key") -> None:
        """Initialise the store; parent directories are created on first append."""
        self.path = path
        self.key_field = key_field

    def iter_records(self) -> Iterator[dict[str, Any]]:
        """Yield all valid records on disk in write order, skipping corrupt lines."""
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    record = json.loads(stripped)
                except json.JSONDecodeError:
                    logger.warning(
                        "Skipping corrupt line %d in %s (likely a truncated "
                        "write from an interrupted run)",
                        line_number,
                        self.path,
                    )
                    continue
                if not isinstance(record, dict):
                    logger.warning(
                        "Skipping non-object line %d in %s", line_number, self.path
                    )
                    continue
                yield record

    def completed_keys(self) -> set[str]:
        """Return the set of keys already checkpointed on disk."""
        keys: set[str] = set()
        for record in self.iter_records():
            key = record.get(self.key_field)
            if isinstance(key, str):
                keys.add(key)
        if keys:
            logger.info("Resuming: %d completed records found in %s", len(keys), self.path)
        return keys

    def append(self, record: Mapping[str, Any]) -> None:
        """Append one record and force it to disk (flush + fsync)."""
        if not isinstance(record.get(self.key_field), str):
            raise ValueError(f"Record is missing string key field {self.key_field!r}")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(dict(record), ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()
            os.fsync(handle.fileno())
