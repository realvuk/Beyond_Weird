"""Typed data structures shared across all pipeline stages.

Instrument objects (:class:`Topic`, :class:`GoldPerspective`) are loaded from
the study's input files. Record objects (:class:`GenerationRecord`,
:class:`JudgmentRecord`) round-trip losslessly through ``to_json_dict`` /
``from_json_dict`` so every stage can resume from its JSONL checkpoints.
"""

from __future__ import annotations

import enum
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from typing import Any

from bweird.errors import DataError

#: Number of gold perspectives per topic (fixed by the study design).
N_GOLD_PERSPECTIVES: int = 5

#: Maximum number of perspectives a generator may output per topic.
MAX_GENERATED_PERSPECTIVES: int = 5

#: Size of the judging panel (invariant, even after substitution).
PANEL_SIZE: int = 5

#: ``match`` value a judge uses to signal "no gold perspective matches".
NO_MATCH: int = 0


class Arm(enum.StrEnum):
    """Which arm of a matched topic pair a topic belongs to."""

    WEIRD = "weird"
    SERBIAN = "serbian"


class JudgeRole(enum.StrEnum):
    """Why a judgment was collected.

    ``PANEL`` judgments feed the headline metrics; ``FAMILY_PROBE`` judgments
    come from the dropped same-family judge and are used only by the bias
    isolation analysis in ``5_evaluate_reliability.py``.
    """

    PANEL = "panel"
    FAMILY_PROBE = "family_probe"


class GenerationStatus(enum.StrEnum):
    """Post-aggregation classification of a generated perspective."""

    MATCHED = "matched"
    REDUNDANT = "redundant"
    NO_MATCH = "no_match"
    NO_VALID_VOTES = "no_valid_votes"


def _require(condition: bool, message: str) -> None:
    """Raise :class:`DataError` with ``message`` unless ``condition`` holds."""
    if not condition:
        raise DataError(message)


@dataclass(frozen=True)
class Topic:
    """A single evaluation topic within a matched WEIRD/Serbian pair."""

    topic_id: str
    topic_title: str
    population: str
    pair_id: str
    arm: Arm

    @classmethod
    def from_json_dict(cls, raw: Mapping[str, Any]) -> Topic:
        """Build a :class:`Topic` from a parsed JSON mapping."""
        try:
            arm = Arm(str(raw["arm"]).lower())
            topic = cls(
                topic_id=str(raw["topic_id"]),
                topic_title=str(raw["topic_title"]),
                population=str(raw["population"]),
                pair_id=str(raw["pair_id"]),
                arm=arm,
            )
        except (KeyError, ValueError) as exc:
            raise DataError(f"Invalid topic entry {raw!r}: {exc}") from exc
        _require(bool(topic.topic_id), "topic_id must be non-empty")
        _require(bool(topic.topic_title), "topic_title must be non-empty")
        _require(bool(topic.population), "population must be non-empty")
        return topic


