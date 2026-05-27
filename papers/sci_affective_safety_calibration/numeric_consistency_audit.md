# Numeric Consistency Audit

## 1. SafeKeywordFirstBaseline Risky Auto-Exec: 0.872 vs 0.624

### Source of Truth

| Source File | Value | Benchmark |
|-------------|-------|-----------|
| `experiments/results/semireal/semireal_full_results.json` | **0.8723** | Affective-Agent-Safety-300 (semi-real) |
| `experiments/results/affective_safety_full_results.json` | **0.8092** | Affective-Safety-200 (V1.0) |

### Conflict Location

| Document | Stated Value | Benchmark Context | Correct? |
|----------|-------------|-------------------|----------|
| `v1_1_paper_tables.md` Table 2 | 0.872 | Semi-real | **Correct** |
| `sci_claim_evidence_map.md` Claim 1 | 0.624 | Unclear/mixed | **Incorrect** |
| `materials_for_manuscript_v0_1.md` Part B3 | 0.872 | Semi-real | **Correct** |

### Root Cause

The value 0.624 in `sci_claim_evidence_map.md` appears to be from the V1.0 benchmark (Affective-Safety-200), where SafeKeywordFirstBaseline Risky Auto-Exec = 0.8092. The value 0.624 does not match either benchmark and may be a copy error from an earlier iteration.

## 2. Relative Reduction Calculation

### Semi-Real Benchmark (Primary)

```
FullCalibratorAdapter Risky Auto-Exec = 0.0355
SafeKeywordFirstBaseline Risky Auto-Exec = 0.8723
Relative reduction = (0.8723 - 0.0355) / 0.8723 = 0.9593 = 95.9%
```

### V1.0 Benchmark

```
FullCalibratorAdapter Risky Auto-Exec = 0.0461
SafeKeywordFirstBaseline Risky Auto-Exec = 0.8092
Relative reduction = (0.8092 - 0.0461) / 0.8092 = 0.9431 = 94.3%
```

## 3. Correction Required

| Location | Current Text | Corrected Text |
|----------|-------------|----------------|
| `sci_claim_evidence_map.md` Claim 1 | "3.6% vs 62.4%" | "3.6% vs 87.2%" |
| `sci_claim_evidence_map.md` Claim 1 | "93.6% reduction" | "95.9% reduction" |
| `v1_1_paper_tables.md` Table 2 | 0.872 | **Correct, no change needed** |
| `materials_for_manuscript_v0_1.md` Part E1 C1 | "93.6%" | "95.9%" |

## 4. Recommendations for Manuscript v0.2

1. **Always specify which benchmark** when citing numeric results. Use "on the semi-real benchmark (N=300)" or "on the Affective-Safety-200 benchmark (N=200)".
2. **Use semi-real benchmark as primary** for the main results table since it's more realistic.
3. **Correct the claim**: "The three-tier calibrator with strict context priority reduced risky auto-execution by 95.9% compared to the safe-keyword-first baseline (3.6% vs 87.2% on the semi-real benchmark, N=300)."
4. **V1.0 result can be cited separately**: "On the Affective-Safety-200 benchmark, the reduction was 94.3% (4.6% vs 80.9%)."
