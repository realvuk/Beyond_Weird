#!/usr/bin/env python3
"""Stage 2: family-disjoint five-judge matching against the gold standard.

For every generated perspective, each of five judges independently decides
which single gold perspective (if any) expresses the same viewpoint.
"""


from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import logging
import random
import sys
from pathlib import Path

from bweird.checkpoint import JsonlCheckpoint
from bweird.config import JudgeConfig, ModelSpec, load_judge_config
from bweird.errors import CircuitBreakerError, DataError, OpenRouterError, ParseError
from bweird.logging_utils import run_stage
from bweird.openrouter import OpenRouterClient
from bweird.parsing import parse_judgment
from bweird.prompts import build_judge_messages, build_repair_messages
from bweird.schemas import (
    NO_MATCH,
    GeneratedPerspective,
    GenerationRecord,
    GoldPerspective,
    JudgeRole,
    JudgmentRecord,
    Topic,
    load_gold_standard,
    load_topics,
)

logger = logging.getLogger("judge_panel")


def make_judgment_key(
    generator_slug: str, topic_id: str, gen_index: int, judge_slug: str, role: JudgeRole
) -> str:
    """Build the unique checkpoint key for one judge execution."""
    return f"{generator_slug}::{topic_id}::p{gen_index}::{judge_slug}::{role.value}"


def presentation_rng(seed: int, key: str) -> random.Random:
    """Derive an independent, reproducible RNG for one judge execution.

    Hashing the run seed together with the execution key gives every judge
    execution its own statistically independent shuffle while keeping the
    whole run reproducible and resumable.
    """
    digest = hashlib.sha256(f"{seed}|{key}".encode()).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def execute_judgment(
    client: OpenRouterClient,
    topic: Topic,
    generation: GenerationRecord,
    candidate: GeneratedPerspective,
    gold: tuple[GoldPerspective, ...],
    judge: ModelSpec,
    role: JudgeRole,
    key: str,
    seed: int,
    max_tokens: int,
) -> JudgmentRecord:
    """Run one judge execution, returning a record even on failure.

    The gold perspectives are shuffled with an execution-specific RNG; the
    judge's ``match`` vote (presented-label space) is mapped back to the
    canonical gold ID before recording. Permanent failures produce an
    abstention record rather than raising, so the panel seat is preserved
    with a shrunken denominator downstream.
    """
    rng = presentation_rng(seed, key)
    presented = list(gold)
    rng.shuffle(presented)
    presentation_order = tuple(g.gold_id for g in presented)
    created_at = dt.datetime.now(dt.UTC).isoformat()

    messages = build_judge_messages(topic, candidate, presented)
    try:
        response = client.chat(judge.slug, messages, temperature=0.0, max_tokens=max_tokens)
        try:
            judgment = parse_judgment(response.content, n_gold=len(presented))
        except ParseError as exc:
            logger.warning(
                "Judge %s unparseable on %s (%s); attempting repair", judge.slug, key, exc
            )
            repair = build_repair_messages(messages, response.content)
            response = client.chat(judge.slug, repair, temperature=0.0, max_tokens=max_tokens)
            judgment = parse_judgment(response.content, n_gold=len(presented))
    except (OpenRouterError, ParseError) as exc:
        logger.error("Judge %s abstains on %s: %s", judge.slug, key, exc)
        return JudgmentRecord(
            key=key,
            generator_slug=generation.model_slug,
            generator_family=generation.model_family,
            topic_id=topic.topic_id,
            gen_index=candidate.index,
            judge_slug=judge.slug,
            judge_family=judge.family,
            role=role,
            presentation_order=presentation_order,
            match_presented=None,
            match_gold_id=None,
            reason=f"ABSTENTION: {type(exc).__name__}: {exc}",
            created_at=created_at,
        )

    if judgment.match == NO_MATCH:
        match_gold_id = NO_MATCH
    else:
        match_gold_id = presentation_order[judgment.match - 1]

    return JudgmentRecord(
        key=key,
        generator_slug=generation.model_slug,
        generator_family=generation.model_family,
        topic_id=topic.topic_id,
        gen_index=candidate.index,
        judge_slug=judge.slug,
        judge_family=judge.family,
        role=role,
        presentation_order=presentation_order,
        match_presented=judgment.match,
        match_gold_id=match_gold_id,
        attributes=judgment.attributes,
        scope_ok=judgment.scope_ok,
        comparisons=judgment.comparisons,
        reason=judgment.reason,
        raw_response=response.content,
        created_at=created_at,
    )


def plan_executions(
    generations: list[GenerationRecord],
    judge_config: JudgeConfig,
    include_family_probe: bool,
) -> list[tuple[GenerationRecord, GeneratedPerspective, ModelSpec, JudgeRole, str]]:
    """Enumerate every judge execution required by the study design.

    Returns one tuple per execution: (generation record, candidate
    perspective, judge, role, checkpoint key).
    """
    plan: list[tuple[GenerationRecord, GeneratedPerspective, ModelSpec, JudgeRole, str]] = []
    for generation in generations:
        panel = judge_config.build_panel(generation.model_family)
        probe = (
            judge_config.dropped_judge(generation.model_family) if include_family_probe else None
        )
        for candidate in generation.perspectives:
            seats: list[tuple[ModelSpec, JudgeRole]] = [
                (member.judge, JudgeRole.PANEL) for member in panel
            ]
            if probe is not None:
                seats.append((probe, JudgeRole.FAMILY_PROBE))
            for judge, role in seats:
                key = make_judgment_key(
                    generation.model_slug, generation.topic_id, candidate.index, judge.slug, role
                )
                plan.append((generation, candidate, judge, role, key))
    return plan


