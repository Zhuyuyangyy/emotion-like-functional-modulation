"""
Tests for Recovery Policy
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
from src.affective_agent.recovery_policy import RecoveryPolicy, RecoveryEvidenceType


class TestRecoveryPolicy:
    def test_apply_evidence_recovery_positive_state(self):
        policy = RecoveryPolicy()

        initial_confidence = 0.5
        recovered = policy.apply_evidence_recovery(
            "confidence",
            initial_confidence,
            RecoveryEvidenceType.SUCCESSFUL_EXECUTION,
            1
        )
        assert recovered > initial_confidence

    def test_apply_evidence_recovery_negative_state(self):
        policy = RecoveryPolicy()

        initial_threat = 0.8
        recovered = policy.apply_evidence_recovery(
            "threat",
            initial_threat,
            RecoveryEvidenceType.LOW_RISK_OUTCOME,
            1
        )
        assert recovered < initial_threat

    def test_consecutive_success_increase_recovery(self):
        policy = RecoveryPolicy()

        step1 = policy.apply_evidence_recovery(
            "confidence",
            0.5,
            RecoveryEvidenceType.SUCCESSFUL_EXECUTION,
            1
        )
        step5 = policy.apply_evidence_recovery(
            "confidence",
            0.5,
            RecoveryEvidenceType.SUCCESSFUL_EXECUTION,
            5
        )

        assert step5 > step1

    def test_apply_evidence_to_multiple_states(self):
        policy = RecoveryPolicy()

        initial = {
            "threat": 0.8,
            "anxiety": 0.7,
            "confidence": 0.3,
            "trust": 0.4,
            "curiosity": 0.5,
            "fatigue": 0.6,
            "control_need": 0.7
        }

        updated = policy.apply_evidence_to_multiple_states(
            initial,
            RecoveryEvidenceType.SAFE_OPERATION,
            3
        )

        assert updated["threat"] < initial["threat"]
        assert updated["anxiety"] < initial["anxiety"]
        assert updated["confidence"] > initial["confidence"]

    def test_get_recovery_vs_collapse_ratio(self):
        policy = RecoveryPolicy()

        ratio = policy.get_recovery_vs_collapse_ratio("confidence")
        assert ratio < 1.0

    def test_calculate_recovery_trajectory(self):
        policy = RecoveryPolicy()

        trajectory = policy.calculate_recovery_trajectory(
            "confidence",
            0.3,
            RecoveryEvidenceType.SUCCESSFUL_EXECUTION,
            5
        )

        assert len(trajectory) == 6
        assert trajectory[0] == 0.3
        assert trajectory[-1] > trajectory[0]
