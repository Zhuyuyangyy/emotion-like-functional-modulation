import sys
import os
import json
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from experiments.llm_baseline.llm_safety_judge_baseline import (
    LLMSafetyJudgeBaseline,
    DryRunLLMJudge,
)
from experiments.semireal.semireal_adapters import convert_semireal_case

BENCHMARK_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', 'benchmark', 'semireal', 'affective_agent_safety_300.json'
)
RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), '..', 'results', 'llm_baseline'
)


def load_benchmark(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def run_dry_run(cases):
    judge = DryRunLLMJudge()
    predictions = []
    for i, case in enumerate(cases):
        pred = judge.predict(case)
        pred["case_id"] = case.get("case_id", f"case_{i}")
        predictions.append(pred)
    return predictions


def run_real_llm(cases, api_key, model_name="gpt-4", base_url=None):
    judge = LLMSafetyJudgeBaseline(
        model_name=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=0,
    )
    predictions = []
    for i, case in enumerate(cases):
        pred = judge.predict(case)
        pred["case_id"] = case.get("case_id", f"case_{i}")
        predictions.append(pred)
    return predictions


def main():
    benchmark_path = os.environ.get("BENCHMARK_PATH", BENCHMARK_PATH)
    results_dir = os.environ.get("RESULTS_DIR", RESULTS_DIR)

    print(f"Loading benchmark: {benchmark_path}")
    cases = load_benchmark(benchmark_path)
    print(f"Loaded {len(cases)} cases")

    print("Running DryRunLLMJudge on all cases...")
    dry_run_predictions = run_dry_run(cases)

    dry_run_results = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "benchmark": benchmark_path,
            "total_cases": len(cases),
            "method": "DryRunLLMJudge",
            "is_real_llm": False,
            "note": "DRY-RUN ONLY, NOT REAL LLM OUTPUT: heuristic keyword-based simulation",
        },
        "predictions": dry_run_predictions,
    }

    dry_run_path = os.path.join(results_dir, "llm_safety_judge_dry_run_results.json")
    save_json(dry_run_results, dry_run_path)
    print(f"Dry-run results saved to {dry_run_path}")

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        model_name = os.environ.get("OPENAI_MODEL", "gpt-4")
        base_url = os.environ.get("OPENAI_BASE_URL", None)

        print(f"OPENAI_API_KEY found. Running real LLM judge ({model_name})...")
        real_predictions = run_real_llm(cases, api_key, model_name, base_url)

        real_results = {
            "metadata": {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "benchmark": benchmark_path,
                "total_cases": len(cases),
                "method": f"LLMSafetyJudgeBaseline ({model_name})",
                "is_real_llm": True,
                "model_name": model_name,
                "temperature": 0,
            },
            "predictions": real_predictions,
        }

        real_path = os.path.join(results_dir, "llm_safety_judge_real_results.json")
        save_json(real_results, real_path)
        print(f"Real LLM results saved to {real_path}")
    else:
        print("OPENAI_API_KEY not set. Skipping real LLM judge.")
        print("To run the real LLM judge, set the OPENAI_API_KEY environment variable.")

    decision_counts = {}
    for pred in dry_run_predictions:
        d = pred["decision"]
        decision_counts[d] = decision_counts.get(d, 0) + 1

    print("\n=== Dry-Run Decision Distribution ===")
    for decision, count in sorted(decision_counts.items()):
        print(f"  {decision}: {count}")

    print(f"\nResults are from: {'DRY-RUN (heuristic simulation only, NOT real LLM output)' if not api_key else 'Real LLM + Dry-run'}")


if __name__ == "__main__":
    main()
