"""Assemble the review guide and portable manuscript package from checked edits."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import textwrap
import zipfile
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, Spacer, PageBreak

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
MAN = BASE / 'manuscript'
OUT = ROOT / 'output/pdf/review_implementation'
OUT.mkdir(parents=True, exist_ok=True)
edits = sorted(json.loads((BASE/'edit_manifest.json').read_text()), key=lambda e:e['tex_start'])
locations = {x['id']:x for x in json.loads((BASE/'pdf_line_locations.json').read_text())}

# Preserve workbook evidence; record the bounded subsequent check separately.
audit_path = BASE/'source_audit/SOURCE_AUDIT.md'
audit = audit_path.read_text()
audit = audit.replace('The decoded candidate URL is retained separately and is unverified; the original source is not silently replaced.',
    'The decoded public candidate was opened and concerns border protection, but full support for this reference remains unresolved; the original source is not silently replaced.')
audit = audit.replace('Only three workbook-linked public pages were opened.', 'Four public pages were opened, including the public candidate decoded from the private-chat link.')
if '4. [Magyar Nemzet' not in audit:
    marker = '\nThese checks make the manuscript'
    audit = audit.replace(marker, '\n4. [Magyar Nemzet, National consensus in Hungary on border protection](https://magyarnemzet.hu/english/2025/10/national-consensus-in-hungary-on-border-protection), the candidate decoded from `01_WEIRD!D8`: accessible public article dated 2 October 2025. It discusses border protection and a migration-policy poll. This supports topic relevance, not every clause about Ukraine or family policy in the benchmark explanation. The ledger field remains labelled unverified-by-extraction; this subsequent bounded check does not replace the original workbook entry.\n'+marker)
audit_path.write_text(audit)
for name in ['source_provenance_ledger.csv','source_provenance_ledger.json','source_urls.csv','extraction_summary.json','SOURCE_AUDIT.md']:
    shutil.copy2(BASE/'source_audit'/name, MAN/'supplementary'/name)

# Minimal self-contained analysis inputs; no model calls and no hidden project paths.
analysis = MAN/'analysis'
inputs = analysis/'inputs'
inputs.mkdir(parents=True, exist_ok=True)
input_files = {
    'results/agg/prf_per_topic.csv':'prf_per_topic.csv',
    'results/agg/pairwise_models.csv':'pairwise_models.csv',
    'results/agg/ranking.csv':'ranking.csv',
    'config/models.json':'models.json',
    'output/pdf/version_3/supplementary/developer_country_contrasts.csv':'developer_country_contrasts.csv'}
script = (BASE/'statistics/reproduce_sensitivity.py').read_text()
script = script.replace('Run from the repository root:\n.venv/bin/python output/review_version_2/implementation/statistics/reproduce_sensitivity.py',
    'Run from the extracted package root:\npython3 analysis/reproduce_sensitivity.py')
script = script.replace('ROOT = OUT.parents[3]', "ROOT = OUT / 'inputs'")
for source,dest in input_files.items():
    shutil.copy2(ROOT/source, inputs/dest)
    script = script.replace(source, dest)
(analysis/'reproduce_sensitivity.py').write_text(script)
extractor = (BASE/'source_audit/extract_sources.py').read_text()
extractor = extractor.replace("WORKBOOK = Path('/Users/vuk/Downloads/Perspectives.xlsx')", "WORKBOOK = ROOT.parent / 'supplementary/Perspectives.xlsx'")
extractor = extractor.replace("GOLD = Path('/Users/vuk/Downloads/BWEIRD/data/gold_standard.json')", "GOLD = ROOT.parent / 'supplementary/gold_standard.json'")
(analysis/'extract_sources.py').write_text(extractor)
shutil.copy2(BASE/'statistics/README.md', analysis/'STATISTICAL_FINDINGS.md')
p = analysis/'STATISTICAL_FINDINGS.md'
p.write_text(p.read_text().replace('Run from the BWEIRD repository root:', 'Run from the extracted package root:').replace('.venv/bin/python output/review_version_2/implementation/statistics/reproduce_sensitivity.py', 'python3 analysis/reproduce_sensitivity.py').replace('`proposed_statistical_revisions.tex` provides exact replacement/insertion blocks for the editor. Its `supplementary/` paths assume the two CSV files below are copied into the final source package\'s supplementary folder.', 'The accompanying change guide records the exact manuscript edits. The submitted supplementary copies are already included.'))
for name in ['pair_blocked_model_comparisons.csv','model_recall_interval_sensitivity.csv','sensitivity_summary.json']:
    shutil.copy2(BASE/'statistics'/name, analysis/name)

mapping = {
 'abstract':['abstract_interval','abstract_agreement'],
 'contributions':['contribution_count'], 'superglue':['citation_weird_prompting'],
 'overtonbench':['citation_closest_benchmark'], 'judge_citation':['citation_judge_sensitivity'],
 'weird_scope':['operational_weird_definition'], 'source_ledger':['reference_construction'],
 'source_language':['reference_construction'], 'size_groups':['parameter_note'],
 'panel_protection':['panel_protection_claim'], 'notation':['eq2_definitions'],
 'stats_summary':['main_pairwise_unit'], 'figure1_interval_caption':['figure1_layout'],
 'rq2_pairwise':['rq2_pairwise_result'],
 'rq2_panel_attribution':['rq2_panel_causality_start','rq2_panel_causality_end'],
 'rq3_effect':['rq3_sign_interval'], 'rq3_duplicate':['rq3_duplicate_pairwise'],
 'discussion_duplicate':['discussion_duplicate'],
 'discussion_categories':['discussion_categories','discussion_extremity_pointer'],
 'deliberation_citation':['citation_deliberation'],
 'reference_limits_language':['limits_reference_review'],
 'power_and_bound':['limits_interval_bound','limits_power'],
 'availability':['availability_start','availability_end'],
 'judge_table_reference':['table7_crossref_start','table7_crossref_end'],
 'judge_table_layout':['table7_legibility'],
 'bootstrap_details':['d1_model_intervals','d1_primary_intervals','d1_power'],
 'pairwise_details':['d6_pairwise_start','d6_pairwise_end'],
 'remove_extremity':['d9_tiers'], 'figure2_legibility':['figure2_legibility'],
 'pairwise_results':['e3_pairwise_results'],
 'per_model_table_layout':['table9_layout'],
 'per_model_table_reference':['table9_missing_crossref'],
 'worked_tables_layout':['table10_layout','table11_layout'],
 'identifier_table_layout':['table12_layout']}

def locator(e):
    if e['id'].startswith('preamble_'):
        return 'No printed PDF line: preamble-only change; repairs internal links to floats.'
    if e['id']=='owen_citation':
        return 'Original PDF p. 16, lines 1598-1599 (footnote 2); associated crossed-bootstrap paragraph in Appendix D.3.'
    return '; '.join(f"original PDF p. {locations[k]['page']}, lines {locations[k]['lines']}" for k in mapping[e['id']])

def changed_span(old,new):
    """One exact contiguous replacement, expanded to whitespace boundaries."""
    i=0
    while i<min(len(old),len(new)) and old[i]==new[i]: i+=1
    j=0
    while j<min(len(old)-i,len(new)-i) and old[-1-j]==new[-1-j]: j+=1
    while i>0 and not old[i-1].isspace(): i-=1
    while j>0 and not old[len(old)-j].isspace(): j-=1
    a,b=old[i:len(old)-j if j else None],new[i:len(new)-j if j else None]
    assert old[:i]+b+(old[len(old)-j:] if j else '')==new
    return a,b,old[max(0,i-160):i],old[len(old)-j:len(old)-j+100] if j else ''

parts=[]
def add(s): parts.append(s)
add('# Manuscript implementation and original-PDF change guide\n\n28 September 2026. Target: unspecified AI/NLP journal.\n')
add('All locations below refer to the grey printed margin numbers in the original 22-page `0_version_2.pdf`, not the revised PDF or PDF-extraction row numbers. Each page has two columns of margin numbers. Full-width figures and tables are located by their caption plus the nearby margin grid. Line ranges identify the affected passage; exact LaTeX snippets below define the replacement boundaries. Source-line numbers refer to the original `0_version_2.tex`. Preamble changes have no printed body line.\n')
add('## What is implemented\n\nThe separate manuscript contains 38 tracked LaTeX edits, bibliography updates, a legible vector Figure 2, and accompanying source and statistical evidence. Original manuscript files and the workbook remain unchanged. The title, main RQ order, prompts, reference texts, main equations, reported point estimates, and primary RQ1 result are preserved. Descriptive judge checks remain after RQ1-RQ3.\n')
add('The supplied workbook resolves the previous missing source-to-perspective mapping: all 80 summaries and all 80 explanations exactly match the evaluated reference set, and all 80 source cells contain information. Seventy-four contain URLs and six contain textual citations. This verifies provenance correspondence, not complete support for every claim. Seven specific source records still need author attention; they are listed below.\n')
add('Your clarification is incorporated: topic matching began with Serbian topics; comparator inclusion was investigator-guided using broad WEIRD attributes, with Poland acknowledged as borderline; distinct stances were chosen from the linked research. No formal threshold, selection algorithm, or tier-coding procedure has been invented. Appendix D.9 and its main-text pointer are removed at your request. Original archived metadata and the verbatim generation prompt remain intact.\n')
add('The new analysis reruns saved scores only. The original 16-topic model comparison gives 15 BH-adjusted significant contrasts; exact enumeration at the same unit also gives 15. Keeping the eight matched pairs together gives zero (minimum adjusted p = 0.08705357). This is a sensitivity to the inferential unit, not evidence of model equivalence. All model means are unchanged. The primary RQ1 test is unchanged.\n')
add('## Three highest-impact changes\n\n1. Reference construction and provenance: original p. 3, lines 268-288; source workbook and an exact 80-record ledger are now supplied.\n2. Inferential-unit sensitivity: p. 7, lines 665-668, with methods at p. 6, 584-596 and p. 17, 1646-1671; both specifications are reported.\n3. Calibrated claims: p. 5, 476-481; p. 11, 1023-1038; fixed panels, uncertainty bounds, and illustrative t-test power are described without unsupported guarantees.\n')
add('## Applied edits with exact locations\n\nApply these only to the original source if merging manually. They are already present in `revised_manuscript.tex`. “Replace” means replace the exact old span with the exact new span; retained surrounding text is intentionally omitted. “Add” gives the preceding anchor. For the PDF, use the page, margin range, and quoted anchor together. Copy from the Markdown version or source file to avoid PDF soft wrapping.\n')
analysis_ids={'stats_summary','rq2_pairwise','rq3_effect','bootstrap_details','pairwise_details','pairwise_results'}
optional_ids={'discussion_duplicate','rq3_duplicate','notation','worked_tables_layout','identifier_table_layout'}
for n,e in enumerate(edits,1):
    a,b,before,after=changed_span(e['old'],e['new'])
    action='Replace' if a and b else ('Delete' if a else 'Add')
    title=e['id'].replace('_',' ').capitalize()
    add(f"### {n:02d}. {title}\n\n**Location:** {locator(e)} Original LaTeX lines {e['tex_start']}-{e['tex_end']}.\n")
    kind='Existing-data analysis and reporting' if e['id'] in analysis_ids else 'Editing / documented clarification'
    priority='Optional presentation or compactness improvement, applied' if e['id'] in optional_ids else 'Review correction, applied'
    if e['id']=='availability': priority='Partly resolved; persistent archive identifier remains a submission action'
    add(f"**Reason:** {e['reason']} **Type/status:** {kind}. {priority}.\n")
    if e['id'] in mapping:
        first=locations[mapping[e['id']][0]]
        add(f"**PDF anchor:** “{first['anchor_start']}”\n")
    if not a:
        add('**Add after this exact source anchor:**\n\n```latex\n'+before+'\n```\n')
    else:
        add(f'**{action} this exact source span:**\n\n```latex\n'+a+'\n```\n')
    if b:
        add('**With / insert:**\n\n```latex\n'+b+'\n```\n')
    if e['id']=='figure2_legibility':
        add('The referenced `plots/paired_recall.pdf` is supplied in the source package; changing the filename alone is insufficient. It retains the same 104 cells and all three panels.\n')

add('## Bibliography and added files\n')
bib=(MAN/'tacl2021.bib').read_text()
for label,key,loc,why in [
 ('B1. Sorensen publication details','sorensenRoadmapPluralisticAlignment2024','Original p. 13, lines 1229-1233; anchor “Taylor Sorensen, Jared Moore, Jillian Fisher”','Replace the provisional preprint record with the inspected ICML/PMLR publication record, retaining its citation key.'),
 ('B2. Owen bibliography entry','owen2007pigeonhole','Original p. 16, lines 1598-1599, footnote 2','Add the bibliographic record below. The corresponding text edit removes the manual footnote and uses the citation key. There is no original bibliography line for this new entry.')]:
    entry=re.search(r'@\w+\{'+key+r',.*?\n\}',bib,re.S).group(0)
    add(f'### {label}\n\n**Location:** {loc}. {why}\n\n```bibtex\n{entry}\n```\n')
add('### B3. Removed in-text citations and corrected unused metadata\n\nThe Chen citation is removed at original p. 3, line 220 (edit 08 in source order); its rendered reference at p. 12, lines 1130-1139 disappears automatically after BibTeX because it is no longer cited. The retained database record corrects `pages = {10091--10109}` to `pages = {10080--10098}`. This is an explicit metadata correction, not a new citation. The Kim/DEBATE citation is removed at p. 10, line 973; its entry at p. 12, lines 1182-1188 likewise disappears from the rendered reference list. Do not manually edit the generated `.bbl`. Both unused database records remain available.\n')
add('### S1. Source supplement\n\n**Insertion location:** original p. 3, lines 277-279 and p. 11, lines 1098-1099 through p. 12, lines 1100-1103. Those passages already point to the accompanying source package after edits. Add the supplied original workbook, `source_provenance_ledger.csv` / `.json`, `source_urls.csv`, and `SOURCE_AUDIT.md` as supplementary files. A supplement itself has no original PDF line number. The extractor in `analysis/extract_sources.py` verifies the exact 80-record correspondence. Original source strings and conflicting native hyperlink targets are preserved separately.\n')
add('### S2. Statistical supplement\n\n**Insertion locations:** original p. 16, lines 1516-1533 and p. 18, lines 1744-1749. Add the supplied pair-blocked comparison CSV, model-pair bootstrap CSV, saved analysis inputs, and `analysis/reproduce_sensitivity.py`. The script verifies all 13 original intervals within 1e-12, all 78 unchanged mean differences, the exact sign-flip counts, and the saved RQ3 overall-recall interval. The new paired intervals are wider for six models and narrower for seven; do not claim that blocking necessarily widens them.\n')

add('## Remaining author actions\n\nThese are unresolved evidence or submission details, not edits that can be invented. The current copy is a revised review draft, not a claim of final submission readiness.\n')
query_table=audit.split('## Specific author actions\n\n',1)[1].split('\nThe six URL-free',1)[0]
add(query_table+'\n')
add('**Manuscript locations for all seven source queries:** original p. 3, lines 268-288 (construction and provenance) and p. 10, lines 985-999 through p. 11, lines 1000-1002 (scope of the reference set). The individual records occur in the workbook/supplement, so their exact actionable locators are sheet and cell, not invented PDF lines. For fracking p4/p5, also locate Table 2 on original p. 4, identified by the caption “Reference summaries for UK fracking”. Resolve the ledger entries first. If support is found, retain benchmark text and results. If an evaluated stance must change, that is a benchmark change requiring an explicit decision about affected scores and analyses; a new citation alone does not authorize changing it.\n')
add('1. **Persistent access:** original p. 11, 1098-1099 through p. 12, 1100-1103. Deposit the final package and replace “The final repository or archival identifier will be added before submission.” with “The benchmark, source ledger, saved scores, and analysis code are available at [actual persistent URL].” This sentence is a template only until the real URL exists. Local files are provided; nothing was published. This remains a submission blocker.\n')
add('2. **Author and venue information:** no target journal was specified. Venue-specific word/page limits, author statements, and anonymity requirements remain unverified. The PDF uses a TACL review template; that does not establish TACL as the intended journal. Check the acknowledgment at original p. 12, lines 1105-1111 against the chosen venue. The original hidden template-author fields have no printed PDF line and must be replaced with real author-supplied metadata for a non-anonymous version. Do not invent funding, ethics, conflict-of-interest, or contribution declarations.\n')
add('3. **Generation and judgment archive:** the portable package supplies saved topic scores, configurations, and new-analysis inputs, not a complete API rerun environment or raw generation/judgment logs. The availability sentence has been limited accordingly. If the submission will claim full end-to-end reproducibility, include the existing raw logs and original pipeline in the final archive and document their execution. No new experiments are required for this packaging action.\n')
add('## Optional work deliberately not presented as completed\n\nAppendix D.8 (original p. 17, lines 1693-1699 through p. 18, 1700-1707) remains as a labelled descriptive sensitivity. Removing it is an optional compactness choice, unlike the author-requested deletion of D.9. Its existing caveats and cross-references remain. No further deletion is necessary for the present RQ argument.\n\nHuman judge validation is not fabricated. The manuscript already states this limitation at original p. 11, lines 1006-1019, and the calibrated claims remain conditional on the evaluation procedure. A stratified human audit would support stronger validity claims; it is not imposed as an arbitrary new experiment for the current conditional findings. Likewise, extra countries, models, prompts, or generation repeats would expand the study rather than repair the implemented writing changes.\n')
add('## Verification and limits\n\nThe revised manuscript compiled with no unresolved references, overfull boxes, or duplicate hyperlink destinations. All 22 rendered manuscript pages were inspected. Source hashing confirms that the original manuscript and workbook were not edited. The 80-record text correspondence and additional statistics were checked programmatically; no new model generations or judgments were collected, and data authenticity was not established.\n\nOnly four workbook-related public pages received bounded live inspection: the UNDP migration publication page, two DESNZ Spring 2024 pages (renewables; energy infrastructure and security), and the Magyar Nemzet candidate decoded from the private-chat link. Their exact links and the limits of each check are in `supplementary/SOURCE_AUDIT.md`. This is not a claim to have authenticated all 80 underlying sources. The earlier citation audit also inspected the relevant OvertonBench, Serbian SuperGLUE, Chen, DEBATE, Sorensen, and Owen records/content used for the specific editorial corrections; it was not a verification of every cited article.\n')
add('The unresolved source records and archive/venue details above remain author actions. Everything that can be implemented from the supplied materials is integrated in a separate source copy; unsupported details have not been guessed.\n')
guide='\n'.join(parts)
guide=guide.replace('(edit 08 in source order)', '(see the judge-citation edit above)')
(OUT/'change_guide.md').write_text(guide)

# Plain, searchable PDF. Exact pasteable text is also supplied as Markdown.
fontdir=Path('/System/Library/Fonts/Supplemental')
for name,file in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf'),('Mono','Courier New.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.5,leading=13,spaceAfter=7),
 'h1':ParagraphStyle('h1',fontName='Bold',fontSize=21,leading=25,spaceAfter=14),
 'h2':ParagraphStyle('h2',fontName='Bold',fontSize=14,leading=18,spaceBefore=13,spaceAfter=9,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='Bold',fontSize=11,leading=15,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=8.6,leading=11.2,spaceAfter=8,textColor=colors.black,backColor=colors.HexColor('#f3f5f7'),borderPadding=5)}
def inline(s):
    s=escape(s)
    s=re.sub(r'\*\*(.*?)\*\*',r'<font name="Bold">\1</font>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Mono">\1</font>',s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#24577c">\1</link>',s)
    return s
story=[]
code=False
buf=[]
for line in guide.splitlines():
    if line.startswith('```'):
        if code:
            wrapped=[]
            for raw in buf:
                wrapped += textwrap.wrap(raw, width=93, expand_tabs=False, replace_whitespace=False, drop_whitespace=False, break_long_words=True, break_on_hyphens=False) or ['']
            story.append(Preformatted('\n'.join(wrapped), styles['code']))
            buf=[]
        code=not code
        continue
    if code: buf.append(line);continue
    if not line.strip():continue
    if line.startswith('|---'):continue
    if line.startswith('|'):
        cells=[x.strip() for x in line.strip('|').split('|')]
        if cells[0]=='Reference':continue
        story.append(Paragraph(inline(' / '.join(cells[:2])+': '+cells[2]+' '+cells[3]),styles['body']))
        continue
    key='body'
    for mark,sty in [('### ','h3'),('## ','h2'),('# ','h1')]:
        if line.startswith(mark):line=line[len(mark):];key=sty;break
    para=Paragraph(inline(line),styles[key])
    if line.startswith(('**Location:', '**Reason:', '**PDF anchor:', '**Replace ', '**Delete ', '**With /', '**Add after')):
        para.keepWithNext=True
    story.append(para)
def footer(c,doc):
    c.saveState()
    c.setFont('Body',8)
    c.setFillColor(colors.HexColor('#59616b'))
    c.drawString(43,25,'Change guide | locators refer to the original manuscript PDF')
    c.drawRightString(552,25,str(doc.page))
    c.restoreState()
SimpleDocTemplate(str(OUT/'change_guide.pdf'),pagesize=(595.28,841.89),rightMargin=43,leftMargin=43,topMargin=42,bottomMargin=43,title='Manuscript changes with original PDF line numbers',author='').build(story,onFirstPage=footer,onLaterPages=footer)

readme='''# Revised manuscript and review evidence

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
'''
(MAN/'README.md').write_text(readme)
for name in ['change_guide.md','change_guide.pdf']:
    shutil.copy2(OUT/name,MAN/name)
shutil.copy2(BASE/'edit_manifest.json',MAN/'edit_manifest.json')
shutil.copy2(BASE/'original_hashes.json',MAN/'original_hashes.json')
shutil.copy2(MAN/'revised_manuscript.pdf',OUT/'revised_manuscript.pdf')
shutil.copy2(MAN/'revised_manuscript.tex',OUT/'revised_manuscript.tex')
with zipfile.ZipFile(OUT/'revised_manuscript_source.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(MAN.rglob('*')):
        if p.is_file() and p.suffix not in {'.aux','.log','.blg','.fls','.fdb_latexmk','.out'}:
            z.write(p,p.relative_to(MAN))
assert len(edits)==38
assert all(locator(e) for e in edits)
with zipfile.ZipFile(OUT/'revised_manuscript_source.zip') as z:assert z.testzip() is None
for name,digest in json.loads((BASE/'original_hashes.json').read_text()).items():
    assert hashlib.sha256((Path('/Users/vuk/Downloads/Vuk_First_Journal_Paper')/name).read_bytes()).hexdigest()==digest
assert hashlib.sha256(Path('/Users/vuk/Downloads/Perspectives.xlsx').read_bytes()).hexdigest()=='f9f6c8d62236959176c463f468fe4df1c617b1bc62767427d51aefd438c1c61b'
print(f'Wrote guide, revised PDF, exact LaTeX, and source ZIP to {OUT}')
