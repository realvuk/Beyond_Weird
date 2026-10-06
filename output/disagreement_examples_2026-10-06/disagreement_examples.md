# BWEIRD: verified disagreement examples

The strongest framing is that judges sometimes interpreted the requirements for stance identity differently. Some cases also involve overlapping references. The generated text need not itself be unclear.

## Scope and checks

The scan covers 1,040 generated perspectives and 5,228 raw judgement rows. Resolving 28 superseded retry records leaves 5,200 panel seats: 5,184 valid decisions and 16 missing/error decisions. There are 368 perspectives with at least two distinct valid labels (176 Serbian and 192 WEIRD). Of these, 358 have five valid judges and 10 have four. These counts describe disagreement, not its semantic causes.

- Scanned every generated perspective and every raw judgement row.
- Retained the last record per generator/topic/perspective/judge, matching the repository retry semantics.
- Restricted decisions to the configured family-disjoint panel; checked generator and judge families differ.
- Excluded null decisions as missing/error judgements; retained canonical label 0 as a valid no-match decision.
- Verified presented labels map to stored canonical labels through presentation_order.
- Cross-checked all 5,184 valid labels against results/adapted/verdicts.jsonl: zero mismatches.
- Defined disagreement as more than one distinct canonical label among valid judges; missing seats do not count as disagreement.
- Selected eight illustrative examples by editorial relevance after examining candidate text, references and all five recorded reasons. This is not random sampling or a semantic classification of all disagreements.

The judging prompt requires the same underlying side and stance, rejects loose thematic overlap, and directs judges to return 0 when in doubt. See [prompt](/Users/vuk/Downloads/BWEIRD/bweird/prompts.py:109). This is study material, not an instruction to the assistant.

The prose explanations below are editorial interpretations of recorded reasons, not independent evidence of the models’ internal reasoning. The selected examples do not establish equivalence to human annotation or absence of hallucination.

## Suggested replacement

Disagreement within the family-disjoint panel sometimes concerned which reasons or conditions had to be shared for two perspectives to count as the same stance. On the UK fracking topic, one output opposed fracking because it distrusted companies and regulators to protect local residents. One judge matched it to a reference opposing fracking on environmental and seismic grounds, while four returned “no match” because the references did not capture its distrust-based rationale.

On the Serbian Jadar topic, one output supported the mine only if strict environmental standards were enforced and the entire battery supply chain was built in Serbia. Two judges matched it to the reference expressing conditional support under enforceable environmental safeguards, while three returned “no match” because that reference lacked the domestic supply-chain requirement. The recorded explanations in these cases suggest different interpretations of which commitments were essential to stance identity. These examples illustrate a source of disagreement; they do not establish how common it was or rule out other judgement errors.

## Selected examples

### 1. Opposition based on distrust versus opposition based on environmental and seismic harms

ID: `uk_fracking_distrust`. Generator: `openai/gpt-5.5`. Topic: `pair03_weird`. Generated perspective: 2.

[Generated output](/Users/vuk/Downloads/BWEIRD/data/outputs/generations.jsonl:22)

> I oppose fracking mainly because I do not trust companies or government regulators to keep local people safe.

> Even if industry says it can be done safely, I have no confidence that corners will not be cut once drilling starts. If something goes wrong with earthquakes, water, noise, or house values, it is local residents who pay the price while companies take the profit. I do not want my community used as a test site.

**Verified labels:** no match = 4, reference 2 = 1.

**Editorial interpretation:** One judge prioritised the shared opposition and safety concerns; four treated distrust and the distribution of risks as a distinct rationale absent from the references.

**Reference perspectives receiving votes (canonical IDs):**

- Reference 2 (`pair03_weird_p2`): Ban fracking permanently on environmental and seismic grounds.
  - Full text: Fracking is just bad science. It causes earthquakes, pollutes groundwater, and locks us into another decade of fossil fuels when we should be investing in offshore wind and grid storage. Britain must stay frack-free.

