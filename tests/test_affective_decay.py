"""
Tests for Affective Decay
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
from src.affective_agent.affective_decay import AffectiveDecay, DecayType


class TestAffectiveDecay:
    def test_linear_decay(self):
        decay = AffectiveDecay()
        val = decay.linear_decay(1.0, 0.1, 0.0)
        assert val == 0.9

        val = decay.linear_decay(0.1, 0.1, 0.0)
        assert val == 0.0

        val = decay.linear_decay(0.05, 0.1, 0.01)
        assert val == 0.01

    def test_exponential_decay(self):
        decay = AffectiveDecay()
        val = decay.exponential_decay(1.0, 0.1, 0.0)
        assert abs(val - 0.9) < 0.0001

        val = decay.exponential_decay(0.1, 0.1, 0.0)
        assert abs(val - 0.09) < 0.0001

    def test_apply_decay_defaults(self):
        decay = AffectiveDecay()

        initial = 0.8
        decayed = decay.apply_decay("threat", initial, None)
        assert decayed < initial

    def test_apply_decay_high_weight_slower(self):
        decay = AffectiveDecay()

        initial = 0.8
        slow_decayed = decay.apply_decay("threat", initial, 0.9)
        normal_decayed = decay.apply_decay("threat", initial, 0.3)

        assert slow_decayed > normal_decayed

    def test_decay_memory_strength(self):
        decay = AffectiveDecay()

        high_weight = 0.9
        low_weight = 0.3

        decayed_high = decay.decay_memory_strength(high_weight, 0.1)
        decayed_low = decay.decay_memory_strength(low_weight, 0.1)

        assert decayed_high > decayed_low

    def test_get_decay_curve_points(self):
        decay = AffectiveDecay()
        curve = decay.get_decay_curve_points("threat", 1.0, 5)

        assert len(curve) == 5
        assert curve[0] == 1.0
        assert curve[-1] < curve[0]

    def test_decay_type_enum(self):
        assert DecayType.LINEAR.value == "linear"
        assert DecayType.EXPONENTIAL.value == "exponential"
