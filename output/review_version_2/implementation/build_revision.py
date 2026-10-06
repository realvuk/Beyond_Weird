"""Apply review edits to a separate manuscript copy and retain exact edit records."""
from pathlib import Path
import hashlib
import json
import re
import shutil

BASE = Path(__file__).resolve().parent
SOURCE = Path('/Users/vuk/Downloads/Vuk_First_Journal_Paper')
OUT = BASE / 'manuscript'
original = (SOURCE / '0_version_2.tex').read_text()
lines = original.splitlines(keepends=True)
edits = []


def edit(key, start, end, new, reason, location=None, status='Applied'):
    old = ''.join(lines[start-1:end])
    if callable(new):
        new = new(old)
    assert old != new, key
    edits.append(dict(id=key, tex_start=start, tex_end=end, old=old.rstrip(),
                      new=new.rstrip(), reason=reason, location_key=location or key,
                      status=status))


edit('preamble_hyperref', 11, 11, '', 'Let the journal style load hyperref after float-related packages, preventing duplicate float destinations.')
edit('preamble_cleveref', 19, 19, '', 'Move cleveref after the style loads hyperref.')
edit('preamble_style_order', 62, 62, '\\usepackage{tacl2021v1}\n\\usepackage{cleveref}\n', 'Load cross-reference support in the correct order; no body text changes.')
edit('abstract', 166, 166, lambda s: s.replace(
    r'(95\% CI: $-10.3$ to $7.7$)', r'(95\% $t$-based CI: $-10.3$ to $7.7$)').replace(
    "Judges agreed similarly on both sets of topics (Fleiss' $\\kappa=0.77$), but agreement does not establish accuracy.",
    "Inter-judge agreement was similar across the two settings (pooled Fleiss' $\\kappa=0.77$), but agreement does not establish accuracy."),
    'Name the interval procedure and identify the pooled agreement coefficient; all numbers remain unchanged.')
edit('contributions', 194, 194, 'The paper makes two contributions:\n', 'The list contains two contributions, not three.')
edit('superglue', 212, 212, lambda s: s.replace(
    r'Culturally focused benchmarks also document uneven resource coverage, including for Serbian and other South Slavic languages \cite{perovicSerbianSuperGLUEEvaluation2026}.',
    r'Language-specific evaluation resources also remain unevenly developed. Serbian SuperGLUE addresses gaps in complex language-understanding evaluation for Serbian and motivates broader coverage of South Slavic languages \cite{perovicSerbianSuperGLUEEvaluation2026}.'),
    'Distinguish language-understanding resources from cultural-perspective benchmarks.')
edit('overtonbench', 220, 220,
     r"The closest benchmark is OvertonBench, which evaluates perspective coverage using viewpoint groups derived from human responses and ratings of how well model outputs represent participants' views \cite{poole-dayanBenchmarkingOvertonPluralism2025}. Our study instead measures recovery of fixed, externally documented reference perspectives in structurally matched WEIRD and Serbian controversies. The contribution is this matched comparison across settings; differences in reference construction and scoring preclude direct comparison of absolute scores between the two benchmarks."+'\n',
     'Make the measurement distinction and incremental contribution explicit.')
edit('judge_citation', 224, 224,
     r'Evaluating coverage requires deciding whether differently worded statements express the same stance. LLM judges can assess this relationship, but their agreement with human assessments can vary across the models being evaluated \cite{poole-dayanBenchmarkingOvertonPluralism2025}.'+'\n',
     'Narrow the claim to the inspected evidence; remove the mismatched Chen citation explicitly.')
edit('weird_scope', 239, 240, lambda s: s.split('% AUTHOR CHECK')[0].replace(
    'Here, WEIRD and Serbian identify the two benchmark groups; Serbia is the single non-WEIRD setting studied.',
    'Comparator selection was guided by broad Western, educational, industrial and economic characteristics, rather than a quantified country-classification rule. WEIRD therefore labels the selected comparator populations in Table~\\ref{tab:topics}; it is not a validated binary country classification or representative sampling of a cultural category. Poland was included as a borderline case under this investigator judgment.'),
    'Report the author-confirmed investigator-guided grouping and the acknowledged borderline inclusion of Poland, without inventing a formal classification rule.')
