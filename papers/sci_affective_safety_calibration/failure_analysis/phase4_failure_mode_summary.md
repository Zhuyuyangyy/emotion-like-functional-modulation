# Phase 4: Failure Mode Summary

## External-Style Stress Test Value
The external-style stress test serves three critical purposes:
1. **Diagnostic Tool**: Reveals weaknesses in the system's decision-making
2. **Generalization Check**: Tests performance on differently formatted data
3. **Improvement Guide**: Points to specific areas for future research

## Main Failure Modes Found
1. **Read-Only Security-Sensitive Misclassification**: Over-caution on metadata checks
2. **Deployment Context Ambiguity**: Confusion between staging/production and safe/risky deploys
3. **Benign Review Confusion**: Mixing up operational reviews and security reviews
4. **Keyword Override**: Safe keywords overriding actual risk context
5. **Experience Underuse**: Not properly utilizing historical failure signals
6. **Label Dependency**: Over-reliance on specific structured label formats
7. **External API Ambiguity**: Misclassifying cloud/infra API calls

## Impact on Q2 Submission
- The results **do not prevent Q2 submission**
- We need to revise claims to avoid overstating generalization
- We should include the failure analysis as part of the Discussion section
- The bounded risky auto-exec (<10%) is a key positive result to highlight

## Recommendation: Proceed to Phase 5
**Recommendation**: Proceed to Phase 5 with the following caveats:
- Include the failure analysis in the manuscript
- Revise claims to be honest about degradation
- Highlight the bounded risky auto-exec as a safety win
- Use the error taxonomy to guide future work
