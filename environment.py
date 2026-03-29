import os
import json
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from models import (
    TaskID, Observation, Action, Reward,
    StepResult, EnvironmentState, UserGoalProfile
)
from graders import grade
from test_cases import TASK_INSTRUCTIONS

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("API_BASE_URL"),
)
MODEL = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")


def _call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content or ""


def _extract_goal_profile(analysis: str) -> Optional[UserGoalProfile]:
    try:
        prompt = f"""
Read this analysis and extract the goal profile as JSON.
Return ONLY valid JSON with these exact keys:
{{
  "primary_goal": "string",
  "constraints": ["string"],
  "risk_tolerance": "low or medium or high",
  "success_definition": "string",
  "time_horizon": "string",
  "domain": "business or personal or career or investment or policy"
}}

ANALYSIS:
{analysis}

Return only the JSON object. No explanation. No markdown.
"""
        raw = _call_llm(prompt)
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw.strip())
        return UserGoalProfile(**data)
    except Exception:
        return UserGoalProfile(
            primary_goal="Could not extract",
            success_definition="Unknown",
            domain="business"
        )


class DecisionSimEnv:
    def __init__(self):
        self._state: Optional[EnvironmentState] = None

    def reset(self, task_id: str, user_input: str) -> Observation:
        tid = TaskID(task_id)

        self._state = EnvironmentState(
            task_id=tid,
            current_step=1,
            max_steps=3,
            user_input=user_input,
            goal_profile=None,
            step_scores=[],
            episode_complete=False,
            total_score=None,
        )

        instructions = TASK_INSTRUCTIONS["task1_step1"].format(
            user_input=user_input
        )

        return Observation(
            task_id=tid,
            user_input=user_input,
            goal_profile=None,
            current_step=1,
            max_steps=3,
            previous_analysis=None,
            instructions=instructions,
        )

    def step(self, action: Action) -> StepResult:
        if self._state is None:
            raise ValueError("Call reset() before step()")

        s = self._state
        analysis = action.analysis
        task_id_str = s.task_id.value
        result = grade(task_id_str, analysis)

        reward = Reward(
            score=result["score"],
            breakdown=result["breakdown"],
            feedback=result["feedback"],
            total_episode_score=None,
        )

        s.step_scores.append(result["score"])

        if s.current_step == 1:
            s.goal_profile = _extract_goal_profile(analysis)

        done = False
        next_obs = None

        if s.task_id == TaskID.TASK1_AUTOPSY:
            done = True
            s.episode_complete = True
            s.total_score = result["score"]
            reward.total_episode_score = s.total_score
            next_obs = Observation(
                task_id=s.task_id,
                user_input=s.user_input,
                goal_profile=s.goal_profile,
                current_step=s.current_step,
                max_steps=s.max_steps,
                previous_analysis=analysis,
                instructions="Task 1 complete.",
            )

        elif s.task_id == TaskID.TASK2_SCENARIOS:
            done = True
            s.episode_complete = True
            s.total_score = result["score"]
            reward.total_episode_score = s.total_score
            next_obs = Observation(
                task_id=s.task_id,
                user_input=s.user_input,
                goal_profile=s.goal_profile,
                current_step=s.current_step,
                max_steps=s.max_steps,
                previous_analysis=analysis,
                instructions="Task 2 complete.",
            )

        elif s.task_id == TaskID.TASK3_SIMULATION:
            if s.current_step < s.max_steps:
                s.current_step += 1
                goal_str = (
                    s.goal_profile.model_dump_json()
                    if s.goal_profile else "Not extracted yet"
                )
                instructions = TASK_INSTRUCTIONS["task3_step1"].format(
                    user_input=s.user_input,
                    goal_profile=goal_str,
                    previous_analysis=analysis,
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
                    instructions="Task 3 complete.",
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
