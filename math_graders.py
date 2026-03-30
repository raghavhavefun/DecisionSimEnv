import re
import math
from typing import Dict, List


def extract_probabilities(text: str) -> List[float]:
    matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
    probs = [float(m) for m in matches if 0 < float(m) <= 100]
    return probs[:10]


def calculate_bayesian_score(text: str) -> float:
    """
    Real Bayesian check:
    P(outcome | conditions) = P(base rate) x P(user adjustment) x P(market factor)
    Checks if the AI named a base rate, made a user-specific adjustment,
    and produced probabilities that sum to ~100%.
    """
    text_lower = text.lower()
    score = 0.0

    has_base_rate = any(phrase in text_lower for phrase in [
        "base rate", "historically", "on average", "industry average",
        "success rate", "typically", "in india", "sector average",
        "survival rate", "failure rate",
    ])
    if has_base_rate:
        score += 0.25

    has_adjustment = any(phrase in text_lower for phrase in [
        "adjusted for", "given that", "because of", "specific to",
        "in this case", "for this person", "considering", "accounting for",
    ])
    if has_adjustment:
        score += 0.25

    probs = extract_probabilities(text)
    if len(probs) >= 4:
        total = sum(probs)
        deviation = abs(100 - total)
        if deviation <= 5:
            score += 0.35
        elif deviation <= 15:
            score += 0.20
        elif deviation <= 25:
            score += 0.10

    has_final_prob = any(phrase in text_lower for phrase in [
        "final =", "final probability", "therefore", "probability:",
        "final probability =", "adjusted probability",
    ])
    if has_final_prob:
        score += 0.15

    return round(min(score, 1.0), 2)


def calculate_shannon_entropy(text: str) -> float:
    """
    H = -sum(p_i x log(p_i)) for all scenarios i
    Normalized by max entropy = log(n).
    High entropy (close to 1.0) = scenarios are well spread = good.
    Low entropy (close to 0.0) = all probability on one scenario = bad.
    """
    probs = extract_probabilities(text)
    if len(probs) < 3:
        return 0.0
    total = sum(probs)
    if total == 0:
        return 0.0
    normalized = [p / total for p in probs]
    entropy = -sum(p * math.log(p + 1e-10) for p in normalized)
    max_entropy = math.log(len(normalized))
    return round(entropy / max_entropy if max_entropy > 0 else 0, 3)


def calculate_derivative_score(text: str) -> float:
    """
    Checks for real differential equation usage:
    dV/dt = r(t) x V(t)
    V(t) = V0 x e^(r x t)
    d²V/dt² > 0 means accelerating, < 0 means decelerating.
    """
    text_lower = text.lower()
    score = 0.0

    has_derivative_language = any(phrase in text_lower for phrase in [
        "dv/dt", "d²v", "d2v", "rate of change", "r(t)",
        "v(t)", "v0", "e^", "exponential", "accelerating", "decelerating",
        "second derivative", "compounding", "growth rate this month",
    ])
    if has_derivative_language:
        score += 0.30

    month_mentions = re.findall(r'month\s+(\d+)', text_lower)
    unique_months = set(month_mentions)
    if len(unique_months) >= 8:
        score += 0.30
    elif len(unique_months) >= 5:
        score += 0.20
    elif len(unique_months) >= 3:
        score += 0.10

    has_rate_values = bool(re.search(
        r'r\s*[=(:]\s*\d+\.?\d*\s*%|'
        r'r\(t\)\s*=\s*\d+\.?\d*|'
        r'growth\s+rate\s*[=:]\s*\d+\.?\d*\s*%',
        text_lower
    ))
    if has_rate_values:
        score += 0.25

    has_acceleration_signal = any(phrase in text_lower for phrase in [
        "accelerat", "decele", "slowing down", "speeding up",
        "positive", "negative", "d²v/dt²", "second derivative",
    ])
    if has_acceleration_signal:
        score += 0.15

    return round(min(score, 1.0), 2)


def calculate_elasticity_score(text: str) -> float:
    """
    Elasticity = (dOutput / Output) / (dInput / Input)
    Checks if the AI showed: if assumption X changes by Y%,
    outcome changes by Z%. And whether it labeled the plan
    fragile (elasticity > 1) or resilient (elasticity < 1).
    """
    text_lower = text.lower()
    score = 0.0

    has_elasticity_pattern = bool(re.search(
        r'wrong\s+by\s+\d+\s*%|'
        r'changes?\s+by\s+\d+\s*%.*?outcome|'
        r'outcome.*?changes?\s+by\s+\d+\s*%|'
        r'elasticity\s*[=:><!]',
        text_lower
    ))
    if has_elasticity_pattern:
        score += 0.40

    has_fragile_resilient = any(phrase in text_lower for phrase in [
        "fragile", "resilient", "highly sensitive", "not sensitive",
        "elasticity > 1", "elasticity < 1", "robust to", "sensitive to",
    ])
    if has_fragile_resilient:
        score += 0.35

    has_critical_assumption = any(phrase in text_lower for phrase in [
        "critical assumption", "key assumption", "most sensitive",
        "single most important", "validate before", "test before spending",
    ])
    if has_critical_assumption:
        score += 0.25

    return round(min(score, 1.0), 2)


