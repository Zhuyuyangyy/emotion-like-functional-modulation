# V1.1 Semi-Real Experiment Report

## 1. Benchmark
Affective-Agent-Safety-300: 300 semi-real cases across 5 source types.

| Source Type | Count |
|-------------|-------|
| affective_pressure_trace | 60 |
| coding_agent_trace | 100 |
| experience_failure_trace | 20 |
| safe_low_risk_trace | 40 |
| tool_use_risk_trace | 80 |

## 2. Methods
- **FullCalibratorAdapter**: Three-tier SafeActionCalibrator with affective/experience integration
- **KeywordRuleBaseline**: Simple keyword matching
- **SafeKeywordFirstBaseline**: Safe keywords override risk context (pre-V0.9.1 bug)
- **RiskContextOracleBaseline**: Oracle that directly reads risk_context (upper-bound reference)
- **NoExperienceNoAffectiveBaseline**: Real calibrator without affective/experience signals

## 3. Main Results

| Method | Accuracy | Risky Auto-Exec | False Caution | Safe Auto-Exec Acc | Composite |
|--------|----------|-----------------|---------------|---------------------|-----------|
| FullCalibratorAdapter | 0.753 | 0.035 | 0.121 | 0.757 | 0.835 |
| KeywordRuleBaseline | 0.460 | 0.780 | 0.000 | 1.000 | 0.508 |
| SafeKeywordFirstBaseline | 0.417 | 0.872 | 0.000 | 1.000 | 0.461 |
| RiskContextOracleBaseline | 0.510 | 0.064 | 0.000 | 1.000 | 0.767 |
| NoExperienceNoAffectiveBaseline | 0.717 | 0.043 | 0.121 | 0.757 | 0.813 |

## 4. Findings
- Full Method risky auto-exec: 0.035
- Full Method false over-caution: 0.121
- Full Method safe auto-execute accuracy: 0.757
- SafeKeywordFirstBaseline risky auto-exec: 0.872

## 5. Limitations
- Semi-real traces are simulated, not collected from real agent deployments.
- Affective pressure labels are structured annotations, not real-time emotion signals.
- Results validate the calibration mechanism on structured scenarios, not general affective intelligence.