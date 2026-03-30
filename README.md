---
title: DecisionSimEnv
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: Universal Decision Stress-Tester — OpenEnv Hackathon
---

# DecisionSimEnv
## Universal Decision Stress-Tester
**OpenEnv Hackathon Submission | Raghav Agarwal**

---

## What This Is

DecisionSimEnv is an AI-powered decision simulation environment. Anyone — a student, a founder, an investor, a person facing a personal decision — enters their situation in plain language. The AI runs it through 3 tasks of increasing difficulty, finds every flaw, maps every possible future, simulates the best path month by month using real mathematics, and gives a final verdict.

Built for the OpenEnv Hackathon. Judged by Meta and Hugging Face engineers.

---

## Live Demo

https://ragarwal023-decisionsimenv.hf.space

---

## The 3 Tasks

### Task 1 — Diagnose (Easy) — 2 Steps
Step 1: The AI reads the user's situation, searches the web using Tavily and NewsAPI for real competitors and past failures, and extracts a full goal profile.
Step 2: The AI outputs a structured pros and cons analysis with real named companies, real numbers, and the single biggest blind spot.
Graded on: goal extraction, weaknesses found, real examples used, failure analysis, blind spot identified.

### Task 2 — Map Futures (Medium) — 2 Steps
Step 1: The AI generates exactly 6 named scenarios using Bayesian probability. All probabilities sum to 100%. Each scenario has a cause, month 6 and month 12 outcomes, an elasticity score, and a goal alignment rating.
Step 2: The AI ranks all 6 scenarios against the user's goal profile using a regret minimization table and selects the best fit scenario for Task 3.
Graded on: scenario count, probability quality, Shannon entropy, scenario coverage, goal alignment.

### Task 3 — Simulate (Hard) — 3 Steps
Step 1: The AI simulates the chosen scenario month by month for 12 months using the differential equation V(t) = V0 x e^(r x t) where r changes each month. Shows d²V/dt² at each stage. Runs elasticity check.
Step 2: The AI checks if the simulation outcome aligns with the user's original goal. Scores alignment out of 10. Produces gap analysis and path comparison table with regret scores.
Step 3: The AI gives a final verdict — PROCEED, DO NOT PROCEED, or PIVOT TO — with a specific week by week action plan or honest guide.
Graded on: timeline simulation, derivative modeling, elasticity analysis, path comparison, final verdict quality.

---

## Mathematics Used

| Formula | Task | What It Measures |
|---------|------|-----------------|
| P(A given B) = P(B given A) x P(A) / P(B) | Task 2 | Bayesian scenario probabilities grounded in real base rates |
| H = -sum(p x log p) | Task 2 | Shannon entropy — how well spread the scenarios are |
| dV/dt = r(t) x V(t) | Task 3 | Differential equation for month-by-month growth or decay |
| V(t) = V0 x e^(r x t) | Task 3 | Exponential simulation — value at any future month |
| d²V/dt² positive or negative | Task 3 | Is growth accelerating or decelerating |
| Elasticity = (dOutput/Output) / (dInput/Input) | Task 3 | How fragile the plan is if one assumption is wrong |
| Regret = max(all outcomes) minus outcome(i) | Task 2 and 3 | Regret minimization — which path causes least regret |

---

## APIs Used

| API | What It Gives | Key Required |
|-----|--------------|-------------|
| Tavily | Web search — real competitors, news, case studies from any domain | Yes — TAVILY_API_KEY |
| NewsAPI | Recent news on any topic — business, career, personal, policy | Yes — NEWS_API_KEY |
| Alpha Vantage | Stock and sector market data for investment and business decisions | Yes — ALPHA_VANTAGE_KEY |
| World Bank API | GDP, market size, India economic data | No key needed |
| Hacker News API | Startup community data — who failed, who succeeded and why | No key needed |

---

## Baseline Scores

| Task | Average Score |
|------|--------------|
| Task 1 — Diagnose | 0.71 |
| Task 2 — Map Futures | 0.83 |
| Task 3 — Simulate | Pending full run |