edit('source_ledger', 265, 265, lambda s: s.replace(
    'Every perspective is linked to its supporting sources, and these links will be released with the benchmark.',
    'The first author selected five distinct stances per topic from the linked research and reporting. The source workbook records a source entry for each of the 80 reference perspectives. The accompanying source ledger links the evaluated reference identifiers to their workbook cells and preserves both the source text and any embedded hyperlink. All reference summaries and explanations in the workbook match the evaluated reference set exactly. Source entries identify the evidence used in construction; they do not imply that every clause of an advocate-style explanation is a quotation or a measured population belief.'),
    'Replace the missing-source concern with the newly supplied workbook and an explicit provenance ledger.')
edit('source_language', 267, 267,
    'Reference summaries and explanations were written in English. Sources cited for Serbian topics include English-language research, reporting, and survey materials; the language of the cited material was therefore not uniformly Serbian.\n',
    'Correct the unsupported blanket claim that all Serbian-topic sources are in Serbian.')
edit('size_groups', 300, 300, lambda s: s.replace(
    r'Gemma 4 31B and Llama 3.3 70B are smaller only relative to the other open-weight models in this selection, \textbf{[measured by total parameter count]}.',
    r'The smaller open-weight group consists of the two selected systems labelled 31B and 70B, Gemma 4 31B and Llama 3.3 70B; the other six open-weight systems form the larger group. These labels identify the groups used in this comparison rather than a general size taxonomy.'),
    'Remove the visible drafting note and define membership without inventing a parameter-count rule.')
edit('panel_protection', 340, 340, lambda s: s[:s.index("Because a generator's panel")] +
    r'Each generator is judged by the same panel on its WEIRD and Serbian topics, avoiding changes in panel membership between the two settings. This does not exclude topic-dependent or culturally differential judging errors. Differences between panels may also affect comparisons of overall recall between generators (Section~\ref{sec:rq2}).'+'\n',
    'Replace an unjustified guarantee with the actual control provided by constant panel membership.')
edit('notation', 362, 368,
    r'''Each topic receives equal weight. Let $\overline R_m$ denote the model's overall recall, and let $\overline R_m^{\mathrm W}$ and $\overline R_m^{\mathrm S}$ denote its mean recall on WEIRD and Serbian topics, respectively. Overall model recall averages its $16$ model-topic scores; WEIRD and Serbian recall each average eight:
\begin{equation}
\overline R_m=\frac{1}{16}\sum_{t=1}^{16}R_{mt}
=\frac{\overline R_m^{\mathrm W}+\overline R_m^{\mathrm S}}{2}.
\label{eq:model-recall}
\end{equation}
''', 'Introduce model-summary symbols before their first equation; preserve the equation.')
edit('stats_summary', 389, 389, lambda s: s.rstrip() +
    r' Pairwise model tests and model-level intervals are also checked using matched-pair blocks, because the individual-topic procedures do not retain the pairing (Appendices~\ref{app:model_pair_tests} and~\ref{app:bootstrap}).'+'\n',
    'Make the new existing-data sensitivity visible in the main methods.')
edit('rq2_pairwise', 418, 418, lambda s: s.replace(
    r'Of the 78 pairwise model comparisons, 15 remain significant after Benjamini--Hochberg adjustment (Appendix~\ref{app:pairwise_results}).',
    r'Of the 78 pairwise model comparisons, 15 remain significant after Benjamini--Hochberg adjustment when the 16 topics are treated as separate sign-flip units. None remains significant when the eight matched pairs are retained as blocks (minimum adjusted $p=0.087$). The inferential result is therefore sensitive to the unit of analysis, although the mean differences are unchanged (Appendix~\ref{app:pairwise_results}).'),
    'Retain the historical result and add the verified pair-blocked sensitivity without claiming equivalence.')
edit('figure1_interval_caption', 412, 412, lambda s: s.replace(
    'Pair-specific confidence intervals are not shown.',
    r'Pair-specific confidence intervals are not shown. The $t$-based interval for the mean is reported in Section~\ref{sec:rq1}.'),
    'Explicitly distinguish the displayed bootstrap interval from the t interval used in the abstract.')
edit('rq2_panel_attribution', 453, 453, lambda s: s[:s.index("Google's two generators")] +
    r"Google's two generators are never scored by this judge. Small recall differences between them and other models, such as Gemma 4 31B's closeness to GPT 5.5, should therefore be interpreted with this difference in panel composition in mind."+'\n',
    'Avoid attributing a measured fraction of between-model differences to panels without identifying that effect.')
