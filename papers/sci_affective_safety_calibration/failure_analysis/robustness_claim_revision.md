# Robustness Claim Revision

## Forbidden Claims (Do Not Use)
- ❌ "The model generalizes well across benchmarks"
- ❌ "The system is robust across external datasets"
- ❌ "Our approach solves cross-domain safety"
- ❌ "Performance is maintained across all settings"

## Allowed Claims (Use These Instead)

### 1. Limited Cross-Benchmark Robustness
- "The system shows bounded robustness to external-style stress tests, maintaining risky auto-execution below 10%"
- "While performance degrades on external-style tests, the safety guardrails remain partially effective"

### 2. Risky Auto-Exec Bound
- "The full calibrator adapter maintains risky auto-execution below 10% on external-style stress tests"
- "Even with degraded overall performance, the critical safety metric (risky auto-exec) remains bounded"

### 3. Honest Degradation Disclosure
- "External-style stress tests reveal degraded performance compared to the original semireal benchmark"
- "The composite score drops from 0.835 to 0.664 when evaluated on external-style data"

### 4. Motivates Future Improvements
- "These failures motivate future work on better cross-domain generalization"
- "The identified error categories point to clear avenues for improvement"

## Key Message
The external-style stress test is a **diagnostic tool**, not a proof of generalization. It reveals weaknesses and guides improvements, rather than demonstrating broad robustness.