def calculate_regret_score(text: str) -> float:
    """
    Regret minimization: Regret(scenario) = max(all outcomes) - outcome(this scenario)
    The best path = path with minimum maximum regret.
    Checks if the AI used regret scores, irreversibility analysis,
    and worst-case framing.
    """
    text_lower = text.lower()
    score = 0.0

    has_regret = any(phrase in text_lower for phrase in [
        "regret score", "max regret", "minimum regret",
        "regret minimization", "regret =", "regret:",
    ])
    if has_regret:
        score += 0.35

    has_irreversible = any(phrase in text_lower for phrase in [
        "irreversible", "cannot undo", "point of no return",
        "reversible", "reversibility", "can be undone", "can you undo",
    ])
    if has_irreversible:
        score += 0.30

    has_worst_case = any(phrase in text_lower for phrase in [
        "worst case", "downside", "maximum loss",
        "floor", "minimum outcome", "if everything goes wrong",
    ])
    if has_worst_case:
        score += 0.20

    has_comparison = any(phrase in text_lower for phrase in [
        "compared to", "versus", "better than", "worse than",
        "relative to", "higher regret", "lower regret",
    ])
    if has_comparison:
        score += 0.15

    return round(min(score, 1.0), 2)


def calculate_specificity_score(text: str) -> float:
    number_count = len(re.findall(
        r'\b\d+(?:\.\d+)?(?:\s*%|\s*rs|\s*₹|\s*months?|\s*weeks?'
        r'|\s*years?|\s*days?|\s*users?|\s*lakhs?|\s*crores?'
        r'|\s*k\b|\s*million|\s*billion)|\brs\s*[\d,]+|₹\s*[\d,]+',
        text.lower()
    ))
    named_entities = len(re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', text))
    return round((min(number_count / 8, 1.0) * 0.6) + (min(named_entities / 6, 1.0) * 0.4), 2)


def calculate_coverage_score(text: str) -> float:
    dimensions = {
        "financial": ["money", "cost", "revenue", "profit", "salary", "investment",
                      "capital", "rs ", "lakh", "crore", "budget", "spend", "earn"],
        "emotional": ["feel", "stress", "anxiety", "fear", "love", "regret",
                      "confidence", "motivation", "passion", "burnout"],
        "strategic": ["plan", "goal", "objective", "strategy", "long term",
                      "vision", "priority", "direction", "milestone"],
        "risk": ["risk", "danger", "threat", "downside", "worst case",
                 "failure", "lose", "fragile", "vulnerable"],
        "time": ["month", "year", "week", "deadline", "timeline",
                 "phase", "stage", "duration", "horizon"],
        "people": ["team", "partner", "family", "friend", "colleague",
                   "mentor", "investor", "customer", "relationship"],
    }
    text_lower = text.lower()
    covered = sum(
        1 for words in dimensions.values()
        if any(w in text_lower for w in words)
    )
    return round(covered / len(dimensions), 2)


def score_mathematical(analysis: str, task_id: str) -> Dict:
    scores = {
        "bayesian_probability": calculate_bayesian_score(analysis),
        "shannon_entropy":      calculate_shannon_entropy(analysis),
        "derivative_modeling":  calculate_derivative_score(analysis),
        "elasticity_analysis":  calculate_elasticity_score(analysis),
        "regret_minimization":  calculate_regret_score(analysis),
        "specificity":          calculate_specificity_score(analysis),
        "coverage":             calculate_coverage_score(analysis),
    }

    if task_id == "task1_autopsy":
        weights = {
            "bayesian_probability": 0.05,
            "shannon_entropy":      0.05,
            "derivative_modeling":  0.05,
            "elasticity_analysis":  0.10,
            "regret_minimization":  0.15,
            "specificity":          0.35,
            "coverage":             0.25,
        }
    elif task_id == "task2_scenarios":
        weights = {
            "bayesian_probability": 0.30,
            "shannon_entropy":      0.25,
            "derivative_modeling":  0.05,
            "elasticity_analysis":  0.15,
            "regret_minimization":  0.15,
            "specificity":          0.05,
            "coverage":             0.05,
        }
    else:  # task3_simulation
        weights = {
            "bayesian_probability": 0.05,
            "shannon_entropy":      0.05,
            "derivative_modeling":  0.35,
            "elasticity_analysis":  0.25,
            "regret_minimization":  0.20,
            "specificity":          0.05,
            "coverage":             0.05,
        }

    total = sum(scores[k] * weights[k] for k in weights)

    return {
        "math_score": round(total, 2),
        "math_breakdown": scores,
    }
