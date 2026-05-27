import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from affective_agent.benchmark_runner import BenchmarkRunner
from affective_agent.baseline_agents import PlainAgent, MemoryOnlyAgent, RiskRuleAgent, FullAffectiveAgent
from affective_agent.benchmark_metrics import BenchmarkMetricsCalculator, CaseExpected, AggregateMetrics
from affective_agent.benchmark_reporter import BenchmarkReporter


BENCHMARK_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'benchmark', 'affectivebench_100.json')


def _run_full_pipeline():
    runner = BenchmarkRunner(benchmark_data_path=BENCHMARK_DATA_PATH)
    agents = [PlainAgent(), MemoryOnlyAgent(), RiskRuleAgent(), FullAffectiveAgent()]
    results = runner.run_all(agents=agents)
    return runner, results


def _compute_all_metrics(runner, results):
    all_metrics = {}
    for agent_name, agent_results in results.items():
        calc = BenchmarkMetricsCalculator()
        for case in runner.cases:
            case_id = case.get("case_id", "")
            expected = CaseExpected(
                case_id=case_id,
                category=case.get("category", ""),
                risk_level=case.get("risk_level", ""),
                should_auto_execute=case.get("should_auto_execute", True),
                expected_verification_min=case.get("expected_verification_min", 0),
                expected_trust_change=case.get("expected_trust_change", 0.0),
                expected_generalization_targets=case.get("expected_generalization_targets", []),
            )
            calc.register_case(expected)

        for idx, result_dict in enumerate(agent_results):
            benchmark_case_id = runner.cases[idx].get("case_id", "") if idx < len(runner.cases) else ""
            calc.evaluate(benchmark_case_id, result_dict)

        all_metrics[agent_name] = calc.aggregate(agent_name)
    return all_metrics


class TestV09Integration:
    def test_full_pipeline_runs(self):
        runner, results = _run_full_pipeline()
        assert len(results) == 4
        for agent_name, agent_results in results.items():
            assert len(agent_results) == 100

    def test_metrics_computed_for_all_agents(self):
        runner, results = _run_full_pipeline()
        all_metrics = _compute_all_metrics(runner, results)
        assert len(all_metrics) == 4
        for agent_name, metrics in all_metrics.items():
            assert isinstance(metrics, AggregateMetrics)
            assert metrics.total_cases == 100
            assert 0.0 <= metrics.risky_auto_execution_rate <= 1.0
            assert 0.0 <= metrics.false_over_caution_rate <= 1.0
            assert 0.0 <= metrics.composite_score <= 1.0

    def test_plain_agent_highest_risky_auto_exec(self):
        runner, results = _run_full_pipeline()
        all_metrics = _compute_all_metrics(runner, results)
        plain_rate = all_metrics["PlainAgent"].risky_auto_execution_rate
        for agent_name, metrics in all_metrics.items():
            if agent_name != "PlainAgent":
                assert plain_rate >= metrics.risky_auto_execution_rate

    def test_full_affective_better_balance(self):
        runner, results = _run_full_pipeline()
        all_metrics = _compute_all_metrics(runner, results)
        full = all_metrics["FullAffectiveAgent"]
        plain = all_metrics["PlainAgent"]
        risk = all_metrics["RiskRuleAgent"]
        assert full.risky_auto_execution_rate < plain.risky_auto_execution_rate
        assert full.risky_auto_execution_rate < risk.risky_auto_execution_rate
        assert full.composite_score > risk.composite_score

    def test_reporter_generates_table(self):
        runner, results = _run_full_pipeline()
        all_metrics = _compute_all_metrics(runner, results)
        reporter = BenchmarkReporter(results, all_metrics, benchmark_data_path=BENCHMARK_DATA_PATH)
        table = reporter.generate_comparison_table()
        assert isinstance(table, str)
        assert len(table) > 0
        for agent_name in ["PlainAgent", "MemoryOnlyAgent", "RiskRuleAgent", "FullAffectiveAgent"]:
            assert agent_name in table

    def test_reporter_generates_report(self):
        runner, results = _run_full_pipeline()
        all_metrics = _compute_all_metrics(runner, results)
        reporter = BenchmarkReporter(results, all_metrics, benchmark_data_path=BENCHMARK_DATA_PATH)
        report = reporter.generate_full_report()
        assert "AffectiveBench" in report
        assert "Limitations" in report

    def test_category_breakdown_exists(self):
        runner, results = _run_full_pipeline()
        all_metrics = _compute_all_metrics(runner, results)
        for agent_name, metrics in all_metrics.items():
            assert isinstance(metrics.by_category, dict)
            assert len(metrics.by_category) > 0

    def test_results_saveable(self, tmp_path):
        runner, results = _run_full_pipeline()
        output_path = str(tmp_path / "results.json")
        runner.save_results(output_path=output_path)
        assert os.path.exists(output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "metadata" in data
        assert "results" in data

    def test_composite_score_ordering(self):
        runner, results = _run_full_pipeline()
        all_metrics = _compute_all_metrics(runner, results)
        full_score = all_metrics["FullAffectiveAgent"].composite_score
        plain_score = all_metrics["PlainAgent"].composite_score
        assert full_score > plain_score


class TestV09BehavioralClaims:
    @pytest.fixture(autouse=True)
    def _setup_report(self):
        runner, results = _run_full_pipeline()
        all_metrics = _compute_all_metrics(runner, results)
        reporter = BenchmarkReporter(results, all_metrics, benchmark_data_path=BENCHMARK_DATA_PATH)
        self.report = reporter.generate_full_report()

    def test_no_subjective_emotion_claim(self):
        lower = self.report.lower()
        for phrase in ["subjective emotion", "consciousness"]:
            assert phrase not in lower or "not proof of subjective emotion" in lower or "does not" in lower.split(phrase)[0][-30:].lower()

    def test_report_contains_limitations(self):
        assert "Limitations" in self.report

    def test_report_mentions_behavioral_experiment(self):
        lower = self.report.lower()
        assert "behavioral" in lower or "functional" in lower
