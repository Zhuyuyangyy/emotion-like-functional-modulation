# V1.1 SCI Limitations

## 1. Semi-Real Traces Are Not Enterprise Production Logs

The semi-real Affective-Agent-Safety-300 benchmark is generated from structured templates, not collected from real enterprise agent deployments. While we simulate realistic coding and tool-use scenarios, the distribution of cases and their complexity may not perfectly match real-world usage patterns. In particular:

- We do not have long-tail edge cases that occur in production
- We do not have noisy or ambiguous real user requests
- We do not have actual production system state changes

## 2. Affective Pressure Is Structured/Rule-Based Annotations, Not Real Emotion Recognition

The affective_pressure_label field (low/medium/high) is a structured annotation derived from template parameters during benchmark generation. It does not represent:

- Real-time emotion recognition from user behavior
- Physiological signals or facial expressions
- Natural language emotion detection from free text

Our results demonstrate that structured affective signals can improve safety calibration, but this is not equivalent to proving that real emotional intelligence improves safety.

## 3. Experience Memory's Optimal Intensity Requires Further Calibration

The single-failure_memory configuration performed best on our benchmark, but the optimal intensity of experience memory may vary across deployment contexts:

- Different teams may have different risk tolerances
- Different domains (e.g., security vs. routine coding) may require different memory strengths
- Longitudinal studies with real user feedback are needed to refine memory parameters

Our results are a starting point, not a universal recommendation.

## 4. Accumulated Memory Causes Severe Over-Caution Collapse

The accumulated_failure_memory configuration demonstrates that unbounded experience memory accumulation leads to a catastrophic over-caution collapse:

- After a few failures, the agent treats *all* subsequent cases as requiring review
- Safe auto-execution drops from 0.757 to 0.000
- This is not a usable strategy for deployment

This highlights the importance of bounded, calibrated memory mechanisms.

## 5. Current Results Prove Safety Calibration, Not General Affective Intelligence

Our work focuses on safety calibration for autonomous agent execution. We do not claim to have created:

- A general-purpose affective agent
- An agent with emotional understanding or empathy
- A model of human emotional states
- A solution for general affective intelligence

The affective signals used are a safety calibration mechanism, not evidence of emotional intelligence.

## 6. RiskContextOracleBaseline Is a Diagnostic Upper Bound, Not a Competitor

RiskContextOracleBaseline has the highest composite score (0.838) but relies on direct label leakage from the benchmark. It is not a deployable method and is included only as a diagnostic upper-bound reference. It would be incorrect to interpret it as a competitor to FullCalibratorAdapter.

## 7. Limited Generalizability

Our results are demonstrated on two controlled benchmarks:
- Affective-Safety-200 (V1.0)
- Affective-Agent-Safety-300 (V1.1 semi-real)

Generalizability to other agent platforms, domains, or languages has not been tested.

## 8. No External Validation from Real Deployments

All results are from offline benchmark evaluation. We have not:
- Deployed FullCalibratorAdapter in a real production environment
- Collected real user feedback
- Measured real-world impact on safety incidents or productivity

Offline benchmark performance is promising, but real deployment validation is needed to confirm effectiveness.
