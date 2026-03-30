---
title: DecisionSimEnv
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: Universal Decision Stress-Tester for the OpenEnv Hackathon
---

# DecisionSimEnv
### Universal Decision Stress-Tester

An OpenEnv environment where anyone — a founder, student, investor, or individual facing any life decision — enters their situation in plain language and gets a full simulation: what could go wrong, every possible future, and one clear final verdict.

Like Dr Strange viewing 14 million futures before Infinity War — except for your actual life decisions.

---

## What It Does

Most people make major decisions with incomplete information. They launch products that already failed. They invest in flawed ideas. They take wrong career paths. Not because they are stupid — but because they never had access to proper simulation tools.

DecisionSimEnv fixes this. Enter any situation. The environment stress-tests it across three escalating tasks, each building on the last.

Works for any domain: business, personal, career, investment, policy — anything.

---

## The Three Tasks

**Task 1 — Idea Autopsy** `task1_autopsy` · Easy · 3 steps

The AI reads the situation, extracts the user's real goals and constraints into a structured goal profile, finds at least 3 specific weaknesses, names real competitors who tried something similar, explains why at least one of them failed with specific details, and identifies the single biggest blind spot the user is missing.

Scoring criteria: goal extraction · weaknesses found · real examples used · failure analysis · blind spot identified

---

**Task 2 — Scenario Mapping** `task2_scenarios` · Medium · 3 steps

The AI maps exactly 5 realistic future scenarios like Dr Strange viewing all possible futures. Each scenario has a name, a cause, a 12-month outcome, a probability estimate (all 5 sum to 100%), and a check against the user's actual goals. Covers best realistic case, most likely case, worst case, unexpected external event, and the path nobody considers but should.

Scoring criteria: scenario count · probability estimates · probabilities sum correctly · scenario coverage · goal alignment checked

---

**Task 3 — Future Path Simulator** `task3_simulation` · Hard · 3 steps

The AI picks the scenario that best matches the user's goals and simulates it month by month for 12 months. At each month: what happens, what decision they face, what risk appears. Then compares all paths in a table (survival probability · goal alignment · biggest risk). Ends with one clear recommendation — not "it depends" — with 3 specific reasons tied to the user's goals and exact first actions to take this week.

Scoring criteria: timeline simulation · unexpected consequences · path comparison · final verdict · actionable recommendation

---

## Mathematical Grading

Every score blends keyword scoring (60%) with mathematical analysis (40%):

| Math Criterion | What It Measures |
|---|---|
| Expected Value | Whether probability estimates are provided and internally consistent |
| Sensitivity Analysis | How many "what if" and dependency checks are in the analysis |
| Regret Minimization | Whether downside, irreversibility, and worst-case thinking is present |
| Specificity | Density of real numbers, named entities, and concrete figures |
| Coverage | How many dimensions are addressed: financial, emotional, strategic, risk, time, people |
| Entropy Quality | Whether scenario probabilities are well-distributed (not all weight on one outcome) |

Penalties applied before blending: −0.20 if analysis is under 150 words · −0.15 if vague phrases detected ("it depends", "consult a professional", "as an AI", etc.)

---

## Baseline Scores

Tested with `llama-3.3-70b-versatile` via Groq API.

| Task | Baseline Score |
|---|---|
| task1_autopsy | 1.00 |
| task2_scenarios | 0.93 |
| task3_simulation | 0.89 |
| **Overall Average** | **0.94** |

---

## Action Space

```json
{
  "analysis": "The agent's full text response to the current task instructions",
  "chosen_path": "Optional — only used in Task 3 to specify which scenario to simulate"
}
```

Pass `"analysis": "AUTO"` to have the server call its own LLM automatically. No API key needed from the caller.

## Observation Space

```json
{
  "task_id": "task1_autopsy | task2_scenarios | task3_simulation",
  "user_input": "The raw situation the user described",
  "goal_profile": "Extracted goals, constraints, risk tolerance, success definition",
  "current_step": "Which step of the episode (1, 2, or 3)",
  "max_steps": "Total steps in this task (3 for all tasks)",
  "previous_analysis": "Output from the previous step passed forward as context",
  "instructions": "Exact prompt the agent must respond to right now"
}
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Environment info and task list |
| POST | `/reset` | Start a new episode: `{"task_id": "...", "user_input": "..."}` |
| POST | `/step` | Submit analysis: `{"analysis": "..."}` — returns score + next observation |
| GET | `/state` | Full current environment state |
| GET | `/health` | Health check |
| GET | `/ui` | Browser UI for interactive use |
| GET | `/runs` | Last 20 saved runs |
| GET | `/test_cases` | The 5 built-in test cases |

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | API key for the LLM provider (Groq-compatible) |
| `API_BASE_URL` | LLM API base URL (e.g. `https://api.groq.com/openai/v1`) |
| `MODEL_NAME` | Model to use (default: `llama-3.3-70b-versatile`) |
| `HF_TOKEN` | HuggingFace token for Space deployment |
| `TAVILY_API_KEY` | Optional — enables real-world web search context in Task 1 |

---

## Setup

```bash
git clone https://huggingface.co/spaces/ragarwal023/DecisionSimEnv
cd DecisionSimEnv
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
API_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
HF_TOKEN=your_hf_token_here
TAVILY_API_KEY=your_tavily_key_here
```

Run locally:

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

Open the UI at `http://localhost:7860/ui`

Run baseline inference:

```bash
python inference.py
```

---

## What Makes This Environment Unique

Most decision-support benchmarks test narrow domains with rigid formats. DecisionSimEnv is domain-agnostic by design — the same three tasks work for a startup founder, a person choosing between a job offer and a masters degree, an investor evaluating a deal, or anyone facing an irreversible life decision.

The grading combines keyword heuristics with mathematical scoring (entropy, expected value, sensitivity analysis, regret minimization) so that vague, hedged, or low-specificity answers are penalised even if they contain the right keywords.

The three-task cascade forces the AI to reason progressively: extract structure → map uncertainty → simulate and commit to a verdict.

---

*Built for the OpenEnv Hackathon by Raghav Agarwal*
