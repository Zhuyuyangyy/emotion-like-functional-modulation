# V1.1 SCI Claim-Evidence Map

## Claim 1: Strict Context Priority Reduces Risky Auto-Execution

| Item | Value |
|------|-------|
| **Claim** | Evaluating strict risk context *before* safe verbs significantly reduces risky auto-execution compared to the safe-keyword-first approach. |
| **Evidence** | `experiments/results/semireal/semireal_full_results.json`, `docs/demo_evidence_v1_1/v1_1_semireal_experiment_report.md` |
| **Metrics** | FullCalibratorAdapter Risky Auto-Exec Rate = 0.036, SafeKeywordFirstBaseline = 0.624; 93.6% reduction. |
| **Support Strength** | **Strong** (directly measurable on two benchmarks, large effect size) |
| **Allow in Main Paper?** | Yes |
| **Recommended Wording** | "The three-tier calibrator with strict context priority reduced risky auto-execution by 93.6% compared to the safe-keyword-first baseline (3.6% vs 62.4%)." |
| **Prohibited Wording** | "Eliminates risky auto-execution entirely," "Best method in all scenarios" |

---

## Claim 2: Affective Pressure Improves Safety Without Severe Efficiency Tradeoff

| Item | Value |
|------|-------|
| **Claim** | Affective pressure signals slightly reduce risky auto-execution without drastically harming safe auto-execution accuracy. |
| **Evidence** | `experiments/results/semireal/semireal_full_results.json`, `experiments/results/semireal/statistical_analysis_results.json` |
| **Metrics** | NoExperienceNoAffectiveBaseline Risky Auto-Exec = 0.043 vs FullCalibratorAdapter = 0.036; Safe Auto-Exec Acc both ≈ 0.757. |
| **Support Strength** | **Moderate** (measurable effect, consistent across two benchmarks) |
| **Allow in Main Paper?** | Yes |
| **Recommended Wording** | "Including affective pressure signals reduced risky auto-execution by 16.3% while maintaining safe auto-execution accuracy (0.757)." |
| **Prohibited Wording** | "Proof that emotional intelligence improves safety," "Drastically reduces risk" |

---

## Claim 3: Single-Failure Memory Achieves Best Safety-Utility Balance

| Item | Value |
|------|-------|
| **Claim** | A single-failure memory achieves the best tradeoff between reducing risky auto-execution and preserving safe auto-execution efficiency. |
| **Evidence** | `docs/demo_evidence_v1_1/v1_1_longitudinal_memory_report.md`, `experiments/results/longitudinal/longitudinal_memory_table.csv` |
| **Metrics** | single_failure_memory Risky Auto-Exec = 0.036 (better than no_memory 0.043) and Safe Auto-Exec Acc = 0.757 (same as no_memory). |
| **Support Strength** | **Strong** (direct comparison across three groups, clear tradeoff curve) |
| **Allow in Main Paper?** | Yes |
| **Recommended Wording** | "The single-failure memory configuration achieved the best safety-utility balance: 16.3% lower risky auto-execution than no memory, while maintaining identical safe auto-execution accuracy (0.757)." |
| **Prohibited Wording** | "Accumulated memory is the best strategy," "Single-failure memory is universally optimal" |

---

## Claim 4: Accumulated Memory Causes Severe Over-Caution Collapse

| Item | Value |
|------|-------|
| **Claim** | Accumulated failure memory leads to severe over-caution, eliminating safe auto-execution entirely. |
| **Evidence** | `docs/demo_evidence_v1_1/v1_1_longitudinal_memory_report.md` |
| **Metrics** | accumulated_failure_memory Safe Auto-Exec Acc = 0.000 (all safe cases are reviewed/blocked). |
| **Support Strength** | **Strong** (clear 0/100 effect) |
| **Allow in Main Paper?** | Yes (as a cautionary case, not a recommended strategy) |
| **Recommended Wording** | "The accumulated-failure memory configuration demonstrates an extreme caution tradeoff: it eliminated risky auto-execution entirely (0.000) but also reduced safe auto-execution accuracy to 0.000." |
| **Prohibited Wording** | "Accumulated memory is a valid strategy," "Eliminating risk requires sacrificing safety" |

---

## Claim 5: RiskContextOracleBaseline Is a Diagnostic Upper Bound, Not a Deployable Baseline

| Item | Value |
|------|-------|
| **Claim** | RiskContextOracleBaseline is a diagnostic upper-bound baseline that directly reads structured risk context, not a deployable method. |
| **Evidence** | `experiments/baselines_affective_safety.py`, `docs/demo_evidence_v1_1/annotation_guideline.md` |
| **Metrics** | RiskContextOracleBaseline has the highest composite score (0.838) but relies on direct label leakage. |
| **Support Strength** | **Strong** (code inspection confirms label leakage) |
| **Allow in Main Paper?** | Yes (with clear disclaimer) |
| **Recommended Wording** | "We include RiskContextOracleBaseline as a diagnostic upper-bound reference (0.838 composite score). It directly reads structured risk context from the benchmark, which is not realistic in deployment where risk must be inferred from natural language." |
| **Prohibited Wording** | "RiskContextOracleBaseline is a strong competitor," "Outperforms Full Method" |

---

## Claim 6: Full Method Achieves Strong Safety Performance on Semi-Real Traces

| Item | Value |
|------|-------|
| **Claim** | The FullCalibratorAdapter achieves strong safety performance on the semi-real Affective-Agent-Safety-300 benchmark. |
| **Evidence** | `docs/demo_evidence_v1_1/v1_1_semireal_experiment_report.md`, `experiments/results/semireal/statistical_analysis_results.json` |
| **Metrics** | Action Accuracy = 0.753, Risky Auto-Exec Rate = 0.036, Composite Score = 0.835. |
| **Support Strength** | **Moderate** (strong performance, but semi-real traces are still simulated) |
| **Allow in Main Paper?** | Yes |
| **Recommended Wording** | "The FullCalibratorAdapter achieved strong performance on the semi-real benchmark: action accuracy 0.753, risky auto-execution rate 3.6%, composite score 0.835." |
| **Prohibited Wording** | "Achieves perfect safety," "State-of-the-art performance," "Solves the autonomous safety problem" |

---

## Prohibited Claims (Do Not Include)

- "Our agent has emotional intelligence"
- "We prove that emotions improve safety"
- "Full Method outperforms RiskContextOracleBaseline"
- "Accumulated memory is a recommended strategy"
- "This solves the autonomous agent safety problem"
- "Generalizable to all agent platforms"
- "Real-time emotion detection" (we use structured labels)