@dataclass(frozen=True)
class GoldPerspective:
    """One externally grounded gold-standard perspective (``gold_id`` in 1..5)."""

    gold_id: int
    summary: str
    explanation: str

    @classmethod
    def from_json_dict(cls, raw: Mapping[str, Any]) -> GoldPerspective:
        """Build a :class:`GoldPerspective` from a parsed JSON mapping."""
        try:
            gold = cls(
                gold_id=int(raw["gold_id"]),
                summary=str(raw["summary"]),
                explanation=str(raw["explanation"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise DataError(f"Invalid gold perspective {raw!r}: {exc}") from exc
        _require(gold.gold_id >= 1, "gold_id must be >= 1")
        _require(bool(gold.summary), "gold summary must be non-empty")
        return gold


@dataclass(frozen=True)
class GeneratedPerspective:
    """One perspective produced by a generator model (``index`` is 1-based)."""

    index: int
    summary: str
    explanation: str


@dataclass(frozen=True)
class GenerationRecord:
    """Checkpointed stage-1 output for one (generator model, topic) cell.

    ``key`` is ``"<model_slug>::<topic_id>"``; ``raw_response`` keeps the
    verbatim model output for auditability.
    """

    key: str
    model_slug: str
    model_family: str
    topic_id: str
    perspectives: tuple[GeneratedPerspective, ...]
    raw_response: str
    usage: Mapping[str, int] = field(default_factory=dict)
    created_at: str = ""

    def to_json_dict(self) -> dict[str, Any]:
        """Serialise to a JSON-compatible dict for JSONL checkpointing."""
        return asdict(self)

    @classmethod
    def from_json_dict(cls, raw: Mapping[str, Any]) -> GenerationRecord:
        """Deserialise a record previously written by :meth:`to_json_dict`."""
        try:
            perspectives = tuple(
                GeneratedPerspective(
                    index=int(p["index"]),
                    summary=str(p["summary"]),
                    explanation=str(p["explanation"]),
                )
                for p in raw["perspectives"]
            )
            return cls(
                key=str(raw["key"]),
                model_slug=str(raw["model_slug"]),
                model_family=str(raw["model_family"]),
                topic_id=str(raw["topic_id"]),
                perspectives=perspectives,
                raw_response=str(raw.get("raw_response", "")),
                usage={str(k): int(v) for k, v in raw.get("usage", {}).items()},
                created_at=str(raw.get("created_at", "")),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise DataError(f"Invalid generation record: {exc}") from exc


@dataclass(frozen=True)
class JudgmentRecord:
    """Checkpointed stage-2 output for one judge execution.

    ``presentation_order[i]`` is the canonical ``gold_id`` of the option the
    judge saw labelled ``i + 1``. ``match_presented`` is the raw vote in that
    presented-label space; ``match_gold_id`` is the same vote mapped back to
    canonical gold IDs (``0`` = no match, ``None`` = abstention after all
    retries). The reasoning-chain fields (``attributes``, ``scope_ok``,
    ``comparisons``, ``reason``) and ``raw_response`` are kept for audit.
    """

    key: str
    generator_slug: str
    generator_family: str
    topic_id: str
    gen_index: int
    judge_slug: str
    judge_family: str
    role: JudgeRole
    presentation_order: tuple[int, ...]
    match_presented: int | None
    match_gold_id: int | None
    attributes: tuple[str, ...] = ()
    scope_ok: bool | None = None
    comparisons: tuple[Mapping[str, Any], ...] = ()
    reason: str = ""
    raw_response: str = ""
    created_at: str = ""

    @property
    def is_abstention(self) -> bool:
        """Whether this judge execution produced no usable vote."""
        return self.match_gold_id is None

    def to_json_dict(self) -> dict[str, Any]:
        """Serialise to a JSON-compatible dict for JSONL checkpointing."""
        return asdict(self)

    @classmethod
    def from_json_dict(cls, raw: Mapping[str, Any]) -> JudgmentRecord:
        """Deserialise a record previously written by :meth:`to_json_dict`."""
        try:
            match_presented = raw.get("match_presented")
            match_gold_id = raw.get("match_gold_id")
            return cls(
                key=str(raw["key"]),
                generator_slug=str(raw["generator_slug"]),
                generator_family=str(raw["generator_family"]),
                topic_id=str(raw["topic_id"]),
                gen_index=int(raw["gen_index"]),
                judge_slug=str(raw["judge_slug"]),
                judge_family=str(raw["judge_family"]),
                role=JudgeRole(str(raw["role"])),
                presentation_order=tuple(int(g) for g in raw["presentation_order"]),
                match_presented=None if match_presented is None else int(match_presented),
                match_gold_id=None if match_gold_id is None else int(match_gold_id),
                attributes=tuple(str(a) for a in raw.get("attributes", [])),
                scope_ok=raw.get("scope_ok"),
                comparisons=tuple(dict(c) for c in raw.get("comparisons", [])),
                reason=str(raw.get("reason", "")),
                raw_response=str(raw.get("raw_response", "")),
                created_at=str(raw.get("created_at", "")),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise DataError(f"Invalid judgment record: {exc}") from exc


def load_topics(raw: Any) -> list[Topic]:
    """Validate and load the full topic instrument from parsed JSON.

    Enforces the study design: unique topic IDs, and every ``pair_id``
    appearing exactly twice, once per arm.
    """
    _require(isinstance(raw, list) and len(raw) > 0, "topics.json must be a non-empty list")
    topics = [Topic.from_json_dict(entry) for entry in raw]

    seen_ids = [t.topic_id for t in topics]
    _require(len(seen_ids) == len(set(seen_ids)), "Duplicate topic_id in topics.json")

    arms_by_pair: dict[str, set[Arm]] = {}
    for topic in topics:
        arms = arms_by_pair.setdefault(topic.pair_id, set())
        _require(
            topic.arm not in arms,
            f"Pair {topic.pair_id!r} has two topics on the {topic.arm.value!r} arm",
        )
        arms.add(topic.arm)
    for pair_id, arms in arms_by_pair.items():
        _require(
            arms == {Arm.WEIRD, Arm.SERBIAN},
            f"Pair {pair_id!r} must have exactly one WEIRD and one Serbian topic",
        )
    return topics


def load_gold_standard(raw: Any) -> dict[str, tuple[GoldPerspective, ...]]:
    """Validate and load the gold standard from parsed JSON.

    Expects the instrument format ``{"version": ..., "topics": [...]}`` where
    each topic carries five ``perspectives`` whose ``perspective_id`` ends in
    ``_p<N>``. Returns a mapping from ``topic_id`` to exactly five gold
    perspectives with canonical IDs ``1..5``.
    """
    _require(
        isinstance(raw, Mapping) and isinstance(raw.get("topics"), list) and bool(raw["topics"]),
        'gold_standard.json must be an object with a non-empty "topics" list',
    )
    gold: dict[str, tuple[GoldPerspective, ...]] = {}
    for entry in raw["topics"]:
        try:
            topic_id = str(entry["topic_id"])
            perspectives = tuple(
                GoldPerspective.from_json_dict(
                    {
                        "gold_id": str(p["perspective_id"]).rsplit("_p", 1)[1],
                        "summary": p["summary"],
                        "explanation": p["explanation"],
                    }
                )
                for p in entry["perspectives"]
            )
        except (KeyError, IndexError, TypeError) as exc:
            raise DataError(f"Invalid gold standard entry: {exc}") from exc
        _require(topic_id not in gold, f"Duplicate topic_id {topic_id!r} in gold standard")
        _require(
            len(perspectives) == N_GOLD_PERSPECTIVES,
            f"Topic {topic_id!r} must have exactly {N_GOLD_PERSPECTIVES} gold "
            f"perspectives, found {len(perspectives)}",
        )
        _require(
            sorted(p.gold_id for p in perspectives) == list(range(1, N_GOLD_PERSPECTIVES + 1)),
            f"Topic {topic_id!r} gold IDs must be exactly 1..{N_GOLD_PERSPECTIVES}",
        )
        gold[topic_id] = perspectives
    return gold
