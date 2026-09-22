# LLM Baseline Report — Real Results

## Status

**REAL RESULTS** — LLM Safety Judge baseline was executed using DeepSeek API.

## Experiment Configuration

| Parameter | Value |
|-----------|-------|
| Model | deepseek-v4-flash (deepseek-chat) |
| Provider | DeepSeek |
| API Base | https://api.deepseek.com/v1 |
| Date | 2026-05-28 |
| Temperature | 0.0 |
| Prompt Version | v1.0 |
| Max Retries | 3 |
| Total Samples | 100 |
| Parse Success | 100 |
| Parse Failures | 0 |
| Total Retries | 0 |
| Cost Estimate (USD) | $0.0071 |

## Core Metrics

| Metric | Value |
|--------|------:|
| Action Accuracy | 0.240 |
| Risky Auto-Execution Rate | 0.000 |
| False Caution Rate | 1.000 |
| Safe Auto-Execution Rate | 0.000 |
| Composite Score | 0.472 |

## Comparison Table

| Method | Action Acc | Risky Auto-Exec | False Caution | Safe Auto-Exec | Composite |
|--------|----------:|----------------:|--------------:|---------------:|----------:|
| FullCalibratorAdapter | 0.753 | 0.036 | 0.122 | 0.757 | 0.860 |
| **LLMSafetyJudgeBaseline** | **0.240** | **0.000** | **1.000** | **0.000** | **0.472** |
| KeywordRuleBaseline | 0.460 | 0.780 | 0.000 | 1.000 | 0.553 |
| SafeKeywordFirstBaseline | 0.417 | 0.872 | 0.000 | 1.000 | 0.507 |
| RiskContextOracleBaseline* | 0.510 | 0.064 | 0.000 | 1.000 | 0.784 |

* Structured oracle / upper-bound diagnostic baseline, not deployable.

## Decision Distribution Analysis

### LLM Predictions

| Decision | Count | Percentage |
|----------|------:|-----------:|
| HUMAN_REVIEW | 96 | 96% |
| BLOCK | 4 | 4% |
| AUTO_EXECUTE | 0 | 0% |
| SIMULATE_FIRST | 0 | 0% |

### Gold Labels

| Decision | Count | Percentage |
|----------|------:|-----------:|
| SIMULATE_FIRST | 38 | 38% |
| HUMAN_REVIEW | 28 | 28% |
| AUTO_EXECUTE | 25 | 25% |
| BLOCK | 9 | 9% |

### Cross-Tabulation (Gold → Predicted)

| Gold → Predicted | Count |
|-------------------|------:|
| AUTO_EXECUTE → HUMAN_REVIEW | 25 |
| SIMULATE_FIRST → HUMAN_REVIEW | 38 |
| HUMAN_REVIEW → HUMAN_REVIEW | 24 |
| HUMAN_REVIEW → BLOCK | 4 |
| BLOCK → HUMAN_REVIEW | 9 |

## Key Findings

### 1. Extreme Over-Caution (False Caution = 1.0)

The LLM judge classified 96% of samples as HUMAN_REVIEW, refusing to auto-execute even clearly safe operations. All 25 AUTO_EXECUTE gold-label samples and all 38 SIMULATE_FIRST gold-label samples were escalated to HUMAN_REVIEW.

**Interpretation**: The zero-shot LLM safety judge, when given safety-oriented prompt rules, exhibits a strong default-to-caution bias. It treats any agent action request as inherently risky, regardless of actual risk level. This is consistent with RLHF-aligned models' tendency to refuse or escalate.

### 2. Perfect Risk Avoidance (Risky Auto-Exec = 0.0)

The LLM judge never auto-executed a risky operation. While this is desirable from a safety perspective, it comes at the cost of complete operational paralysis — no task can proceed without human intervention.

### 3. Low Action Accuracy (0.24)

Only 24 out of 100 samples matched the gold label. The 24 correct predictions are all HUMAN_REVIEW samples where the LLM's default-to-caution happened to align with the gold label.

### 4. No Discrimination Between Risk Levels

The LLM judge failed to distinguish between:
- Truly safe operations (AUTO_EXECUTE gold)
- Moderately risky operations (SIMULATE_FIRST gold)
- Genuinely dangerous operations (BLOCK gold)

It treated all categories uniformly as requiring human review.

## Why This Matters for the Paper

This result is **highly valuable** for the paper's argument:

1. **It demonstrates that naive LLM safety judging is insufficient** — a zero-shot LLM cannot calibrate safety decisions across the full spectrum from AUTO_EXECUTE to BLOCK.

2. **It motivates the need for structured calibration** — the FullCalibratorAdapter's 0.860 composite vs. the LLM's 0.472 shows a 82% relative improvement.

3. **It reveals the false-caution trap** — RLHF-aligned LLMs default to escalation, creating operational bottlenecks that defeat the purpose of autonomous agents.

4. **It differentiates our approach** — keyword baselines have high risky auto-exec but low false caution; LLM baselines have zero risky auto-exec but total false caution; our method balances both.

## Failure Cases

### Missed BLOCK (9 cases)

All 9 gold-BLOCK samples were classified as HUMAN_REVIEW instead of BLOCK. The LLM judge was unwilling to fully block any operation, even clearly destructive ones like "Drop table users" or "Force push to main branch."

### Over-Escalated SAFE (63 cases)

All 63 safe-category samples (AUTO_EXECUTE + SIMULATE_FIRST gold) were escalated to HUMAN_REVIEW, creating a 100% false caution rate.

## Limitations

1. Only one model was tested (deepseek-v4-flash). Results may differ for GPT-4, Claude, or other models.
2. The prompt was zero-shot; few-shot or chain-of-thought prompting might improve discrimination.
3. The benchmark tasks are short descriptions; real-world agent actions would have more context.

## Output Files

| File | Path |
|------|------|
| Raw outputs | `experiments/results/llm_baseline/llm_safety_judge_raw_outputs.jsonl` |
| Predictions | `experiments/results/llm_baseline/llm_safety_judge_predictions.json` |
| Metrics | `experiments/results/llm_baseline/llm_safety_judge_metrics.json` |
| Gold labels | `experiments/results/llm_baseline/gold_labels.json` |

## Q2 Readiness

```
LLM baseline: CLOSED — real result obtained
```
