#!/usr/bin/env python3
"""Smoke test for kappa computation pipeline using AI-generated fixture data.

This is NOT a human validation test. It validates that the kappa
computation pipeline works correctly with fixture data.
"""

import csv
import sys
from pathlib import Path
from collections import Counter

FIXTURE_DIR = Path(__file__).resolve().parent / 'fixtures' / 'annotation'
VALID_LABELS = {'AUTO_EXECUTE', 'SIMULATE_FIRST', 'HUMAN_REVIEW', 'BLOCK'}


def load_labels(path):
    labels = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            labels[row['case_id']] = row['annotator_label'].strip()
    return labels


def cohen_kappa(labels_a, labels_b):
    n = len(labels_a)
    if n == 0:
        return 0.0
    all_labels = sorted(set(labels_a + labels_b))
    agree = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    p_o = agree / n
    counter_a = Counter(labels_a)
    counter_b = Counter(labels_b)
    p_e = sum(counter_a[l] / n * counter_b[l] / n for l in all_labels)
    if p_e == 1.0:
        return 1.0 if p_o == 1.0 else 0.0
    return (p_o - p_e) / (1.0 - p_e)


def main():
    path_a = FIXTURE_DIR / 'ai_generated_pilot30_A.csv'
    path_b = FIXTURE_DIR / 'ai_generated_pilot30_B.csv'

    if not path_a.exists():
        print(f'SKIP: {path_a} not found (fixture data not available)')
        sys.exit(0)
    if not path_b.exists():
        print(f'SKIP: {path_b} not found (fixture data not available)')
        sys.exit(0)

    ann_a = load_labels(path_a)
    ann_b = load_labels(path_b)

    assert len(ann_a) == 30, f'Expected 30 cases in A, got {len(ann_a)}'
    assert len(ann_b) == 30, f'Expected 30 cases in B, got {len(ann_b)}'
    assert set(ann_a.keys()) == set(ann_b.keys()), 'Case ID mismatch'

    for cid, label in ann_a.items():
        assert label in VALID_LABELS, f'A {cid}: invalid label {label}'
    for cid, label in ann_b.items():
        assert label in VALID_LABELS, f'B {cid}: invalid label {label}'

    common_ids = sorted(set(ann_a.keys()) & set(ann_b.keys()))
    labels_a = [ann_a[cid] for cid in common_ids]
    labels_b = [ann_b[cid] for cid in common_ids]
    kappa = cohen_kappa(labels_a, labels_b)

    print(f'Kappa smoke test: kappa={kappa:.4f} (AI-generated fixture data)')
    print('  This is NOT a human validation result.')
    print('PIPELINE VALIDATION PASSED')


if __name__ == '__main__':
    main()
