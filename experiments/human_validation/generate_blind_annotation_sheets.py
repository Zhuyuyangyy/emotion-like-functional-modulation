#!/usr/bin/env python3
"""Generate blind annotation sheets for annotator A and B from pilot30 cases."""

import csv
import json
import sys
from pathlib import Path

INPUT = Path("data/human_validated/pilot30_cases.json")
OUTPUT_A = Path("data/human_validated/annotator_A_pilot30.csv")
OUTPUT_B = Path("data/human_validated/annotator_B_pilot30.csv")

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


def validate_input(data):
    """Basic validation before generating sheets."""
    errors = []
    if len(data) != 30:
        errors.append(f"Expected 30 cases, got {len(data)}")

    valid_labels = {"AUTO_EXECUTE", "SIMULATE_FIRST", "HUMAN_REVIEW", "BLOCK"}
    for i, case in enumerate(data):
        ed = case.get("expected_decision_hidden", "")
        if ed not in valid_labels:
            errors.append(f"Case {i+1}: invalid expected_decision_hidden '{ed}'")

    for fc in FORBIDDEN_COLUMNS:
        if fc in CSV_COLUMNS:
            errors.append(f"CSV output contains forbidden column '{fc}'")

    return len(errors) == 0, errors


def generate_sheets(data):
    """Generate A and B annotation CSVs."""
    for output_path in [OUTPUT_A, OUTPUT_B]:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writeheader()

            for case in data:
                row = {
                    "case_id": case["case_id"],
                    "source_type": case["source_type"],
                    "user_request": case["user_request"],
                    "task_context": case["task_context"],
                    "proposed_agent_action": case["proposed_agent_action"],
                    "risk_factors": "; ".join(case.get("risk_factors", [])),
                    "allowed_tools": "; ".join(case.get("allowed_tools", [])),
                    "annotator_label": "",
                    "annotator_rationale": "",
                    "uncertainty_flag": "",
                }
                writer.writerow(row)


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} not found")
        sys.exit(1)

    with open(INPUT, encoding="utf-8") as f:
        data = json.load(f)

    passed, errors = validate_input(data)
    if not passed:
        print(f"Validation failed: {len(errors)} errors")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    generate_sheets(data)
    print("PASS: Generated annotation sheets.")
    print(f"  Annotator A: {OUTPUT_A}")
    print(f"  Annotator B: {OUTPUT_B}")
    print(f"  Total cases: {len(data)}")
    print("  Empty fields: annotator_label, annotator_rationale, uncertainty_flag")
    print("  AWAITING_ANNOTATION: sheets are blank, waiting for human annotators.")


if __name__ == "__main__":
    main()
