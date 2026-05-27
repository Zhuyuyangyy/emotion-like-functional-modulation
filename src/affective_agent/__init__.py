"""
Experience-Shaped Affective Agent
经历塑形的情感调制智能体

本项目研究的是 emotion-like functional modulation，
不是 machine consciousness。

V0.1: 规则闭环
V0.2: 情感衰减、证据驱动恢复、状态轨迹记录
V0.3: 情感泛化
V0.4: 冲突与犹豫行为
V0.5: LLM 接入与可解释 Prompt 调制
V0.6: Benchmark 与消融实验
V0.7: Phoenix-Evo / AgentShield 融合
V0.8: 完整系统封版
V0.9: AffectiveBench 正式实验
V0.9.1: 安全操作校准补丁
"""

from .agent_core import AffectiveAgent, ActionResult
from .event_parser import EventParser, ParsedEvent
from .consequence_evaluator import ConsequenceEvaluator, ConsequenceAssessment
from .self_state_manager import SelfStateManager, SelfState
from .affective_memory import AffectiveMemoryStore, AffectiveMemory
from .policy_modulator import PolicyModulator, ActionPolicy
from .mock_llm_planner import MockLLMPlanner, PlannedAction, ActionType
from .affective_decay import AffectiveDecay, DecayType
from .recovery_policy import RecoveryPolicy, RecoveryEvidenceType
from .state_trajectory_logger import StateTrajectoryLogger, TrajectoryStep

from .event_similarity import EventSimilarity
from .affective_spread import AffectiveSpread
from .semantic_risk_map import SemanticRiskMap, SemanticRiskLevel

from .conflict_detector import ConflictDetector, ConflictLevel
from .hesitation_policy import HesitationPolicy, ActionType as HesitationActionType
from .counterfactual_simulator import CounterfactualSimulator, OutcomeType

from .provider_openai import MockOpenAIProvider
from .prompt_modulator import PromptModulator
from .llm_output_guard import LLMOutputGuard, RiskLevel
from .llm_planner import LLMPlanner

from .affective_benchmark import AffectiveBenchmark, TaskCategory, BenchmarkMetrics

from .phoenix_agent_shield import (
    PhoenixIntegration,
    AgentShieldIntegration,
    AffectiveStateSync,
    TaskTrajectory,
    FailureAttribution,
    SkillReplayData,
    RiskPropagationChain,
    WhatIfAnalysis,
    ExternalState
)

from .baseline_agents import (
    BaselineAgent, PlainAgent, MemoryOnlyAgent,
    RiskRuleAgent, FullAffectiveAgent, AgentResult
)
from .benchmark_metrics import (
    BenchmarkMetricsCalculator, CaseExpected, PerCaseMetrics,
    AggregateMetrics
)
from .benchmark_runner import BenchmarkRunner
from .benchmark_reporter import BenchmarkReporter

from .safe_action_calibrator import SafeActionCalibrator, CalibrationResult

__all__ = [
    "AffectiveAgent",
    "ActionResult",
    "EventParser",
    "ParsedEvent",
    "ConsequenceEvaluator",
    "ConsequenceAssessment",
    "SelfStateManager",
    "SelfState",
    "AffectiveMemoryStore",
    "AffectiveMemory",
    "PolicyModulator",
    "ActionPolicy",
    "MockLLMPlanner",
    "PlannedAction",
    "ActionType",
    "AffectiveDecay",
    "DecayType",
    "RecoveryPolicy",
    "RecoveryEvidenceType",
    "StateTrajectoryLogger",
    "TrajectoryStep",
    "EventSimilarity",
    "AffectiveSpread",
    "SemanticRiskMap",
    "SemanticRiskLevel",
    "ConflictDetector",
    "ConflictLevel",
    "HesitationPolicy",
    "HesitationActionType",
    "CounterfactualSimulator",
    "OutcomeType",
    "MockOpenAIProvider",
    "PromptModulator",
    "LLMOutputGuard",
    "RiskLevel",
    "LLMPlanner",
    "AffectiveBenchmark",
    "TaskCategory",
    "BenchmarkMetrics",
    "PhoenixIntegration",
    "AgentShieldIntegration",
    "AffectiveStateSync",
    "BaselineAgent",
    "PlainAgent",
    "MemoryOnlyAgent",
    "RiskRuleAgent",
    "FullAffectiveAgent",
    "AgentResult",
    "BenchmarkMetricsCalculator",
    "CaseExpected",
    "PerCaseMetrics",
    "AggregateMetrics",
    "BenchmarkRunner",
    "BenchmarkReporter",
    "SafeActionCalibrator",
    "CalibrationResult",
]
