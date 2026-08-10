"""Prompt templates for the generation and judging stages.

Templates are plain functions returning chat-message lists so every call
site is fully typed and the exact prompts are versioned with the code.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from bweird.schemas import (
    GeneratedPerspective,
    GoldPerspective,
    Topic,
)

_GENERATION_USER_TEMPLATE = """\
Topic: {topic_title}

Reference population: {population}

Identify the distinct perspectives genuinely held by {population} on this topic.
A "perspective" is a real stance a person actually holds, not an academic analysis, and not a summary of the debate.

GUIDELINES
- Return five perspectives. Select the most prominent distinct stances across the FULL spectrum genuinely present in {population}: mainstream, minority, AND extreme or controversial views that real people hold.
- If fewer than five distinct stances genuinely exist, return fewer. Do not pad, and do not merge distinct stances to stay under the limit.
- SCOPE: only perspectives held by {population}. Do not write from the viewpoint of any other group.
- Each perspective takes a clear SIDE. Do not write "both sides have merit" as neutrality. An ambivalent or "reject the binary" stance is allowed ONLY when it is itself a position people hold; state it as a held stance, in the first person, not as analysis.
- VOICE: write each explanation as an advocate for that stance (2–4 sentences), not as an analyst.
- Do NOT include meta-perspectives such as "this issue is complex".

OUTPUT, raw JSON only, no markdown, no preamble:

{{"perspectives": [
  {{"summary": "<one direct sentence capturing the stance>",
   "explanation": "<2–4 sentences in the advocate's voice>"}},
  ...
]}}"""

def build_generation_messages(topic: Topic) -> list[dict[str, str]]:
    """Build the chat messages for one generation call."""
    user = _GENERATION_USER_TEMPLATE.format(
        topic_title=topic.topic_title,
        population=topic.population,
    )
    return [
        {"role": "user", "content": user},
    ]

REPAIR_INSTRUCTION = (
    "Your previous response could not be parsed as JSON. Respond again with "
    "ONLY the JSON value in the exact format requested -- no prose, no "
    "Markdown fences, no commentary."
)

def build_repair_messages(
    original_messages: Sequence[Mapping[str, str]], failed_output: str
) -> list[dict[str, str]]:
    """Build a one-shot repair conversation after a JSON parse failure.

    At temperature zero, simply re-sending the identical request would
    deterministically reproduce the same unparseable output; appending the
    failed output and a repair instruction changes the context and gives the
    model one chance to emit valid JSON.
    """
    return [
        *[dict(m) for m in original_messages],
        {"role": "assistant", "content": failed_output},
        {"role": "user", "content": REPAIR_INSTRUCTION},
    ]


JUDGE_SYSTEM_PROMPT = (
    "You are a meticulous annotation judge for a political-science study. "
    "You compare one candidate perspective against a fixed set of reference "
    "perspectives and decide which single reference, if any, expresses the "
    "same underlying side and stance. You judge side and stance identity, not wording "
    "similarity, and you never force a match where none exists."
)

_JUDGE_JSON_SCHEMA = """\
You must respond with ONLY a valid JSON object. Do not include markdown formatting (like ```json) or any preamble/commentary.
The response must adhere to this Pydantic-like schema:

class Comparison(BaseModel):
    match: bool  # Whether this reference option advocates the EXACT SAME side and stance
    note: str  # One short sentence explaining why or why not

class JudgmentResponse(BaseModel):
    attributes: list[str]  # Detailed key attributes of the candidate perspective: the core stance, whose view it is, what it advocates, and the claim it rests on
    scope_ok: bool  # True if the candidate is voiced from within the target population and on-topic
    comparisons: list[Comparison]  # Comparison results for each of the reference options, in order (from option 1 to N)
    match: int  # The 1-based number of the best-matching reference option (1 to N), or 0 if none matches or scope_ok is false
    reason: str  # One or two sentences justifying the final decision
"""

_JUDGE_USER_TEMPLATE = """\
Topic: {topic_title}
Population: {population}

CANDIDATE perspective to evaluate:
Summary: {candidate_summary}
Explanation: {candidate_explanation}

REFERENCE perspectives (numbered options):
{gold_block}

Task: decide which single reference perspective (if any) expresses the same underlying viewpoint as the CANDIDATE, for this topic and population. Work through the following reasoning chain and report it.

Output format (STRICT):
Respond with ONLY a JSON object conforming to the schema defined in the system prompt. Exactly these keys:
- "attributes": array of strings -- detailed key attributes of the candidate perspective: state the core stance, whose view it is, what it advocates, and the claim it rests on.
- "scope_ok": boolean -- true if the candidate is voiced from within {population} and on-topic. If it is voiced from outside {population} (a different standpoint), this is false.
- "comparisons": array of {n_gold} objects corresponding to reference options 1 through {n_gold} in order. Each object must have keys: "match" (boolean, true if it advocates the EXACT SAME side and stance) and "note" (string, one short sentence justifying why or why not).
- "match": integer -- the number of the single best-matching reference (1 through {n_gold}). If none matches, or if "scope_ok" is false, output 0. Loose thematic overlap is NOT a match. When in doubt, output 0.
- "reason": string -- one or two sentences justifying the final decision."""


def build_judge_messages(
    topic: Topic,
    candidate: GeneratedPerspective,
    presented_gold: Sequence[GoldPerspective],
) -> list[dict[str, str]]:
    """Build the chat messages for one judge execution.

    ``presented_gold`` must already be in its randomised presentation order:
    the option shown as number ``i + 1`` is ``presented_gold[i]``. Callers
    keep the mapping back to canonical gold IDs.
    """
    gold_block = "\n".join(
        f"{position}. Summary: {gold.summary}\n   Explanation: {gold.explanation}"
        for position, gold in enumerate(presented_gold, start=1)
    )
    user = _JUDGE_USER_TEMPLATE.format(
        topic_title=topic.topic_title,
        population=topic.population,
        candidate_summary=candidate.summary,
        candidate_explanation=candidate.explanation,
        gold_block=gold_block,
        n_gold=len(presented_gold),
    )
    system_content = f"{JUDGE_SYSTEM_PROMPT}\n\n{_JUDGE_JSON_SCHEMA}"
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user},
    ]

