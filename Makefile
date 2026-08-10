# Beyond WEIRD — reproduction entry points.
#
# `make verify` is the one to run first: it needs no API key and no network,
# and it re-derives the paper's numbers from the committed data.

PY ?= .venv/bin/python

.PHONY: help install verify analysis reanalysis figures lint clean

help:
	@grep -E '^[a-z-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[1m%-12s\033[0m %s\n", $$1, $$2}'

install:  ## Create .venv and install the package plus dev tooling
	uv venv .venv 2>/dev/null || $(PY) -m venv .venv
	uv pip install -e ".[dev,figures]" 2>/dev/null || .venv/bin/python -m pip install -e ".[dev,figures]"

verify:  ## Re-derive and check every published number (no API key needed)
	$(PY) verify/test_smoke.py
	$(PY) verify/check_manuscript_numbers.py
	$(PY) verify/reverify.py

analysis:  ## Rebuild results/agg/ from the committed judgments
	$(PY) pipeline/adapter.py
	$(PY) pipeline/3_aggregate.py
	$(PY) pipeline/4_eval_prf.py
	$(PY) pipeline/5_eval_reliability.py
	$(PY) pipeline/6_eval_stats.py

reanalysis:  ## Rebuild results/reanalysis/ via the independent pack
	$(PY) reanalysis/audit_counts.py
	$(PY) reanalysis/eval_coverage.py
	$(PY) reanalysis/topic_difficulty.py
	$(PY) reanalysis/weird_gap.py
	$(PY) reanalysis/lojo_audit.py
	$(PY) reanalysis/human_assignment_audit.py

figures:  ## Regenerate the manuscript figures into figures/
	$(PY) figures/plot_1.py
	$(PY) figures/plot_2.py

lint:  ## Static checks
	$(PY) -m ruff check .
	$(PY) -m mypy

clean:  ## Remove caches and build artefacts (never touches results/ or data/)
	rm -rf .mypy_cache .ruff_cache **/__pycache__ *.egg-info
