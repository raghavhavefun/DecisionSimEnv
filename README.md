# DecisionSimEnv
### Universal Decision Stress-Tester

An OpenEnv environment where anyone — a founder, student, investor, or individual facing any decision — enters their situation in plain language and gets a full simulation of what could go wrong, all possible futures, and a clear final verdict.

---

## What It Does

Most people make major decisions with incomplete information. They launch products that already failed. They invest in flawed ideas. They take wrong career paths. Not because they are stupid — but because they never had access to proper simulation tools.

DecisionSimEnv fixes this. Enter any situation. The AI stress-tests it across three levels.

---

## The Three Tasks

**Task 1 — Idea Autopsy (Easy)**
The AI reads the situation, extracts the user's real goals and constraints, finds at least 3 specific weaknesses, names real competitors who tried something similar, explains why one of them failed, and identifies the single biggest blind spot the user is missing.

**Task 2 — Scenario Mapping (Medium)**
The AI maps 5 realistic future scenarios like Dr Strange viewing all possible futures. Each scenario has a name, a cause, a 12-month outcome, a probability estimate, and a check against the user's actual goals. All probabilities sum to 100%.

**Task 3 — Future Path Simulator (Hard)**
The AI picks the path that best matches the user's goals and simulates it month by month for 12 months. It surfaces unexpected consequences at each stage, compares all 5 paths in a table, and gives one final clear recommendation with specific actions to take this week.

---

## Who Can Use This

- Startup founders before launching a product
- Students deciding between job offers or career paths
- Investors doing due diligence before writing a cheque
- Business owners deciding whether to expand
- Individuals facing any major life decision

---

## Action Space
```json
{
  "analysis": "The agent's full text response to the current task",
  "chosen_path": "Optional — only used in Task 3 to specify which scenario to simulate"
}
```

## Observation Space
```json
{
  "task_id": "task1_autopsy or task2_scenarios or task3_simulation",
  "user_input": "The raw situation the user described",
  "goal_profile": "Extracted goals, constraints, risk tolerance, success definition",
  "current_step": "Which step of the episode we are on",
  "max_steps": "Total steps in this task",
  "previous_analysis": "Output from the previous step passed forward",
  "instructions": "Exact instructions for what the agent must do right now"
}
```

---

## Task Difficulty and Scoring

| Task | Difficulty | Max Steps | Score Range |
|------|-----------|-----------|-------------|
| task1_autopsy | Easy | 1 | 0.0 to 1.0 |
| task2_scenarios | Medium | 1 | 0.0 to 1.0 |
| task3_simulation | Hard | 3 | 0.0 to 1.0 |

Scoring is multi-criteria at every step. Partial credit is given. No binary pass/fail.

---

## Baseline Scores

Tested with llama-3.3-70b-versatile via Groq API.

| Task | Baseline Score |
|------|---------------|
| task1_autopsy | 0.96 |
| task2_scenarios | 0.10 |
| task3_simulation | 0.51 |
| Overall Average | 0.52 |

---

## Setup Instructions
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/DecisionSimEnv
cd DecisionSimEnv
pip install -r requirements.txt
```

Create a `.env` file with your keys:
```
API_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_key_here
HF_TOKEN=your_hf_token_here
```

Run locally:
```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

Run baseline inference:
```bash
python inference.py
```

---

## API Endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | / | Returns environment info and task list |
| POST | /reset | Starts a new episode with a task and user input |
| POST | /step | Agent submits analysis, gets score and next observation |
| GET | /state | Returns full current environment state |
| GET | /health | Health check — returns ok |

---

## Environment Variables Required

| Variable | Description |
|----------|-------------|
| API_BASE_URL | The LLM API endpoint |
| MODEL_NAME | The model to use for inference |
| GROQ_API_KEY | Your Groq API key |
| HF_TOKEN | Your HuggingFace token |

---

*Built for the OpenEnv Hackathon by Raghav Agarwal leveraging AI*