---

## The 5 Test Cases

| # | Domain | Situation Summary |
|---|--------|------------------|
| 1 | Business | AI tutoring app for tier 2 and 3 cities in India, Rs 199/month, target 10,000 users in 6 months |
| 2 | Personal | 24 years old in Bangalore, girlfriend wants marriage, wants to go abroad for masters degree |
| 3 | Business | Cloud kitchen in Kolkata, Rs 8L/month revenue, 18% margin, expanding to Delhi or Hyderabad |
| 4 | Investment | Founder asking Rs 30L for 8% equity in D2C skincare brand targeting men, Rs 4L MRR, 3 months old |
| 5 | Career | 3rd year BTech CSE tier 2 college, TCS offer Rs 6.5L, considering product companies or starting up |

---

## Project Structure
DecisionSimEnv/
├── environment.py      Main environment — reset() step() state() + all API calls
├── graders.py          Scoring logic for all 3 tasks
├── math_graders.py     Real mathematical scoring — Bayesian, Shannon entropy, derivatives, elasticity, regret
├── inference.py        Baseline inference script required by hackathon
├── models.py           Pydantic typed models — Observation, Action, Reward, EnvironmentState
├── test_cases.py       5 test cases and all 7 task step instruction prompts
├── app.py              FastAPI wrapper with all endpoints
├── storage.py          Run storage and history
├── openenv.yaml        OpenEnv spec configuration file
├── Dockerfile          Container for deployment
├── requirements.txt    Python dependencies
└── ui.html             Web interface

---

## Setup and Running Locally
```bash
git clone https://huggingface.co/spaces/ragarwal023/DecisionSimEnv
cd DecisionSimEnv
pip install -r requirements.txt
```

Create a `.env` file in the root directory:
API_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
OPENAI_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
NEWS_API_KEY=your_newsapi_key_here
ALPHA_VANTAGE_KEY=your_alpha_vantage_key_here

Start the server:
```bash
uvicorn app:app --reload
```

Run the baseline inference:
```bash
python inference.py
```

---

## Docker
```bash
docker build -t decisionsimenv .
docker run -p 7860:7860 --env-file .env decisionsimenv
```

---

## API Endpoints

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| /reset | POST | Start a new episode. Pass task_id and user_input. |
| /step | POST | Submit analysis and get score plus next instruction. Pass analysis as AUTO to let server call LLM. |
| /state | GET | Get current episode state including step number and scores so far. |
| /health | GET | Health check. Returns status ok. |
| /ui | GET | Opens the web interface. |

### Quick Example
```bash
curl -X POST https://ragarwal023-decisionsimenv.hf.space/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task1_autopsy", "user_input": "I want to build an AI tutoring app for tier 2 cities in India."}'

curl -X POST https://ragarwal023-decisionsimenv.hf.space/step \
  -H "Content-Type: application/json" \
  -d '{"analysis": "AUTO"}'
```

---

## OpenEnv Spec Compliance

| Requirement | Status |
|-------------|--------|
| Typed Pydantic models Observation Action Reward | Done |
| step() returns obs reward done info | Done |
| reset() returns initial observation | Done |
| state() returns current state | Done |
| openenv.yaml present with metadata | Done |
| Minimum 3 tasks easy medium hard | Done |
| Graders score 0.0 to 1.0 | Done |
| Meaningful partial progress signals | Done |
| inference.py in root directory | Done |
| Uses OpenAI client for all LLM calls | Done |
| Reads API_BASE_URL MODEL_NAME HF_TOKEN from env | Done |
| Dockerfile builds and runs cleanly | Done |
| Deployed to HuggingFace Spaces tagged openenv | Done |
| Inference runtime under 20 minutes | Done |
| Runs on 2 vCPU 8GB RAM no GPU | Done |

---

## Submitted By

Name: Raghav Agarwal
Email: raghav22062003ss@gmail.com
Competition: OpenEnv Hackathon Round 1
Format: Solo Warrior
Environment: DecisionSimEnv — Universal Decision Stress-Tester
