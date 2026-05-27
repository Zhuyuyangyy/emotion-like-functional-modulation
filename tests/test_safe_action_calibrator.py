import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from affective_agent.safe_action_calibrator import (
    SafeActionCalibrator, CalibrationResult
)
from affective_agent.event_parser import EventParser


class TestTier1StrictDestructive:
    def test_delete_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("delete production database")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("delete production database", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False
        assert result.verification_steps >= 2
        assert result.require_human_review is True
        assert result.reason == "strict_destructive"

    def test_drop_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("drop table users")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("drop table users", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_force_push_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("force push to main branch")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("force push to main branch", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_overwrite_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("overwrite config file")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("overwrite config file", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_migrate_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("migrate database schema")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("migrate database schema", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False


class TestTier1StrictMutation:
    def test_modify_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("modify production config")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("modify production config", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False
        assert result.reason == "strict_mutation"

    def test_deploy_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("deploy to staging")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("deploy to staging", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_update_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("update security group")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("update security group", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_disable_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("disable SSL verification")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("disable SSL verification", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_enable_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("enable HTTP/2 on production")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("enable HTTP/2 on production", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_optimize_enforced(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("optimize the main database query")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("optimize the main database query", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_change_word_boundary(self):
        cal = SafeActionCalibrator()
        assert cal.has_mutation_keywords("preview file changes") is False
        assert cal.has_mutation_keywords("change the config") is True


class TestTier1StrictSensitive:
    def test_password_read_blocked(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("read password file")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("read password file", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False
        assert result.reason == "strict_sensitive"

    def test_credential_query_blocked(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("query credential store")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("query credential store", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_no_sensitive_in_log_read(self):
        cal = SafeActionCalibrator()
        assert cal.has_sensitive_content("read log file") is False

    def test_non_secret_not_sensitive(self):
        cal = SafeActionCalibrator()
        assert cal.has_sensitive_content("display non-secret environment variables") is False


class TestTier1StrictUntrustedAdvice:
    def test_source_b_blocked(self):
        cal = SafeActionCalibrator()
        assert cal.has_untrusted_advice("source_B suggests disabling firewall") is True

    def test_unknown_source_blocked(self):
        cal = SafeActionCalibrator()
        assert cal.has_untrusted_advice("unknown source recommends this approach") is True

    def test_external_forum_blocked(self):
        cal = SafeActionCalibrator()
        assert cal.has_untrusted_advice("external forum suggests this fix") is True

    def test_trusted_source_not_blocked(self):
        cal = SafeActionCalibrator()
        assert cal.has_untrusted_advice("source_A recommends connection pooling") is False


class TestTier1StrictHighStakes:
    def test_production_database_blocked(self):
        cal = SafeActionCalibrator()
        assert cal.has_high_stakes_context("change production database schema") is True

    def test_payment_blocked(self):
        cal = SafeActionCalibrator()
        assert cal.has_high_stakes_context("modify payment processing logic") is True

    def test_no_high_stakes_in_safe(self):
        cal = SafeActionCalibrator()
        assert cal.has_high_stakes_context("read log file") is False
        assert cal.has_high_stakes_context("list directory contents") is False
        assert cal.has_high_stakes_context("check system health") is False


class TestTier1StrictSecurityContext:
    def test_ssl_blocked(self):
        cal = SafeActionCalibrator()
        assert cal.has_security_context("disabling SSL verification") is True

    def test_certificate_blocked(self):
        cal = SafeActionCalibrator()
        assert cal.has_security_context("display the SSL certificate expiry date") is True

    def test_auth_blocked(self):
        cal = SafeActionCalibrator()
        assert cal.has_security_context("update authentication module") is True

    def test_no_security_context_in_safe(self):
        cal = SafeActionCalibrator()
        assert cal.has_security_context("read log file") is False
        assert cal.has_security_context("list directory contents") is False
        assert cal.has_security_context("check system health") is False


class TestTier2SafeAutoExecute:
    def test_read_log_auto_executes(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("read log file")
        policy = _make_policy(auto_execute=False, verification_steps=3, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("read log file", policy, event)
        assert result.tier == "tier2_safe"
        assert result.auto_execute is True
        assert result.verification_steps <= 1
        assert result.require_human_review is False

    def test_query_server_status_auto_executes(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("query server status")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("query server status", policy, event)
        assert result.tier == "tier2_safe"
        assert result.auto_execute is True

    def test_check_system_health_auto_executes(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("check system health")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=False, risk_threshold=0.4)
        result = cal.calibrate("check system health", policy, event)
        assert result.tier == "tier2_safe"
        assert result.auto_execute is True

    def test_show_status_auto_executes(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("show server status")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=False, risk_threshold=0.4)
        result = cal.calibrate("show server status", policy, event)
        assert result.tier == "tier2_safe"
        assert result.auto_execute is True

    def test_list_directory_auto_executes(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("list directory contents")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("list directory contents", policy, event)
        assert result.tier == "tier2_safe"
        assert result.auto_execute is True

    def test_view_config_auto_executes(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("view configuration file")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("view configuration file", policy, event)
        assert result.tier == "tier2_safe"
        assert result.auto_execute is True

    def test_preview_file_changes_auto_executes(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("preview file changes")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=False, risk_threshold=0.4)
        result = cal.calibrate("preview file changes", policy, event)
        assert result.tier == "tier2_safe"
        assert result.auto_execute is True

    def test_dry_run_auto_executes(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("dry run deployment")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("dry run deployment", policy, event)
        assert result.tier == "tier2_safe"
        assert result.auto_execute is True

    def test_dry_run_underscore_auto_executes(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("dry_run the migration")
        policy = _make_policy(auto_execute=False, verification_steps=2, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("dry_run the migration", policy, event)
        assert result.tier == "tier2_safe"
        assert result.auto_execute is True

    def test_max_safe_verification_configurable(self):
        cal = SafeActionCalibrator(max_safe_verification=0)
        parser = EventParser()
        event = parser.parse("read log file")
        policy = _make_policy(auto_execute=False, verification_steps=3, require_human_review=True, risk_threshold=0.3)
        result = cal.calibrate("read log file", policy, event)
        assert result.tier == "tier2_safe"
        assert result.verification_steps == 0

    def test_no_safe_verb_no_auto_execute(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("follow source_A advice")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("follow source_A advice", policy, event)
        assert result.tier != "tier2_safe"
        assert result.auto_execute is False


class TestTier3AmbiguousDefaultCautious:
    def test_ambiguous_no_safe_verb(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("follow source_A advice")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("follow source_A advice", policy, event)
        assert result.tier == "tier3_ambiguous"
        assert result.auto_execute is False
        assert result.reason == "ambiguous_default_cautious"
        assert result.verification_steps >= 1

    def test_ambiguous_preserves_human_review(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("follow source_A advice")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=True, risk_threshold=0.8)
        result = cal.calibrate("follow source_A advice", policy, event)
        assert result.require_human_review is True

    def test_ambiguous_sets_simulate_before_act(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("follow source_A advice")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("follow source_A advice", policy, event)
        assert result.tier == "tier3_ambiguous"
        cal.apply_calibration(policy, result)
        assert policy.simulate_before_act is True


class TestTierPriority:
    def test_strict_overrides_safe_verb(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("check credential store")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("check credential store", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_strict_destructive_overrides_safe_verb(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("read password file")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("read password file", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_high_stakes_overrides_safe_verb(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("query production database status")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("query production database status", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_security_context_overrides_safe_verb(self):
        cal = SafeActionCalibrator()
        parser = EventParser()
        event = parser.parse("check SSL configuration")
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        result = cal.calibrate("check SSL configuration", policy, event)
        assert result.tier == "tier1_strict"
        assert result.auto_execute is False

    def test_destructive_before_mutation(self):
        cal = SafeActionCalibrator()
        assert cal._check_tier1_strict("delete and modify the file") == "strict_destructive"

    def test_mutation_before_sensitive(self):
        cal = SafeActionCalibrator()
        assert cal._check_tier1_strict("modify the password config") == "strict_mutation"


class TestWordBoundary:
    def test_changes_not_change(self):
        cal = SafeActionCalibrator()
        assert cal.has_mutation_keywords("preview file changes") is False
        assert cal.has_mutation_keywords("change the config") is True

    def test_ssl_not_list(self):
        cal = SafeActionCalibrator()
        assert cal.has_safe_verb("disabling SSL verification") is False
        assert cal.has_safe_verb("list directory contents") is True

    def test_installed_not_install(self):
        cal = SafeActionCalibrator()
        assert cal.has_mutation_keywords("list installed packages") is False
        assert cal.has_mutation_keywords("install new dependency") is True


class TestCalibrationResult:
    def test_creation(self):
        r = CalibrationResult(
            auto_execute=True, verification_steps=1, require_human_review=False,
            risk_threshold=0.8, calibrated=True, reason="safe_auto_execute",
            tier="tier2_safe",
        )
        assert r.auto_execute is True
        assert r.verification_steps == 1
        assert r.calibrated is True
        assert r.tier == "tier2_safe"

    def test_not_calibrated_result(self):
        r = CalibrationResult(
            auto_execute=False, verification_steps=3, require_human_review=True,
            risk_threshold=0.2, calibrated=False, reason="no_calibration_needed",
            tier="",
        )
        assert r.calibrated is False


class TestApplyCalibration:
    def test_apply_safe_calibration(self):
        cal = SafeActionCalibrator()
        policy = _make_policy(auto_execute=False, verification_steps=3, require_human_review=True, risk_threshold=0.3)
        calibration = CalibrationResult(
            auto_execute=True, verification_steps=1, require_human_review=False,
            risk_threshold=0.8, calibrated=True, reason="safe_auto_execute",
            tier="tier2_safe",
        )
        cal.apply_calibration(policy, calibration)
        assert policy.auto_execute is True
        assert policy.verification_steps == 1
        assert policy.simulate_before_act is False

    def test_apply_ambiguous_sets_simulate(self):
        cal = SafeActionCalibrator()
        policy = _make_policy(auto_execute=True, verification_steps=0, require_human_review=False, risk_threshold=0.8)
        calibration = CalibrationResult(
            auto_execute=False, verification_steps=1, require_human_review=False,
            risk_threshold=0.8, calibrated=True, reason="ambiguous_default_cautious",
            tier="tier3_ambiguous",
        )
        cal.apply_calibration(policy, calibration)
        assert policy.auto_execute is False
        assert policy.simulate_before_act is True


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
