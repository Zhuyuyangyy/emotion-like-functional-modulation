"""
Run all demos
"""

import sys
import os
sys.path.insert(0, '/workspace/src')

sys.path.insert(0, '/workspace')
os.chdir('/workspace')

from demos.demo_pain_memory import run as run_pain_memory
from demos.demo_trust_collapse import run as run_trust_collapse
from demos.demo_anxiety_control import run as run_anxiety_control


def main():
    print("\n" + "=" * 70)
    print("  Experience-Shaped Affective Agent V0.1 - Demo Suite")
    print("=" * 70)

    results = []

    results.append(("Pain Memory", run_pain_memory()))
    results.append(("Trust Collapse", run_trust_collapse()))
    results.append(("Anxiety Control", run_anxiety_control()))

    print("\n" + "=" * 70)
    print("  Demo Summary")
    print("=" * 70)

    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {name}: {status}")

    all_passed = all(success for _, success in results)
    print("\n" + "=" * 70)
    if all_passed:
        print("  All demos passed!")
    else:
        print("  Some demos failed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
