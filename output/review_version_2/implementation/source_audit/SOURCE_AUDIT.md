# Source provenance audit

Read-only inspection of `/Users/vuk/Downloads/Perspectives.xlsx` against `/Users/vuk/Downloads/BWEIRD/data/gold_standard.json`, 28 September 2026. The workbook was not modified. SHA-256 values and reproducible extraction checks are in `extraction_summary.json` and `extract_sources.py`.

## What the workbook establishes

- The three sheets are `00_overview`, `01_WEIRD`, and `02_Serbian`. The overview contains the eight pair assignments and the 16-topic/80-perspective totals. The two reference sheets contain eight topics each, with five explanation/summary/source triplets per topic.
- All **80 summaries and all 80 full explanations match the canonical gold-standard JSON exactly**, including punctuation and whitespace. No fuzzy or inferred matching was needed. All topic titles also correspond to the same rows and pairs.
- All **80 source cells contain source information**. Of these, 74 have at least one URL and 6 contain textual citations only. There are 72 native hyperlink objects. Preserving both visible cell values and native targets gives 82 reference-to-URL associations and 62 distinct literal URL strings (including two fragment variants of the same private chat). These are URL counts, not counts of unique documents or independently verified sources.
- Three substantive visible-URL/native-hyperlink conflicts were found; both versions are preserved in the ledger. One further difference only removes a text fragment from a Claude chat URL.
- No comments, explicit extremity tiers, tier assignment rules, WEIRD inclusion criteria, source-selection rules, or reference-construction protocol are recorded in the workbook. Tier values in the exported ledger come from the gold JSON, not the workbook. The overview records assignments, not their justification.

The workbook therefore resolves the earlier absence of a source-to-reference mapping. A populated source cell does **not** by itself establish that every element of an advocate-voice explanation is supported by the source, or that the stance is held in the stated reference population.

## Specific author actions

| Reference | Workbook location | Evidence | Required action |
|---|---|---|---|
| Catalan independence p5 (`pair02_weird_p5`) | `01_WEIRD!P3` | Visible URL is a Converses a Catalunya article; native hyperlink points to a ResearchGate review of Kathryn Crameri's book. | Specify the intended source(s), preserve both in the working ledger, and identify the supporting passage. |
| Fracking p4 (`pair03_weird_p4`) | `01_WEIRD!M4` | Visible URL is an ECIU poll about MPs and net zero; native hyperlink points to the DESNZ renewable-energy report. | Resolve the link conflict and provide direct support for the reference's categorical anti-fracking stance. The cited DESNZ renewable report does not discuss shale gas/fracking. |
| Kosovo p3 (`pair02_serbian_p3`) | `02_Serbian!J3` | Visible Balkan Insight URL concerns Thaci's proposed border correction; native hyperlink points to a different article, “history's shadow.” | Specify the intended article(s) and support for the stance being held by people in Serbia. |
| Orbán p1 (`pair07_weird_p1`) | `01_WEIRD!D8` | A private Claude conversation is recorded as the source. Its displayed text fragment contains an encoded Magyar Nemzet URL. | Supply the underlying public document and supporting passage. The decoded public candidate was opened and concerns border protection, but full support for this reference remains unresolved; the original source is not silently replaced. |
| Kosovo p4 (`pair02_serbian_p4`) | `02_Serbian!M3` (explanation/summary `K3:L3`) | Broad references to HLC reports, named public intellectuals, and a foreign-policy-priority percentage; no identified HLC report or passage. Cells are red in the original workbook, without a legend. | Provide exact source titles/pages/URLs establishing the particular recognition/apology stance. A statistic about EU foreign-policy priority alone does not establish prevalence of this specific Kosovo stance. |
| Migrants p5 (`pair06_serbian_p5`) | `02_Serbian!P7` (explanation/summary `N7:O7`) | General references to party programmes and CRTA 2023–2024 media monitoring; no exact programme/report/passage. Original cells are red, without explanation. | Identify the exact documents and passages for the stated conspiratorial position. Do not infer why the cells were coloured red. |
| Fracking p5 (`pair03_weird_p5`) | `01_WEIRD!P4` | The sole listed URL is the DESNZ renewable-energy report; the benchmark statement is conditional support for shale gas. | Supply a fracking-specific source and a supporting passage. Do not replace the reference or recompute outcomes merely to repair a citation without an author decision. |

