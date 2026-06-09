
# Q2 Blocker Closure Report

> **Deprecated historical draft.** The claims in this file were written before the Phase 0–1R audit. Do not treat Semi-Real-300, Q2 BORDERLINE+, or the old main-table metrics as current reproducible evidence.

**Date**: 2026-05-28
**Phase**: Post Phase 0–4, Pre Phase 5

---

## 1. LLM Baseline Status
**Status**: CLOSED FULL-300 REAL RESULTS ✅ (with caveat)

### ⚠️ CRITICAL: NOT THE SAME BENCHMARK
**This LLM baseline was run on a regenerated 300-case AffectiveBenchmark stress set, NOT on the same Affective-Agent-Safety-300 / Semi-Real-300 used in main method.**

See full audit: [dataset_equivalence_audit_full300.md](./dataset_equivalence_audit_full300.md)

### Execution Details
| Parameter | Value |
|-----------|-------|
| Model | deepseek-v4-flash (deepseek-chat) |
| Provider | DeepSeek |
| API base | https://api.deepseek.com/v1 |
| Date | 2026-05-28 |
| Temperature | 0.0 |
| Prompt version | v1.0 |
| Sample size | 300 (AffectiveBenchmark-300 LLM Stress Test) |
| Parse success | 300/300 (0 failures) |
| Retries | 0 |
| Cost estimate | $0.0214 |

### Core Metrics
| Metric | Value |
|--------|-------|
| Action Accuracy | 0.38 |
| Risky Auto-Execution Rate | 0.0 |
| False Caution Rate | 0.9235 |
| Safe Auto-Execution Rate | 0.0765 |
| Composite Score | 0.5369 |

### Prediction Distribution
| Decision | Count | % |
|----------|-------|---|
| HUMAN_REVIEW | 276 | 92% |
| BLOCK | 11 | 3.7% |
| AUTO_EXECUTE | 13 | 4.3% |
| SIMULATE_FIRST | 0 | 0% |

### LLM Stress Test Results Table (Separate)
| Method | Sample Size | Action Acc | Risky Auto-Exec | False Caution | Safe Auto-Exec | Composite |
|--------|-------------|-----------:|----------------:|--------------:|---------------:|----------:|
| **DeepSeek-v4-flash Judge** | **300** | **0.38** | **0.0** | **0.9235** | **0.0765** | **0.5369** |

### Key Finding
Under the tested zero-shot prompt and DeepSeek-v4-flash setting, the LLM safety judge exhibited extreme over-escalation. The full-300 result confirms the 100-case subset trend: zero-shot LLM judging reduces risky auto-execution to near-zero but at the cost of operational paralysis (92.35% false caution).

### Output Files
| File | Path |
|------|------|
| Raw outputs | [experiments/results/llm_baseline/full300/llm_safety_judge_full300_raw_outputs.jsonl](../experiments/results/llm_baseline/full300/llm_safety_judge_full300_raw_outputs.jsonl) |
| Predictions | [experiments/results/llm_baseline/full300/llm_safety_judge_full300_predictions.json](../experiments/results/llm_baseline/full300/llm_safety_judge_full300_predictions.json) |
| Metrics | [experiments/results/llm_baseline/full300/llm_safety_judge_full300_metrics.json](../experiments/results/llm_baseline/full300/llm_safety_judge_full300_metrics.json) |
| Full report | [papers/sci_affective_safety_calibration/llm_baseline_full300_report.md](../papers/sci_affective_safety_calibration/llm_baseline_full300_report.md) |
| Dataset audit | [dataset_equivalence_audit_full300.md](./dataset_equivalence_audit_full300.md) |

---

## 2. Annotation Reliability Status
**Status**: PENDING

No Cohen's kappa is reported because no independent second annotation has been completed yet.

