# Q2 Blocker Closure Report

**Date**: 2026-05-28
**Phase**: Post Phase 0–4, Pre Phase 5

---

## 1. LLM Baseline Status

**Status: CLOSED — Real result obtained ✅**

### Execution Details

| Parameter | Value |
|-----------|-------|
| Model | deepseek-v4-flash (deepseek-chat) |
| Provider | DeepSeek |
| API Base | https://api.deepseek.com/v1 |
| Date | 2026-05-28 |
| Temperature | 0.0 |
| Prompt Version | v1.0 |
| Total Samples | 100 (100-case subset) |
| Parse Success | 100 (0 failures) |
| Total Retries | 0 |
| Cost (USD) | $0.0071 |

### Core Metrics

| Metric | Value |
|--------|------:|
| Action Accuracy | 0.240 |
| Risky Auto-Execution Rate | 0.000 |
| False Caution Rate | 1.000 |
| Safe Auto-Execution Rate | 0.000 |
| Composite Score | 0.472 |

### Prediction Distribution

| Label | Count | Percentage |
|-------|------:|-----------:|
| HUMAN_REVIEW | 96 | 96% |
| BLOCK | 4 | 4% |
| AUTO_EXECUTE | 0 | 0% |
| SIMULATE_FIRST | 0 | 0% |

### Updated Comparison Table

| Method | Action Acc | Risky Auto-Exec | False Caution | Safe Auto-Exec | Composite |
|--------|----------:|----------------:|--------------:|---------------:|----------:|
| FullCalibratorAdapter | 0.753 | 0.036 | 0.122 | 0.757 | 0.860 |
| **LLMSafetyJudgeBaseline** | **0.240** | **0.000** | **1.000** | **0.000** | **0.472** |
| KeywordRuleBaseline | 0.460 | 0.780 | 0.000 | 1.000 | 0.553 |
| SafeKeywordFirstBaseline | 0.417 | 0.872 | 0.000 | 1.000 | 0.507 |
| RiskContextOracleBaseline* | 0.510 | 0.064 | 0.000 | 1.000 | 0.784 |

* Structured oracle / upper-bound diagnostic baseline, not deployable.

### Key Finding

Under the tested zero-shot prompt and DeepSeek-v4-flash setting, the LLM safety judge exhibited extreme over-escalation: 96% of samples classified as HUMAN_REVIEW, 4% as BLOCK, 0% as AUTO_EXECUTE or SIMULATE_FIRST. This resulted in:
- Perfect risk avoidance (risky auto-exec = 0.000) but total operational paralysis (false caution = 1.000)
- No discrimination between risk levels — safe and risky operations treated identically
- Composite score (0.472) below even the keyword baselines (0.507–0.553)

This finding suggests that structured calibration better balances safety and utility than a zero-shot LLM safety judge under this specific tested setting. The FullCalibratorAdapter preserved safe auto-execution better than the zero-shot LLM judge.

### Output Files

