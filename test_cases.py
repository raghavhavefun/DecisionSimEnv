TEST_CASES = [
    {
        "id": "tc1_startup",
        "user_input": "I want to build an AI-powered tutoring app for students in tier 2 and 3 cities in India. Monthly subscription Rs 199. Target: 10,000 users in 6 months. Team: 2 engineers, 1 designer. No funding yet.",
        "domain": "business",
    },
    {
        "id": "tc2_personal",
        "user_input": "I am 24, working in Bangalore, earning Rs 12L per year. My girlfriend wants to get married but I want to move abroad for a masters degree. We have been together 3 years. I love her but this opportunity may not come again.",
        "domain": "personal",
    },
    {
        "id": "tc3_expansion",
        "user_input": "I run a profitable cloud kitchen in Kolkata. Revenue Rs 8L per month, profit margin 18%. I want to expand to a second city. I have Rs 25L capital saved. Options: Delhi or Hyderabad.",
        "domain": "business",
    },
    {
        "id": "tc4_investment",
        "user_input": "A founder is asking me for Rs 30L for 8% equity in a D2C skincare brand targeting men in India. They have Rs 4L MRR, 3 months old, no patent, team of 4. I have Rs 50L total to invest this year.",
        "domain": "investment",
    },
    {
        "id": "tc5_career",
        "user_input": "I am in 3rd year B.Tech CSE at a tier 2 college in Jaipur. I have a placement offer at TCS for Rs 6.5L. I also want to try for product companies or start something. I have 8 months before placement season ends.",
        "domain": "career",
    },
]

