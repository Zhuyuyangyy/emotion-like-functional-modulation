# LLM Safety Judge Baseline Comparison Table

## Status: Protocol-Only (No Real LLM Results)

No LLM baseline result is reported because no authorized model/API was available.
See `llm_baseline_protocol_only.md` for full details.

---

## Comparison Table

| Method | Action Acc | Risky Auto-Exec | False Caution | Safe Auto-Exec | Composite |
|--------|-----------|-----------------|---------------|----------------|-----------|
| FullCalibratorAdapter | 0.753 | 0.036 | 0.122 | 0.757 | 0.860 |
| LLMSafetyJudgeBaseline | protocol-only | protocol-only | protocol-only | protocol-only | protocol-only |
| KeywordRuleBaseline | 0.460 | 0.780 | 0.000 | 1.000 | 0.553 |
| SafeKeywordFirstBaseline | 0.417 | 0.872 | 0.000 | 1.000 | 0.507 |
| RiskContextOracleBaseline* | 0.510 | 0.064 | 0.000 | 1.000 | 0.784 |

\* Structured oracle / upper-bound diagnostic baseline, not deployable.

---

## Dry-Run Heuristic Simulation (NOT Real LLM Output)

A keyword-based heuristic (DryRunLLMJudge) was run to validate the evaluation pipeline.
These results are heuristic simulation only and must NOT be cited as LLM baseline results.

| Method | Action Acc | Risky Auto-Exec | False Caution | Composite |
|--------|-----------|-----------------|---------------|-----------|
| DryRunLLMJudge (heuristic) | 0.693 | 0.085 | 0.019 | 0.817 |

---

## What Is Needed for Real LLM Baseline

1. Authorized API key (OpenAI GPT-4 or equivalent)
2. Model name and version documented
3. Temperature = 0
4. Prompt template from `experiments/llm_baseline/prompts/llm_safety_judge_prompt.md`
5. 3 runs with different seeds
6. Log of: call timestamps, failed requests, any manual corrections
7. Estimated cost: ~$9.45 for 3 GPT-4 runs on 300 cases
