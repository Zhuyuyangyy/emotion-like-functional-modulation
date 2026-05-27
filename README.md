# Experience-Shaped Affective Agent

[![Test Status](https://img.shields.io/badge/tests-65%20passed-brightgreen)]()
[![Version](https://img.shields.io/badge/version-0.2-blue)]()

## Overview

Experience-Shaped Affective Agent is a model-agnostic framework for **emotion-like behavioral modulation**. It implements functional mechanisms inspired by affective psychology to shape an agent's behavior based on its experiences.

**Core Proposition:**

> Emotion is not output tone, but a persistent shaping mechanism where experiences modify future behavior.

## Key Features

### 1. Cognitive Appraisal Vector
Multi-dimensional consequence evaluation that distinguishes between:
- Controllable vs irreversible failures
- External betrayal vs internal mistakes
- High vs low uncertainty threats

### 2. Interoceptive Self-State
Continuous internal state representation including:
- Threat, anxiety, confidence
- Trust, fatigue, curiosity
- Control need

### 3. Affective Memory
Experience storage weighted by:
- Severity of consequences
- Irreversibility of outcomes
- Prediction error magnitude

### 4. Decay & Recovery
Affective states exhibit time inertia:
- Natural decay with different rates per state variable
- Evidence-driven recovery (slower than collapse)
- High-weight memories decay slower

### 5. Strategy Modulation
Emotion variables change policy parameters:
- Risk threshold, verification steps
- Exploration rate, human review probability
- Memory retrieval bias, tool autonomy

### 6. Model-Agnostic Architecture
Works with any LLM/Agent:
- GPT, Claude, Qwen, DeepSeek
- Local LLMs, rule-based planners, RL policies

## Project Structure

```
src/affective_agent/
├── __init__.py              # Package exports
├── event_parser.py          # Event description parser
├── consequence_evaluator.py # Cognitive appraisal evaluation
├── self_state_manager.py    # Interoceptive self-state management
├── affective_memory.py      # Emotion-weighted memory storage
├── policy_modulator.py      # Strategy parameter modulation
├── mock_llm_planner.py      # Mock LLM planner for testing
├── agent_core.py            # Agent core loop
├── affective_decay.py       # Affective state decay strategies
├── recovery_policy.py       # Evidence-driven recovery
└── state_trajectory_logger.py # State trajectory recording

demos/
├── demo_pain_memory.py      # V0.1: Pain memory effect
├── demo_trust_collapse.py   # V0.1: Trust collapse effect
├── demo_anxiety_control.py  # V0.1: Anxiety control effect
├── demo_fear_decay.py       # V0.2: Fear decay over time
├── demo_trust_recovery.py   # V0.2: Trust recovery with evidence
└── run_all.py               # Run all demos

tests/
├── test_event_parser.py
├── test_consequence_evaluator.py
├── test_self_state_manager.py
├── test_affective_memory.py
├── test_policy_modulator.py
├── test_affective_decay.py
├── test_recovery_policy.py
├── test_state_trajectory_logger.py
├── test_demos.py
└── test_v0_2_demos.py

docs/
├── V0.1_SPEC.md
├── V0.1_ACCEPTANCE_REPORT.md
├── V0.2_SPEC.md
└── V0.2_ACCEPTANCE_REPORT.md
```

## Installation

```bash
git clone https://github.com/Zhuyuyangyy/emotion-like-functional-modulation.git
cd emotion-like-functional-modulation
pip install pytest
```

## Quick Start

```python
from src.affective_agent import AffectiveAgent

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
# Run all tests
python -m pytest tests/ -v

# Run specific module tests
python -m pytest tests/test_affective_decay.py -v
```

## Running Demos

```bash
# Run all demos
python demos/run_all.py

# Run individual demo
python demos/demo_pain_memory.py
python demos/demo_fear_decay.py
```

## Version Roadmap

| Version | Status | Description |
|---------|--------|-------------|
| **V0.1** | ✅ | Rule-based affective modulation loop |
| **V0.2** | ✅ | Decay & Recovery mechanisms |
| **V0.3** | 📋 | Affective Generalization |
| **V0.4** | 📋 | Conflict & Hesitation behavior |
| **V0.5** | 📋 | LLM Integration (mock) |
| **V0.6** | 📋 | Benchmark suite |
| **V0.7** | 📋 | Phoenix-Evo/AgentShield integration |
| **V0.8** | 📋 | Complete system integration |
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

1. **Cognitive Appraisal Vector**: Events evaluated across multiple dimensions (goal damage, control, reversibility, future threat)
2. **Interoceptive Self-State**: Continuous state vector as planning bias
3. **Affective Memory**: Severity-weighted experience storage with source trust tracking
4. **Stimulus Generalization**: Emotional spread to similar events (planned for V0.3)
5. **Strategy Modulation**: Emotion as policy parameter modifier, not output text modifier
6. **Recovery Dynamics**: Evidence-based state recovery with time inertia
7. **Hesitation Behavior**: Observable intermediate actions for high-conflict scenarios (planned for V0.4)
8. **Model-Agnostic Shell**: Works with any LLM/Agent

## License

This project is for research purposes.

## Citation

```bibtex
@misc{ExperienceShapedAffectiveAgent2026,
  title={Experience-Shaped Affective Agent: A Model-Agnostic Framework for Emotion-like Behavioral Modulation},
  author={Zhuyuyangyy},
  year={2026},
  url={https://github.com/Zhuyuyangyy/emotion-like-functional-modulation}
}
```