The six URL-free source cells are `02_Serbian!D2`, `G2`, `M2`, `P2`, `M3`, and `P7`. The first four contain named books/articles or a party programme with named secondary sources and should not be described as “missing sources.” Page/section locators would make the exact support auditable. `02_Serbian!J2` cites a book review and includes a DOI; retain its source type accurately rather than presenting the review as the underlying monograph.

## Bounded live verification

Four public pages were opened, including the public candidate decoded from the private-chat link. No attempt was made to authenticate all 80 references or to test availability of all 62 literal URL strings.

1. [UNDP, Attitudes to Refugee and Migrant Crisis in Serbia](https://www.undp.org/serbia/publications/attitudes-refugee-and-migrant-crisis-serbia), source for `02_Serbian!D7`: accessible English-language page, explicitly linking English quantitative and qualitative reports. Its description concerns survey rounds and migration-affected Serbian municipalities. This establishes an English source pathway; it does not validate every detail of the corresponding advocate-voice reference.
2. [DESNZ renewable energy, Spring 2024](https://www.gov.uk/government/statistics/desnz-public-attitudes-tracker-spring-2024/desnz-public-attitudes-tracker-renewable-energy-spring-2024-uk), source for `01_WEIRD!P4` and native target of `M4`: accessible English-language official report about renewables, windfarms, and solar farms. It does not supply the claimed fracking-specific conditional stance. This is a source-relevance concern, not a finding that the stance does not exist.
3. [DESNZ energy infrastructure and energy security, Spring 2024](https://www.gov.uk/government/statistics/desnz-public-attitudes-tracker-spring-2024/desnz-public-attitudes-tracker-energy-infrastructure-and-energy-security-spring-2024-uk), source for `01_WEIRD!D4`: accessible English-language official report with a shale-gas support section. Topic relevance is confirmed; the full support for each detail of the reference was not validated.

4. [Magyar Nemzet, National consensus in Hungary on border protection](https://magyarnemzet.hu/english/2025/10/national-consensus-in-hungary-on-border-protection), the candidate decoded from `01_WEIRD!D8`: accessible public article dated 2 October 2025. It discusses border protection and a migration-policy poll. This supports topic relevance, not every clause about Ukraine or family policy in the benchmark explanation. The ledger field remains labelled unverified-by-extraction; this subsequent bounded check does not replace the original workbook entry.

These checks make the manuscript's categorical claim “Sources for the Serbian topics are in Serbian” unsustainable as written. The workbook includes English-language research, reporting, and survey materials. The presence of a Serbian-language title elsewhere does not establish the language of every linked document; no comprehensive source-language inventory was performed.

## Safe manuscript wording

Provenance sentence that can be inserted without claiming unperformed validation:

> The accompanying provenance ledger links each of the 80 reference perspectives to its source entry in the construction workbook. It preserves the exact reference summary and explanation, the workbook sheet and cell, the recorded source text, and both displayed URLs and hyperlink targets where these differ. All reference texts in the ledger match the evaluation dataset exactly.

Source-language replacement:

> Reference summaries and explanations were written in English. Sources cited for Serbian topics include English-language research, reporting, and survey materials; the language of the cited material was therefore not uniformly Serbian.

If author-supplied process knowledge supports translation details, the author may additionally describe which Serbian sources were translated and how. Do not infer that process from the workbook alone.

Do not describe the ledger as “fully validated,” “all links verified,” or “all source support confirmed.” The remaining source-specific actions above concern precision and support, not the existence of an 80-record mapping.

## Deliverables

- `source_provenance_ledger.csv` and `.json`: one exact, matched record per reference; no reference text changed.
- `source_urls.csv`: URLs tied to reference IDs and source cells, preserving their origins.
- `workbook_cells_exact.json`: all 344 populated/annotated cells, values, hyperlinks, comments, and fill metadata.
- `extraction_summary.json`: counts and input file hashes.
- `extract_sources.py`: read-only extractor with assertions for 80 exact summary/explanation matches, unique IDs, populated source cells, and an unchanged workbook hash.
