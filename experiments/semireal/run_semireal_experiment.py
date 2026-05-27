import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import json
import argparse
import time

from experiments.semireal.semireal_adapters import (
    SemirealFullCalibratorAdapter,
    SemirealKeywordRuleBaseline,
    SemirealSafeKeywordFirstBaseline,
    SemirealRiskContextOracleBaseline,
    SemirealNoExperienceNoAffectiveBaseline,
    compute_semireal_metrics,
)
from experiments.semireal.statistical_tests import (
    run_statistical_analysis,
)


def load_benchmark(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_all_baselines(cases):
    baselines = {
        "FullCalibratorAdapter": SemirealFullCalibratorAdapter(),
        "KeywordRuleBaseline": SemirealKeywordRuleBaseline(),
        "SafeKeywordFirstBaseline": SemirealSafeKeywordFirstBaseline(),
        "RiskContextOracleBaseline": SemirealRiskContextOracleBaseline(),
        "NoExperienceNoAffectiveBaseline": SemirealNoExperienceNoAffectiveBaseline(),
    }
    all_predictions = {}
    for name, baseline in baselines.items():
        predictions = [baseline.predict(case) for case in cases]
        all_predictions[name] = predictions
    return all_predictions


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def generate_report(cases, baseline_metrics, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    lines = []
    lines.append("# V1.1 Semi-Real Experiment Report")
    lines.append("")
    lines.append("## 1. Benchmark")
    lines.append(f"Affective-Agent-Safety-300: {len(cases)} semi-real cases across 5 source types.")
    lines.append("")
    source_counts = {}
    for c in cases:
        st = c.get("source_type", "unknown")
        source_counts[st] = source_counts.get(st, 0) + 1
    lines.append("| Source Type | Count |")
    lines.append("|-------------|-------|")
    for st, cnt in sorted(source_counts.items()):
        lines.append(f"| {st} | {cnt} |")
    lines.append("")
    lines.append("## 2. Methods")
    lines.append("- **FullCalibratorAdapter**: Three-tier SafeActionCalibrator with affective/experience integration")
    lines.append("- **KeywordRuleBaseline**: Simple keyword matching")
    lines.append("- **SafeKeywordFirstBaseline**: Safe keywords override risk context (pre-V0.9.1 bug)")
    lines.append("- **RiskContextOracleBaseline**: Oracle that directly reads risk_context (upper-bound reference)")
    lines.append("- **NoExperienceNoAffectiveBaseline**: Real calibrator without affective/experience signals")
    lines.append("")
    lines.append("## 3. Main Results")
    lines.append("")
    lines.append("| Method | Accuracy | Risky Auto-Exec | False Caution | Safe Auto-Exec Acc | Composite |")
    lines.append("|--------|----------|-----------------|---------------|---------------------|-----------|")
    for name in [
        "FullCalibratorAdapter",
        "KeywordRuleBaseline",
        "SafeKeywordFirstBaseline",
        "RiskContextOracleBaseline",
        "NoExperienceNoAffectiveBaseline",
    ]:
        m = baseline_metrics.get(name, {})
        lines.append(
            f"| {name} | {m.get('action_accuracy', 0):.3f} | "
            f"{m.get('risky_auto_exec_rate', 0):.3f} | "
            f"{m.get('false_over_caution_rate', 0):.3f} | "
            f"{m.get('safe_auto_execute_accuracy', 0):.3f} | "
            f"{m.get('composite_score', 0):.3f} |"
        )
    lines.append("")
    lines.append("## 4. Findings")
    full_m = baseline_metrics.get("FullCalibratorAdapter", {})
    safe_kw_m = baseline_metrics.get("SafeKeywordFirstBaseline", {})
    lines.append(f"- Full Method risky auto-exec: {full_m.get('risky_auto_exec_rate', 0):.3f}")
    lines.append(f"- Full Method false over-caution: {full_m.get('false_over_caution_rate', 0):.3f}")
    lines.append(f"- Full Method safe auto-execute accuracy: {full_m.get('safe_auto_execute_accuracy', 0):.3f}")
    lines.append(f"- SafeKeywordFirstBaseline risky auto-exec: {safe_kw_m.get('risky_auto_exec_rate', 0):.3f}")
    lines.append("")
    lines.append("## 5. Limitations")
    lines.append("- Semi-real traces are simulated, not collected from real agent deployments.")
    lines.append("- Affective pressure labels are structured annotations, not real-time emotion signals.")
    lines.append("- Results validate the calibration mechanism on structured scenarios, not general affective intelligence.")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_sci_checklist(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    lines = []
    lines.append("# V1.1 SCI Readiness Checklist")
    lines.append("")
    items = [
        ("Benchmark", "Affective-Safety-200 + Semi-Real-300 benchmarks available"),
        ("Baseline Comparison", "4 baselines + Full Method with unified canonical implementation"),
        ("Ablation Study", "6 ablation variants including w/o_strict_context_priority"),
        ("Longitudinal Memory", "3-group experiment (no/single/accumulated memory)"),
        ("Statistical Tests", "Bootstrap 95% CI + McNemar paired comparison"),
        ("Per-Category Metrics", "Both benchmarks have per-category breakdowns"),
        ("Annotation Guideline", "Semi-Real-300 has formal annotation guideline"),
        ("Reproducibility", "All experiments deterministic with fixed seed"),
        ("No Label Leakage", "Full Method does not read gold_decision/expected_decision"),
        ("Limitations Section", "All reports include explicit limitations"),
        ("Oracle Baseline Labeled", "RiskContextOracleBaseline clearly marked as oracle/upper-bound"),
        ("Canonical Full Method", "Single FullCalibratorAdapter used in both baseline and ablation tables"),
        ("V0.9.1 Unchanged", "Core framework not modified for V1.0/V1.1 experiments"),
    ]
    lines.append("| Item | Status |")
    lines.append("|------|--------|")
    for item, desc in items:
        lines.append(f"| {item} | {desc} |")
    lines.append("")
    lines.append("## Remaining Work for SCI Submission")
    lines.append("- [ ] External validation on real agent logs (not simulated traces)")
    lines.append("- [ ] Inter-annotator agreement on semi-real benchmark")
    lines.append("- [ ] Comparison with LLM-based safety classifiers")
    lines.append("- [ ] Computational cost analysis")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default="benchmark/semireal/affective_agent_safety_300.json")
    parser.add_argument("--output-dir", default="experiments/results/semireal")
    args = parser.parse_args()

    print(f"Loading benchmark: {args.benchmark}")
    cases = load_benchmark(args.benchmark)
    print(f"Loaded {len(cases)} cases")

    print("Running baselines...")
    all_predictions = run_all_baselines(cases)

    print("Computing metrics...")
    baseline_metrics = {}
    for name, predictions in all_predictions.items():
        baseline_metrics[name] = compute_semireal_metrics(cases, predictions)

    results_dir = args.output_dir
    docs_dir = "docs/demo_evidence_v1_1"
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    full_results = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "benchmark": args.benchmark,
            "total_cases": len(cases),
        },
        "baseline_metrics": baseline_metrics,
    }
    save_json(full_results, os.path.join(results_dir, "semireal_full_results.json"))

    print("Running statistical analysis...")
    run_statistical_analysis(cases, all_predictions, results_dir)

    print("Generating reports...")
    generate_report(
        cases, baseline_metrics,
        os.path.join(docs_dir, "v1_1_semireal_experiment_report.md"),
    )
    generate_sci_checklist(os.path.join(docs_dir, "v1_1_sci_readiness_checklist.md"))

    print("\n=== Full Method Metrics (Semi-Real) ===")
    full_m = baseline_metrics.get("FullCalibratorAdapter", {})
    print(f"  Action Accuracy:          {full_m.get('action_accuracy', 0):.4f}")
    print(f"  Risky Auto-Exec Rate:     {full_m.get('risky_auto_exec_rate', 0):.4f}")
    print(f"  False Over-Caution Rate:  {full_m.get('false_over_caution_rate', 0):.4f}")
    print(f"  Safe Auto-Exec Accuracy:  {full_m.get('safe_auto_execute_accuracy', 0):.4f}")
    print(f"  Composite Score:          {full_m.get('composite_score', 0):.4f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
