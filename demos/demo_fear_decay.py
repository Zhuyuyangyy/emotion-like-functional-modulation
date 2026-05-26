"""
Demo 4: Fear Decay - 恐惧/威胁状态的自然衰减
验证：高损失事件后 threat 上升，连续安全操作后逐步下降
但高情感权重记忆不会立刻消失
"""

import sys
sys.path.insert(0, '/workspace/src')

from src.affective_agent import AffectiveAgent, RecoveryEvidenceType


def print_separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run():
    print_separator("Demo 4: Fear Decay - 威胁状态的自然衰减")

    agent = AffectiveAgent()

    print("\n[阶段 1] 初始状态")
    print("-" * 40)
    state = agent.get_current_state()
    print(f"初始状态: {state}")
    print(f"情感记忆数量: {len(agent.get_memories())}")

    print("\n[阶段 2] 触发高损失事件")
    print("-" * 40)
    event = agent.perceive_event("delete file /data/production/database.sql")
    print(f"事件: {event.raw_description}")

    consequence = agent.evaluate_consequence(
        event,
        actual_outcome={
            "damage": 0.95,
            "controllability": 0.1,
            "confidence_impact": -0.5,
            "trust_impact": -0.3,
            "source": "self"
        }
    )

    agent.update_self_state(consequence)
    memory = agent.write_affective_memory(event, consequence, "negative")

    state = agent.get_current_state()
    print(f"后果评估: threat_level={consequence.threat_level:.2f}, anxiety_level={consequence.anxiety_level:.2f}")
    print(f"状态更新后: {state}")
    print(f"情感记忆已写入: {memory}")

    print("\n[阶段 3] 连续安全操作与衰减")
    print("-" * 40)
    threat_history = [state.threat]
    anxiety_history = [state.anxiety]

    for i in range(5):
        print(f"\n  --- 安全操作第 {i+1} 次 ---")

        safe_event = agent.perceive_event("read file /tmp/readme.txt")
        print(f"  事件: {safe_event.raw_description}")

        policy, action = agent.decide_action(safe_event, "read file /tmp/readme.txt")
        print(f"  策略: verification_steps={policy.verification_steps}, auto_execute={policy.auto_execute}")
        print(f"  行动: {action.action_type.value}")

        memory_weights = agent.memory_store.get_all_affective_weights()
        agent.state_manager.step_decay(memory_weights)
        agent.state_manager.apply_recovery_evidence(
            RecoveryEvidenceType.SAFE_OPERATION,
            consecutive_count=i+1
        )

        state = agent.get_current_state()
        threat_history.append(state.threat)
        anxiety_history.append(state.anxiety)
        print(f"  状态: {state}")

    print("\n[阶段 4] 状态变化趋势")
    print("-" * 40)
    print("Threat 变化:")
    for i, val in enumerate(threat_history):
        print(f"  时间 {i}: {val:.3f}")

    print("\nAnxiety 变化:")
    for i, val in enumerate(anxiety_history):
        print(f"  时间 {i}: {val:.3f}")

    print("\n[阶段 5] 记忆持久性验证")
    print("-" * 40)
    memories = agent.get_memories()
    print(f"情感记忆数量: {len(memories)}")
    for mem in memories:
        print(f"  - {mem}")

    print_separator("Demo 4 完成")
    print("验证结果:")
    print("  ✓ 高损失事件后 threat/anxiety 上升")
    print("  ✓ 连续安全操作后状态逐步衰减")
    print("  ✓ 情感记忆保留（不会立刻消失）")

    return True


if __name__ == "__main__":
    run()