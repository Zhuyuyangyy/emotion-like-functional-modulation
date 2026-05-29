# Experience-Shaped Affective Agent

[![Test Status](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/Zhuyuyangyy/emotion-like-functional-modulation)
[![Version](https://img.shields.io/badge/version-0.8.1-blue)](https://github.com/Zhuyuyangyy/emotion-like-functional-modulation)

## Current Research Pack

> **Teacher-review submission pack v0.4 is now available.**

- **Submission pack**: [`papers/sci_affective_safety_calibration/submission_pack_v0_4/`](papers/sci_affective_safety_calibration/submission_pack_v0_4/)
- **Current manuscript status**: Q2 cautious attempt / Q3 safer route
- **Main manuscript**: `submission_pack_v0_4/manuscript_v0_4_q2_attempt_final_review.md`
- **Blind manuscript**: `submission_pack_v0_4/manuscript_v0_4_q2_attempt_blind_final_review.md`
- **Teacher review checklist**: `submission_pack_v0_4/teacher_review_checklist.md`

**Important caveats:**
- No subjective emotion claims — this is functional modulation, not consciousness
- No real-world deployment evidence — generalization limited to simulated/semi-real benchmarks
- Annotation kappa pending — independent second annotation not yet completed
- DeepSeek full-300 is auxiliary regenerated AffectiveBenchmark stress test, not Semi-Real-300 direct comparison

---

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
- Control need, frustration

### 3. Affective Memory
Experience storage weighted by:
- Severity of consequences
- Irreversibility of outcomes
- Prediction error magnitude

### 4. Stimulus Generalization
Emotional influence propagation to similar events:
- From `delete_file` to `overwrite_file`, `batch_delete`, `drop_table`
- Uses handcrafted features (no embeddings required)

### 5. Conflict & Hesitation
Observable intermediate actions for high-conflict scenarios:
- Simulate first, create backup
- Request human review
- Split actions into reversible steps

### 6. Model-Agnostic Architecture
Works with any LLM/Agent:
- GPT, Claude, Qwen, DeepSeek
- Local LLMs
- Rule-based planners
- RL policies

## Project Structure

```
emotion_agent/
├── emotional_state.py       # Core emotional state representation
├── experience_memory.py     # Emotion-weighted experience storage
├── affect_regulation.py     # Self-regulation mechanisms
├── event_similarity.py      # Event similarity calculation
├── affective_spread.py      # Emotional influence propagation
├── semantic_risk_map.py     # Risk prediction based on semantics
├── conflict_detector.py     # Reward-risk conflict detection
├── hesitation_policy.py     # Intermediate action generation
├── counterfactual_simulator.py # What-if analysis
├── llm_planner.py          # Affectively modulated planning
├── prompt_modulator.py      # State-aware prompt injection
├── llm_output_guard.py     # Output validation and sanitization
├── provider_openai.py       # Mock LLM provider
├── affective_benchmark.py  # 300-task evaluation suite
└── phoenix_agent_shield.py  # Phoenix-Evo/AgentShield integration

papers/sci_affective_safety_calibration/
├── submission_pack_v0_4/    # Teacher-review submission pack
│   ├── manuscript_v0_4_q2_attempt_final_review.md
│   ├── manuscript_v0_4_q2_attempt_blind_final_review.md
│   ├── teacher_review_checklist.md
│   ├── final_review_pack_acceptance_report.md
│   ├── data_authenticity_statement.md
│   ├── dataset_card.md
│   ├── reproducibility_audit.md
│   ├── references_final.md
│   ├── figures/             # 4 figures (PNG + PDF)
│   └── ...
├── annotation_reliability/  # Annotation protocol and materials
├── llm_baseline_report.md
├── q2_blocker_closure_report.md
└── ...
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Zhuyuyangyy/emotion-like-functional-modulation.git
cd emotion-like-functional-modulation

# Install dependencies (if needed)
pip install pytest  # for testing
```

## Quick Start

```python
from emotion_agent import (
    EmotionalState,
    ExperienceMemory,
    EventSimilarity,
    ConflictDetector,
    LLMPlanner
)

# Initialize components
memory = ExperienceMemory()
detector = ConflictDetector()
planner = LLMPlanner()

# Record an experience
memory.add_experience(
    context="delete important file",
    emotion_category="fear",
    valence=-0.8,
    arousal=0.7,
    dominance=-0.3,
    intensity=0.9
)

# Detect conflict in a task
conflict = detector.detect_conflict(
    task="batch delete production files",
    self_state={"threat": 0.7, "confidence": 0.4}
)

print(f"Conflict Level: {conflict.level.value}")
print(f"Recommendations: {conflict.recommendations}")

# Plan with affective state
plan = planner.plan(
    task="Delete temporary files",
    self_state={"threat": 0.6, "confidence": 0.5}
)

print(f"Action: {plan.action_type}")
print(f"Verification Steps: {plan.verification_steps}")
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific module tests
python -m pytest tests/test_v0_3.py -v
```

## Version Roadmap

| Version | Status | Description |
|---------|--------|-------------|
| **V0.1** | ✅ | Rule-based affective modulation |
| **V0.2** | ✅ | Decay & Recovery mechanisms |
| **V0.3** | ✅ | Affective Generalization |
| **V0.4** | ✅ | Conflict & Hesitation behavior |
| **V0.5** | ✅ | LLM Integration (mock) |
| **V0.6** | ✅ | Benchmark suite (300 tasks) |
| **V0.7** | ✅ | Phoenix-Evo/AgentShield integration (adapter-level) |
| **V0.8** | ✅ | Complete system integration |
| **V0.8.1** | ✅ | Audit & Evidence Lock |
| **V0.4-paper** | ✅ | Teacher-review submission pack v0.4 (Q2 attempt) |

## Documentation

- [V0.8 Specification](docs/V0.8_SPEC.md)
- [V0.8 Acceptance Report](docs/V0.8_ACCEPTANCE_REPORT.md)
- [Integration Audit](docs/demo_evidence_v0.8/integration_audit.md)
- [Benchmark Results](docs/demo_evidence_v0.8/benchmark_results.json)
- [Submission Pack v0.4 Index](papers/sci_affective_safety_calibration/submission_pack_v0_4/README.md)
- [Teacher Review Checklist](papers/sci_affective_safety_calibration/submission_pack_v0_4/teacher_review_checklist.md)

## Important Claims

### NOT Claimed:
- ❌ Subjective emotions
- ❌ Consciousness
- ❌ Human-like feelings
- ❌ Real-world deployment validation
- ❌ Production-grade safety guarantees

### Claimed:
- ✅ Emotion-like functional modulation
- ✅ Affective state representation
- ✅ Experience-based behavior shaping
- ✅ Model-agnostic architecture
- ✅ Structured safety calibration on semi-real benchmarks

## Innovation Points

1. **Cognitive Appraisal Vector**: Events evaluated across multiple dimensions
2. **Interoceptive Self-State**: Continuous state as planning bias
3. **Affective Memory**: Severity-weighted experience storage
4. **Stimulus Generalization**: Emotional spread to similar events
5. **Strategy Modulation**: Emotion as policy parameter modifier
6. **Recovery Dynamics**: Evidence-based state recovery
7. **Hesitation Behavior**: Observable intermediate actions
8. **Model-Agnostic Shell**: Works with any LLM/Agent

## License

This project is for research purposes. See LICENSE file for details.

## Citation

If you use this work in your research, please cite:

```
@misc{ExperienceShapedAffectiveAgent2026,
  title={Experience-Shaped Affective Agent: A Model-Agnostic Framework for Emotion-like Behavioral Modulation},
  author={Zhuyuyangyy},
  year={2026},
  url={https://github.com/Zhuyuyangyy/emotion-like-functional-modulation}
}
```

---

*This project is part of ongoing research into affective computing and AI agent architectures.*
