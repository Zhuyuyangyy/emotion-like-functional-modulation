"""
Self-State Manager: 管理 Agent 的内部状态向量
基于躯体标记假说：内部状态影响决策偏置
V0.2 新增：affective decay、evidence-based recovery
"""

from dataclasses import dataclass, field
from typing import Dict
import math

from .affective_decay import AffectiveDecay
from .recovery_policy import RecoveryPolicy, RecoveryEvidenceType


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
        self.affective_decay = AffectiveDecay()
        self.recovery_policy = RecoveryPolicy()
        self.consecutive_safe_operations = 0

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

    def step_decay(self, memory_affective_weights: dict = None) -> SelfState:
        """
        V0.2 新增：应用情感衰减策略，支持差异化衰减
        """
        memory_affective_weights = memory_affective_weights or {}
        max_affective_weight = max(memory_affective_weights.values()) if memory_affective_weights else None

        self.state.threat = self._clamp(
            self.affective_decay.apply_decay(
                "threat", self.state.threat, max_affective_weight
            ),
            min_val=self.MIN_THRESHOLD
        )
        self.state.anxiety = self._clamp(
            self.affective_decay.apply_decay(
                "anxiety", self.state.anxiety, max_affective_weight
            ),
            min_val=self.MIN_THRESHOLD
        )
        self.state.fatigue = self._clamp(
            self.affective_decay.apply_decay(
                "fatigue", self.state.fatigue, None
            ),
            min_val=self.MIN_VALUE
        )
        self.state.confidence = self._clamp(
            self.affective_decay.apply_decay(
                "confidence", self.state.confidence, None
            ),
            min_val=self.MIN_VALUE
        )
        self.state.curiosity = self._clamp(
            self.affective_decay.apply_decay(
                "curiosity", self.state.curiosity, None
            ),
            min_val=self.MIN_VALUE
        )
        self.state.trust = self._clamp(
            self.affective_decay.apply_decay(
                "trust", self.state.trust, None
            ),
            min_val=self.MIN_VALUE
        )
        self.state.control_need = self._clamp(
            self.affective_decay.apply_decay(
                "control_need", self.state.control_need, None
            ),
            min_val=self.MIN_THRESHOLD
        )

        self.state.exploration_rate = self._calculate_exploration_rate()
        self._record_history()
        return self.state

    def apply_recovery_evidence(
        self,
        evidence_type: RecoveryEvidenceType,
        consecutive_count: int = 1,
    ) -> SelfState:
        """
        V0.2 新增：根据证据类型应用恢复策略
        """
        state_dict = self.state.to_dict()
        new_state_dict = self.recovery_policy.apply_evidence_to_multiple_states(
            state_dict=state_dict,
            evidence_type=evidence_type,
            consecutive_success_count=consecutive_count,
        )

        self.state.threat = new_state_dict["threat"]
        self.state.confidence = new_state_dict["confidence"]
        self.state.anxiety = new_state_dict["anxiety"]
        self.state.trust = new_state_dict["trust"]
        self.state.curiosity = new_state_dict["curiosity"]
        self.state.fatigue = new_state_dict["fatigue"]
        self.state.control_need = new_state_dict["control_need"]

        self.state.exploration_rate = self._calculate_exploration_rate()
        self._record_history()
        return self.state

    def record_safe_operation(self):
        """
        记录安全操作，增加连续安全计数
        """
        self.consecutive_safe_operations += 1

    def reset_safe_operation_count(self):
        """
        重置连续安全计数
        """
        self.consecutive_safe_operations = 0
