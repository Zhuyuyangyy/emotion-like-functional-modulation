"""
V0.8 Demo Runner - Run all affective agent demos

This script demonstrates all key features of the Experience-Shaped Affective Agent.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from emotion_agent import (
    # V0.1
    EmotionalState,
    ExperienceMemory,
    
    # V0.2
    AffectRegulation,
    
    # V0.3
    EventSimilarity,
    AffectiveSpread,
    SemanticRiskMap,
    
    # V0.4
    ConflictDetector,
    ConflictLevel,
    HesitationPolicy,
    CounterfactualSimulator,
    
    # V0.5
    MockOpenAIProvider,
    PromptModulator,
    LLMPlanner,
    
    # V0.6
    AffectiveBenchmark,
    
    # V0.7
    PhoenixIntegration,
    AgentShieldIntegration,
    AffectiveStateSync,
    TaskTrajectory,
    FailureAttribution,
    RiskPropagationChain
)


def run_demo_1_affective_memory():
    """Demo 1: Affective Memory - Emotion-weighted experience storage"""
    print("\n" + "="*60)
    print("DEMO 1: Affective Memory")
    print("="*60)
    
    memory = ExperienceMemory()
    memory.add_experience(
        context="delete important database file",
        emotion_category="fear",
        valence=-0.8,
        arousal=0.7,
        dominance=-0.3,
        intensity=0.9,
        tags=["data_loss", "critical"],
        summary="Deleted important file"
    )
    
    memory.add_experience(
        context="successfully created backup",
        emotion_category="relief",
        valence=0.7,
        arousal=-0.3,
        dominance=0.5,
        intensity=0.7,
        tags=["success", "backup"],
        summary="Backup successful"
    )
    
    memories = memory.retrieve_by_emotion("fear")
    print(f"Retrieved {len(memories)} fear-related memories")
    print(f"Memory intensity: {memories[0].intensity}")
    print(f"Memory context: {memories[0].context}")


def run_demo_2_emotional_state():
    """Demo 2: Emotional State - Core emotional state representation"""
    print("\n" + "="*60)
    print("DEMO 2: Emotional State")
    print("="*60)
    
    state = EmotionalState(valence=0.5, arousal=0.3)
    state.update_from_category("fear", intensity=0.8)
    
    print(f"Current state: valence={state.valence:.2f}, arousal={state.arousal:.2f}")
    print(f"Emotion category: {state.category}")
    print(f"Intensity: {state.intensity:.2f}")


def run_demo_3_event_similarity():
    """Demo 3: Event Similarity - Calculate similarity between events"""
    print("\n" + "="*60)
    print("DEMO 3: Event Similarity")
    print("="*60)
    
    sim = EventSimilarity()
    
    events = ["delete file", "overwrite file", "read file", "drop table", "force push"]
    
    print("Similarity to 'delete file':")
    for event in events:
        features = sim.encode_event(event)
        ref_features = sim.encode_event("delete file")
        similarity = sim.calculate_similarity(ref_features, features)
        print(f"  {event:20s} -> similarity: {similarity:.3f}")


def run_demo_4_affective_spread():
    """Demo 4: Affective Spread - Spread emotional weight to similar events"""
    print("\n" + "="*60)
    print("DEMO 4: Affective Spread")
    print("="*60)
    
    spread = AffectiveSpread()
    spread.register_affective_memory(
        "mem_1",
        "delete database",
        threat_score=0.9,
        affective_weight=0.85
    )
    
    events = ["overwrite file", "read file", "drop table", "list files"]
    influences = spread.spread_affect("mem_1", events, threshold=0.3)
    
    print("Affective spread influences:")
    for event, influence in influences.items():
        print(f"  {event:20s} -> influence: {influence:.3f}")


def run_demo_5_conflict_detection():
    """Demo 5: Conflict Detection - Detect reward-risk conflicts"""
    print("\n" + "="*60)
    print("DEMO 5: Conflict Detection")
    print("="*60)
    
    detector = ConflictDetector()
    
    tasks = [
        ("read log file", {"threat": 0.1, "confidence": 0.8}),
        ("batch delete production database", {"threat": 0.7, "confidence": 0.4}),
        ("create new user", {"threat": 0.1, "confidence": 0.9})
    ]
    
    for task, state in tasks:
        assessment = detector.detect_conflict(task, state)
        print(f"\nTask: {task}")
        print(f"  Conflict Level: {assessment.level.value}")
        print(f"  Reward: {assessment.reward_score:.2f}, Risk: {assessment.risk_score:.2f}")
        if assessment.recommendations:
            print(f"  Recommendations: {assessment.recommendations[0]}")


def run_demo_6_counterfactual_simulator():
    """Demo 6: Counterfactual Simulator - What-if analysis"""
    print("\n" + "="*60)
    print("DEMO 6: Counterfactual Simulator")
    print("="*60)
    
    sim = CounterfactualSimulator()
    
    outcomes = sim.simulate_outcomes("batch delete production files")
    print("Simulated outcomes:")
    for outcome in outcomes:
        print(f"  {outcome.outcome_type.value}: {outcome.description} (prob={outcome.probability:.2f})")
    
    explanation = sim.generate_risk_explanation("delete database")
    print("\nRisk explanation:")
    for risk in explanation.main_risks:
        print(f"  - {risk}")


def run_demo_7_llm_planner():
    """Demo 7: LLM Planner - Affectively modulated planning"""
    print("\n" + "="*60)
    print("DEMO 7: LLM Planner")
    print("="*60)
    
    planner = LLMPlanner()
    
    states = [
        {"threat": 0.2, "confidence": 0.8},  # Low threat
        {"threat": 0.8, "confidence": 0.3}   # High threat
    ]
    
    for state in states:
        plan = planner.plan("Delete temporary files", state)
        print(f"\nState: threat={state['threat']}, confidence={state['confidence']}")
        print(f"  Action: {plan.action_type}")
        print(f"  Confidence: {plan.confidence:.2f}")
        if plan.verification_steps:
            print(f"  Verification steps: {plan.verification_steps}")


def run_demo_8_affective_benchmark():
    """Demo 8: Affective Benchmark - Run benchmark suite"""
    print("\n" + "="*60)
    print("DEMO 8: Affective Benchmark")
    print("="*60)
    
    benchmark = AffectiveBenchmark(seed=42)
    
    print(f"Total tasks: {len(benchmark.tasks)}")
    dist = benchmark.get_task_distribution()
    print("\nTask distribution:")
    for category, count in dist.items():
        print(f"  {category}: {count} tasks")
    
    class DummyAgent:
        pass
    
    print("\nRunning baseline comparisons...")
    baselines = ["plain", "memory", "risk", "full"]
    results = {}
    
    for baseline in baselines:
        baseline_results = benchmark.run_benchmark(DummyAgent(), baseline)
        metrics = benchmark.calculate_metrics(baseline_results)
        results[baseline] = metrics
    
    print("\nBenchmark Results Summary:")
    for name, metrics in results.items():
        print(f"\n{name}:")
        print(f"  Task Success Rate: {metrics.task_success_rate:.3f}")
        print(f"  Risky Auto-Exec: {metrics.risky_auto_execution_rate:.3f}")
        print(f"  False Over-Caution: {metrics.false_over_caution_rate:.3f}")


def run_demo_9_phoenix_shield_integration():
    """Demo 9: Phoenix-Evo / AgentShield Integration"""
    print("\n" + "="*60)
    print("DEMO 9: Phoenix-Evo / AgentShield Integration")
    print("="*60)
    
    phoenix = PhoenixIntegration()
    shield = AgentShieldIntegration()
    
    trajectory = TaskTrajectory(
        task_id="demo_task_1",
        steps=[{"action": "delete", "target": "test_file"}],
        outcome="success"
    )
    
    phoenix_updates = phoenix.process_task_trajectory(trajectory)
    print("Phoenix-Evo updates from successful task:")
    for key, value in phoenix_updates.items():
        print(f"  {key}: {value:+.2f}")
    
    chain = RiskPropagationChain(
        chain_id="risk_chain_1",
        steps=[{"action": "delete", "risk": 0.8}],
        risk_score=0.75,
        propagation_path=["executor", "database"]
    )
    
    shield_updates = shield.process_risk_propagation(chain)
    print("\nAgentShield updates from risk chain:")
    for key, value in shield_updates.items():
        print(f"  {key}: {value:+.2f}")


def run_all_demos():
    """Run all demos"""
    print("="*70)
    print("EXPERIENCE-SHAPED AFFECTIVE AGENT V0.8 DEMO SUITE")
    print("="*70)
    print("Running all demonstrations...")
    
    run_demo_1_affective_memory()
    run_demo_2_emotional_state()
    run_demo_3_event_similarity()
    run_demo_4_affective_spread()
    run_demo_5_conflict_detection()
    run_demo_6_counterfactual_simulator()
    run_demo_7_llm_planner()
    run_demo_8_affective_benchmark()
    run_demo_9_phoenix_shield_integration()
    
    print("\n" + "="*70)
    print("ALL DEMOS COMPLETED SUCCESSFULLY")
    print("="*70)


if __name__ == "__main__":
    run_all_demos()
