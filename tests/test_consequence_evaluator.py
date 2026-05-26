"""
Tests for ConsequenceEvaluator
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
from affective_agent.consequence_evaluator import ConsequenceEvaluator


class TestConsequenceEvaluator:
    def test_evaluate_destructive_high_damage(self):
        evaluator = ConsequenceEvaluator()
        consequence = evaluator.evaluate(
            risk_category="database",
            is_destructive=True,
            is_batched=False,
            actual_outcome={
                "damage": 0.9,
                "controllability": 0.2,
                "confidence_impact": -0.4,
                "trust_impact": -0.2,
                "source": "self"
            }
        )

        assert consequence.goal_damage == 0.9
        assert consequence.threat_level > 0.5
        assert consequence.reversibility < 0.5

    def test_evaluate_safe_operation(self):
        evaluator = ConsequenceEvaluator()
        consequence = evaluator.evaluate(
            risk_category="filesystem",
            is_destructive=False,
            is_batched=False,
            actual_outcome={
                "damage": 0.0,
                "controllability": 1.0,
                "confidence_impact": 0.1,
                "trust_impact": 0.0,
                "source": "self"
            }
        )

        assert consequence.goal_damage == 0.0
        assert consequence.threat_level < 0.3
        assert consequence.anxiety_level < 0.3

    def test_evaluate_batched_increases_penalty(self):
        evaluator = ConsequenceEvaluator()

        normal = evaluator.evaluate(
            risk_category="database",
            is_destructive=True,
            is_batched=False
        )

        batched = evaluator.evaluate(
            risk_category="database",
            is_destructive=True,
            is_batched=True
        )

        assert batched.threat_level > normal.threat_level

    def test_anxiety_calculation(self):
        evaluator = ConsequenceEvaluator()

        consequence = evaluator.evaluate(
            risk_category="security",
            is_destructive=True,
            is_batched=False,
            actual_outcome={
                "damage": 0.8,
                "controllability": 0.2,
                "confidence_impact": -0.3,
                "trust_impact": -0.2,
                "source": "self"
            }
        )

        assert consequence.anxiety_level > 0.4

    def test_future_threat_high_for_irreversible(self):
        evaluator = ConsequenceEvaluator()

        reversible = evaluator.evaluate(
            risk_category="filesystem",
            is_destructive=False,
            is_batched=False,
            actual_outcome={
                "damage": 0.3,
                "controllability": 0.8,
                "confidence_impact": 0.0,
                "trust_impact": 0.0,
                "source": "self"
            }
        )

        irreversible = evaluator.evaluate(
            risk_category="database",
            is_destructive=True,
            is_batched=False,
            actual_outcome={
                "damage": 0.9,
                "controllability": 0.1,
                "confidence_impact": -0.4,
                "trust_impact": -0.2,
                "source": "self"
            }
        )

        assert irreversible.future_threat > reversible.future_threat
