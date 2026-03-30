import json
import os
from datetime import datetime

DATA_DIR = "data"
OUTPUTS_DIR = os.path.join(DATA_DIR, "outputs")
TRAINING_FILE = os.path.join(DATA_DIR, "training_data.json")

os.makedirs(OUTPUTS_DIR, exist_ok=True)


def save_run(user_input: str, task1: str, task2: str, task3: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run = {
        "id": ts,
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "task1_output": task1,
        "task2_output": task2,
        "task3_output": task3,
    }
    path = os.path.join(OUTPUTS_DIR, f"run_{ts}.json")
    with open(path, "w") as f:
        json.dump(run, f, indent=2)
    append_training(run)
    return ts


def append_training(run: dict):
    data = []
    if os.path.exists(TRAINING_FILE):
        with open(TRAINING_FILE) as f:
            data = json.load(f)
    data.append(run)
    with open(TRAINING_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_all_runs() -> list:
    runs = []
    for fname in sorted(os.listdir(OUTPUTS_DIR), reverse=True):
        if fname.endswith(".json"):
            with open(os.path.join(OUTPUTS_DIR, fname)) as f:
                runs.append(json.load(f))
    return runs[:20]


def get_test_cases() -> list:
    path = os.path.join(DATA_DIR, "test_cases.json")
    with open(path) as f:
        return json.load(f)
