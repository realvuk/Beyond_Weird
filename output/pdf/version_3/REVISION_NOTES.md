# Version 3: corrections to version 2

This is a complete, integrated manuscript revision, dated 24 September 2026. The PDF contains 20 pages.

## Changes made

1. **Consistent model categories.** Tables 3 and 4 both use Frontier/API (5), larger open-weight (6), and smaller open-weight (2). Qwen 3.7 Max is in Frontier/API in both tables. All 13 models occur exactly once in each table. The stored original model configurations remain unchanged as research records; the revised grouping is recorded separately in `supplementary/model_recall.csv`.
2. **Readable appendix tables.** Table 10 uses a wrapping summary column, so it no longer overlaps Table 11. Table 12 spans both columns, keeping the configured endpoint identifiers intact and inside the page margins. The final table shares page 20 with the accompanying explanation.
3. **References and formatting.** Appendix G now links to Tables 2 and 10. The Qwen announcement has a functioning footnote with its source link. The bibliography has one References heading. All table and equation references resolve.
4. **Abstract uncertainty.** Restored the mean difference of -0.013 as -1.3 percentage points, with the 95% bootstrap interval of -8.1 to 5.8 percentage points. The one-sided p-value remains 0.680, and the abstract retains the distinction between no detectable advantage and equivalence.
5. **Proofreading.** Corrected the reported spelling and grammatical errors, including “famaily,” “my be,” “people involve,” the misplaced comma after “and,” and doubled parentheses around the Mehrotra citation. Retained the academic tone and existing qualifications.
6. **Undocumented extremity test.** Removed the p = 0.148 statement and its unverified permutation-count claim. No documented statistic and permutation scheme were found in the supplied project. Appendix D.9 is now titled “Descriptive extremity analysis”; all reported tier counts, recovery means, and correlations remain. The discussion refers to these results as descriptive.

## Source and preservation

The exact editable file that produced the uploaded `version_2.pdf` was not present. This revision was rebuilt from the closely matching local source, `output/pdf/readability_revision/revised_paper.tex`, with version 2's Methodology/Evaluation subsection hierarchy restored. The numbered topic table and fuller reference-example caption from the local source are retained. Figure assets come from `output/pdf/paper_figures/` and match the updated figures in version 2.

The six numerical results tables, all 16 numbered equations, both archived prompts, and the 21-entry bibliography are unchanged from that editable source. Supplementary data files are copied without modification. The main RQ1–RQ3 estimates and conclusions are preserved. No generation or judging experiments were rerun. The only intentionally removed inferential result is the undocumented extremity p-value.

## Validation

- Compiled successfully with pdfLaTeX through latexmk.
- No overfull boxes, undefined citations/references, duplicate labels, or unresolved `??` markers.
- Inspected the rendered pages, including the corrected tables, abstract, footnote, and bibliography.
- Verified both model tables have category sizes 5/6/2 and 13 distinct models.
- Checked the saved 13-by-8 differences: mean gap -0.013076923; exact one-sided signed-rank p = 0.6796875.
- Checked the saved worked-example judgments: judge recalls 0.60, 0.60, 0.60, 0.60, and 0.40; combined recall 0.56.
- Confirmed preservation of all supplementary data files and the retained numerical tables.

The source retains pre-existing author-check comments about reference provenance, benchmark-construction documentation, and the final repository URL. Those research-documentation matters were outside these six corrections.

## Editing and compilation

Upload `version_3_overleaf.zip` to Overleaf and select `version_3.tex` as the main document, using pdfLaTeX. The bibliography is embedded, so no `.bib` file is needed. The package includes the journal style, both figure assets, and supplementary records.

For local compilation, run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error version_3.tex
```
