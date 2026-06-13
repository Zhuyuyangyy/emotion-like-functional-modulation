#!/usr/bin/env python3
"""Compute Cohen's kappa for pilot-30 dual annotation.

Reads:
  - data/human_validated/annotator_A_pilot30.csv
  - data/human_validated/annotator_B_pilot30.csv

If annotations are incomplete (blank annotator_label),
prints AWAITING_ANNOTATION and exits with code 1.
"""

import csv
import sys
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "human_validated"
VALID_LABELS = {"AUTO_EXECUTE", "SIMULATE_FIRST", "HUMAN_REVIEW", "BLOCK"}


def load_annotations(csv_path):
    """Load annotator labels from a CSV file.

    Returns:
        dict mapping case_id -> annotator_label
    """
    annotations = {}
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row["case_id"]
            label = row.get("annotator_label", "").strip()
            annotations[cid] = label
    return annotations


def cohen_kappa(labels_a, labels_b):
    """Compute Cohen's kappa for two sets of labels.

    Args:
        labels_a: list of labels from annotator A
        labels_b: list of labels from annotator B

    Returns:
        float: Cohen's kappa coefficient
    """
    n = len(labels_a)
    if n == 0:
        return 0.0

    # All unique labels
    all_labels = sorted(set(labels_a + labels_b))

    # Observed agreement
    agree = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    p_o = agree / n

    # Expected agreement
    counter_a = Counter(labels_a)
    counter_b = Counter(labels_b)
    p_e = sum(counter_a[l] / n * counter_b[l] / n for l in all_labels)

    if p_e == 1.0:
        return 1.0 if p_o == 1.0 else 0.0

    kappa = (p_o - p_e) / (1.0 - p_e)
    return kappa


def compute_per_label_kappa(labels_a, labels_b):
    """Compute per-label binary kappa (one-vs-rest)."""
    all_labels = sorted(set(labels_a + labels_b))
    results = {}
    for label in all_labels:
        bin_a = [1 if l == label else 0 for l in labels_a]
        bin_b = [1 if l == label else 0 for l in labels_b]
        k = cohen_kappa(bin_a, bin_b)
        results[label] = k
    return results


def main():
    path_a = DATA_DIR / "annotator_A_pilot30.csv"
    path_b = DATA_DIR / "annotator_B_pilot30.csv"

    if not path_a.exists():
        print(f"ERROR: {path_a} not found", file=sys.stderr)
        sys.exit(1)
    if not path_b.exists():
        print(f"ERROR: {path_b} not found", file=sys.stderr)
        sys.exit(1)

    ann_a = load_annotations(path_a)
    ann_b = load_annotations(path_b)

    # Check for incomplete annotations
    blank_a = [cid for cid, label in ann_a.items() if not label]
    blank_b = [cid for cid, label in ann_b.items() if not label]

    if blank_a or blank_b:
        print(f"AWAITING_ANNOTATION")
        if blank_a:
            print(f"  Annotator A has {len(blank_a)} blank labels")
        if blank_b:
            print(f"  Annotator B has {len(blank_b)} blank labels")
        print(f"  Total cases: {len(ann_a)}")
        print(f"  Completed A: {len(ann_a) - len(blank_a)}/{len(ann_a)}")
        print(f"  Completed B: {len(ann_b) - len(blank_b)}/{len(ann_b)}")
        sys.exit(1)

    # Validate labels
    invalid_a = [cid for cid, label in ann_a.items() if label not in VALID_LABELS]
    invalid_b = [cid for cid, label in ann_b.items() if label not in VALID_LABELS]
    if invalid_a or invalid_b:
        print("INVALID LABELS FOUND:")
        for cid in invalid_a:
            print(f"  A {cid}: {ann_a[cid]!r}")
        for cid in invalid_b:
            print(f"  B {cid}: {ann_b[cid]!r}")
        sys.exit(1)

    # Align by case_id
    common_ids = sorted(set(ann_a.keys()) & set(ann_b.keys()))
    labels_a = [ann_a[cid] for cid in common_ids]
    labels_b = [ann_b[cid] for cid in common_ids]

    # Compute overall kappa
    kappa = cohen_kappa(labels_a, labels_b)
    print(f"Cohen's kappa (overall): {kappa:.4f}")

    # Compute per-label kappa
    per_label = compute_per_label_kappa(labels_a, labels_b)
    print(f"\nPer-label kappa:")
    for label, k in sorted(per_label.items()):
        print(f"  {label}: {k:.4f}")

    # Agreement stats
    agree = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    print(f"\nRaw agreement: {agree}/{len(common_ids)} = {agree/len(common_ids):.4f}")

    # Distribution
    dist_a = Counter(labels_a)
    dist_b = Counter(labels_b)
    print(f"\nAnnotator A distribution: {dict(sorted(dist_a.items()))}")
    print(f"Annotator B distribution: {dict(sorted(dist_b.items()))}")

    # Interpretation
    if kappa < 0:
        interp = "Poor (kappa < 0)"
    elif kappa < 0.20:
        interp = "Slight (0.00-0.20)"
    elif kappa < 0.40:
        interp = "Fair (0.20-0.40)"
    elif kappa < 0.60:
        interp = "Moderate (0.40-0.60)"
    elif kappa < 0.80:
        interp = "Substantial (0.60-0.80)"
    else:
        interp = "Almost perfect (0.80-1.00)"
    print(f"\nInterpretation: {interp}")

    sys.exit(0)


if __name__ == "__main__":
    main()
