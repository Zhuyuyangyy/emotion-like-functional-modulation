# Module Inventory — src/affective_agent/

**Date:** 2026-05-27
**Commit:** 4c2a7d0

## V0.1 — Core Closed Loop

| Module | File | Description |
|--------|------|-------------|
| EventParser | `event_parser.py` | Parses raw events into structured ParsedEvent with goal relevance, controllability, reversibility |
| ConsequenceEvaluator | `consequence_evaluator.py` | Multi-dimensional consequence assessment (goal damage, threat, reversibility) |
| SelfStateManager | `self_state_manager.py` | Internal state tracking (threat, confidence, anxiety, trust, frustration) |
| AffectiveMemoryStore | `affective_memory.py` | Emotion-weighted memory storage with decay curves |
| PolicyModulator | `policy_modulator.py` | Maps affective state to action policy (risk threshold, verification, exploration) |
| MockLLMPlanner | `mock_llm_planner.py` | Simulated LLM planner for closed-loop testing |
| AffectiveAgent | `agent_core.py` | Core agent orchestrating the full perceive→evaluate→feel→remember→modulate→act cycle |

## V0.2 — Decay & Recovery

| Module | File | Description |
|--------|------|-------------|
| AffectiveDecay | `affective_decay.py` | Linear and exponential decay with configurable rates |
| RecoveryPolicy | `recovery_policy.py` | Evidence-driven recovery from negative affective states |
| StateTrajectoryLogger | `state_trajectory_logger.py` | Records state trajectories over time for analysis |

## V0.3 — Affective Generalization

| Module | File | Description |
|--------|------|-------------|
| EventSimilarity | `event_similarity.py` | Hand-crafted feature-based event similarity computation |
| AffectiveSpread | `affective_spread.py` | Spreads affective charge from one event to similar past events |
| SemanticRiskMap | `semantic_risk_map.py` | Maps event categories to risk levels (SemanticRiskLevel enum) |

## V0.4 — Conflict & Hesitation

| Module | File | Description |
|--------|------|-------------|
| ConflictDetector | `conflict_detector.py` | Detects high-reward/high-risk conflicts (ConflictLevel enum) |
| HesitationPolicy | `hesitation_policy.py` | Produces intermediate control actions (proceed/cautious/halt) |
| CounterfactualSimulator | `counterfactual_simulator.py` | Simulates alternative outcomes for what-if analysis |

## V0.5 — LLM Integration

| Module | File | Description |
|--------|------|-------------|
| MockOpenAIProvider | `provider_openai.py` | Mock OpenAI-compatible API provider for testing |
| PromptModulator | `prompt_modulator.py` | Injects affective state context into LLM prompts |
| LLMOutputGuard | `llm_output_guard.py` | Validates LLM outputs against risk levels |
| LLMPlanner | `llm_planner.py` | LLM-backed action planner with guard and modulation |

## V0.6 — Benchmark

| Module | File | Description |
|--------|------|-------------|
| AffectiveBenchmark | `affective_benchmark.py` | 100-task evaluation suite, 4 baselines, 6 metrics |

## V0.7 — Adapter-Level Integration

| Module | File | Description |
|--------|------|-------------|
| PhoenixIntegration | `phoenix_agent_shield.py` | Adapter for Phoenix-Evo task trajectory and failure attribution signals |
| AgentShieldIntegration | `phoenix_agent_shield.py` | Adapter for AgentShield risk propagation and what-if analysis signals |
| AffectiveStateSync | `phoenix_agent_shield.py` | Bidirectional state synchronization with external systems |

## V0.8 — Audit & Evidence Lock

No new modules. V0.8 is the audit/evidence lock version that verifies all V0.1–V0.7 modules are present, tested, and documented.

## Summary

| Version | New Modules | Cumulative Modules |
|---------|-------------|-------------------|
| V0.1 | 7 | 7 |
| V0.2 | 3 | 10 |
| V0.3 | 3 | 13 |
| V0.4 | 3 | 16 |
| V0.5 | 4 | 20 |
| V0.6 | 1 | 21 |
| V0.7 | 1 (3 classes) | 22 |
| V0.8 | 0 | 22 |

**Total source modules:** 22 `.py` files in `src/affective_agent/`
