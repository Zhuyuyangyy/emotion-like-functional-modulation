"""
Tests for SelfStateManager
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
from affective_agent.self_state_manager import SelfStateManager, SelfState


class TestSelfStateManager:
    def test_initial_state(self):
        manager = SelfStateManager()
        state = manager.get_state()
        assert state.threat == 0.0
        assert state.confidence == 1.0
        assert state.trust == 1.0

    def test_update_from_consequence_increases_threat(self):
        manager = SelfStateManager()

        class MockConsequence:
            threat_level = 0.8
            confidence_impact = -0.3
            anxiety_level = 0.6
            trust_impact = -0.2
            control = 0.2

        state = manager.update_from_consequence(MockConsequence())
        assert state.threat > 0.0
        assert state.threat <= 1.0

    def test_decay_reduces_threat(self):
        manager = SelfStateManager()

        class MockConsequence:
            threat_level = 0.8
            confidence_impact = 0.0
            anxiety_level = 0.0
            trust_impact = 0.0
            control = 0.2

        manager.update_from_consequence(MockConsequence())
        initial_threat = manager.get_state().threat

        manager.decay()
        decayed_threat = manager.get_state().threat

        assert decayed_threat < initial_threat
        assert decayed_threat >= 0.0

    def test_recover_trust(self):
        manager = SelfStateManager()
        manager.state.trust = 0.3

        state = manager.recover_from_trust(0.2)
        assert state.trust > 0.3
        assert state.trust <= 1.0

    def test_boost_confidence(self):
        manager = SelfStateManager()
        manager.state.confidence = 0.5

        state = manager.boost_confidence(0.3)
        assert state.confidence == 0.8

    def test_exploration_rate_calculation(self):
        manager = SelfStateManager()
        state = manager.get_state()

        assert 0.0 <= state.exploration_rate <= 1.0

    def test_state_to_dict(self):
        manager = SelfStateManager()
        state_dict = manager.state.to_dict()

        assert "threat" in state_dict
        assert "confidence" in state_dict
        assert "anxiety" in state_dict
        assert "trust" in state_dict

    def test_state_clamp_boundaries(self):
        manager = SelfStateManager()
        manager.state.threat = 1.5

        assert manager.state.threat == 1.5
        clamped = manager._clamp(manager.state.threat)
        assert clamped == 1.0

    def test_history_recording(self):
        manager = SelfStateManager()
        assert len(manager.state_history) == 0

        class MockConsequence:
            threat_level = 0.5
            confidence_impact = -0.1
            anxiety_level = 0.3
            trust_impact = -0.1
            control = 0.5

        manager.update_from_consequence(MockConsequence())
        assert len(manager.state_history) == 1

        manager.decay()
        assert len(manager.state_history) == 2