**All five recorded reasons:**

Numbers within the verbatim reasons refer to each judge’s independently shuffled list. The canonical label stated before each quote is the de-randomised label.

- **google/gemini-3.1-pro-preview: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:425)

  > The candidate's perspective is uniquely centered on a lack of trust in regulators and companies, emphasizing the unfair distribution of local risks versus corporate profits. None of the reference options capture this specific anti-corporate, trust-based opposition.

- **anthropic/claude-sonnet-5: canonical reference 2.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:426)

  > The candidate and option 3 both oppose fracking entirely due to fears of environmental and safety risks (earthquakes, water contamination), making them the closest match in stance despite differing emphasis on distrust versus science-based argument.

- **deepseek/deepseek-v4-pro: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:427)

  > The candidate opposes fracking due to distrust in safety and regulation, a stance not represented by any reference. The references cover pro-fracking, NIMBY, conditional support, environmental ban, and climate rejection, none of which match the candidate's specific rationale of safety distrust.

- **moonshotai/kimi-k2.6: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:428)

  > The candidate’s viewpoint centers on skepticism toward corporate and regulatory safety assurances and the unfair risk burden on local communities, which does not correspond exactly to the core stance of any reference option.

- **x-ai/grok-4.5: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:4295)

  > The candidate opposes fracking specifically from distrust that companies and regulators will protect locals from harms, with no matching reference sharing that exact distrust-based anti-fracking stance. Loose anti-fracking overlap with 1/3/4 is insufficient for identity of side and stance.

### 2. Distrust of particular actors versus rejection of all lithium mining

ID: `jadar_distrust`. Generator: `anthropic/claude-opus-4.8`. Topic: `pair03_serbian`. Generated perspective: 3.

[Generated output](/Users/vuk/Downloads/BWEIRD/data/outputs/generations.jsonl:5)

> I don't trust Rio Tinto or our government, so I oppose it as a matter of principle.

> Rio Tinto has a horrible track record abroad, blowing up sacred sites and leaving pollution behind, and our own leaders have shown they'll sign secret deals over our heads. Even if lithium mining could theoretically be safe, I don't believe these specific actors will do it honestly or protect us. This is about corruption and sovereignty as much as the environment.

**Verified labels:** no match = 3, reference 1 = 2.

**Editorial interpretation:** Two judges prioritised outright opposition to the project; three distinguished distrust of Rio Tinto and the government from a blanket rejection of lithium mining.

**Reference perspectives receiving votes (canonical IDs):**

- Reference 1 (`pair03_serbian_p1`): Block Rio Tinto's Jadar mine outright; no lithium mining in Serbia.
  - Full text: Lithium is poisonous chemistry next to our drinking water, our river, and villages. Rio Tinto has destroyed communities from Bougainville to Mongolia. We will lie on the railway tracks before they open this mine, Ne damo Jadar.

**All five recorded reasons:**

Numbers within the verbatim reasons refer to each judge’s independently shuffled list. The canonical label stated before each quote is the de-randomised label.

- **google/gemini-3.1-pro-preview: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:89)

  > The candidate opposes the mine specifically due to a lack of trust in Rio Tinto and the Serbian government (citing corruption and sovereignty), which differs from Reference 1's absolute environmental rejection of all lithium mining and Reference 4's focus on EU eco-colonialism.

- **openai/gpt-5.5: canonical reference 1.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:90)

  > The candidate is an anti-Jadar/Rio Tinto viewpoint from within Serbia, grounded in distrust of Rio Tinto and Serbian authorities. Option 1 is the only reference that shares the same outright opposition to Rio Tinto's mine, despite emphasizing environmental danger more strongly.

- **deepseek/deepseek-v4-pro: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:91)

  > The candidate opposes the Jadar mine based on distrust of Rio Tinto and the Serbian government, emphasizing corruption and sovereignty. No reference captures this exact combination: reference 2 goes further to a blanket lithium ban, reference 5 focuses on EU colonialism, and the others support or conditionally support the mine. Thus, no match.

