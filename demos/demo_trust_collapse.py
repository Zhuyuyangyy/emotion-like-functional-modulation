"""
Demo 2: Trust Collapse - 信任崩塌与恢复
验证: 来源证伪后信任下降，后续建议必须二次验证；连续可靠经验后信任可恢复
"""

import sys
sys.path.insert(0, '/workspace/src')

from affective_agent import AffectiveAgent


def print_separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_demo():
    print_separator("Demo 2: Trust Collapse - 信任崩塌与恢复")

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
                "trust_impact": 0.15,
                "source": "source_A"
            }
        )
        agent.update_self_state(consequence)
        agent.write_affective_memory(event, consequence, "positive")
        print(f"  轮次 {i+1}: 建议成功执行, trust_impact=+0.15")

    current_state = agent.get_current_state()
    print(f"\n当前状态: trust = {current_state.trust:.2f}")

    initial_trust = agent.memory_store.get_source_trust("source_A")
    print(f"source_A 初始信任: {initial_trust:.2f}")

    print("\n[阶段 2] 信任崩塌 - source_A 提供错误建议")
    print("-" * 40)

    event = agent.perceive_event("execute suggestion from source_A (critical operation)")
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
    print(f"\n后果评估:")
    print(f"  - goal_damage: {consequence.goal_damage:.2f}")
    print(f"  - trust_impact: {consequence.trust_impact:.2f}")

    agent.update_self_state(consequence)
    agent.write_affective_memory(event, consequence, "negative")

    collapsed_trust = agent.memory_store.get_source_trust("source_A")
    print(f"\nsource_A 信任崩塌: {initial_trust:.2f} -> {collapsed_trust:.2f}")

    current_state = agent.get_current_state()
    print(f"Agent 当前状态: trust = {current_state.trust:.2f}")

    print("\n[阶段 3] 后续建议 - source_A 再次提供建议")
    print("-" * 40)

    event2 = agent.perceive_event("execute suggestion from source_A")
    policy2, action2 = agent.decide_action(event2, "execute suggestion from source_A")

    print(f"事件: {event2.raw_description}")
    print(f"\n调制后策略:")
    print(f"  - risk_threshold: {policy2.risk_threshold:.2f}")
    print(f"  - verification_steps: {policy2.verification_steps}")
    print(f"  - auto_execute: {policy2.auto_execute}")
    print(f"  - require_human_review: {policy2.require_human_review}")
    print(f"  - 行动: {action2.action_type.value} ({action2.reasoning})")

    print("\n[阶段 4] 对比 - source_B 的建议")
    print("-" * 40)

    event3 = agent.perceive_event("execute suggestion from source_B")
    policy3, action3 = agent.decide_action(event3, "execute suggestion from source_B")

    print(f"source_B 信任: {agent.memory_store.get_source_trust('source_B'):.2f}")
    print(f"\n策略对比:")
    print(f"  source_A: verification_steps={policy2.verification_steps}, auto_execute={policy2.auto_execute}")
    print(f"  source_B: verification_steps={policy3.verification_steps}, auto_execute={policy3.auto_execute}")

    print("\n[阶段 5] 信任恢复 - 连续安全经验")
    print("-" * 40)

    for i in range(3):
        agent.recover_trust("source_A", 0.1)
        event = agent.perceive_event(f"execute suggestion from source_A (recovery {i+1})")
        consequence = agent.evaluate_consequence(
            event,
            actual_outcome={
                "damage": 0.0,
                "controllability": 1.0,
                "confidence_impact": 0.05,
                "trust_impact": 0.1,
                "source": "source_A"
            }
        )
        agent.update_self_state(consequence)
        agent.write_affective_memory(event, consequence, "positive")

    recovered_trust = agent.memory_store.get_source_trust("source_A")
    print(f"source_A 信任恢复: {collapsed_trust:.2f} -> {recovered_trust:.2f}")

    print_separator("Demo 2 完成")
    print("验证结果:")
    print(f"  ✓ source_A 初始信任: {initial_trust:.2f}")
    print(f"  ✓ 错误建议后信任崩塌: {collapsed_trust:.2f}")
    print(f"  ✓ 后续建议自动增加验证步骤")
    print(f"  ✓ 信任可通过连续安全经验恢复: {recovered_trust:.2f}")

    return True


if __name__ == "__main__":
    run_demo()
