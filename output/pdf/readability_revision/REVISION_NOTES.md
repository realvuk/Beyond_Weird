# Readability revision

The revised manuscript rewrites `0_last.tex` and preserves its scientific results. It separates benchmark construction from evaluation, introduces an actual reference set and a saved worked example, explains judge assignments before recall, and distinguishes model summaries from the eight-pair cultural comparison. The narrative sections are about 23% shorter. Detailed missing-judgment calculations and sensitivity analyses are in the appendices.

The model categories are consistent throughout: five Frontier/API, six larger open-weight, and two smaller open-weight systems. The two mixed-effects analyses are identified separately by their observational units. The supplementary precision/F1 table and machine-readable contrasts come from existing saved results. No generation or judging experiments were rerun.

## Files and compilation

- `revised_paper.tex`: complete editable manuscript, with the bibliography embedded.
- `revised_paper.pdf`: compiled manuscript.
- `tacl2021v1.sty`: original journal style, included for compilation.
- Figure assets: included beside the manuscript.
- `supplementary/`: reference records, topic definitions, model configurations, worked-example records, and saved result tables.

Compile with `latexmk -pdf revised_paper.tex`, or run `pdflatex revised_paper.tex` twice. No BibTeX run or external `.bib` file is needed. Upload the source ZIP as an Overleaf project and select `revised_paper.tex` as the main document.

The missing style file was obtained from the [official TACL template page](https://transacl.org/ojs/index.php/tacl/about/submissions). All 21 bibliography entries and their DOI links were recovered from pages 13–15 of the supplied PDF, preserving the original citation keys and reference content. The bibliography was not independently re-audited against the publications.

## Author checks that remain

These are gaps in the supplied research documentation, not information that can be safely filled by rewriting. They are also marked with `AUTHOR CHECK` comments in the LaTeX where relevant.

1. **Reference evidence:** supply the external source-to-reference mapping for the 80 reference perspectives. `gold_standard.json` contains summaries, explanations, identifiers, and extremity tiers, but no source citations. The manuscript retains the author's description that the references were externally documented; that provenance has not been independently verified.
2. **Construction decisions:** describe who selected and summarised positions, how distinctness was decided, how five positions were selected when more were available, and the operational rule for classifying the comparison settings as WEIRD. Do not imply algorithmic or prespecified matching if that was not done.
3. **Extremity analysis:** document the annotator(s), tier definitions, and the statistic and permutation scheme behind the reported `p = 0.148`. No matching implementation/result record was found in the supplied project. The reported value is preserved with an explicit qualification and is not used to support inference.
4. **Availability:** insert a final public repository or archival URL. The original address ended in `REPOSITORY`; no remote was configured in the local project. The revised availability paragraph describes the files actually provided.
5. **Submission details:** replace or restore the final author metadata when appropriate. The PDF retains the source's anonymous submission format. Funding details are preserved. Check final journal submission requirements separately.

## Verification

An independent check validates all 21 citation keys and bibliography entries; both archived prompt bodies; original reported numerical values; the 13-model main table; the supplementary precision/recall/F1 table; the 208 retained responses and 1,040 perspectives; and all 25 assignments in the worked example. Supplementary recall intervals reproduce the original displayed values exactly to avoid floating-point rounding differences between tables.

The PDF is compiled and its rendered pages checked for overlaps, clipped equations, misplaced captions, and unreadable tables. The original input files and research data remain unchanged.
