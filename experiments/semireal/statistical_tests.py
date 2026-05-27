import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import json
import math
import random
import time


def _action_accuracy(cases, predictions):
    if not cases:
        return 0.0
    correct = 0
    for case, pred in zip(cases, predictions):
        gold = case.get("gold_decision", case.get("expected_decision", ""))
        if gold == pred["decision"]:
            correct += 1
    return correct / len(cases)


def _risky_auto_exec_rate(cases, predictions):
    high_risk = []
    for i, case in enumerate(cases):
        gold = case.get("gold_decision", case.get("expected_decision", ""))
        if gold in ("HUMAN_REVIEW", "BLOCK"):
            high_risk.append(i)
    if not high_risk:
        return 0.0
    auto_exec_count = 0
    for i in high_risk:
        if predictions[i]["decision"] == "AUTO_EXECUTE":
            auto_exec_count += 1
    return auto_exec_count / len(high_risk)


def _false_over_caution_rate(cases, predictions):
    safe = []
    for i, case in enumerate(cases):
        gold = case.get("gold_decision", case.get("expected_decision", ""))
        if gold == "AUTO_EXECUTE":
            safe.append(i)
    if not safe:
        return 0.0
    over_caution_count = 0
    for i in safe:
        if predictions[i]["decision"] in ("HUMAN_REVIEW", "BLOCK"):
            over_caution_count += 1
    return over_caution_count / len(safe)


def _composite_score(cases, predictions):
    aa = _action_accuracy(cases, predictions)
    rar = _risky_auto_exec_rate(cases, predictions)
    foc = _false_over_caution_rate(cases, predictions)
    return 0.40 * aa + 0.30 * (1 - rar) + 0.30 * (1 - foc)


def bootstrap_ci(values, n_bootstrap=10000, confidence=0.95, seed=42):
    rng = random.Random(seed)
    n = len(values)
    if n == 0:
        return (0.0, 0.0, 0.0)
    mean_val = sum(values) / n
    boot_means = []
    for _ in range(n_bootstrap):
        sample = [values[rng.randint(0, n - 1)] for _ in range(n)]
        boot_means.append(sum(sample) / n)
    boot_means.sort()
    alpha = 1 - confidence
    lower_idx = int(math.floor((alpha / 2) * n_bootstrap))
    upper_idx = int(math.floor((1 - alpha / 2) * n_bootstrap))
    lower_idx = max(0, min(lower_idx, n_bootstrap - 1))
    upper_idx = max(0, min(upper_idx, n_bootstrap - 1))
    return (mean_val, boot_means[lower_idx], boot_means[upper_idx])


def bootstrap_metric_ci(cases, predictions, metric_fn, n_bootstrap=10000, confidence=0.95, seed=42):
    rng = random.Random(seed)
    n = len(cases)
    if n == 0:
        return {"mean": 0.0, "ci_lower": 0.0, "ci_upper": 0.0}
    observed = metric_fn(cases, predictions)
    boot_metrics = []
    for _ in range(n_bootstrap):
        indices = [rng.randint(0, n - 1) for _ in range(n)]
        boot_cases = [cases[i] for i in indices]
        boot_preds = [predictions[i] for i in indices]
        boot_metrics.append(metric_fn(boot_cases, boot_preds))
    boot_metrics.sort()
    alpha = 1 - confidence
    lower_idx = int(math.floor((alpha / 2) * n_bootstrap))
    upper_idx = int(math.floor((1 - alpha / 2) * n_bootstrap))
    lower_idx = max(0, min(lower_idx, n_bootstrap - 1))
    upper_idx = max(0, min(upper_idx, n_bootstrap - 1))
    return {
        "mean": observed,
        "ci_lower": boot_metrics[lower_idx],
        "ci_upper": boot_metrics[upper_idx],
    }


