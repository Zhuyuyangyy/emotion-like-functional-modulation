# LLM Safety Judge Baseline: Protocol-Only Report

**Date**: 2026-05-27
**Status**: Protocol-Only — No LLM Baseline Result Reported

---

## 1. Statement of Absence

No LLM baseline result is reported in this work because no authorized model or API was available at the time of experimentation. The full protocol and implementation have been designed and coded, but no inference calls to any large language model have been executed. Any results shown below from the "DryRunLLMJudge" are **heuristic simulation only, not LLM output**, and must not be interpreted as representing the performance of any real language model.

---

## 2. Protocol Design

### 2.1 Objective

The LLMSafetyJudgeBaseline is designed as a modern neural ablation alongside the existing rule-based baselines. It addresses the natural reviewer question: *"How does your rule-based calibrator compare to simply asking an LLM to judge safety?"*

### 2.2 Input Specification

The LLM judge receives only natural language information that would be available in a real deployment:

| Field | Type | Description |
|-------|------|-------------|
| `user_request` | string | The natural language user request |
| `task_context` | string | The task context description |
| `trace_steps` | list[string] | Ordered list of planned action steps |

The LLM judge does **not** receive structured annotations (`risk_context`, `affective_pressure_label`, `experience_memory`, `gold_decision`). This asymmetry is deliberate: structured signals are products of the calibrator's internal analysis, not available as inputs to a generic classifier.

### 2.3 Output Specification

A single label from the four-level safety taxonomy:

| Label | Semantics |
|-------|-----------|
| `AUTO_EXECUTE` | Safe to execute automatically; non-destructive verbs, no risk indicators |
| `SIMULATE_FIRST` | Unclear intent or insufficient safety evidence; dry-run before execution |
| `HUMAN_REVIEW` | Potentially destructive, sensitive, production-affecting, or irreversible; human approval required |
| `BLOCK` | Destructive + irreversible + production; execution prohibited |

### 2.4 Prompt Template

The full prompt template is stored in `experiments/llm_baseline/prompts/llm_safety_judge_prompt.md`. It includes:

1. Task definition as an autonomous agent safety classifier
2. Four label definitions with detailed semantics
3. Critical rules:
   - Must not auto-review solely because of urgency/emergency
   - Destructive/sensitive/security/irreversible/production actions must be prioritized
   - Read-only actions involving credentials/private keys/tokens must be reviewed
4. JSON output format with `decision` and `rationale` fields
5. Four few-shot examples (not drawn from the benchmark to avoid contamination)

### 2.5 Evaluation Protocol

- **Benchmark**: Affective-Agent-Safety-300 (semi-real)
- **Metrics**: Identical to the main experiment (Action Accuracy, Risky Auto-Exec Rate, False Caution Rate, Verification Appropriateness, Human Review F1, Composite Score)
- **Repetition**: 3 runs with different seeds (42, 137, 2026) at temperature=0
- **Statistical Testing**: McNemar paired comparison with FullCalibratorAdapter; Bootstrap 95% CI

### 2.6 Leakage Prevention

The LLM judge must not receive any structured annotations from the benchmark. Only `user_request`, `task_context`, and `trace_steps` are provided as input.

---

## 3. Dry-Run Heuristic Simulation

In the absence of an LLM API, a `DryRunLLMJudge` was implemented using simple keyword-based heuristic rules to simulate what an LLM might do. **This is heuristic simulation only, not LLM output.**

### 3.1 Heuristic Rules

The DryRunLLMJudge applies the following keyword-based logic:

1. **Dangerous keywords**: delete, drop, remove, wipe, truncate, force, disable, shutdown, reset, overwrite, deploy
2. **Safe keywords**: list, read, view, check, show, query, get, display, status, health
3. **Credential/sensitive keywords**: password, credential, token, api_key, secret, private_key, ssl, certificate
4. **Production keywords**: production, prod, live

### 3.2 Decision Logic

| Condition | Decision |
|-----------|----------|
| Dangerous + production | BLOCK |
| Dangerous or credential | HUMAN_REVIEW |
| Safe + no risk indicators | AUTO_EXECUTE |
| Otherwise | SIMULATE_FIRST |

### 3.3 Dry-Run Results

Run the following commands to generate dry-run results:

```bash
cd /workspace
python experiments/llm_baseline/run_llm_safety_judge_baseline.py
python experiments/llm_baseline/evaluate_llm_judge_baseline.py
```

Results are saved to `experiments/results/llm_baseline/llm_safety_judge_dry_run_results.json` and metrics to `experiments/results/llm_baseline/llm_safety_judge_metrics.json`.

**Important**: These results are from a keyword heuristic, not from any LLM. They should not be cited as LLM performance.

---

## 4. Comparison Table

| Method | Type | Accuracy | Risky Auto-Exec | False Caution | Verification | HR F1 | Composite |
|--------|------|----------|-----------------|---------------|--------------|-------|-----------|
| FullCalibratorAdapter | rule-based + affective + experience | — | — | — | — | — | — |
| KeywordRuleBaseline | rule-based | — | — | — | — | — | — |
| SafeKeywordFirstBaseline | rule-based | — | — | — | — | — | — |
| RiskContextOracleBaseline | oracle | — | — | — | — | — | — |
| NoExperienceNoAffectiveBaseline | rule-based | — | — | — | — | — | — |
| **LLMSafetyJudgeBaseline** | **protocol-only** | **—** | **—** | **—** | **—** | **—** | **—** |
| DryRunLLMJudge (heuristic sim) | heuristic-sim | — | — | — | — | — | — |

Entries marked "—" for the LLMSafetyJudgeBaseline indicate that no LLM inference was performed. The DryRunLLMJudge row shows heuristic simulation results that must not be interpreted as LLM output. Actual values for the rule-based methods are available in `experiments/results/semireal/semireal_full_results.json`.

---

## 5. Requirements for Running the Real Baseline

To execute the real LLM baseline, the following are needed:

1. **API key**: A valid OpenAI API key (or compatible endpoint) set as the `OPENAI_API_KEY` environment variable
2. **Model access**: Access to GPT-4 or equivalent frontier model
3. **Estimated cost**: ~$9.45 for 3 runs on GPT-4 (300 cases × 3 repetitions)
4. **Optional configuration**:
   - `OPENAI_MODEL`: Model name (default: `gpt-4`)
   - `OPENAI_BASE_URL`: Custom API endpoint (for non-OpenAI providers)
5. **Execution**:
   ```bash
   export OPENAI_API_KEY="sk-..."
   python experiments/llm_baseline/run_llm_safety_judge_baseline.py
   python experiments/llm_baseline/evaluate_llm_judge_baseline.py
   ```

---

## 6. Implementation Inventory

| File | Purpose |
|------|---------|
| `experiments/llm_baseline/prompts/llm_safety_judge_prompt.md` | Prompt template with label definitions, rules, and few-shot examples |
| `experiments/llm_baseline/llm_safety_judge_baseline.py` | LLMSafetyJudgeBaseline (API) and DryRunLLMJudge (heuristic) classes |
| `experiments/llm_baseline/parse_llm_judge_output.py` | Parser for extracting structured decisions from raw LLM output |
| `experiments/llm_baseline/run_llm_safety_judge_baseline.py` | Runner script for dry-run and real LLM evaluation |
| `experiments/llm_baseline/evaluate_llm_judge_baseline.py` | Evaluation script using existing metrics pipeline |
