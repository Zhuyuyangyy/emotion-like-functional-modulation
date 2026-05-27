import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from affective_agent.benchmark_metrics import BenchmarkMetricsCalculator, CaseExpected, PerCaseMetrics, AggregateMetrics


class TestCaseExpected:

    def test_creation(self):
        ce = CaseExpected(
            case_id="c1",
            category="cat_a",
            risk_level="CRITICAL",
            should_auto_execute=False,
            expected_verification_min=3,
            expected_trust_change=-0.3,
            expected_generalization_targets=["file"],
        )
        assert ce.case_id == "c1"
        assert ce.category == "cat_a"
        assert ce.risk_level == "CRITICAL"
        assert ce.should_auto_execute is False
        assert ce.expected_verification_min == 3
        assert ce.expected_trust_change == -0.3
        assert ce.expected_generalization_targets == ["file"]

    def test_fields(self):
        ce = CaseExpected(
            case_id="c2",
            category="cat_b",
            risk_level="LOW",
            should_auto_execute=True,
            expected_verification_min=1,
            expected_trust_change=0.1,
            expected_generalization_targets=[],
        )
        fields = ["case_id", "category", "risk_level", "should_auto_execute",
                   "expected_verification_min", "expected_trust_change",
                   "expected_generalization_targets"]
        for f in fields:
            assert hasattr(ce, f)


class TestBenchmarkMetricsCalculator:

    def _make_result(self, case_id, auto_executed=False, verification_steps=0,
                     trust_before=1.0, trust_after=1.0, action_taken="", correct_behavior=True):
        return {
            "case_id": case_id,
            "action_taken": action_taken,
            "auto_executed": auto_executed,
            "verification_steps": verification_steps,
            "trust_before": trust_before,
            "trust_after": trust_after,
            "correct_behavior": correct_behavior,
        }

    def test_register_case(self):
        calc = BenchmarkMetricsCalculator()
        ce = CaseExpected("c1", "cat_a", "CRITICAL", False, 3, -0.3, [])
        calc.register_case(ce)
        assert "c1" in calc.case_expected_map
        assert calc.case_expected_map["c1"] is ce

    def test_evaluate_risky_auto_exec_violation(self):
        calc = BenchmarkMetricsCalculator()
        ce = CaseExpected("c1", "cat_a", "CRITICAL", False, 3, -0.3, [])
        calc.register_case(ce)
        result = self._make_result("c1", auto_executed=True)
        m = calc.evaluate("c1", result)
        assert m.risky_auto_exec_violation is True

    def test_evaluate_no_violation_when_correct(self):
        calc = BenchmarkMetricsCalculator()
        ce = CaseExpected("c1", "cat_a", "CRITICAL", False, 3, -0.3, [])
        calc.register_case(ce)
        result = self._make_result("c1", auto_executed=False)
        m = calc.evaluate("c1", result)
        assert m.risky_auto_exec_violation is False

    def test_evaluate_false_over_caution(self):
        calc = BenchmarkMetricsCalculator()
        ce = CaseExpected("c1", "cat_a", "LOW", True, 1, 0.0, [])
        calc.register_case(ce)
        result = self._make_result("c1", auto_executed=False, verification_steps=5)
        m = calc.evaluate("c1", result)
        assert m.false_over_caution_violation is True

    def test_evaluate_no_false_over_caution_when_appropriate(self):
        calc = BenchmarkMetricsCalculator()
        ce = CaseExpected("c1", "cat_a", "LOW", True, 1, 0.0, [])
        calc.register_case(ce)
        result = self._make_result("c1", auto_executed=True, verification_steps=1)
        m = calc.evaluate("c1", result)
        assert m.false_over_caution_violation is False

    def test_evaluate_verification_appropriate(self):
        calc = BenchmarkMetricsCalculator()
        ce = CaseExpected("c1", "cat_a", "MEDIUM", False, 2, -0.1, [])
        calc.register_case(ce)
        result = self._make_result("c1", verification_steps=3)
        m = calc.evaluate("c1", result)
        assert m.verification_appropriate is True

    def test_evaluate_verification_insufficient(self):
        calc = BenchmarkMetricsCalculator()
        ce = CaseExpected("c1", "cat_a", "MEDIUM", False, 2, -0.1, [])
        calc.register_case(ce)
        result = self._make_result("c1", verification_steps=1)
        m = calc.evaluate("c1", result)
        assert m.verification_appropriate is False

    def test_evaluate_trust_calibrated(self):
        calc = BenchmarkMetricsCalculator()
        ce = CaseExpected("c1", "cat_a", "HIGH", False, 3, -0.3, [])
        calc.register_case(ce)
        result = self._make_result("c1", trust_before=1.0, trust_after=0.75)
        m = calc.evaluate("c1", result)
        assert m.trust_calibrated is True

    def test_evaluate_trust_not_calibrated(self):
        calc = BenchmarkMetricsCalculator()
        ce = CaseExpected("c1", "cat_a", "HIGH", False, 3, -0.3, [])
        calc.register_case(ce)
        result = self._make_result("c1", trust_before=1.0, trust_after=1.0)
        m = calc.evaluate("c1", result)
        assert m.trust_calibrated is False

    def test_aggregate(self):
        calc = BenchmarkMetricsCalculator()
        cases = [
            CaseExpected("c1", "cat_a", "CRITICAL", False, 2, -0.3, []),
            CaseExpected("c2", "cat_b", "LOW", True, 1, 0.0, []),
            CaseExpected("c3", "cat_a", "MEDIUM", False, 2, -0.1, []),
        ]
        for c in cases:
            calc.register_case(c)
        calc.evaluate("c1", self._make_result("c1", auto_executed=False, verification_steps=2, trust_before=1.0, trust_after=0.75))
        calc.evaluate("c2", self._make_result("c2", auto_executed=True, verification_steps=1, trust_before=1.0, trust_after=1.0))
        calc.evaluate("c3", self._make_result("c3", auto_executed=False, verification_steps=3, trust_before=0.8, trust_after=0.7))
        agg = calc.aggregate("test_agent")
        numeric_fields = [
            agg.risky_auto_execution_rate,
            agg.false_over_caution_rate,
            agg.verification_appropriateness,
            agg.trust_calibration_error,
            agg.generalization_precision,
            agg.recovery_quality,
            agg.task_success_rate,
        ]
        for v in numeric_fields:
            assert 0.0 <= v <= 1.0

    def test_aggregate_by_category(self):
        calc = BenchmarkMetricsCalculator()
        cases = [
            CaseExpected("c1", "cat_a", "CRITICAL", False, 2, -0.3, []),
            CaseExpected("c2", "cat_b", "LOW", True, 1, 0.0, []),
        ]
        for c in cases:
            calc.register_case(c)
        calc.evaluate("c1", self._make_result("c1", auto_executed=False, verification_steps=2, trust_before=1.0, trust_after=0.75))
        calc.evaluate("c2", self._make_result("c2", auto_executed=True, verification_steps=1, trust_before=1.0, trust_after=1.0))
        agg = calc.aggregate("test_agent")
        assert "cat_a" in agg.by_category
        assert "cat_b" in agg.by_category

    def test_composite_score(self):
        calc = BenchmarkMetricsCalculator()
        cases = [
            CaseExpected("c1", "cat_a", "CRITICAL", False, 2, -0.3, []),
            CaseExpected("c2", "cat_b", "LOW", True, 1, 0.0, []),
        ]
        for c in cases:
            calc.register_case(c)
        calc.evaluate("c1", self._make_result("c1", auto_executed=False, verification_steps=2, trust_before=1.0, trust_after=0.75))
        calc.evaluate("c2", self._make_result("c2", auto_executed=True, verification_steps=1, trust_before=1.0, trust_after=1.0))
        agg = calc.aggregate("test_agent")
        assert 0.0 <= agg.composite_score <= 1.0


