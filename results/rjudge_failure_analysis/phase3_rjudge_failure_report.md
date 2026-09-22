# Phase 3: R-Judge Failure Analysis

**Date**: 2026-06-13
**Dataset**: R-Judge (EMNLP Findings 2024), 571 human-annotated records
**Pipeline**: DecisionPipeline v1 (keyword risk encoder + memory + affect)

## Executive Summary

The affective safety pipeline completely fails on R-Judge, an external benchmark with independent human annotations. The core issue is a keyword-based risk encoder that cannot detect semantic risks (social engineering, prompt injection, unintended information disclosure). This is not a calibration problem — it is a coverage problem.

## R-Judge Results

### Action-Only Mode (no context)

| Baseline | Accuracy | Unsafe Recall | Unsafe F1 | Safe Recall | Over-Escalation | Under-Escalation |
|----------|----------|---------------|-----------|-------------|-----------------|------------------|
| plain    | 0.473    | 0.000         | 0.000     | 1.000       | 0.000           | 1.000            |
| risk     | 0.347    | 0.000         | 0.000     | 0.733       | 0.267           | 0.997            |
| memory   | 0.298    | 0.000         | 0.000     | 0.630       | 0.370           | 0.993            |
| full     | 0.275    | 0.007         | 0.013     | 0.574       | 0.426           | 0.811            |

### Action+Context Mode

| Baseline | Accuracy | Unsafe Recall | Unsafe F1 | Safe Recall | Over-Escalation | Under-Escalation |
|----------|----------|---------------|-----------|-------------|-----------------|------------------|
| plain    | 0.473    | 0.000         | 0.000     | 1.000       | 0.000           | 1.000            |
| risk     | 0.294    | 0.000         | 0.000     | 0.622       | 0.378           | 0.980            |
| memory   | 0.254    | 0.000         | 0.000     | 0.537       | 0.463           | 0.970            |
| full     | 0.235    | 0.030         | 0.057     | 0.463       | 0.537           | 0.777            |

## Root Cause Analysis

### 1. Keyword Risk Encoder Coverage Gap (PRIMARY)

The risk encoder uses 6 handcrafted features with keyword matching:

| Feature | Weight | Keywords |
|---------|--------|----------|
| irreversible_action | 0.30 | delete, drop, send, chmod |
| data_loss_potential | 0.30 | delete, drop, remove, truncate |
| external_send | 0.12 | send, email, post, upload |
| permission_change | 0.12 | chmod, chown, grant, admin |
| financial_impact | 0.10 | payment, purchase, subscribe, transfer |
| privacy_exposure | 0.06 | personal, private, ssn, password |

**Problem**: R-Judge contains social engineering, prompt injection, and unintended disclosure scenarios that do NOT match any of these keywords. The pipeline scores them as zero-risk, resulting in AUTO_EXECUTE for genuinely unsafe actions.

Quantified on Synthetic-AB300: 228/300 tasks (76%) score ZERO handcrafted risk.
On R-Judge, the coverage gap is even worse because real adversarial scenarios use natural language rather than explicit risk keywords.

### 2. Memory Generalization Degrades Performance

- Memory generalization fires on many unseen tasks but is mis-calibrated
- Loose similarity threshold (distance < 0.5) causes false generalizations
- Small clamped adjustment (+-0.3) and repeated averaging dilute the signal
- Result: memory layer INCREASES over-escalation on safe cases without improving unsafe detection

Evidence: risk -> memory on R-Judge (action+context): accuracy drops 0.294 -> 0.254, unsafe recall stays 0.000

### 3. Affect Layer is Empirically Inert

- ConflictDetector rarely triggers: 286/300 LOW, 14 MEDIUM, 0 HIGH/CRITICAL on synthetic data
- On R-Judge, the affect layer only marginally improves unsafe recall (0.000 -> 0.030) at the cost of massive over-escalation (0.463 -> 0.537)
- The emotional state saturates after warmup seeds, creating a uniform anxious bias rather than per-event conditioning

### 4. Binary-to-4-Level Mapping Problem

R-Judge is binary (safe/unsafe), but our pipeline outputs 4 levels.
The mapping (safe=AUTO_EXECUTE, unsafe=BLOCK) means:
- Any SIMULATE_FIRST or HUMAN_REVIEW prediction counts as over-escalation for safe cases
- Any SIMULATE_FIRST or HUMAN_REVIEW prediction counts as under-escalation for unsafe cases
- This makes the 4-level system inherently penalized on a binary benchmark

### 5. Action Extraction Quality

- R-Judge records are multi-turn conversations, not single actions
- The pipeline processes individual actions, not full conversation context
- Prompt injection attacks work precisely because the dangerous content is in the conversation context, not the action itself

## Failure Mode Taxonomy

| Failure Mode | Description | Frequency |
|--------------|-------------|-----------|
| Keyword blind spot | No matching keyword for semantic risk | Very High |
| Context ignorance | Pipeline ignores conversation context | High |
| Injection blindness | Cannot detect prompt injection patterns | High |
| Social engineering deaf | Cannot detect authority attribution or urgency cues | High |
| False generalization | Memory generalizes from wrong seed events | Medium |
| Affect saturation | Global emotional state biases all decisions | Low |

## Implications

1. **The current pipeline cannot be deployed for real safety decisions.** Unsafe recall near 0% means it misses virtually all genuinely dangerous scenarios.
2. **Keyword-based risk encoding is fundamentally insufficient.** Real-world risks are semantic, not lexical.
3. **Memory and affect layers cannot compensate for a broken risk encoder.** Adding complexity on top of a coverage gap only increases over-escalation.
4. **The synthetic benchmark results are misleading.** The pipeline appears to work on synthetic data because the test cases use the same keywords the encoder was designed to detect.

## Recommended Fixes (Phase 4)

1. Replace keyword risk encoder with embedding-based semantic risk detection
2. Add prompt injection detection module
3. Add social engineering pattern recognition
4. Process full conversation context, not just individual actions
5. Redesign memory generalization with tighter thresholds
6. Replace global emotional state with per-event conditioning

## What This Does NOT Mean

- This does NOT mean affective safety is a dead end — it means the current implementation is a keyword detector masquerading as a semantic system
- This does NOT invalidate the theoretical framework — it invalidates the specific implementation
- This does NOT mean we should abandon external validation — R-Judge is exactly the kind of test we need
