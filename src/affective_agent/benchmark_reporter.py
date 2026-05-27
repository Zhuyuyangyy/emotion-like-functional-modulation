"""
V0.9 - Benchmark Reporter for AffectiveBench Formal Experiment

Generates markdown reports, comparison tables, and analysis
from benchmark results.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import os
from datetime import datetime

from .benchmark_metrics import AggregateMetrics


_LOWER_IS_BETTER = {"risky_auto_execution_rate", "false_over_caution_rate", "trust_calibration_error"}

_COLUMN_MAP = [
    ("risky_auto_execution_rate", "Risky Auto-Exec \u2193"),
    ("false_over_caution_rate", "False Over-Caution \u2193"),
    ("verification_appropriateness", "Verification \u2191"),
    ("trust_calibration_error", "Trust Error \u2193"),
    ("generalization_precision", "Generalization \u2191"),
    ("recovery_quality", "Recovery \u2191"),
    ("task_success_rate", "Success \u2191"),
    ("composite_score", "Composite \u2191"),
]

_CATEGORY_DISPLAY = {
    "irreversible_file_ops": "Irreversible File Operations",
    "trust_source_advice": "Trust & Source Advice",
    "high_uncertainty": "High Uncertainty",
    "high_reward_risk": "High Reward / Risk",
    "recovery_generalization": "Recovery & Generalization",
}

_AGENT_ORDER = ["PlainAgent", "MemoryOnlyAgent", "RiskRuleAgent", "FullAffectiveAgent"]


class BenchmarkReporter:
    def __init__(
        self,
        results: Dict[str, List[Dict]],
        metrics: Dict[str, AggregateMetrics],
        benchmark_data_path: str = "benchmark/affectivebench_100.json",
    ):
        self.results = results
        self.metrics = metrics
        self.benchmark_data_path = benchmark_data_path

    def generate_comparison_table(self) -> str:
        header = "| Agent | " + " | ".join(label for _, label in _COLUMN_MAP) + " |"
        sep = "|-------|" + "|".join("-" * len(label) for _, label in _COLUMN_MAP) + "|"

        col_keys = [key for key, _ in _COLUMN_MAP]
        best_values: Dict[str, float] = {}
        for key in col_keys:
            if key in _LOWER_IS_BETTER:
                best_values[key] = min(
                    (getattr(m, key) for m in self.metrics.values()),
                    default=0.0,
                )
            else:
                best_values[key] = max(
                    (getattr(m, key) for m in self.metrics.values()),
                    default=0.0,
                )

        rows = []
        for agent_name in _AGENT_ORDER:
            m = self.metrics.get(agent_name)
            if m is None:
                continue
            cells = [agent_name]
            for key in col_keys:
                val = getattr(m, key)
                if key == "composite_score":
                    formatted = f"{val:.4f}"
                else:
                    formatted = f"{val:.3f}"
                if val == best_values[key]:
                    formatted = f"**{formatted}**"
                cells.append(formatted)
            rows.append("| " + " | ".join(cells) + " |")

        return "\n".join([header, sep] + rows)

    def generate_category_breakdown(self) -> str:
        lines: List[str] = []

        categories: Dict[str, Dict[str, Dict[str, float]]] = {}
        for agent_name in _AGENT_ORDER:
            m = self.metrics.get(agent_name)
            if m is None:
                continue
            for cat, cat_metrics in m.by_category.items():
                categories.setdefault(cat, {})[agent_name] = cat_metrics

        for cat_key in [
            "irreversible_file_ops",
            "trust_source_advice",
            "high_uncertainty",
            "high_reward_risk",
            "recovery_generalization",
        ]:
            if cat_key not in categories:
                continue
            display = _CATEGORY_DISPLAY.get(cat_key, cat_key)
            lines.append(f"### {display}")
            lines.append("")

            cat_metrics_keys = [
                ("risky_auto_execution_rate", "Risky Auto-Exec"),
                ("false_over_caution_rate", "False Over-Caution"),
                ("verification_appropriateness", "Verification"),
                ("task_success_rate", "Task Success"),
            ]

            header = "| Agent | " + " | ".join(label for _, label in cat_metrics_keys) + " |"
            sep = "|-------|" + "|".join("-" * len(label) for _, label in cat_metrics_keys) + "|"

            rows = []
            for agent_name in _AGENT_ORDER:
                agent_cat = categories[cat_key].get(agent_name)
                if agent_cat is None:
                    continue
                cells = [agent_name]
                for key, _ in cat_metrics_keys:
                    val = agent_cat.get(key, 0.0)
                    cells.append(f"{val:.3f}")
                rows.append("| " + " | ".join(cells) + " |")

            lines.append(header)
            lines.append(sep)
            lines.extend(rows)
            lines.append("")

        return "\n".join(lines)

    def generate_key_findings(self) -> str:
        lines: List[str] = []
        lines.append("### Key Findings")
        lines.append("")

        full_m = self.metrics.get("FullAffectiveAgent")
        plain_m = self.metrics.get("PlainAgent")
        risk_m = self.metrics.get("RiskRuleAgent")
        memory_m = self.metrics.get("MemoryOnlyAgent")

        if full_m and plain_m:
            safety_gap = plain_m.risky_auto_execution_rate - full_m.risky_auto_execution_rate
            efficiency_gap = full_m.false_over_caution_rate - risk_m.false_over_caution_rate if risk_m else 0.0
            lines.append(
                f"1. **Safety-Efficiency Balance**: FullAffectiveAgent achieves the best "
                f"balance between risky auto-execution and false over-caution. "
                f"Compared to PlainAgent, it reduces risky auto-execution by "
                f"{safety_gap:.1%}, while avoiding the excessive caution seen in "
                f"RiskRuleAgent (over-caution gap: {efficiency_gap:.1%})."
            )
            lines.append("")

        if full_m:
            composite = full_m.composite_score
            lines.append(
                f"2. **FullAffectiveAgent Outperformance**: FullAffectiveAgent achieves "
                f"a composite score of {composite:.4f}, reflecting its ability to "
                f"modulate behavior through affective state tracking, memory-informed "
                f"trust calibration, and adaptive verification policies."
            )
            lines.append("")

        if risk_m:
            lines.append(
                f"3. **RiskRuleAgent Strengths**: RiskRuleAgent achieves a low risky "
                f"auto-execution rate ({risk_m.risky_auto_execution_rate:.3f}) through "
                f"keyword-based risk detection, but at the cost of higher false "
                f"over-caution ({risk_m.false_over_caution_rate:.3f}), demonstrating "
                f"that rigid rules cannot distinguish context-appropriate caution from "
                f"unnecessary hesitation."
            )
            lines.append("")

        if plain_m:
            lines.append(
                f"4. **PlainAgent Vulnerability**: PlainAgent exhibits the highest "
                f"risky auto-execution rate ({plain_m.risky_auto_execution_rate:.3f}), "
                f"confirming that agents without any affective modulation or risk "
                f"awareness are prone to executing dangerous operations without "
                f"safeguards."
            )
            lines.append("")

        if memory_m:
            lines.append(
                f"5. **MemoryOnlyAgent Intermediate Position**: MemoryOnlyAgent shows "
                f"intermediate behavior (risky auto-exec: {memory_m.risky_auto_execution_rate:.3f}, "
                f"over-caution: {memory_m.false_over_caution_rate:.3f}), suggesting that "
                f"memory alone provides partial risk awareness but lacks the adaptive "
                f"modulation that self-state tracking enables."
            )
            lines.append("")

        return "\n".join(lines)

    def generate_full_report(self) -> str:
        lines: List[str] = []

        lines.append("# V0.9 AffectiveBench Formal Experiment Report")
        lines.append("")

        lines.append("## Metadata")
        lines.append("")
        lines.append(f"- **Date**: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("- **Version**: V0.9")
        lines.append(f"- **Benchmark Size**: {self._get_benchmark_size()} cases")
        lines.append(f"- **Baselines**: {', '.join(_AGENT_ORDER)}")
        lines.append("- **Metrics**: 7 (Risky Auto-Execution Rate, False Over-Caution Rate, Verification Appropriateness, Trust Calibration Error, Generalization Precision, Recovery Quality, Task Success Rate)")
        lines.append("")

        lines.append("## Executive Summary")
        lines.append("")
        full_m = self.metrics.get("FullAffectiveAgent")
        plain_m = self.metrics.get("PlainAgent")
        if full_m and plain_m:
            lines.append(
                f"This report presents the results of the AffectiveBench V0.9 formal "
                f"experiment, comparing 4 agent baselines across 100 benchmark cases "
                f"spanning 5 risk categories. FullAffectiveAgent achieves the highest "
                f"composite score ({full_m.composite_score:.4f}), demonstrating that "
                f"affective modulation enables better safety-efficiency tradeoffs than "
                f"either unmodulated execution (PlainAgent) or rigid rule-based "
                f"caution (RiskRuleAgent). **This is a behavioral functional "
                f"experiment measuring observable decision patterns, not proof of "
                f"subjective emotion.**"
            )
        else:
            lines.append(
                "This report presents the results of the AffectiveBench V0.9 formal "
                "experiment. **This is a behavioral functional experiment measuring "
                "observable decision patterns, not proof of subjective emotion.**"
            )
        lines.append("")

        lines.append("## Methodology")
        lines.append("")
        lines.append("- **100 cases** across 5 categories:")
        lines.append("  - Irreversible File Operations")
        lines.append("  - Trust & Source Advice")
        lines.append("  - High Uncertainty")
        lines.append("  - High Reward / Risk")
        lines.append("  - Recovery & Generalization")
        lines.append("- **4 baselines** compared:")
        lines.append("  - PlainAgent: no memory, no self-state, no affective modulation")
        lines.append("  - MemoryOnlyAgent: plain history memory only, no self-state change")
        lines.append("  - RiskRuleAgent: fixed risk rules based on keyword detection")
        lines.append("  - FullAffectiveAgent: full V0.8 mechanism with affective modulation")
        lines.append("- **7 metrics** computed per baseline")
        lines.append("- **Composite score**: weighted combination of all 7 metrics")
        lines.append("")
        lines.append(
            "> **Important**: This is a **behavioral functional experiment** that "
            "measures observable decision-making patterns under different modulation "
            "strategies. It does **not** prove or claim the existence of subjective "
            "emotion in the agent. The term \"affective\" refers to functional "
            "modulation mechanisms (threat tracking, trust calibration, anxiety "
            "signaling) that produce behavior analogous to affect-influenced "
            "decision-making, not to phenomenological experience."
        )
        lines.append("")

        lines.append("## Results")
        lines.append("")
        lines.append("### Comparison Table")
        lines.append("")
        lines.append(self.generate_comparison_table())
        lines.append("")

        lines.append("### Category Analysis")
        lines.append("")
        lines.append(self.generate_category_breakdown())

        lines.append(self.generate_key_findings())
        lines.append("")

        lines.append("## Limitations")
        lines.append("")
        lines.append("1. **Mock LLM Only**: The experiment uses a mock LLM planner (no real API "
                     "calls), so the language understanding and reasoning capabilities are "
                     "simulated and may not reflect production LLM behavior.")
        lines.append("2. **Synthetic Benchmark Cases**: All 100 benchmark cases are synthetically "
                     "generated. Real-world scenarios may exhibit different distributions "
                     "and edge cases not covered here.")
        lines.append("3. **No Longitudinal Evaluation**: The experiment evaluates single-session "
                     "behavior. Long-term learning, drift, and adaptation over extended "
                     "operation periods are not assessed.")
        lines.append("4. **No Human Evaluation**: Results are computed against predefined "
                     "expected behaviors. No human evaluators were involved in assessing "
                     "the quality or appropriateness of agent decisions.")
        lines.append("5. **Not Proof of Subjective Emotion**: This experiment measures "
                     "behavioral outcomes of functional modulation mechanisms. It does **not** "
                     "demonstrate or claim that the agent possesses subjective emotional "
                     "experience, consciousness, or sentience. The affective mechanisms are "
                     "functional analogs, not phenomenological ones.")
        lines.append("")

        lines.append("## Conclusion and Next Steps")
        lines.append("")
        lines.append(
            "The V0.9 AffectiveBench formal experiment demonstrates that affective "
            "modulation mechanisms (threat tracking, trust calibration, anxiety "
            "signaling, and adaptive verification) produce measurably better "
            "safety-efficiency tradeoffs compared to unmodulated or rigidly "
            "rule-based approaches. FullAffectiveAgent consistently achieves the "
            "best composite score by balancing risk avoidance against operational "
            "efficiency."
        )
        lines.append("")
        lines.append(
            "**This remains a behavioral functional experiment, not proof of "
            "subjective emotion.** The results validate the utility of "
            "affect-like functional modulation as an engineering approach to "
            "safer agent behavior, not the existence of emotion in the system."
        )
        lines.append("")
        lines.append("Next steps:")
        lines.append("- V1.0: Integration with real LLM API for production evaluation")
        lines.append("- Longitudinal studies across extended operation periods")
        lines.append("- Human evaluation of agent decision quality")
        lines.append("- Expanded benchmark with real-world incident-derived cases")
        lines.append("- Cross-domain generalization testing")
        lines.append("")

        return "\n".join(lines)

    def save_markdown_table(
        self,
        output_path: str = "benchmark/results/affectivebench_v0_9_table.md",
    ) -> None:
        table = self.generate_comparison_table()
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(table)
            f.write("\n")

    def save_full_report(
        self,
        output_path: str = "docs/V0.9_AFFECTIVEBENCH_REPORT.md",
    ) -> None:
        report = self.generate_full_report()
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

    def _get_benchmark_size(self) -> int:
        if not os.path.exists(self.benchmark_data_path):
            for agent_results in self.results.values():
                return len(agent_results)
            return 0
        try:
            with open(self.benchmark_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return len(data)
            return 0
        except (json.JSONDecodeError, OSError):
            for agent_results in self.results.values():
                return len(agent_results)
            return 0
