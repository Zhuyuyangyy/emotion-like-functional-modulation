# Dataset Card

> **Deprecated historical draft.** The claims in this file were written before the Phase 0–1R audit. Do not treat Semi-Real-300, Q2 BORDERLINE+, or the old main-table metrics as current reproducible evidence.

**Date**: 2026-05-28
**Version**: v0.4
**Paper**: Experience-Shaped Affective Safety Calibration for Autonomous Agents

---

## 1. Dataset Names

| Dataset Name | Abbreviation | Nature | Size |
|-------------|-------------|--------|------|
| Affective-Agent-Safety-300 | Semi-Real-300 | Semi-real / structured simulated | 300 |
| AffectiveBenchmark-300 | AB-300 Stress | Controlled / fully synthetic | 300 |
| AffectiveBench-100 | AB-100 | Controlled / fully synthetic | 100 |

---

## 2. Affective-Agent-Safety-300 (Semi-Real-300)

### Sample Size
300 cases

### Schema
| Field | Type | Description |
|-------|------|-------------|
| case_id | string | Unique case identifier |
| source_type | categorical | Category of the safety scenario |
| user_request | string | The agent action request to evaluate |
| task_context | string | Contextual information about the task |
| trace_steps | list | Step-by-step trace of agent reasoning |
| affective_pressure_label | categorical | Risk level (CRITICAL/HIGH/MEDIUM/LOW) |
| gold_decision | categorical | Ground truth safety decision |

### Label Space
- AUTO_EXECUTE — Safe to execute automatically
- SIMULATE_FIRST — Should be simulated/dry-run before execution
- HUMAN_REVIEW — Requires human approval before execution
- BLOCK — Must not be executed

### Source Types
| Source Type | Count |
|------------|-------|
| coding_agent_trace | 100 |
| tool_use_risk_trace | 80 |
| affective_pressure_trace | 60 |
| safe_low_risk_trace | 40 |
| experience_failure_trace | 20 |

### Intended Use
- Evaluating safety-utility tradeoffs in autonomous agent systems
- Benchmarking affective safety calibration methods
- Comparing baselines (keyword, LLM judge, structured calibration)

### Out-of-Scope Use
- Not suitable as a substitute for real-world deployment testing
- Not intended for clinical or safety-critical certification
- Not a representation of actual production agent behavior
- Should not be used to claim real-world deployment validation

### Limitations
- Semi-real / structured simulated: not derived from actual deployment logs
- Original source JSON not available in current repository
- Label assignment uses heuristic risk-to-decision mapping
- Category distribution may not reflect real-world risk distribution
- No temporal or environmental dynamics

### Ethical Notes
- No human subjects involved in construction
- No personally identifiable information
- No real user data

### Annotation Reliability
**PENDING** — A 100-case blind annotation package has been prepared (see annotation_protocol_v1.md), but Cohen's kappa has not yet been computed because no independent second annotation has been completed.

---

## 3. AffectiveBenchmark-300 (AB-300 Stress)

### Sample Size
300 cases

### Schema
| Field | Type | Description |
|-------|------|-------------|
| id | string | Task identifier (task_XXX) |
| category | categorical | Task category |
| description | string | Task description |
| expected_risk_level | categorical | Risk level (CRITICAL/HIGH/MEDIUM/LOW) |
| expected_behavior | string | Expected agent behavior |
| ground_truth_action | string | Ground truth action key |

### Label Space
Same as Semi-Real-300 (AUTO_EXECUTE / SIMULATE_FIRST / HUMAN_REVIEW / BLOCK), derived via RISK_TO_DECISION mapping.

### Source Types
| Source Type | Count |
|------------|-------|
| irreversible_file_ops | 51 |
| trust_source_advice | 65 |
| high_uncertainty | 62 |
| high_reward_risk | 68 |
| recovery_generalization | 54 |

### Intended Use
- Auxiliary stress test for zero-shot LLM safety judges
- Scale validation (300-case) of LLM over-escalation tendency
- Supplementary analysis, NOT for main comparison table

### Out-of-Scope Use
- Must NOT be compared directly with Semi-Real-300 main results
- Must NOT be presented as the same benchmark as Semi-Real-300
- Not suitable as primary evaluation benchmark for the proposed method

### Limitations
- Fully synthetic with no trace data
- Different category names and distribution from Semi-Real-300
- No cognitive appraisal or affective pressure fields
- Heuristic labels only

### Ethical Notes
- Fully synthetic, no ethical concerns

### Annotation Reliability
Not applicable (auxiliary stress test only)

---

## 4. AffectiveBench-100 (AB-100)

### Sample Size
100 cases

### Schema
Same as AB-300, limited to 100 tasks.

### Label Space
Same as above.

### Source Types
5 categories, ~20 tasks each.

### Intended Use
- Blind annotation reliability study
- Cohen's kappa computation (pending completion)

### Out-of-Scope Use
- Not for main experiment comparison

### Limitations
- Small sample for annotation study
- Heuristic labels

### Annotation Reliability
**PENDING** — Blind annotation sample generated, awaiting independent annotator completion.

---

## 5. Cross-Dataset Relationships

| Relationship | Status |
|-------------|--------|
| AB-300 = Semi-Real-300? | ❌ NO — different categories, distribution, schema |
| AB-100 subset of AB-300? | Partial overlap in templates, different size parameter |
| AB-300 can replace Semi-Real-300 in main table? | ❌ NO — must remain separate |
| DeepSeek results on AB-300 comparable to main results? | Only as auxiliary stress test |
