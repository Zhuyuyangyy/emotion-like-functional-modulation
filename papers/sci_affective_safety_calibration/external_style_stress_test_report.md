# External-Style Stress Test Report (Phase 2)

## 1. Benchmark Construction Rules

The External-Style Agent Safety Stress Test (EXT-AS-150) is a 150-case controlled stress test benchmark designed to evaluate the robustness of the affective safety calibration framework on scenarios outside the original Semi-Real-300 distribution.

### 1.1 Schema

Each case follows this structured schema:

| Field | Type | Description |
|-------|------|-------------|
| `case_id` | string | Unique identifier: `EXT-AS-XXXX` |
| `source_type` | string | One of 6 operational trace categories |
| `trace_steps` | list[str] | Ordered sequence of agent actions |
| `user_request` | string | Natural language user instruction |
| `task_context` | string | Situational context for the request |
| `risk_context` | object | Binary risk flags (destructive, sensitive_data, security_related, production_environment, irreversible) |
| `pressure_context` | object | Continuous pressure signals (urgency, trust_pressure) |
| `experience_context` | object | Experience signals (similar_failure_before, risk_count) |
| `gold_decision` | string | Ground-truth label: AUTO_EXECUTE, SIMULATE_FIRST, HUMAN_REVIEW, or BLOCK |
| `annotation_rationale` | string | Justification for the gold decision |

### 1.2 Source Type Distribution

| Source Type | Count | Domain Focus |
|-------------|-------|-------------|
| repo_maintenance_trace | 30 | Git operations, branch management, history rewrites |
| cloud_config_trace | 30 | AWS/GCP/Azure resource management, K8s config, IAM policies |
| database_operation_trace | 25 | SQL operations, schema changes, privilege management |
| credential_security_trace | 25 | SSH/key management, vault operations, secret rotation |
| deployment_pipeline_trace | 20 | CI/CD pipelines, canary/blue-green deployments, rollbacks |
| benign_review_trace | 20 | Health checks, log reading, service monitoring |

### 1.3 Gold Decision Distribution

| Decision | Count | Percentage | Target |
|----------|-------|-----------|--------|
| AUTO_EXECUTE | 45 | 30.0% | ~30% |
| SIMULATE_FIRST | 38 | 25.3% | ~25% |
| HUMAN_REVIEW | 52 | 34.7% | ~35% |
| BLOCK | 15 | 10.0% | ~10% |

### 1.4 Construction Principles

1. **No reuse from Semi-Real-300**: All scenario templates, user requests, and rationales are newly written. No template sentences or cases were copied from the original Affective-Agent-Safety-300 benchmark.
2. **Real development/ops focus**: Scenarios emphasize real git operations, Docker/K8s management, SQL operations, SSH/key management, CI/CD pipelines, log reading, and health checks.
3. **Structured labels**: All risk_context, pressure_context, and experience_context fields are explicitly labeled with structured values.
4. **Controlled stress test**: This is an external-style controlled stress test, NOT real production data. Cases are synthetically generated to probe specific failure modes.
5. **Deterministic generation**: All cases generated with fixed seed (20260527) for reproducibility.

## 2. Differences from Semi-Real-300

| Dimension | Semi-Real-300 | External-Style-150 |
|-----------|--------------|-------------------|
| Source types | coding_agent_trace, tool_use_risk_trace, affective_pressure_trace, safe_low_risk_trace, experience_failure_trace | repo_maintenance_trace, cloud_config_trace, database_operation_trace, credential_security_trace, deployment_pipeline_trace, benign_review_trace |
| Pressure representation | `affective_pressure_label` (low/medium/high) | `pressure_context` with continuous `urgency` and `trust_pressure` values |
| Experience representation | `experience_memory` with `has_similar_failure`, `failure_type`, `risk_count` | `experience_context` with `similar_failure_before`, `risk_count` |
| Domain focus | General coding + tool use + affective pressure | DevOps, cloud infrastructure, database ops, credential management, CI/CD |
| Decision distribution | Heavily weighted toward AUTO_EXECUTE (many safe_low_risk cases) | Balanced: 30% AUTO, 25% SIMULATE, 35% REVIEW, 10% BLOCK |
| Case ID prefix | SR-AS-XXXX | EXT-AS-XXXX |

## 3. Main Results

### 3.1 Overall Metrics

| Method | Accuracy | Risky Auto-Exec | False Caution | Verification Approp | HR F1 | Composite |
|--------|----------|-----------------|---------------|---------------------|-------|-----------|
| FullCalibratorAdapter | 0.567 | 0.083 | 0.400 | 0.580 | 0.680 | 0.664 |
| KeywordRuleBaseline | 0.313 | 0.810 | 0.067 | 0.373 | 0.326 | 0.419 |
| SafeKeywordFirstBaseline | 0.300 | 0.893 | 0.000 | 0.360 | 0.237 | 0.404 |
| RiskContextOracleBaseline | 0.467 | 0.000 | 0.000 | 0.747 | 0.887 | 0.763 |
| NoExperienceNoAffectiveBaseline | 0.567 | 0.083 | 0.400 | 0.580 | 0.680 | 0.664 |

### 3.2 Comparison with Semi-Real-300 (FullCalibratorAdapter)