def collect_completed_keys(checkpoint: JsonlCheckpoint, retry_abstentions: bool) -> set[str]:
    """Collect checkpoint keys that do not need to be re-run.

    With ``retry_abstentions``, keys whose *latest* record is an abstention
    are treated as pending so failed judges get another chance; downstream
    stages deduplicate by key keeping the last record, so the retried vote
    supersedes the abstention.
    """
    latest_is_abstention: dict[str, bool] = {}
    for raw in checkpoint.iter_records():
        key = raw.get("key")
        if isinstance(key, str):
            latest_is_abstention[key] = raw.get("match_gold_id") is None
    if not retry_abstentions:
        return set(latest_is_abstention)
    return {key for key, abstained in latest_is_abstention.items() if not abstained}


def run(args: argparse.Namespace) -> int:
    """Execute the judging stage; abstentions are recorded as data, not failures."""
    with args.topics.open("r", encoding="utf-8") as handle:
        topics = {t.topic_id: t for t in load_topics(json.load(handle))}
    with args.gold.open("r", encoding="utf-8") as handle:
        gold_standard = load_gold_standard(json.load(handle))
    judge_config = load_judge_config(args.judges)

    generations = [
        GenerationRecord.from_json_dict(raw)
        for raw in JsonlCheckpoint(args.generations).iter_records()
    ]
    if not generations:
        raise DataError(f"No generation records found in {args.generations}")
    for generation in generations:
        if generation.topic_id not in topics:
            raise DataError(f"Generation {generation.key!r} references unknown topic")
        if generation.topic_id not in gold_standard:
            raise DataError(f"No gold standard for topic {generation.topic_id!r}")

    checkpoint = JsonlCheckpoint(args.output)
    completed = collect_completed_keys(checkpoint, args.retry_abstentions)
    plan = plan_executions(generations, judge_config, args.include_family_probe)
    pending = [item for item in plan if item[4] not in completed]
    logger.info(
        "%d/%d judge executions already checkpointed; %d pending",
        len(plan) - len(pending),
        len(plan),
        len(pending),
    )
    if args.dry_run:
        for *_, key in pending:
            logger.info("DRY RUN would judge: %s", key)
        return 0
    if not pending:
        logger.info("Nothing to do")
        return 0

    client = OpenRouterClient()
    abstention_count = 0
    consecutive_abstentions = 0
    for position, (generation, candidate, judge, role, key) in enumerate(pending, start=1):
        logger.info("[%d/%d] judging %s", position, len(pending), key)
        record = execute_judgment(
            client=client,
            topic=topics[generation.topic_id],
            generation=generation,
            candidate=candidate,
            gold=gold_standard[generation.topic_id],
            judge=judge,
            role=role,
            key=key,
            seed=args.seed,
            max_tokens=args.max_tokens,
        )
        checkpoint.append(record.to_json_dict())
        if record.is_abstention:
            abstention_count += 1
            consecutive_abstentions += 1
            if (
                args.max_consecutive_abstentions > 0
                and consecutive_abstentions >= args.max_consecutive_abstentions
            ):
                raise CircuitBreakerError(
                    f"Aborting run: reached {consecutive_abstentions} consecutive abstentions."
                )
        else:
            consecutive_abstentions = 0

    logger.info(
        "Judging finished: %d executions, %d abstentions (re-run with "
        "--retry-abstentions to give failed judges another chance)",
        len(pending),
        abstention_count,
    )
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the command-line interface."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--generations",
        type=Path,
        default=Path("data/outputs/generations.jsonl"),
        help="Generation records from stage 1",
    )
    parser.add_argument(
        "--gold",
        type=Path,
        default=Path("data/gold_standard.json"),
        help="Gold standard JSON file",
    )
    parser.add_argument(
        "--topics",
        type=Path,
        default=Path("data/topics.json"),
        help="Topic instrument JSON file",
    )
    parser.add_argument(
        "--judges",
        type=Path,
        default=Path("config/judges.json"),
        help="Judge panel configuration",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/outputs/judgments.jsonl"),
        help="JSONL checkpoint for judgment records",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260708,
        help="Run-level seed for presentation randomisation",
    )
    parser.add_argument(
        "--max-tokens", type=int, default=4096, help="Completion token budget per call"
    )
    parser.add_argument(
        "--max-consecutive-abstentions",
        type=int,
        default=10,
        help="Abort the run if this number of consecutive abstentions is reached",
    )
    parser.add_argument(
        "--include-family-probe",
        action="store_true",
        help="Also query the dropped same-family judge (bias analysis only)",
    )
    parser.add_argument(
        "--retry-abstentions",
        action="store_true",
        help="Re-run executions whose latest record is an abstention",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="List pending executions without calling the API"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Script entry point."""
    return run_stage(build_arg_parser(), run, argv)


if __name__ == "__main__":
    sys.exit(main())
