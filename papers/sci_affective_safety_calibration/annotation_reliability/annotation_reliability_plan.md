# Annotation Reliability Plan

## 1. Dual-Annotation Workflow

- **Annotators**: Two independent annotators will label the 100-case blind sample.
- **Guidance**: Annotators will use `annotation_protocol_v1.md` for label definitions, priority rules, and edge case handling.
- **Blinding**: Annotators will not have access to gold decisions or model predictions.
- **Tooling**: Annotators will fill in `annotator_label` and `annotator_rationale` columns in `blind_annotation_sample_100.csv`.

## 2. Dispute Resolution Rules

- For cases where annotators disagree:
  1. Both annotators will independently review their decisions and the protocol.
  2. They will discuss the case to reach a consensus.
  3. If consensus cannot be reached, a third (tiebreaker) annotator will review and make the final decision.
  4. All dispute resolutions will be documented.

## 3. Cohen's Kappa Calculation Method

Cohen's kappa will be calculated to measure inter-annotator agreement:
- Observed agreement (Po): proportion of cases where annotators agree.
- Expected agreement (Pe): proportion of agreement expected by chance.
- Kappa = (Po - Pe) / (1 - Pe).
- We will use `compute_kappa.py` to calculate kappa and the confusion matrix.

## 4. Acceptance Criteria

- **Strong agreement**: κ ≥ 0.75
- **Acceptable agreement**: 0.60 ≤ κ < 0.75
- **Needs revision**: κ < 0.60 (protocol or sample may need adjustment)

## 5. Current Status

- ✅ Annotation protocol ready (`annotation_protocol_v1.md`)
- ✅ Blind sample ready (`blind_annotation_sample_100.csv`)
- ✅ Kappa calculation tool ready (`compute_kappa.py`)
- ⏳ Human annotation pending