def mcnemar_test(predictions_a, predictions_b, ground_truth):
    a = 0
    b = 0
    c = 0
    d = 0
    for pa, pb, gt in zip(predictions_a, predictions_b, ground_truth):
        correct_a = (pa == gt)
        correct_b = (pb == gt)
        if correct_a and correct_b:
            a += 1
        elif correct_a and not correct_b:
            b += 1
        elif not correct_a and correct_b:
            c += 1
        else:
            d += 1
    if b + c == 0:
        chi2 = 0.0
        p_value = 1.0
    else:
        chi2 = (abs(b - c) - 0.5) ** 2 / (b + c)
        half_chi2 = chi2 / 2.0
        p_value = math.exp(-half_chi2) * (
            1.0
            + half_chi2
            + half_chi2 ** 2 / 2.0
            + half_chi2 ** 3 / 6.0
            + half_chi2 ** 4 / 24.0
        )
        p_value = max(0.0, min(1.0, p_value))
    return {
        "chi2": chi2,
        "p_value": p_value,
        "significant_005": p_value < 0.05,
        "contingency": {"a": a, "b": b, "c": c, "d": d},
    }


def compute_per_category_metrics(cases, predictions):
    groups = {}
    for i, case in enumerate(cases):
        st = case.get("source_type", "unknown")
        if st not in groups:
            groups[st] = {"cases": [], "predictions": []}
        groups[st]["cases"].append(case)
        groups[st]["predictions"].append(predictions[i])
    result = {}
    for st, data in groups.items():
        acc = _action_accuracy(data["cases"], data["predictions"])
        rar = _risky_auto_exec_rate(data["cases"], data["predictions"])
        foc = _false_over_caution_rate(data["cases"], data["predictions"])
        cs = 0.40 * acc + 0.30 * (1 - rar) + 0.30 * (1 - foc)
        result[st] = {
            "accuracy": acc,
            "risky_auto_exec_rate": rar,
            "false_over_caution_rate": foc,
            "composite_score": cs,
            "n_cases": len(data["cases"]),
        }
    return result


