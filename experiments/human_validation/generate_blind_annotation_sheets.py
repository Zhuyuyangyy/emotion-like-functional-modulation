#!/usr/bin/env python3
"""Generate dual blank annotation CSVs from pilot30_cases.json.

Creates:
  - data/human_validated/annotator_A_pilot30.csv
  - data/human_validated/annotator_B_pilot30.csv

Each CSV contains case info columns (no hidden/label columns)
plus blank annotator_label, annotator_rationale, uncertainty_flag.
"""

import json
import csv
import sys
from pathlib import Path

CASES_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "human_validated" / "pilot30_cases.json"
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "human_validated"

CSV_COLUMNS = [
    "case_id",
    "source_type",
    "user_request",
    "task_context",
    "proposed_agent_action",
    "risk_factors",
    "allowed_tools",
    "annotator_label",
    "annotator_rationale",
    "uncertainty_flag",
]

FORBIDDEN_COLUMNS = {
    "expected_decision_hidden",
    "model_prediction",
    "final_label",
    "annotator_A_label",
    "annotator_B_label",
}


def generate():
    """Generate blank annotation sheets for two annotators."""
    if not CASES_PATH.exists():
        print(f"ERROR: {CASES_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with open(CASES_PATH, encoding="utf-8") as f:
        cases = json.load(f)

    # Verify no forbidden columns in CSV_COLUMNS
    for col in CSV_COLUMNS:
        if col in FORBIDDEN_COLUMNS:
            print(f"ERROR: forbidden column {col!r} in CSV_COLUMNS", file=sys.stderr)
            sys.exit(1)

    for annotator in ["A", "B"]:
        out_path = OUT_DIR / f"annotator_{annotator}_pilot30.csv"
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(CSV_COLUMNS)
            for case in cases:
                row = [
                    case["case_id"],
                    case["source_type"],
                    case["user_request"],
                    case["task_context"],
                    case["proposed_agent_action"],
                    ";".join(case["risk_factors"]),
                    ";".join(case.get("allowed_tools", [])),
                    "",  # annotator_label (blank)
                    "",  # annotator_rationale (blank)
                    "",  # uncertainty_flag (blank)
                ]
                writer.writerow(row)
        print(f"Generated {out_path} with {len(cases)} cases")

    print("ANNOTATION SHEETS GENERATED")


def main():
    generate()


if __name__ == "__main__":
    main()
