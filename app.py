import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from environment import DecisionSimEnv
from models import Action

load_dotenv()

app = FastAPI(
    title="DecisionSimEnv",
    description="Universal Decision Stress-Tester — OpenEnv Environment",
    version="1.0.0",
)

env = DecisionSimEnv()


class ResetRequest(BaseModel):
    task_id: str
    user_input: str


class StepRequest(BaseModel):
    analysis: str
    chosen_path: str = None


@app.get("/")
def root():
    return {
        "name": "DecisionSimEnv",
        "version": "1.0.0",
        "description": "Universal Decision Stress-Tester",
        "tasks": [
            "task1_autopsy",
            "task2_scenarios",
            "task3_simulation"
        ],
        "status": "ready"
    }


@app.post("/reset")
def reset(req: ResetRequest):
    try:
        obs = env.reset(task_id=req.task_id, user_input=req.user_input)
        return obs.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step")
def step(req: StepRequest):
    try:
        action = Action(analysis=req.analysis, chosen_path=req.chosen_path)
        result = env.step(action)
        return {
            "observation": result.observation.model_dump(),
            "reward": result.reward.model_dump(),
            "done": result.done,
            "info": result.info,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
def state():
    try:
        s = env.state()
        return s.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
