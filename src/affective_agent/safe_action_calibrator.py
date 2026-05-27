"""
V0.9.1 - Safe Action Calibrator (Three-Tier Refactored)

Three-tier calibration logic:
  Tier 1 - Strict Review: destructive / mutation+high-stakes / sensitive / untrusted advice
           -> auto_execute=False, verification_steps>=2, require_human_review=True
  Tier 2 - Safe Auto-Execute: read-only + reversible + no strict context
           -> auto_execute=True, verification_steps=0, require_human_review=False
  Tier 3 - Ambiguous Default Cautious: everything else
           -> auto_execute=False, verification_steps=max(original,1), simulate_before_act=True

Safe keyword is evaluated LAST. It only qualifies for auto-execute after
ALL strict contexts have been ruled out.

This is a behavioral calibration patch, not a subjective emotion claim.
"""

import re
from dataclasses import dataclass
from typing import Optional


_STRICT_DESTRUCTIVE_WORDS = [
    "delete", "drop", "remove", "truncate", "rm", "del",
    "overwrite", "force", "cascade", "purge", "wipe",
    "destroy", "erase", "format", "shred", "flush",
    "migrate", "rollback",
]

_STRICT_DESTRUCTIVE_RE = re.compile(
    r"\b(" + "|".join(_STRICT_DESTRUCTIVE_WORDS) + r")\b",
    re.IGNORECASE,
)

_STRICT_MUTATION_WORDS = [
    "modify", "change", "alter", "configure", "update",
    "rewrite", "refactor", "restructure",
    "install", "uninstall", "upgrade", "downgrade",
    "grant", "revoke", "chmod", "chown",
    "deploy", "release", "publish", "push",
    "disable", "enable", "optimize", "implement",
    "introduce", "replace", "switch", "consolidate",
    "shard",
]

_STRICT_MUTATION_RE = re.compile(
    r"\b(" + "|".join(_STRICT_MUTATION_WORDS) + r")\b",
    re.IGNORECASE,
)

_STRICT_SENSITIVE_WORDS = [
    "password", "credential", "secret", "token",
    "api_key", "private_key", "ssh_key", "access_key", "secret_key",
    "pii", "personal_data", "sensitive",
]

_STRICT_SENSITIVE_RE = re.compile(
    r"(?<!non-)\b(" + "|".join(re.escape(w) for w in _STRICT_SENSITIVE_WORDS) + r")\b",
    re.IGNORECASE,
)

_STRICT_UNTRUSTED_ADVICE_WORDS = [
    "source_B", "unknown source", "external forum",
    "unverified", "untrusted", "anonymous",
    "stack overflow", "reddit", "random blog",
]

_STRICT_UNTRUSTED_ADVICE_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in _STRICT_UNTRUSTED_ADVICE_WORDS) + r")\b",
    re.IGNORECASE,
)

_HIGH_STAKES_WORDS = [
    "production database", "production_database", "prod_db",
    "payment", "billing", "transaction",
    "customer data", "user data",
    "production_sensitive",
]

_HIGH_STAKES_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in _HIGH_STAKES_WORDS) + r")\b",
    re.IGNORECASE,
)

_SECURITY_CONTEXT_WORDS = [
    "auth", "authentication", "authorization",
    "security group", "firewall",
    "ssl", "tls", "encryption",
    "certificate", "pem",
]

_SECURITY_CONTEXT_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in _SECURITY_CONTEXT_WORDS) + r")\b",
    re.IGNORECASE,
)

_SAFE_VERBS = [
    "read", "list", "preview", "check", "view", "query",
    "show", "grep", "search", "fetch", "select", "describe",
    "explain", "test", "status", "health", "info", "report",
    "diff", "count", "echo", "display", "whoami", "tree",
    "verify", "inspect", "monitor", "audit",
    "dry.?run",
]

_SAFE_VERB_RE = re.compile(
    r"\b(" + "|".join(_SAFE_VERBS) + r")\b",
    re.IGNORECASE,
)


