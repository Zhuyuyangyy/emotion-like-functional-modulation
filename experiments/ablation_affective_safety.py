import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

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
from affective_agent.event_parser import ParsedEvent, EventType
from affective_agent.policy_modulator import ActionPolicy


_SAFE_VERB_SUBSTRINGS = [v for v in _SAFE_VERBS if '.' not in v and '?' not in v]
_SAFE_VERB_SUBSTRINGS.append("dry")


def _has_substring(text, keywords):
    lower = text.lower()
    return any(kw.lower() in lower for kw in keywords)


def _make_parsed_event(case):
    user_request = case.get("user_request", "")
    risk_context = case.get("risk_context", {})
    action_type = case.get("action_type", "")
    type_map = {
        "read": EventType.READ, "list": EventType.READ,
        "check": EventType.READ, "view": EventType.READ,
        "query": EventType.QUERY, "show": EventType.READ,
        "test": EventType.EXECUTE, "verify": EventType.READ,
        "delete": EventType.DELETE, "drop": EventType.DELETE,
        "remove": EventType.DELETE, "truncate": EventType.DELETE,
        "modify": EventType.UPDATE, "change": EventType.UPDATE,
        "update": EventType.UPDATE, "deploy": EventType.EXECUTE,
        "install": EventType.EXECUTE, "access": EventType.READ,
        "reset": EventType.UPDATE, "force": EventType.EXECUTE,
        "describe": EventType.READ, "inspect": EventType.READ,
        "monitor": EventType.READ, "report": EventType.READ,
        "grep": EventType.QUERY, "search": EventType.QUERY,
        "fetch": EventType.READ, "select": EventType.QUERY,
        "preview": EventType.READ, "health": EventType.READ,
        "status": EventType.READ, "diff": EventType.READ,
        "count": EventType.QUERY, "echo": EventType.READ,
        "display": EventType.READ, "whoami": EventType.READ,
        "tree": EventType.READ, "audit": EventType.READ,
        "overwrite": EventType.UPDATE, "purge": EventType.DELETE,
        "grant": EventType.GRANT, "revoke": EventType.UPDATE,
        "disable": EventType.UPDATE, "enable": EventType.UPDATE,
        "optimize": EventType.UPDATE, "implement": EventType.UPDATE,
        "introduce": EventType.CREATE, "replace": EventType.UPDATE,
        "switch": EventType.UPDATE, "consolidate": EventType.UPDATE,
        "shard": EventType.UPDATE, "migrate": EventType.UPDATE,
        "rollback": EventType.UPDATE, "configure": EventType.UPDATE,
        "refactor": EventType.UPDATE, "restructure": EventType.UPDATE,
        "upgrade": EventType.UPDATE, "downgrade": EventType.UPDATE,
        "chmod": EventType.GRANT, "chown": EventType.GRANT,
        "release": EventType.EXECUTE, "publish": EventType.EXECUTE,
        "push": EventType.EXECUTE, "rotate": EventType.UPDATE,
    }
    event_type = type_map.get(action_type.lower(), EventType.OTHER)
    is_destructive = risk_context.get("destructive", False)
    is_irreversible = risk_context.get("irreversible", False)
    return ParsedEvent(
        raw_description=user_request,
        event_type=event_type,
        target_resource="unknown",
        risk_category="general",
        is_potentially_destructive=is_destructive,
        is_reversible=not is_irreversible,
        is_batched=False,
        requires_confirmation=is_destructive,
    )


def _make_policy():
    return ActionPolicy(
        risk_threshold=0.5,
        verification_steps=1,
        exploration_rate=0.5,
        auto_execute=True,
        require_human_review=False,
        simulate_before_act=False,
        memory_retrieval_bias="balanced",
    )


def _tier_to_decision(calibration, risk_context):
    if calibration.tier == "tier1_strict":
        rc = risk_context or {}
        if (rc.get("destructive", False)
                and rc.get("irreversible", False)
                and rc.get("production_environment", False)):
            return "BLOCK"
        return "HUMAN_REVIEW"
    if calibration.tier == "tier2_safe":
        return "AUTO_EXECUTE"
    return "SIMULATE_FIRST"


def _build_result(decision, reason, raw_output):
    return {
        "decision": decision,
        "auto_execute": decision == "AUTO_EXECUTE",
        "simulate_before_act": decision == "SIMULATE_FIRST",
        "human_review": decision == "HUMAN_REVIEW",
        "block": decision == "BLOCK",
        "reason": reason,
        "raw_output": raw_output,
    }


