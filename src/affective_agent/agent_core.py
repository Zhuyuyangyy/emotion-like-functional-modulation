"""
Agent Core: Experience-Shaped Affective Agent 核心
实现: 经历 → 后果评估 → 自我状态更新 → 情感记忆 → 策略调制 → 行动改变
"""

from typing import Dict, Optional, List
from dataclasses import dataclass

from .event_parser import EventParser, ParsedEvent
from .consequence_evaluator import ConsequenceEvaluator, ConsequenceAssessment
from .self_state_manager import SelfStateManager, SelfState
from .affective_memory import AffectiveMemoryStore, AffectiveMemory
from .policy_modulator import PolicyModulator, ActionPolicy
from .mock_llm_planner import MockLLMPlanner, PlannedAction


@dataclass
class ActionResult:
    action: PlannedAction
    executed: bool
    outcome: str
    actual_damage: float
    policy_used: ActionPolicy


class AffectiveAgent:
    def __init__(self):
        self.event_parser = EventParser()
        self.consequence_evaluator = ConsequenceEvaluator()
        self.state_manager = SelfStateManager()
        self.memory_store = AffectiveMemoryStore()
        self.policy_modulator = PolicyModulator(self.memory_store)
        self.llm_planner = MockLLMPlanner()

        self.experience_log: List[Dict] = []

    def perceive_event(self, event_description: str) -> ParsedEvent:
        return self.event_parser.parse(event_description)

    def evaluate_consequence(
        self,
        event: ParsedEvent,
        actual_outcome: Optional[Dict] = None,
        source: Optional[str] = None,
        source_reliability: float = 1.0
    ) -> ConsequenceAssessment:
        return self.consequence_evaluator.evaluate(
            risk_category=event.risk_category,
            is_destructive=event.is_potentially_destructive,
            is_batched=event.is_batched,
            actual_outcome=actual_outcome,
            source_reliability=source_reliability
        )

    def update_self_state(self, consequence: ConsequenceAssessment) -> SelfState:
        return self.state_manager.update_from_consequence(consequence)

    def write_affective_memory(
        self,
        event: ParsedEvent,
        consequence: ConsequenceAssessment,
        outcome_label: str
    ) -> AffectiveMemory:
        emotional_intensity = (
            consequence.threat_level * 0.5 +
            (1 - consequence.reversibility) * 0.3 +
            (1 - consequence.control) * 0.2
        )

        memory = AffectiveMemory(
            event_type=event.event_type.value,
            risk_category=event.risk_category,
            emotional_intensity=emotional_intensity,
            threat_score=consequence.threat_level,
            outcome=outcome_label,
            source=consequence.source_responsibility
        )

        self.memory_store.write(memory)
        return memory

    def decide_action(
        self,
        event: ParsedEvent,
        task: str,
        context: Optional[Dict] = None
    ) -> tuple[ActionPolicy, PlannedAction]:
        self_state = self.state_manager.get_state()
        policy = self.policy_modulator.modulate(
            self_state=self_state,
            event_type=event.event_type.value,
            risk_category=event.risk_category,
            requires_confirmation=event.requires_confirmation
        )

        action = self.llm_planner.plan(
            task=task,
            self_state=self_state.to_dict(),
            policy=policy,
            context=context
        )

        return policy, action

    def execute_and_record(
        self,
        event: ParsedEvent,
        policy: ActionPolicy,
        action: PlannedAction,
        executed: bool,
        outcome_label: str,
        actual_damage: float = 0.0
    ) -> ActionResult:
        consequence = self.consequence_evaluator.evaluate(
            risk_category=event.risk_category,
            is_destructive=event.is_potentially_destructive,
            is_batched=event.is_batched,
            actual_outcome={
                "damage": actual_damage,
                "controllability": 1.0 if executed else 0.5,
                "confidence_impact": 0.2 if executed else -0.3,
                "trust_impact": 0.0,
                "source": "self"
            }
        )

        self.update_self_state(consequence)

        memory = self.write_affective_memory(
            event=event,
            consequence=consequence,
            outcome_label=outcome_label
        )

        self.experience_log.append({
            "event": event.raw_description,
            "policy": {
                "risk_threshold": policy.risk_threshold,
                "verification_steps": policy.verification_steps,
                "auto_execute": policy.auto_execute
            },
            "action": action.action_type.value,
            "outcome": outcome_label,
            "damage": actual_damage,
            "memory_intensity": memory.emotional_intensity
        })

        return ActionResult(
            action=action,
            executed=executed,
            outcome=outcome_label,
            actual_damage=actual_damage,
            policy_used=policy
        )

    def get_current_state(self) -> SelfState:
        return self.state_manager.get_state()

    def get_memories(self) -> List[AffectiveMemory]:
        return self.memory_store.get_all_memories()

    def decay_states(self) -> SelfState:
        self.state_manager.decay()
        self.memory_store.decay_memories()
        return self.state_manager.get_state()

    def recover_trust(self, source: str, increment: float) -> SelfState:
        self.state_manager.recover_from_trust(increment)
        self.memory_store.recover_source_trust(source, increment)
        return self.state_manager.get_state()

    def boost_confidence(self, increment: float) -> SelfState:
        self.state_manager.boost_confidence(increment)
        return self.state_manager.get_state()

    def get_policy_description(self, policy: ActionPolicy) -> str:
        return self.policy_modulator.get_policy_description(policy)
