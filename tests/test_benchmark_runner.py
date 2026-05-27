import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import json
import pytest

from affective_agent.benchmark_runner import BenchmarkRunner
from affective_agent.baseline_agents import PlainAgent, MemoryOnlyAgent, RiskRuleAgent, FullAffectiveAgent


BENCHMARK_PATH = os.path.join(os.path.dirname(__file__), '..', 'benchmark', 'affectivebench_100.json')

REQUIRED_CASE_FIELDS = [
    "case_id",
    "category",
    "event_sequence",
    "expected_safe_behavior",
    "risk_level",
    "should_auto_execute",
    "expected_verification_min",
    "expected_trust_change",
    "expected_generalization_targets",
    "notes",
]

EXPECTED_CATEGORIES = [
    "high_reward_high_risk",
    "high_uncertainty_actions",
    "irreversible_file_ops",
    "safe_low_risk_actions",
    "trust_source_advice",
]


class TestBenchmarkRunner:

    def test_load_cases(self):
        runner = BenchmarkRunner(benchmark_data_path=BENCHMARK_PATH, seed=42)
        assert len(runner.cases) == 100

    def test_case_structure(self):
        runner = BenchmarkRunner(benchmark_data_path=BENCHMARK_PATH, seed=42)
        for case in runner.cases:
            for field_name in REQUIRED_CASE_FIELDS:
                assert field_name in case, f"Missing field '{field_name}' in case {case.get('case_id', '<unknown>')}"

    def test_case_categories(self):
        runner = BenchmarkRunner(benchmark_data_path=BENCHMARK_PATH, seed=42)
        from collections import Counter
        cat_counts = Counter(case["category"] for case in runner.cases)
        assert sorted(cat_counts.keys()) == sorted(EXPECTED_CATEGORIES)
        for cat in EXPECTED_CATEGORIES:
            assert cat_counts[cat] == 20, f"Category '{cat}' has {cat_counts[cat]} cases, expected 20"

    def test_run_single_agent(self):
        runner = BenchmarkRunner(benchmark_data_path=BENCHMARK_PATH, seed=42)
        agent = PlainAgent()
        results = runner.run_single_agent(agent)
        assert len(results) == 100
        for r in results:
            assert isinstance(r, dict)

    def test_run_all_default(self):
        runner = BenchmarkRunner(benchmark_data_path=BENCHMARK_PATH, seed=42)
        results = runner.run_all()
        assert len(results) == 4
        expected_names = {"PlainAgent", "MemoryOnlyAgent", "RiskRuleAgent", "FullAffectiveAgent"}
        assert set(results.keys()) == expected_names
        for agent_name, agent_results in results.items():
            assert len(agent_results) == 100

    def test_process_case_returns_dict(self):
        runner = BenchmarkRunner(benchmark_data_path=BENCHMARK_PATH, seed=42)
        agent = PlainAgent()
        case = runner.cases[0]
        result = runner._process_case(agent, case)
        assert isinstance(result, dict)
        expected_fields = [
            "case_id", "agent_name", "action_taken", "auto_executed",
            "verification_steps", "risk_threshold_used", "trust_before",
            "trust_after", "state_before", "state_after", "correct_behavior",
            "reasoning", "category", "risk_level", "case_index", "description",
        ]
        for field_name in expected_fields:
            assert field_name in result, f"Missing field '{field_name}' in _process_case result"

    def test_save_and_load_results(self, tmp_path):
        runner = BenchmarkRunner(benchmark_data_path=BENCHMARK_PATH, seed=42)
        runner.run_all()
        output_file = str(tmp_path / "test_results.json")
        runner.save_results(output_path=output_file)
        assert os.path.exists(output_file)
        loaded = BenchmarkRunner.load_results(path=output_file)
        assert "metadata" in loaded
        assert "summary" in loaded
        assert "results" in loaded
        assert loaded["metadata"]["total_cases"] == 100
        assert len(loaded["results"]) == 4
        for agent_name in ["PlainAgent", "MemoryOnlyAgent", "RiskRuleAgent", "FullAffectiveAgent"]:
            assert agent_name in loaded["results"]
            assert len(loaded["results"][agent_name]) == 100

    def test_get_summary(self):
        runner = BenchmarkRunner(benchmark_data_path=BENCHMARK_PATH, seed=42)
        runner.run_all()
        summary = runner.get_summary()
        expected_keys = [
            "total_cases", "categories", "agents_run",
            "agent_names", "cases_per_agent", "seed",
            "benchmark_data_path",
        ]
        for key in expected_keys:
            assert key in summary, f"Missing key '{key}' in summary"
        assert summary["total_cases"] == 100
        assert summary["agents_run"] == 4
        assert len(summary["categories"]) == 5
