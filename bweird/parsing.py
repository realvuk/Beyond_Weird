"""Robust extraction and validation of structured JSON from model output.

LLMs frequently wrap JSON in Markdown fences or prepend commentary despite
strict instructions. :func:`extract_json_value` recovers the first valid
JSON value from raw text; the ``parse_*`` validators then enforce the
pipeline's schemas and raise :class:`~bweird.errors.ParseError` with a
diagnostic message when the payload is unusable.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from bweird.errors import ParseError
from bweird.schemas import MAX_GENERATED_PERSPECTIVES, NO_MATCH, GeneratedPerspective

_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def extract_json_value(text: str) -> Any:
    """Extract the first JSON value (object or array) from raw model text.

    Tries, in order: the whole text; the contents of each Markdown code
    fence; the first balanced JSON value found by scanning for ``{`` / ``[``
    and using :meth:`json.JSONDecoder.raw_decode`.
    """
    stripped = text.strip()
    if not stripped:
        raise ParseError("Model output is empty")

    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    for fenced in _FENCE_RE.findall(stripped):
        try:
            return json.loads(fenced.strip())
        except json.JSONDecodeError:
            continue

    decoder = json.JSONDecoder()
    for start in re.finditer(r"[{\[]", stripped):
        try:
            value, _ = decoder.raw_decode(stripped, start.start())
        except json.JSONDecodeError:
            continue
        return value

    raise ParseError(f"No valid JSON found in model output (first 200 chars: {stripped[:200]!r})")


def parse_perspectives(text: str) -> tuple[GeneratedPerspective, ...]:
    """Parse and validate a generator's perspective list.

    Accepts a JSON array of 1..:data:`~bweird.schemas.MAX_GENERATED_PERSPECTIVES`
    objects with non-empty ``summary`` and ``explanation`` strings, optionally
    wrapped as ``{"perspectives": [...]}``. Returned perspectives carry
    1-based ``index`` values.
    """
    value = extract_json_value(text)
    if isinstance(value, dict) and isinstance(value.get("perspectives"), list):
        value = value["perspectives"]
    if not isinstance(value, list):
        raise ParseError(f"Expected a JSON array of perspectives, got {type(value).__name__}")
    if not value:
        raise ParseError("Perspective list is empty")
    if len(value) > MAX_GENERATED_PERSPECTIVES:
        raise ParseError(
            f"Got {len(value)} perspectives, maximum is {MAX_GENERATED_PERSPECTIVES}"
        )

    perspectives: list[GeneratedPerspective] = []
    for position, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise ParseError(f"Perspective {position} is not a JSON object")
        summary = item.get("summary")
        explanation = item.get("explanation")
        if not isinstance(summary, str) or not summary.strip():
            raise ParseError(f"Perspective {position} has a missing or empty 'summary'")
        if not isinstance(explanation, str) or not explanation.strip():
            raise ParseError(f"Perspective {position} has a missing or empty 'explanation'")
        perspectives.append(
            GeneratedPerspective(
                index=position, summary=summary.strip(), explanation=explanation.strip()
            )
        )
    return tuple(perspectives)


@dataclass(frozen=True)
class ParsedJudgment:
    """A judge's validated reasoning chain, in presented-label space.

    ``match`` is a presented label in ``1..n_gold``, or
    :data:`~bweird.schemas.NO_MATCH` for no match.
    """

    attributes: tuple[str, ...]
    scope_ok: bool
    comparisons: tuple[dict[str, Any], ...]
    match: int
    reason: str


def parse_judgment(text: str, n_gold: int) -> ParsedJudgment:
    """Parse and validate a judge's reasoning-chain JSON.

    ``n_gold`` is the number of gold options presented (upper bound for the
    ``match`` vote).
    """
    value = extract_json_value(text)
    if not isinstance(value, dict):
        raise ParseError(f"Expected a JSON object judgment, got {type(value).__name__}")

    match_raw = value.get("match")
    if isinstance(match_raw, bool) or not isinstance(match_raw, (int, str)):
        raise ParseError(f"Judgment 'match' must be an integer, got {match_raw!r}")
    try:
        match = int(match_raw)
    except ValueError as exc:
        raise ParseError(f"Judgment 'match' is not an integer: {match_raw!r}") from exc
    if not NO_MATCH <= match <= n_gold:
        raise ParseError(f"Judgment 'match' must be in 0..{n_gold}, got {match}")

    attributes_raw = value.get("attributes", [])
    if isinstance(attributes_raw, str):
        attributes_raw = [attributes_raw]
    elif not isinstance(attributes_raw, list):
        raise ParseError("Judgment 'attributes' must be a JSON array or a string")
    attributes = tuple(str(a) for a in attributes_raw)


    scope_ok = value.get("scope_ok")
    if not isinstance(scope_ok, bool):
        raise ParseError(f"Judgment 'scope_ok' must be a boolean, got {scope_ok!r}")

    comparisons_raw = value.get("comparisons", [])
    if not isinstance(comparisons_raw, list):
        raise ParseError("Judgment 'comparisons' must be a JSON array")
    comparisons = tuple(
        item if isinstance(item, dict) else {"note": str(item)} for item in comparisons_raw
    )

    reason = value.get("reason", "")
    if not isinstance(reason, str) or not reason.strip():
        raise ParseError("Judgment 'reason' must be a non-empty string")

    return ParsedJudgment(
        attributes=attributes,
        scope_ok=scope_ok,
        comparisons=comparisons,
        match=match,
        reason=reason.strip(),
    )
