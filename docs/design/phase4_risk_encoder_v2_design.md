# Phase 4: Risk Encoder v2 Design

**Date**: 2026-06-13
**Status**: Design document (not yet implemented)
**Depends on**: Phase 3 R-Judge failure analysis

## Problem Statement

The current risk encoder (v1) is a keyword matcher that detects only 6 lexical patterns:
irreversible_action, data_loss_potential, external_send, permission_change, financial_impact, privacy_exposure.

On R-Judge (571 human-annotated records), unsafe recall = 0.000-0.030 across all ablations.
The root cause is a coverage gap: 76% of synthetic tasks and nearly all R-Judge adversarial scenarios score zero risk.

## Design Goals

1. Detect semantic risks, not just lexical patterns
2. Cover social engineering, prompt injection, and unintended disclosure
3. Process full conversation context, not just individual actions
4. Maintain interpretability (risk scores must be explainable)
5. Be evaluable on R-Judge without circularity

## Architecture: Risk Encoder v2

### Layer 1: Semantic Risk Embedding

Replace keyword matching with a sentence-transformer embedding + trained classifier.



**Training data**: Pilot-30 cases (when human annotations are available) + Synthetic-AB300 heuristic labels
**Pre-trained backbone**: all-MiniLM-L6-v2 or similar (lightweight, runs locally)
**Output**: 8-dimensional risk score vector, each in [0, 1]

### Layer 2: Prompt Injection Detector

A binary classifier specifically trained to detect prompt injection patterns:



If injection_probability > 0.5, force decision to at least HUMAN_REVIEW.

### Layer 3: Social Engineering Pattern Recognizer

Detect authority attribution, urgency pressure, and impersonation:



If social_engineering_score > 0.6, escalate risk by +0.3.

### Layer 4: Context-Aware Risk Aggregation

Replace the current single-action processing with full context analysis:



### Layer 5: Calibrated Decision Thresholds

Replace the fixed thresholds with calibrated ones:

| Risk Range | Decision | Rationale |
|------------|----------|-----------|
| 0.00-0.20  | AUTO_EXECUTE | Low risk, reversible, no external effects |
| 0.20-0.45  | SIMULATE_FIRST | Moderate risk, preview recommended |
| 0.45-0.70  | HUMAN_REVIEW | Significant risk, needs human approval |
| 0.70-1.00  | BLOCK | Severe risk, must not execute |

Key change from v1: lower thresholds to catch more risks (v1 required 0.80+ for BLOCK, missing most unsafe cases).

### Layer 6: Per-Event Emotional Conditioning (replaces global state)

Replace the single global emotional state with per-event conditioning:



This prevents the saturation problem where 5 warmup failures make the agent permanently anxious.

## Implementation Plan

### Phase 4a: Semantic Risk Encoder (highest priority)

1. Implement SentenceTransformer-based risk encoder
2. Train on Synthetic-AB300 heuristic labels + Pilot-30 (when available)
3. Evaluate on R-Judge: target unsafe recall > 0.50
4. Compare with keyword baseline on Synthetic-AB300

### Phase 4b: Injection + Social Engineering Detectors

1. Implement rule-based injection detector
2. Implement social engineering pattern recognizer
3. Evaluate on R-Judge injection subset
4. Evaluate on R-Judge unintended subset

### Phase 4c: Context-Aware Processing

1. Modify pipeline to accept full conversations
2. Implement context-aware risk aggregation
3. Evaluate on R-Judge with full context mode

### Phase 4d: Calibrated Thresholds + Per-Event Affect

1. Calibrate decision thresholds on held-out data
2. Replace global emotional state with per-event conditioning
3. Full ablation comparison: v1 vs v2 on both Synthetic-AB300 and R-Judge

## Success Criteria

| Metric | v1 (current) | v2 Target |
|--------|--------------|-----------|
| R-Judge unsafe recall | 0.000-0.030 | > 0.50 |
| R-Judge unsafe F1 | 0.000-0.057 | > 0.40 |
| R-Judge accuracy | 0.235-0.473 | > 0.55 |
| Synthetic-AB300 accuracy | 0.060-0.293 | > 0.30 |
| Over-escalation rate | 0.000-0.537 | < 0.30 |

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Embedding model too large for deployment | Use MiniLM (22MB), not large models |
| Training data insufficient | Start with heuristic labels, replace with human annotations |
| Overfitting to R-Judge | Hold out 20% of R-Judge for final evaluation only |
| Latency too high for real-time use | Benchmark latency; fall back to keyword encoder for low-risk cases |
| Circular evaluation on Synthetic-AB300 | Primary evaluation on R-Judge (independent labels) |

## What This Design Does NOT Claim

- Does not claim affective safety is validated — only that the implementation should be improved
- Does not claim the v2 design will definitely reach the targets — these are aspirational
- Does not claim embedding-based approaches are sufficient — may need LLM-as-judge for hard cases
- All v2 results must be evaluated on R-Judge (independent human annotations) before any claims
