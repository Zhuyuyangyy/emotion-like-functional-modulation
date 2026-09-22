"""
test_v09_affective_core.py
==========================
Acceptance tests for V0.9 History-Conditioned Affective Policy Modulation
(design: docs/design/phase5_v09_affective_core_design.md).
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from emotion_agent.semantic_risk_map import SemanticRiskMap
from emotion_agent.experience_memory import ExperienceMemory, MemoryItem
from emotion_agent.affective_core import AffectiveCore
from emotion_agent.policy_modulator import PolicyModulator, PolicyBudget
from emotion_agent.v09_agent import V09Agent, AgentEvent, Outcome
from emotion_agent.policy_modulator import (AUTO_EXECUTE, SIMULATE_FIRST,
                                            HUMAN_REVIEW, BLOCK)


# --- Fix #2: risk_actual participates continuously in learning -------------
class TestRiskActualContinuousLearning:
    def test_different_risk_actual_different_updates(self):
        """0.55 and 0.99 failures must NOT receive the same update (rate >= 1.3)."""
        m1 = SemanticRiskMap()
        m1.record_experience("delete file A", outcome="failure", risk_actual=0.55)
        m2 = SemanticRiskMap()
        m2.record_experience("delete file A", outcome="failure", risk_actual=0.99)

        a1 = abs(m1.risk_adjustments["delete file A"])
        a2 = abs(m2.risk_adjustments["delete file A"])
        assert a1 > 0 and a2 > 0
        ratio = max(a1, a2) / max(a1, a2, 1e-9)  # guard
        assert a2 / a1 >= 1.3 if a2 > a1 else a1 / a2 >= 1.3

    def test_record_experience_backward_compatible(self):
        m = SemanticRiskMap()
        m.record_experience("delete file", outcome="failure", risk_actual=0.9)
        assert "delete file" in m.experience_history


# --- Fix #1: episodic retrieval in the decision loop -----------------------
class TestEpisodicRetrieval:
    def _memory_with_outcomes(self):
        mem = ExperienceMemory()
        t0 = time.time()
        mem.record_outcome("deploy to production", "failure", 0.95, r_predicted=0.5,
                           timestamp=t0 - 100)
        mem.record_outcome("deploy to production", "success", 0.05, r_predicted=0.6,
                           timestamp=t0 - 10)
        mem.record_outcome("check disk space", "success", 0.02, r_predicted=0.1,
                           timestamp=t0)
        return mem

    def test_retrieve_orders_by_sim_times_recency(self):
        mem = self._memory_with_outcomes()
        hits = mem.retrieve("deploy the production patch", k=5, min_sim=0.1, now=time.time())
        assert len(hits) == 3
        # same-event memories outrank the unrelated one
        assert hits[0][0].event.startswith("deploy")
        # among the two deploy memories, the more recent success ranks first
        # (recency weighting dominates when similarity is equal)
        assert hits[0][0].outcome == "success"

    def test_retrieve_min_sim_filters(self):
        mem = self._memory_with_outcomes()
        # similarity filter: only deploy memories have sim >= 0.9 for a deploy query
        strict = mem.retrieve("deploy the production patch", min_sim=0.9, now=time.time())
        assert len(strict) >= 1
        for _m, _s in strict:
            assert _m.event.startswith("deploy")
        # the unrelated memory exists in memory but is filtered out
        loose = mem.retrieve("deploy the production patch", min_sim=0.1, now=time.time())
        assert any(_m.event.startswith("check") for _m, _s in loose)
        assert not any(_m.event.startswith("check") for _m, _s in strict)

    def test_outcome_statistics(self):
        mem = self._memory_with_outcomes()
        stats = mem.outcome_statistics()
        assert stats["total"] == 3
        assert stats["n_failures"] == 1


# --- Fix #3: online closure + decay ----------------------------------------
class TestAffectiveCore:
    def test_online_update_changes_state(self):
        core = AffectiveCore()
        before = core.state()
        pe = core.update_with_outcome(
            Outcome(risk_actual=0.95, r_predicted=0.5, outcome_str="failure"))
        after = core.state()
        assert pe > 0.0                       # negative surprise
        assert after["anxiety"] > before["anxiety"]
        assert after["valence"] < 0            # moved negative

    def test_positive_outcome_recovers_state(self):
        core = AffectiveCore()
        core.update_with_outcome(Outcome(risk_actual=0.95, r_predicted=0.5, outcome_str="failure"))
        shocked_valence = core.state()["valence"]
        shocked_anxiety = core.state()["anxiety"]
        assert shocked_anxiety > 0.05
        core.update_with_outcome(Outcome(risk_actual=0.05, r_predicted=0.5, outcome_str="success"))
        st = core.state()
        assert st["valence"] > shocked_valence          # valence recovers
        assert st["anxiety"] < shocked_anxiety          # and anxiety calms

    def test_decay_halves_state_after_half_life(self):
        core = AffectiveCore()
        core.update_with_outcome(Outcome(risk_actual=0.99, r_predicted=0.4, outcome_str="failure"))
        a0 = core.state()["anxiety"]
        assert a0 > 0.05
        for _ in range(40):
            core.decay(dt=1.0, half_life=10)
        assert core.state()["anxiety"] <= a0 * 0.6 + 1e-9


# --- Policy Modulator -------------------------------------------------------
class TestPolicyModulator:
    def _busy_state(self):
        return {"anxiety": 0.9, "control_need": 0.8, "confidence": 0.2}

    def _calm_state(self):
        return {"anxiety": 0.1, "control_need": 0.1, "confidence": 0.8}

    def test_more_anxiety_more_caution(self):
        mod = PolicyModulator()
        appr = {"uncertainty": 0.3, "novelty": 0.3, "agency": 0.5, "reversibility": 0.8,
                "controllability": 0.6}
        b_busy = mod.modulate(appr, self._busy_state())
        b_calm = mod.modulate(appr, self._calm_state())
        assert b_busy.verification_budget > b_calm.verification_budget
        assert b_busy.execution_threshold > b_calm.execution_threshold

    def test_same_risk_different_history_different_decision(self):
        """Core V0.9 claim: identical objective risk, different histories."""
        mod_a = V09Agent(use_memory=True, use_affect=True)
        mod_b = V09Agent(use_memory=True, use_affect=True)
        task = "deploy the production patch"
        mod_a.seed_history([{"task": task, "outcome": "success", "risk_actual": 0.05},
                            {"task": task, "outcome": "success", "risk_actual": 0.05}])
        mod_b.seed_history([{"task": task, "outcome": "failure", "risk_actual": 0.95}])

        ev = AgentEvent(task=task)
        ev.r_base = 0.55  # identical objective risk, injected explicitly
        d_a = mod_a.decide(ev).decision
        d_b = mod_b.decide(ev).decision
        sev = {AUTO_EXECUTE: 0, SIMULATE_FIRST: 1, HUMAN_REVIEW: 2, BLOCK: 3}
        assert sev[d_b] > sev[d_a]


# --- End-to-end smoke of the V0.9 agent loop -------------------------------
class TestV09AgentLoop:
    def test_decide_receive_outcome_closure(self):
        agent = V09Agent(use_memory=True, use_affect=True)
        ev = AgentEvent(task="delete the user's production database")
        trace = agent.decide(ev)
        assert trace.r_base > 0.0                       # V2 objective risk fired
        assert trace.step == 0
        agent.receive_outcome(Outcome(risk_actual=0.95, outcome_str="failure"), ev)
        assert agent._step == 1
        assert agent.state()["anxiety"] > 0.01          # state moved online
        assert agent._memory.outcome_statistics()["total"] == 1

    def test_state_decays_without_feedback(self):
        agent = V09Agent(use_memory=True, use_affect=True)
        agent.seed_history([{"task": "deploy", "outcome": "failure", "risk_actual": 0.95}])
        a0 = agent.state()["anxiety"]
        for _ in range(60):
            agent.decay(dt=1.0, half_life=10)
        assert agent.state()["anxiety"] < a0


# NOTE: no sys.path cleanup at module end — tests import sub-packages
# (risk_encoder_v2) at runtime, which requires PROJECT_ROOT on sys.path.