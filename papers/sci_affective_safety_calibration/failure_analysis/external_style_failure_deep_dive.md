# External Style Failure Deep Dive

## Overall Degradation Summary
| Metric | Original (Semireal) | External Style | Delta |
|--------|---------------------|----------------|-------|
| Composite Score | 0.835 | 0.664 | -0.171 |
| Risky Auto-Exec Rate | 3.6% | 8.3% | +4.7pp |
| Action Accuracy | 0.753 | 0.627 | -0.126 |

## Worst Performing Source Types

### 1. Benign Review Trace
- **Composite Score**: 0.378
- **Risky Auto-Exec Rate**: 27.3%
- **False Over-Caution Rate**: 57.1%
- **Action Accuracy**: 0.20

### 2. Deployment Pipeline Trace
- **Composite Score**: 0.542
- **Risky Auto-Exec Rate**: 30.8%
- **False Over-Caution Rate**: 66.7%
- **Action Accuracy**: 0.55

## Error Categories with ≥3 Case IDs

### 1. Read-Only But Security-Sensitive
- **Description**: Cases where operations are read-only but involve security-critical contexts (credential metadata, compliance checks)
- **Example Case IDs**: EXT-AS-0004, EXT-AS-0036, EXT-AS-0040
- **Impact**: Over-caution leading to unnecessary human review

### 2. Deployment Verbs Too Broad
- **Description**: Cases where deployment pipeline operations are misclassified due to ambiguous action verbs
- **Example Case IDs**: EXT-AS-0029, EXT-AS-0052, EXT-AS-0022
- **Impact**: Either too risky auto-exec or too much over-caution

### 3. Benign Security Review Over/Under-Trigger
- **Description**: Cases where routine operational reviews are misclassified as security-critical or vice versa
- **Example Case IDs**: EXT-AS-0015, EXT-AS-0026, EXT-AS-0042
- **Impact**: Inconsistent decision making

### 4. External API Ambiguity
- **Description**: Cases where cloud/infra API calls have ambiguous risk profiles
- **Example Case IDs**: EXT-AS-0002, EXT-AS-0017, EXT-AS-0047
- **Impact**: Misclassification of risk levels

### 5. Credential Read Access
- **Description**: Cases involving credential metadata vs actual secret material access
- **Example Case IDs**: EXT-AS-0016, EXT-AS-0045, EXT-AS-0051
- **Impact**: Over-caution on metadata checks, or under-caution on actual secret access
