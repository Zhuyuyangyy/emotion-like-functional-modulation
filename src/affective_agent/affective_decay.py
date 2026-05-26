"""
Affective Decay: 情感状态的时间衰减与记忆强度衰减
实现三类衰减机制：linear_decay、exponential_decay、evidence_based_recovery
"""

from typing import Dict, Optional
from enum import Enum


class DecayType(Enum):
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    EVIDENCE_BASED = "evidence_based"


class AffectiveDecay:
    """
    情感状态的衰减策略
    """

    # 不同状态变量的预设衰减参数
    DECAY_CONFIGS = {
        "threat": {
            "decay_type": DecayType.LINEAR,
            "base_rate": 0.05,
            "min_value": 0.01,
            "slow_decay_factor": 0.3,
        },
        "anxiety": {
            "decay_type": DecayType.EXPONENTIAL,
            "base_rate": 0.1,
            "min_value": 0.0,
            "slow_decay_factor": 0.5,
        },
        "fatigue": {
            "decay_type": DecayType.LINEAR,
            "base_rate": 0.15,
            "min_value": 0.0,
            "slow_decay_factor": 1.0,
        },
        "confidence": {
            "decay_type": DecayType.LINEAR,
            "base_rate": 0.02,
            "min_value": 0.0,
            "slow_decay_factor": 0.5,
        },
        "trust": {
            "decay_type": DecayType.LINEAR,
            "base_rate": 0.01,
            "min_value": 0.0,
            "slow_decay_factor": 0.2,
        },
        "curiosity": {
            "decay_type": DecayType.LINEAR,
            "base_rate": 0.03,
            "min_value": 0.0,
            "slow_decay_factor": 1.0,
        },
    }

    def __init__(self):
        self.decay_configs = self.DECAY_CONFIGS.copy()

    def linear_decay(
        self,
        current_value: float,
        decay_rate: float,
        min_value: float = 0.0,
    ) -> float:
        """
        线性衰减：每次固定减少
        """
        decayed = current_value - decay_rate
        return max(decayed, min_value)

    def exponential_decay(
        self,
        current_value: float,
        decay_factor: float,
        min_value: float = 0.0,
    ) -> float:
        """
        指数衰减：值越高衰减越快
        """
        decayed = current_value * (1 - decay_factor)
        return max(decayed, min_value)

    def apply_decay(
        self,
        state_name: str,
        current_value: float,
        memory_affective_weight: Optional[float] = None,
    ) -> float:
        """
        根据状态类型和情感权重，应用适当的衰减策略
        """
        config = self.decay_configs.get(state_name, self.decay_configs["threat"])
        decay_type = config["decay_type"]
        base_rate = config["base_rate"]
        min_value = config["min_value"]

        # 高情感权重记忆下衰减更慢
        if memory_affective_weight and memory_affective_weight > 0.7:
            slow_factor = config["slow_decay_factor"]
            base_rate *= slow_factor

        if decay_type == DecayType.LINEAR:
            return self.linear_decay(current_value, base_rate, min_value)
        elif decay_type == DecayType.EXPONENTIAL:
            return self.exponential_decay(current_value, base_rate, min_value)
        else:
            return current_value

    def decay_memory_strength(
        self,
        affective_weight: float,
        decay_rate: float = 0.02,
    ) -> float:
        """
        记忆强度衰减，但高情感权重记忆衰减更慢
        """
        # 情感权重越高，衰减越慢
        if affective_weight > 0.8:
            effective_rate = decay_rate * 0.2
        elif affective_weight > 0.5:
            effective_rate = decay_rate * 0.5
        else:
            effective_rate = decay_rate

        decayed = affective_weight - effective_rate
        return max(decayed, 0.01)

    def get_decay_curve_points(
        self,
        state_name: str,
        initial_value: float,
        steps: int = 10,
    ) -> list:
        """
        获取衰减曲线的预测点（用于可视化）
        """
        points = [initial_value]
        current = initial_value

        config = self.decay_configs.get(state_name, self.decay_configs["threat"])
        decay_type = config["decay_type"]
        base_rate = config["base_rate"]

        for _ in range(steps - 1):
            if decay_type == DecayType.LINEAR:
                current = self.linear_decay(current, base_rate, 0.0)
            elif decay_type == DecayType.EXPONENTIAL:
                current = self.exponential_decay(current, base_rate, 0.0)
            points.append(current)

        return points
