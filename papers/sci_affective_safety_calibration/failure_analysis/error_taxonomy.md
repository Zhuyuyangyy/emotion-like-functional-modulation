# Error Taxonomy

## 1. READ_ONLY_SECURITY_SENSITIVE
- **Definition**: Operations that are read-only but involve security-sensitive contexts (credential metadata, compliance audits, security review)
- **Typical Scenario**: Checking credential rotation status, viewing security logs, or auditing IAM policies
- **Likely Model Behavior**: Over-classifies as requiring human review, increasing false over-caution rate
- **Mitigation Direction**: Add nuanced risk scoring that differentiates metadata access from actual secret material access

## 2. DEPLOYMENT_CONTEXT_AMBIGUITY
- **Definition**: Deployment pipeline operations where the context (staging vs production, with/without safety checks) is ambiguous
- **Typical Scenario**: "Deploy to production" vs "Deploy to staging" with similar wording, or force-deploy vs normal deploy
- **Likely Model Behavior**: Either under-caution (auto-executes risky deploys) or over-caution (blocks safe deploys)
- **Mitigation Direction**: Explicitly parse deployment targets and safety gate status from the context

## 3. BENIGN_SECURITY_REVIEW_CONFUSION
- **Definition**: Confusion between routine operational reviews and actual security-critical reviews
- **Typical Scenario**: Checking service health vs performing a security audit; both use "review" terminology
- **Likely Model Behavior**: Inconsistent classification - sometimes blocks benign checks, sometimes auto-execs risky ones
- **Mitigation Direction**: Better semantic understanding of review intent and context

## 4. SAFE_KEYWORD_RISK_OVERRIDE
- **Definition**: Cases where "safe" keywords (like "check", "view", "list") override actual risk signals from the context
- **Typical Scenario**: "Check production database encryption status" sounds safe but involves a security-critical production context
- **Likely Model Behavior**: Under-caution, auto-executing operations that should be reviewed
- **Mitigation Direction**: Context-aware keyword weighting that gives priority to production/security signals over action verbs

## 5. EXPERIENCE_SIGNAL_UNDERUSE
- **Definition**: Failure to properly utilize experience signals (similar failures, risk counts) from the context
- **Typical Scenario**: A case with "similar_failure_before: true" but model ignores it and makes the same risky decision
- **Likely Model Behavior**: Repeat mistakes, not learning from historical signals in the prompt
- **Mitigation Direction**: Explicitly surface and weight experience signals in the decision-making process

## 6. ORACLE_LABEL_DEPENDENCY
- **Definition**: Over-reliance on explicit risk context labels that might not generalize to new formats
- **Typical Scenario**: Model performs well when given explicit `risk_context` fields but fails in external formats without them
- **Likely Model Behavior**: Degraded performance in external-style tests where labeling schema differs
- **Mitigation Direction**: Reduce dependency on structured labels and improve semantic risk understanding

## 7. EXTERNAL_API_AMBIGUITY
- **Definition**: Ambiguity in cloud/infrastructure API calls that can be either safe or risky depending on parameters
- **Typical Scenario**: "Update AWS Lambda configuration" could be safe (changing log levels) or risky (changing IAM roles)
- **Likely Model Behavior**: Misclassification of risk level
- **Mitigation Direction**: Parse API parameters and resource context to assess actual risk
