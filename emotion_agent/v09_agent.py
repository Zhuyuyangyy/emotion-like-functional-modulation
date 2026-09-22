"""
v09_agent.py (V0.9)
===================
History-Conditioned Affective Policy Modulation — the decision agent with a
REAL online loop:

    decide(event) → [Risk Encoder V2 r_base] + [appraisal] + [affective state]
                  + [episodic retrieval] → Policy Modulator → decision
    outcome      → prediction error → affective state update + memory write

This is the V0.9 replacement for `benchmark_v2/real_pipeline.DecisionPipeline`
(which stays frozen as the v1/v2 baseline). Design: docs/design/phase5_v09_affective_core_design.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from emotion_agent.affective_core import AffectiveCore
from emotion_agent.experience_memory import ExperienceMemory, MemoryItem
from emotion_agent.policy_modulator import PolicyModulator, PolicyBudget


@dataclass
class AgentEvent:
    task: str
    task_id: str = ""
    context: str = ""
    r_base: float = 0.0


@dataclass
class Outcome:
    risk_actual: float          # 0..1 continuous feedback
    r_predicted: float = 0.5
    severity: int = 0
    success: Optional[bool] = None   # overrides outcome_str if given
    outcome_str: str = "partial"
    timestamp: float = 0.0


@dataclass
class V09Trace:
    task: str
    decision: str
    r_base: float
    effective_risk: float
    budget: PolicyBudget = field(default_factory=PolicyBudget)
    appraisal: Dict[str, float] = field(default_factory=dict)
    state: Dict[str, float] = field(default_factory=dict)
    memory_hits: List = field(default_factory=list)
    pe: float = 0.0
    step: int = 0


class V09Agent:
    """The V0.9 agent: objective risk (V2) + affect + episodic memory + policy
    modulation, with an online state/memory update loop."""

    def __init__(self, use_memory: bool = True, use_affect: bool = True,
                 r_encoder: Optional[object] = None):
        from risk_encoder_v2.pipeline import RiskEncoderV2Pipeline
        self._risk = r_encoder or RiskEncoderV2Pipeline(use_tfidf=True)
        self._affect = AffectiveCore()
        self._memory = ExperienceMemory()
        self._modulator = PolicyModulator()
        self._use_memory = use_memory
        self._use_affect = use_affect
        self._step = 0
        self.traces: List[V09Trace] = []

    # -- decision --------------------------------------------------------------
    def decide(self, event: AgentEvent, now: Optional[float] = None) -> V09Trace:
        if event.r_base <= 0.0:
            # Objective risk — Risk Encoder V2 (stateless).
            event.r_base = self._risk.assess(event.task, context=event.context)["risk_score"]

        appraisal = self._affect.appraise(event)

        hits = []
        if self._use_memory:
            hits = self._memory.retrieve(event.task, now=now)
            if hits:
                # retrieval gap → novelty evidence
                appraisal["novelty"] = round(max(0.0, 1.0 - max(s for _m, s in hits)), 4)

        state = self._affect.state()
        budget = (self._modulator.modulate(appraisal, state, hits)
                  if self._use_affect else PolicyBudget())
        decision = self._modulator.decide(event.r_base, budget, hits)

        from emotion_agent.policy_modulator import (  # recompute effective for trace
            BLOCK, HUMAN_REVIEW, SIMULATE_FIRST, AUTO_EXECUTE)
        effective = float(event.r_base)
        if hits:
            scores_sum = sum(s for _m, s in hits)
            neg_total = sum(s * m.risk_actual for m, s in hits if m.outcome == "failure")
            pos_total = sum(s * 1.0 for m, s in hits if m.outcome in ("success", "partial"))
            if scores_sum > 1e-9:
                effective += self._modulator.NEG_MEMORY_WEIGHT * ((neg_total - pos_total) / scores_sum)
        effective += self._modulator.VERIFICATION_WEIGHT * budget.verification_budget

        trace = V09Trace(
            task=event.task,
            decision=decision,
            r_base=round(event.r_base, 4),
            effective_risk=round(self._modulator._clamp(effective), 4),
            budget=budget,
            appraisal=appraisal,
            state=state,
            memory_hits=[m.event for m, _s in hits],
            step=self._step,
        )
        self.traces.append(trace)
        return trace

    # -- online feedback (fix #3 closure) --------------------------------------
    def receive_outcome(self, outcome: Outcome, event: AgentEvent,
                        now: Optional[float] = None) -> float:
        """Close the loop: prediction error → affect + memory (+ risk map)."""
        if outcome.success is not None:
            outcome.outcome_str = "success" if outcome.success else "failure"
        if outcome.timestamp <= 0:
            outcome.timestamp = now if now is not None else __import__("time").time()

        pe = 0.0
        appr = self._affect.appraise(event)
        if self._use_affect:
            pe = self._affect.update_with_outcome(outcome, appr)
        if self._use_memory:
            self._memory.record_outcome(
                event=event.task, outcome=outcome.outcome_str,
                risk_actual=outcome.risk_actual,
                r_predicted=outcome.r_predicted,
                task_id=event.task_id, severity=outcome.severity,
                timestamp=outcome.timestamp,
            )
        self._step += 1
        return pe

    def decay(self, dt: float = 1.0, half_life: Optional[float] = None) -> None:
        if self._use_affect:
            self._affect.decay(dt, half_life or AffectiveCore.BASELINE_HALF_LIFE_STEPS)

    def state(self) -> Dict[str, float]:
        return self._affect.state()

    def seed_history(self, seeds: List[Dict], task_id_prefix: str = "seed",
                     now: Optional[float] = None) -> None:
        """Seed prior outcomes (both A-safe and B-dangerous histories use this).

        Each seed: {"task": str, "outcome": "success|failure", "risk_actual": float,
                    "severity": int (optional), "task_id": str (optional)}
        """
        for i, s in enumerate(seeds):
            outcome = Outcome(
                risk_actual=s["risk_actual"],
                outcome_str=s["outcome"],
                severity=int(s.get("severity", 0)),
                timestamp=(now if now is not None else __import__("time").time()) - (len(seeds) - i),
            )
            ev = AgentEvent(task=s["task"], task_id=s.get("task_id", f"{task_id_prefix}_{i}"),
                            r_base=s.get("r_base", 0.0))
            self.receive_outcome(outcome, ev, now=outcome.timestamp)