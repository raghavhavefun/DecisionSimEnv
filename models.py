from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class TaskID(str, Enum):
    TASK1_AUTOPSY = "task1_autopsy"
    TASK2_SCENARIOS = "task2_scenarios"
    TASK3_SIMULATION = "task3_simulation"


class UserGoalProfile(BaseModel):
    primary_goal: str = Field(description="What the user ultimately wants")
    constraints: List[str] = Field(default=[], description="What they won't sacrifice")
    risk_tolerance: str = Field(default="medium", description="low / medium / high")
    success_definition: str = Field(description="What winning looks like for THIS person")
    time_horizon: str = Field(default="1 year", description="How far ahead they plan")
    domain: str = Field(description="business / personal / career / investment / policy")


class Observation(BaseModel):
    task_id: TaskID
    user_input: str = Field(description="The raw situation the user described")
    goal_profile: Optional[UserGoalProfile] = Field(default=None)
    current_step: int = Field(default=1)
    max_steps: int = Field(default=3)
    previous_analysis: Optional[str] = Field(default=None)
    instructions: str = Field(description="What the agent must do right now")


class Action(BaseModel):
    analysis: str = Field(description="The agent's full analysis response")
    chosen_path: Optional[str] = Field(default=None, description="Task 3 only")


class Reward(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Score for this step")
    breakdown: Dict[str, float] = Field(description="Individual criterion scores")
    feedback: str = Field(description="What was good and what was missing")
    total_episode_score: Optional[float] = Field(default=None)


class StepResult(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Any] = Field(default={})


class EnvironmentState(BaseModel):
    task_id: TaskID
    current_step: int
    max_steps: int
    user_input: str
    goal_profile: Optional[UserGoalProfile]
    step_scores: List[float] = Field(default=[])
    episode_complete: bool = Field(default=False)
    total_score: Optional[float] = Field(default=None)