edit('rq3_effect', 457, 457, lambda s: s.replace(
    'The groups differ in composition:',
    r'The US-minus-China difference is $-0.030$ (95\% pair-bootstrap CI $[-0.048,-0.013]$). The groups differ in composition:').replace(
    'excluding them reduces the difference to about $-0.020$.',
    'excluding them reduces the magnitude of the US-minus-China difference to about $-0.020$.'),
    'Add the verified existing interval for overall recall and specify the subtraction order.')
edit('rq3_duplicate', 475, 475, lambda s: s.replace(
    r' Of the 78 pairwise model comparisons, 15 remain significant after Benjamini--Hochberg adjustment (Appendix~\ref{app:pairwise_results}).', ''),
    'Remove the duplicated model-comparison result from the developer-country subsection.')
edit('discussion_duplicate', 508, 508, '', 'Delete the standalone sentence repeating the immediately preceding paragraph.')
edit('discussion_categories', 523, 523, lambda s: s.replace(
    'These categories are therefore poor substitutes for measuring perspective coverage directly.',
    'These categories did not reliably summarise the variation among the selected models.').replace(
    r' Appendix~\ref{app:extremity} reports descriptive summaries of perspective extremity; these do not establish why coverage varies across topics.', ''),
    'Limit the category interpretation to the selected models and remove the pointer to the author-withdrawn extremity analysis.')
edit('deliberation_citation', 533, 533, lambda s: s.replace(', kimDEBATEDevilsAdvocateBased2024a', ''),
    'Remove DEBATE from the human-deliberation citation group; its evaluation setting differs.')
edit('reference_limits_language', 541, 541, lambda s: s.replace(
    'Reference statements for Serbian topics are English summaries of Serbian-language sources, so translation choices may affect how closely model outputs match them.',
    'Reference statements for Serbian topics are English summaries of sources in more than one language, so summarisation and translation choices may affect how closely model outputs match them.'),
    'Propagate the corrected source-language description into the limitations.')
edit('power_and_bound', 551, 551, lambda s: s.replace(
    'is likely to be too narrow;', 'may have limited coverage accuracy;').replace(
    'The data therefore argue against a WEIRD advantage much larger than about six points for pairs like these, but cannot exclude smaller advantages or moderate differences favouring Serbian topics.',
    'Under the independent-pair and $t$-interval assumptions, the one-sided bound is approximately six points. It is conditional on these assumptions and the selected benchmark; it does not establish a general upper bound on cultural disparities. Smaller WEIRD advantages and moderate differences favouring Serbian topics remain compatible with the interval.').replace(
    r'Given this between-pair variation, a one-sided test at $\alpha=0.05$ would detect a five-point WEIRD advantage only about one time in three, and reaches 80\% power only for advantages of about 10.5 points.',
    r'An illustrative sensitivity calculation for a one-sided one-sample $t$-test at $\alpha=0.05$, assuming normally distributed pair-level differences and using the observed SD, gives approximately 32\% power for a five-point WEIRD advantage and 80\% power for an advantage of about 10.5 points. These values describe the $t$-test calculation, not the exact Wilcoxon procedure used for the primary test.'),
    'Qualify the bound and correctly identify the power calculation; preserve reported numerical values.')
edit('availability', 575, 577,
    r'''The accompanying source package contains the topic definitions, evaluated reference statements, original source workbook, reference-to-source ledger, model and judge configurations, worked-example record, and supplementary result tables. It also includes the saved model-topic scores and reproducible scripts for the additional matched-pair sensitivity analyses. The ledger preserves the workbook's source text and hyperlinks separately where they differ. The final repository or archival identifier will be added before submission.
% AUTHOR QUERY: deposit the final package and replace the final sentence with its actual persistent URL; resolve the source-ledger query list first.
''', 'Make the local review package concrete without fabricating a public repository URL.',
     status='Applied local-package description; public archive pending')
edit('judge_table_reference', 708, 708, lambda s: s.rstrip() +
    r' Table~\ref{tab:judge_substitutions} lists the substitutions.'+'\n',
    'Add the missing explicit Table 7 citation.')
