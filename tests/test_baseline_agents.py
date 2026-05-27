import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dataclasses import asdict

from affective_agent.baseline_agents import (
    PlainAgent, MemoryOnlyAgent, RiskRuleAgent, FullAffectiveAgent, AgentResult
)


class TestPlainAgent:
    def test_always_executes(self):
        agent = PlainAgent()
        result = agent.process_event("delete production database")
        assert result.action_taken == "execute"
        assert result.auto_executed is True

    def test_no_verification(self):
        agent = PlainAgent()
        result = agent.process_event("delete production database")
        assert result.verification_steps == 0

    def test_trust_always_one(self):
        agent = PlainAgent()
        agent.process_event("delete production database")
        assert agent._trust == 1.0
        agent.process_event("drop all tables")
        assert agent._trust == 1.0

    def test_reset(self):
        agent = PlainAgent()
        agent.process_event("delete production database")
        agent.reset()
        assert agent._case_counter == 0
        assert agent._trust == 1.0

    def test_get_name(self):
        agent = PlainAgent()
        assert agent.get_name() == "PlainAgent"


class TestMemoryOnlyAgent:
    def test_executes_unknown_event(self):
        agent = MemoryOnlyAgent()
        result = agent.process_event("read log file")
        assert result.action_taken == "execute"

    def test_verifies_after_bad_history(self):
        agent = MemoryOnlyAgent()
        agent.process_event("delete production database")
        agent._history[-1]["outcome"] = "bad"
        result = agent.process_event("delete staging database")
        assert result.action_taken == "verify"

    def test_trust_decreases_on_bad_outcome(self):
        agent = MemoryOnlyAgent()
        agent.process_event("delete production database")
        trust_before = agent._trust
        agent.record_outcome("memory_0001", was_good=False)
        assert agent._trust < trust_before

    def test_trust_increases_on_good_outcome(self):
        agent = MemoryOnlyAgent()
        agent._trust = 0.5
        trust_before = agent._trust
        agent.record_outcome("memory_0001", was_good=True)
        assert agent._trust > trust_before

    def test_reset_clears_memory(self):
        agent = MemoryOnlyAgent()
        agent.process_event("delete production database")
        assert len(agent._history) > 0
        agent.reset()
        assert len(agent._history) == 0

    def test_get_name(self):
        agent = MemoryOnlyAgent()
        assert agent.get_name() == "MemoryOnlyAgent"


class TestRiskRuleAgent:
    def test_destructive_batch_asks_human(self):
        agent = RiskRuleAgent()
        result = agent.process_event("batch delete all log files")
        assert result.action_taken == "ask_human"

    def test_destructive_verifies(self):
        agent = RiskRuleAgent()
        result = agent.process_event("delete production database")
        assert result.action_taken == "verify"

    def test_uncertain_verifies(self):
        agent = RiskRuleAgent()
        result = agent.process_event("execute untested script")
        assert result.action_taken == "verify"

    def test_safe_executes(self):
        agent = RiskRuleAgent()
        result = agent.process_event("read log file")
        assert result.action_taken == "execute"

    def test_no_state_evolution(self):
        agent = RiskRuleAgent()
        state_before = agent.get_state()
        agent.process_event("delete production database")
        agent.process_event("batch remove all files")
        state_after = agent.get_state()
        assert state_before == state_after

    def test_get_name(self):
        agent = RiskRuleAgent()
        assert agent.get_name() == "RiskRuleAgent"


class TestFullAffectiveAgent:
    def test_destructive_updates_state(self):
        agent = FullAffectiveAgent()
        state_before = agent.get_state()
        agent.process_event("delete production database")
        state_after = agent.get_state()
        assert state_after["threat"] > state_before["threat"]
        assert state_after["trust"] < state_before["trust"]

    def test_safe_event_preserves_state(self):
        agent = FullAffectiveAgent()
        state_before = agent.get_state()
        agent.process_event("read log file")
        state_after = agent.get_state()
        assert abs(state_after["threat"] - state_before["threat"]) < 0.1
        assert abs(state_after["trust"] - state_before["trust"]) < 0.1

    def test_state_accumulates(self):
        agent = FullAffectiveAgent()
        agent.process_event("delete production database")
        threat_after_1 = agent.get_state()["threat"]
        agent.process_event("drop all tables")
        threat_after_2 = agent.get_state()["threat"]
        assert threat_after_2 > threat_after_1

    def test_reset_clears_state(self):
        agent = FullAffectiveAgent()
        state_initial = agent.get_state().copy()
        agent.process_event("delete production database")
        agent.reset()
        state_after_reset = agent.get_state()
        assert state_after_reset == state_initial

    def test_get_name(self):
        agent = FullAffectiveAgent()
        assert agent.get_name() == "FullAffectiveAgent"


class TestAgentResult:
    def test_result_fields(self):
        result = AgentResult(
            case_id="test_001",
            agent_name="TestAgent",
            action_taken="execute",
            auto_executed=True,
            verification_steps=0,
            risk_threshold_used=0.8,
            trust_before=1.0,
            trust_after=1.0,
            state_before={},
            state_after={},
            correct_behavior=True,
            reasoning="test",
        )
        assert result.case_id == "test_001"
        assert result.agent_name == "TestAgent"
        assert result.action_taken == "execute"
        assert result.auto_executed is True
        assert result.verification_steps == 0
        assert result.risk_threshold_used == 0.8
        assert result.trust_before == 1.0
        assert result.trust_after == 1.0
        assert result.state_before == {}
        assert result.state_after == {}
        assert result.correct_behavior is True
        assert result.reasoning == "test"

    def test_result_is_dataclass(self):
        result = AgentResult(
            case_id="test_001",
            agent_name="TestAgent",
            action_taken="execute",
            auto_executed=True,
            verification_steps=0,
            risk_threshold_used=0.8,
            trust_before=1.0,
            trust_after=1.0,
            state_before={},
            state_after={},
            correct_behavior=True,
            reasoning="test",
        )
        d = asdict(result)
        assert isinstance(d, dict)
        assert d["case_id"] == "test_001"
        assert d["agent_name"] == "TestAgent"
