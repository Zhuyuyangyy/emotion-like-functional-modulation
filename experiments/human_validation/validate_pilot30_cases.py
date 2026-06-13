#!/usr/bin/env python3
"""Validate pilot30_cases.json against schema and integrity rules."""

import json
import re
import sys
from pathlib import Path

INPUT = Path("data/human_validated/pilot30_cases.json")
OUTPUT = Path("results/human_validation/pilot30_validation_report.json")

VALID_LABELS = {"AUTO_EXECUTE", "SIMULATE_FIRST", "HUMAN_REVIEW", "BLOCK"}

VALID_SOURCE_TYPES = {
    "public_issue_derived",
    "public_security_scenario_derived",
    "handcrafted_agent_failure_case",
    "low_risk_control",
}

VALID_RISK_FACTORS = {
    "data_loss",
    "privacy_leakage",
    "credential_or_secret",
    "social_engineering",
    "harmful_automation",
    "irreversible_operation",
    "financial_or_external_side_effect",
    "low_risk_routine",
}

FORBIDDEN_FIELDS = {
    "annotator_A_label",
    "annotator_B_label",
    "final_label",
    "model_prediction",
}

PRIVACY_PATTERNS = [
    (r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "email address"),
    (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "phone number"),
    (r"(?i)api[_-]?key\s*[:=]\s*\S+", "api_key assignment"),
    (r"(?i)password\s*[:=]\s*\S+", "password assignment"),
    (r"(?i)secret\s*[:=]\s*\S+", "secret assignment"),
    (r"\b\d{17}[\dXx]\b", "ID number"),
]

REQUIRED_FIELDS = {
    "case_id", "source_type", "source_note", "user_request",
    "task_context", "proposed_agent_action", "risk_factors",
    "allowed_tools", "expected_decision_hidden", "split", "version",
}


def validate(data):
    """Validate pilot30 cases. Returns (passed, errors)."""
    errors = []

    if len(data) != 30:
        errors.append(f"Expected 30 cases, got {len(data)}")

    case_ids = set()
    for i, case in enumerate(data):
        prefix = f"Case {i+1}"

        cid = case.get("case_id", "")
        if not re.match(r"^P30-\d{3}$", cid):
            errors.append(f"{prefix}: case_id '{cid}' does not match P30-XXX format")
        if cid in case_ids:
            errors.append(f"{prefix}: duplicate case_id '{cid}'")
        case_ids.add(cid)

        st = case.get("source_type", "")
        if st not in VALID_SOURCE_TYPES:
            errors.append(f"{prefix}: invalid source_type '{st}'")

        if case.get("split") != "pilot30":
            errors.append(f"{prefix}: split must be 'pilot30', got '{case.get('split')}'")

        if case.get("version") != "human_validated_pilot_v1":
            errors.append(
                f"{prefix}: version must be 'human_validated_pilot_v1', "
                f"got '{case.get('version')}'"
            )

        ed = case.get("expected_decision_hidden", "")
        if ed not in VALID_LABELS:
            errors.append(f"{prefix}: invalid expected_decision_hidden '{ed}'")

        rf = case.get("risk_factors", [])
        for r in rf:
            if r not in VALID_RISK_FACTORS:
                errors.append(f"{prefix}: invalid risk_factor '{r}'")

        missing = REQUIRED_FIELDS - set(case.keys())
        if missing:
            errors.append(f"{prefix}: missing required fields: {missing}")

        forbidden = FORBIDDEN_FIELDS & set(case.keys())
        if forbidden:
            errors.append(f"{prefix}: forbidden fields present: {forbidden}")

        text_fields = [
            "user_request", "task_context", "proposed_agent_action",
            "source_note", "allowed_tools",
        ]
        for field in text_fields:
            val = case.get(field, "")
            if isinstance(val, list):
                val = " ".join(str(v) for v in val)
            for pattern, label in PRIVACY_PATTERNS:
                if re.search(pattern, str(val)):
                    errors.append(f"{prefix}: potential {label} found in {field}")

    all_risks = set()
    for case in data:
        all_risks.update(case.get("risk_factors", []))
    missing_risks = VALID_RISK_FACTORS - all_risks
    if missing_risks:
        errors.append(f"Missing risk taxonomy coverage: {missing_risks}")

    return len(errors) == 0, errors


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} not found")
        sys.exit(1)

    with open(INPUT, encoding="utf-8") as f:
        data = json.load(f)

    passed, errors = validate(data)

    report = {
        "input": str(INPUT),
        "total_cases": len(data),
        "passed": passed,
        "errors": errors,
        "label_distribution": {},
        "risk_factor_coverage": {},
    }

    for case in data:
        ed = case.get("expected_decision_hidden", "UNKNOWN")
        report["label_distribution"][ed] = report["label_distribution"].get(ed, 0) + 1
        for rf in case.get("risk_factors", []):
            report["risk_factor_coverage"][rf] = report["risk_factor_coverage"].get(rf, 0) + 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    if passed:
        print(f"PASS: {len(data)} cases validated successfully.")
        print(f"Report: {OUTPUT}")
    else:
        print(f"FAIL: {len(errors)} validation errors found.")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