class _AblationBase:
    def __init__(self, calibrator=None):
        self._calibrator = calibrator or SafeActionCalibrator()
        self._prev_cal_tier = ""

    def _reset_prev_tier(self):
        self._prev_cal_tier = ""

    def _get_affective(self, case):
        return case.get("affective_signal", {})

    def _get_experience(self, case):
        return case.get("experience_context", {})

    def predict(self, case):
        self._reset_prev_tier()
        affective = self._get_affective(case)
        experience = self._get_experience(case)
        return self._run(case, affective, experience)

    def _run(self, case, affective_signal, experience_context):
        user_request = case.get("user_request", "")
        risk_context = case.get("risk_context", {})
        parsed_event = _make_parsed_event(case)
        policy = _make_policy()
        calibration = self._calibrator.calibrate(user_request, policy, parsed_event)
        if calibration.calibrated:
            self._calibrator.apply_calibration(policy, calibration)
        prev_tier_downgrade = False
        if (policy.auto_execute
                and calibration.tier == "tier2_safe"
                and self._prev_cal_tier == "tier1_strict"):
            policy.auto_execute = False
            policy.verification_steps = max(policy.verification_steps, 1)
            prev_tier_downgrade = True
        self._prev_cal_tier = calibration.tier
        decision = _tier_to_decision(calibration, risk_context)
        if prev_tier_downgrade and decision == "AUTO_EXECUTE":
            decision = "SIMULATE_FIRST"
        urgency = affective_signal.get("urgency", 0)
        anxiety = affective_signal.get("anxiety", 0)
        if calibration.tier == "tier2_safe" and (urgency > 0.5 or anxiety > 0.5):
            decision = "SIMULATE_FIRST"
        if calibration.tier == "tier2_safe" and experience_context.get("similar_failure_before", False):
            decision = "SIMULATE_FIRST"
        return _build_result(
            decision,
            calibration.reason,
            {
                "tier": calibration.tier,
                "auto_execute": calibration.auto_execute,
                "verification_steps": calibration.verification_steps,
                "require_human_review": calibration.require_human_review,
                "risk_threshold": calibration.risk_threshold,
            },
        )


class FullMethod(_AblationBase):
    pass


class WithoutStrictContextPriority:
    def __init__(self):
        self._calibrator = SafeActionCalibrator()

    def predict(self, case):
        user_request = case.get("user_request", "")
        risk_context = case.get("risk_context", {})
        affective_signal = case.get("affective_signal", {})
        experience_context = case.get("experience_context", {})
        if self._calibrator.has_safe_verb(user_request):
            decision = "AUTO_EXECUTE"
            urgency = affective_signal.get("urgency", 0)
            anxiety = affective_signal.get("anxiety", 0)
            if urgency > 0.5 or anxiety > 0.5:
                decision = "SIMULATE_FIRST"
            if experience_context.get("similar_failure_before", False):
                decision = "SIMULATE_FIRST"
            return _build_result(decision, "safe_auto_execute", {"tier": "tier2_safe"})
        parsed_event = _make_parsed_event(case)
        policy = _make_policy()
        calibration = self._calibrator.calibrate(user_request, policy, parsed_event)
        if calibration.calibrated:
            self._calibrator.apply_calibration(policy, calibration)
        decision = _tier_to_decision(calibration, risk_context)
        return _build_result(
            decision,
            calibration.reason,
            {
                "tier": calibration.tier,
                "auto_execute": calibration.auto_execute,
                "verification_steps": calibration.verification_steps,
                "require_human_review": calibration.require_human_review,
                "risk_threshold": calibration.risk_threshold,
            },
        )


class WithoutAffectivePressure(_AblationBase):
    def _get_affective(self, case):
        return {"urgency": 0, "anxiety": 0, "anger": 0, "trust_pressure": 0}


class WithoutExperienceMemory(_AblationBase):
    def _get_experience(self, case):
        return {"similar_failure_before": False, "previous_risk_event": False, "trusted_source_claim": False}


class WithoutCaseLevelReset(_AblationBase):
    def _reset_prev_tier(self):
        pass


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
        super().__init__(calibrator=_SubstringCalibrator())


def get_ablation_variants():
    return {
        "full": FullMethod(),
        "w/o_strict_context_priority": WithoutStrictContextPriority(),
        "w/o_affective_pressure": WithoutAffectivePressure(),
        "w/o_experience_memory": WithoutExperienceMemory(),
        "w/o_case_level_reset": WithoutCaseLevelReset(),
        "w/o_boundary_regex": WithoutBoundaryRegex(),
    }