- **moonshotai/kimi-k2.6: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:92)

  > Although the candidate shares opposition to the Jadar mine with Reference 3, its underlying stance is actor-specific distrust that leaves theoretical room for safe lithium mining, whereas Reference 3 categorically rejects all lithium mining in Serbia as poisonous; none of the references advocate the exact same side and stance.

- **x-ai/grok-4.5: canonical reference 1.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:4211)

  > The candidate's principled opposition to the mine over Rio Tinto's record, government corruption and sovereignty aligns exactly with reference 3's outright block-the-mine stance and 'Ne damo Jadar' refusal; other references either support the mine or oppose it for mismatched reasons.

### 3. Recognition for pragmatic reasons versus recognition plus apology

ID: `kosovo_recognition`. Generator: `google/gemini-3.1-pro-preview`. Topic: `pair02_serbian`. Generated perspective: 3.

[Generated output](/Users/vuk/Downloads/BWEIRD/data/outputs/generations.jsonl:35)

> Serbia must accept the reality of Kosovo's independence to secure our own economic and European future.

> We lost Kosovo decades ago due to disastrous nationalist policies, and pretending otherwise is only holding our country hostage. Refusing to recognize reality blocks our path to the European Union and isolates us from the modern world. It is time to formally recognize Kosovo, normalize relations, and focus on building a prosperous future for the citizens actually living in Serbia.

**Verified labels:** reference 4 = 2, no match = 3.

**Editorial interpretation:** Two judges prioritised the shared call for formal recognition; three required the additional moral-historical commitments and apology present in the reference.

**Reference perspectives receiving votes (canonical IDs):**

- Reference 4 (`pair02_serbian_p4`): Recognise Kosovo's independence and apologise for the crimes of the 1990s.
  - Full text: I'm Serbian and I want to be honest: Milošević and the regime committed atrocities against Albanians in 1998–99, and Kosovo Albanians have the right to self-determination just like we did from the Ottomans. Recognise Kosovo, apologise, and let both states build a European future.

**All five recorded reasons:**

Numbers within the verbatim reasons refer to each judge’s independently shuffled list. The canonical label stated before each quote is the de-randomised label.

- **openai/gpt-5.5: canonical reference 4.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:689)

  > The candidate's defining stance is that Serbia should formally recognize Kosovo and normalize relations to secure a European future. Reference 2 is the only option that also advocates Serbian recognition of Kosovo, while the others reject recognition, avoid de jure recognition, or seek force or partition.

- **anthropic/claude-sonnet-5: canonical reference 4.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:690)

  > The candidate's core stance—formally recognizing Kosovo's independence to secure Serbia's EU and economic future—aligns most closely with option 1, which also calls for recognition and a shared European future, despite option 1's additional emphasis on apology.

- **deepseek/deepseek-v4-pro: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:691)

  > The candidate perspective advocates formal recognition of Kosovo for pragmatic reasons (EU accession, economic future) without demanding an apology. None of the reference options express this exact combination: option 5 comes closest but adds a call for apology and moral reckoning, which the candidate does not do. Therefore no matching viewpoint.

- **moonshotai/kimi-k2.6: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:692)

  > The candidate presents a pragmatic, EU-oriented argument for the formal de jure recognition of Kosovo, which none of the references exactly match: option 2 stops short of formal recognition, while option 4 adds a distinct moral-historical reckoning and apology not found in the candidate.

- **x-ai/grok-4.5: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:4361)

  > Candidate uniquely demands formal/de-jure recognition on purely pragmatic EU-economic grounds from inside Serbia. No reference shares that exact stance: ref 2 adds apology/rights claims, ref 4 rejects formal recognition, and the rest are opposed or orthogonal.

### 4. Two overlapping pro-mine reference perspectives

