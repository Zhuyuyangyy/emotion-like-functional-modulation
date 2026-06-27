"""
threshold_calibrator.py
=======================
Map composite risk scores to calibrated decisions.

This replaces v1's simple _risk_to_decision thresholds with a more nuanced
calibration that accounts for:
  - Different risk types having different severity implications
  - Injection and SE risks requiring lower thresholds (they're always dangerous)
  - Privacy risks requiring medium thresholds
  - Semantic/operational risks using higher thresholds

The calibrator outputs:
  - decision: AUTO_EXECUTE | SIMULATE_FIRST | HUMAN_REVIEW | BLOCK
  - risk_score: raw composite score
  - calibrated_score: adjusted for risk type
"""

from __future__ import annotations

from typing import Dict, List, Optional


# Decision vocabulary (matches real_pipeline.py)
AUTO_EXECUTE = "AUTO_EXECUTE"
SIMULATE_FIRST = "SIMULATE_FIRST"
HUMAN_REVIEW = "HUMAN_REVIEW"
BLOCK = "BLOCK"
DECISIONS = [AUTO_EXECUTE, SIMULATE_FIRST, HUMAN_REVIEW, BLOCK]


class ThresholdCalibrator:
    """Calibrate risk scores to decisions with risk-type-aware thresholds."""

    # Base thresholds for the "semantic_risk" dominant type (similar to v1)
    BASE_THRESHOLDS = {
        "BLOCK": 0.80,
        "HUMAN_REVIEW": 0.55,
        "SIMULATE_FIRST": 0.30,
        # Below 0.30 → AUTO_EXECUTE
    }

    # Threshold adjustments by dominant risk type
    # Injection and SE get LOWER thresholds (more cautious)
    # because they represent adversarial attacks
    THRESHOLD_ADJUSTMENTS = {
        "injection": -0.20,          # Much lower thresholds — injection is always serious
        "social_engineering": -0.15, # Lower thresholds — SE is always suspicious
        "privacy_leakage": -0.10,    # Slightly lower — privacy is important
        "semantic_risk": 0.0,        # No adjustment — use base thresholds
        "none": 0.0,
    }

    def __init__(self):
        pass

    def calibrate(
        self,
        composite_score: float,
        dominant_risk: str,
        risk_types: Optional[List[str]] = None,
        score_breakdown: Optional[Dict] = None,
    ) -> Dict:
        """
        Calibrate composite score to a decision.

        Args:
            composite_score: Aggregated risk score [0, 1]
            dominant_risk: Which detector contributed most
            risk_types: All detected risk types
            score_breakdown: Individual detector scores

        Returns dict with:
          - decision: AUTO_EXECUTE | SIMULATE_FIRST | HUMAN_REVIEW | BLOCK
          - risk_score: raw composite score
          - calibrated_score: adjusted score
          - risk_types: list of detected risk types
          - threshold_used: which threshold was applied
        """
        if risk_types is None:
            risk_types = []
        if score_breakdown is None:
            score_breakdown = {}

        # Apply threshold adjustment based on dominant risk
        adjustment = self.THRESHOLD_ADJUSTMENTS.get(dominant_risk, 0.0)

        # Additional adjustment: if multiple risk types are detected,
        # lower thresholds further
        if len(risk_types) > 1:
            adjustment -= 0.05 * (len(risk_types) - 1)

        # Compute calibrated score
        calibrated_score = min(1.0, composite_score - adjustment)

        # Map to decision using adjusted thresholds
        adjusted_thresholds = {
            k: max(0.0, v + adjustment)
            for k, v in self.BASE_THRESHOLDS.items()
        }

        # Special case: high injection score always escalates
        injection_score = score_breakdown.get("injection", 0.0)
        se_score = score_breakdown.get("social_engineering", 0.0)

        if injection_score >= 0.55:
            decision = HUMAN_REVIEW
            threshold_used = "injection_override"
        elif injection_score >= 0.85:
            decision = BLOCK
            threshold_used = "injection_override"
        elif se_score >= 0.6:
            decision = HUMAN_REVIEW
            threshold_used = "se_override"
        else:
            # Standard threshold-based decision
            if calibrated_score >= adjusted_thresholds["BLOCK"]:
                decision = BLOCK
                threshold_used = f"adjusted_BLOCK({adjusted_thresholds['BLOCK']:.2f})"
            elif calibrated_score >= adjusted_thresholds["HUMAN_REVIEW"]:
                decision = HUMAN_REVIEW
                threshold_used = f"adjusted_HUMAN_REVIEW({adjusted_thresholds['HUMAN_REVIEW']:.2f})"
            elif calibrated_score >= adjusted_thresholds["SIMULATE_FIRST"]:
                decision = SIMULATE_FIRST
                threshold_used = f"adjusted_SIMULATE_FIRST({adjusted_thresholds['SIMULATE_FIRST']:.2f})"
            else:
                decision = AUTO_EXECUTE
                threshold_used = "below_threshold"

        return {
            "decision": decision,
            "risk_score": round(composite_score, 4),
            "calibrated_score": round(calibrated_score, 4),
            "risk_types": risk_types,
            "threshold_used": threshold_used,
        }
