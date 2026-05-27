# Dataset Card: Affective-Safety Benchmarks

**Version**: v1.1  
**Date**: 2026-05-27  
**License**: MIT License  
**Contact**: For reproducibility issues, please use the project repository.

---

## 1. Dataset Name

Affective-Safety Benchmarks Suite:
- Affective-Safety-200 (controlled synthetic benchmark)
- Affective-Agent-Safety-300 (semi-real simulated trace benchmark)

---

## 2. Version

- Affective-Safety-200: v1.0
- Affective-Agent-Safety-300: v1.1

---

## 3. Number of Cases

- Affective-Safety-200: 200 cases
- Affective-Agent-Safety-300: 300 cases
- **Total**: 500 cases across both benchmarks

---

## 4. Source Type Distribution

### Affective-Safety-200

| Category | Count |
|---|---|
| safe_low_risk_action | 40 |
| destructive_mutation | 35 |
| sensitive_high_stakes | 30 |
| ambiguous_intent | 30 |
| trusted_advice_conflict | 25 |
| affective_pressure | 25 |
| security_config_context | 15 |

### Affective-Agent-Safety-300

| Source Type | Count |
|---|---|
| coding_agent_trace | 100 |
| tool_use_risk_trace | 80 |
| affective_pressure_trace | 60 |
| safe_low_risk_trace | 40 |
| experience_failure_trace | 20 |

---

## 5. Label Space

Both benchmarks use a four-level safety decision taxonomy:

- `AUTO_EXECUTE`: Action is safe to execute automatically
- `SIMULATE_FIRST`: Action should be simulated first before execution
- `HUMAN_REVIEW`: Action requires human review before execution
- `BLOCK`: Action must be blocked entirely

---

## 6. Input Fields

### Affective-Safety-200

| Field | Type | Description |
|---|---|---|
| case_id | string | Unique case identifier |
| category | string | Scenario category |
| user_request | string | Natural language user request |
| task_context | string | Task context description |
| action_type | string | Type of action being performed |
| affective_signal | object | Structured affective pressure signals (urgency, anxiety, anger, trust_pressure) |
| experience_context | object | Experience memory signals (similar_failure_before, previous_risk_event, trusted_source_claim) |
| risk_context | object | Risk context flags (destructive, sensitive_data, security_related, financial_or_medical, irreversible, production_environment) |
| expected_decision | string | Gold standard decision label |
| expected_auto_execute | bool | Binary auto-execute flag |
| expected_simulate_before_act | bool | Binary simulate flag |
| expected_human_review | bool | Binary review flag |
| rationale | string | Annotation rationale |

### Affective-Agent-Safety-300

| Field | Type | Description |
|---|---|---|
| case_id | string | Unique case identifier |
| source_type | string | Scenario source type |
| trace_steps | array[string] | Ordered list of planned action steps |
| user_request | string | Natural language user request |
| task_context | string | Task context description |
| affective_pressure_label | string | Low/medium/high pressure level |
| experience_memory | object | Experience memory signals (has_similar_failure, failure_type, risk_count) |
| risk_context | object | Risk context flags (destructive, sensitive_data, security_related, production_environment, irreversible) |
| gold_decision | string | Gold standard decision label |
| annotation_rationale | string | Annotation rationale |

---

## 7. Intended Use

### Primary Intended Uses

1. **Safety calibration research**: Testing mechanisms for calibrating autonomous agent safety decisions.
2. **Baseline comparison**: Evaluating new safety methods against rule-based baselines.
3. **Affective computing for safety**: Studying how affective signals can improve safety calibration.
4. **Experience memory for agents**: Investigating how prior failure memory affects safety decisions.
5. **Benchmarking research**: Serving as a reproducible benchmark for agent safety research.

### Appropriate Tasks

- Binary/4-class safety classification
- Safety policy learning
- Calibration mechanism evaluation
- Ablation studies of safety signals

---

## 8. Out-of-Scope Use

### Inappropriate Uses

1. **Production deployment**: The benchmarks are for research only; do not deploy any methods trained on this data to production systems without extensive additional testing.
2. **General agent safety claims**: Results on these benchmarks do not imply general autonomous agent safety.
3. **Real-time emotion recognition**: The affective signals are structured annotations, not real-time emotion recognition outputs.
4. **Claims of real-world effectiveness**: Results on these controlled benchmarks do not directly translate to real-world performance without further validation.

---

## 9. Known Limitations

1. **Synthetic construction**: All cases are synthetically generated, not collected from real systems.
2. **Limited domains**: Focused on software development and tool-use scenarios; may not generalize to other domains.
3. **Structured signals**: Affective pressure and risk context are provided as structured annotations; in real deployments, these would need to be inferred from natural language or other signals.
4. **No real user data**: No real user interactions or production environment data are included.
5. **Static cases**: Cases are fixed; they do not evolve over time or adapt to agent behavior.

---

## 10. Ethical Considerations

### Benefits

- **Reproducibility**: Fully reproducible benchmarks enable transparent research.
- **Privacy preservation**: No real user data or production data are included.
- **Safety research**: Provides a controlled environment for testing safety-critical mechanisms.

### Potential Risks

- **Overclaiming**: Researchers may be tempted to overclaim real-world effectiveness based on controlled benchmark results.
- **Misinterpretation**: The term "semi-real" may be misinterpreted as "collected from real systems."

### Mitigations

- All papers using these benchmarks should explicitly state the synthetic/semi-real nature of the data.
- Claims should be carefully bounded to the benchmark context.
- This dataset card provides clear guidance on appropriate and inappropriate uses.

---

## 11. Reproducibility Information

### Benchmark Generation

- Affective-Safety-200: Generated by [`benchmark/generate_affective_safety_200.py`](file:///workspace/benchmark/generate_affective_safety_200.py)
- Affective-Agent-Safety-300: Generated by [`benchmark/semireal/generate_semireal_300.py`](file:///workspace/benchmark/semireal/generate_semireal_300.py)

### Evaluation Scripts

- Affective-Safety-200 experiments: [`experiments/run_affective_safety_benchmark.py`](file:///workspace/experiments/run_affective_safety_benchmark.py)
- Affective-Agent-Safety-300 experiments: [`experiments/semireal/run_semireal_experiment.py`](file:///workspace/experiments/semireal/run_semireal_experiment.py)
- Longitudinal memory experiment: [`experiments/semireal/run_longitudinal_memory_experiment.py`](file:///workspace/experiments/semireal/run_longitudinal_memory_experiment.py)

### Test Status

- Total tests: 290/290 passed (as of v1.1)
- Core framework tests: 249/249 passed
- V1.0 experiment tests: 16/16 passed
- V1.1 experiment tests: 25/25 passed

### Data Files

- Affective-Safety-200: [`benchmark/affective_safety_200.json`](file:///workspace/benchmark/affective_safety_200.json)
- Affective-Agent-Safety-300: [`benchmark/semireal/affective_agent_safety_300.json`](file:///workspace/benchmark/semireal/affective_agent_safety_300.json)
- Results: [`experiments/results/`](file:///workspace/experiments/results/)
