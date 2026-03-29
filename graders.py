import re
from typing import Dict


def score_task1(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    has_goal_profile = "goal profile" in text
    has_primary_goal = "primary goal" in text
    has_constraints = "constraint" in text
    has_risk = "risk tolerance" in text
    has_success = "success definition" in text or "winning" in text
    has_domain = "domain" in text
    goal_score = sum([
        0.2 if has_goal_profile else 0,
        0.2 if has_primary_goal else 0,
        0.15 if has_constraints else 0,
        0.15 if has_risk else 0,
        0.15 if has_success else 0,
        0.15 if has_domain else 0,
    ])
    breakdown["goal_extraction"] = round(min(goal_score, 1.0), 2)

    has_autopsy = "autopsy" in text
    weakness_count = len(re.findall(
        r'weakness|weak point|problem|flaw|risk|challenge|issue|gap', text
    ))
    weakness_score = min(weakness_count / 3, 1.0)
    breakdown["weaknesses_found"] = round(weakness_score, 2)

    real_names = len(re.findall(
        r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*|(?:byju|unacademy|vedantu|swiggy|'
        r'zomato|ola|uber|flipkart|amazon|google|meta|netflix|cult\.fit|'
        r'lenskart|meesho|zepto|blinkit|dunzo)', analysis
    ))
    name_score = min(real_names / 2, 1.0)
    breakdown["real_examples_used"] = round(name_score, 2)

    has_failure_reason = any(word in text for word in [
        "failed", "shut down", "closed", "bankrupt",
        "couldn't", "unable", "collapsed", "withdrew"
    ])
    breakdown["failure_analysis"] = 1.0 if has_failure_reason else 0.0

    has_blind_spot = any(phrase in text for phrase in [
        "blind spot", "missing", "overlooking", "assumption",
        "assuming", "underestimating", "overestimating"
    ])
    breakdown["blind_spot_identified"] = 1.0 if has_blind_spot else 0.0

    weights = {
        "goal_extraction": 0.30,
        "weaknesses_found": 0.25,
        "real_examples_used": 0.20,
        "failure_analysis": 0.15,
        "blind_spot_identified": 0.10,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    feedback_parts = []
    if breakdown["goal_extraction"] < 0.5:
        feedback_parts.append("Goal profile was incomplete — missing key fields.")
    if breakdown["weaknesses_found"] < 0.5:
        feedback_parts.append("Not enough specific weaknesses identified.")
    if breakdown["real_examples_used"] < 0.5:
        feedback_parts.append("Needed more real named examples and competitors.")
    if breakdown["failure_analysis"] == 0:
        feedback_parts.append("Did not explain why a competitor or similar attempt failed.")
    if breakdown["blind_spot_identified"] == 0:
        feedback_parts.append("Did not identify a key blind spot or wrong assumption.")
    if not feedback_parts:
        feedback_parts.append("Strong autopsy with good goal extraction and real examples.")

    return {
        "score": round(total, 2),
        "breakdown": breakdown,
        "feedback": " ".join(feedback_parts)
    }


def score_task2(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    scenario_count = len(re.findall(
        r'scenario\s+[a-e]|scenario\s+\d|scenario:', text
    ))
    breakdown["scenario_count"] = round(min(scenario_count / 5, 1.0), 2)

    probability_matches = re.findall(r'\d+\s*%', text)
    has_probabilities = len(probability_matches) >= 3
    breakdown["has_probabilities"] = 1.0 if has_probabilities else 0.0

    if has_probabilities:
        numbers = [int(re.search(r'\d+', p).group()) for p in probability_matches]
        total_prob = sum(numbers)
        prob_sum_ok = 90 <= total_prob <= 110
    else:
        prob_sum_ok = False
    breakdown["probabilities_sum_correctly"] = 1.0 if prob_sum_ok else 0.0

    has_best = any(w in text for w in ["best case", "optimistic", "best realistic"])
    has_worst = any(w in text for w in ["worst case", "pessimistic", "failure"])
    has_unexpected = any(w in text for w in [
        "unexpected", "external", "nobody", "surprise", "shock"
    ])
    coverage_score = sum([
        0.4 if has_best else 0,
        0.4 if has_worst else 0,
        0.2 if has_unexpected else 0,
    ])
    breakdown["scenario_coverage"] = round(coverage_score, 2)

    has_alignment = "goal alignment" in text or "aligned" in text
    breakdown["goal_alignment_checked"] = 1.0 if has_alignment else 0.0

    weights = {
        "scenario_count": 0.30,
        "has_probabilities": 0.20,
        "probabilities_sum_correctly": 0.15,
        "scenario_coverage": 0.25,
        "goal_alignment_checked": 0.10,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    feedback_parts = []
    if breakdown["scenario_count"] < 0.6:
        feedback_parts.append("Fewer than 3 scenarios detected — needed at least 5.")
    if breakdown["has_probabilities"] == 0:
        feedback_parts.append("No probability estimates found.")
    if breakdown["probabilities_sum_correctly"] == 0:
        feedback_parts.append("Probabilities do not sum to approximately 100%.")
    if breakdown["scenario_coverage"] < 0.8:
        feedback_parts.append("Did not cover both best case and worst case scenarios.")
    if breakdown["goal_alignment_checked"] == 0:
        feedback_parts.append("Did not check if scenarios align with user goals.")
    if not feedback_parts:
        feedback_parts.append("Excellent scenario mapping with good coverage and probabilities.")

    return {
        "score": round(total, 2),
        "breakdown": breakdown,
        "feedback": " ".join(feedback_parts)
    }


def score_task3(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    month_mentions = len(re.findall(r'month\s+\d+|\bmonth\b', text))
    timeline_score = min(month_mentions / 6, 1.0)
    breakdown["timeline_simulation"] = round(timeline_score, 2)

    has_unexpected_consequences = any(phrase in text for phrase in [
        "unexpected", "surprise", "risk at", "critical month",
        "turning point", "pivot", "danger", "warning"
    ])
    breakdown["unexpected_consequences"] = 1.0 if has_unexpected_consequences else 0.0

    has_comparison = any(phrase in text for phrase in [
        "comparison", "compare", "vs", "versus",
        "path a", "path b", "survival probability"
    ])
    breakdown["path_comparison"] = 1.0 if has_comparison else 0.0

    has_verdict = any(phrase in text for phrase in [
        "final verdict", "recommendation", "my recommendation",
        "you should", "i recommend", "verdict"
    ])
    breakdown["has_final_verdict"] = 1.0 if has_verdict else 0.0

    has_specific_action = any(phrase in text for phrase in [
        "this week", "start with", "first step", "immediately",
        "right now", "today", "next 7 days", "next 30 days"
    ])
    breakdown["actionable_recommendation"] = 1.0 if has_specific_action else 0.0

    weights = {
        "timeline_simulation": 0.25,
        "unexpected_consequences": 0.20,
        "path_comparison": 0.20,
        "has_final_verdict": 0.20,
        "actionable_recommendation": 0.15,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    feedback_parts = []
    if breakdown["timeline_simulation"] < 0.5:
        feedback_parts.append("Timeline simulation was too thin — needed month by month detail.")
    if breakdown["unexpected_consequences"] == 0:
        feedback_parts.append("Did not surface unexpected consequences at specific stages.")
    if breakdown["path_comparison"] == 0:
        feedback_parts.append("Did not compare all paths against each other.")
    if breakdown["has_final_verdict"] == 0:
        feedback_parts.append("No clear final verdict or recommendation given.")
    if breakdown["actionable_recommendation"] == 0:
        feedback_parts.append("Recommendation was not actionable — needed specific first steps.")
    if not feedback_parts:
        feedback_parts.append("Excellent simulation with strong verdict and actionable steps.")

    return {
        "score": round(total, 2),
        "breakdown": breakdown,
        "feedback": " ".join(feedback_parts)
    }


def grade(task_id: str, analysis: str) -> Dict:
    if task_id == "task1_autopsy":
        return score_task1(analysis)
    elif task_id == "task2_scenarios":
        return score_task2(analysis)
    elif task_id == "task3_simulation":
        return score_task3(analysis)
    else:
        return {
            "score": 0.0,
            "breakdown": {},
            "feedback": f"Unknown task_id: {task_id}"
        }
