# Synthetic Ablation Report

**Date**: 2026-06-09
**Dataset**: Synthetic-AB300 (seed=42)
**Pipeline**: DecisionPipeline (real components, not DummyAgent)

## Command

```bash
# Step 1: Export frozen dataset
python experiments/rebuild/export_synthetic_ab300.py --seed 42

# Step 2: Run ablation
python experiments/rebuild/run_synthetic_ablation.py \
    --input data/rebuild/synthetic_ab300_seed42.json
```

## Input Data

- **Path**: `data/rebuild/synthetic_ab300_seed42.json`
- **Records**: 300 (60 unique templates)
- **Gold label type**: Heuristic (NOT human-validated)
- **Source**: `AffectiveBenchmark(seed=42, size=300)` frozen to JSON

## Output Results

- **Path**: `results/rebuild/synthetic_ablation_results.json`

## Metrics Table

| Baseline | Accuracy | Macro-F1 | Severity MAE | Risky-Auto ↓ | Over-Caution ↓ |
|----------|----------|----------|--------------|--------------|-----------------|
| plain    | 0.060    | 0.028    | 1.207        | 1.000        | 0.000           |
| risk     | 0.293    | 0.191    | 0.873        | 0.546        | 0.000           |
| memory   | 0.127    | 0.110    | 1.020        | 0.546        | 0.000           |
| full     | 0.130    | 0.108    | 1.233        | 0.515        | 0.000           |

### Per-Class Metrics

#### plain (no risk, no memory, no affect)

| Class           | Precision | Recall | F1     | Support |
|-----------------|-----------|--------|--------|---------|
| AUTO_EXECUTE    | 0.060     | 1.000  | 0.113  | 18      |
| SIMULATE_FIRST  | 0.000     | 0.000  | 0.000  | 217     |
| HUMAN_REVIEW    | 0.000     | 0.000  | 0.000  | 50      |
| BLOCK           | 0.000     | 0.000  | 0.000  | 15      |

#### risk (keyword risk encoder only)

| Class           | Precision | Recall | F1     | Support |
|-----------------|-----------|--------|--------|---------|
| AUTO_EXECUTE    | 0.087     | 1.000  | 0.160  | 18      |
| SIMULATE_FIRST  | 0.756     | 0.300  | 0.429  | 217     |
| HUMAN_REVIEW    | 0.714     | 0.100  | 0.175  | 50      |
| BLOCK           | 0.000     | 0.000  | 0.000  | 15      |

#### memory (risk + experience generalization)

| Class           | Precision | Recall | F1     | Support |
|-----------------|-----------|--------|--------|---------|
| AUTO_EXECUTE    | 0.087     | 1.000  | 0.160  | 18      |
| SIMULATE_FIRST  | 0.000     | 0.000  | 0.000  | 217     |
| HUMAN_REVIEW    | 0.215     | 0.400  | 0.280  | 50      |
| BLOCK           | 0.000     | 0.000  | 0.000  | 15      |

#### full (risk + memory + affect)

| Class           | Precision | Recall | F1     | Support |
|-----------------|-----------|--------|--------|---------|
| AUTO_EXECUTE    | 0.093     | 1.000  | 0.170  | 18      |
| SIMULATE_FIRST  | 1.000     | 0.060  | 0.113  | 217     |
| HUMAN_REVIEW    | 0.000     | 0.000  | 0.000  | 50      |
| BLOCK           | 0.086     | 0.533  | 0.148  | 15      |

### Ablation Deltas

| Transition       | Δ Accuracy | Δ Macro-F1 | Δ Risky-Auto |
|------------------|------------|------------|--------------|
| plain → risk     | +0.233     | +0.163     | +0.454       |
| risk → memory    | -0.166     | -0.081     | +0.000       |
| memory → full    | +0.003     | -0.002     | +0.031       |

## Key Findings

1. **Risk encoder provides the only meaningful improvement**: plain → risk shows +0.233 accuracy and +0.454 reduction in risky auto-execution. This is expected — the keyword-based risk encoder can detect obvious risk keywords.

2. **Memory layer hurts performance**: risk → memory shows -0.166 accuracy. Memory generalization causes over-escalation on unseen templates, pulling risk predictions away from the keyword-based baseline.

3. **Affect layer is noise-level**: memory → full shows Δ accuracy = +0.003, Δ macro-F1 = -0.002. The affect layer (emotional state + conflict + hesitation) cannot be distinguished from random on this synthetic benchmark.

4. **BLOCK class is essentially undetected**: Across all baselines, BLOCK precision/recall is near zero (except full with 0.086/0.533). The pipeline cannot reliably identify tasks that should be blocked.

5. **DummyAgent guard passes**: The pipeline correctly rejects inert stand-ins, confirming the old DummyAgent failure mode cannot recur.

## Limitations

1. **Gold labels are heuristic, not human-validated**: The gold decisions are derived from hand-authored task metadata using a deterministic rule, not independent human annotation. Cohen's kappa has not been computed.

2. **Synthetic data only**: All 300 records are generated from 60 hand-written templates. No real-world or semi-real data is involved.

3. **Circular evaluation risk**: The gold labels and the pipeline's risk thresholds both derive from the same hand-authored task metadata. This weakens (does not eliminate) the validity of the ablation comparison.

4. **Category imbalance**: SIMULATE_FIRST dominates (217/300 = 72.3%), making per-class metrics for minority classes (BLOCK: 15, AUTO_EXECUTE: 18) unreliable.

5. **Keyword dependency**: The risk encoder is keyword-based. It cannot detect semantic risks such as phishing, social engineering, or privacy leakage. R-Judge external validation confirmed unsafe recall = 0.000 on 571 real human-annotated records.

## Why This Does Not Validate Real-World Safety

- The dataset is synthetic: 60 templates repeated ~5x, not real-world scenarios
- Gold labels are heuristic: derived from the same rules that inform the pipeline
- No independent human annotation exists (kappa pending)
- R-Judge external validation on real data completely failed (unsafe recall = 0.000)
- The keyword-based risk encoder cannot detect semantic risks
- Memory and affect layers show no reliable improvement over the keyword baseline

**These results are a mechanism sanity check only. They should not be cited as evidence of real-world safety effectiveness.**
