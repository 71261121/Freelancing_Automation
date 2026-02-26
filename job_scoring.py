"""
Simple rule-based scoring for jobs.

The goal is *not* to be perfect, but to remove obvious junk and highlight
reasonable matches for manual review.
"""
from typing import Dict, List
from .utils import normalize_text, contains_any, count_matches


def score_job(
    job: Dict,
    must_have_keywords: List[str],
    nice_to_have_keywords: List[str],
    blocked_keywords: List[str],
    min_budget_usd: int = 0,
) -> Dict:
    """
    Returns job with an added 'score' and 'reasons' field.
    """
    text = f"{job.get('title', '')} {job.get('description', '')}"
    text_norm = normalize_text(text)

    score = 0
    reasons: List[str] = []

    # Hard block
    if contains_any(text_norm, blocked_keywords):
        return {**job, "score": 0, "reasons": ["blocked_keyword"]}

    # Must-have: at least 1 should be present
    must_matches = count_matches(text_norm, must_have_keywords)
    if must_matches == 0:
        return {**job, "score": 0, "reasons": ["no_must_have_keyword"]}

    score += 30 + must_matches * 5
    reasons.append(f"{must_matches} must-have keyword(s)")

    nice_matches = count_matches(text_norm, nice_to_have_keywords)
    if nice_matches:
        score += nice_matches * 3
        reasons.append(f"{nice_matches} nice-to-have keyword(s)")

    # Very rough heuristic: detect "fixed price $X"
    budget_score, budget_reason = _estimate_budget_score(text_norm, min_budget_usd)
    score += budget_score
    if budget_reason:
        reasons.append(budget_reason)

    return {**job, "score": score, "reasons": reasons}


def _estimate_budget_score(text: str, min_budget_usd: int) -> (int, str):
    """
    Very rough budget extraction: looks for patterns like '$50', '$100'.
    Not perfect, but good enough to separate $5 trash from $100+ jobs.
    """
    import re
    matches = re.findall(r"\$(\d+)", text)
    if not matches:
        return 0, ""
    amounts = [int(m) for m in matches]
    max_amt = max(amounts)
    if max_amt < min_budget_usd:
        return -20, f"budget<{min_budget_usd}"
    if max_amt >= min_budget_usd * 3:
        return 15, f"budget_high~{max_amt}"
    return 5, f"budget_ok~{max_amt}"
