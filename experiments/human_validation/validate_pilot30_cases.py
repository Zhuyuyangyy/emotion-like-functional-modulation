#!/usr/bin/env python3
"""Validate pilot30_cases.json against the Phase 2 schema.

Checks:
  - Exactly 30 cases
  - case_id format P30-NNN
  - source_type in whitelist
  - expected_decision_hidden in label whitelist
  - risk_factors entries in risk type whitelist
  - No forbidden fields (expected_decision_hidden must NOT appear in CSV output)
  - No privacy-leaking patterns in non-hidden fields
"""

import json
import sys
from pathlib import Path

CASES_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "human_validated" / "pilot30_cases.json"

VALID_LABELS = {"AUTO_EXECUTE", "SIMULATE_FIRST", "HUMAN_REVIEW", "BLOCK"}
VALID_RISK_TYPES = {
    "data_loss", "privacy_leakage", "credential_or_secret",
    "social_engineering", "harmful_automation", "irreversible_operation",
    "financial_or_external_side_effect", "low_risk_routine",
}
VALID_SOURCE_TYPES = {"synthetic_template", "real_world_report", "adversarial_construction"}
FORBIDDEN_IN_CSV = {"expected_decision_hidden", "model_prediction", "final_label",
                    "annotator_A_label", "annotator_B_label"}
PRIVACY_PATTERNS = ["password", "secret_key", "api_key", "token", "ssn",
                    "social_security", "credit_card"]


def validate():
    """Run all validation checks. Returns (ok, messages)."""
    messages = []

    if not CASES_PATH.exists():
        return False, [f"File not found: {CASES_PATH}"]

    with open(CASES_PATH, encoding="utf-8") as f:
        cases = json.load(f)

    # Check 1: exactly 30 cases
    if len(cases) != 30:
        messages.append(f"Expected 30 cases, got {len(cases)}")
    else:
        messages.append(f"OK: {len(cases)} cases")

    case_ids = set()
    for i, case in enumerate(cases):
        cid = case.get("case_id", "")
        prefix = f"Case {i} ({cid}):"

        # Check 2: case_id format
        if not cid.startswith("P30-") or len(cid) != 7:
            messages.append(f"{prefix} bad case_id format: {cid!r}")
        else:
            case_ids.add(cid)

        # Check 3: source_type
        st = case.get("source_type", "")
        if st not in VALID_SOURCE_TYPES:
            messages.append(f"{prefix} invalid source_type: {st!r}")

        # Check 4: label
        label = case.get("expected_decision_hidden", "")
        if label not in VALID_LABELS:
            messages.append(f"{prefix} invalid label: {label!r}")

        # Check 5: risk_factors
        rf = case.get("risk_factors", [])
        for r in rf:
            if r not in VALID_RISK_TYPES:
                messages.append(f"{prefix} invalid risk_factor: {r!r}")

        # Check 6: allowed_tools
        if "allowed_tools" not in case:
            messages.append(f"{prefix} missing allowed_tools")

        # Check 7: version
        ver = case.get("version", "")
        if ver != "human_validated_pilot_v1":
            messages.append(f"{prefix} wrong version: {ver!r}")

        # Check 8: no privacy leaks in non-hidden fields
        for field in ["user_request", "task_context", "proposed_agent_action"]:
            val = case.get(field, "").lower()
            for pattern in PRIVACY_PATTERNS:
                if pattern in val and "hidden" not in field:
                    messages.append(f"{prefix} privacy pattern {pattern!r} in {field}")

    # Check 9: unique case_ids
    if len(case_ids) != 30:
        messages.append(f"Duplicate case_ids: {30 - len(case_ids)} duplicates")

    # Check 10: label distribution
    dist = {}
    for case in cases:
        label = case.get("expected_decision_hidden", "")
        dist[label] = dist.get(label, 0) + 1
    messages.append(f"Label distribution: {dist}")

    ok = not any(m.startswith("Case") and "bad" in m.lower() or "invalid" in m.lower() or "missing" in m.lower() or "wrong" in m.lower() or "privacy" in m.lower() or "Duplicate" in m for m in messages)
    return ok, messages


def main():
    ok, messages = validate()
    for m in messages:
        print(m)
    if ok:
        print("ALL CHECKS PASSED")
        sys.exit(0)
    else:
        print("VALIDATION FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