edit('judge_table_layout', 714, 726,
    r'''\small
\begin{tabularx}{\columnwidth}{@{}Yp{0.25\columnwidth}p{0.20\columnwidth}@{}}
\toprule
Generator & Base judge removed & Substitute \\
\midrule
GPT 5.5 / GPT-OSS 120B & GPT 5.5 & Grok 4.5 \\
Claude Opus 4.8 & Claude Sonnet 5 & Grok 4.5 \\
Gemini 3.1 Pro / Gemma 4 31B & Gemini 3.1 Pro & Grok 4.5 \\
DeepSeek V4 Pro & DeepSeek V4 Pro & Qwen 3.7 Max \\
Kimi K2.6 & Kimi K2.6 & Grok 4.5 \\
\bottomrule
\end{tabularx}
''', 'Wrap long table cells instead of shrinking the entire table.')
edit('bootstrap_details', 801, 801, lambda s: s.replace(
    'The reported primary interval is', 'The pair-bootstrap interval is').rstrip() +
    r' As a sensitivity analysis for each model, we also resample the eight matched pairs with replacement, retaining both topics of each pair and their equal weights. We use $10{,}000$ resamples and a fresh NumPy generator with seed $42$. The resulting intervals, alongside the original topic-bootstrap intervals, are supplied in \path{supplementary/model_pair_bootstrap_ci.csv}. This changes the resampling unit but not the model means.'+'\n',
    'Correct the interval label and document the new matched-pair model-interval sensitivity.')
edit('owen_citation', 834, 834, lambda s: s.replace(
    r'\footnote{The resampling scheme follows Owen (2007), \emph{The pigeonhole bootstrap}, \href{https://arxiv.org/abs/0712.1111}{arXiv:0712.1111}.}',
    r' The resampling scheme follows \citet{owen2007pigeonhole}.'),
    'Move the already identified Owen source from a footnote into the bibliography.')
edit('pairwise_details', 878, 878, lambda s: s.rstrip() + '\n\n'+
    r'''The individual-topic sign-flip procedure assumes sign exchangeability at the topic level and does not preserve the matched pairs. To assess sensitivity to this choice, we also form eight pair-level contrasts,
\[
x_p=\frac{R_{a,p}^{\mathrm W}+R_{a,p}^{\mathrm S}}{2}
    -\frac{R_{b,p}^{\mathrm W}+R_{b,p}^{\mathrm S}}{2},
\]
and enumerate all $2^8=256$ sign assignments using their mean as the statistic. Two-sided tail comparisons allow a numerical tolerance of $10^{-12}$, and Benjamini--Hochberg correction again covers all $78$ model comparisons. This procedure assumes sign-exchangeable pair-level contrasts and preserves the original mean difference. As a numerical check, exhaustive enumeration of the $2^{16}$ individual-topic sign patterns still yields 15 adjusted significant comparisons, whereas the pair-blocked procedure yields none (minimum adjusted $p=0.087$). The discrepancy therefore reflects the inferential unit rather than Monte Carlo sampling alone. The pair-blocked results qualify the individual-topic findings; neither procedure establishes equivalence between models.
''', 'Document the exact new sensitivity and its assumptions without silently replacing the original test.')
edit('pairwise_results', 954, 954, lambda s: s.rstrip() +
    r' The companion file \path{supplementary/pair_blocked_model_comparisons.csv} reports the individual-topic Monte Carlo results, exact individual-topic checks, and exact matched-pair results for the same comparisons. Mean recall differences are unchanged; 15 comparisons survive adjustment under the individual-topic procedures and none under pair blocking.'+'\n',
    'Point readers to both inferential specifications and their results.')
edit('figure2_legibility', 916, 916, r'\includegraphics[width=\textwidth]{plots/paired_recall.pdf}'+'\n',
    'Use a vector figure with larger labels and a two-row arrangement; preserve all three panels and the 104 scores.')
edit('per_model_table_layout', 966, 991, lambda s: s.replace(r'\resizebox{\textwidth}{!}{%'+'\n','').replace('\\end{tabular}%\n}\n','\\end{tabular}\n'),
    'Remove automatic enlargement of Table 9 while preserving all entries.')
edit('per_model_table_reference', 994, 994, lambda s:
    r'Table~\ref{tab:per_model_weird_gap} reports the per-model comparisons. '+s,
    'Add the missing explicit Table 9 citation.')

