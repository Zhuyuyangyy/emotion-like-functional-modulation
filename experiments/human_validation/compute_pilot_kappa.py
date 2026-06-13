#!/usr/bin/env python3
"""Compute Cohen's kappa and agreement metrics for pilot30 annotations.

If completed annotation files do not exist, outputs AWAITING_ANNOTATION
and exits 1. No fake results are ever generated.
"""

import csv
import json
import sys
from pathlib import Path

INPUT_A = Path("data/human_validated/annotator_A_pilot30_completed.csv")
INPUT_B = Path("data/human_validated/annotator_B_pilot30_completed.csv")
OUTPUT_KAPPA = Path("results/human_validation/pilot30_kappa_report.json")
OUTPUT_DISAGREEMENT = Path("results/human_validation/pilot30_disagreement_report.md")

VALID_LABELS = {"AUTO_EXECUTE", "SIMULATE_FIRST", "HUMAN_REVIEW", "BLOCK"}
LABEL_ORDER = ["AUTO_EXECUTE", "SIMULATE_FIRST", "HUMAN_REVIEW", "BLOCK"]


def check_awaiting():
    """Return True if completed files don't exist (expected state)."""
    if not INPUT_A.exists() or not INPUT_B.exists():
        print("AWAITING_ANNOTATION")
        if not INPUT_A.exists():
            print(f"  Missing: {INPUT_A.name}")
        if not INPUT_B.exists():
            print(f"  Missing: {INPUT_B.name}")
        print("  Cannot compute kappa without completed annotation files.")
        print("  Please provide completed annotation CSVs from two annotators.")
        return True
    return False


def read_annotations(path):
    """Read completed annotation CSV into dict keyed by case_id."""
    annotations = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row["case_id"]
            annotations[cid] = {
                "annotator_label": row.get("annotator_label", "").strip(),
                "annotator_rationale": row.get("annotator_rationale", "").strip(),
                "uncertainty_flag": row.get("uncertainty_flag", "").strip(),
                "user_request": row.get("user_request", ""),
                "risk_factors": row.get("risk_factors", ""),
            }
    return annotations


def validate_annotations(ann_a, ann_b):
    """Validate completed annotations."""
    errors = []

    if set(ann_a.keys()) != set(ann_b.keys()):
        errors.append(f"Case ID mismatch: A has {len(ann_a)}, B has {len(ann_b)}")

    common = set(ann_a.keys()) & set(ann_b.keys())
    for cid in common:
        a_label = ann_a[cid]["annotator_label"]
        b_label = ann_b[cid]["annotator_label"]

        if not a_label:
            errors.append(f"{cid}: annotator_A label is empty")
        elif a_label not in VALID_LABELS:
            errors.append(f"{cid}: annotator_A invalid label '{a_label}'")

        if not b_label:
            errors.append(f"{cid}: annotator_B label is empty")
        elif b_label not in VALID_LABELS:
            errors.append(f"{cid}: annotator_B invalid label '{b_label}'")

        if not ann_a[cid]["annotator_rationale"]:
            errors.append(f"{cid}: annotator_A rationale is empty")
        if not ann_b[cid]["annotator_rationale"]:
            errors.append(f"{cid}: annotator_B rationale is empty")

    return len(errors) == 0, errors


def compute_kappa(labels_a, labels_b):
    """Compute Cohen's kappa manually."""
    label_to_idx = {l: i for i, l in enumerate(LABEL_ORDER)}
    n = len(LABEL_ORDER)
    matrix = [[0] * n for _ in range(n)]

    for a, b in zip(labels_a, labels_b):
        if a in label_to_idx and b in label_to_idx:
            matrix[label_to_idx[a]][label_to_idx[b]] += 1

    total = sum(sum(row) for row in matrix)
    if total == 0:
        return 0.0

    po = sum(matrix[i][i] for i in range(n)) / total

    row_sums = [sum(matrix[i]) for i in range(n)]
    col_sums = [sum(matrix[i][j] for i in range(n)) for j in range(n)]
    pe = sum(row_sums[i] * col_sums[i] for i in range(n)) / (total * total)

    if pe == 1.0:
        return 1.0

    return (po - pe) / (1.0 - pe)


