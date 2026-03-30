import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from environment import DecisionSimEnv
from models import Action
from test_cases import TEST_CASES

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("API_BASE_URL"),
)
MODEL = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

TASK_IDS = [
    "task1_autopsy",
    "task2_scenarios",
    "task3_simulation",
]


def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content or ""


def run_task(task_id: str, test_case: dict) -> float:
    env = DecisionSimEnv()
    obs = env.reset(task_id=task_id, user_input=test_case["user_input"])

    print(f"\n  Running {task_id} on: {test_case['id']}")

    total_score = 0.0
    done = False
    step_count = 0
    last_result = None

    while not done and step_count < 5:
        for attempt in range(3):
            try:
                analysis = call_llm(obs.instructions)
                break
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    print(f"    Rate limited — waiting 60s (attempt {attempt + 1}/3)")
                    time.sleep(60)
                else:
                    raise
        action = Action(analysis=analysis)
        result = env.step(action)

        obs = result.observation
        done = result.done
        last_result = result
        step_count += 1

        print(f"    Step {step_count} score: {result.reward.score}")
        time.sleep(1)

    if last_result and last_result.reward.total_episode_score is not None:
        total_score = last_result.reward.total_episode_score
    elif last_result:
        total_score = last_result.reward.score

    print(f"  Final score: {total_score}")
    return total_score


def main():
    print("=" * 60)
    print("DecisionSimEnv — Baseline Inference")
    print("=" * 60)

    all_scores = {}

    for task_id in TASK_IDS:
        print(f"\nTask: {task_id}")
        print("-" * 40)
        task_scores = []

        for tc in TEST_CASES[:2]:
            try:
                score = run_task(task_id, tc)
                task_scores.append(score)
            except Exception as e:
                print(f"  Error on {tc['id']}: {e}")
                task_scores.append(0.0)

        avg = round(sum(task_scores) / len(task_scores), 2)
        all_scores[task_id] = avg
        print(f"\nAverage for {task_id}: {avg}")

    print("\n" + "=" * 60)
    print("BASELINE SCORES SUMMARY")
    print("=" * 60)
    for task_id, score in all_scores.items():
        print(f"{task_id}: {score}")
    overall = round(sum(all_scores.values()) / len(all_scores), 2)
    print(f"\nOverall average: {overall}")
    print("=" * 60)


if __name__ == "__main__":
    main()