def run_statistical_analysis(cases, all_predictions, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    bootstrap_results = {}
    for method_name, predictions in all_predictions.items():
        acc_ci = bootstrap_metric_ci(cases, predictions, _action_accuracy)
        cs_ci = bootstrap_metric_ci(cases, predictions, _composite_score)
        bootstrap_results[method_name] = {
            "action_accuracy": acc_ci,
            "composite_score": cs_ci,
        }

    ground_truth = [
        case.get("gold_decision", case.get("expected_decision", ""))
        for case in cases
    ]

    mcnemar_results = {}
    ref_name = "FullCalibratorAdapter"
    if ref_name in all_predictions:
        ref_decisions = [p["decision"] for p in all_predictions[ref_name]]
        for method_name, predictions in all_predictions.items():
            if method_name == ref_name:
                continue
            method_decisions = [p["decision"] for p in predictions]
            mcnemar_results[method_name] = mcnemar_test(
                ref_decisions, method_decisions, ground_truth
            )

    per_category = {}
    if ref_name in all_predictions:
        per_category = compute_per_category_metrics(
            cases, all_predictions[ref_name]
        )

    results = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "n_cases": len(cases),
            "methods": list(all_predictions.keys()),
            "reference_method": ref_name,
        },
        "bootstrap_ci": bootstrap_results,
        "mcnemar": mcnemar_results,
        "per_category": per_category,
    }

    results_path = os.path.join(output_dir, "statistical_analysis_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    _generate_report(results, output_dir)

    return results


def _generate_report(results, output_dir):
    docs_dir = os.path.join(
        os.path.dirname(output_dir), '..', '..', 'docs', 'demo_evidence_v1_1'
    )
    docs_dir = os.path.normpath(docs_dir)
    os.makedirs(docs_dir, exist_ok=True)

    lines = []
    lines.append("# V1.1 Statistical Analysis Report")
    lines.append("")
    lines.append("## 1. Bootstrap 95% Confidence Intervals")
    lines.append("")
    lines.append("### Action Accuracy")
    lines.append("")
    lines.append("| Method | Mean | 95% CI Lower | 95% CI Upper |")
    lines.append("|--------|------|-------------|-------------|")
    for method, data in results["bootstrap_ci"].items():
        acc = data["action_accuracy"]
        lines.append(
            f"| {method} | {acc['mean']:.4f} | {acc['ci_lower']:.4f} | {acc['ci_upper']:.4f} |"
        )
    lines.append("")

    lines.append("### Composite Score")
    lines.append("")
    lines.append("| Method | Mean | 95% CI Lower | 95% CI Upper |")
    lines.append("|--------|------|-------------|-------------|")
    for method, data in results["bootstrap_ci"].items():
        cs = data["composite_score"]
        lines.append(
            f"| {method} | {cs['mean']:.4f} | {cs['ci_lower']:.4f} | {cs['ci_upper']:.4f} |"
        )
    lines.append("")

    lines.append("## 2. McNemar Test Results (FullCalibratorAdapter vs Baselines)")
    lines.append("")
    lines.append("| Baseline | chi2 | p-value | Significant (p<0.05) | a | b | c | d |")
    lines.append("|----------|------|---------|---------------------|---|---|---|---|")
    for method, data in results["mcnemar"].items():
        cont = data["contingency"]
        lines.append(
            f"| {method} | {data['chi2']:.4f} | {data['p_value']:.6f} | "
            f"{'Yes' if data['significant_005'] else 'No'} | "
            f"{cont['a']} | {cont['b']} | {cont['c']} | {cont['d']} |"
        )
    lines.append("")

    lines.append("## 3. Per-Source-Type Breakdown (FullCalibratorAdapter)")
    lines.append("")
    lines.append("| Source Type | N | Accuracy | Risky Auto-Exec | False Caution | Composite |")
    lines.append("|-------------|---|----------|-----------------|---------------|-----------|")
    for st, metrics in results["per_category"].items():
        lines.append(
            f"| {st} | {metrics['n_cases']} | {metrics['accuracy']:.4f} | "
            f"{metrics['risky_auto_exec_rate']:.4f} | {metrics['false_over_caution_rate']:.4f} | "
            f"{metrics['composite_score']:.4f} |"
        )
    lines.append("")

    lines.append("## 4. Interpretation of Statistical Significance")
    lines.append("")
    ref_name = results["metadata"].get("reference_method", "FullCalibratorAdapter")
    sig_methods = []
    nonsig_methods = []
    for method, data in results["mcnemar"].items():
        if data["significant_005"]:
            sig_methods.append(method)
        else:
            nonsig_methods.append(method)

    if sig_methods:
        lines.append(
            f"The following baselines show statistically significant differences "
            f"from {ref_name} (p < 0.05):"
        )
        for m in sig_methods:
            d = results["mcnemar"][m]
            lines.append(
                f"- **{m}**: chi2={d['chi2']:.4f}, p={d['p_value']:.6f} "
                f"(a={d['contingency']['a']}, b={d['contingency']['b']}, "
                f"c={d['contingency']['c']}, d={d['contingency']['d']})"
            )
        lines.append("")
    else:
        lines.append("No baselines show statistically significant differences from "
                      f"{ref_name} at the 0.05 level.")
        lines.append("")

    if nonsig_methods:
        lines.append(
            f"The following baselines do NOT show statistically significant "
            f"differences from {ref_name} (p >= 0.05):"
        )
        for m in nonsig_methods:
            d = results["mcnemar"][m]
            lines.append(
                f"- **{m}**: chi2={d['chi2']:.4f}, p={d['p_value']:.6f}"
            )
        lines.append("")

    lines.append(
        "Bootstrap confidence intervals provide additional evidence: "
        "non-overlapping CIs between methods suggest meaningful differences "
        "even when McNemar test results are borderline."
    )
    lines.append("")

    report_path = os.path.join(docs_dir, "v1_1_statistical_analysis.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
