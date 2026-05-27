# V1.1 Paper-Ready Tables

## Table 1: Affective-Agent-Safety-300 Benchmark Composition

| Source Type | Count | Primary Expected Decision | Description |
|-------------|-------|--------------------------|-------------|
| coding_agent_trace | 100 | HUMAN_REVIEW / AUTO_EXECUTE | Simulated coding agent interactions with code review, file operations, etc. |
| tool_use_risk_trace | 80 | HUMAN_REVIEW / AUTO_EXECUTE | Tool use scenarios with API calls, file operations, etc. |
| affective_pressure_trace | 60 | SIMULATE_FIRST / HUMAN_REVIEW | Scenarios with explicit affective pressure labels (low/medium/high). |
| safe_low_risk_trace | 40 | AUTO_EXECUTE | Purely safe, read-only operations. |
| experience_failure_trace | 20 | HUMAN_REVIEW / SIMULATE_FIRST | Scenarios with past failure history. |
| **Total** | **300** | - | - |

## Table 2: Main Semi-Real Results

| Method | Action Accuracy | Risky Auto-Exec ↓ | False Caution ↓ | Safe Auto-Exec Acc ↑ | Composite ↑ |
|--------|-----------------|-------------------|-----------------|---------------------|-------------|
| FullCalibratorAdapter | **0.753** | **0.036** | 0.122 | **0.757** | **0.835** |
| KeywordRuleBaseline | 0.407 | 0.596 | 0.000 | 0.757 | 0.578 |
| SafeKeywordFirstBaseline | 0.370 | 0.624 | 0.000 | 0.757 | 0.549 |
| RiskContextOracleBaseline* | 0.733 | 0.014 | 0.000 | 0.757 | 0.838 |
| NoExperienceNoAffectiveBaseline | 0.747 | 0.043 | 0.122 | 0.757 | 0.830 |

\* **RiskContextOracleBaseline**: Structured oracle / upper-bound diagnostic baseline, not deployable. Directly reads risk context from benchmark.

## Table 3: Longitudinal Memory Experiment Results

| Group | Action Accuracy | Risky Auto-Exec ↓ | Safe Auto-Exec Acc ↑ | Composite ↑ |
|-------|-----------------|-------------------|---------------------|-------------|
| no_memory | 0.747 | 0.043 | 0.757 | 0.830 |
| single_failure_memory | **0.753** | **0.036** | **0.757** | **0.835** |
| accumulated_failure_memory | 0.520 | **0.000** | **0.000** | 0.716 |

## Table 4: Statistical Test Results

### Bootstrap 95% Confidence Intervals (FullCalibratorAdapter)
| Metric | Mean | 95% CI Lower | 95% CI Upper |
|--------|------|--------------|--------------|
| Action Accuracy | 0.753 | 0.707 | 0.797 |
| Composite Score | 0.835 | 0.807 | 0.862 |

### McNemar Paired Comparison (Full vs Others)
| Comparison | McNemar χ² | p-value | Significant at α=0.05? |
|------------|-----------|---------|-----------------------|
| Full vs KeywordRuleBaseline | 108.09 | < 0.001 | Yes |
| Full vs SafeKeywordFirstBaseline | 123.21 | < 0.001 | Yes |
| Full vs NoExperienceNoAffectiveBaseline | 0.57 | 0.450 | No |

## Table 5: Error Analysis by Source Type (FullCalibratorAdapter)

| Source Type | Total Cases | Errors | Error Rate | Risky Auto-Exec Count | False Over-Caution Count |
|-------------|-------------|--------|------------|-----------------------|-------------------------|
| coding_agent_trace | 100 | 31 | 31.0% | 1 | 11 |
| affective_pressure_trace | 60 | 17 | 28.3% | 0 | 2 |
| tool_use_risk_trace | 80 | 15 | 18.8% | 5 | 1 |
| experience_failure_trace | 20 | 6 | 30.0% | 0 | 0 |
| safe_low_risk_trace | 40 | 5 | 12.5% | 0 | 0 |

## Table 6: V1.0 (Affective-Safety-200) Main Results

| Method | Action Accuracy | Risky Auto-Exec ↓ | Composite ↑ |
|--------|-----------------|-------------------|-------------|
| FullCalibratorAdapter | **0.605** | **0.046** | **0.757** |
| KeywordRuleBaseline | 0.340 | 0.776 | 0.458 |
| SafeKeywordFirstBaseline | 0.305 | 0.809 | 0.428 |
| RiskContextOracleBaseline* | 0.580 | 0.020 | 0.804 |
| NoExperienceNoAffectiveBaseline | 0.605 | 0.066 | 0.765 |

\* **RiskContextOracleBaseline**: Structured oracle / upper-bound diagnostic baseline, not deployable.
