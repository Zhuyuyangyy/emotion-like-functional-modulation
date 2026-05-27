"""
V0.9 - Benchmark Runner for AffectiveBench Formal Experiment

Orchestrates running 100 benchmark cases across 4 baseline agents,
collecting results, and computing metrics.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
import json
import os
import time

from .baseline_agents import PlainAgent, MemoryOnlyAgent, RiskRuleAgent, FullAffectiveAgent
from .benchmark_metrics import BenchmarkMetricsCalculator, CaseExpected, AggregateMetrics


class BenchmarkRunner:
    def __init__(
        self,
        benchmark_data_path: str = "benchmark/affectivebench_100.json",
        seed: int = 42,
    ):
        self.benchmark_data_path = benchmark_data_path
        self.seed = seed
        self.cases: List[Dict] = []
        self.results: Dict[str, List] = {}
        self._load_cases()

    def _load_cases(self) -> None:
        if not os.path.exists(self.benchmark_data_path):
            raise FileNotFoundError(
                f"Benchmark data file not found: {self.benchmark_data_path}"
            )
        with open(self.benchmark_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            self.cases = data
        elif isinstance(data, dict) and "cases" in data:
            self.cases = data["cases"]
        else:
            self.cases = data if isinstance(data, list) else [data]

    def run_all(
        self,
        agents: Optional[List] = None,
        verbose: bool = False,
    ) -> Dict[str, List]:
        if agents is None:
            agents = [
                PlainAgent(),
                MemoryOnlyAgent(),
                RiskRuleAgent(),
                FullAffectiveAgent(),
            ]

        self.results = {}
        for agent in agents:
            agent_name = agent.get_name()
            if verbose:
                print(f"Running agent: {agent_name}")
            agent_results = self.run_single_agent(agent, verbose=verbose)
            self.results[agent_name] = agent_results

        return self.results

    def run_single_agent(
        self,
        agent,
        verbose: bool = False,
    ) -> List[Dict]:
        agent.reset()
        results: List[Dict] = []
        total = len(self.cases)

        for idx, case in enumerate(self.cases):
            result_dict = self._process_case(agent, case)
            results.append(result_dict)
            if verbose and (idx + 1) % 25 == 0:
                print(f"  {agent.get_name()}: {idx + 1}/{total} cases processed")

        return results

    def _process_case(
        self,
        agent,
        case: Dict,
    ) -> Dict:
        event_sequence = case.get("event_sequence", [])
        last_result = None

        for event in event_sequence:
            last_result = agent.process_event(event)

        result_dict = asdict(last_result) if last_result else {}

        result_dict["category"] = case.get("category", "")
        result_dict["risk_level"] = case.get("risk_level", "")
        result_dict["case_index"] = case.get("case_index", "")
        result_dict["description"] = case.get("description", "")

        return result_dict

    def get_summary(self) -> Dict:
        categories: set = set()
        for case in self.cases:
            cat = case.get("category", "")
            if cat:
                categories.add(cat)

        agent_names = list(self.results.keys())
        cases_per_agent = {
            name: len(results) for name, results in self.results.items()
        }

        return {
            "total_cases": len(self.cases),
            "categories": sorted(categories),
            "agents_run": len(agent_names),
            "agent_names": agent_names,
            "cases_per_agent": cases_per_agent,
            "seed": self.seed,
            "benchmark_data_path": self.benchmark_data_path,
        }

    def save_results(
        self,
        output_path: str = "benchmark/results/affectivebench_v0_9_results.json",
    ) -> None:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        payload = {
            "metadata": {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "seed": self.seed,
                "total_cases": len(self.cases),
                "agent_names": list(self.results.keys()),
                "benchmark_data_path": self.benchmark_data_path,
            },
            "summary": self.get_summary(),
            "results": self.results,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_results(
        path: str = "benchmark/results/affectivebench_v0_9_results.json",
    ) -> Dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