ID: `jadar_economic_support`. Generator: `google/gemini-3.1-pro-preview`. Topic: `pair03_serbian`. Generated perspective: 2.

[Generated output](/Users/vuk/Downloads/BWEIRD/data/outputs/generations.jsonl:37)

> The lithium mine is a once-in-a-generation economic opportunity that will modernize Serbia and create thousands of jobs.

> We are sitting on one of Europe's largest lithium deposits, and developing it will bring massive foreign investment and infrastructure to our country. By partnering with global companies, we can become a central hub in the European green energy transition. Rejecting this project means choosing poverty and backwardness over progress and wealth.

**Verified labels:** reference 2 = 3, reference 5 = 2.

**Editorial interpretation:** Three judges chose economic and strategic opportunity; two chose modernisation and rejection of opposition. The explanations differ over the role of safeguards and how strongly the candidate dismisses opposition.

**Reference perspectives receiving votes (canonical IDs):**

- Reference 2 (`pair03_serbian_p2`): Open the Jadar mine; it's an economic and strategic opportunity under EU standards.
  - Full text: Europe needs lithium for the green transition, and Jadar could supply up to 17% of EU demand. With the EU's Critical Raw Materials Act now imposing real environmental standards, this is a generational opportunity for Serbian jobs, taxes, and industrialisation.
- Reference 5 (`pair03_serbian_p5`): Reject the 'green' opposition as misinformation; embrace Lithium as modernisation.
  - Full text: The opposition is hysteria fuelled by conspiracy theories, sulphuric acid rain, secret uranium mining, none of which is true. Serbia is starved of investment, and the educated diaspora won't come home without industry. Open the mine.

**All five recorded reasons:**

Numbers within the verbatim reasons refer to each judge’s independently shuffled list. The canonical label stated before each quote is the de-randomised label.

- **openai/gpt-5.5: canonical reference 2.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:725)

  > The candidate most closely matches option 4 because both present opening Jadar as a generational economic and strategic opportunity linked to jobs, industrialization, and Europe's green transition. Other options either oppose the mine, make support conditional, or emphasize a different anti-opposition misinformation frame.

- **anthropic/claude-sonnet-5: canonical reference 5.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:726)

  > The candidate’s unconditional pro-mine stance, framing rejection as choosing poverty and emphasizing investment and modernization without any mention of environmental safeguards, aligns most closely with option 1’s dismissal of opposition and unconditional call to open the mine.

- **deepseek/deepseek-v4-pro: canonical reference 5.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:727)

  > The candidate perspective unconditionally supports the lithium mine as a modernization and economic opportunity, framing rejection as backwardness. Reference 1 matches this exactly, advocating for the mine as modernization and dismissing opposition as misinformation. Other references either add conditions (2, 3) or oppose the mine (4, 5).

- **moonshotai/kimi-k2.6: canonical reference 2.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:728)

  > The candidate and reference 3 share the exact same underlying viewpoint: unconditional support for opening the Jadar mine as a transformative economic and strategic opportunity for Serbia within the European green transition, centered on jobs, investment, and national progress. While reference 5 is also pro-mine, its core stance is defined by rebutting opposition misinformation rather than the green-transition economic hub argument that defines the candidate.

- **x-ai/grok-4.5: canonical reference 2.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:4370)

  > The candidate and reference 2 both voice unconditional support from inside Serbia for opening Jadar as a once-in-a-generation economic opportunity tied to jobs, industrialization, and Europe's green transition; no other reference shares this precise side and stance.

### 5. Whether an additional condition changes the stance

ID: `jadar_supply_chain`. Generator: `google/gemini-3.1-pro-preview`. Topic: `pair03_serbian`. Generated perspective: 4.

[Generated output](/Users/vuk/Downloads/BWEIRD/data/outputs/generations.jsonl:37)

> We should allow the mine only if strict European environmental standards are enforced and the entire battery supply chain is built in Serbia.