| File | Path |
|------|------|
| Raw outputs | [experiments/results/llm_baseline/llm_safety_judge_raw_outputs.jsonl](file:///workspace/experiments/results/llm_baseline/llm_safety_judge_raw_outputs.jsonl) |
| Predictions | [experiments/results/llm_baseline/llm_safety_judge_predictions.json](file:///workspace/experiments/results/llm_baseline/llm_safety_judge_predictions.json) |
| Metrics | [experiments/results/llm_baseline/llm_safety_judge_metrics.json](file:///workspace/experiments/results/llm_baseline/llm_safety_judge_metrics.json) |
| Gold labels | [experiments/results/llm_baseline/gold_labels.json](file:///workspace/experiments/results/llm_baseline/gold_labels.json) |
| Full report | [papers/sci_affective_safety_calibration/llm_baseline_report.md](file:///workspace/papers/sci_affective_safety_calibration/llm_baseline_report.md) |

---

## 2. Annotation Reliability Status

**Status: PENDING**

No Cohen's kappa is reported because no independent second annotation has been completed yet.

### What Has Been Prepared

| Artifact | Path | Status |
|----------|------|--------|
| Blind sample (100) | [papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100.csv](file:///workspace/papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100.csv) | Ready (annotator_label and annotator_rationale EMPTY) |
| Annotation protocol v1 | [papers/sci_affective_safety_calibration/annotation_reliability/annotation_protocol_v1.md](file:///workspace/papers/sci_affective_safety_calibration/annotation_reliability/annotation_protocol_v1.md) | Ready |
| Annotator 2 task pack | [papers/sci_affective_safety_calibration/annotation_reliability/annotator_2_task_pack.md](file:///workspace/papers/sci_affective_safety_calibration/annotation_reliability/annotator_2_task_pack.md) | Ready |
| Annotator 2 instructions | [papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/annotation_instructions_for_annotator.md](file:///workspace/papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/annotation_instructions_for_annotator.md) | Ready |
| Annotator 2 blank CSV | [papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/blind_annotation_sample_100.csv](file:///workspace/papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/blind_annotation_sample_100.csv) | Ready |
| Hidden gold reference | [papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100_with_gold_hidden_reference.csv](file:///workspace/papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100_with_gold_hidden_reference.csv) | Ready (NOT for distribution to annotators) |
| Gold reference JSON | [experiments/annotation/gold_reference_hidden.json](file:///workspace/experiments/annotation/gold_reference_hidden.json) | Ready |
| Kappa computation script | [experiments/annotation/compute_kappa.py](file:///workspace/experiments/annotation/compute_kappa.py) | Ready |
| Pending report | [papers/sci_affective_safety_calibration/annotation_reliability/annotation_reliability_pending_report.md](file:///workspace/papers/sci_affective_safety_calibration/annotation_reliability/annotation_reliability_pending_report.md) | Ready |

### Verification: Blind Sample Integrity

Confirmed ✓:
- `annotator_label` column is EMPTY
- `annotator_rationale` column is EMPTY
- Does NOT contain `gold_decision`
- Does NOT contain any model prediction
- Does NOT contain `expected_decision`
- Gold reference is kept separate and not in annotator-facing files

### How to Close This Blocker

1. Provide the [for_annotator_2](file:///workspace/papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/) package to an independent annotator
2. Annotator completes `annotator_2_completed.csv`
3. Run: `python experiments/annotation/compute_kappa.py --gold <gold_ref> --annotator <completed> --output <results>`
4. Report Cohen's kappa in the manuscript

---

## 3. Phase 5 Entry Decision

**Recommendation: BORDERLINE — Can enter Phase 5 with caveats ✅**

The LLM baseline blocker is now closed. The annotation kappa blocker remains pending. Given that:
- LLM baseline is a real, valuable result that addresses the primary reviewer concern
- The LLM baseline finding strongly supports the paper's argument
- Annotation reliability is pending, but can be noted appropriately in the manuscript

Proceeding to Phase 5 is acceptable, provided the manuscript honestly notes that independent annotation reliability is not yet established.

---

## 4. Q2 Readiness Assessment

| Blocker | Status | Impact on Q2 |
|---------|--------|-------------|
| LLM Baseline | **CLOSED ✅** | Addressed — real comparison with DeepSeek-v4-flash on 100-case subset |
| Annotation Kappa | PENDING | Important but not blocking — manuscript can note pending reliability |

**Overall Q2 Readiness: BORDERLINE**

- LLM baseline: Real result on 100-case subset obtained ✅
- Annotation kappa: Pending (no second annotator yet)

---

## 5. Q2 Readiness Levels (Reference)

| Level | Condition | Implication |
|-------|-----------|------------|
| **READY** | LLM baseline real result + kappa completed | Q2 submission viable |
| **BORDERLINE** | LLM baseline real result, kappa pending | Q2 possible with caveat about pending reliability |
| **WEAK** | LLM baseline protocol-only + kappa pending | Q2 not recommended; target Q3 first |

**Current level: BORDERLINE**

---

## 6. Next Steps

### Priority 1: Close Annotation Kappa (Upgrade to READY)

- Find an independent annotator (domain knowledge preferred but not required)
- Provide the [annotator_2_task_pack.md](file:///workspace/papers/sci_affective_safety_calibration/annotation_reliability/annotator_2_task_pack.md) and associated files
- Expected time: 1.5–3 hours of annotation + computation
- This would upgrade Q2 readiness from BORDERLINE to READY

### Priority 2: Enter Phase 5

- With BORDERLINE readiness, Phase 5 is now acceptable
- Write v0.4 manuscript incorporating the LLM baseline comparison
- Note clearly in the manuscript: "100-case subset" (not full 300) and "No independent annotation reliability established yet"
- Use appropriate language for the LLM baseline finding (avoid absolute conclusions)

---

## 7. Current Submission Target Recommendation

| Target | Recommendation |
|--------|---------------|
| SCI Q2 | **Attempt viable** — LLM baseline closed (100-case), kappa pending but manageable with proper caveats |
| SCI Q3 | **Strong position** — all baselines present, analysis solid |
| EI | **Already sufficient** |

**Primary recommendation: Q2 attempt is viable. Close annotation kappa to upgrade to READY.**

---

## 8. Verification Summary

| Check | Result |
|-------|--------|
| Was main framework code modified? | **No** — only new files under [experiments/](file:///workspace/experiments/) and [papers/](file:///workspace/papers/) |
| Were any experimental results fabricated? | **No** — LLM baseline is a real API call result |
| Is blind sample integrity preserved? | **Yes** — no gold labels leaked to annotator-facing files |
| Is gold reference kept separate? | **Yes** — hidden reference not in annotator-facing files |
| Can kappa be computed once data is available? | **Yes** — [compute_kappa.py](file:///workspace/experiments/annotation/compute_kappa.py) is ready |
| Was LLM baseline run with real API? | **Yes** — DeepSeek API, 100 samples, 0 parse failures |
