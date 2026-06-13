# Phase 2 Status Report

**Date**: 2026-06-09
**Branch**: `phase-2-human-pilot30`
**Current Status**: **AWAITING_ANNOTATION**

---

## Completed Files

| File | Description |
|------|-------------|
| `data/human_validated/annotation_guideline_v2.md` | Annotation guideline with label definitions, risk taxonomy, conflict rules, annotator rules |
| `data/human_validated/pilot30_cases.json` | 30 pilot cases for human annotation |
| `data/human_validated/annotator_A_pilot30.csv` | Blank annotation sheet for annotator A |
| `data/human_validated/annotator_B_pilot30.csv` | Blank annotation sheet for annotator B |
| `experiments/human_validation/validate_pilot30_cases.py` | Validation script for pilot30 data |
| `experiments/human_validation/generate_blind_annotation_sheets.py` | Script to generate blind annotation CSVs |
| `experiments/human_validation/compute_pilot_kappa.py` | Script to compute Cohen's kappa (requires completed annotations) |
| `results/human_validation/pilot30_validation_report.json` | Validation report output |

---

## Pilot-30 Data Source

All 30 cases are derived from one of four source types:
- **public_issue_derived**: Scenarios inspired by publicly reported AI agent safety issues
- **public_security_scenario_derived**: Scenarios derived from public security advisories
- **handcrafted_agent_failure_case**: Handcrafted scenarios based on known agent failure modes
- **low_risk_control**: Low-risk routine scenarios included as controls

**No private user data, real chat logs, internal company data, personal emails, or real credentials are included.**

---

## Why We Cannot Claim "Human-Validated" Now

1. No human annotator has completed any annotation yet.
2. Both annotation sheets are blank (annotator_label, annotator_rationale, uncertainty_flag are empty).
3. Cohen's kappa has not been computed - it requires two completed independent annotations.
4. The `expected_decision_hidden` field is only a reference for future arbitration, not a validated label.
5. Until dual annotation is completed and kappa is computed, the pilot30 data is **not human-validated**.

---

## Why We Cannot Run Model Evaluation Now

1. There are no final labels to evaluate against.
2. Running model evaluation on `expected_decision_hidden` would be circular - those are heuristic labels, not human labels.
3. Model evaluation must wait until human-validated labels are available.

---

## Next Required Human Action

To proceed past AWAITING_ANNOTATION, the following must be provided:

1. **`annotator_A_pilot30_completed.csv`** - The annotator A sheet with all `annotator_label` and `annotator_rationale` fields filled in by an independent human annotator.
2. **`annotator_B_pilot30_completed.csv`** - The annotator B sheet with all `annotator_label` and `annotator_rationale` fields filled in by a second independent human annotator.

Once both files are placed in `data/human_validated/`, run:
```bash
python experiments/human_validation/compute_pilot_kappa.py
```

---

## Prohibited Actions

- Do NOT fill in annotation labels yourself (agent/auto-fill).
- Do NOT generate fake completed annotation files.
- Do NOT claim the dataset is "human-validated" until kappa is computed.
- Do NOT run model evaluation against `expected_decision_hidden`.
- Do NOT generate `final_label` without human arbitration.
- Do NOT proceed to Human-Validated-100 until pilot30 kappa is acceptable.
