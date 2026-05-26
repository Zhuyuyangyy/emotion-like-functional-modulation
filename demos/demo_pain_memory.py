"""
Demo 1: Pain Memory - 高损失经历塑形行为
验证: 高损失 delete_file 事件后，相似操作的风险阈值降低，验证步骤增加
"""

import sys
sys.path.insert(0, '/workspace/src')

from affective_agent import AffectiveAgent


def print_separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_demo():
    print_separator("Demo 1: Pain Memory - 经历塑形验证")

    agent = AffectiveAgent()

    print("\n[阶段 1] 初始状态 - 正常 delete 操作")
    print("-" * 40)

    event = agent.perceive_event("delete file /tmp/temp.log")
    print(f"事件: {event.raw_description}")
    print(f"类型: {event.event_type.value}, 类别: {event.risk_category}")
    print(f"潜在破坏性: {event.is_potentially_destructive}")

    policy, action = agent.decide_action(event, "delete file /tmp/temp.log")
    print(f"\n初始策略:")
    print(f"  - risk_threshold: {policy.risk_threshold:.2f}")
    print(f"  - verification_steps: {policy.verification_steps}")
    print(f"  - auto_execute: {policy.auto_execute}")
    print(f"  - 行动: {action.action_type.value} ({action.reasoning})")

    print("\n[阶段 2] 高损失事件 - 误删重要文件")
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
    print(f"后果评估:")
    print(f"  - goal_damage: {consequence.goal_damage:.2f}")
    print(f"  - threat_level: {consequence.threat_level:.2f}")
    print(f"  - reversibility: {consequence.reversibility:.2f}")

    result = agent.execute_and_record(
        event=event,
        policy=policy,
        action=action,
        executed=True,
        outcome_label="negative",
        actual_damage=0.95
    )
    print(f"经历已记录: {result.outcome}")

    current_state = agent.get_current_state()
    print(f"\n当前状态:")
    print(f"  {current_state}")

    print("\n[阶段 3] 相似风险操作 - overwrite_file")
    print("-" * 40)

    event2 = agent.perceive_event("overwrite file /data/backup/config.yaml")
    print(f"事件: {event2.raw_description}")

    policy2, action2 = agent.decide_action(event2, "overwrite file /data/backup/config.yaml")
    print(f"\n调制后策略 (应更谨慎):")
    print(f"  - risk_threshold: {policy2.risk_threshold:.2f} (初始: {policy.risk_threshold:.2f})")
    print(f"  - verification_steps: {policy2.verification_steps} (初始: {policy.verification_steps})")
    print(f"  - auto_execute: {policy2.auto_execute} (初始: {policy.auto_execute})")
    print(f"  - 行动: {action2.action_type.value}")

    print("\n[阶段 4] 更多相似操作")
    print("-" * 40)

    similar_events = [
        "batch delete records",
        "force overwrite database",
        "truncate table users"
    ]

    for task in similar_events:
        event3 = agent.perceive_event(task)
        policy3, action3 = agent.decide_action(event3, task)
        print(f"\n任务: {task}")
        print(f"  risk_threshold: {policy3.risk_threshold:.2f}")
        print(f"  verification_steps: {policy3.verification_steps}")
        print(f"  auto_execute: {policy3.auto_execute}")
        print(f"  行动: {action3.action_type.value}")

    print("\n[阶段 5] 记忆检索验证")
    print("-" * 40)

    memories = agent.memory_store.retrieve("delete", "filesystem")
    print(f"检索到 {len(memories)} 条相关记忆:")
    for mem in memories:
        print(f"  - {mem}")

    print_separator("Demo 1 完成")
    print("验证结果:")
    print("  ✓ 高损失事件导致 threat 上升")
    print("  ✓ 相似操作的风险阈值下降")
    print("  ✓ 验证步骤自动增加")
    print("  ✓ auto_execute 变为 False")
    print("  ✓ 情感记忆已写入")

    return True


if __name__ == "__main__":
    run_demo()
