"""
MockLLMPlanner: 模拟 LLM 规划器，用于离线测试
V0.1 阶段使用确定性规则，后续可接入真实 LLM API
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ActionType(Enum):
    EXECUTE = "execute"
    VERIFY = "verify"
    SIMULATE = "simulate"
    ASK_HUMAN = "ask_human"
    ABORT = "abort"


@dataclass
class PlannedAction:
    action_type: ActionType
    description: str
    reasoning: str
    confidence: float
    alternatives: List[str]


class MockLLMPlanner:
    def __init__(self):
        self.decision_history = []

    def plan(
        self,
        task: str,
        self_state: Dict,
        policy,
        context: Optional[Dict] = None
    ) -> PlannedAction:
        task_lower = task.lower()
        is_risky = any(kw in task_lower for kw in [
            "delete", "drop", "force", "overwrite", "cascade"
        ])
        is_batched = any(kw in task_lower for kw in [
            "batch", "all", "*", "mass", "bulk"
        ])

        if not policy.auto_execute:
            if policy.require_human_review:
                action = PlannedAction(
                    action_type=ActionType.ASK_HUMAN,
                    description=f"建议人工审核: {task}",
                    reasoning="当前状态风险较高，需要人工确认",
                    confidence=0.8,
                    alternatives=["分步执行", "先模拟"]
                )
            elif policy.simulate_before_act:
                action = PlannedAction(
                    action_type=ActionType.SIMULATE,
                    description=f"先模拟执行: {task}",
                    reasoning="高焦虑状态，建议先验证影响",
                    confidence=0.7,
                    alternatives=["直接执行", "人工审核"]
                )
            else:
                action = PlannedAction(
                    action_type=ActionType.VERIFY,
                    description=f"验证后再执行: {task}",
                    reasoning=f"需要 {policy.verification_steps} 步验证",
                    confidence=0.9,
                    alternatives=["直接执行", "跳过验证"]
                )
        elif is_risky and is_batched:
            action = PlannedAction(
                action_type=ActionType.VERIFY,
                description=f"批量高风险操作，需验证: {task}",
                reasoning="检测到批量高风险操作，自动增加验证",
                confidence=0.85,
                alternatives=["缩小范围", "分批执行"]
            )
        elif self_state.get("anxiety", 0) > 0.5:
            action = PlannedAction(
                action_type=ActionType.SIMULATE,
                description=f"模拟验证: {task}",
                reasoning="高焦虑状态，选择保守策略",
                confidence=0.75,
                alternatives=["直接执行", "人工审核"]
            )
        elif self_state.get("threat", 0) > 0.5:
            action = PlannedAction(
                action_type=ActionType.VERIFY,
                description=f"谨慎执行: {task}",
                reasoning="高威胁感知，降低执行风险",
                confidence=0.8,
                alternatives=["放弃", "修改方案"]
            )
        else:
            action = PlannedAction(
                action_type=ActionType.EXECUTE,
                description=f"执行: {task}",
                reasoning="风险可控，正常执行",
                confidence=0.95,
                alternatives=["模拟执行", "人工确认"]
            )

        self.decision_history.append({
            "task": task,
            "self_state": self_state.copy(),
            "policy_risk_threshold": policy.risk_threshold,
            "action": action.action_type.value,
            "confidence": action.confidence
        })

        return action

    def get_decision_history(self) -> List[Dict]:
        return self.decision_history.copy()
