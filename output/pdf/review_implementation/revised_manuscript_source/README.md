# Revised manuscript and review evidence

This is a separate review draft. The original PDF, LaTeX and workbook were not changed.
Read `change_guide.pdf` or `change_guide.md` for every edit, original PDF margin
line numbers, exact replacements, and unresolved author actions.

## Compile

From the extracted package folder, with a working TeX Live installation:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error revised_manuscript.tex
```

## Reproduce the added analyses

Python dependencies: numpy, pandas, statsmodels (statistics); openpyxl (provenance).
The scripts read only packaged inputs and write their outputs into `analysis/`.
They make no model/API calls and contain runnable assertions.

```sh
python3 analysis/reproduce_sensitivity.py
python3 analysis/extract_sources.py
```

The statistics script reproduces the added matched-pair checks, not every
analysis in the paper. Supplementary tables include saved historical results.
The supplied scripts do not collect generations/judgments or authenticate data.
`model_recall_interval_sensitivity.csv` in analysis is the same table supplied as
`supplementary/model_pair_bootstrap_ci.csv` for the manuscript.

## Unresolved before submission

Resolve the seven exact source records in `supplementary/SOURCE_AUDIT.md`;
add a real persistent repository/archive identifier; choose the journal and
complete its author/anonymity/declaration requirements. No public deposit was
made. Template author metadata is inherited from the original anonymous draft.
Archived tier metadata and the exact original prompt are preserved, while the
unused extremity analysis and its discussion pointer were removed.

The package supplies evaluated references, provenance, configurations, saved
scores and the added-analysis scripts. It does not include the raw API logs or
the full original execution environment. Broader reproducibility claims require
adding those existing records to the final research archive.
