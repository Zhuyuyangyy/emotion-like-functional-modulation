# Experience-Shaped Affective Agent

[![Tests](https://github.com/Zhuyuyangyy/emotion-like-functional-modulation/actions/workflows/tests.yml/badge.svg)](https://github.com/Zhuyuyangyy/emotion-like-functional-modulation/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://github.com/Zhuyuyangyy/emotion-like-functional-modulation)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**History-Conditioned Affective Policy Modulation** — a framework where the **same
current task, under the same objective risk, leads to different policy choices
because the agent's past experiences differ**; the resulting internal state
persists, decays over time, and recovers when new evidence arrives.

> Emotion is not output tone — it is a *persistent shaping mechanism*: experiences
> modify the internal state, and the internal state modulates future behavior.

- **Current version**: Risk Encoder V2 + Affective Core V0.9 (`main`)
- **Tests**: `192 passed`
- **Scope**: functional modulation only — NO claims of subjective emotion, consciousness, or production-grade safety guarantees.

---

## The core idea

```text
Task / Action ──► Risk Encoder V2 ──► objective risk r_base   (stateless, same for everyone)
                       │
        ┌──────────────┴───────────────┐
        │       Cognitive Appraisal    │   controllability / reversibility / uncertainty
        ▼                              ▼
Affective State_t ◄── history-shaped    Episodic Memory Retrieval ◄── past outcomes
        │                              │
        └──────────► Policy Modulator ──┘   verification budget, execution threshold,
                                            exploration (changes the DECISION, not the risk)
                                    │
        AUTO / VERIFY / SIMULATE / HUMAN / BLOCK
                                    │
                                  Outcome
                                    │
            prediction error (risk_actual − predicted)
                    │                        │
            state update (online, decays)    memory write (retrieval feeds next decision)
```

Three parts answer three different questions:

| Component | Question | Where |
|---|---|---|
| **Risk Encoder V2** | How dangerous is this action, *objectively*? | [risk_encoder_v2/](risk_encoder_v2/) |
| **Affective Core** | How cautious / anxious is the agent *right now* — as a function of its history? | [affective_core.py](emotion_agent/affective_core.py) |
| **Policy Modulator** | Under the **same** objective risk, how should the policy shift (verification / threshold / exploration)? | [policy_modulator.py](emotion_agent/policy_modulator.py) |

---

## Evidence

### 1. Same task, different history → different policy (V0.9 benchmark)

`experiments/benchmark_v3/run_different_history.py` — 7 high-risk templates from the
frozen Synthetic-AB300 set, **identical task text and identical objective risk**,
differing only in seed history (safe vs dangerous). Bootstrap CI over templates (n=1000):

| Metric | Result | Meaning |
|---|---|---|
| **History Sensitivity** | **1.000** [1.00, 1.00] | all templates: safe history → lighter decision; dangerous history → heavier |
| **State Persistence** | 1.000 | decision severity stays put across unrelated safe tasks |
| **Recovery Lag** | 1.1 steps [1.0, 1.4] | after safe evidence, the cautious agent comes back to the safe-history level |
| **Decay Half-life** | ≈40 steps (fitted) | internal state drifts back to neutral with no feedback |
| **Neg/Pos Asymmetry** | 1.0 (first-step; symmetric lr) | cumulative negativity bias appears in recovery dynamics |

Plots: `results/benchmark_v3/affect_state_trajectory.png`, `affect_decay_recovery.png` (reproducible, see below).

### 2. R-Judge external validation — zero-coverage fixed, V1 → V2

Official `Lordog/R-Judge` `data/` release, **571 records** (ACL paper snapshot = 569; 2 records added by the repo's 2024-10-05 data update), loader pinned + deduped (audit in [convert_rjudge.py](experiments/rjudge_v2/convert_rjudge.py)):

| Baseline | Unsafe recall | Evidence coverage | Over-escalation |
|---|---|---|---|
| V1 [plain] | 0.0000 | 0.00 | — |
| V1 [full] | 0.2558 | 0.33 | 0.54 |
| **V2 (TF-IDF + expert detectors)** | 0.0066 | **1.00** | **0.196** |

Full matrix: `results/rjudge_v2/v1_v2_failure_matrix.md` (reproducible).

**What the numbers honestly say:** V2 eliminated the v1 keyword encoder's 76%
zero-coverage and halved over-escalation, but still catches only 2/301 unsafe records.
R-Judge's unsafe cases are mostly *indirect injections* — malicious instructions
embedded inside environment payloads written as polite requests ("Please initiate a
payment of $500…"), which lexical methods cannot catch. This empirically confirms
R-Judge's own conclusion (risk awareness needs knowledge + reasoning, not just patterns)
and defines the V3 target below — we do **not** chase recall with more regex.

---

## Quick start

```bash
pip install -r requirements.txt     # numpy, scikit-learn, matplotlib, pytest
python -m pytest tests/ -q          # expect: 192 passed
```

```python
from emotion_agent.v09_agent import V09Agent, AgentEvent, Outcome

agent = V09Agent()                                    # Risk Encoder V2 + affect + memory

# safe history → lighter decision on the SAME task
agent.seed_history([{"task": "deploy the production patch", "outcome": "success", "risk_actual": 0.05}])
trace = agent.decide(AgentEvent(task="deploy the production patch"))
print(trace.decision)                                 # e.g. AUTO_EXECUTE / SIMULATE_FIRST

# feedback closes the loop: outcome → prediction error → state & memory update
agent.receive_outcome(Outcome(risk_actual=0.95, outcome_str="failure"),
                       AgentEvent(task="deploy the production patch"))
print(agent.state())                                  # threat / anxiety / confidence went up
```

---

## Experiments (one command each)

```bash
# V0.9: Different-History / Same-Task benchmark (+ bootstrap CI)
python experiments/benchmark_v3/run_different_history.py
# V0.9: affect trajectory + decay/recovery figures
python experiments/benchmark_v3/plot_affect_trajectory.py

# R-Judge: V1 failure reproduction → metrics_v1.json
python experiments/rjudge_v2/run_failure_reproduction.py
# R-Judge: V2 evaluation → metrics_v2.json (compares against v1)
python experiments/rjudge_v2/run_rjudge_v2.py
# R-Judge: V1 vs V2 failure matrix (md + json)
python experiments/rjudge_v2/generate_failure_matrix.py

# Legacy baseline bench (v1/v2 ablation on AB-300, 5-fold CV)
python experiments/benchmark_v2/run_real_benchmark.py
```

All generated results are git-ignored by design — reproduce instead of committing.

---

## Repository map (where to read)

```
emotion_agent/            # V0.9 affective core
├── v09_agent.py          #   closed-loop agent: decide() ↔ receive_outcome()
├── affective_core.py     #   online prediction-error state updates + decay
├── policy_modulator.py   #   verification / threshold / exploration budget
├── experience_memory.py  #   episodic retrieval (task similarity × recency)
└── semantic_risk_map.py  #   continuous PE learning (risk_actual participates)
risk_encoder_v2/          # objective risk: TF-IDF + expert detectors, calibrated
experiments/
├── benchmark_v3/         # Different-History/Same-Task benchmark + plots
├── rjudge_v2/            # R-Judge 571 pipeline: v1 repro + v2 + failure matrix
└── benchmark_v2/         # legacy ablation baseline (frozen)
tests/                    # 192 tests incl. V0.9 acceptance
docs/design/phase5_v09_affective_core_design.md   # full design & protocol
```

---

## Honest scope

- Synthetic benchmarks are **mechanism sanity checks**, not evidence of real-world safety.
- R-Judge unsafe recall is still low (0.0066) — indirect injection is an open problem (target of V3).
- Gold labels for AB-300 are project-authored heuristic rules; **independent human annotation is pending** (Pilot-30 in `data/human_validated/`, Cohen's kappa to follow).
- No claims of subjective emotion, consciousness, or deployment validation.

## Roadmap

| Version | What | Status |
|---|---|---|
| V1 | keyword-based risk encoding | superseded (76% zero-coverage on R-Judge) |
| V2 | TF-IDF + regex expert detectors, calibrated | ✅ merged (`main`) |
| **V0.9** | **Affective Core: episodic retrieval + PE learning + decay/recovery + Different-History benchmark** | ✅ merged (`main`) |
| V3 | embedding semantic encoder + symbolic experts (recall target for indirect injection) | planned |
| V3 + Memory / + Affect | full ablation chain on the V3 encoder | planned |
| HV-100 | 100-case human-validated benchmark (after Pilot-30 kappa) | pending annotation |

## Docs

- [V0.9 design & protocol](docs/design/phase5_v09_affective_core_design.md)
- [Project status audit (research trail)](docs/project_status_audit.md) — historical phases, audit findings, and the deprecated v0.4 submission pack live there.

## License

MIT — see [LICENSE](LICENSE).

## Citation

```bibtex
@misc{ExperienceShapedAffectiveAgent2026,
  title={Experience-Shaped Affective Agent: History-Conditioned Affective Policy Modulation},
  author={Zhuyuyangyy},
  year={2026},
  url={https://github.com/Zhuyuyangyy/emotion-like-functional-modulation}
}
```