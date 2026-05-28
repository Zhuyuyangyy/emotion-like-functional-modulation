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

BENCHMARK_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', 'benchmark', 'semireal', 'affective_agent_safety_300.json'
)
RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), '..', 'results', 'llm_baseline'
)
PROMPT_PATH = os.path.join(
    os.path.dirname(__file__), 'prompts', 'llm_safety_judge_prompt.md'
)


def load_benchmark(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def save_jsonl(records, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")


def detect_api_config():
    api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None, None, None

    if os.environ.get("DEEPSEEK_API_KEY"):
        model_name = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
        base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        return api_key, model_name, base_url

    model_name = os.environ.get("OPENAI_MODEL", "gpt-4")
    base_url = os.environ.get("OPENAI_BASE_URL", None)
    return api_key, model_name, base_url


def run_real_llm(cases, api_key, model_name, base_url):
    judge = LLMSafetyJudgeBaseline(
        model_name=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=0,
    )
    predictions = []
    raw_outputs = []
    parse_failures = 0
    retries = 0

    for i, case in enumerate(cases):
        case_id = case.get("case_id", f"case_{i}")
        t0 = time.time()
        pred = judge.predict(case)
        elapsed = time.time() - t0

        pred["case_id"] = case_id
        pred["elapsed_seconds"] = round(elapsed, 3)

        if pred.get("raw_output", {}).get("error"):
            retries += 1
        if pred["decision"] == "SIMULATE_FIRST" and "Malformed" in pred.get("reason", ""):
            parse_failures += 1

        raw_record = {
            "case_id": case_id,
            "raw_llm_output": pred.get("raw_output", {}).get("raw_llm_output", ""),
            "parsed_decision": pred["decision"],
            "parsed_rationale": pred.get("reason", ""),
            "elapsed_seconds": round(elapsed, 3),
        }
        raw_outputs.append(raw_record)
        predictions.append(pred)

        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(cases)} cases...")

    return predictions, raw_outputs, parse_failures, retries


def main():
    benchmark_path = os.environ.get("BENCHMARK_PATH", BENCHMARK_PATH)
    results_dir = os.environ.get("RESULTS_DIR", RESULTS_DIR)

    print(f"Loading benchmark: {benchmark_path}")
    cases = load_benchmark(benchmark_path)
    print(f"Loaded {len(cases)} cases")

    api_key, model_name, base_url = detect_api_config()

    if api_key:
        provider = "DeepSeek" if os.environ.get("DEEPSEEK_API_KEY") else "OpenAI"
        print(f"API key found ({provider}). Running real LLM judge ({model_name})...")
        print(f"Base URL: {base_url or 'default'}")
        print(f"Temperature: 0")
        print(f"Prompt version: {PROMPT_PATH}")

        predictions, raw_outputs, parse_failures, retries = run_real_llm(
            cases, api_key, model_name, base_url
        )

        real_results = {
            "metadata": {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "benchmark": benchmark_path,
                "total_cases": len(cases),
                "method": f"LLMSafetyJudgeBaseline ({model_name})",
                "is_real_llm": True,
                "model_name": model_name,
                "provider": provider,
                "base_url": base_url,
                "temperature": 0,
                "prompt_version": PROMPT_PATH,
                "parse_failure_count": parse_failures,
                "retry_count": retries,
            },
            "predictions": predictions,
        }

        real_path = os.path.join(results_dir, "llm_safety_judge_real_results.json")
        save_json(real_results, real_path)
        print(f"Real LLM results saved to {real_path}")

        raw_path = os.path.join(results_dir, "llm_safety_judge_raw_outputs.jsonl")
        save_jsonl(raw_outputs, raw_path)
        print(f"Raw outputs saved to {raw_path}")

        pred_path = os.path.join(results_dir, "llm_safety_judge_predictions.json")
        save_json({
            "metadata": real_results["metadata"],
            "predictions": [
                {"case_id": p["case_id"], "decision": p["decision"], "reason": p.get("reason", "")}
                for p in predictions
            ],
        }, pred_path)
        print(f"Predictions saved to {pred_path}")

        decision_counts = {}
        for p in predictions:
            d = p["decision"]
            decision_counts[d] = decision_counts.get(d, 0) + 1

        print(f"\n=== Real LLM Decision Distribution ({model_name}) ===")
        for decision, count in sorted(decision_counts.items()):
            print(f"  {decision}: {count}")
        print(f"Parse failures: {parse_failures}")
        print(f"Retries: {retries}")
    else:
        print("No API key found (DEEPSEEK_API_KEY or OPENAI_API_KEY). Skipping real LLM judge.")

    print("\nRunning DryRunLLMJudge on all cases...")
    judge = DryRunLLMJudge()
    dry_run_predictions = []
    for i, case in enumerate(cases):
        pred = judge.predict(case)
        pred["case_id"] = case.get("case_id", f"case_{i}")
        dry_run_predictions.append(pred)

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

    print(f"\nResults source: {'Real LLM + Dry-run' if api_key else 'DRY-RUN ONLY (heuristic simulation)'}")


if __name__ == "__main__":
    main()
