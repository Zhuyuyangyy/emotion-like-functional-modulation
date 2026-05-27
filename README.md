# Experience-Shaped Affective Agent

[![Test Status](https://img.shields.io/badge/tests-110%20passed-brightgreen)]()
[![Version](https://img.shields.io/badge/version-0.8-blue)]()

## Overview

Experience-Shaped Affective Agent is a model-agnostic framework for **emotion-like behavioral modulation**. It implements functional mechanisms inspired by affective psychology to shape an agent's behavior based on its experiences.

**Core Proposition:**

> Emotion is not output tone, but a persistent shaping mechanism where experiences modify future behavior.

## Key Features

### 1. Cognitive Appraisal Vector
Multi-dimensional consequence evaluation that distinguishes between controllable vs irreversible failures, external betrayal vs internal mistakes, and high vs low uncertainty threats.

### 2. Interoceptive Self-State
Continuous internal state representation including threat, anxiety, confidence, trust, fatigue, curiosity, and control need.

### 3. Affective Memory
Experience storage weighted by severity, irreversibility, and prediction error magnitude.

### 4. Decay & Recovery
Affective states exhibit time inertia with natural decay, evidence-driven recovery (slower than collapse), and high-weight memories decaying slower.

### 5. Affective Generalization
Emotional influence propagation to similar events based on handcrafted features.

### 6. Conflict & Hesitation
Observable intermediate actions for high-conflict scenarios: simulate first, create backup, request human review.

### 7. LLM Integration (Mock)
Affectively modulated planning with prompt injection, output validation, and model-agnostic architecture.

### 8. Benchmark Suite
100-task evaluation with 4 baselines and 6 metrics including False Over-Caution Rate.

## Project Structure

```
src/affective_agent/
├── __init__.py                # Package exports
├── event_parser.py            # Event description parser
├── consequence_evaluator.py   # Cognitive appraisal evaluation
├── self_state_manager.py      # Interoceptive self-state management
├── affective_memory.py        # Emotion-weighted memory storage
├── policy_modulator.py        # Strategy parameter modulation
├── mock_llm_planner.py        # Mock LLM planner for testing
├── agent_core.py              # Agent core loop
├── affective_decay.py         # Affective state decay strategies
├── recovery_policy.py         # Evidence-driven recovery
├── state_trajectory_logger.py # State trajectory recording
├── event_similarity.py        # Event similarity calculation (V0.3)
├── affective_spread.py        # Emotional influence propagation (V0.3)
├── semantic_risk_map.py       # Risk prediction based on semantics (V0.3)
├── conflict_detector.py       # Reward-risk conflict detection (V0.4)
├── hesitation_policy.py       # Intermediate action generation (V0.4)
├── counterfactual_simulator.py # What-if analysis (V0.4)
├── provider_openai.py         # Mock OpenAI provider (V0.5)
├── prompt_modulator.py        # State-aware prompt injection (V0.5)
├── llm_output_guard.py        # Output validation and sanitization (V0.5)
├── llm_planner.py             # Affectively modulated planning (V0.5)
├── affective_benchmark.py     # 100-task evaluation suite (V0.6)
└── phoenix_agent_shield.py    # Phoenix-Evo/AgentShield integration (V0.7)

demos/
├── demo_pain_memory.py        # V0.1: Pain memory effect
├── demo_trust_collapse.py     # V0.1: Trust collapse effect
├── demo_anxiety_control.py    # V0.1: Anxiety control effect
├── demo_fear_decay.py         # V0.2: Fear decay over time
├── demo_trust_recovery.py     # V0.2: Trust recovery with evidence
└── run_all.py                 # Run all demos

tests/                         # 110 tests, all passing
docs/                          # Version specs and acceptance reports
benchmark/                     # Benchmark scripts
```

## Installation

```bash
git clone https://github.com/Zhuyuyangyy/emotion-like-functional-modulation.git
cd emotion-like-functional-modulation
pip install pytest
```

## Quick Start

```python
from affective_agent import AffectiveAgent

agent = AffectiveAgent()

# Perceive an event
event = agent.perceive_event("delete important database file")

# Evaluate consequences
consequence = agent.evaluate_consequence(event)

# Update self-state
state = agent.update_self_state(consequence)

# Write affective memory
memory = agent.write_affective_memory(event, consequence, "negative")

# Decide action
policy, action = agent.decide_action(event, "Proceed with deletion")
print(f"Risk threshold: {policy.risk_threshold}")
print(f"Verification steps: {policy.verification_steps}")
print(f"Auto execute: {policy.auto_execute}")
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Version Roadmap

| Version | Status | Description |
|---------|--------|-------------|
| **V0.1** | ✅ | Rule-based affective modulation loop |
| **V0.2** | ✅ | Decay & Recovery mechanisms |
| **V0.3** | ✅ | Affective Generalization |
| **V0.4** | ✅ | Conflict & Hesitation behavior |
| **V0.5** | ✅ | LLM Integration (mock) |
| **V0.6** | ✅ | Benchmark suite (100 tasks) |
| **V0.7** | ✅ | Phoenix-Evo/AgentShield integration (adapter-level) |
| **V0.8** | ✅ | Complete system integration |
| **V0.8.1** | ✅ | Audit & Evidence Lock |
| **V0.9** | 📋 | AffectiveBench formal validation |
| **V1.0** | 📋 | Paper/technical report submission |

## Important Claims

### NOT Claimed:
- ❌ Subjective emotions
- ❌ Consciousness
- ❌ Human-like feelings

### Claimed:
- ✅ Emotion-like functional modulation
- ✅ Affective state representation
- ✅ Experience-based behavior shaping
- ✅ Model-agnostic architecture

## Innovation Points

1. **Cognitive Appraisal Vector**: Events evaluated across multiple dimensions
2. **Interoceptive Self-State**: Continuous state vector as planning bias
3. **Affective Memory**: Severity-weighted experience storage with source trust tracking
4. **Stimulus Generalization**: Emotional spread to similar events
5. **Strategy Modulation**: Emotion as policy parameter modifier, not output text modifier
6. **Recovery Dynamics**: Evidence-based state recovery with time inertia
7. **Hesitation Behavior**: Observable intermediate actions for high-conflict scenarios
8. **Model-Agnostic Shell**: Works with any LLM/Agent

## Citation

```bibtex
@misc{ExperienceShapedAffectiveAgent2026,
  title={Experience-Shaped Affective Agent: A Model-Agnostic Framework for Emotion-like Behavioral Modulation},
  author={Zhuyuyangyy},
  year={2026},
  url={https://github.com/Zhuyuyangyy/emotion-like-functional-modulation}
}
```