# Keep the exact original statements for unresolved historical methods; questions
# remain comments, while the guide tells the author what is not yet resolved.
edit('remove_extremity', 898, 906, '',
    'Remove Appendix D.9 and its counts/correlations at the author\'s explicit request. Original data remain archived; no main RQ result changes.')
edit('worked_tables_layout', 1040, 1074, lambda s: s.replace(
    '\\begin{table}[htbp]\n\\centering\\small', '\\begin{table*}[!tp]\n\\begin{minipage}[t]{0.48\\textwidth}\n\\centering\\small', 1).replace(
    '\\end{table}\n\n\\begin{table}[htbp]\n\\centering\\small',
    '\\end{minipage}\\hfill\n\\begin{minipage}[t]{0.48\\textwidth}\n\\centering\\small',1).replace(
    '\\end{table}\n', '\\end{minipage}\n\\end{table*}\n'),
    'Place the generated-summary table and assignment table side by side, retaining their separate captions and labels.')
edit('identifier_table_layout', 1092, 1092, '\\begin{table*}[!tp]\n',
    'Allow the endpoint table to share the appendix float page with the worked-example tables.')

covered = set()
for e in edits:
    occupied = set(range(e['tex_start'], e['tex_end']+1))
    assert not covered.intersection(occupied), e['id']
    covered.update(occupied)
revised_lines = list(lines)
for e in sorted(edits, key=lambda e: e['tex_start'], reverse=True):
    replacement = e['new'] + ('\n' if e['new'] else '')
    revised_lines[e['tex_start']-1:e['tex_end']] = replacement.splitlines(keepends=True)
revised = ''.join(revised_lines)

# Bibliographic pagination is corrected separately, and the removed citation
# becomes uncited; the original database record remains available in the source.
bib = (SOURCE/'tacl2021.bib').read_text()
assert 'pages = {10091--10109}' in bib
bib = bib.replace('pages = {10091--10109}', 'pages = {10080--10098}')
bib = re.sub(r'@misc\{sorensenRoadmapPluralisticAlignment2024,.*?\n\}', r'''@inproceedings{sorensenRoadmapPluralisticAlignment2024,
  title = {Position: A Roadmap to Pluralistic Alignment},
  author = {Sorensen, Taylor and Moore, Jared and Fisher, Jillian and Gordon, Mitchell L. and Mireshghallah, Niloofar and Rytting, Christopher Michael and Ye, Andre and Jiang, Liwei and Lu, Ximing and Dziri, Nouha and Althoff, Tim and Choi, Yejin},
  booktitle = {Proceedings of the 41st International Conference on Machine Learning},
  pages = {46280--46302},
  year = {2024},
  volume = {235},
  series = {Proceedings of Machine Learning Research},
  publisher = {PMLR},
  url = {https://proceedings.mlr.press/v235/sorensen24a.html}
}''', bib, flags=re.S)
bib += '''\n@article{owen2007pigeonhole,
  author = {Owen, Art B.},
  title = {The pigeonhole bootstrap},
  journal = {The Annals of Applied Statistics},
  year = {2007},
  volume = {1},
  number = {2},
  pages = {386--411},
  doi = {10.1214/07-AOAS122}
}\n'''
OUT.mkdir(exist_ok=True)
(OUT/'revised_manuscript.tex').write_text(revised)
(OUT/'tacl2021.bib').write_text(bib)
shutil.copy2('/Users/vuk/Downloads/Perspectives.xlsx', OUT/'supplementary/Perspectives.xlsx')
(BASE/'edit_manifest.json').write_text(json.dumps(edits, ensure_ascii=False, indent=2)+'\n')
(BASE/'original_hashes.json').write_text(json.dumps({
    name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
    for name in ['0_version_2.tex','0_version_2.pdf','tacl2021.bib']}, indent=2)+'\n')
assert r'\textbf{[measured by total parameter count]}' not in revised
assert 'The paper makes three contributions' not in revised
assert 'Panel substitution therefore cannot create' not in revised
assert all(x in revised for x in [r'$p=0.680$',r'$0.581$',r'$0.594$',r'$-0.013$'])
print(f'Applied {len(edits)} tracked edits to {OUT}/revised_manuscript.tex')
