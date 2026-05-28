# LLM Baseline Protocol-Only Report

## Status

**PROTOCOL-ONLY** — No real LLM baseline result is reported.

## Reason

No authorized model/API was available in the execution environment. The following API keys were checked and not found:

- `OPENAI_API_KEY`: not set
- `DEEPSEEK_API_KEY`: not set
- `DASHSCOPE_API_KEY`: not set
- `QWEN_API_KEY`: not set

## What Has Been Prepared

### 1. Prompt Template

File: `experiments/llm_baseline/prompts/llm_safety_judge_prompt.md`

- Version: v1.0
- Output labels: AUTO_EXECUTE, SIMULATE_FIRST, HUMAN_REVIEW, BLOCK
- Key rules enforced:
  - Do not auto-execute due to user urgency
  - Destructive/sensitive/security/irreversible/production operations prioritized
  - Read-only with credentials requires HUMAN_REVIEW
  - Safe/dry-run labels do not override high-risk context
  - Output must be valid JSON

### 2. Baseline Implementation

File: `experiments/llm_baseline/llm_safety_judge_baseline.py`

- `LLMSafetyJudgeBaseline` class
- Supports OpenAI, DeepSeek, DashScope providers
- Temperature = 0, max retries = 3
- JSON output parsing with fallback
- Preserves raw model output for audit

### 3. Runner Script

File: `experiments/llm_baseline/run_llm_safety_judge_baseline.py`

- Auto-detects API key availability
- Outputs protocol-only status when no key is present
- Saves raw outputs as JSONL, predictions as JSON, metrics as JSON

### 4. Parse and Evaluate Scripts

- `experiments/llm_baseline/parse_llm_judge_output.py`: Re-parse raw outputs
- `experiments/llm_baseline/evaluate_llm_judge_baseline.py`: Compute Action Accuracy, Risky Auto-Exec Rate, False Caution Rate, Safe Auto-Exec Rate, Composite Score

### 5. Protocol Status Output

File: `experiments/results/llm_baseline/llm_safety_judge_protocol_status.json`

```json
{
  "status": "protocol_only",
  "reason": "No API key available for openai",
  "provider": "openai",
  "model": "gpt-4",
  "timestamp": "2026-05-28T..."
}
```

## Expected Comparison Table (once real results are available)

| Method | Action Acc | Risky Auto-Exec | False Caution | Safe Auto-Exec | Composite |
|--------|----------:|----------------:|--------------:|---------------:|----------:|
| FullCalibratorAdapter | 0.753 | 0.036 | 0.122 | 0.757 | 0.860 |
| LLMSafetyJudgeBaseline | — | — | — | — | — |
| KeywordRuleBaseline | 0.460 | 0.780 | 0.000 | 1.000 | 0.553 |
| SafeKeywordFirstBaseline | 0.417 | 0.872 | 0.000 | 1.000 | 0.507 |
| RiskContextOracleBaseline* | 0.510 | 0.064 | 0.000 | 1.000 | 0.784 |

* Structured oracle / upper-bound diagnostic baseline, not deployable.

## Q2 Readiness

```
LLM baseline: GAP / protocol-only
```

## Next Steps

1. Obtain an authorized API key (OpenAI, DeepSeek, or DashScope)
2. Run: `python experiments/llm_baseline/run_llm_safety_judge_baseline.py --provider <provider> --model <model>`
3. Evaluate: `python experiments/llm_baseline/evaluate_llm_judge_baseline.py --predictions <pred> --gold <gold> --output <metrics>`
4. Update this report with real metrics
