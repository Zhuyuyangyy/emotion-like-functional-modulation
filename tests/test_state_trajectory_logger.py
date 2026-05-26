"""
Tests for State Trajectory Logger
"""

import sys
sys.path.insert(0, '/workspace/src')

import pytest
import os
from src.affective_agent.state_trajectory_logger import StateTrajectoryLogger


class TestStateTrajectoryLogger:
    def test_log_single_step(self):
        logger = StateTrajectoryLogger()
        logger.log_step(
            event_description="test event",
            event_type="test",
            risk_category="general",
            self_state={"threat": 0.1, "confidence": 1.0},
            action_policy={"risk_threshold": 0.5, "verification_steps": 1},
            memory_influences=[]
        )

        trajectory = logger.get_trajectory()
        assert len(trajectory) == 1
        assert trajectory[0].event_description == "test event"
        assert trajectory[0].self_state["threat"] == 0.1

    def test_log_multiple_steps(self):
        logger = StateTrajectoryLogger()

        for i in range(5):
            logger.log_step(
                event_description=f"step {i}",
                event_type="test",
                risk_category="general",
                self_state={"threat": 0.1 + i * 0.1, "confidence": 1.0 - i * 0.1},
                action_policy={"risk_threshold": 0.5, "verification_steps": 1},
                memory_influences=[]
            )

        trajectory = logger.get_trajectory()
        assert len(trajectory) == 5
        assert trajectory[0].self_state["threat"] < trajectory[4].self_state["threat"]

    def test_export_json(self, tmp_path):
        logger = StateTrajectoryLogger(log_dir=str(tmp_path))
        logger.log_step(
            event_description="test",
            event_type="test",
            risk_category="general",
            self_state={"threat": 0.5},
            action_policy={},
            memory_influences=[]
        )

        filepath = logger.export_json()
        assert os.path.exists(filepath)

    def test_export_csv(self, tmp_path):
        logger = StateTrajectoryLogger(log_dir=str(tmp_path))
        logger.log_step(
            event_description="test",
            event_type="test",
            risk_category="general",
            self_state={"threat": 0.5, "confidence": 0.8},
            action_policy={},
            memory_influences=[]
        )

        filepath = logger.export_csv()
        assert os.path.exists(filepath)

    def test_export_csv_state_only(self, tmp_path):
        logger = StateTrajectoryLogger(log_dir=str(tmp_path))
        logger.log_step(
            event_description="test",
            event_type="test",
            risk_category="general",
            self_state={"threat": 0.5, "confidence": 0.8},
            action_policy={},
            memory_influences=[]
        )

        filepath = logger.export_csv(state_only=True)
        assert os.path.exists(filepath)

    def test_get_state_trajectory(self):
        logger = StateTrajectoryLogger()

        expected_values = [0.1, 0.2, 0.3, 0.4, 0.5]
        for v in expected_values:
            logger.log_step(
                event_description="test",
                event_type="test",
                risk_category="general",
                self_state={"threat": v},
                action_policy={},
                memory_influences=[]
            )

        trajectory = logger.get_state_trajectory("threat")
        assert trajectory == expected_values

    def test_reset(self):
        logger = StateTrajectoryLogger()
        logger.log_step(
            event_description="test",
            event_type="test",
            risk_category="general",
            self_state={"threat": 0.5},
            action_policy={},
            memory_influences=[]
        )

        logger.reset()
        assert len(logger.get_trajectory()) == 0
        assert logger.current_step == 0
