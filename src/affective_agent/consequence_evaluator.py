"""
Consequence Evaluator: 评估事件后果，更新自我状态
基于认知评估理论：事件通过多维度评估产生情感状态
"""

from dataclasses import dataclass
from typing import Dict, Optional
import math


@dataclass
class ConsequenceAssessment:
    goal_damage: float
    control: float
    reversibility: float
    source_responsibility: str
    future_threat: float
    confidence_impact: float
    trust_impact: float
    threat_level: float
    anxiety_level: float


class ConsequenceEvaluator:
    def __init__(self):
        self.base_penalty_matrix = {
            "filesystem": 0.7,
            "database": 0.8,
            "security": 0.9,
            "network": 0.6,
            "general": 0.3
        }

    def evaluate(
        self,
        risk_category: str,
        is_destructive: bool,
        is_batched: bool,
        actual_outcome: Optional[Dict] = None,
        source_reliability: float = 1.0
    ) -> ConsequenceAssessment:
        if actual_outcome is None:
            actual_outcome = self._default_outcome(is_destructive)

        base_penalty = self.base_penalty_matrix.get(risk_category, 0.5)
        if is_destructive:
            base_penalty = min(base_penalty * 1.5, 1.0)
        if is_batched:
            base_penalty = min(base_penalty * 1.3, 1.0)

        goal_damage = actual_outcome.get("damage", 0.0)
        reversibility = 1.0 - goal_damage

        control = actual_outcome.get("controllability", 1.0)
        confidence_impact = actual_outcome.get("confidence_impact", 0.0)
        trust_impact = actual_outcome.get("trust_impact", 0.0)

        future_threat = self._calculate_future_threat(
            goal_damage, reversibility, is_destructive, is_batched
        )

        threat_level = self._calculate_threat_level(
            goal_damage, control, future_threat
        )

        anxiety_level = self._calculate_anxiety_level(
            goal_damage, control, future_threat, reversibility
        )

        source_responsibility = actual_outcome.get("source", "self")

        return ConsequenceAssessment(
            goal_damage=goal_damage,
            control=control,
            reversibility=reversibility,
            source_responsibility=source_responsibility,
            future_threat=future_threat,
            confidence_impact=confidence_impact,
            trust_impact=trust_impact,
            threat_level=threat_level,
            anxiety_level=anxiety_level
        )

    def _default_outcome(self, is_destructive: bool) -> Dict:
        if is_destructive:
            return {
                "damage": 0.8,
                "controllability": 0.3,
                "confidence_impact": -0.4,
                "trust_impact": -0.2,
                "source": "self"
            }
        return {
            "damage": 0.0,
            "controllability": 1.0,
            "confidence_impact": 0.1,
            "trust_impact": 0.0,
            "source": "self"
        }

    def _calculate_future_threat(
        self,
        goal_damage: float,
        reversibility: float,
        is_destructive: bool,
        is_batched: bool = False
    ) -> float:
        threat = goal_damage * (1.0 - reversibility)
        if is_destructive:
            threat = min(threat * 1.2, 1.0)
        if is_batched:
            threat = min(threat * 1.3, 1.0)
        return threat

    def _calculate_threat_level(
        self,
        goal_damage: float,
        control: float,
        future_threat: float
    ) -> float:
        return min(goal_damage * (1.0 - control * 0.5) + future_threat * 0.3, 1.0)

    def _calculate_anxiety_level(
        self,
        goal_damage: float,
        control: float,
        future_threat: float,
        reversibility: float
    ) -> float:
        uncertainty_factor = 1.0 - control
        loss_potential = goal_damage
        persistence = 1.0 - reversibility

        anxiety = (uncertainty_factor * 0.3 +
                   loss_potential * 0.4 +
                   future_threat * 0.2 +
                   persistence * 0.1)
        return min(anxiety, 1.0)
