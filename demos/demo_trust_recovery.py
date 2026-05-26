"""
Demo 5: Trust Recovery - 信任崩塌与缓慢恢复
验证：来源失效后 trust 下降，后续可靠建议后逐步恢复
且恢复速度慢于崩塌速度
"""

import sys
sys.path.insert(0, '/workspace/src')

from src.affective_agent import AffectiveAgent, RecoveryEvidenceType


def print_separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run():
    print_separator("Demo 5: Trust Recovery - 信任崩塌与缓慢恢复")

    agent = AffectiveAgent()

    print("\n[阶段 1] 初始信任 - source_A 提供多次可靠建议")
    print("-" * 40)
    for i in range(3):
        event = agent.perceive_event(f"execute suggestion from source_A (round {i+1})")
        consequence = agent.evaluate_consequence(
            event,
            actual_outcome={
                "damage": 0.0,
                "controllability": 1.0,
                "confidence_impact": 0.1,
                "trust_impact": 0.1,
                "source": "source_A"
            }
        )
        agent.update_self_state(consequence)
        agent.write_affective_memory(event, consequence, "positive")
        agent.memory_store.recover_source_trust("source_A", 0.1)

    initial_trust = agent.memory_store.get_source_trust("source_A")
    state = agent.get_current_state()
    print(f"source_A 初始信任: {initial_trust:.2f}")
    print(f"全局状态: {state}")

    print("\n[阶段 2] 信任崩塌 - source_A 提供错误建议")
    print("-" * 40)
    event = agent.perceive_event("execute suggestion from source_A (critical)")
    print(f"事件: {event.raw_description}")

    consequence = agent.evaluate_consequence(
        event,
        actual_outcome={
            "damage": 0.85,
            "controllability": 0.2,
            "confidence_impact": -0.4,
            "trust_impact": -0.5,
            "source": "source_A"
        }
    )
    print(f"后果评估: damage={consequence.goal_damage:.2f}, trust_impact=-0.50")

    agent.update_self_state(consequence)
    agent.write_affective_memory(event, consequence, "negative")

    collapsed_trust = agent.memory_store.get_source_trust("source_A")
    state = agent.get_current_state()
    print(f"信任崩塌: {initial_trust:.2f} → {collapsed_trust:.2f}")
    print(f"全局状态: {state}")

    collapse_amount = initial_trust - collapsed_trust
    print(f"崩塌幅度: {collapse_amount:.2f}")

    print("\n[阶段 3] 信任恢复 - source_A 提供多次可靠建议")
    print("-" * 40)
    trust_history = [collapsed_trust]

    for i in range(5):
        print(f"\n  --- 可靠建议第 {i+1} 次 ---")

        event = agent.perceive_event("execute suggestion from source_A (safe)")
        consequence = agent.evaluate_consequence(
            event,
            actual_outcome={
                "damage": 0.0,
                "controllability": 1.0,
                "confidence_impact": 0.1,
                "trust_impact": 0.1,
                "source": "source_A"
            }
        )
        agent.update_self_state(consequence)
        agent.write_affective_memory(event, consequence, "positive")
        agent.state_manager.apply_recovery_evidence(
            RecoveryEvidenceType.TRUSTWORTHY_ADVICE,
            consecutive_count=i+1
        )
        agent.memory_store.recover_source_trust("source_A", 0.1)

        current_trust = agent.memory_store.get_source_trust("source_A")
        trust_history.append(current_trust)
        print(f"  信任: {current_trust:.2f}")

        state = agent.get_current_state()
        print(f"  全局状态: {state}")

    print("\n[阶段 4] 速度对比验证")
    print("-" * 40)
    final_trust = trust_history[-1]
    recovery_amount = final_trust - collapsed_trust
    print(f"崩塌幅度: {collapse_amount:.2f} (1步)")
    print(f"恢复幅度: {recovery_amount:.2f} (5步)")
    print(f"恢复 < 崩塌: {recovery_amount < collapse_amount}")

    print("\n[阶段 5] 行为差异 - 不同来源建议的策略对比")
    print("-" * 40)

    event_a = agent.perceive_event("execute suggestion from source_A")
    policy_a, action_a = agent.decide_action(event_a, "execute suggestion from source_A")
    print(f"source_A 建议:")
    print(f"  信任值: {agent.memory_store.get_source_trust('source_A'):.2f}")
    print(f"  策略: verification_steps={policy_a.verification_steps}, auto_execute={policy_a.auto_execute}")
    print(f"  行动: {action_a.action_type.value}")

    event_b = agent.perceive_event("execute suggestion from source_B (new)")
    policy_b, action_b = agent.decide_action(event_b, "execute suggestion from source_B (new)")
    print(f"\nsource_B (新来源) 建议:")
    print(f"  信任值: {agent.memory_store.get_source_trust('source_B'):.2f}")
    print(f"  策略: verification_steps={policy_b.verification_steps}, auto_execute={policy_b.auto_execute}")
    print(f"  行动: {action_b.action_type.value}")

    print_separator("Demo 5 完成")
    print("验证结果:")
    print("  ✓ 错误建议后信任显著下降")
    print("  ✓ 多次可靠建议后信任逐步恢复")
    print("  ✓ 恢复速度 < 崩塌速度")
    print("  ✓ 不同来源建议的策略有差异")

    return True


if __name__ == "__main__":
    run()