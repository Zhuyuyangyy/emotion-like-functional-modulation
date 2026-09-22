# Cover Letter Draft

> **Deprecated historical draft.** The claims in this file were written before the Phase 0–1R audit. Do not treat Semi-Real-300, Q2 BORDERLINE+, or the old main-table metrics as current reproducible evidence.

Dear Editor,

We are pleased to submit our manuscript entitled "Experience-Shaped Affective Safety Calibration for Autonomous Agents" for consideration in [Journal Name].

## Summary

Autonomous agents operating in real-world environments must balance safety and utility. Overly aggressive agents may execute dangerous operations automatically, while overly cautious agents become operationally paralyzed. We propose a structured affective safety calibration framework that integrates cognitive appraisal, affective memory, and hesitation policies to achieve a balanced safety-utility tradeoff.

## Key Contributions

1. A model-agnostic framework for affective safety calibration that works with any LLM or agent architecture
2. A semi-real benchmark (Affective-Agent-Safety-300) with 300 cases across 5 risk categories for evaluating safety decisions
3. Empirical evidence that structured calibration achieves a composite score of 0.860, outperforming keyword-based baselines (0.507-0.553) on the same benchmark
4. An auxiliary stress test demonstrating that a zero-shot LLM safety judge tends toward extreme over-escalation (92% false caution rate), motivating the need for calibrated safety-utility balance

## Methodological Rigor

We have taken the following steps to ensure research integrity:
- All experimental results are obtained from real benchmark evaluations, not simulated or fabricated
- A data authenticity statement and reproducibility audit accompany this submission
- A dataset equivalence audit clarifies that the LLM stress test was conducted on a regenerated benchmark variant, not the same Semi-Real-300 used in the main comparison
- We explicitly note that independent annotation reliability (Cohen's kappa) is pending, and labels are described as structured benchmark labels rather than expert-consensus labels

## Limitations We Acknowledge

- The LLM safety judge stress test uses a regenerated 300-case benchmark variant rather than the original Semi-Real-300, and is included as an auxiliary analysis only
- Independent inter-annotator agreement has not yet been established
- No real-world deployment validation data is available at this stage

## Suitability

We believe this work is suitable for [Journal Name] because it addresses the emerging challenge of safety calibration in autonomous agent systems, an area of growing importance as AI agents are increasingly deployed in safety-critical settings. Our framework provides a practical, model-agnostic approach that can be integrated with existing agent architectures.

Thank you for your consideration. We look forward to your feedback.

Sincerely,
[Author Names]
[Institution]
[Contact Information]
