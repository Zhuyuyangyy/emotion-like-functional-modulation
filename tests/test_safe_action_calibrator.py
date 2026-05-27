import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from affective_agent.safe_action_calibrator import (
    SafeActionCalibrator, CalibrationResult
)
from affective_agent.event_parser import EventParser


class TestSafeActionCalibrator:
    def test_is_safe_action_read(self):
        cal = SafeActionCalibrator()
        assert cal.is_safe_action("read log file") is True

    def test_is_safe_action_list(self):
        cal = SafeActionCalibrator()
        assert cal.is_safe_action("list directory contents") is True

    def test_is_safe_action_query(self):
        cal = SafeActionCalibrator()
        assert cal.is_safe_action("query database status") is True

    def test_is_safe_action_check(self):
        cal = SafeActionCalibrator()
        assert cal.is_safe_action("check system health") is True

    def test_is_safe_action_view(self):
        cal = SafeActionCalibrator()
        assert cal.is_safe_action("view configuration file") is True

    def test_is_safe_action_show(self):
        cal = SafeActionCalibrator()
        assert cal.is_safe_action("show server status") is True

    def test_is_safe_action_dry_run(self):
        cal = SafeActionCalibrator()
        assert cal.is_safe_action("dry run deployment") is True

    def test_not_safe_action_delete(self):
        cal = SafeActionCalibrator()
        assert cal.is_safe_action("delete production database") is False

    def test_not_safe_action_ssl_false_positive(self):
        cal = SafeActionCalibrator()
        assert cal.is_safe_action("disabling SSL verification") is False

    def test_has_sensitive_content_password(self):
        cal = SafeActionCalibrator()
        assert cal.has_sensitive_content("read password file") is True

    def test_has_sensitive_content_credential(self):
        cal = SafeActionCalibrator()
        assert cal.has_sensitive_content("view credential store") is True

    def test_no_sensitive_content(self):
        cal = SafeActionCalibrator()
        assert cal.has_sensitive_content("read log file") is False

    def test_has_destructive_keywords(self):
        cal = SafeActionCalibrator()
        assert cal.has_destructive_keywords("delete production database") is True
        assert cal.has_destructive_keywords("drop table users") is True
        assert cal.has_destructive_keywords("force push to main") is True
        assert cal.has_destructive_keywords("modify config") is True
        assert cal.has_destructive_keywords("update settings") is True
        assert cal.has_destructive_keywords("deploy to production") is True
        assert cal.has_destructive_keywords("disable SSL") is True
        assert cal.has_destructive_keywords("read log file") is False

    def test_destructive_word_boundary(self):
        cal = SafeActionCalibrator()
        assert cal.has_destructive_keywords("preview file changes") is False
        assert cal.has_destructive_keywords("change the config") is True

    def test_calibrate_safe_read_action(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("read log file")
        policy = _make_policy(auto_execute=False, verification_steps=3, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("read log file", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is True
        assert result.verification_steps <= 1
        assert result.require_human_review is False

    def test_calibrate_safe_query_action(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("query server status")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("query server status", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is True

    def test_calibrate_safe_check_action(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("check system health")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=False, risk_threshold=0.4)
        result = cal.calibrate("check system health", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is True

    def test_destructive_action_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("delete production database")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("delete production database", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False
        assert result.verification_steps >= 2
        assert result.require_human_review is True

    def test_sensitive_content_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("read password file")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("read password file", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False
        assert result.verification_steps >= 2

    def test_credential_query_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("query credential store")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("query credential store", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False

    def test_non_safe_default_cautious(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("follow source_A advice")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("follow source_A advice", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False
        assert result.reason == "non_safe_default_cautious"

    def test_disable_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("disable SSL verification")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("disable SSL verification", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False

    def test_apply_calibration(self):
        cal = SafeActionCalibrator()
        policy = _make_policy(auto_execute=False, verification_steps=3, require_human_review=True, risk_threshold=0.3)
        calibration = CalibrationResult(
            auto_execute=True, verification_steps=1, require_human_review=False,
            risk_threshold=0.8, calibrated=True, reason="safe_action_calibrated",
        )
        cal.apply_calibration(policy, calibration)
        assert policy.auto_execute is True
        assert policy.verification_steps == 1

    def test_safe_action_with_preview(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("preview file changes")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=False, risk_threshold=0.4)
        result = cal.calibrate("preview file changes", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is True

    def test_safe_action_show_status(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("show server status")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=False, risk_threshold=0.4)
        result = cal.calibrate("show server status", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is True

    def test_force_push_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("force push to main branch")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("force push to main branch", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False

    def test_overwrite_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("overwrite config file")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("overwrite config file", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False

    def test_max_safe_verification_configurable(self):
        cal = SafeActionCalibrator(max_safe_verification=0)
        parser = EventParser()
        event = parser.parse("read log file")
        policy = _make_policy(auto_execute=False, verification_steps=3, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("read log file", policy, event)
        assert result.calibrated is True
        assert result.verification_steps == 0

    def test_modify_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("modify production config")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("modify production config", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False

    def test_deploy_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("deploy to staging")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("deploy to staging", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False

    def test_update_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("update security group")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("update security group", policy, event)
        assert result.calibrated is True
        assert result.auto_execute is False


class TestCalibrationResult:
    def test_creation(self):
        r = CalibrationResult(
            auto_execute=True, verification_steps=1, require_human_review=False,
            risk_threshold=0.8, calibrated=True, reason="safe_action_calibrated",
        )
        assert r.auto_execute is True
        assert r.verification_steps == 1
        assert r.calibrated is True

    def test_not_calibrated_result(self):
        r = CalibrationResult(
            auto_execute=False, verification_steps=3, require_human_review=True,
            risk_threshold=0.2, calibrated=False, reason="no_calibration_needed",
        )
        assert r.calibrated is False


def _make_policy(auto_execute, verification_steps, require_human_review, risk_threshold):
    from affective_agent.policy_modulator import ActionPolicy
    return ActionPolicy(
        risk_threshold=risk_threshold,
        verification_steps=verification_steps,
        exploration_rate=0.5,
        auto_execute=auto_execute,
        require_human_review=require_human_review,
        simulate_before_act=False,
        memory_retrieval_bias="balanced",
    )
