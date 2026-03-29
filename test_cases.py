TEST_CASES = [
    {
        "id": "tc1_startup",
        "user_input": (
            "I want to build an AI-powered tutoring app for students in tier 2 "
            "and 3 cities in India. Monthly subscription Rs 199. Target: 10,000 "
            "users in 6 months. Team: 2 engineers, 1 designer. No funding yet."
        ),
        "domain": "business"
    },
    {
        "id": "tc2_personal",
        "user_input": (
            "I am 24, working in Bangalore, earning Rs 12L per year. My girlfriend "
            "wants to get married but I want to move abroad for a masters degree. "
            "We have been together 3 years. I love her but this opportunity may not come again."
        ),
        "domain": "personal"
    },
    {
        "id": "tc3_expansion",
        "user_input": (
            "I run a profitable cloud kitchen in Kolkata. Revenue Rs 8L per month, "
            "profit margin 18%. I want to expand to a second city. I have Rs 25L "
            "capital saved. Options: Delhi or Hyderabad."
        ),
        "domain": "business"
    },
    {
        "id": "tc4_investment",
        "user_input": (
            "A founder is asking me for Rs 30L for 8% equity in a D2C skincare brand "
            "targeting men in India. They have Rs 4L MRR, 3 months old, no patent, "
            "team of 4. I have Rs 50L total to invest this year."
        ),
        "domain": "investment"
    },
    {
        "id": "tc5_career",
        "user_input": (
            "I am in 3rd year B.Tech CSE at a tier 2 college in Jaipur. I have a "
            "placement offer at TCS for Rs 6.5L. I also want to try for product "
            "companies or start something. I have 8 months before placement season ends."
        ),
        "domain": "career"
    }
]


TASK_INSTRUCTIONS = {

    "task1_step1": """\
You are a world-class decision analyst. Read the user's situation carefully.

Do TWO things:

PART 1 - EXTRACT THEIR GOALS:
Write a section called GOAL PROFILE with:
- Primary goal: what they truly want (not just what they said)
- Constraints: what they are NOT willing to sacrifice (list each one)
- Risk tolerance: low / medium / high
- Success definition: what does winning look like for THIS specific person
- Time horizon: how far ahead they are thinking
- Domain: business / personal / career / investment / policy

PART 2 - AUTOPSY:
Write a section called AUTOPSY FINDINGS with:
- At least 3 specific weaknesses in their plan
- Real named competitors or real people who tried something similar
- Why at least one of them failed with specific details
- Assumption check: what are they assuming that may be wrong
- The single biggest blind spot they are missing

Use real names. Use real numbers. No generic advice.

USER SITUATION:
{user_input}
""",

    "task2_step1": """\
You are running a full scenario simulation like Dr Strange viewing all possible futures.

USER SITUATION:
{user_input}

THEIR GOAL PROFILE:
{goal_profile}

WEAKNESSES ALREADY FOUND:
{previous_analysis}

Map out exactly 5 scenarios. For each one write:
- Scenario name
- What causes this scenario to happen
- What the situation looks like 12 months from now
- Probability: X% (all 5 must add up to 100%)
- Goal alignment: yes / partial / no

Your 5 scenarios must cover:
1. Best realistic case
2. Most likely case
3. Worst case
4. Unexpected external event
5. The path nobody considers but should

Be specific to THIS person only.
""",

    "task3_step1": """\
You are simulating the full future timeline and giving a final verdict.

USER SITUATION:
{user_input}

THEIR GOAL PROFILE:
{goal_profile}

ALL SCENARIOS MAPPED:
{previous_analysis}

Do THREE things:

1. TIMELINE SIMULATION:
   Pick the scenario that best matches their goals.
   Simulate month by month for 12 months.
   For each month: what happens, what decision they face, what risk appears.

2. PATH COMPARISON:
   One line per scenario:
   Scenario name | survival probability | goal alignment | biggest risk

3. FINAL VERDICT:
   One clear recommendation. Not it depends.
   Tell them: do THIS, avoid THAT, start with THIS action THIS week.
   Give 3 specific reasons tied to their goals.
"""
}