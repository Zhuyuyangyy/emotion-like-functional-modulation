"""
Run all demos for Experience-Shaped Affective Agent V0.2

Runs all available demos:
- V0.1: Pain Memory, Trust Collapse, Anxiety Control
- V0.2: Fear Decay, Trust Recovery
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from demos.demo_pain_memory import run_demo as run_pain_memory
from demos.demo_trust_collapse import run_demo as run_trust_collapse
from demos.demo_anxiety_control import run_demo as run_anxiety_control
from demos.demo_fear_decay import run as run_fear_decay
from demos.demo_trust_recovery import run as run_trust_recovery


def main():
    print("\n" + "=" * 70)
    print("  Experience-Shaped Affective Agent V0.2 - Demo Suite")
    print("=" * 70)

    results = []

    print("\n--- V0.1 Demos ---")
    results.append(("Pain Memory (V0.1)", run_pain_memory()))
    results.append(("Trust Collapse (V0.1)", run_trust_collapse()))
    results.append(("Anxiety Control (V0.1)", run_anxiety_control()))

    print("\n--- V0.2 Demos ---")
    results.append(("Fear Decay (V0.2)", run_fear_decay()))
    results.append(("Trust Recovery (V0.2)", run_trust_recovery()))

    print("\n" + "=" * 70)
    print("  Demo Summary")
    print("=" * 70)

    for name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"  {name}: {status}")

    all_passed = all(success for _, success in results)
    passed_count = sum(1 for _, success in results if success)

    print("\n" + "=" * 70)
    if all_passed:
        print(f"  All {len(results)} demos passed!")
    else:
        print(f"  {passed_count}/{len(results)} demos passed, {len(results) - passed_count} failed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
