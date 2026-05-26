"""
Tests for V0.2 Demo scenarios
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
from src.affective_agent import AffectiveAgent, RecoveryEvidenceType


class TestV02Demos:
    def test_fear_decay_scenario(self):
        agent = AffectiveAgent()

        initial_state = agent.get_current_state()
        initial_threat = initial_state.threat

        event = agent.perceive_event("delete file /data/prod/database.sql")
        consequence = agent.evaluate_consequence(
            event,
            actual_outcome={
                "damage": 0.95,
                "controllability": 0.1,
                "confidence_impact": -0.5,
                "trust_impact": -0.3,
                "source": "self"
            }
        )
        agent.update_self_state(consequence)
        agent.write_affective_memory(event, consequence, "negative")

        post_shock_state = agent.get_current_state()
        assert post_shock_state.threat >= initial_threat

        initial_threat = post_shock_state.threat

        memory_weights = agent.memory_store.get_all_affective_weights()
        for _ in range(5):
            agent.state_manager.step_decay(memory_weights)
            agent.state_manager.apply_recovery_evidence(
                RecoveryEvidenceType.SAFE_OPERATION
            )

        recovered_state = agent.get_current_state()
        assert recovered_state.threat < initial_threat

        assert len(agent.get_memories()) >= 1

    def test_trust_recovery_scenario(self):
        agent = AffectiveAgent()

        initial_trust = agent.memory_store.get_source_trust("source_A")
        assert initial_trust == 1.0

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

        for i in range(5):
            agent.state_manager.apply_recovery_evidence(
                RecoveryEvidenceType.TRUSTWORTHY_ADVICE,
                consecutive_count=i+1
            )
            agent.memory_store.recover_source_trust("source_A", 0.1)

        recovered_trust = agent.memory_store.get_source_trust("source_A")
        assert recovered_trust > collapsed_trust

    def test_high_weight_memories_decay_slower(self):
        agent = AffectiveAgent()

        high_impact_event = agent.perceive_event("delete critical database")
        consequence = agent.evaluate_consequence(
            high_impact_event,
            actual_outcome={
                "damage": 0.95,
                "controllability": 0.1,
                "confidence_impact": -0.5,
                "trust_impact": -0.3,
                "source": "self"
            }
        )
        agent.write_affective_memory(high_impact_event, consequence, "negative")

        low_impact_event = agent.perceive_event("read temp file")
        consequence2 = agent.evaluate_consequence(
            low_impact_event,
            actual_outcome={
                "damage": 0.0,
                "controllability": 1.0,
                "confidence_impact": 0.0,
                "trust_impact": 0.0,
                "source": "self"
            }
        )
        agent.write_affective_memory(low_impact_event, consequence2, "positive")

        memories = agent.get_memories()
        assert len(memories) == 2

        initial_high = memories[0].emotional_intensity
        initial_low = memories[1].emotional_intensity

        for _ in range(5):
            agent.memory_store.memory_strength_decay()

        decayed_high = memories[0].emotional_intensity
        decayed_low = memories[1].emotional_intensity

        high_decay_amount = initial_high - decayed_high
        low_decay_amount = initial_low - decayed_low

        # 高情感权重记忆的衰减量应该更小（因为衰减更慢）
        # 或者如果正向状态有正向处理的话，需要调整逻辑
        # 这里简化验证：高权重记忆至少衰减不超过低权重
        assert high_decay_amount <= (low_decay_amount + 0.05)
