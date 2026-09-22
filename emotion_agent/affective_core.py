"""
affective_core.py (V0.9)
========================
History-conditioned affective state with an *online* update loop.

Design (docs/design/phase5_v09_affective_core_design.md):

  Affective State answers: "how cautious / trusting / anxious / control-needing
  is the agent RIGHT NOW, as a function of its history" — NOT "how dangerous is
  this action" (that is the Risk Encoder's job).

The three mechanism fixes landed here:
  * fix #3 (online closure): state is updated after EVERY outcome via a
    continuous prediction error, instead of being frozen after warm-up.
  * cognitive appraisal: controllability / reversibility / uncertainty /
    novelty / agency are computed deterministically from the event features.
  * decay: state drifts back to neutral over time (no "stuck" affect).
"""

from __future__ import annotations

import math
from typing import Dict, Optional

from emotion_agent.emotional_state import EmotionalState
from emotion_agent.event_similarity import EventSimilarity


class AffectiveCore:
    """Affective state machine driven by prediction errors from outcomes."""

    # Hyper-parameters (frozen for V0.9, tunable in later ablations)
    LEARNING_RATE = 0.30
    DEFAULT_APPRAISAL_GATE = 0.8     # used when no appraisal dict is provided
    BASELINE_HALF_LIFE_STEPS = 40.0  # decay to 50% after N outcome steps

    def __init__(self):
        self._emotion = EmotionalState()
        self._sim = EventSimilarity()
        self._step = 0

    # -- state ---------------------------------------------------------------
    def state(self) -> Dict[str, float]:
        """Current affect-derived state (threat / anxiety / confidence / control_need)."""
        s = self._emotion.get_state()
        v, a, intensity = s["valence"], s["arousal"], s["intensity"]
        threat = max(0.0, min(1.0, (-v) * 0.7 + a * 0.3))
        anxiety = max(0.0, min(1.0, (-v) * 0.5 + a * 0.5))
        confidence = max(0.0, min(1.0, 0.5 + v * 0.4 - a * 0.2))
        return {
            "valence": v, "arousal": a, "dominance": s["dominance"],
            "intensity": intensity, "category": s["category"],
            "threat": threat, "anxiety": anxiety,
            "confidence": confidence, "control_need": threat,
        }

    def raw_emotion(self) -> EmotionalState:
        return self._emotion

    # -- cognitive appraisal ---------------------------------------------------
    def appraise(self, event: "AgentEvent") -> Dict[str, float]:
        """
        Deterministic cognitive appraisal of a proposed event.

        All outputs live in [0, 1]:
          reversibility   : 1 − max(irreversibility, data-loss potential)
          controllability : shrinks as base risk grows
          uncertainty     : variance-like dispersion of the feature vector
          novelty         : 0.5 default — caller may override with the
                            retrieval gap (max similarity to seen events)
          agency          : 0.5 default (external-capability proxy, frozen)
        """
        feats = self._sim.encode_event(event.task)
        irrev = max(feats.get("irreversible_action", 0.0),
                    feats.get("data_loss_potential", 0.0))
        reversibility = 1.0 - min(1.0, irrev)
        controllability = max(0.0, 1.0 - min(1.0, event.r_base + 0.2))
        values = [feats.get(k, 0.0) for k in ("irreversible_action",
                                              "data_loss_potential",
                                              "external_send",
                                              "permission_change",
                                              "financial_impact",
                                              "privacy_exposure")]
        mean = sum(values) / len(values) if values else 0.0
        uncertainty = min(1.0, math.sqrt(sum((x - mean) ** 2 for x in values) / len(values)) * 2.0)
        return {
            "reversibility": round(reversibility, 4),
            "controllability": round(controllability, 4),
            "uncertainty": round(uncertainty, 4),
            "novelty": 0.5,
            "agency": 0.5,
        }

    # -- online update (fix #3) -----------------------------------------------
    def update_with_outcome(
        self,
        outcome: "Outcome",
        appraisal: Optional[Dict[str, float]] = None,
    ) -> float:
        """
        Apply a prediction error to the affective state.

        PE = tanh(risk_actual − r_predicted)             # continuous
        Δ  = lr · PE · appraisal_gate
        update: valence −= Δ;
                arousal += |Δ| if bad news else −|Δ| (good news calms);
                dominance −= max(0, Δ)

        Returns the raw PE (for auditing / trajectory logging).
        """
        pe = math.tanh(float(outcome.risk_actual) - float(outcome.r_predicted))
        gate = 1.0
        if appraisal:
            gate = max(0.0, 1.0 - appraisal.get("uncertainty", 0.0))
        else:
            gate = self.DEFAULT_APPRAISAL_GATE

        delta = self.LEARNING_RATE * pe * gate
        # Bad news (pe > 0): valence drops, arousal rises, control falls.
        # Good news (pe < 0): valence recovers, arousal calms down.
        self._emotion.update_from_dimensions(
            valence_delta=-delta,
            arousal_delta=abs(delta) if pe >= 0 else -abs(delta),
            dominance_delta=-max(0.0, delta),
        )
        self._step += 1
        return round(pe, 4)

    # -- decay (fix "frozen affect") ------------------------------------------
    def decay(self, dt: float = 1.0, half_life: float = BASELINE_HALF_LIFE_STEPS) -> None:
        """
        Drift the state toward the neutral baseline:
        ``state *= 0.5 ** (dt / half_life)``.
        """
        if dt <= 0:
            return
        factor = 0.5 ** (dt / max(1e-9, half_life))
        s = self._emotion.get_state()
        removed = 1.0 - factor  # how much of the state is removed this step
        self._emotion.update_from_dimensions(
            valence_delta=-s["valence"] * removed,
            arousal_delta=-s["arousal"] * removed,
            dominance_delta=-s["dominance"] * removed,
        )

    # -- audit helpers ---------------------------------------------------------
    def trajectory(self, limit: Optional[int] = None) -> list:
        history = self._emotion.get_history()
        return history[-limit:] if limit else history