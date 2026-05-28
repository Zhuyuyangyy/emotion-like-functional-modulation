# Q2 Blocker Closure Report

**Date**: 2026-05-28
**Phase**: Post Phase 0–4, Pre Phase 5

---

## 1. LLM Baseline Status

**Status: PROTOCOL-ONLY**

No real LLM baseline result is reported because no authorized model/API was available.

### What was checked

| Provider | Environment Variable | Status |
|----------|---------------------|--------|
| OpenAI | OPENAI_API_KEY | Not set |
| DeepSeek | DEEPSEEK_API_KEY | Not set |
| DashScope | DASHSCOPE_API_KEY | Not set |
| Qwen | QWEN_API_KEY | Not set |

### What was prepared

| Artifact | Path | Status |
|----------|------|--------|
| Prompt template (v1.0) | `experiments/llm_baseline/prompts/llm_safety_judge_prompt.md` | Ready |
| Baseline implementation | `experiments/llm_baseline/llm_safety_judge_baseline.py` | Ready |
| Runner script | `experiments/llm_baseline/run_llm_safety_judge_baseline.py` | Ready |
| Parse script | `experiments/llm_baseline/parse_llm_judge_output.py` | Ready |
| Evaluate script | `experiments/llm_baseline/evaluate_llm_judge_baseline.py` | Ready |
| Protocol-only status | `experiments/results/llm_baseline/llm_safety_judge_protocol_status.json` | Generated |
| Protocol-only report | `papers/sci_affective_safety_calibration/llm_baseline_protocol_only.md` | Generated |

### How to close this blocker

1. Obtain an API key for any supported provider
2. Run: `python experiments/llm_baseline/run_llm_safety_judge_baseline.py --provider <provider> --model <model>`
3. Evaluate against gold: `python experiments/llm_baseline/evaluate_llm_judge_baseline.py --predictions <pred> --gold <gold> --output <metrics>`
4. Update the comparison table with real metrics

---

## 2. Annotation Reliability Status

**Status: PENDING**

No Cohen's kappa is reported because no independent second annotation has been completed.

### What was prepared

| Artifact | Path | Status |
|----------|------|--------|
| Blind sample (100) | `annotation_reliability/blind_annotation_sample_100.csv` | Ready (annotator_label EMPTY) |
| Annotation protocol v1 | `annotation_reliability/annotation_protocol_v1.md` | Ready |
| Annotator 2 instructions | `annotation_reliability/for_annotator_2/annotation_instructions_for_annotator.md` | Ready |
| Annotator 2 blank CSV | `annotation_reliability/for_annotator_2/blind_annotation_sample_100.csv` | Ready |
| Hidden gold reference | `annotation_reliability/blind_annotation_sample_100_with_gold_hidden_reference.csv` | Ready (NOT for distribution) |
| Gold reference JSON | `experiments/annotation/gold_reference_hidden.json` | Ready |
| Kappa computation script | `experiments/annotation/compute_kappa.py` | Ready |
| Pending report | `annotation_reliability/annotation_reliability_pending_report.md` | Generated |

### Verification: blind sample integrity

- `annotator_label`: EMPTY ✓
- `annotator_rationale`: EMPTY ✓
- Does NOT contain `gold_decision` ✓
- Does NOT contain model prediction ✓
- Does NOT contain `expected_decision` ✓

### How to close this blocker

1. Provide the `for_annotator_2/` package to an independent annotator
2. Annotator completes `annotator_2_completed.csv`
3. Run: `python experiments/annotation/compute_kappa.py --gold <gold_ref> --annotator <completed> --output <results>`
4. Report Cohen's kappa in the manuscript

---

## 3. Phase 5 Entry Decision

**Recommendation: DO NOT enter Phase 5 yet.**

Both Q2 blockers remain open. Proceeding to Phase 5 (writing v0.4 manuscript) without closing at least the LLM baseline would weaken the paper against reviewer scrutiny.

---

## 4. Q2 Readiness Assessment

| Blocker | Status | Impact on Q2 |
|---------|--------|-------------|
| LLM Baseline | GAP / protocol-only | Critical — reviewers will ask "why no LLM comparison?" |
| Annotation Kappa | PENDING | Important — reviewers will ask "how reliable are your labels?" |

**Overall Q2 Readiness: WEAK**

- LLM baseline: protocol-only (no real result)
- Annotation kappa: pending (no second annotator)

---

## 5. Q2 Readiness Levels (Reference)

| Level | Condition | Implication |
|-------|-----------|------------|
| **READY** | LLM baseline real result + kappa completed | Q2 submission viable |
| **BORDERLINE** | LLM baseline real result, kappa pending | Q2 possible with caveat on label reliability |
| **WEAK** | LLM baseline protocol-only + kappa pending | Q2 not recommended; target Q3 first |

**Current level: WEAK**

---

## 6. Next Steps

### Priority 1: Close LLM Baseline (highest impact)

- Obtain API key (even a single provider is sufficient)
- Run the prepared script on Affective-Agent-Safety-300
- A single model (e.g., GPT-4, DeepSeek-V3, Qwen-Max) is enough for Q2
- Expected time: ~1 hour of API calls + evaluation

### Priority 2: Close Annotation Kappa

- Find an independent annotator (domain knowledge preferred but not required)
- Provide the `for_annotator_2/` package
- Expected time: ~2-3 hours of annotation + computation

### Priority 3: Then enter Phase 5

- Once at least the LLM baseline is closed (BORDERLINE or READY), proceed to Phase 5–7

---

## 7. Current Submission Target Recommendation

| Target | Recommendation |
|--------|---------------|
| SCI Q2 | **Defer** until both blockers are closed |
| SCI Q3 | **Viable now** — the framework, baselines, and analysis are sufficient for Q3 |
| EI | **Already sufficient** |

**Primary recommendation: SCI Q3 first, Q2 attempt after blocker closure.**

---

## 8. Verification Summary

| Check | Result |
|-------|--------|
| Was main framework code modified? | **No** — only new files under `experiments/` and `papers/` |
| Were any experimental results fabricated? | **No** — all outputs are protocol-only or pending |
| Is the blind sample integrity preserved? | **Yes** — no gold labels leaked to annotator package |
| Is the gold reference kept separate? | **Yes** — hidden reference not in annotator package |
| Can kappa be computed once data is available? | **Yes** — script is ready |
| Can LLM baseline be run once API is available? | **Yes** — all scripts and prompts are ready |
