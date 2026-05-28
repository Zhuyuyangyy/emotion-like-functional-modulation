# Annotation Reliability — Pending Report

## Status

**PENDING** — No Cohen's kappa is reported because no independent second annotation has been completed.

## What Has Been Prepared

### 1. Blind Annotation Sample

File: `annotation_reliability/blind_annotation_sample_100.csv`

- 100 randomly sampled benchmark tasks
- Columns: sample_id, task_description, category, risk_context, annotator_label, annotator_rationale
- `annotator_label` and `annotator_rationale` are EMPTY (to be filled by annotator)
- Does NOT contain: gold_decision, model prediction, expected_decision

### 2. Annotation Protocol

File: `annotation_reliability/annotation_protocol_v1.md`

- Four-label system: AUTO_EXECUTE, SIMULATE_FIRST, HUMAN_REVIEW, BLOCK
- Priority rules for edge cases
- Explicit prohibitions against referencing model output or gold labels

### 3. Annotator 2 Package

Directory: `annotation_reliability/for_annotator_2/`

Contains:
- `blind_annotation_sample_100.csv` — the blank annotation form
- `annotation_instructions_for_annotator.md` — detailed instructions
- `annotation_protocol_v1.md` — to be copied from parent directory

Expected output: `annotator_2_completed.csv`

### 4. Hidden Gold Reference

File: `annotation_reliability/blind_annotation_sample_100_with_gold_hidden_reference.csv`

- Contains gold_decision column
- NOT distributed to annotators
- Used as reference in kappa computation

### 5. Kappa Computation Script

File: `experiments/annotation/compute_kappa.py`

Usage:
```bash
python compute_kappa.py \
  --gold papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100_with_gold_hidden_reference.csv \
  --annotator papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/annotator_2_completed.csv \
  --output experiments/results/annotation/annotation_agreement_results.json
```

If the gold reference or annotator file is missing, the script outputs a clear error message.

## What Is Missing

1. **No independent second annotator has completed the 100-sample annotation**
2. Therefore, no Cohen's kappa can be computed
3. No inter-annotator agreement statistics are available

## Recommendations

1. Random 100 cases are ready for independent annotation at: `annotation_reliability/for_annotator_2/`
2. The current manuscript should describe labels as **structured benchmark labels**, not expert-consensus labels
3. Once a second annotator completes the annotation, run `compute_kappa.py` to obtain agreement metrics
4. A kappa ≥ 0.67 would support the "substantial agreement" claim; κ ≥ 0.80 would support "almost perfect agreement"

## Manuscript Language Guidance

Until kappa is available, use language such as:

> "Labels were derived from a structured annotation protocol based on risk-level heuristics. Independent inter-annotator agreement (Cohen's κ) is pending and will be reported in a subsequent version."

Do NOT claim:
- "Expert consensus labels"
- "High inter-annotator agreement"
- "Validated by multiple annotators"