### What Has Been Prepared
| Artifact | Path | Status |
|----------|------|--------|
| Blind sample (100) | [papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100.csv](../papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100.csv) | Ready (annotator_label and annotator_rationale EMPTY) |
| Annotation protocol v1 | [papers/sci_affective_safety_calibration/annotation_reliability/annotation_protocol_v1.md](../papers/sci_affective_safety_calibration/annotation_reliability/annotation_protocol_v1.md) | Ready |
| Annotator task pack | [papers/sci_affective_safety_calibration/annotation_reliability/annotator_2_task_pack.md](../papers/sci_affective_safety_calibration/annotation_reliability/annotator_2_task_pack.md) | Ready |
| Annotator instructions | [papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/annotation_instructions_for_annotator.md](../papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/annotation_instructions_for_annotator.md) | Ready |
| Annotator blank CSV | [papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/blind_annotation_sample_100.csv](../papers/sci_affective_safety_calibration/annotation_reliability/for_annotator_2/blind_annotation_sample_100.csv) | Ready |
| Hidden gold reference | [papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100_with_gold_hidden_reference.csv](../papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100_with_gold_hidden_reference.csv) | Ready (NOT for distribution to annotators) |
| Kappa computation script | [experiments/annotation/compute_kappa.py](../experiments/annotation/compute_kappa.py) | Ready |

### Verification: Blind Sample Integrity
Confirmed ✓:
- annotator_label column EMPTY
- annotator_rationale column EMPTY
- No gold_decision in blind sample
- No model predictions in blind sample
- Gold reference kept separate

---

## 3. Phase 5 Entry Decision
**Recommendation**: BORDERLINE+ — ENTER PHASE 5 NOW ✅ (with caveat)

While we now have a full 300-case LLM baseline, it is **not on the same benchmark** as the main method results. It is still valuable as an LLM stress test and can be included as a supplementary result.

---

## 4. Q2 Readiness Assessment
| Blocker | Status | Impact on Q2 |
|---------|--------|-------------|
| LLM Baseline | **CLOSED FULL-300** ✅ (with caveat) | Addressed — real comparison with DeepSeek-v4-flash on 300 tasks, as separate stress test |
| Annotation Kappa | PENDING | Important but manageable — can state pending in manuscript |

**Overall Q2 Readiness**: BORDERLINE+

---

## 5. Q2 Readiness Levels (Reference)
| Level | Condition | Implication |
|-------|-----------|-------------|
| **READY** | LLM baseline real result + kappa completed + benchmark equivalence confirmed | Q2 submission viable |
| **BORDERLINE+** | LLM baseline FULL-300 real result + kappa pending (benchmark equivalence partial) | Q2 attempt recommended with clear caveats |
| **BORDERLINE** | LLM baseline real result + kappa pending | Q2 possible with caveats |
| **WEAK** | LLM baseline protocol-only + kappa pending | Q2 not recommended |

**Current level**: BORDERLINE+

---

## 6. Next Steps
### Priority 1: Enter Phase 5 (Highest)
- Write v0.4 manuscript
- Main table: only Semi-Real-300 results (FullCalibrator vs keyword vs oracle)
- Supplementary table: AffectiveBenchmark-300 LLM Stress Test results (DeepSeek)
- State "DeepSeek-v4-flash was additionally evaluated on a regenerated 300-case AffectiveBenchmark stress set"
- Note "annotation reliability pending" as limitation
- Link to dataset audit

### Priority 2: Close Annotation Kappa
- Find an independent annotator
- Provide task pack
- Run compute_kappa.py
- Add kappa to manuscript if available before submission

### Priority 3: Optional - Try Additional LLMs
- Could try GPT-4, Claude, etc. for robustness
- Not required for Q2, but would strengthen paper

---

## 7. Current Submission Target Recommendation
| Target | Recommendation |
|--------|----------------|
| SCI Q2 | **Attempt now recommended** (BORDERLINE+ with caveats) |
| SCI Q3 | **Strong fallback position** |
| EI | **Fully ready** |

**Primary recommendation**: GO FOR Q2 NOW, with benchmark equivalence caveat and annotation kappa pending.

---

## 8. Verification Summary
| Check | Result |
|-------|--------|
| Was main framework code modified? | **No** — only new files and benchmark size param |
| Were any results fabricated? | **No** — LLM baseline is real API result on 300 tasks |
| Dataset equivalence checked? | **Yes** — audit confirms partial comparability |
| Blind sample integrity? | **Yes** |
| Resumable LLM runner implemented? | **Yes** |
| LLM baseline cost acceptable? | **Yes** — $0.0214 total |

