#!/usr/bin/env python3
"""Stage 1: query target LLMs for sociopolitical perspectives.

For every (generator model, topic) cell, sends the generation prompt through
OpenRouter at temperature zero and stores the parsed perspectives in an append-only JSONL
checkpoint. Cells already present in the checkpoint are skipped, so an
interrupted run resumes exactly where it stopped.

Cells that fail permanently (API exhaustion or unparseable output after one
repair attempt) are logged to a separate failures file and left out of the
checkpoint; re-running the script retries them.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import sys
from pathlib import Path

from bweird.checkpoint import JsonlCheckpoint
from bweird.config import ModelSpec, load_generator_models
from bweird.errors import OpenRouterError, ParseError
from bweird.logging_utils import run_stage
from bweird.openrouter import OpenRouterClient
from bweird.parsing import parse_perspectives
from bweird.prompts import build_generation_messages, build_repair_messages
from bweird.schemas import GenerationRecord, Topic, load_topics

logger = logging.getLogger("generate_perspectives")

def make_cell_key(model_slug: str, topic_id: str) -> str:
    """Build the unique checkpoint key for one (model, topic) cell."""
    return f"{model_slug}::{topic_id}"

def generate_cell(
    client: OpenRouterClient,
    model: ModelSpec,
    topic: Topic,
    max_tokens: int,
) -> GenerationRecord:
    """Generate and validate the perspectives for one (model, topic) cell."""
    messages = build_generation_messages(topic)
    response = client.chat(model.slug, messages, temperature=0.0, max_tokens=max_tokens)
    try:
        perspectives = parse_perspectives(response.content)
    except ParseError as exc:
        logger.warning(
            "Parse failure for %s on %s (%s); attempting repair", model.slug, topic.topic_id, exc
        )
        repair_messages = build_repair_messages(messages, response.content)
        response = client.chat(model.slug, repair_messages, temperature=0.0, max_tokens=max_tokens)
        perspectives = parse_perspectives(response.content)

    return GenerationRecord(
        key=make_cell_key(model.slug, topic.topic_id),
        model_slug=model.slug,
        model_family=model.family,
        topic_id=topic.topic_id,
        perspectives=perspectives,
        raw_response=response.content,
        usage=response.usage,
        created_at=dt.datetime.now(dt.UTC).isoformat(),
    )

def run(args: argparse.Namespace) -> int:
    """Execute the generation stage; exit 1 if any cell failed permanently."""
    with args.topics.open("r", encoding="utf-8") as handle:
        topics = load_topics(json.load(handle))
    models = load_generator_models(args.models)

    checkpoint = JsonlCheckpoint(args.output)
    completed = checkpoint.completed_keys()

    pending = [
        (model, topic)
        for model in models
        for topic in topics
        if make_cell_key(model.slug, topic.topic_id) not in completed
    ]
    total = len(models) * len(topics)
    logger.info(
        "%d/%d cells already checkpointed; %d pending", total - len(pending), total, len(pending)
    )
    if args.dry_run:
        for model, topic in pending:
            logger.info("DRY RUN would generate: %s", make_cell_key(model.slug, topic.topic_id))
        return 0
    if not pending:
        logger.info("Nothing to do")
        return 0

    client = OpenRouterClient()
    failures_log = JsonlCheckpoint(args.failures)
    failure_count = 0
    for position, (model, topic) in enumerate(pending, start=1):
        key = make_cell_key(model.slug, topic.topic_id)
        logger.info("[%d/%d] generating %s", position, len(pending), key)
        try:
            record = generate_cell(client, model, topic, args.max_tokens)
        except (OpenRouterError, ParseError) as exc:
            failure_count += 1
            logger.error("Cell %s failed permanently: %s", key, exc)
            failures_log.append(
                {
                    "key": key,
                    "stage": "generate",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "created_at": dt.datetime.now(dt.UTC).isoformat(),
                }
            )
            continue
        checkpoint.append(record.to_json_dict())
        logger.info("Cell %s: %d perspectives", key, len(record.perspectives))

    logger.info(
        "Generation finished: %d succeeded, %d failed (failures logged to %s)",
        len(pending) - failure_count,
        failure_count,
        args.failures,
    )
    return 1 if failure_count else 0

def build_arg_parser() -> argparse.ArgumentParser:
    """Build the command-line interface."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--topics",
        type=Path,
        default=Path("data/topics.json"),
        help="Topic instrument JSON file",
    )
    parser.add_argument(
        "--models",
        type=Path,
        default=Path("config/models.json"),
        help="Generator model registry",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/outputs/generations.jsonl"),
        help="JSONL checkpoint for generation records",
    )
    parser.add_argument(
        "--failures",
        type=Path,
        default=Path("data/outputs/generation_failures.jsonl"),
        help="JSONL log of permanently failed cells",
    )
    parser.add_argument(
        "--max-tokens", type=int, default=4096, help="Completion token budget per call"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="List pending cells without calling the API"
    )
    return parser

def main(argv: list[str] | None = None) -> int:
    """Script entry point."""
    return run_stage(build_arg_parser(), run, argv)

if __name__ == "__main__":
    sys.exit(main())