> It is foolish to completely ignore the economic potential of our natural resources, but we cannot just export raw lithium. We must demand ironclad guarantees for environmental protection and insist that battery and EV factories are built right here. If the state can enforce these strict regulations, the project can be a win-win for our economy and society.

**Verified labels:** no match = 3, reference 3 = 2.

**Editorial interpretation:** Two judges accepted the shared conditional-support position; three treated the domestic battery and EV supply-chain requirement as essential and absent from the reference.

**Reference perspectives receiving votes (canonical IDs):**

- Reference 3 (`pair03_serbian_p3`): Conditional support, Lithium only with strict, enforceable guarantees.
  - Full text: I would accept Jadar, but only with watertight guarantees: independent environmental monitoring, full local consent, EU-grade waste handling, and a binding ban on water contamination. Without them,no. With them, let's talk.

**All five recorded reasons:**

Numbers within the verbatim reasons refer to each judge’s independently shuffled list. The canonical label stated before each quote is the de-randomised label.

- **openai/gpt-5.5: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:733)

  > No reference expresses the exact same stance because the candidate combines enforceable EU-level environmental conditions with a mandatory domestic battery and EV supply chain. Option 3 is closest on environmental conditionality but omits the candidate's central value-chain condition.

- **anthropic/claude-sonnet-5: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:734)

  > Both the candidate and option 4 take a conditional stance: acceptance of the mine only if strict, enforceable environmental (and in the candidate's case, value-chain) guarantees are met, which distinguishes them from outright rejection, unconditional support, or anti-EU framing.

- **deepseek/deepseek-v4-pro: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:735)

  > The candidate perspective is conditional support with a unique requirement that the entire battery supply chain be built in Serbia, which no reference shares. Option 3 is the closest but lacks the supply-chain condition, so it does not express the exact same side and stance.

- **moonshotai/kimi-k2.6: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:736)

  > The candidate occupies a distinct conditional-support position that couples strict environmental enforcement with a mandatory domestic battery-supply-chain requirement; no reference combines these exact elements, so none expresses the same underlying viewpoint.

- **x-ai/grok-4.5: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:4372)

  > The candidate and reference 5 share the identical underlying side and stance of conditional support for the mine solely under strict enforceable environmental protections. Minor extra emphasis on local supply chain does not change the core conditional position.

### 6. Two overlapping reference perspectives on closer EU relations

ID: `brexit_alignment`. Generator: `qwen/qwen3.7-max`. Topic: `pair08_weird`. Generated perspective: 5.

[Generated output](/Users/vuk/Downloads/BWEIRD/data/outputs/generations.jsonl:80)

> We should have left the political union but remained in the Single Market, and we must urgently align with EU rules to stop the economic self-harm of hard Brexit.

> The hard Brexit negotiated by the government has suffocated our businesses with pointless customs red tape and destroyed our export markets without delivering any real domestic benefits. We need to swallow our pride and unilaterally align with EU regulations, or better yet, rejoin the Single Market and Customs Union like Norway, to remove the friction that is currently killing our economy. We can maintain our political independence without engaging in this suicidal regulatory divergence.

**Verified labels:** reference 3 = 3, reference 4 = 2.

**Editorial interpretation:** Three judges chose the reformist-Leaver reference; two chose pragmatic realignment without rejoining. The candidate combined criticism of how Brexit was implemented with a demand for closer economic alignment.

**Reference perspectives receiving votes (canonical IDs):**

- Reference 3 (`pair08_weird_p3`): Reformist Leaver, Brexit was botched, not wrong.
  - Full text: Brexit was badly negotiated, not bad in principle. With better politicians, not Johnson, not Truss, we could have got an EFTA-style deal and kept the trade benefits. Don't rejoin, just fix it.
- Reference 4 (`pair08_weird_p4`): Pragmatic re-alignment without rejoining, the "Starmer" middle.
  - Full text: Don't rejoin, that's a referendum we don't need, but get as close to the EU as possible: customs union, single market alignment, mobility for young people. 'Closer ties' yes, 'membership' no.

