"""Tests for bweird.config: family-disjoint judge-panel construction."""
from __future__ import annotations

import pytest

from bweird.config import JudgeConfig, ModelSpec
from bweird.errors import ConfigError


def spec(slug: str, family: str) -> ModelSpec:
    return ModelSpec(slug=f"{family}/{slug}", family=family, display_name=slug)


@pytest.fixture
def config() -> JudgeConfig:
    return JudgeConfig(
        base_panel=tuple(spec(f"j{i}", f) for i, f in enumerate("abcde")),
        substitutes={"a": spec("sub", "z")},
    )


def test_build_panel_substitutes_own_family_judge(config):
    panel = config.build_panel("a")
    assert len(panel) == 5
    assert all(m.judge.family != "a" for m in panel)
    assert [m.substituted_for for m in panel] == ["a/j0", None, None, None, None]


def test_build_panel_no_substitution_for_unrelated_family(config):
    panel = config.build_panel("z")
    assert [m.judge.slug for m in panel] == [j.slug for j in config.base_panel]
    assert all(m.substituted_for is None for m in panel)


def test_build_panel_case_insensitive_family(config):
    panel = config.build_panel("A")
    assert all(m.judge.family != "a" for m in panel)


def test_build_panel_raises_when_substitute_missing():
    cfg = JudgeConfig(base_panel=tuple(spec(f"j{i}", f) for i, f in enumerate("abcde")),
                       substitutes={})
    with pytest.raises(ConfigError):
        cfg.build_panel("a")


def test_dropped_judge(config):
    assert config.dropped_judge("a") == spec("j0", "a")
    assert config.dropped_judge("z") is None


def test_model_spec_from_json_dict_requires_slug_with_family_prefix():
    with pytest.raises(ConfigError):
        ModelSpec.from_json_dict({"slug": "no-slash", "family": "x"})


def test_model_spec_from_json_dict_requires_nonempty_family():
    with pytest.raises(ConfigError):
        ModelSpec.from_json_dict({"slug": "org/model", "family": ""})


def test_model_spec_from_json_dict_ok():
    spec_ = ModelSpec.from_json_dict({"slug": "org/model", "family": "Org"})
    assert spec_.slug == "org/model"
    assert spec_.family == "org"  # lowercased
    assert spec_.display_name == "org/model"  # defaults to slug
