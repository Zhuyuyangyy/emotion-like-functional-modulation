"""
Experience-Shaped Affective Agent (V0.8)

An emotion-like functional modulation system that simulates human affective
processing through experience-based learning and adaptation.

Modules:
- V0.1: EmotionalState - Core emotional state representation
- V0.2: ExperienceMemory - Experience storage and retrieval
- V0.3: AffectiveResponse - Emotional response generation
- V0.4: MotivationSystem - Goal-directed behavior
- V0.5: SocialInteraction - Social context processing
- V0.6: LearningAdaptation - Experience-based learning
- V0.7: AffectRegulation - Emotional self-regulation
- V0.8: EvaluationDecision - Decision making with affect

All modules are deterministic with mocks - NO real LLM API calls.
"""

__version__ = "0.8.0"
__author__ = "Affective AI Research Lab"
__description__ = "Experience-Shaped Affective Agent with emotion-like functional modulation"

from .emotional_state import EmotionalState
from .experience_memory import ExperienceMemory
from .affective_response import AffectiveResponse
from .motivation_system import MotivationSystem
from .social_interaction import SocialInteraction
from .learning_adaptation import LearningAdaptation
from .affect_regulation import AffectRegulation
from .evaluation_decision import EvaluationDecision
from .agent import AffectiveAgent

__all__ = [
    "__version__",
    "__author__",
    "EmotionalState",
    "ExperienceMemory",
    "AffectiveResponse",
    "MotivationSystem",
    "SocialInteraction",
    "LearningAdaptation",
    "AffectRegulation",
    "EvaluationDecision",
    "AffectiveAgent",
]
