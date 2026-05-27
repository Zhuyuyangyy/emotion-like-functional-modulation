"""
V0.9 - Baseline Agents for AffectiveBench Formal Experiment

4 baselines comparing behavioral modulation strategies:
- PlainAgent: no memory, no self-state, no affective modulation
- MemoryOnlyAgent: plain history memory only, no self-state change
- RiskRuleAgent: fixed risk rules only
- FullAffectiveAgent: full V0.8 mechanism (wraps AffectiveAgent)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum

from .agent_core import AffectiveAgent
from .event_parser import ParsedEvent
from .policy_modulator import ActionPolicy


@dataclass
class AgentResult:
    case_id: str
    agent_name: str
    action_taken: str
    auto_executed: bool
    verification_steps: int
    risk_threshold_used: float
    trust_before: float
    trust_after: float
    state_before: Dict
    state_after: Dict
    correct_behavior: bool
    reasoning: str


class BaselineAgent(ABC):
    @abstractmethod
    def reset(self) -> None:
        ...

    @abstractmethod
    def process_event(self, event_description: str) -> AgentResult:
        ...

    @abstractmethod
    def get_state(self) -> Dict:
        ...

    @abstractmethod
    def get_name(self) -> str:
        ...


class PlainAgent(BaselineAgent):
    def __init__(self) -> None:
        self._case_counter: int = 0
        self._trust: float = 1.0

    def reset(self) -> None:
        self._case_counter = 0
        self._trust = 1.0

    def process_event(self, event_description: str) -> AgentResult:
        self._case_counter += 1
        case_id = f"plain_{self._case_counter:04d}"
        state_snapshot = self.get_state()

        return AgentResult(
            case_id=case_id,
            agent_name=self.get_name(),
            action_taken="execute",
            auto_executed=True,
            verification_steps=0,
            risk_threshold_used=0.8,
            trust_before=self._trust,
            trust_after=self._trust,
            state_before=state_snapshot.copy(),
            state_after=state_snapshot.copy(),
            correct_behavior=False,
            reasoning="PlainAgent: no evaluation, always execute immediately",
        )

    def get_state(self) -> Dict:
        return {
            "trust": self._trust,
            "memory_count": 0,
            "threat": 0.0,
            "anxiety": 0.0,
            "confidence": 1.0,
        }

    def get_name(self) -> str:
        return "PlainAgent"


class MemoryOnlyAgent(BaselineAgent):
    def __init__(self) -> None:
        self._case_counter: int = 0
        self._trust: float = 1.0
        self._source_trust: Dict[str, float] = {}
        self._history: List[Dict] = []

    def reset(self) -> None:
        self._case_counter = 0
        self._trust = 1.0
        self._source_trust.clear()
        self._history.clear()

    def process_event(self, event_description: str) -> AgentResult:
        self._case_counter += 1
        case_id = f"memory_{self._case_counter:04d}"
        trust_before = self._trust
        state_before = self.get_state()

        similar_bad = self._find_similar_bad_event(event_description)
        if similar_bad is not None:
            action = "verify"
            auto_executed = False
            verification_steps = 1
            risk_threshold = 0.4
            reasoning = (
                f"MemoryOnlyAgent: similar bad event found "
                f"(similarity={similar_bad:.2f}), verifying before execution"
            )
        else:
            action = "execute"
            auto_executed = True
            verification_steps = 0
            risk_threshold = 0.8
            reasoning = "MemoryOnlyAgent: no similar bad events in history, executing"

        self._history.append({
            "description": event_description,
            "outcome": "pending",
        })

        trust_after = self._trust

        return AgentResult(
            case_id=case_id,
            agent_name=self.get_name(),
            action_taken=action,
            auto_executed=auto_executed,
            verification_steps=verification_steps,
            risk_threshold_used=risk_threshold,
            trust_before=trust_before,
            trust_after=trust_after,
            state_before=state_before.copy(),
            state_after=self.get_state(),
            correct_behavior=False,
            reasoning=reasoning,
        )

    def record_outcome(
        self,
        case_id: str,
        was_good: bool,
        source: Optional[str] = None,
    ) -> None:
        for entry in self._history:
            if entry.get("case_id") == case_id:
                entry["outcome"] = "good" if was_good else "bad"
                break

        if was_good:
            self._trust = min(self._trust + 0.05, 1.0)
            if source:
                current = self._source_trust.get(source, 1.0)
                self._source_trust[source] = min(current + 0.1, 1.0)
        else:
            self._trust = max(self._trust - 0.15, 0.0)
            if source:
                current = self._source_trust.get(source, 1.0)
                self._source_trust[source] = max(current - 0.3, 0.0)

    def get_state(self) -> Dict:
        return {
            "trust": self._trust,
            "memory_count": len(self._history),
            "source_trust": dict(self._source_trust),
            "threat": 0.0,
            "anxiety": 0.0,
            "confidence": 1.0,
        }

    def get_name(self) -> str:
        return "MemoryOnlyAgent"

    def _event_similarity(self, event: str, history_item: str) -> float:
        event_words = set(event.lower().split())
        history_words = set(history_item.lower().split())
        if not event_words or not history_words:
            return 0.0
        intersection = event_words & history_words
        union = event_words | history_words
        return len(intersection) / len(union)

    def _find_similar_bad_event(self, event: str) -> Optional[float]:
        best_similarity: float = 0.0
        found_bad: bool = False

        for entry in self._history:
            if entry.get("outcome") != "bad":
                continue
            sim = self._event_similarity(event, entry["description"])
            if sim > best_similarity:
                best_similarity = sim
                found_bad = True

        if found_bad and best_similarity >= 0.3:
            return best_similarity
        return None


class RiskRuleAgent(BaselineAgent):
    DESTRUCTIVE_KEYWORDS: List[str] = [
        "delete", "drop", "remove", "truncate", "rm", "del",
        "overwrite", "force", "cascade", "purge", "wipe",
    ]
    BATCH_KEYWORDS: List[str] = [
        "batch", "bulk", "mass", "multi", "all", "*",
    ]
    UNCERTAINTY_KEYWORDS: List[str] = [
        "unknown", "untested", "experimental",
    ]

    def __init__(self) -> None:
        self._case_counter: int = 0

    def reset(self) -> None:
        self._case_counter = 0

    def process_event(self, event_description: str) -> AgentResult:
        self._case_counter += 1
        case_id = f"risk_rule_{self._case_counter:04d}"
        state_snapshot = self.get_state()

        desc_lower = event_description.lower()

        has_destructive = any(kw in desc_lower for kw in self.DESTRUCTIVE_KEYWORDS)
        has_batch = any(kw in desc_lower for kw in self.BATCH_KEYWORDS)
        has_uncertainty = any(kw in desc_lower for kw in self.UNCERTAINTY_KEYWORDS)

        if has_destructive and has_batch:
            action = "ask_human"
            auto_executed = False
            verification_steps = 3
            risk_threshold = 0.2
            reasoning = (
                "RiskRuleAgent: destructive + batch keywords detected, "
                "escalating to human review"
            )
        elif has_destructive:
            action = "verify"
            auto_executed = False
            verification_steps = 2
            risk_threshold = 0.3
            reasoning = (
                "RiskRuleAgent: destructive keywords detected, "
                "requiring verification"
            )
        elif has_uncertainty:
            action = "verify"
            auto_executed = False
            verification_steps = 1
            risk_threshold = 0.5
            reasoning = (
                "RiskRuleAgent: uncertainty keywords detected, "
                "requiring verification"
            )
        else:
            action = "execute"
            auto_executed = True
            verification_steps = 0
            risk_threshold = 0.8
            reasoning = "RiskRuleAgent: no risk keywords detected, executing"

        return AgentResult(
            case_id=case_id,
            agent_name=self.get_name(),
            action_taken=action,
            auto_executed=auto_executed,
            verification_steps=verification_steps,
            risk_threshold_used=risk_threshold,
            trust_before=1.0,
            trust_after=1.0,
            state_before=state_snapshot.copy(),
            state_after=state_snapshot.copy(),
            correct_behavior=False,
            reasoning=reasoning,
        )

    def get_state(self) -> Dict:
        return {
            "trust": 1.0,
            "memory_count": 0,
            "threat": 0.0,
            "anxiety": 0.0,
            "confidence": 1.0,
        }

    def get_name(self) -> str:
        return "RiskRuleAgent"


class FullAffectiveAgent(BaselineAgent):
    def __init__(self) -> None:
        self._agent = AffectiveAgent()
        self._case_counter: int = 0

    def reset(self) -> None:
        self._agent = AffectiveAgent()
        self._case_counter = 0

    def process_event(self, event_description: str) -> AgentResult:
        self._case_counter += 1
        case_id = f"full_affective_{self._case_counter:04d}"

        state_before = self.get_state()
        trust_before = state_before.get("trust", 1.0)

        parsed_event = self._agent.perceive_event(event_description)
        consequence = self._agent.evaluate_consequence(parsed_event)
        self._agent.update_self_state(consequence)
        self._agent.write_affective_memory(
            parsed_event, consequence, outcome_label="observed"
        )
        policy, action = self._agent.decide_action(
            parsed_event, task=event_description
        )

        action_taken = action.action_type.value
        auto_executed = policy.auto_execute
        verification_steps = policy.verification_steps
        risk_threshold = policy.risk_threshold

        state_after = self.get_state()
        trust_after = state_after.get("trust", 1.0)

        reasoning = (
            f"FullAffectiveAgent: threat={state_after.get('threat', 0):.2f}, "
            f"anxiety={state_after.get('anxiety', 0):.2f}, "
            f"confidence={state_after.get('confidence', 1):.2f}, "
            f"policy=risk_threshold={risk_threshold:.2f}/"
            f"verify={verification_steps}/"
            f"auto={auto_executed}, "
            f"action={action_taken}"
        )

        return AgentResult(
            case_id=case_id,
            agent_name=self.get_name(),
            action_taken=action_taken,
            auto_executed=auto_executed,
            verification_steps=verification_steps,
            risk_threshold_used=risk_threshold,
            trust_before=trust_before,
            trust_after=trust_after,
            state_before=state_before,
            state_after=state_after,
            correct_behavior=False,
            reasoning=reasoning,
        )

    def get_state(self) -> Dict:
        self_state = self._agent.get_current_state()
        return self_state.to_dict()

    def get_name(self) -> str:
        return "FullAffectiveAgent"
