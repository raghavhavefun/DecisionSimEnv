import re
import math
from typing import Dict
from math_graders import score_mathematical


# ─── TASK 1 STEP 1 — Goal extraction + Autopsy ────────────────────────────────

def score_task1_step1(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    # Goal profile extraction
    goal_score = sum([
        0.2 if "goal profile" in text else 0,
        0.2 if "primary goal" in text else 0,
        0.15 if "constraint" in text else 0,
        0.15 if "risk tolerance" in text else 0,
        0.15 if ("success definition" in text or "winning" in text) else 0,
        0.15 if "domain" in text else 0,
    ])
    breakdown["goal_extraction"] = round(min(goal_score, 1.0), 2)

    # Weaknesses
    weakness_count = len(re.findall(
        r'weakness|weak point|problem|flaw|risk|challenge|issue|gap', text
    ))
    breakdown["weaknesses_found"] = round(min(weakness_count / 4, 1.0), 2)

    # Real named examples
    real_names = len(re.findall(
        r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*|(?:byju|unacademy|vedantu|swiggy|'
        r'zomato|ola|uber|flipkart|amazon|google|meta|netflix|meesho|zepto|'
        r'blinkit|dunzo|oyo|paytm|phonepe|razorpay|zomato|nykaa|boat|'
        r'lenskart|cure\.fit|cult\.fit|urban\s*company)', analysis
    ))
    breakdown["real_examples_used"] = round(min(real_names / 3, 1.0), 2)

    # Failure analysis
    has_failure = any(w in text for w in [
        "failed", "shut down", "closed", "bankrupt", "withdrew",
        "collapsed", "couldn't scale", "burned through", "ran out"
    ])
    breakdown["failure_analysis"] = 1.0 if has_failure else 0.0

    # Blind spot
    has_blind_spot = any(phrase in text for phrase in [
        "blind spot", "missing", "overlooking", "assumption",
        "assuming", "underestimating", "overestimating", "ignoring"
    ])
    breakdown["blind_spot_identified"] = 1.0 if has_blind_spot else 0.0

    # Pros and cons table
    has_pros = "pros" in text or "pro:" in text or "advantage" in text
    has_cons = "cons" in text or "con:" in text or "disadvantage" in text or "weakness" in text
    breakdown["pros_cons_present"] = round(
        (0.5 if has_pros else 0) + (0.5 if has_cons else 0), 2
    )

    weights = {
        "goal_extraction": 0.25,
        "weaknesses_found": 0.20,
        "real_examples_used": 0.20,
        "failure_analysis": 0.15,
        "blind_spot_identified": 0.10,
        "pros_cons_present": 0.10,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    # Penalties
    if len(analysis.split()) < 150:
        total = max(0.0, total - 0.20)
    if any(p in text for p in ["it depends", "as an ai", "i cannot", "consult a professional"]):
        total = max(0.0, total - 0.15)

    math_result = score_mathematical(analysis, "task1_autopsy")
    final_score = round((total * 0.6) + (math_result["math_score"] * 0.4), 2)
    breakdown["math_score"] = math_result["math_score"]
    breakdown.update(math_result["math_breakdown"])

    feedback = []
    if breakdown["goal_extraction"] < 0.5:
        feedback.append("Goal profile incomplete.")
    if breakdown["weaknesses_found"] < 0.5:
        feedback.append("Not enough specific weaknesses.")
    if breakdown["real_examples_used"] < 0.5:
        feedback.append("Needed more real named examples.")
    if breakdown["failure_analysis"] == 0:
        feedback.append("No failure analysis found.")
    if breakdown["blind_spot_identified"] == 0:
        feedback.append("No blind spot identified.")
    if not feedback:
        feedback.append("Strong autopsy with good goal extraction and real examples.")

    return {"score": final_score, "breakdown": breakdown, "feedback": " ".join(feedback)}


# ─── TASK 1 STEP 2 — Structured pros/cons + critical question ─────────────────

def score_task1_step2(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    # Pros table quality
    pros_count = len(re.findall(
        r'pro\s*\d*\s*[:\|]|advantage\s*\d*\s*[:\|]|\|\s*pro|strength|benefit|opportunity|upside',
        text
    ))
    breakdown["pros_table"] = round(min(pros_count / 3, 1.0), 2)

    # Cons table quality
    cons_count = len(re.findall(
        r'con\s*\d*\s*[:\|]|disadvantage\s*\d*\s*[:\|]|\|\s*con|weakness|risk|challenge|downside|threat',
        text
    ))
    breakdown["cons_table"] = round(min(cons_count / 3, 1.0), 2)

    # Confidence levels mentioned
    has_confidence = any(w in text for w in [
        "high", "medium", "low", "confidence",
        "likely", "unlikely", "certain", "probable"
    ])
    breakdown["confidence_levels"] = 1.0 if has_confidence else 0.0

    # Severity scores (1-10 scale)
    has_severity = bool(re.search(
        r'\b([1-9]|10)\s*/\s*10\b|\bscale\b|\bseverity\b|\bimpact\b|\bcritical\b|\bminor\b|\bmajor\b',
        text
    ))
    breakdown["severity_scores"] = 1.0 if has_severity else 0.0

    # Biggest blind spot present
    has_blind_spot = any(phrase in text for phrase in [
        "blind spot", "biggest", "assumption", "critical", "destroys", "kills"
    ])
    breakdown["blind_spot"] = 1.0 if has_blind_spot else 0.0

    # Critical question present
    has_question = "?" in analysis and any(phrase in text for phrase in [
        "critical question", "must answer", "before", "question"
    ])
    breakdown["critical_question"] = 1.0 if has_question else 0.0

    # Real numbers still present
    number_count = len(re.findall(
        r'\b\d+(?:\.\d+)?(?:\s*%|\s*rs|\s*l\b|\s*cr\b|\s*lakhs?|\s*crores?|\s*users?|\s*months?)',
        text
    ))
    breakdown["specificity"] = round(min(number_count / 3, 1.0), 2)

    weights = {
        "pros_table": 0.20,
        "cons_table": 0.20,
        "confidence_levels": 0.10,
        "severity_scores": 0.10,
        "blind_spot": 0.15,
        "critical_question": 0.15,
        "specificity": 0.10,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    if len(analysis.split()) < 150:
        total = max(0.0, total - 0.20)

    math_result = score_mathematical(analysis, "task1_autopsy")
    final_score = round((total * 0.7) + (math_result["math_score"] * 0.3), 2)
    breakdown["math_score"] = math_result["math_score"]

    feedback = []
    if breakdown["pros_table"] < 0.5:
        feedback.append("Pros table needs more entries.")
    if breakdown["cons_table"] < 0.5:
        feedback.append("Cons table needs more entries.")
    if breakdown["critical_question"] == 0:
        feedback.append("No critical question identified.")
    if breakdown["blind_spot"] == 0:
        feedback.append("Biggest blind spot not clearly stated.")
    if not feedback:
        feedback.append("Strong structured pros/cons with clear blind spot and critical question.")

    return {"score": final_score, "breakdown": breakdown, "feedback": " ".join(feedback)}


# ─── TASK 2 STEP 1 — 6 scenarios with Bayesian probability ───────────────────

def score_task2_step1(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    # Scenario count — need exactly 6
    scenario_patterns = [
        r'scenario\s+[1-6a-f]', r'scenario\s*:', r'scenario\s*\d',
        r'^\s*\d+[\.\)]\s+\*{0,2}(?:the\s+)?\w+',
    ]
    scenario_count = 0
    for pattern in scenario_patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        scenario_count = max(scenario_count, len(matches))
    prob_blocks = len(re.findall(r'\d+\s*%', text))
    scenario_count = max(scenario_count, min(prob_blocks, 8))
    breakdown["scenario_count"] = round(min(scenario_count / 6, 1.0), 2)

    # Probabilities present and sum to 100
    prob_matches = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
    probs = [float(p) for p in prob_matches if 0 < float(p) <= 100]
    breakdown["has_probabilities"] = 1.0 if len(probs) >= 4 else 0.0
    if len(probs) >= 4:
        total_prob = sum(probs[:10])
        deviation = abs(100 - total_prob)
        breakdown["probabilities_sum"] = 1.0 if deviation <= 10 else (0.5 if deviation <= 20 else 0.0)
    else:
        breakdown["probabilities_sum"] = 0.0

    # Bayesian reasoning present
    has_bayesian = any(phrase in text for phrase in [
        "base rate", "adjusted for", "final probability", "base rate for",
        "in india", "historically", "sector average", "survival rate"
    ])
    breakdown["bayesian_reasoning"] = 1.0 if has_bayesian else 0.0

    # Elasticity present
    has_elasticity = any(phrase in text for phrase in [
        "elasticity", "fragile", "resilient", "wrong by", "changes by"
    ])
    breakdown["elasticity_present"] = 1.0 if has_elasticity else 0.0

    # Coverage — best, worst, unexpected
    has_best = any(w in text for w in ["best", "optimistic", "success", "growth", "thrive"])
    has_worst = any(w in text for w in ["worst", "failure", "collapse", "fail", "struggle"])
    has_unexpected = any(w in text for w in ["unexpected", "external", "shock", "surprise", "pivot"])
    breakdown["scenario_coverage"] = round(
        (0.4 if has_best else 0) + (0.4 if has_worst else 0) + (0.2 if has_unexpected else 0), 2
    )

    # Goal alignment checked
    has_alignment = any(phrase in text for phrase in [
        "goal alignment", "aligned", "matches", "your goal", "best fit"
    ])
    breakdown["goal_alignment"] = 1.0 if has_alignment else 0.0

    weights = {
        "scenario_count": 0.25,
        "has_probabilities": 0.15,
        "probabilities_sum": 0.15,
        "bayesian_reasoning": 0.15,
        "elasticity_present": 0.10,
        "scenario_coverage": 0.10,
        "goal_alignment": 0.10,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    if len(analysis.split()) < 150:
        total = max(0.0, total - 0.20)
    if any(p in text for p in ["it depends", "as an ai", "i cannot"]):
        total = max(0.0, total - 0.15)

    math_result = score_mathematical(analysis, "task2_scenarios")
    final_score = round((total * 0.6) + (math_result["math_score"] * 0.4), 2)
    breakdown["math_score"] = math_result["math_score"]
    breakdown.update(math_result["math_breakdown"])

    feedback = []
    if breakdown["scenario_count"] < 0.8:
        feedback.append("Need at least 6 distinct scenarios.")
    if breakdown["has_probabilities"] == 0:
        feedback.append("No probability estimates found.")
    if breakdown["probabilities_sum"] == 0:
        feedback.append("Probabilities do not sum to 100%.")
    if breakdown["bayesian_reasoning"] == 0:
        feedback.append("No Bayesian reasoning — need base rate and adjustment.")
    if breakdown["elasticity_present"] == 0:
        feedback.append("No elasticity analysis found.")
    if not feedback:
        feedback.append("Excellent scenario mapping with Bayesian probabilities and elasticity.")

    return {"score": final_score, "breakdown": breakdown, "feedback": " ".join(feedback)}


# ─── TASK 2 STEP 2 — Scenario ranking + regret minimization ──────────────────

def score_task2_step2(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    # Ranking table present
    has_ranking = any(phrase in text for phrase in [
        "ranking", "rank", "ranked", "1-10", "score", "table"
    ])
    breakdown["ranking_table"] = 1.0 if has_ranking else 0.0

    # Regret scores present
    has_regret = any(phrase in text for phrase in [
        "regret", "regret score", "max regret", "regret =",
        "worst outcome", "missed opportunity", "opportunity cost"
    ])
    breakdown["regret_scores"] = 1.0 if has_regret else 0.0

    # Reversibility mentioned
    has_reversible = any(phrase in text for phrase in [
        "reversible", "irreversible", "undo", "reverse", "reversibility",
        "can be undone", "cannot be undone", "permanent", "temporary",
        "exit", "back out", "change course"
    ])
    breakdown["reversibility"] = 1.0 if has_reversible else 0.0

    # Survival probability mentioned
    has_survival = any(phrase in text for phrase in [
        "survival", "survive", "survival probability"
    ])
    breakdown["survival_probability"] = 1.0 if has_survival else 0.0

    # Chosen scenario clearly stated
    has_chosen = any(phrase in text for phrase in [
        "chosen scenario", "task 3 will", "we will simulate", "selected", "choose"
    ])
    breakdown["chosen_scenario"] = 1.0 if has_chosen else 0.0

    # 3 reasons given for choice
    reason_count = len(re.findall(r'reason\s+\d|first\s+reason|second\s+reason|third\s+reason|\d\.\s+', text))
    breakdown["reasons_given"] = round(min(reason_count / 3, 1.0), 2)

    weights = {
        "ranking_table": 0.20,
        "regret_scores": 0.25,
        "reversibility": 0.15,
        "survival_probability": 0.15,
        "chosen_scenario": 0.15,
        "reasons_given": 0.10,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    if len(analysis.split()) < 100:
        total = max(0.0, total - 0.20)

    math_result = score_mathematical(analysis, "task2_scenarios")
    final_score = round((total * 0.7) + (math_result["math_score"] * 0.3), 2)
    breakdown["math_score"] = math_result["math_score"]

    feedback = []
    if breakdown["ranking_table"] == 0:
        feedback.append("No ranking table found.")
    if breakdown["regret_scores"] == 0:
        feedback.append("No regret scores found.")
    if breakdown["reversibility"] == 0:
        feedback.append("Reversibility not assessed.")
    if breakdown["chosen_scenario"] == 0:
        feedback.append("Chosen scenario for Task 3 not clearly stated.")
    if not feedback:
        feedback.append("Strong scenario ranking with regret minimization and clear choice.")

    return {"score": final_score, "breakdown": breakdown, "feedback": " ".join(feedback)}


# ─── TASK 3 STEP 1 — Month-by-month simulation with differential equations ────

def score_task3_step1(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    # Month by month coverage — need at least 8 unique months
    month_mentions = re.findall(r'month\s+(\d+)', text)
    unique_months = set(month_mentions)
    breakdown["timeline_simulation"] = round(min(len(unique_months) / 8, 1.0), 2)

    # Differential equation language
    has_derivative = any(phrase in text for phrase in [
        "dv/dt", "v(t)", "v0", "e^", "r(t)", "growth rate",
        "accelerating", "decelerating", "d²v", "exponential"
    ])
    breakdown["derivative_modeling"] = 1.0 if has_derivative else 0.0

    # Explicit calculations shown at months 3, 6, 9, 12
    calc_months = sum(1 for m in ["3", "6", "9", "12"] if f"month {m}" in text or f"month{m}" in text)
    breakdown["explicit_calculations"] = round(min(calc_months / 4, 1.0), 2)

    # Growth rate values stated
    has_rate = bool(re.search(r'r\s*[=(:]\s*\d+\.?\d*\s*%|r\(t\)\s*=\s*\d+\.?\d*|growth rate\s*[=:]\s*\d+', text))
    breakdown["growth_rates_stated"] = 1.0 if has_rate else 0.0

    # Elasticity and sensitivity
    has_elasticity = any(phrase in text for phrase in [
        "elasticity", "fragile", "resilient", "wrong by", "changes by", "sensitivity"
    ])
    breakdown["elasticity_check"] = 1.0 if has_elasticity else 0.0

    # Unexpected consequences
    has_unexpected = any(phrase in text for phrase in [
        "unexpected", "surprise", "risk at", "turning point", "pivot", "danger", "warning"
    ])
    breakdown["unexpected_consequences"] = 1.0 if has_unexpected else 0.0

    weights = {
        "timeline_simulation": 0.25,
        "derivative_modeling": 0.20,
        "explicit_calculations": 0.15,
        "growth_rates_stated": 0.15,
        "elasticity_check": 0.15,
        "unexpected_consequences": 0.10,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    if len(analysis.split()) < 200:
        total = max(0.0, total - 0.20)

    math_result = score_mathematical(analysis, "task3_simulation")
    final_score = round((total * 0.6) + (math_result["math_score"] * 0.4), 2)
    breakdown["math_score"] = math_result["math_score"]
    breakdown.update(math_result["math_breakdown"])

    feedback = []
    if breakdown["timeline_simulation"] < 0.6:
        feedback.append("Timeline simulation too thin — need at least 8 months covered.")
    if breakdown["derivative_modeling"] == 0:
        feedback.append("No differential equation language — need V(t), r(t), dV/dt.")
    if breakdown["explicit_calculations"] < 0.5:
        feedback.append("Missing explicit calculations at months 3, 6, 9, 12.")
    if breakdown["elasticity_check"] == 0:
        feedback.append("No elasticity or sensitivity analysis.")
    if not feedback:
        feedback.append("Excellent month-by-month simulation with derivatives and elasticity.")

    return {"score": final_score, "breakdown": breakdown, "feedback": " ".join(feedback)}


# ─── TASK 3 STEP 2 — Alignment check + gap analysis + path comparison ─────────

def score_task3_step2(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    # Alignment score stated
    has_alignment_score = bool(re.search(
        r'alignment\s+score\s*[=:]\s*\d+|alignment\s*:\s*\d+\s*/\s*10|\d+\s+out\s+of\s+10|score\s*[=:]\s*\d+\s*/\s*10|\d+/10',
        text
    ))
    breakdown["alignment_score"] = 1.0 if has_alignment_score else 0.0

    # Gap analysis present
    has_gap = any(phrase in text for phrase in [
        "gap analysis", "gap:", "difference between", "what they want", "what they get"
    ])
    breakdown["gap_analysis"] = 1.0 if has_gap else 0.0

    # Path comparison table
    has_comparison = any(phrase in text for phrase in [
        "path comparison", "comparison table", "vs", "versus",
        "scenario name", "month 12 outcome", "survival probability"
    ])
    breakdown["path_comparison"] = 1.0 if has_comparison else 0.0

    # Regret scores in comparison
    has_regret = "regret" in text
    breakdown["regret_in_comparison"] = 1.0 if has_regret else 0.0

    # ALIGNED or NOT ALIGNED verdict
    has_verdict = any(phrase in text for phrase in [
        "aligned", "not aligned", "alignment score"
    ])
    breakdown["alignment_verdict"] = 1.0 if has_verdict else 0.0

    # Specific numbers showing gaps
    number_count = len(re.findall(r'\b\d+(?:\.\d+)?(?:\s*%|\s*rs|\s*l\b|\s*cr\b)', text))
    breakdown["numerical_gaps"] = round(min(number_count / 4, 1.0), 2)

    weights = {
        "alignment_score": 0.20,
        "gap_analysis": 0.20,
        "path_comparison": 0.20,
        "regret_in_comparison": 0.15,
        "alignment_verdict": 0.15,
        "numerical_gaps": 0.10,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    if len(analysis.split()) < 150:
        total = max(0.0, total - 0.20)

    math_result = score_mathematical(analysis, "task3_simulation")
    final_score = round((total * 0.7) + (math_result["math_score"] * 0.3), 2)
    breakdown["math_score"] = math_result["math_score"]

    feedback = []
    if breakdown["alignment_score"] == 0:
        feedback.append("No alignment score stated out of 10.")
    if breakdown["gap_analysis"] == 0:
        feedback.append("No gap analysis found.")
    if breakdown["path_comparison"] == 0:
        feedback.append("No path comparison table found.")
    if breakdown["alignment_verdict"] == 0:
        feedback.append("ALIGNED or NOT ALIGNED verdict missing.")
    if not feedback:
        feedback.append("Strong alignment check with gap analysis and path comparison.")

    return {"score": final_score, "breakdown": breakdown, "feedback": " ".join(feedback)}


# ─── TASK 3 STEP 3 — Final verdict + action plan ──────────────────────────────

def score_task3_step3(analysis: str) -> Dict:
    text = analysis.lower()
    breakdown = {}

    # PROCEED / DO NOT PROCEED / PIVOT TO verdict
    has_verdict = any(phrase in text for phrase in [
        "proceed:", "do not proceed:", "pivot to:", "proceed —", "do not proceed —", "pivot to —"
    ])
    breakdown["clear_verdict"] = 1.0 if has_verdict else 0.0

    # Action plan present
    has_action = any(phrase in text for phrase in [
        "this week", "days 1-7", "month 1", "first step", "action plan"
    ])
    breakdown["action_plan"] = 1.0 if has_action else 0.0

    # Specific milestones
    milestone_count = len(re.findall(r'month\s+[136]|week\s+\d|day\s+\d', text))
    breakdown["milestones"] = round(min(milestone_count / 3, 1.0), 2)

    # 3 reasons tied to goal profile
    reason_count = len(re.findall(r'reason\s+[123]|first\s+reason|second\s+reason|third\s+reason', text))
    breakdown["three_reasons"] = round(min(reason_count / 3, 1.0), 2)

    # Specific numbers in action plan
    number_count = len(re.findall(r'\b\d+(?:\.\d+)?(?:\s*%|\s*rs|\s*l\b|\s*days?|\s*weeks?|\s*months?)', text))
    breakdown["specificity"] = round(min(number_count / 5, 1.0), 2)

    # Kill factor or critical assumption
    has_kill = any(phrase in text for phrase in [
        "will kill", "if skipped", "critical assumption", "validate before",
        "one thing", "most important"
    ])
    breakdown["kill_factor"] = 1.0 if has_kill else 0.0

    weights = {
        "clear_verdict": 0.25,
        "action_plan": 0.20,
        "milestones": 0.15,
        "three_reasons": 0.15,
        "specificity": 0.15,
        "kill_factor": 0.10,
    }
    total = sum(breakdown[k] * weights[k] for k in breakdown)

    if len(analysis.split()) < 150:
        total = max(0.0, total - 0.20)
    if any(p in text for p in ["it depends", "as an ai", "i cannot", "consult a professional"]):
        total = max(0.0, total - 0.15)

    math_result = score_mathematical(analysis, "task3_simulation")
    final_score = round((total * 0.7) + (math_result["math_score"] * 0.3), 2)
    breakdown["math_score"] = math_result["math_score"]

    feedback = []
    if breakdown["clear_verdict"] == 0:
        feedback.append("No clear PROCEED / DO NOT PROCEED / PIVOT TO verdict.")
    if breakdown["action_plan"] == 0:
        feedback.append("No specific action plan found.")
    if breakdown["three_reasons"] < 0.5:
        feedback.append("Did not give 3 specific reasons tied to goal profile.")
    if breakdown["kill_factor"] == 0:
        feedback.append("No kill factor or critical assumption identified.")
    if not feedback:
        feedback.append("Excellent final verdict with specific action plan and clear reasoning.")

    return {"score": final_score, "breakdown": breakdown, "feedback": " ".join(feedback)}


# ─── ROUTER ───────────────────────────────────────────────────────────────────

def grade(task_id: str, analysis: str) -> Dict:
    graders = {
        "task1_step1":     score_task1_step1,
        "task1_step2":     score_task1_step2,
        "task2_step1":     score_task2_step1,
        "task2_step2":     score_task2_step2,
        "task3_step1":     score_task3_step1,
        "task3_step2":     score_task3_step2,
        "task3_step3":     score_task3_step3,
        # Legacy fallbacks
        "task1_autopsy":   score_task1_step1,
        "task2_scenarios": score_task2_step1,
        "task3_simulation": score_task3_step1,
    }
    fn = graders.get(task_id)
    if fn:
        return fn(analysis)
    return {"score": 0.0, "breakdown": {}, "feedback": f"Unknown task_id: {task_id}"}