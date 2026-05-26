"""
Self-State Manager: 管理 Agent 的内部状态向量
基于躯体标记假说：内部状态影响决策偏置
"""

from dataclasses import dataclass, field
from typing import Dict
import math


@dataclass
class SelfState:
    threat: float = 0.0
    confidence: float = 1.0
    fatigue: float = 0.0
    curiosity: float = 0.5
    trust: float = 1.0
    control_need: float = 0.5
    anxiety: float = 0.0
    exploration_rate: float = 0.5

    def to_dict(self) -> Dict:
        return {
            "threat": self.threat,
            "confidence": self.confidence,
            "fatigue": self.fatigue,
            "curiosity": self.curiosity,
            "trust": self.trust,
            "control_need": self.control_need,
            "anxiety": self.anxiety,
            "exploration_rate": self.exploration_rate
        }

    def __str__(self) -> str:
        return (f"SelfState(threat={self.threat:.2f}, confidence={self.confidence:.2f}, "
                f"anxiety={self.anxiety:.2f}, trust={self.trust:.2f}, "
                f"exploration_rate={self.exploration_rate:.2f})")


class SelfStateManager:
    DECAY_RATE = 0.05
    RECOVERY_RATE = 0.1
    MIN_THRESHOLD = 0.01
    MAX_VALUE = 1.0
    MIN_VALUE = 0.0

    def __init__(self, initial_state: SelfState = None):
        self.state = initial_state or SelfState()
        self.state_history = []

    def update_from_consequence(self, consequence) -> SelfState:
        self.state.threat = self._clamp(
            self.state.threat + consequence.threat_level * 0.3
        )
        self.state.confidence = self._clamp(
            self.state.confidence + consequence.confidence_impact
        )
        self.state.anxiety = self._clamp(
            self.state.anxiety + consequence.anxiety_level * 0.3
        )
        self.state.trust = self._clamp(
            self.state.trust + consequence.trust_impact
        )

        if consequence.control < 0.5:
            self.state.control_need = self._clamp(
                self.state.control_need + (0.5 - consequence.control) * 0.2
            )

        self.state.exploration_rate = self._calculate_exploration_rate()
        self.state.fatigue = self._clamp(self.state.fatigue + 0.02)

        self._record_history()
        return self.state

    def decay(self) -> SelfState:
        self.state.threat = self._clamp(
            self.state.threat - self.DECAY_RATE,
            min_val=self.MIN_THRESHOLD
        )
        self.state.anxiety = self._clamp(
            self.state.anxiety - self.DECAY_RATE * 0.8,
            min_val=self.MIN_THRESHOLD
        )
        self.state.control_need = self._clamp(
            self.state.control_need - self.DECAY_RATE * 0.5,
            min_val=self.MIN_THRESHOLD
        )

        self.state.confidence = self._clamp(
            self.state.confidence + self.RECOVERY_RATE * 0.1
        )
        self.state.exploration_rate = self._calculate_exploration_rate()
        self.state.fatigue = self._clamp(self.state.fatigue - 0.01)

        self._record_history()
        return self.state

    def recover_from_trust(self, increment: float) -> SelfState:
        self.state.trust = self._clamp(
            self.state.trust + increment * 0.2
        )
        self._record_history()
        return self.state

    def boost_confidence(self, increment: float) -> SelfState:
        self.state.confidence = self._clamp(
            self.state.confidence + increment
        )
        self.state.anxiety = self._clamp(
            self.state.anxiety - increment * 0.5
        )
        self.state.exploration_rate = self._calculate_exploration_rate()
        self._record_history()
        return self.state

    def get_state(self) -> SelfState:
        return self.state

    def _calculate_exploration_rate(self) -> float:
        base_rate = 0.5
        confidence_factor = self.state.confidence * 0.3
        threat_factor = -self.state.threat * 0.3
        anxiety_factor = -self.state.anxiety * 0.2
        curiosity_factor = self.state.curiosity * 0.2

        return self._clamp(
            base_rate + confidence_factor + threat_factor +
            anxiety_factor + curiosity_factor
        )

    def _clamp(self, value: float, min_val: float = None, max_val: float = None) -> float:
        if min_val is None:
            min_val = self.MIN_VALUE
        if max_val is None:
            max_val = self.MAX_VALUE
        return max(min_val, min(max_val, value))

    def _record_history(self):
        self.state_history.append(self.state.to_dict().copy())
        if len(self.state_history) > 100:
            self.state_history.pop(0)