TASK_INSTRUCTIONS = {

    "task1_step1": """
You are a world-class decision analyst with access to real market data.

Read the user's situation carefully. Do TWO things:

PART 1 — GOAL PROFILE:
Write a section called GOAL PROFILE:
- Primary goal: what they truly want (not just what they said)
- Constraints: what they will NOT sacrifice — list each one separately
- Risk tolerance: low / medium / high — explain why based on their situation
- Success definition: what does winning look like for THIS specific person
- Time horizon: exactly how far ahead they are planning
- Domain: business / personal / career / investment / policy

PART 2 — AUTOPSY FINDINGS:
Write a section called AUTOPSY FINDINGS:
- At least 4 specific weaknesses — each must have a real number attached
- Name at least 3 real companies or real people who tried something similar to this
- For at least 2 of them: explain exactly why they failed with specific details and numbers
- Assumption check: list every assumption they are making that could be wrong
- The single biggest blind spot: the one thing that will kill this if not addressed
- Pros table: at least 4 pros, each with a specific reason and number
- Cons table: at least 4 cons, each with a specific reason and number

Use the web search data below. Use real names. Use real numbers. No generic advice.

USER SITUATION:
{user_input}

REAL WORLD DATA FROM SEARCH:
{web_context}
""",

    "task1_step2": """
You are completing the diagnosis started in the previous step.

USER SITUATION:
{user_input}

GOAL PROFILE AND AUTOPSY FROM STEP 1:
{previous_analysis}

Now do this:

STRUCTURED PROS AND CONS:
Using everything found in step 1, write a clean final table:

PROS (at least 4):
For each pro: what it is | why it matters for THIS person | confidence level (high/medium/low)

CONS (at least 4):
For each con: what it is | how bad it is on a scale of 1-10 | can it be fixed? yes/no

BIGGEST BLIND SPOT:
The single assumption that if wrong, destroys everything. State it in one sentence.

CRITICAL QUESTION:
The one question this person must answer before spending a single rupee or making any move.
This question must be specific to their situation — not generic.
""",

    "task2_step1": """
You are mapping all possible futures using Bayesian probability.

USER SITUATION:
{user_input}

GOAL PROFILE AND DIAGNOSIS FROM TASK 1:
{previous_analysis}

REAL WORLD MARKET DATA:
{web_context}

Generate exactly 6 named scenarios. For each scenario write:

SCENARIO [number]: [creative specific name]
- Cause: what specific combination of events makes this happen
- Month 6: what the situation looks like with specific numbers
- Month 12: what the situation looks like with specific numbers
- Probability calculation:
  Base rate for this type of decision in India = X%
  Adjusted for this person's specific constraints = Y%
  Final probability = Z%
- Elasticity: if the key assumption in this scenario is wrong by 20%, the outcome changes by approximately __%
  If elasticity > 1.0 this scenario is FRAGILE. If < 1.0 it is RESILIENT.
- Goal alignment: yes / partial / no — explain why in one sentence

Rules:
- All 6 probabilities must sum to exactly 100%
- Scenario types must cover: best realistic case, most likely case, worst case, unexpected external shock, pivot nobody considered, slow failure path
- Every number must be specific to this person — not generic

After all 6 scenarios write:
BEST FIT SCENARIO: [name] — because it matches [specific goal from their goal profile] with [specific reasoning]
""",

    "task2_step2": """
You have mapped 6 scenarios. Now rank them and choose one for simulation.

USER SITUATION:
{user_input}

GOAL PROFILE:
{goal_profile}

ALL 6 SCENARIOS FROM STEP 1:
{previous_analysis}

SCENARIO RANKING TABLE:
For each of the 6 scenarios, one row:
Scenario name | Goal alignment (1-10) | Survival probability | Reversibility (can you undo this path?) | Regret score (1-10 — how bad would you feel if this goes wrong?)

Regret score formula: Regret = max(all outcomes) minus outcome of this scenario. Higher = more regret.

CHOSEN SCENARIO FOR TASK 3:
State which scenario Task 3 will simulate.
Give 3 specific reasons why this scenario fits this person's goal profile better than the others.
""",

    "task3_step1": """
You are simulating the future month by month using differential equations.

USER SITUATION:
{user_input}

CHOSEN SCENARIO FROM TASK 2:
{previous_analysis}

GOAL PROFILE:
{goal_profile}

TIMELINE SIMULATION — 12 MONTHS:

Use this mathematical model:
V(t) = V0 x e^(r x t)
where V = the key metric (users / revenue / savings / whatever fits this situation)
where r(t) = growth rate that changes each month based on events
where t = month number

For each month write:
Month [N]:
- Event: what specifically happens this month
- V(t): calculate the key metric value using V0 x e^(r x t)
- r(t) = __% this month
- d\u00b2V/dt\u00b2: is growth accelerating (positive) or decelerating (negative)? State which.
- Risk: what could go wrong this month specifically
- Required action: what must be done before month [N+1]

Show the full calculation explicitly at month 3, month 6, month 9, and month 12.

SENSITIVITY ANALYSIS:
State the single most critical assumption in this entire simulation.
If that assumption is wrong by 20%: the outcome at month 12 changes by approximately __%
Elasticity = (% change in outcome) / (% change in assumption) = __
If elasticity > 1.0: this plan is FRAGILE. If < 1.0: this plan is RESILIENT.
""",

    "task3_step2": """
You are checking if the simulated future actually delivers what the user wants.

USER SITUATION:
{user_input}

GOAL PROFILE:
{goal_profile}

MONTH BY MONTH SIMULATION FROM STEP 1:
{previous_analysis}

ALIGNMENT CHECK:
- What did the user say they wanted? Quote their exact words from the situation.
- What does the simulation show they will actually have at month 12? State specific numbers.
- Alignment score: __ out of 10
- For each point lost from 10: explain exactly what is misaligned

GAP ANALYSIS:
What is different between what they want and what the simulation delivers?
List each gap with a specific number showing the difference.

PATH COMPARISON TABLE:
One row per scenario from Task 2:
Scenario name | Month 12 outcome (specific) | Survival probability | Goal alignment score | Max regret score

VERDICT ON ALIGNMENT:
If alignment score is 7 or above: write ALIGNED — proceed to final action plan
If alignment score is below 7: write NOT ALIGNED — state which scenario from Task 2 would score higher and why
""",

    "task3_step3": """
You are giving the final verdict and complete action plan.

USER SITUATION:
{user_input}

GOAL PROFILE:
{goal_profile}

FULL SIMULATION AND ALIGNMENT RESULTS:
{previous_analysis}

FINAL VERDICT:
Start with exactly one of these three:
PROCEED: [one sentence saying what to proceed with and why]
DO NOT PROCEED: [one sentence saying what to avoid and why]
PIVOT TO: [one sentence naming the better path and why]

IF ALIGNED — FINE-TUNED ACTION PLAN:
- This week (days 1-7): exactly what to do, no vague actions
- Month 1: the one thing that must be achieved and how to measure it
- Month 3: first major milestone — what number confirms you are on track
- Month 6: decision checkpoint — what number tells you to continue or stop
- The one action that will kill this if skipped: [specific]
- The one assumption to validate before spending any money: [specific test with specific target number]

IF NOT ALIGNED — HONEST GUIDE:
- Exactly why this path does not deliver what they want (with numbers)
- Which of the 6 scenarios actually fits their true goal
- What they need to change about their plan or accept about their goal
- The minimum viable version of this idea that could actually work

3 REASONS FOR THIS RECOMMENDATION:
Each reason must reference something specific from their goal profile.
Reason 1: [tied to their primary goal]
Reason 2: [tied to their constraints]
Reason 3: [tied to their success definition]
""",
}