| Metric | External-Style | Semi-Real-300 | Delta |
|--------|---------------|---------------|-------|
| Action Accuracy | 0.567 | 0.753 | -0.187 |
| Risky Auto-Exec Rate | 0.083 | 0.035 | +0.048 |
| False Over-Caution Rate | 0.400 | 0.121 | +0.279 |
| Verification Appropriateness | 0.580 | 0.773 | -0.193 |
| HR F1 | 0.680 | 0.844 | -0.164 |
| Composite Score | 0.664 | 0.835 | -0.172 |
| Safe Auto-Exec Accuracy | 0.444 | 0.757 | -0.313 |

## 4. Does Full Method Maintain Low Risky Auto-Exec?

**Yes, with caveats.** The FullCalibratorAdapter achieves a risky auto-exec rate of 0.083 (8.3%) on the external-style benchmark, which is below the 10% threshold. However:

- This is a **2.4x increase** from the semireal-300 rate of 0.036 (3.6%).
- The increase is driven by specific source types where the calibrator's tier classification does not match the gold labels well (see Section 5).
- The RiskContextOracleBaseline achieves 0.000 risky auto-exec, indicating that the risk_context labels alone are sufficient to avoid all risky auto-executions, but at the cost of lower action accuracy.

## 5. Which Scenarios Degrade?

### 5.1 Per-Source-Type Analysis (FullCalibratorAdapter)

| Source Type | Accuracy | Risky Auto-Exec | False Caution | Composite |
|-------------|----------|-----------------|---------------|-----------|
| cloud_config_trace | 0.933 | 0.000 | 0.000 | 0.977 |
| repo_maintenance_trace | 0.700 | 0.000 | 0.333 | 0.768 |
| credential_security_trace | 0.480 | 0.000 | 1.000 | 0.514 |
| database_operation_trace | 0.360 | 0.000 | 0.000 | 0.648 |
| benign_review_trace | 0.200 | 0.273 | 0.571 | 0.378 |
| deployment_pipeline_trace | 0.550 | 0.308 | 0.667 | 0.542 |

### 5.2 Key Degraded Scenarios

1. **benign_review_trace (risky auto-exec: 27.3%)**: The calibrator classifies many HUMAN_REVIEW and SIMULATE_FIRST benign operations as safe (tier2_safe), leading to auto-execution when human review was expected. This is particularly problematic for production service restarts and resilience tests that the calibrator treats as low-risk.

2. **deployment_pipeline_trace (risky auto-exec: 30.8%)**: Production deployment and pipeline operations are frequently misclassified. The calibrator's tier system does not distinguish well between "view pipeline status" (safe) and "deploy to production" (risky), because both share similar vocabulary patterns.

3. **credential_security_trace (false over-caution: 100%)**: All credential operations are escalated to HUMAN_REVIEW or BLOCK, including metadata-only checks that should be AUTO_EXECUTE. The calibrator's security-related keyword detection over-triggers on credential scenarios.

4. **database_operation_trace (accuracy: 36.0%)**: Low accuracy driven by the calibrator's difficulty distinguishing between read-only SQL queries (AUTO_EXECUTE) and schema modifications (HUMAN_REVIEW) that share similar trace patterns.

### 5.3 Root Cause Analysis

The FullCalibratorAdapter and NoExperienceNoAffectiveBaseline produce **identical results** on this benchmark. This indicates that the affective/experience signals (urgency, anxiety, similar_failure_before) are not differentiating the decisions in this benchmark because:

- The pressure_context values (urgency 0.1-0.7) map to affective signals that rarely exceed the 0.5 threshold in the FullCalibratorAdapter's decision logic.
- The experience_context (similar_failure_before) is only used in the tier2_safe branch, which is not the dominant tier for the degraded scenarios.
- The core issue is the SafeActionCalibrator's tier classification, not the affective/experience integration layer.

## 6. Does This Support Generalization?

**No. These results support limited cross-benchmark robustness only, NOT generalization.**

### 6.1 What the results show

- The Full Method maintains a risky auto-exec rate below 10% on the external-style benchmark, which is a positive signal for safety.
- However, overall performance degrades significantly: composite score drops from 0.835 to 0.664 (-17.2pp), and action accuracy drops from 0.753 to 0.567 (-18.7pp).
- The affective/experience integration provides no benefit over the base calibrator on this benchmark, suggesting the framework's advantages are domain-specific.

### 6.2 What the results do NOT show

- These results do NOT demonstrate generalization to novel operational domains.
- The external-style benchmark is a controlled stress test with structured labels, not real production data.
- Performance on synthetic benchmarks does not predict performance on real agent deployments.
- The identical FullCalibratorAdapter/NoExperienceNoAffectiveBaseline results indicate the affective integration layer is not robustly transferring.

### 6.3 Appropriate claim

The only defensible claim is **limited cross-benchmark robustness**: the core safety mechanism (low risky auto-exec) transfers partially, but the full affective calibration framework does not generalize. Future work should investigate domain-adaptive tier classification and threshold calibration for diverse operational contexts.

## 7. Limitations

1. The external-style benchmark is synthetically generated; it does not reflect the distribution of real agent operations.
2. The pressure_context uses continuous values mapped from structured labels, not real-time affective signals.
3. The SafeActionCalibrator's tier classification was not retrained or adapted for the new source types.
4. The benchmark has only 150 cases; statistical power is limited for per-source-type analysis.
5. The FullCalibratorAdapter and NoExperienceNoAffectiveBaseline produce identical results, suggesting the affective integration layer needs domain-specific tuning to be effective in new operational contexts.
