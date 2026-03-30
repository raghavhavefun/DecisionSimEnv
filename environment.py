import os
import json
import requests
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from models import (
    TaskID, Observation, Action, Reward,
    StepResult, EnvironmentState, UserGoalProfile,
)
from graders import grade
from test_cases import TASK_INSTRUCTIONS

load_dotenv()

try:
    from tavily import TavilyClient
    _tavily_key = os.getenv("TAVILY_API_KEY")
    tavily_client = TavilyClient(api_key=_tavily_key) if _tavily_key else None
except ImportError:
    tavily_client = None

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("API_BASE_URL"),
    timeout=120.0,
)
MODEL = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

TASK_MAX_STEPS = {
    TaskID.TASK1_AUTOPSY:    2,
    TaskID.TASK2_SCENARIOS:  2,
    TaskID.TASK3_SIMULATION: 3,
}

TASK_STEP_GRADERS = {
    TaskID.TASK1_AUTOPSY:    ["task1_autopsy",   "task1_autopsy"],
    TaskID.TASK2_SCENARIOS:  ["task2_scenarios",  "task2_scenarios"],
    TaskID.TASK3_SIMULATION: ["task3_simulation", "task3_simulation", "task3_simulation"],
}

TASK_STEP_KEYS = {
    TaskID.TASK1_AUTOPSY:    ["task1_step1", "task1_step2"],
    TaskID.TASK2_SCENARIOS:  ["task2_step1", "task2_step2"],
    TaskID.TASK3_SIMULATION: ["task3_step1", "task3_step2", "task3_step3"],
}


def _call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content or ""


def _tavily_search(query: str) -> str:
    if not tavily_client:
        return ""
    try:
        results = tavily_client.search(query=query, max_results=3)
        return "\n".join(r.get("content", "") for r in results.get("results", [])[:3])
    except Exception:
        return ""


def _news_search(query: str) -> str:
    if not NEWS_API_KEY:
        return ""
    try:
        resp = requests.get(
            "https://newsapi.org/v2/everything",
            params={"q": query, "sortBy": "relevancy", "pageSize": 3,
                    "apiKey": NEWS_API_KEY, "language": "en"},
            timeout=10,
        )
        articles = resp.json().get("articles", [])
        return "\n".join(
            f"{a.get('title', '')} — {a.get('description', '')}"
            for a in articles[:3]
        )
    except Exception:
        return ""


def _alpha_vantage_search(keyword: str) -> str:
    if not ALPHA_VANTAGE_KEY:
        return ""
    try:
        resp = requests.get(
            "https://www.alphavantage.co/query",
            params={"function": "SYMBOL_SEARCH", "keywords": keyword,
                    "apikey": ALPHA_VANTAGE_KEY},
            timeout=10,
        )
        matches = resp.json().get("bestMatches", [])[:2]
        return "\n".join(
            f"{m.get('2. name', '')} — {m.get('3. type', '')} — {m.get('4. region', '')}"
            for m in matches
        )
    except Exception:
        return ""


def _world_bank_search(indicator: str = "NY.GDP.MKTP.CD", country: str = "IN") -> str:
    try:
        resp = requests.get(
            f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}",
            params={"format": "json", "mrv": 3},
            timeout=10,
        )
        data = resp.json()
        if len(data) > 1 and data[1]:
            entries = data[1][:2]
            return "\n".join(
                f"World Bank {e.get('indicator', {}).get('value', '')}: "
                f"{e.get('value', '')} ({e.get('date', '')})"
                for e in entries if e.get("value")
            )
    except Exception:
        pass
    return ""


def _hacker_news_search(query: str) -> str:
    try:
        resp = requests.get(
            "https://hn.algolia.com/api/v1/search",
            params={"query": query, "hitsPerPage": 3, "tags": "story"},
            timeout=10,
        )
        hits = resp.json().get("hits", [])[:3]
        return "\n".join(
            f"HN: {h.get('title', '')} — points: {h.get('points', 0)}"
            for h in hits
        )
    except Exception:
        return ""


def _build_web_context(user_input: str, domain: str, task_id: str) -> str:
    parts = []

    if task_id == "task1_autopsy":
        query = user_input[:80] + " competitors failed India"
    elif task_id == "task2_scenarios":
        query = user_input[:80] + " market size probability outcomes India 2024"
    else:
        query = user_input[:80] + " results outcomes India"

    t = _tavily_search(query)
    if t:
        parts.append(f"WEB SEARCH RESULTS:\n{t}")

    n = _news_search(user_input[:60])
    if n:
        parts.append(f"RECENT NEWS:\n{n}")

    if domain in ("business", "investment"):
        av = _alpha_vantage_search(" ".join(user_input.split()[:4]))
        if av:
            parts.append(f"MARKET DATA:\n{av}")

    wb = _world_bank_search()
    if wb:
        parts.append(f"ECONOMIC DATA:\n{wb}")

    if domain in ("business", "career", "investment"):
        hn = _hacker_news_search(user_input[:50])
        if hn:
            parts.append(f"STARTUP COMMUNITY DATA:\n{hn}")

    return "\n\n".join(parts) if parts else "No external data retrieved."