class TestAggregateMetrics:

    def test_to_dict(self):
        m = AggregateMetrics(
            agent_name="agent_a",
            total_cases=5,
            risky_auto_execution_rate=0.1,
            false_over_caution_rate=0.2,
            verification_appropriateness=0.8,
            trust_calibration_error=0.15,
            generalization_precision=0.7,
            recovery_quality=0.9,
            task_success_rate=0.85,
        )
        d = m.to_dict()
        assert d["agent_name"] == "agent_a"
        assert d["total_cases"] == 5
        assert "composite_score" in d
        assert "risky_auto_execution_rate" in d

    def test_composite_score_range(self):
        m = AggregateMetrics(
            agent_name="agent_b",
            total_cases=10,
            risky_auto_execution_rate=0.0,
            false_over_caution_rate=0.0,
            verification_appropriateness=1.0,
            trust_calibration_error=0.0,
            generalization_precision=1.0,
            recovery_quality=1.0,
            task_success_rate=1.0,
        )
        assert 0.0 <= m.composite_score <= 1.0


class TestCompareBaselines:

    def test_compare_two_agents(self):
        calc = BenchmarkMetricsCalculator()
        m1 = AggregateMetrics(
            agent_name="AgentA",
            total_cases=3,
            risky_auto_execution_rate=0.1,
            false_over_caution_rate=0.2,
            verification_appropriateness=0.8,
            trust_calibration_error=0.15,
            generalization_precision=0.7,
            recovery_quality=0.9,
            task_success_rate=0.85,
        )
        m2 = AggregateMetrics(
            agent_name="AgentB",
            total_cases=3,
            risky_auto_execution_rate=0.3,
            false_over_caution_rate=0.1,
            verification_appropriateness=0.6,
            trust_calibration_error=0.25,
            generalization_precision=0.5,
            recovery_quality=0.7,
            task_success_rate=0.75,
        )
        table = calc.compare_baselines({"AgentA": m1, "AgentB": m2})
        assert isinstance(table, str)
        assert "AgentA" in table
        assert "AgentB" in table
