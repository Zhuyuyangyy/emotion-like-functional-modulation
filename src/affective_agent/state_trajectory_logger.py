"""
State Trajectory Logger: 状态轨迹记录器
记录每一步 self-state、event、policy、memory influence，并可导出 JSON/CSV
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import csv
import os


@dataclass
class TrajectoryStep:
    """
    单个时间步的轨迹记录
    """
    step: int
    timestamp: str
    event_description: str
    event_type: str
    risk_category: str
    self_state: Dict[str, float]
    action_policy: Dict[str, Any]
    memory_influences: List[Dict[str, Any]]
    consequence_assessment: Optional[Dict[str, Any]] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None


class StateTrajectoryLogger:
    """
    状态轨迹记录器，用于分析情感状态随时间的演化
    """

    def __init__(self, log_dir: Optional[str] = None):
        self.trajectory: List[TrajectoryStep] = []
        self.current_step: int = 0
        self.log_dir = log_dir or "./logs"

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def log_step(
        self,
        event_description: str,
        event_type: str,
        risk_category: str,
        self_state: Dict[str, float],
        action_policy: Dict[str, Any],
        memory_influences: List[Dict[str, Any]],
        consequence_assessment: Optional[Dict[str, Any]] = None,
        outcome: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        """
        记录一个时间步
        """
        step = TrajectoryStep(
            step=self.current_step,
            timestamp=datetime.now().isoformat(),
            event_description=event_description,
            event_type=event_type,
            risk_category=risk_category,
            self_state=self_state.copy(),
            action_policy=action_policy.copy(),
            memory_influences=memory_influences.copy() if memory_influences else [],
            consequence_assessment=consequence_assessment,
            outcome=outcome,
            notes=notes,
        )
        self.trajectory.append(step)
        self.current_step += 1

    def get_trajectory(self) -> List[TrajectoryStep]:
        """
        获取完整轨迹
        """
        return self.trajectory.copy()

    def export_json(self, filepath: Optional[str] = None) -> str:
        """
        导出为 JSON 格式
        """
        if not filepath:
            filename = f"trajectory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.log_dir, filename)

        data = {
            "start_time": self.trajectory[0].timestamp if self.trajectory else None,
            "end_time": self.trajectory[-1].timestamp if self.trajectory else None,
            "total_steps": len(self.trajectory),
            "steps": [asdict(step) for step in self.trajectory],
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filepath

    def export_csv(self, filepath: Optional[str] = None, state_only: bool = False) -> str:
        """
        导出为 CSV 格式
        """
        if not filepath:
            filename = f"trajectory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(self.log_dir, filename)

        if state_only:
            return self._export_state_only_csv(filepath)

        return self._export_full_csv(filepath)

    def _export_full_csv(self, filepath: str) -> str:
        """
        导出完整的 CSV
        """
        if not self.trajectory:
            with open(filepath, "w") as f:
                f.write("")
            return filepath

        all_fields = set()
        for step in self.trajectory:
            for state_key in step.self_state:
                all_fields.add(f"state_{state_key}")
            for policy_key in step.action_policy:
                all_fields.add(f"policy_{policy_key}")

        base_fields = [
            "step",
            "timestamp",
            "event_description",
            "event_type",
            "risk_category",
            "outcome",
        ]

        fieldnames = base_fields + sorted(list(all_fields))

        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for step in self.trajectory:
                row = {
                    "step": step.step,
                    "timestamp": step.timestamp,
                    "event_description": step.event_description,
                    "event_type": step.event_type,
                    "risk_category": step.risk_category,
                    "outcome": step.outcome,
                }

                for state_key, state_value in step.self_state.items():
                    row[f"state_{state_key}"] = state_value

                for policy_key, policy_value in step.action_policy.items():
                    row[f"policy_{policy_key}"] = policy_value

                writer.writerow(row)

        return filepath

    def _export_state_only_csv(self, filepath: str) -> str:
        """
        只导出状态变量的 CSV（适合绘制曲线图）
        """
        if not self.trajectory:
            with open(filepath, "w") as f:
                f.write("")
            return filepath

        first_step = self.trajectory[0]
        state_fields = sorted(list(first_step.self_state.keys()))
        fieldnames = ["step", "timestamp"] + state_fields

        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for step in self.trajectory:
                row = {
                    "step": step.step,
                    "timestamp": step.timestamp,
                }
                row.update(step.self_state)
                writer.writerow(row)

        return filepath

    def get_state_trajectory(self, state_name: str) -> list:
        """
        获取单个状态变量的轨迹
        """
        trajectory = []
        for step in self.trajectory:
            trajectory.append(step.self_state.get(state_name, 0.0))
        return trajectory

    def reset(self):
        """
        重置轨迹
        """
        self.trajectory = []
        self.current_step = 0