**All five recorded reasons:**

Numbers within the verbatim reasons refer to each judge’s independently shuffled list. The canonical label stated before each quote is the de-randomised label.

- **google/gemini-3.1-pro-preview: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:1597)

  > The candidate explicitly states that leaving the political union was the right approach but criticizes the hard Brexit execution, perfectly matching reference 1's reformist Leaver stance advocating for an EFTA-style deal.

- **anthropic/claude-sonnet-5: canonical reference 4.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:1598)

  > The candidate's stance of remaining outside political EU membership while aligning closely with the Single Market and Customs Union to fix the economic damage of hard Brexit matches the pragmatic re-alignment (non-rejoin) position in option 5.

- **deepseek/deepseek-v4-pro: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:1599)

  > The candidate perspective advocates a Norway-style relationship (leaving the political EU but remaining in the Single Market) and criticizes the hard Brexit as botched, which aligns exactly with the reformist leaver view in option 2.

- **moonshotai/kimi-k2.6: canonical reference 4.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:1600)

  > The candidate and reference 1 share the exact same side and stance: reversing hard Brexit through deep economic re-alignment (Single Market/Customs Union) without rejoining the EU as a full member. The other options either support hard Brexit, advocate full rejoin, or defend the principle of leaving.

- **openai/gpt-5.5: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:4588)

  > The candidate's core stance is that leaving the EU political union was acceptable, but hard Brexit was a damaging mistake that should be repaired through Single Market/Customs Union or EFTA-style alignment. That matches reference 4 more precisely than a generic closer-ties position or full rejoin stance.

### 7. Pragmatic versus reluctant support in overlapping references

ID: `vucic_support`. Generator: `moonshotai/kimi-k2.6`. Topic: `pair07_serbian`. Generated perspective: 2.

[Generated output](/Users/vuk/Downloads/BWEIRD/data/outputs/generations.jsonl:93)

> Vučić is the only realistic choice to maintain stability and economic growth in a dangerous neighborhood.

> I don’t agree with everything he does, but the opposition is a chaotic collection of amateurs who would destroy the economy and drag us into conflict. He knows how to balance relations with the EU, Russia, and China without isolating us or sending our sons to die. In this region, you need a pragmatic strongman, not idealistic experiments.

**Verified labels:** reference 1 = 2, reference 3 = 3.

**Editorial interpretation:** Two judges chose pragmatic support based on economic growth and stability; three chose reluctant support based on the absence of a credible alternative and geopolitical competence.

**Reference perspectives receiving votes (canonical IDs):**

- Reference 1 (`pair07_serbian_p1`): Pragmatic pro-Vučić, economic and stability arguments.
  - Full text: Vučić is the best of a bad bunch. Under him wages doubled, foreign investment poured in, the highways got built, and Serbia stayed out of EU sanctions on Russia. He's not perfect, but the opposition is fractured and dishonest. I'll vote SNS again.
- Reference 3 (`pair07_serbian_p3`): Reluctant Vučić-supporter, no credible alternative.
  - Full text: Vučić has problems, but he's the only one who can manage the Kosovo file, the Russians, the Albanians, and the EU at the same time. The students are idealistic and the opposition is unelectable, bring me a credible alternative and we'll talk.

**All five recorded reasons:**

Numbers within the verbatim reasons refer to each judge’s independently shuffled list. The canonical label stated before each quote is the de-randomised label.

- **google/gemini-3.1-pro-preview: canonical reference 1.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:1845)

  > The candidate expresses pragmatic support for Vučić, emphasizing economic growth, stability, and the lack of a viable opposition. This perfectly aligns with reference option 2, which shares the exact same economic and stability arguments for supporting him as the most realistic choice.

- **anthropic/claude-sonnet-5: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:1846)

  > The candidate's reasoning—reluctant support due to the absence of a viable alternative and Vučić's skill in balancing relations with major powers to preserve stability—matches most closely with reference 3's 'reluctant Vučić-supporter, no credible alternative' framing.

