"""Model registry and family-disjoint judge-panel construction.

The judge panel is the methodological core of the pipeline: generations must
never be scored by a judge from the generator's own model family. This module
loads the fixed base panel plus a substitution dictionary and builds, for any
generator family, a concrete 5-judge panel with same-family judges swapped
out for their pre-designated neutral substitutes.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bweird.errors import ConfigError
from bweird.schemas import PANEL_SIZE

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ModelSpec:
    """A concrete model reachable through OpenRouter.

    ``family`` is the label the disjointness constraint operates on; it must
    be assigned consistently between the generator registry and the judge
    configuration.
    """

    slug: str
    family: str
    display_name: str

    @classmethod
    def from_json_dict(cls, raw: Mapping[str, Any]) -> ModelSpec:
        """Build a :class:`ModelSpec` from a parsed JSON mapping."""
        try:
            spec = cls(
                slug=str(raw["slug"]),
                family=str(raw["family"]).lower(),
                display_name=str(raw.get("display_name", raw["slug"])),
            )
        except KeyError as exc:
            raise ConfigError(f"Model entry {raw!r} missing key {exc}") from exc
        if not spec.slug or "/" not in spec.slug:
            raise ConfigError(f"Model slug {spec.slug!r} does not look like an OpenRouter slug")
        if not spec.family:
            raise ConfigError(f"Model {spec.slug!r} has an empty family label")
        return spec


@dataclass(frozen=True)
class PanelMember:
    """One seat of a concrete panel; ``substituted_for`` names the base judge it replaced."""

    judge: ModelSpec
    substituted_for: str | None = None


@dataclass(frozen=True)
class JudgeConfig:
    """The fixed base panel plus the family substitution dictionary.

    The base panel has exactly :data:`~bweird.schemas.PANEL_SIZE` judges with
    pairwise-distinct families (one seat per family, so a single designated
    substitute per family always suffices).
    """

    base_panel: tuple[ModelSpec, ...]
    substitutes: Mapping[str, ModelSpec]

    def build_panel(self, generator_family: str) -> tuple[PanelMember, ...]:
        """Build the concrete panel for a generator of the given family.

        Any base-panel judge whose family matches is dropped and replaced by
        the pre-designated substitute, keeping the panel size at exactly
        :data:`~bweird.schemas.PANEL_SIZE`. Raises :class:`ConfigError` if a
        needed substitute is missing or the resulting panel violates the
        invariants.
        """
        family = generator_family.lower()
        panel: list[PanelMember] = []
        for judge in self.base_panel:
            if judge.family != family:
                panel.append(PanelMember(judge=judge))
                continue
            substitute = self.substitutes.get(family)
            if substitute is None:
                raise ConfigError(
                    f"No substitute configured for family {family!r}, but base "
                    f"judge {judge.slug!r} must be dropped for this generator"
                )
            logger.debug(
                "Family-disjoint substitution: dropping %s, seating %s (generator family=%s)",
                judge.slug,
                substitute.slug,
                family,
            )
            panel.append(PanelMember(judge=substitute, substituted_for=judge.slug))

        self._validate_concrete_panel(panel, family)
        return tuple(panel)

    def dropped_judge(self, generator_family: str) -> ModelSpec | None:
        """Return the base-panel judge dropped for this family (bias-probe target), if any."""
        family = generator_family.lower()
        for judge in self.base_panel:
            if judge.family == family:
                return judge
        return None

    def _validate_concrete_panel(self, panel: list[PanelMember], family: str) -> None:
        """Enforce the panel invariants after substitution."""
        if len(panel) != PANEL_SIZE:
            raise ConfigError(f"Panel size is {len(panel)}, expected {PANEL_SIZE}")
        slugs = [m.judge.slug for m in panel]
        if len(slugs) != len(set(slugs)):
            raise ConfigError(f"Panel for family {family!r} contains duplicate judges: {slugs}")
        offenders = [m.judge.slug for m in panel if m.judge.family == family]
        if offenders:
            raise ConfigError(
                f"Panel for family {family!r} violates family-disjointness: {offenders}"
            )


def _read_json(path: Path) -> Any:
    """Read and parse a JSON file, wrapping failures in :class:`ConfigError`."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ConfigError(f"Configuration file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Malformed JSON in {path}: {exc}") from exc


def load_generator_models(path: Path) -> list[ModelSpec]:
    """Load the registry of generator models (``models.json``), in file order."""
    raw = _read_json(path)
    if not isinstance(raw, list) or not raw:
        raise ConfigError(f"{path} must contain a non-empty JSON list of models")
    models = [ModelSpec.from_json_dict(entry) for entry in raw]
    slugs = [m.slug for m in models]
    if len(slugs) != len(set(slugs)):
        raise ConfigError(f"Duplicate model slugs in {path}")
    logger.info("Loaded %d generator models from %s", len(models), path)
    return models


def load_judge_config(path: Path) -> JudgeConfig:
    """Load and validate the judge panel configuration (``judges.json``).

    Raises :class:`ConfigError` unless the panel has exactly five judges with
    distinct families and every panel family has a substitute that neither
    shares that family nor already sits on the panel.
    """
    raw = _read_json(path)
    if not isinstance(raw, dict):
        raise ConfigError(f"{path} must contain a JSON object")
    try:
        panel_raw = raw["panel"]
        substitutes_raw = raw["substitutes"]
    except KeyError as exc:
        raise ConfigError(f"{path} missing top-level key {exc}") from exc

    panel = tuple(ModelSpec.from_json_dict(entry) for entry in panel_raw)
    if len(panel) != PANEL_SIZE:
        raise ConfigError(f"Base panel must have exactly {PANEL_SIZE} judges, found {len(panel)}")
    families = [j.family for j in panel]
    if len(families) != len(set(families)):
        raise ConfigError(
            "Base panel families must be pairwise distinct (one seat per family); "
            f"found {families}"
        )

    if not isinstance(substitutes_raw, dict):
        raise ConfigError(f"'substitutes' in {path} must be a JSON object")
    substitutes = {
        str(family).lower(): ModelSpec.from_json_dict(entry)
        for family, entry in substitutes_raw.items()
    }

    panel_slugs = {j.slug for j in panel}
    for family in families:
        substitute = substitutes.get(family)
        if substitute is None:
            raise ConfigError(f"No substitute configured for base-panel family {family!r}")
        if substitute.family == family:
            raise ConfigError(
                f"Substitute {substitute.slug!r} for family {family!r} belongs to "
                "that same family and would violate disjointness"
            )
        if substitute.slug in panel_slugs:
            raise ConfigError(
                f"Substitute {substitute.slug!r} for family {family!r} already "
                "sits on the base panel; substitution would duplicate a judge"
            )

    config = JudgeConfig(base_panel=panel, substitutes=substitutes)
    logger.info(
        "Loaded judge config from %s: panel=[%s]",
        path,
        ", ".join(j.slug for j in panel),
    )
    return config
