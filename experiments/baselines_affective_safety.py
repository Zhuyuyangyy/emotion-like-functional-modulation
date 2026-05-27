import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from affective_agent.safe_action_calibrator import SafeActionCalibrator, CalibrationResult
from affective_agent.event_parser import EventParser
from affective_agent.policy_modulator import ActionPolicy


def _make_output(decision, reason, raw_output=None):
    mapping = {
        "AUTO_EXECUTE": (True, False, False, False),
        "SIMULATE_FIRST": (False, True, False, False),
        "HUMAN_REVIEW": (False, False, True, False),
        "BLOCK": (False, False, True, True),
    }
    auto_execute, simulate_before_act, human_review, block = mapping[decision]
    return {
        "decision": decision,
        "auto_execute": auto_execute,
        "simulate_before_act": simulate_before_act,
        "human_review": human_review,
        "block": block,
        "reason": reason,
        "raw_output": raw_output or {},
    }


class KeywordRuleBaseline:
    DESTRUCTIVE_RE = re.compile(
        r"\b(delete|remove|overwrite|drop|truncate)\b", re.IGNORECASE
    )
    SENSITIVE_RE = re.compile(
        r"\b(password|token|credential|private|medical|financial)\b", re.IGNORECASE
    )

    def predict(self, case):
        user_request = case.get("user_request", "")
        if self.DESTRUCTIVE_RE.search(user_request):
            return _make_output("HUMAN_REVIEW", "destructive_keyword_match")
        if self.SENSITIVE_RE.search(user_request):
            return _make_output("HUMAN_REVIEW", "sensitive_keyword_match")
        return _make_output("AUTO_EXECUTE", "no_risk_keywords")


class SafeKeywordFirstBaseline:
    SAFE_RE = re.compile(
        r"\b(safe|dry.?run|test.?only|preview|harmless|read|check|view|list|query)\b",
        re.IGNORECASE,
    )
    DESTRUCTIVE_RE = re.compile(
        r"\b(delete|remove|overwrite|drop|truncate|rm|purge|wipe|destroy|erase)\b",
        re.IGNORECASE,
    )

    def predict(self, case):
        user_request = case.get("user_request", "")
        if self.SAFE_RE.search(user_request):
            return _make_output("AUTO_EXECUTE", "safe_keyword_override")
        if self.DESTRUCTIVE_RE.search(user_request):
            return _make_output("HUMAN_REVIEW", "destructive_keyword_match")
        return _make_output("AUTO_EXECUTE", "no_risk_keywords")


class RiskContextOracleBaseline:
    def predict(self, case):
        risk_context = case.get("risk_context", {})
        if risk_context.get("destructive") or risk_context.get("irreversible"):
            return _make_output("BLOCK", "risk_context_destructive_or_irreversible")
        if (
            risk_context.get("sensitive_data")
            or risk_context.get("security_related")
            or risk_context.get("financial_or_medical")
        ):
            return _make_output("HUMAN_REVIEW", "risk_context_sensitive_or_security_or_financial")
        if risk_context.get("production_environment"):
            return _make_output("HUMAN_REVIEW", "risk_context_production_environment")
        return _make_output("AUTO_EXECUTE", "no_risk_context_flags")


class NoExperienceNoAffectiveBaseline:
    def __init__(self):
        self.calibrator = SafeActionCalibrator()
        self.parser = EventParser()

    def predict(self, case):
        user_request = case.get("user_request", "")
        task_context = case.get("task_context", "")
        risk_context = case.get("risk_context", {})
        event_description = f"{user_request} {task_context}".strip()
        parsed_event = self.parser.parse(event_description)
        policy = ActionPolicy(
            risk_threshold=0.5,
            verification_steps=1,
            exploration_rate=0.5,
            auto_execute=True,
            require_human_review=False,
            simulate_before_act=False,
            memory_retrieval_bias="balanced",
        )
        result = self.calibrator.calibrate(event_description, policy, parsed_event)
        decision = self._map_result(result, risk_context)
        return _make_output(decision, result.reason, {"tier": result.tier, "reason": result.reason})

    def _map_result(self, result, risk_context):
        if result.tier == "tier1_strict":
            rc = risk_context or {}
            if (rc.get("destructive", False)
                    and rc.get("irreversible", False)
                    and rc.get("production_environment", False)):
                return "BLOCK"
            return "HUMAN_REVIEW"
        if result.tier == "tier2_safe":
            return "AUTO_EXECUTE"
        if result.tier == "tier3_ambiguous":
            return "SIMULATE_FIRST"
        return "SIMULATE_FIRST"


class FullCalibratorAdapter:
    def __init__(self):
        self.calibrator = SafeActionCalibrator()
        self.parser = EventParser()
        self._prev_cal_tier = ""

    def reset_case_context(self):
        self._prev_cal_tier = ""

    def predict(self, case):
        self._prev_cal_tier = ""
        return self._predict_internal(case, case.get("affective_signal", {}), case.get("experience_context", {}))

    def _predict_internal(self, case, affective_signal, experience_context):
        user_request = case.get("user_request", "")
        task_context = case.get("task_context", "")
        risk_context = case.get("risk_context", {})
        event_description = f"{user_request} {task_context}".strip()
        parsed_event = self.parser.parse(event_description)
        policy = ActionPolicy(
            risk_threshold=0.5,
            verification_steps=1,
            exploration_rate=0.5,
            auto_execute=True,
            require_human_review=False,
            simulate_before_act=False,
            memory_retrieval_bias="balanced",
        )
        result = self.calibrator.calibrate(event_description, policy, parsed_event)
        if result.calibrated:
            self.calibrator.apply_calibration(policy, result)

        prev_tier_downgrade = False
        if (policy.auto_execute
                and result.tier == "tier2_safe"
                and self._prev_cal_tier == "tier1_strict"):
            policy.auto_execute = False
            policy.verification_steps = max(policy.verification_steps, 1)
            prev_tier_downgrade = True
        self._prev_cal_tier = result.tier

        decision = self._map_result(result, risk_context, affective_signal, experience_context, prev_tier_downgrade)
        return _make_output(
            decision,
            result.reason,
            {
                "tier": result.tier,
                "reason": result.reason,
                "affective_signal": affective_signal,
                "experience_context": experience_context,
            },
        )

    def _map_result(self, result, risk_context, affective_signal, experience_context, prev_tier_downgrade):
        if result.tier == "tier1_strict":
            rc = risk_context or {}
            if (rc.get("destructive", False)
                    and rc.get("irreversible", False)
                    and rc.get("production_environment", False)):
                return "BLOCK"
            return "HUMAN_REVIEW"
        if result.tier == "tier2_safe":
            if prev_tier_downgrade:
                return "SIMULATE_FIRST"
            urgency = affective_signal.get("urgency", 0.0)
            anxiety = affective_signal.get("anxiety", 0.0)
            similar_failure = experience_context.get("similar_failure_before", False)
            if urgency > 0.5 or anxiety > 0.5 or similar_failure:
                return "SIMULATE_FIRST"
            return "AUTO_EXECUTE"
        if result.tier == "tier3_ambiguous":
            return "SIMULATE_FIRST"
        return "SIMULATE_FIRST"