- **deepseek/deepseek-v4-pro: canonical reference 1.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:1847)

  > The candidate's perspective aligns with reference 2's pragmatic pro-Vučić stance, both arguing that despite flaws, Vučić is the best option for stability and economic growth given the opposition's incompetence.

- **openai/gpt-5.5: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:1848)

  > The candidate most closely matches the reluctant pro-Vučić view that he is flawed but uniquely able to manage Serbia’s geopolitical pressures while the opposition is not credible. Reference 3 captures that same no-alternative and stability-centered stance.

- **x-ai/grok-4.5: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:4650)

  > The candidate is a reluctant supporter who sees Vučić as the sole realistic pragmatic strongman able to deliver stability, growth, and balanced foreign relations against a chaotic idealistic opposition, which is the same underlying side and stance as reference 3.

### 8. Indecision versus conditional support

ID: `jadar_undecided`. Generator: `google/gemma-4-31b-it`. Topic: `pair03_serbian`. Generated perspective: 4.

[Generated output](/Users/vuk/Downloads/BWEIRD/data/outputs/generations.jsonl:181)

> I am undecided because I see both the need for jobs and the risk to the environment.

> I want my children to have jobs here in Serbia instead of moving abroad, but I am terrified of what the chemicals will do to the air we breathe. I don't trust the government's promises, but I also don't trust the protesters' extremes. I just want a solution that actually protects us while bringing prosperity.

**Verified labels:** reference 3 = 2, no match = 3.

**Editorial interpretation:** Two judges interpreted the desire for jobs and environmental protection as conditional acceptance; three treated explicit indecision as distinct from commitment to conditional support.

**Reference perspectives receiving votes (canonical IDs):**

- Reference 3 (`pair03_serbian_p3`): Conditional support, Lithium only with strict, enforceable guarantees.
  - Full text: I would accept Jadar, but only with watertight guarantees: independent environmental monitoring, full local consent, EU-grade waste handling, and a binding ban on water contamination. Without them,no. With them, let's talk.

**All five recorded reasons:**

Numbers within the verbatim reasons refer to each judge’s independently shuffled list. The canonical label stated before each quote is the de-randomised label.

- **openai/gpt-5.5: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:3613)

  > The candidate is not pro- or anti-mine outright but wants jobs only if environmental safety is genuinely secured. This aligns best with the conditional-support position in option 2.

- **anthropic/claude-sonnet-5: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:3614)

  > The candidate expresses genuine, unresolved ambivalence without committing to any specific stance (reject, support, or conditional support with defined guarantees), which distinguishes it from all five more decisive reference positions.

- **deepseek/deepseek-v4-pro: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:3615)

  > The candidate is undecided, expressing ambivalence and distrust, without endorsing any specific side — even conditional support. None of the reference perspectives captures this 'torn, wanting a responsible solution' stance; all take a clear position.

- **moonshotai/kimi-k2.6: canonical reference 3.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:3616)

  > The candidate's pragmatic, undecided stance seeks prosperity only if coupled with genuine environmental protection, aligning with option 4's conditional acceptance under strict, enforceable safeguards.

- **x-ai/grok-4.5: no match.** [Raw record](/Users/vuk/Downloads/BWEIRD/data/outputs/judgments.jsonl:5092)

  > The candidate's core position is explicit indecision seeking an unspecified balanced outcome that delivers both jobs and real protection, without endorsing opening, conditional acceptance, or outright rejection. None of the five references shares this exact undecided middle stance.

## Files

- `suggested_paragraph.md`: paste-ready replacement.
- `selected_examples.json`: eight full evidence records, original judge responses, source line numbers, methods, and input hashes.
- `all_disagreements.json`: the complete 368-item disagreement catalogue with original candidate text, references, labels, reasons, and comparison notes.

No source data or manuscript files were changed.
