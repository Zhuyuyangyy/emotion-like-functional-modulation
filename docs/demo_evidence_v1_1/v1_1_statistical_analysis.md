# V1.1 Statistical Analysis Report

## 1. Bootstrap 95% Confidence Intervals

### Action Accuracy

| Method | Mean | 95% CI Lower | 95% CI Upper |
|--------|------|-------------|-------------|
| FullCalibratorAdapter | 0.7533 | 0.7033 | 0.8000 |
| KeywordRuleBaseline | 0.4600 | 0.4033 | 0.5167 |
| SafeKeywordFirstBaseline | 0.4167 | 0.3600 | 0.4733 |
| RiskContextOracleBaseline | 0.5100 | 0.4533 | 0.5667 |
| NoExperienceNoAffectiveBaseline | 0.7167 | 0.6667 | 0.7667 |

### Composite Score

| Method | Mean | 95% CI Lower | 95% CI Upper |
|--------|------|-------------|-------------|
| FullCalibratorAdapter | 0.8604 | 0.8261 | 0.8924 |
| KeywordRuleBaseline | 0.5534 | 0.5147 | 0.5940 |
| SafeKeywordFirstBaseline | 0.5070 | 0.4734 | 0.5416 |
| RiskContextOracleBaseline | 0.7839 | 0.7563 | 0.8108 |
| NoExperienceNoAffectiveBaseline | 0.8435 | 0.8080 | 0.8761 |

## 2. McNemar Test Results (FullCalibratorAdapter vs Baselines)

| Baseline | chi2 | p-value | Significant (p<0.05) | a | b | c | d |
|----------|------|---------|---------------------|---|---|---|---|
| KeywordRuleBaseline | 53.9173 | 0.000000 | Yes | 111 | 115 | 27 | 47 |
| SafeKeywordFirstBaseline | 66.0147 | 0.000000 | Yes | 99 | 127 | 26 | 48 |
| RiskContextOracleBaseline | 37.2784 | 0.000051 | Yes | 119 | 107 | 34 | 40 |
| NoExperienceNoAffectiveBaseline | 10.0227 | 0.438502 | No | 215 | 11 | 0 | 74 |

## 3. Per-Source-Type Breakdown (FullCalibratorAdapter)

| Source Type | N | Accuracy | Risky Auto-Exec | False Caution | Composite |
|-------------|---|----------|-----------------|---------------|-----------|
| affective_pressure_trace | 60 | 0.7167 | 0.0000 | 0.0000 | 0.8867 |
| tool_use_risk_trace | 80 | 0.8125 | 0.0444 | 0.0400 | 0.8997 |
| coding_agent_trace | 100 | 0.6900 | 0.0000 | 0.2667 | 0.7960 |
| safe_low_risk_trace | 40 | 0.8750 | 0.0000 | 0.1000 | 0.9200 |
| experience_failure_trace | 20 | 0.7000 | 0.0000 | 0.0000 | 0.8800 |

## 4. Interpretation of Statistical Significance

The following baselines show statistically significant differences from FullCalibratorAdapter (p < 0.05):
- **KeywordRuleBaseline**: chi2=53.9173, p=0.000000 (a=111, b=115, c=27, d=47)
- **SafeKeywordFirstBaseline**: chi2=66.0147, p=0.000000 (a=99, b=127, c=26, d=48)
- **RiskContextOracleBaseline**: chi2=37.2784, p=0.000051 (a=119, b=107, c=34, d=40)

The following baselines do NOT show statistically significant differences from FullCalibratorAdapter (p >= 0.05):
- **NoExperienceNoAffectiveBaseline**: chi2=10.0227, p=0.438502

Bootstrap confidence intervals provide additional evidence: non-overlapping CIs between methods suggest meaningful differences even when McNemar test results are borderline.