def compute_metrics(ann_a, ann_b):
    """Compute all agreement metrics."""
    common = sorted(set(ann_a.keys()) & set(ann_b.keys()))
    labels_a = [ann_a[c]["annotator_label"] for c in common]
    labels_b = [ann_b[c]["annotator_label"] for c in common]

    agreements = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    percent_agreement = agreements / len(common) if common else 0.0

    kappa = compute_kappa(labels_a, labels_b)

    label_to_idx = {l: i for i, l in enumerate(LABEL_ORDER)}
    n = len(LABEL_ORDER)
    confusion = [[0] * n for _ in range(n)]
    for a, b in zip(labels_a, labels_b):
        if a in label_to_idx and b in label_to_idx:
            confusion[label_to_idx[a]][label_to_idx[b]] += 1

    per_label = {}
    for label in LABEL_ORDER:
        idx = label_to_idx[label]
        total_a = sum(confusion[idx])
        total_b = sum(confusion[i][idx] for i in range(n))
        agree = confusion[idx][idx]
        denom = total_a + total_b
        per_label[label] = {
            "annotator_A_count": total_a,
            "annotator_B_count": total_b,
            "agreements": agree,
            "agreement_rate": (2 * agree / denom) if denom > 0 else 0.0,
        }

    disagreements = []
    for cid in common:
        a_label = ann_a[cid]["annotator_label"]
        b_label = ann_b[cid]["annotator_label"]
        if a_label != b_label:
            disagreements.append({
                "case_id": cid,
                "annotator_A_label": a_label,
                "annotator_B_label": b_label,
                "annotator_A_rationale": ann_a[cid]["annotator_rationale"],
                "annotator_B_rationale": ann_b[cid]["annotator_rationale"],
                "risk_factors": ann_a[cid].get("risk_factors", ""),
                "user_request_summary": ann_a[cid].get("user_request", "")[:100],
            })

    return {
        "total_cases": len(common),
        "agreements": agreements,
        "percent_agreement": round(percent_agreement, 4),
        "cohens_kappa": round(kappa, 4),
        "confusion_matrix": {
            "labels": LABEL_ORDER,
            "matrix": confusion,
        },
        "per_label_agreement": per_label,
        "disagreement_count": len(disagreements),
        "disagreement_cases": disagreements,
    }


def write_disagreement_report(metrics):
    """Write disagreement report as markdown."""
    with open(OUTPUT_DISAGREEMENT, "w", encoding="utf-8") as f:
        f.write("# Pilot-30 Disagreement Report\n\n")
        f.write(f"**Total cases**: {metrics['total_cases']}\n")
        f.write(f"**Agreements**: {metrics['agreements']}\n")
        f.write(f"**Disagreements**: {metrics['disagreement_count']}\n")
        f.write(f"**Percent agreement**: {metrics['percent_agreement']}\n")
        f.write(f"**Cohen's kappa**: {metrics['cohens_kappa']}\n\n")

        if metrics["disagreement_cases"]:
            f.write("## Disagreement Cases\n\n")
            for d in metrics["disagreement_cases"]:
                f.write(f"### {d['case_id']}\n")
                f.write(f"- **A**: {d['annotator_A_label']} - {d['annotator_A_rationale']}\n")
                f.write(f"- **B**: {d['annotator_B_label']} - {d['annotator_B_rationale']}\n")
                f.write(f"- **Risk factors**: {d['risk_factors']}\n")
                f.write(f"- **Request**: {d['user_request_summary']}...\n\n")
        else:
            f.write("No disagreements found.\n")

        f.write("## Confusion Matrix\n\n")
        labels = metrics["confusion_matrix"]["labels"]
        matrix = metrics["confusion_matrix"]["matrix"]
        f.write("| | " + " | ".join(labels) + " |\n")
        f.write("|---|" + "|".join(["---"] * len(labels)) + "|\n")
        for i, label in enumerate(labels):
            f.write(f"| {label} | " + " | ".join(str(v) for v in matrix[i]) + " |\n")

        f.write("\n**Note**: final_label must be determined by human arbitration.\n")


def main():
    if check_awaiting():
        sys.exit(1)

    ann_a = read_annotations(INPUT_A)
    ann_b = read_annotations(INPUT_B)

    passed, errors = validate_annotations(ann_a, ann_b)
    if not passed:
        print(f"Validation failed: {len(errors)} errors")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    metrics = compute_metrics(ann_a, ann_b)

    OUTPUT_KAPPA.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_KAPPA, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    write_disagreement_report(metrics)

    print("PASS: Kappa computed successfully.")
    print(f"  Cohen's kappa: {metrics['cohens_kappa']}")
    print(f"  Percent agreement: {metrics['percent_agreement']}")
    print(f"  Disagreements: {metrics['disagreement_count']}")
    print(f"  Report: {OUTPUT_KAPPA}")
    print(f"  Disagreement report: {OUTPUT_DISAGREEMENT}")


if __name__ == "__main__":
    main()