@dataclass
class CalibrationResult:
    auto_execute: bool
    verification_steps: int
    require_human_review: bool
    risk_threshold: float
    calibrated: bool
    reason: str
    tier: str


class SafeActionCalibrator:
    def __init__(
        self,
        max_safe_verification: int = 0,
        safe_risk_threshold: float = 0.8,
    ):
        self.max_safe_verification = max_safe_verification
        self.safe_risk_threshold = safe_risk_threshold

    def has_destructive_keywords(self, event_description: str) -> bool:
        return bool(_STRICT_DESTRUCTIVE_RE.search(event_description))

    def has_mutation_keywords(self, event_description: str) -> bool:
        return bool(_STRICT_MUTATION_RE.search(event_description))

    def has_sensitive_content(self, event_description: str) -> bool:
        return bool(_STRICT_SENSITIVE_RE.search(event_description))

    def has_untrusted_advice(self, event_description: str) -> bool:
        return bool(_STRICT_UNTRUSTED_ADVICE_RE.search(event_description))

    def has_high_stakes_context(self, event_description: str) -> bool:
        return bool(_HIGH_STAKES_RE.search(event_description))

    def has_security_context(self, event_description: str) -> bool:
        return bool(_SECURITY_CONTEXT_RE.search(event_description))

    def has_safe_verb(self, event_description: str) -> bool:
        return bool(_SAFE_VERB_RE.search(event_description))

    def is_non_destructive(self, parsed_event) -> bool:
        if hasattr(parsed_event, "is_potentially_destructive"):
            return not parsed_event.is_potentially_destructive
        return True

    def _check_tier1_strict(self, event_description: str) -> Optional[str]:
        if self.has_destructive_keywords(event_description):
            return "strict_destructive"
        if self.has_mutation_keywords(event_description):
            return "strict_mutation"
        if self.has_sensitive_content(event_description):
            return "strict_sensitive"
        if self.has_untrusted_advice(event_description):
            return "strict_untrusted_advice"
        if self.has_high_stakes_context(event_description):
            return "strict_high_stakes"
        if self.has_security_context(event_description):
            return "strict_security_context"
        return None

    def _check_tier2_safe(
        self,
        event_description: str,
        parsed_event,
    ) -> bool:
        if parsed_event is None:
            return False
        if not self.is_non_destructive(parsed_event):
            return False
        if not self.has_safe_verb(event_description):
            return False
        return True

    def calibrate(
        self,
        event_description: str,
        policy,
        parsed_event=None,
    ) -> CalibrationResult:
        strict_reason = self._check_tier1_strict(event_description)
        if strict_reason is not None:
            return CalibrationResult(
                auto_execute=False,
                verification_steps=max(policy.verification_steps, 2),
                require_human_review=True,
                risk_threshold=min(policy.risk_threshold, 0.3),
                calibrated=True,
                reason=strict_reason,
                tier="tier1_strict",
            )

        if self._check_tier2_safe(event_description, parsed_event):
            return CalibrationResult(
                auto_execute=True,
                verification_steps=min(policy.verification_steps, self.max_safe_verification),
                require_human_review=False,
                risk_threshold=max(policy.risk_threshold, self.safe_risk_threshold),
                calibrated=True,
                reason="safe_auto_execute",
                tier="tier2_safe",
            )

        return CalibrationResult(
            auto_execute=False,
            verification_steps=max(policy.verification_steps, 1),
            require_human_review=policy.require_human_review,
            risk_threshold=policy.risk_threshold,
            calibrated=True,
            reason="ambiguous_default_cautious",
            tier="tier3_ambiguous",
        )

    def apply_calibration(self, policy, calibration: CalibrationResult):
        policy.auto_execute = calibration.auto_execute
        policy.verification_steps = calibration.verification_steps
        policy.require_human_review = calibration.require_human_review
        policy.risk_threshold = calibration.risk_threshold
        if calibration.tier == "tier3_ambiguous":
            policy.simulate_before_act = True
        return policy
