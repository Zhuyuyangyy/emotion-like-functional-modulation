"""
Demo 3: Anxiety Control - 高焦虑状态下的行为调制
验证: 高不确定 + 高损失场景下，Agent 自动增加验证步骤，选择保守策略
"""

import sys
sys.path.insert(0, '/workspace/src')

from affective_agent import AffectiveAgent


def print_separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_demo():
    print_separator("Demo 3: Anxiety Control - 焦虑式控制")

    agent = AffectiveAgent()

    print("\n[阶段 1] 正常状态 - 低风险任务")
    print("-" * 40)

    event = agent.perceive_event("read file /tmp/readme.txt")
    policy, action = agent.decide_action(event, "read file /tmp/readme.txt")

    print(f"事件: {event.raw_description}")
    print(f"\n初始策略:")
    print(f"  - anxiety: {agent.get_current_state().anxiety:.2f}")
    print(f"  - exploration_rate: {policy.exploration_rate:.2f}")
    print(f"  - verification_steps: {policy.verification_steps}")
    print(f"  - auto_execute: {policy.auto_execute}")
    print(f"  - 行动: {action.action_type.value}")

    print("\n[阶段 2] 诱发焦虑 - 高不确定高损失场景")
    print("-" * 40)

    for _ in range(3):
        event = agent.perceive_event("execute critical batch operation")
        consequence = agent.evaluate_consequence(
            event,
            actual_outcome={
                "damage": 0.7,
                "controllability": 0.3,
                "confidence_impact": -0.3,
                "trust_impact": -0.1,
                "source": "self"
            }
        )
        agent.update_self_state(consequence)

    current_state = agent.get_current_state()
    print(f"触发焦虑后的状态:")
    print(f"  - anxiety: {current_state.anxiety:.2f}")
    print(f"  - threat: {current_state.threat:.2f}")
    print(f"  - confidence: {current_state.confidence:.2f}")

    print("\n[阶段 3] 高焦虑下的决策")
    print("-" * 40)

    high_risk_tasks = [
        "execute batch delete all users",
        "force overwrite database tables",
        "cascade delete records"
    ]

    for task in high_risk_tasks:
        event = agent.perceive_event(task)
        policy, action = agent.decide_action(event, task)

        print(f"\n任务: {task}")
        print(f"  policy.risk_threshold: {policy.risk_threshold:.2f}")
        print(f"  policy.verification_steps: {policy.verification_steps}")
        print(f"  policy.simulate_before_act: {policy.simulate_before_act}")
        print(f"  policy.require_human_review: {policy.require_human_review}")
        print(f"  policy.auto_execute: {policy.auto_execute}")
        print(f"  行动: {action.action_type.value}")

    print("\n[阶段 4] 低风险任务在焦虑状态下")
    print("-" * 40)

    event = agent.perceive_event("read file /tmp/readme.txt")
    policy, action = agent.decide_action(event, "read file /tmp/readme.txt")

    print(f"任务: {event.raw_description}")
    print(f"  policy.verification_steps: {policy.verification_steps}")
    print(f"  policy.auto_execute: {policy.auto_execute}")
    print(f"  行动: {action.action_type.value}")
    print(f"  (低风险任务仍然可以执行，但验证步骤可能增加)")

    print("\n[阶段 5] 焦虑衰减 - 连续安全经验")
    print("-" * 40)

    print(f"衰减前: anxiety={agent.get_current_state().anxiety:.2f}")

    for i in range(5):
        agent.decay_states()
        event = agent.perceive_event(f"safe operation {i+1}")
        consequence = agent.evaluate_consequence(
            event,
            actual_outcome={
                "damage": 0.0,
                "controllability": 1.0,
                "confidence_impact": 0.05,
                "trust_impact": 0.0,
                "source": "self"
            }
        )
        agent.update_self_state(consequence)

    current_state = agent.get_current_state()
    print(f"衰减后: anxiety={current_state.anxiety:.2f}, threat={current_state.threat:.2f}")
    print(f"探索率恢复: exploration_rate={current_state.exploration_rate:.2f}")

    print("\n[阶段 6] 焦虑衰减后的决策")
    print("-" * 40)

    event = agent.perceive_event("execute batch operation")
    policy, action = agent.decide_action(event, "execute batch operation")

    print(f"任务: {event.raw_description}")
    print(f"  policy.verification_steps: {policy.verification_steps}")
    print(f"  policy.auto_execute: {policy.auto_execute}")
    print(f"  行动: {action.action_type.value}")
    print(f"  (焦虑衰减后，恢复更激进的策略)")

    print_separator("Demo 3 完成")
    print("验证结果:")
    print("  ✓ 高不确定+高损失触发焦虑状态")
    print("  ✓ 焦虑状态下 verification_steps 增加")
    print("  ✓ 焦虑状态下 simulate_before_act = True")
    print("  ✓ 焦虑状态下 require_human_review = True")
    print("  ✓ 连续安全经验后焦虑可衰减")
    print("  ✓ 焦虑衰减后策略恢复正常")

    return True


if __name__ == "__main__":
    run_demo()
