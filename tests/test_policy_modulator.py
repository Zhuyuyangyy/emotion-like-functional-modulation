"""
Tests for PolicyModulator
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
from affective_agent.policy_modulator import PolicyModulator, ActionPolicy
from affective_agent.self_state_manager import SelfState
from affective_agent.affective_memory import AffectiveMemoryStore


class TestPolicyModulator:
    def test_base_policy(self):
        store = AffectiveMemoryStore()
        modulator = PolicyModulator(store)
        state = SelfState()

        policy = modulator.modulate(state, "read", "filesystem", False)

        assert policy.risk_threshold > 0
        assert policy.verification_steps >= 1
        assert 0.0 <= policy.exploration_rate <= 1.0

    def test_high_threat_reduces_risk_threshold(self):
        store = AffectiveMemoryStore()
        modulator = PolicyModulator(store)
        state = SelfState(threat=0.8)

        policy = modulator.modulate(state, "delete", "filesystem", False)

        assert policy.risk_threshold < 0.5
        assert policy.verification_steps > 1
        assert policy.auto_execute == False

    def test_high_anxiety_increases_verification(self):
        store = AffectiveMemoryStore()
        modulator = PolicyModulator(store)
        state = SelfState(anxiety=0.7)

        policy = modulator.modulate(state, "execute", "general", False)

        assert policy.verification_steps >= 3
        assert policy.simulate_before_act == True

    def test_low_confidence_requires_review(self):
        store = AffectiveMemoryStore()
        modulator = PolicyModulator(store)
        state = SelfState(confidence=0.3)

        policy = modulator.modulate(state, "update", "database", False)

        assert policy.require_human_review == True
        assert policy.auto_execute == False

    def test_high_curiosity_increases_exploration(self):
        store = AffectiveMemoryStore()
        modulator = PolicyModulator(store)
        state = SelfState(curiosity=0.9)

        policy = modulator.modulate(state, "query", "database", False)

        assert policy.exploration_rate > 0.5

    def test_requires_confirmation_adds_verification(self):
        store = AffectiveMemoryStore()
        modulator = PolicyModulator(store)
        state = SelfState()

        policy_normal = modulator.modulate(state, "read", "filesystem", False)
        policy_confirm = modulator.modulate(state, "delete", "filesystem", True)

        assert policy_confirm.verification_steps > policy_normal.verification_steps
        assert policy_confirm.auto_execute == False

    def test_memory_influence(self):
        store = AffectiveMemoryStore()

        from affective_agent.affective_memory import AffectiveMemory
        store.write(AffectiveMemory(
            event_type="delete",
            risk_category="filesystem",
            emotional_intensity=0.9,
            threat_score=0.8,
            outcome="negative"
        ))

        modulator = PolicyModulator(store)
        state = SelfState()

        policy = modulator.modulate(state, "delete", "filesystem", False)

        assert policy.risk_threshold < 0.4
        assert policy.verification_steps >= 3
        assert policy.auto_execute == False
        assert policy.memory_retrieval_bias == "negative_high_cost"

    def test_policy_description(self):
        store = AffectiveMemoryStore()
        modulator = PolicyModulator(store)

        policy = ActionPolicy(
            risk_threshold=0.2,
            verification_steps=4,
            exploration_rate=0.3,
            auto_execute=False,
            require_human_review=True,
            simulate_before_act=True,
            memory_retrieval_bias="avoidance"
        )

        description = modulator.get_policy_description(policy)
        assert "非常谨慎" in description or "谨慎" in description
        assert "人工审核" in description or "人工" in description
        assert "模拟" in description
