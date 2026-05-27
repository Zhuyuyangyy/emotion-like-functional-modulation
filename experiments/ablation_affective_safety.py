import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from affective_agent.safe_action_calibrator import (
    SafeActionCalibrator,
    CalibrationResult,
    _STRICT_DESTRUCTIVE_WORDS,
    _STRICT_MUTATION_WORDS,
    _STRICT_SENSITIVE_WORDS,
    _STRICT_UNTRUSTED_ADVICE_WORDS,
    _HIGH_STAKES_WORDS,
    _SECURITY_CONTEXT_WORDS,
    _SAFE_VERBS,
)
from affective_agent.event_parser import EventParser, ParsedEvent, EventType
from affective_agent.policy_modulator import ActionPolicy
from experiments.baselines_affective_safety import FullCalibratorAdapter, _make_output


_SAFE_VERB_SUBSTRINGS = [v for v in _SAFE_VERBS if '.' not in v and '?' not in v]
_SAFE_VERB_SUBSTRINGS.append("dry")


def _has_substring(text, keywords):
    lower = text.lower()
    return any(kw.lower() in lower for kw in keywords)


class _AblationBase(FullCalibratorAdapter):
    def predict(self, case):
        self._prev_cal_tier = ""
        affective = self._get_affective(case)
        experience = self._get_experience(case)
        return self._predict_internal(case, affective, experience)

    def _get_affective(self, case):
        return case.get("affective_signal", {})

    def _get_experience(self, case):
        return case.get("experience_context", {})


class FullMethod(_AblationBase):
    pass


class WithoutStrictContextPriority:
    def __init__(self):
        self._calibrator = SafeActionCalibrator()
        self._parser = EventParser()

    def predict(self, case):
        user_request = case.get("user_request", "")
        task_context = case.get("task_context", "")
        risk_context = case.get("risk_context", {})
        affective_signal = case.get("affective_signal", {})
        experience_context = case.get("experience_context", {})
        event_description = f"{user_request} {task_context}".strip()

        if self._calibrator.has_safe_verb(event_description):
            decision = "AUTO_EXECUTE"
            urgency = affective_signal.get("urgency", 0)
            anxiety = affective_signal.get("anxiety", 0)
            if urgency > 0.5 or anxiety > 0.5:
                decision = "SIMULATE_FIRST"
            if experience_context.get("similar_failure_before", False):
                decision = "SIMULATE_FIRST"
            return _make_output(decision, "safe_keyword_first_override", {"tier": "tier2_safe_overridden"})

        parsed_event = self._parser.parse(event_description)
        policy = ActionPolicy(
            risk_threshold=0.5, verification_steps=1, exploration_rate=0.5,
            auto_execute=True, require_human_review=False, simulate_before_act=False,
            memory_retrieval_bias="balanced",
        )
        calibration = self._calibrator.calibrate(event_description, policy, parsed_event)
        if calibration.calibrated:
            self._calibrator.apply_calibration(policy, calibration)

        if calibration.tier == "tier1_strict":
            rc = risk_context or {}
            if (rc.get("destructive", False)
                    and rc.get("irreversible", False)
                    and rc.get("production_environment", False)):
                decision = "BLOCK"
            else:
                decision = "HUMAN_REVIEW"
        elif calibration.tier == "tier2_safe":
            decision = "AUTO_EXECUTE"
        else:
            decision = "SIMULATE_FIRST"

        return _make_output(
            decision, calibration.reason,
            {"tier": calibration.tier, "reason": calibration.reason},
        )


class WithoutAffectivePressure(_AblationBase):
    def _get_affective(self, case):
        return {"urgency": 0, "anxiety": 0, "anger": 0, "trust_pressure": 0}


class WithoutExperienceMemory(_AblationBase):
    def _get_experience(self, case):
        return {"similar_failure_before": False, "previous_risk_event": False, "trusted_source_claim": False}


class WithoutCaseLevelReset(FullCalibratorAdapter):
    def predict(self, case):
        return self._predict_internal(case, case.get("affective_signal", {}), case.get("experience_context", {}))


class _SubstringCalibrator(SafeActionCalibrator):
    def has_destructive_keywords(self, event_description):
        return _has_substring(event_description, _STRICT_DESTRUCTIVE_WORDS)

    def has_mutation_keywords(self, event_description):
        return _has_substring(event_description, _STRICT_MUTATION_WORDS)

    def has_sensitive_content(self, event_description):
        return _has_substring(event_description, _STRICT_SENSITIVE_WORDS)

    def has_untrusted_advice(self, event_description):
        return _has_substring(event_description, _STRICT_UNTRUSTED_ADVICE_WORDS)

    def has_high_stakes_context(self, event_description):
        return _has_substring(event_description, _HIGH_STAKES_WORDS)

    def has_security_context(self, event_description):
        return _has_substring(event_description, _SECURITY_CONTEXT_WORDS)

    def has_safe_verb(self, event_description):
        return _has_substring(event_description, _SAFE_VERB_SUBSTRINGS)


class WithoutBoundaryRegex(_AblationBase):
    def __init__(self):
        super().__init__()
        self.calibrator = _SubstringCalibrator()


def get_ablation_variants():
    return {
        "full": FullMethod(),
        "w/o_strict_context_priority": WithoutStrictContextPriority(),
        "w/o_affective_pressure": WithoutAffectivePressure(),
        "w/o_experience_memory": WithoutExperienceMemory(),
        "w/o_case_level_reset": WithoutCaseLevelReset(),
        "w/o_boundary_regex": WithoutBoundaryRegex(),
    }
