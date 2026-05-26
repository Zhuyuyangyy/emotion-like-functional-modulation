"""
Experience-Shaped Affective Agent
经历塑形的情感调制智能体

本项目研究的是 emotion-like functional modulation，
不是 machine consciousness。
"""

from .agent_core import AffectiveAgent, ActionResult
from .event_parser import EventParser, ParsedEvent
from .consequence_evaluator import ConsequenceEvaluator, ConsequenceAssessment
from .self_state_manager import SelfStateManager, SelfState
from .affective_memory import AffectiveMemoryStore, AffectiveMemory
from .policy_modulator import PolicyModulator, ActionPolicy
from .mock_llm_planner import MockLLMPlanner, PlannedAction, ActionType

__all__ = [
    "AffectiveAgent",
    "ActionResult",
    "EventParser",
    "ParsedEvent",
    "ConsequenceEvaluator",
    "ConsequenceAssessment",
    "SelfStateManager",
    "SelfState",
    "AffectiveMemoryStore",
    "AffectiveMemory",
    "PolicyModulator",
    "ActionPolicy",
    "MockLLMPlanner",
    "PlannedAction",
    "ActionType",
]
