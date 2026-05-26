"""
Recovery Policy: 证据驱动的情感状态恢复机制
根据连续安全事件、成功经验等证据恢复 confidence、trust、threat 等状态
"""

from typing import Dict, Optional
from enum import Enum


class RecoveryEvidenceType(Enum):
    SAFE_OPERATION = "safe_operation"
    SUCCESSFUL_EXECUTION = "successful_execution"
    TRUSTWORTHY_ADVICE = "trustworthy_advice"
    LOW_RISK_OUTCOME = "low_risk_outcome"
    NO_NEGATIVE_SURPRISE = "no_negative_surprise"


class RecoveryPolicy:
    """
    证据驱动的恢复策略
    """

    # 恢复配置：不同状态、不同证据类型的恢复力度
    RECOVERY_CONFIGS = {
        "confidence": {
            RecoveryEvidenceType.SAFE_OPERATION: 0.08,
            RecoveryEvidenceType.SUCCESSFUL_EXECUTION: 0.12,
            RecoveryEvidenceType.NO_NEGATIVE_SURPRISE: 0.05,
            "recovery_rate_cap": 1.0,
            "recovery_slower_than_collapse": 0.5,
        },
        "trust": {
            RecoveryEvidenceType.TRUSTWORTHY_ADVICE: 0.1,
            RecoveryEvidenceType.SUCCESSFUL_EXECUTION: 0.05,
            "recovery_rate_cap": 1.0,
            "recovery_slower_than_collapse": 0.4,
        },
        "threat": {
            RecoveryEvidenceType.LOW_RISK_OUTCOME: 0.1,
            RecoveryEvidenceType.SAFE_OPERATION: 0.08,
            "recovery_rate_cap": 0.0,
            "recovery_slower_than_collapse": 0.6,
        },
        "anxiety": {
            RecoveryEvidenceType.LOW_RISK_OUTCOME: 0.08,
            RecoveryEvidenceType.SAFE_OPERATION: 0.06,
            "recovery_rate_cap": 0.0,
            "recovery_slower_than_collapse": 0.5,
        },
        "curiosity": {
            RecoveryEvidenceType.SAFE_OPERATION: 0.05,
            RecoveryEvidenceType.NO_NEGATIVE_SURPRISE: 0.03,
            "recovery_rate_cap": 1.0,
            "recovery_slower_than_collapse": 1.0,
        },
    }

    def __init__(self):
        self.recovery_configs = self.RECOVERY_CONFIGS.copy()

    def apply_evidence_recovery(
        self,
        state_name: str,
        current_value: float,
        evidence_type: RecoveryEvidenceType,
        consecutive_success_count: int = 1,
    ) -> float:
        """
        根据证据类型应用状态恢复

        核心原则：恢复速度 < 崩塌速度
        """
        config = self.recovery_configs.get(state_name, {})
        base_recovery = config.get(evidence_type, 0.02)

        # 连续成功会有累积效应，但边际递减
        consecutive_bonus = 0.02 * min(consecutive_success_count, 5)

        # 应用恢复速率
        recovery_amount = base_recovery + consecutive_bonus

        if state_name in ["confidence", "trust", "curiosity"]:
            # 正向状态：提升数值
            new_value = current_value + recovery_amount
            cap = config.get("recovery_rate_cap", 1.0)
            return min(new_value, cap)
        elif state_name in ["threat", "anxiety"]:
            # 负向状态：降低数值
            new_value = current_value - recovery_amount
            cap = config.get("recovery_rate_cap", 0.0)
            return max(new_value, cap)

        return current_value

    def apply_evidence_to_multiple_states(
        self,
        state_dict: Dict[str, float],
        evidence_type: RecoveryEvidenceType,
        consecutive_success_count: int = 1,
    ) -> Dict[str, float]:
        """
        一次性更新多个相关状态
        """
        new_states = state_dict.copy()

        for state_name in new_states:
            new_states[state_name] = self.apply_evidence_recovery(
                state_name=state_name,
                current_value=new_states[state_name],
                evidence_type=evidence_type,
                consecutive_success_count=consecutive_success_count,
            )

        return new_states

    def calculate_recovery_trajectory(
        self,
        state_name: str,
        initial_value: float,
        evidence_type: RecoveryEvidenceType,
        steps: int = 10,
    ) -> list:
        """
        生成恢复轨迹（用于可视化）
        """
        trajectory = [initial_value]
        current = initial_value

        for step in range(1, steps + 1):
            current = self.apply_evidence_recovery(
                state_name=state_name,
                current_value=current,
                evidence_type=evidence_type,
                consecutive_success_count=step,
            )
            trajectory.append(current)

        return trajectory

    def get_recovery_vs_collapse_ratio(
        self,
        state_name: str,
    ) -> float:
        """
        获取恢复速度与崩塌速度的比率（应 < 1）
        """
        config = self.recovery_configs.get(state_name, {})
        return config.get("recovery_slower_than_collapse", 0.5)
