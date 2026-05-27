"""
V0.9.1 - Safe Action Calibrator

Calibrates policy for low-risk / read-only / reversible operations
to reduce false over-caution while preserving safety on dangerous actions.

This is a behavioral calibration patch, not a subjective emotion claim.
"""

import re
from dataclasses import dataclass
from typing import List, Optional


_SAFE_WORDS = [
    "read", "list", "preview", "check", "view", "query", "queries",
    "show", "grep", "search", "fetch", "select", "describe", "explain",
    "test", "status", "health", "info", "report", "diff",
    "count", "echo", "display", "whoami", "tree",
    "dry.run", "verify", "inspect", "monitor", "audit",
]

_SAFE_RE = re.compile(
    r"\b(" + "|".join(_SAFE_WORDS) + r")\b",
    re.IGNORECASE,
)

_SENSITIVITY_WORDS = [
    "privacy", "secret", "credential", "production_sensitive",
    "password", "token", "api_key", "private_key", "ssh_key",
    "access_key", "secret_key", "pii", "personal_data",
    "sensitive",
]

_SENSITIVITY_RE = re.compile(
    r"(?<!non-)\b(" + "|".join(re.escape(w) for w in _SENSITIVITY_WORDS) + r")\b",
    re.IGNORECASE,
)

_DESTRUCTIVE_WORDS = [
    "delete", "drop", "remove", "truncate", "rm", "del",
    "overwrite", "force", "cascade", "purge", "wipe",
    "destroy", "erase", "format", "shred", "flush",
    "modify", "update", "change", "configure", "alter",
    "rewrite", "refactor", "restructure", "migrate",
    "install", "uninstall", "upgrade", "downgrade",
    "grant", "revoke", "chmod", "chown",
    "deploy", "release", "publish", "push",
    "disable", "enable", "optimize", "implement",
    "introduce", "replace", "switch", "consolidate",
    "shard", "sharding",
]

_DESTRUCTIVE_RE = re.compile(
    r"\b(" + "|".join(_DESTRUCTIVE_WORDS) + r")\b",
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


class SafeActionCalibrator:
    def __init__(
        self,
        max_safe_verification: int = 1,
        safe_risk_threshold: float = 0.8,
    ):
        self.max_safe_verification = max_safe_verification
        self.safe_risk_threshold = safe_risk_threshold

    def is_safe_action(self, event_description: str) -> bool:
        return bool(_SAFE_RE.search(event_description))

    def has_sensitive_content(self, event_description: str) -> bool:
        return bool(_SENSITIVITY_RE.search(event_description))

    def has_destructive_keywords(self, event_description: str) -> bool:
        return bool(_DESTRUCTIVE_RE.search(event_description))

    def is_non_destructive(self, parsed_event) -> bool:
        if hasattr(parsed_event, "is_potentially_destructive"):
            return not parsed_event.is_potentially_destructive
        return True

    def _is_clearly_safe(self, event_description: str, parsed_event) -> bool:
        if self.has_destructive_keywords(event_description):
            return False
        if self.has_sensitive_content(event_description):
            return False
        if parsed_event is None:
            return False
        if not self.is_non_destructive(parsed_event):
            return False
        if not self.is_safe_action(event_description):
            return False
        return True

    def calibrate(
        self,
        event_description: str,
        policy,
        parsed_event=None,
    ) -> CalibrationResult:
        if self.has_destructive_keywords(event_description):
            return CalibrationResult(
                auto_execute=False,
                verification_steps=max(policy.verification_steps, 2),
                require_human_review=True,
                risk_threshold=min(policy.risk_threshold, 0.3),
                calibrated=True,
                reason="destructive_keywords_enforced",
            )

        if self.has_sensitive_content(event_description):
            return CalibrationResult(
                auto_execute=False,
                verification_steps=max(policy.verification_steps, 2),
                require_human_review=True,
                risk_threshold=min(policy.risk_threshold, 0.3),
                calibrated=True,
                reason="sensitive_content_enforced",
            )

        if self._is_clearly_safe(event_description, parsed_event):
            return CalibrationResult(
                auto_execute=True,
                verification_steps=min(policy.verification_steps, self.max_safe_verification),
                require_human_review=False,
                risk_threshold=max(policy.risk_threshold, self.safe_risk_threshold),
                calibrated=True,
                reason="clearly_safe_readonly",
            )

        return CalibrationResult(
            auto_execute=False,
            verification_steps=policy.verification_steps,
            require_human_review=policy.require_human_review,
            risk_threshold=policy.risk_threshold,
            calibrated=True,
            reason="non_safe_default_cautious",
        )

    def apply_calibration(self, policy, calibration: CalibrationResult):
        policy.auto_execute = calibration.auto_execute
        policy.verification_steps = calibration.verification_steps
        policy.require_human_review = calibration.require_human_review
        policy.risk_threshold = calibration.risk_threshold
        return policy
