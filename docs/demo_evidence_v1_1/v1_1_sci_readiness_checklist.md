# V1.1 SCI Readiness Checklist

| Item | Status |
|------|--------|
| Benchmark | Affective-Safety-200 + Semi-Real-300 benchmarks available |
| Baseline Comparison | 4 baselines + Full Method with unified canonical implementation |
| Ablation Study | 6 ablation variants including w/o_strict_context_priority |
| Longitudinal Memory | 3-group experiment (no/single/accumulated memory) |
| Statistical Tests | Bootstrap 95% CI + McNemar paired comparison |
| Per-Category Metrics | Both benchmarks have per-category breakdowns |
| Annotation Guideline | Semi-Real-300 has formal annotation guideline |
| Reproducibility | All experiments deterministic with fixed seed |
| No Label Leakage | Full Method does not read gold_decision/expected_decision |
| Limitations Section | All reports include explicit limitations |
| Oracle Baseline Labeled | RiskContextOracleBaseline clearly marked as oracle/upper-bound |
| Canonical Full Method | Single FullCalibratorAdapter used in both baseline and ablation tables |
| V0.9.1 Unchanged | Core framework not modified for V1.0/V1.1 experiments |

## Remaining Work for SCI Submission
- [ ] External validation on real agent logs (not simulated traces)
- [ ] Inter-annotator agreement on semi-real benchmark
- [ ] Comparison with LLM-based safety classifiers
- [ ] Computational cost analysis