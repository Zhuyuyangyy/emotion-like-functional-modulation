"""
Policy Modulator: 情感状态调制行为策略
情绪不负责"说什么"，情绪负责"怎么行动"
"""

from dataclasses import dataclass
from typing import Dict, List
from .self_state_manager import SelfState
from .affective_memory import AffectiveMemoryStore


@dataclass
class ActionPolicy:
    risk_threshold: float
    verification_steps: int
    exploration_rate: float
    auto_execute: bool
    require_human_review: bool
    simulate_before_act: bool
    memory_retrieval_bias: str


class PolicyModulator:
    BASE_RISK_THRESHOLD = 0.5
    BASE_VERIFICATION_STEPS = 1
    MEMORY_BIAS_MAP = {
        "high_threat": "negative_high_cost",
        "low_confidence": "uncertain",
        "high_anxiety": "avoidance",
        "curious": "novel",
        "neutral": "balanced"
    }

    def __init__(self, memory_store: AffectiveMemoryStore):
        self.memory_store = memory_store

    def modulate(
        self,
        self_state: SelfState,
        event_type: str,
        risk_category: str,
        requires_confirmation: bool = False
    ) -> ActionPolicy:
        base_policy = ActionPolicy(
            risk_threshold=self.BASE_RISK_THRESHOLD,
            verification_steps=self.BASE_VERIFICATION_STEPS,
            exploration_rate=self_state.exploration_rate,
            auto_execute=True,
            require_human_review=False,
            simulate_before_act=False,
            memory_retrieval_bias="balanced"
        )

        retrieved_memories = self.memory_store.retrieve(event_type, risk_category)
        memory_threat = sum(m.threat_score for m in retrieved_memories) / max(len(retrieved_memories), 1)

        if self_state.threat > 0.3 or memory_threat > 0.3:
            base_policy = self._apply_fear_modulation(base_policy, self_state, memory_threat)

        if self_state.anxiety > 0.4:
            base_policy = self._apply_anxiety_modulation(base_policy, self_state)

        if self_state.confidence < 0.5:
            base_policy = self._apply_uncertainty_modulation(base_policy, self_state)

        if self_state.curiosity > 0.7:
            base_policy = self._apply_curiosity_modulation(base_policy, self_state)

        if requires_confirmation:
            base_policy.verification_steps += 1
            base_policy.auto_execute = False

        return base_policy

    def _apply_fear_modulation(
        self,
        policy: ActionPolicy,
        self_state,
        memory_threat: float
    ) -> ActionPolicy:
        combined_threat = (self_state.threat * 0.5 + memory_threat * 0.5)
        policy.risk_threshold = self.BASE_RISK_THRESHOLD - combined_threat * 0.4
        policy.exploration_rate = max(0.1, self_state.exploration_rate - combined_threat * 0.4)
        policy.verification_steps += 2
        policy.auto_execute = False
        policy.memory_retrieval_bias = "negative_high_cost"
        return policy

    def _apply_anxiety_modulation(
        self,
        policy: ActionPolicy,
        self_state
    ) -> ActionPolicy:
        policy.verification_steps += int(self_state.anxiety * 3)
        policy.risk_threshold -= self_state.anxiety * 0.2
        policy.simulate_before_act = True
        policy.require_human_review = self_state.anxiety > 0.6
        policy.auto_execute = False
        policy.memory_retrieval_bias = "avoidance"
        return policy

    def _apply_uncertainty_modulation(
        self,
        policy: ActionPolicy,
        self_state
    ) -> ActionPolicy:
        policy.verification_steps += 1
        policy.risk_threshold -= (1.0 - self_state.confidence) * 0.3
        policy.exploration_rate = max(0.2, self_state.exploration_rate * 0.7)
        policy.require_human_review = True
        policy.auto_execute = False
        policy.memory_retrieval_bias = "uncertain"
        return policy

    def _apply_curiosity_modulation(
        self,
        policy: ActionPolicy,
        self_state
    ) -> ActionPolicy:
        policy.exploration_rate = min(1.0, self_state.exploration_rate + self_state.curiosity * 0.3)
        policy.risk_threshold += self_state.curiosity * 0.1
        policy.memory_retrieval_bias = "novel"
        return policy

    def get_policy_description(self, policy: ActionPolicy) -> str:
        descriptions = []
        if policy.risk_threshold < 0.3:
            descriptions.append("非常谨慎")
        elif policy.risk_threshold < 0.5:
            descriptions.append("较为谨慎")
        else:
            descriptions.append("正常风险承受")

        descriptions.append(f"验证步骤: {policy.verification_steps}")

        if not policy.auto_execute:
            descriptions.append("需要确认")
        if policy.require_human_review:
            descriptions.append("建议人工审核")
        if policy.simulate_before_act:
            descriptions.append("建议先模拟")

        return ", ".join(descriptions)
