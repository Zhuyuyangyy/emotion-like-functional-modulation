# Manuscript Failure Analysis Insert

## Discussion: External-Style Stress Test Results

To assess the robustness of our approach, we conducted an external-style stress test using a new benchmark with different formatting and distribution compared to our original semireal dataset. The results reveal important insights about the system's performance boundaries.

### Degradation Is Not Failure

While overall performance degrades on the external-style stress test—with composite score dropping from 0.835 to 0.664 and action accuracy decreasing from 0.753 to 0.627—this degradation does not constitute a failure of the safety system. Critically, the risky auto-execution rate remains bounded below 10% (8.3%), maintaining the core safety guarantee. The external-style test serves as a diagnostic tool to identify weaknesses, not as a proof of generalization.

### Weakest Scenarios

We identified two source types where performance degraded most significantly:
1. **Benign Review Trace**: Composite score 0.378, risky auto-exec rate 27.3%, action accuracy 0.20
2. **Deployment Pipeline Trace**: Composite score 0.542, risky auto-exec rate 30.8%, action accuracy 0.55

These failures fall into several key categories:
- Read-only but security-sensitive operations
- Deployment context ambiguity
- Benign security review confusion
- External API ambiguity
- Credential read access confusion

### Future Improvements

The error taxonomy we developed points to clear avenues for future work:
- Better nuanced risk scoring for metadata vs secret access
- Explicit parsing of deployment context
- Improved semantic understanding of review intent
- Context-aware keyword weighting
- Better utilization of experience signals
- Reduced dependency on structured labels

These improvements will help strengthen the system's robustness while maintaining the core safety guarantees.

### Generalization Claim

We do not claim that our system solves cross-domain safety or generalizes broadly. Instead, we show bounded robustness with risky auto-execution below 10% on external-style stress tests, and we use the degraded performance to motivate future research directions.
