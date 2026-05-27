import sys
import os
import json
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from experiments.metrics_affective_safety import (
    compute_all_metrics,
    compute_metrics_by_category,
)
from experiments.semireal.semireal_adapters import convert_semireal_case

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), '..', 'results', 'llm_baseline'
)
BENCHMARK_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', 'benchmark', 'semireal', 'affective_agent_safety_300.json'
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def load_benchmark(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_results(results_path, benchmark_path):
    cases = load_benchmark(benchmark_path)
    results = load_json(results_path)

    predictions = results["predictions"]
    is_real_llm = results["metadata"].get("is_real_llm", False)
    method_name = results["metadata"].get("method", "Unknown")

    converted_cases = [convert_semireal_case(c) for c in cases]

    metrics = compute_all_metrics(converted_cases, predictions)
    metrics_by_category = compute_metrics_by_category(converted_cases, predictions)

    return {
        "method": method_name,
        "is_real_llm": is_real_llm,
        "total_cases": len(cases),
        "metrics": metrics,
        "metrics_by_category": metrics_by_category,
    }


def generate_comparison_table(evaluation_results, existing_metrics_path=None):
    lines = []
    lines.append("| Method | Type | Accuracy | Risky Auto-Exec | False Caution | Verification | HR F1 | Composite |")
    lines.append("|--------|------|----------|-----------------|---------------|--------------|-------|-----------|")

    if existing_metrics_path and os.path.exists(existing_metrics_path):
        existing = load_json(existing_metrics_path)
        baseline_metrics = existing.get("baseline_metrics", {})
        for name, m in baseline_metrics.items():
            lines.append(
                f"| {name} | rule-based | {m.get('action_accuracy', 0):.3f} | "
                f"{m.get('risky_auto_exec_rate', 0):.3f} | "
                f"{m.get('false_over_caution_rate', 0):.3f} | "
                f"{m.get('verification_appropriateness', 0):.3f} | "
                f"{m.get('human_review_f1', 0):.3f} | "
                f"{m.get('composite_score', 0):.3f} |"
            )

    for result in evaluation_results:
        m = result["metrics"]
        method_type = "LLM" if result["is_real_llm"] else "heuristic-sim"
        lines.append(
            f"| {result['method']} | {method_type} | {m.get('action_accuracy', 0):.3f} | "
            f"{m.get('risky_auto_exec_rate', 0):.3f} | "
            f"{m.get('false_over_caution_rate', 0):.3f} | "
            f"{m.get('verification_appropriateness', 0):.3f} | "
            f"{m.get('human_review_f1', 0):.3f} | "
            f"{m.get('composite_score', 0):.3f} |"
        )

    return "\n".join(lines)


def main():
    benchmark_path = os.environ.get("BENCHMARK_PATH", BENCHMARK_PATH)
    results_dir = os.environ.get("RESULTS_DIR", RESULTS_DIR)

    dry_run_path = os.path.join(results_dir, "llm_safety_judge_dry_run_results.json")
    real_path = os.path.join(results_dir, "llm_safety_judge_real_results.json")
    metrics_path = os.path.join(results_dir, "llm_safety_judge_metrics.json")

    existing_semireal_metrics = os.path.join(
        os.path.dirname(__file__), '..', 'results', 'semireal', 'semireal_full_results.json'
    )

    evaluation_results = []

    if os.path.exists(dry_run_path):
        print(f"Evaluating dry-run results from {dry_run_path}...")
        result = evaluate_results(dry_run_path, benchmark_path)
        evaluation_results.append(result)
        print(f"  Method: {result['method']}")
        print(f"  Action Accuracy: {result['metrics']['action_accuracy']:.4f}")
        print(f"  Risky Auto-Exec Rate: {result['metrics']['risky_auto_exec_rate']:.4f}")
        print(f"  False Over-Caution Rate: {result['metrics']['false_over_caution_rate']:.4f}")
        print(f"  Composite Score: {result['metrics']['composite_score']:.4f}")
    else:
        print(f"Dry-run results not found at {dry_run_path}. Run run_llm_safety_judge_baseline.py first.")

    if os.path.exists(real_path):
        print(f"\nEvaluating real LLM results from {real_path}...")
        result = evaluate_results(real_path, benchmark_path)
        evaluation_results.append(result)
        print(f"  Method: {result['method']}")
        print(f"  Action Accuracy: {result['metrics']['action_accuracy']:.4f}")
        print(f"  Risky Auto-Exec Rate: {result['metrics']['risky_auto_exec_rate']:.4f}")
        print(f"  Composite Score: {result['metrics']['composite_score']:.4f}")

    if not evaluation_results:
        print("No results to evaluate.")
        return

    metrics_output = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "benchmark": benchmark_path,
        },
        "evaluation_results": evaluation_results,
    }
    save_json(metrics_output, metrics_path)
    print(f"\nMetrics saved to {metrics_path}")

    print("\n=== Comparison Table ===")
    table = generate_comparison_table(evaluation_results, existing_semireal_metrics)
    print(table)

    table_path = os.path.join(results_dir, "llm_safety_judge_comparison_table.txt")
    with open(table_path, "w", encoding="utf-8") as f:
        f.write(table)
    print(f"Comparison table saved to {table_path}")


if __name__ == "__main__":
    main()
