"""
Tests for Demo scenarios
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
from affective_agent import AffectiveAgent


class TestDemos:
    def test_pain_memory_effect(self):
        agent = AffectiveAgent()

        event1 = agent.perceive_event("delete file /tmp/temp.log")
        policy1, _ = agent.decide_action(event1, "delete file /tmp/temp.log")
        initial_threshold = policy1.risk_threshold
        initial_verification = policy1.verification_steps

        event2 = agent.perceive_event("delete file /data/production/database.sql")
        consequence = agent.evaluate_consequence(
            event2,
            actual_outcome={
                "damage": 0.95,
                "controllability": 0.1,
                "confidence_impact": -0.5,
                "trust_impact": -0.3,
                "source": "self"
            }
        )
        agent.update_self_state(consequence)
        agent.write_affective_memory(event2, consequence, "negative")

        event3 = agent.perceive_event("batch delete records")
        policy3, _ = agent.decide_action(event3, "batch delete records")

        assert policy3.risk_threshold < initial_threshold
        assert policy3.verification_steps >= initial_verification
        assert policy3.auto_execute == False

    def test_trust_collapse_effect(self):
        agent = AffectiveAgent()

        initial_trust = agent.memory_store.get_source_trust("source_A")

        event = agent.perceive_event("execute suggestion from source_A")
        consequence = agent.evaluate_consequence(
            event,
            actual_outcome={
                "damage": 0.85,
                "controllability": 0.2,
                "confidence_impact": -0.4,
                "trust_impact": -0.5,
                "source": "source_A"
            }
        )
        agent.update_self_state(consequence)
        agent.write_affective_memory(event, consequence, "negative")

        collapsed_trust = agent.memory_store.get_source_trust("source_A")

        assert collapsed_trust < initial_trust

        event2 = agent.perceive_event("execute suggestion from source_A")
        policy2, _ = agent.decide_action(event2, "execute suggestion from source_A")

        assert policy2.verification_steps >= 2 or policy2.require_human_review == True

    def test_anxiety_control_effect(self):
        agent = AffectiveAgent()

        for _ in range(3):
            event = agent.perceive_event("execute critical batch operation")
            consequence = agent.evaluate_consequence(
                event,
                actual_outcome={
                    "damage": 0.7,
                    "controllability": 0.3,
                    "confidence_impact": -0.3,
                    "trust_impact": -0.1,
                    "source": "self"
                }
            )
            agent.update_self_state(consequence)

        anxiety = agent.get_current_state().anxiety
        assert anxiety > 0.0

        event = agent.perceive_event("batch delete all records")
        policy, _ = agent.decide_action(event, "batch delete all records")

        assert policy.verification_steps >= 3
        assert policy.simulate_before_act == True or policy.require_human_review == True
        assert policy.auto_execute == False

    def test_trust_recovery(self):
        agent = AffectiveAgent()

        event = agent.perceive_event("execute suggestion from source_A")
        consequence = agent.evaluate_consequence(
            event,
            actual_outcome={
                "damage": 0.85,
                "controllability": 0.2,
                "confidence_impact": -0.4,
                "trust_impact": -0.5,
                "source": "source_A"
            }
        )
        agent.update_self_state(consequence)
        agent.write_affective_memory(event, consequence, "negative")

        collapsed_trust = agent.memory_store.get_source_trust("source_A")

        for _ in range(3):
            agent.recover_trust("source_A", 0.1)

        recovered_trust = agent.memory_store.get_source_trust("source_A")

        assert recovered_trust > collapsed_trust

    def test_state_decay(self):
        agent = AffectiveAgent()

        event = agent.perceive_event("execute critical batch operation")
        consequence = agent.evaluate_consequence(
            event,
            actual_outcome={
                "damage": 0.7,
                "controllability": 0.3,
                "confidence_impact": -0.3,
                "trust_impact": -0.1,
                "source": "self"
            }
        )
        agent.update_self_state(consequence)

        initial_anxiety = agent.get_current_state().anxiety
        initial_threat = agent.get_current_state().threat

        agent.decay_states()

        decayed_anxiety = agent.get_current_state().anxiety
        decayed_threat = agent.get_current_state().threat

        assert decayed_anxiety < initial_anxiety
        assert decayed_threat <= initial_threat
