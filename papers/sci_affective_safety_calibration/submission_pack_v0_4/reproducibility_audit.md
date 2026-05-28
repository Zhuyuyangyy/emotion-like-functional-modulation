# Reproducibility Audit

**Date**: 2026-05-28
**Version**: v0.4
**Paper**: Experience-Shaped Affective Safety Calibration for Autonomous Agents

---

## 1. Key Commands

### 1.1 Benchmark Generation (AffectiveBenchmark-300)
```bash
cd /workspace
python -c "
from emotion_agent.affective_benchmark import AffectiveBenchmark
b = AffectiveBenchmark(seed=42, size=300)
print(f'Generated {len(b.tasks)} tasks')
"
```

### 1.2 LLM Judge Input Preparation
```bash
cd /workspace
python experiments/llm_baseline/prepare_full300_llm_inputs.py
```

### 1.3 DeepSeek-v4-flash LLM Safety Judge Baseline (Full-300)
```bash
cd /workspace
DEEPSEEK_API_KEY=<key> python experiments/llm_baseline/run_deepseek_full300_baseline.py
```

### 1.4 DeepSeek-v4-flash LLM Safety Judge Baseline (100-case)
```bash
cd /workspace
DEEPSEEK_API_KEY=<key> python experiments/llm_baseline/run_deepseek_baseline.py
```

### 1.5 Blind Annotation Sample Generation
```bash
cd /workspace
python experiments/annotation/generate_blind_sample.py
```

### 1.6 Gold Reference Generation
```bash
cd /workspace
python experiments/annotation/generate_gold_reference.py
```

### 1.7 Cohen's Kappa Computation (requires completed annotator CSV)
```bash
cd /workspace
python experiments/annotation/compute_kappa.py \
    --gold experiments/annotation/gold_reference_hidden.json \
    --annotator <path_to_annotator_2_completed.csv> \
    --output experiments/annotation/kappa_results.json
```

---

## 2. Result Files

### 2.1 Full-300 LLM Baseline
| File | Path |
|------|------|
| LLM judge inputs | `experiments/results/llm_baseline/full300/llm_judge_inputs.json` |
| Gold labels | `experiments/results/llm_baseline/full300/gold_labels.json` |
| Raw outputs | `experiments/results/llm_baseline/full300/llm_safety_judge_full300_raw_outputs.jsonl` |
| Predictions | `experiments/results/llm_baseline/full300/llm_safety_judge_full300_predictions.json` |
| Metrics | `experiments/results/llm_baseline/full300/llm_safety_judge_full300_metrics.json` |
| Failures | `experiments/results/llm_baseline/full300/llm_safety_judge_full300_failures.json` |

### 2.2 100-case LLM Baseline
| File | Path |
|------|------|
| Gold labels | `experiments/results/llm_baseline/gold_labels.json` |
| Raw outputs | `experiments/results/llm_baseline/llm_safety_judge_raw_outputs.jsonl` |
| Predictions | `experiments/results/llm_baseline/llm_safety_judge_predictions.json` |
| Metrics | `experiments/results/llm_baseline/llm_safety_judge_metrics.json` |

### 2.3 Annotation Materials
| File | Path |
|------|------|
| Blind sample (100) | `experiments/annotation/blind_annotation_sample_100.csv` |
| Gold reference (CSV) | `experiments/annotation/blind_annotation_sample_100_with_gold_hidden_reference.csv` |
| Gold reference (JSON) | `experiments/annotation/gold_reference_hidden.json` |

---

## 3. Tests Passed

### 3.1 DeepSeek Full-300 Baseline
| Check | Result |
|-------|--------|
| Parse success | 300/300 (0 failures) |
| Retries | 0 |
| Cost estimate | $0.0214 |
| All 300 cases have predictions | ✅ |
| All predictions in valid label space | ✅ |

### 3.2 DeepSeek 100-case Baseline
| Check | Result |
|-------|--------|
| Parse success | 100/100 |
| All predictions valid | ✅ |

### 3.3 Benchmark Generation
| Check | Result |
|-------|--------|
| AffectiveBenchmark(seed=42, size=100) generates 100 tasks | ✅ |
| AffectiveBenchmark(seed=42, size=300) generates 300 tasks | ✅ |
| Deterministic with same seed | ✅ |

---

## 4. Random Seed

| Component | Seed |
|-----------|------|
| AffectiveBenchmark task generation | 42 |
| Blind annotation sampling | 42 |
| DeepSeek API calls | temperature=0.0 (deterministic) |

---

## 5. Key Metrics (DeepSeek Full-300 LLM Stress Test)

| Metric | Value |
|--------|-------|
| Action Accuracy | 0.38 |
| Risky Auto-Execution Rate | 0.0 |
| False Caution Rate | 0.9235 |
| Safe Auto-Execution Rate | 0.0765 |
| Composite Score | 0.5369 |

---

## 6. DeepSeek Baseline Execution Status

| Question | Answer |
|----------|--------|
| Was the DeepSeek baseline actually run? | ✅ Yes — real API calls to DeepSeek |
| Are raw outputs available? | ✅ Yes — `llm_safety_judge_full300_raw_outputs.jsonl` |
| Are metrics computed from real outputs? | ✅ Yes |
| Was it run on the same Semi-Real-300? | ❌ No — on regenerated AffectiveBenchmark-300 |
| Can it be mixed into the main table? | ❌ No — separate auxiliary stress test only |

---

## 7. Main Framework Not Modified

| Check | Status |
|-------|--------|
| `emotion_agent/affective_benchmark.py` modified for this audit? | No changes beyond the size parameter extension (pre-existing) |
| Main experiment code modified? | No |
| Results fabricated or post-hoc adjusted? | No |

---

## 8. Known Gaps

| Gap | Status | Impact |
|-----|--------|--------|
| Original Semi-Real-300 source JSON not in repository | Known | Cannot re-run main method on identical data |
| Cohen's kappa not computed | Pending | Annotation reliability unverified |
| No independent second annotation completed | Pending | Single-annotator labels only |
| No real-world deployment validation | Permanent limitation | Generalization claim limited |
| Main method results not re-run from code | Known | Reported from prior work, not from current repo execution |

---

## 9. Reproducibility Verdict

**PARTIALLY REPRODUCIBLE**

- The DeepSeek LLM baseline is fully reproducible from the current repository (given API key)
- The main method results (FullCalibratorAdapter, baselines) are reported from prior work and cannot be re-run from the current repository alone
- The annotation reliability study is prepared but not yet completed
- All generation scripts and result files are present and verifiable
