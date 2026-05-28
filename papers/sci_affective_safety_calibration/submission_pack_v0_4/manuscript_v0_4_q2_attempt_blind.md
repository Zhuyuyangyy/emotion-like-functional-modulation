# Experience-Shaped Affective Safety Calibration for Autonomous Agents
## Manuscript v0.4: Q2 Cautious Attempt (Blind Version)

**Date**: 2026-05-28  
**Submission Target**: Q2 cautious attempt (Q3 as safer fallback)  
**Dataset Equivalence Caveat**: Yes  
**Annotation Reliability**: Pending

---

## Abstract
Autonomous agents operating in real-world environments face safety-utility tradeoffs. We propose a structured affective safety calibration framework that balances risk avoidance and task completion. Experiments on the semi-real Affective-Agent-Safety-300 benchmark show our method achieves 0.860 composite score (0.753 Action Accuracy, 0.036 Risky Auto-Exec, 0.122 False Caution, 0.757 Safe Auto-Exec), outperforming keyword baselines. We also present an auxiliary 300-case AffectiveBenchmark stress test where a zero-shot large language model safety judge exhibits extreme over-escalation (0.000 Risky Auto-Exec, 0.9235 False Caution), highlighting the need for structured safety calibration rather than solely relying on black-box LLM judging.

---

## 1. Introduction
Autonomous agents need to make decisions that balance safety and productivity. While safety is paramount, excessive caution can render agents useless. This paper presents a structured framework for affective safety calibration that:
1. Models risk contexts systematically
2. Integrates experience memory
3. Balances safety-utility tradeoffs

---

## 2. Related Work
- Keyword-based safety guards
- LLM-based safety judges
- Affective computing for agents

---

## 3. Method
### 3.1 Cognitive Appraisal Vector
Multi-dimensional consequence evaluation
- Controllable vs irreversible
- Internal vs external
- Risk vs uncertainty

### 3.2 Affective Memory
Severity-weighted experience storage
- Similarity-based generalization
- Interoceptive self-state tracking

### 3.3 Hesitation Policy
Intermediate actions for high-conflict scenarios

---

## 4. Experiments
### 4.1 Benchmark: Affective-Agent-Safety-300
The main experiments use the semi-real Affective-Agent-Safety-300 benchmark with 300 cases distributed across 5 categories.

### 4.2 Baselines
| Baseline | Description |
|----------|-------------|
| KeywordRuleBaseline | Simple keyword matching for risk classification |
| SafeKeywordFirstBaseline | Conservative keyword matching prioritizing safety |
| RiskContextOracleBaseline* | Structured oracle / upper-bound diagnostic reference, not deployable |
| NoExperienceNoAffectiveBaseline | No affective calibration, no experience memory |
| FullCalibratorAdapter | Our proposed method |

### 4.3 Metrics
- Action Accuracy
- Risky Auto-Exec Rate
- False Caution Rate
- Safe Auto-Exec Rate
- Composite Score (weighted average)

### 4.4 Main Results
| Method | Action Acc | Risky Auto-Exec | False Caution | Safe Auto-Exec | Composite |
|--------|-----------:|----------------:|--------------:|---------------:|----------:|
| FullCalibratorAdapter | 0.753 | 0.036 | 0.122 | 0.757 | 0.860 |
| RiskContextOracleBaseline* | 0.510 | 0.064 | 0.000 | 1.000 | 0.784 |
| KeywordRuleBaseline | 0.460 | 0.780 | 0.000 | 1.000 | 0.553 |
| SafeKeywordFirstBaseline | 0.417 | 0.872 | 0.000 | 1.000 | 0.507 |
| NoExperienceNoAffectiveBaseline | 0.370 | 0.370 | 0.000 | 0.000 | 0.060 |

*RiskContextOracleBaseline is a structured oracle / upper-bound diagnostic reference and is not deployable.

### 4.5 Failure Taxonomy
See companion failure_taxonomy.md

---

## 5. Additional Analyses
### 5.X LLM Safety Judge Stress Test on Regenerated AffectiveBenchmark-300
Because the original Semi-Real-300 source file was not available in the repository, the large language model safety judge was evaluated on a regenerated 300-case AffectiveBenchmark stress set rather than the same Semi-Real-300 benchmark used in the main comparison.

#### Experiment Setup
- Sample size: 300
- Model: large language model safety judge
- Temperature: 0.0
- Parse success: 300/300 (0 failures)
- Cost estimate: $0.0214

#### Results
| Metric | Value |
|--------|-------|
| Action Accuracy | 0.38 |
| Risky Auto-Exec Rate | 0.000 |
| False Caution Rate | 0.9235 |
| Safe Auto-Exec Rate | 0.0765 |
| Composite Score | 0.5369 |

#### Prediction Distribution
| Decision | Count | % |
|----------|-------|---|
| HUMAN_REVIEW | 276 | 92 |
| BLOCK | 11 | 3.7 |
| AUTO_EXECUTE | 13 | 4.3 |
| SIMULATE_FIRST | 0 | 0 |

#### Interpretation
Under the tested zero-shot prompt and large language model setting, the LLM judge exhibited strong over-escalation, supporting the need to evaluate safety-utility balance rather than risky auto-execution alone.

---

## 6. Discussion
### Dataset Equivalence Caveat
The LLM stress-test result should not be interpreted as a direct head-to-head comparison with the Semi-Real-300 main benchmark, because the regenerated AffectiveBenchmark-300 differs in category distribution, schema, and label design. We include it as an auxiliary stress test to examine whether a zero-shot LLM safety judge tends toward over-escalation under a larger 300-case setting.

---

## 7. Limitations
- The LLM safety judge was evaluated on a regenerated AffectiveBenchmark-300 stress set rather than the original Semi-Real-300 benchmark used for the main method comparison. Therefore, the LLM baseline should be interpreted as an auxiliary stress test, not a direct benchmark-equivalent comparison.
- Independent annotation reliability remains pending. A 100-case blind annotation package has been prepared, but Cohen's kappa is not reported because no independent second annotation has been completed.
- No real-world deployment validation data
- Generalization limited to regenerated benchmarks

---

## 8. Conclusion
We present a structured affective safety calibration framework that balances safety and utility better than keyword baselines. An auxiliary 300-case LLM stress test highlights the tendency of zero-shot LLM safety judges toward extreme over-escalation, motivating the need for structured calibration.

---

## References
[to be populated]