def _extract_goal_profile(analysis: str) -> Optional[UserGoalProfile]:
    try:
        prompt = f"""Extract the goal profile from this analysis as JSON only.
Return ONLY this JSON with no extra text:
{{
  "primary_goal": "string",
  "constraints": ["string"],
  "risk_tolerance": "low or medium or high",
  "success_definition": "string",
  "time_horizon": "string",
  "domain": "business or personal or career or investment or policy"
}}

ANALYSIS:
{analysis}"""
        raw = _call_llm(prompt).strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return UserGoalProfile(**json.loads(raw.strip()))
    except Exception:
        return UserGoalProfile(
            primary_goal="Could not extract",
            success_definition="Unknown",
            domain="business",
        )


class DecisionSimEnv:
    def __init__(self):
        self._state: Optional[EnvironmentState] = None
        self._web_context: str = ""
        self._domain: str = "business"

    def reset(self, task_id: str, user_input: str, domain: str = "business") -> Observation:
        tid = TaskID(task_id)
        max_steps = TASK_MAX_STEPS[tid]
        self._domain = domain

        self._state = EnvironmentState(
            task_id=tid,
            current_step=1,
            max_steps=max_steps,
            user_input=user_input,
            goal_profile=None,
            step_scores=[],
            episode_complete=False,
            total_score=None,
        )

        self._web_context = _build_web_context(user_input, domain, task_id)

        instructions = self._build_instructions(
            TASK_STEP_KEYS[tid][0], user_input, None, None
        )

        return Observation(
            task_id=tid,
            user_input=user_input,
            goal_profile=None,
            current_step=1,
            max_steps=max_steps,
            previous_analysis=None,
            instructions=instructions,
        )

    def _build_instructions(self, key: str, user_input: str,
                             goal_profile, previous_analysis) -> str:
        template = TASK_INSTRUCTIONS.get(key, "")
        goal_str = goal_profile.model_dump_json() if goal_profile else "Not extracted yet"
        prev_str = str(previous_analysis) if previous_analysis is not None else "None"
        result = template
        result = result.replace("{user_input}", user_input)
        result = result.replace("{goal_profile}", goal_str)
        result = result.replace("{previous_analysis}", prev_str)
        result = result.replace("{web_context}", self._web_context)
        return result

    def step(self, action: Action) -> StepResult:
        if self._state is None:
            raise ValueError("Call reset() before step()")

        s = self._state
        analysis = action.analysis
        grader_key = TASK_STEP_GRADERS[s.task_id][s.current_step - 1]
        result = grade(grader_key, analysis)

        reward = Reward(
            score=result["score"],
            breakdown=result["breakdown"],
            feedback=result["feedback"],
            total_episode_score=None,
        )
        s.step_scores.append(result["score"])

        if s.task_id == TaskID.TASK1_AUTOPSY and s.current_step == 1:
            s.goal_profile = _extract_goal_profile(analysis)

        if s.current_step < s.max_steps:
            s.current_step += 1
            key = TASK_STEP_KEYS[s.task_id][s.current_step - 1]
            instructions = self._build_instructions(
                key, s.user_input, s.goal_profile, analysis
            )
            next_obs = Observation(
                task_id=s.task_id,
                user_input=s.user_input,
                goal_profile=s.goal_profile,
                current_step=s.current_step,
                max_steps=s.max_steps,
                previous_analysis=analysis,
                instructions=instructions,
            )
            done = False
        else:
            done = True
            s.episode_complete = True
            s.total_score = round(sum(s.step_scores) / len(s.step_scores), 2)
            reward.total_episode_score = s.total_score
            next_obs = Observation(
                task_id=s.task_id,
                user_input=s.user_input,
                goal_profile=s.goal_profile,
                current_step=s.current_step,
                max_steps=s.max_steps,
                previous_analysis=analysis,
                instructions=f"{s.task_id.value.replace('_', ' ').title()} complete.",
            )

        return StepResult(
            observation=next_obs,
            reward=reward,
            done=done,
            info={
                "step": s.current_step,
                "step_scores": s.step_scores,
                "task_id": s.task_id.value,
            },
        )

    def state(self) -> EnvironmentState:
        if self._state is None:
            raise ValueError("Call reset() first")
        return self._state
