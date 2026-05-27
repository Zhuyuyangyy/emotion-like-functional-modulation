# Phase 3: Annotation Reliability Summary

## What Was Produced

1. **`annotation_protocol_v1.md`**: Defines labels, priority rules, edge cases, and examples.
2. **`blind_annotation_sample_100.csv`**: 100-case blind sample (60 from Semi-Real-300, 40 from External-Style-150) with annotator fields left empty.
3. **`annotation_reliability_plan.md`**: Details dual-annotation workflow, dispute resolution, and acceptance criteria.
4. **`compute_kappa.py`**: Tool to calculate Cohen's kappa and confusion matrix from completed annotations.
5. **`generate_blind_sample.py`**: Script to generate the blind sample (reproducible with seed=42).

## Next Steps

Before submitting the paper, we recommend:
- Completing dual-annotation of `blind_annotation_sample_100.csv`.
- Resolving disputes as per the plan.
- Calculating kappa using `compute_kappa.py`.
- If kappa is < 0.60, revising the protocol or sample and re-annotating.
- Including the kappa result in the paper.

## Note

- **No real dual-annotation results have been produced yet.**
- **No inter-annotator agreement calculations have been performed yet.**
