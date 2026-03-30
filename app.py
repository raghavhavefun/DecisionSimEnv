import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from environment import DecisionSimEnv, _call_llm
from models import Action
from storage import save_run, get_all_runs, get_test_cases
from test_cases import TASK_INSTRUCTIONS

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
async def step(req: StepRequest):
    try:
        analysis = req.analysis
        if analysis == "AUTO":
            s = env._state
            if s is None:
                raise HTTPException(status_code=400, detail="Call reset first")

            step_key_map = {
                ("task1_autopsy",    1): "task1_step1",
                ("task1_autopsy",    2): "task1_step2",
                ("task2_scenarios",  1): "task2_step1",
                ("task2_scenarios",  2): "task2_step2",
                ("task3_simulation", 1): "task3_step1",
                ("task3_simulation", 2): "task3_step2",
                ("task3_simulation", 3): "task3_step3",
            }

            key = step_key_map.get((s.task_id.value, s.current_step))
            if not key:
                raise HTTPException(status_code=400, detail="Unknown task/step combination")

            instructions = env._build_instructions(
                key, s.user_input, s.goal_profile,
                s.step_scores[-1] if s.step_scores else None,
            )
            analysis = await asyncio.to_thread(_call_llm, instructions)

        action = Action(analysis=analysis, chosen_path=req.chosen_path)
        result = await asyncio.to_thread(env.step, action)
        return {
            "observation": result.observation.model_dump(),
            "reward": result.reward.model_dump(),
            "done": result.done,
            "info": result.info,
            "analysis": analysis,
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


@app.get("/ui")
def serve_ui():
    return FileResponse("ui.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/save_run")
def save_run_endpoint(data: dict):
    ts = save_run(
        data["user_input"],
        data.get("task1", ""),
        data.get("task2", ""),
        data.get("task3", ""),
    )
    return {"saved": True, "id": ts}


@app.get("/runs")
def get_runs():
    return get_all_runs()


@app.get("/test_cases")
def list_test_cases():
    return get_test_cases()
