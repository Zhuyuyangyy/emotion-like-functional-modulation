# Numeric Consistency Audit — v0.3

**Project**: Experience-Shaped Affective Safety Calibration for Autonomous Agent Execution
**Audit Version**: v0.3
**Date**: 2026-05-27
**Scope**: All core numbers across project documentation files, with emphasis on residual errors from the 0.624/93.6% correction chain.

---

## 1. Core Number Registry

### 1.1 FullCalibratorAdapter (Semi-Real / Affective-Agent-Safety-300)

| Metric | Canonical Value | Raw Value (JSON) |
|--------|----------------|-------------------|
| Action Accuracy | 0.753 | 0.7533 |
| Risky Auto-Exec | 0.036 | 0.0355 |
| False Caution | 0.122 | — |
| Safe Auto-Exec Acc | 0.757 | — |
| Composite | 0.860 | — |

**Locations across audited files:**

| File | Line(s) | Form | Consistent? |
|------|---------|------|-------------|
| `manuscript_v0_2.md` | L132 (table) | 0.753 / 0.036 / 0.860 | ✅ |
| `manuscript_v0_2.md` | L140 (text) | "3.6% risky auto-execution" | ✅ |
| `manuscript_v0_2.md` | L160–L161 (bootstrap) | Mean 0.753 / 0.860 | ✅ |
| `reproducibility_audit.md` | L64–L66 | 0.753 / 0.036 / 0.860 | ✅ |
| `figure_captions.md` | L13 | "3.6% risky auto-execution" | ✅ |
| `numeric_consistency_audit.md` (v0.1) | L29 | 0.0355 (raw) | ✅ |
| `materials_for_manuscript_v0_1.md` | L71, L97–L98, L305 | 0.753 / 0.036 / 0.860 | ✅ |

**Verdict**: ✅ Fully consistent across all files.

---

### 1.2 SafeKeywordFirstBaseline Risky Auto-Exec

| Benchmark | Canonical Value | Raw Value (JSON) |
|-----------|----------------|-------------------|
| Semi-Real (Affective-Agent-Safety-300) | **0.872** | 0.8723 |
| V1.0 (Affective-Safety-200) | **0.809** | 0.8092 |

**Locations across audited files:**

| File | Line(s) | Value | Benchmark Context | Consistent? |
|------|---------|-------|-------------------|-------------|
| `manuscript_v0_2.md` | L134 (table) | 0.872 | Semi-real | ✅ |
| `manuscript_v0_2.md` | L140 (text) | "87.2%" | Semi-real | ✅ |
| `manuscript_v0_2.md` | L260 (appendix table) | 0.809 | V1.0 | ✅ |
| `reproducibility_audit.md` | L67 | 0.872 | Semi-real | ✅ |
| `reproducibility_audit.md` | L42 | 0.809 | V1.0 | ✅ |
| `figure_captions.md` | L13 | "87.2%" | Semi-real | ✅ |
| `numeric_consistency_audit.md` (v0.1) | L9 | 0.8723 (raw) | Semi-real | ✅ |
| `numeric_consistency_audit.md` (v0.1) | L10 | 0.8092 (raw) | V1.0 | ✅ |
| `materials_for_manuscript_v0_1.md` | L73 | 0.872 | Semi-real | ✅ |
| `materials_for_manuscript_v0_1.md` | L46 | 0.809 | V1.0 | ✅ |
| `materials_for_manuscript_v0_1.md` | **L300** | **"62.4%"** | Semi-real | ❌ **ACTIVE RESIDUAL ERROR** |

**Verdict**: ⚠️ One active residual error in `materials_for_manuscript_v0_1.md` L300.

---

### 1.3 Relative Reduction

| Benchmark | Formula | Result |
|-----------|---------|--------|
| Semi-Real | (0.872 − 0.036) / 0.872 | **95.9%** |
| V1.0 | (0.809 − 0.046) / 0.809 | **94.3%** |

**Locations across audited files:**

| File | Line(s) | Value | Consistent? |
|------|---------|-------|-------------|
| `manuscript_v0_2.md` | L5 (abstract) | "95.9% relative reduction" | ✅ |
| `manuscript_v0_2.md` | L140 | "a 95.9% relative reduction" | ✅ |
| `manuscript_v0_2.md` | L190 | "a 95.9% relative reduction" | ✅ |
| `manuscript_v0_2.md` | L219 | "95.9% compared to a safe-keyword-first baseline" | ✅ |
| `reproducibility_audit.md` | L77 | "(0.872 − 0.036) / 0.872 = 95.9%" | ✅ |
| `numeric_consistency_audit.md` (v0.1) | L31 | "95.9%" | ✅ |
| `numeric_consistency_audit.md` (v0.1) | L39 | "94.3%" (V1.0) | ✅ |
| `manuscript_v0_2_revision_checklist.md` | L68 | "~95.9%" | ✅ |
| `materials_for_manuscript_v0_1.md` | **L300** | **"93.6%"** | ❌ **ACTIVE RESIDUAL ERROR** |

**Verdict**: ⚠️ One active residual error in `materials_for_manuscript_v0_1.md` L300.

---

### 1.4 Longitudinal Memory Experiment

| Group | Risky Auto-Exec | Safe Auto-Exec Acc | Composite |
|-------|----------------|-------------------|-----------|
| no_memory | 0.043 | 0.757 | 0.830 |
| single_failure_memory | 0.036 | 0.757 | 0.835 |
| accumulated_failure_memory | 0.000 | 0.000 | 0.716 |

**Locations across audited files:**

| File | Line(s) | Values | Consistent? |
|------|---------|--------|-------------|
| `manuscript_v0_2.md` | L148–L150 (table) | All three rows | ✅ |
| `manuscript_v0_2.md` | L152 (text) | "0.757 to 0.000" | ✅ |
| `reproducibility_audit.md` | L94–L96 | All three rows | ✅ |
| `figure_captions.md` | L17 | "3.6% vs 4.3%", "0.757", "0.000" | ✅ |
| `materials_for_manuscript_v0_1.md` | L85–L86 | no_memory / single_failure | ✅ |

**Verdict**: ✅ Fully consistent across all files.

---

### 1.5 Test Counts

| Suite | Count |
|-------|-------|
| Total | 290/290 |
| V0.9.1 core framework | 249/249 |
| V1.0 experiment tests | 16/16 |
| V1.1 experiment tests | 25/25 |

**Locations across audited files:**

| File | Line(s) | Values | Consistent? |
|------|---------|--------|-------------|
| `dataset_card.md` | L183–L186 | 290/290, 249/249, 16/16, 25/25 | ✅ |
| `reproducibility_audit.md` | L17, L175–L178 | 290/290, 249/249, 16/16, 25/25 | ✅ |

**Verdict**: ✅ Fully consistent across all files.

---

### 1.6 V1.0 (Affective-Safety-200) FullCalibratorAdapter

| Metric | Value |
|--------|-------|
| Action Accuracy | 0.605 |
| Risky Auto-Exec | 0.046 |
| Composite | 0.757 |

**Locations across audited files:**

| File | Line(s) | Values | Consistent? |
|------|---------|--------|-------------|
| `manuscript_v0_2.md` | L258 (appendix table) | 0.605 / 0.046 / 0.757 | ✅ |
| `manuscript_v0_2.md` | L270 (ablation table) | 0.605 / 0.046 / 0.757 | ✅ |
| `reproducibility_audit.md` | L39–L41 | 0.605 / 0.046 / 0.757 | ✅ |
| `materials_for_manuscript_v0_1.md` | L44, L58, L61 | 0.605 / 0.046 / 0.757 | ✅ |

**Verdict**: ✅ Fully consistent across all files.

---

### 1.7 V1.0 SafeKeywordFirstBaseline Risky Auto-Exec

| Value |
|-------|
| 0.809 |

**Locations across audited files:**

| File | Line(s) | Value | Consistent? |
|------|---------|-------|-------------|
| `manuscript_v0_2.md` | L260 (appendix table) | 0.809 | ✅ |
| `reproducibility_audit.md` | L42 | 0.809 | ✅ |
| `numeric_consistency_audit.md` (v0.1) | L10 | 0.8092 (raw) | ✅ |
| `materials_for_manuscript_v0_1.md` | L46 | 0.809 | ✅ |

**Verdict**: ✅ Fully consistent across all files.

---

## 2. Residual "0.624" Check

### Project-wide search results

| File | Line | Context | Classification |
|------|------|---------|----------------|
| `materials_for_manuscript_v0_1.md` | L300 | "3.6% vs 62.4% on semi-real benchmark" | ❌ **ACTIVE RESIDUAL — must be corrected to "3.6% vs 87.2%"** |
| `numeric_consistency_audit.md` (v0.1) | L3 | Section title "0.872 vs 0.624" | ℹ️ Error-documentation context (v0.1 audit) |
| `numeric_consistency_audit.md` (v0.1) | L17 | "0.624 \| Unclear/mixed \| **Incorrect**" | ℹ️ Error-documentation context |
| `numeric_consistency_audit.md` (v0.1) | L22 | "value 0.624...may be a copy error" | ℹ️ Error-documentation context |
| `numeric_consistency_audit.md` (v0.1) | L46 | "3.6% vs 62.4%" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L12 | "originally reported as 0.624" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L16 | "0.624 \| **0.872**" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L22 | "0.624 \| 0.872" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L68 | "Replace 0.624 → 0.872" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L92 | "citing baseline Risky Auto-Exec as 0.624" | ℹ️ Error-documentation context |
| `manuscript_v0_2.md` | — | Not found | ✅ Clean |

**Summary**: 1 active residual error in `materials_for_manuscript_v0_1.md` L300. All other occurrences are in error-documentation context (v0.1 audit and revision checklist) and are acceptable. The manuscript itself is clean.

---

## 3. Residual "93.6%" Check

### Project-wide search results

| File | Line | Context | Classification |
|------|------|---------|----------------|
| `materials_for_manuscript_v0_1.md` | L300 | "reduced risky auto-execution by 93.6%" | ❌ **ACTIVE RESIDUAL — must be corrected to "95.9%"** |
| `numeric_consistency_audit.md` (v0.1) | L47 | "93.6% reduction" → "95.9% reduction" | ℹ️ Error-documentation context |
| `numeric_consistency_audit.md` (v0.1) | L49 | "93.6%" → "95.9%" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L17 | "93.6% \| **95.9%**" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L18 | "93.6% \| **95.9%**" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L21 | "93.6% \| **95.9%**" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L68 | "93.6% → 95.9%" | ℹ️ Error-documentation context |
| `manuscript_v0_2_revision_checklist.md` | L91 | "93.6% reduction" | ℹ️ Error-documentation context |
| `manuscript_v0_2.md` | — | Not found | ✅ Clean |

**Summary**: 1 active residual error in `materials_for_manuscript_v0_1.md` L300 (same line as the 0.624 residual). All other occurrences are in error-documentation context. The manuscript itself is clean.

---

## 4. "Production Validation" Claims Check

### Project-wide search results

| File | Line | Context | Classification |
|------|------|---------|----------------|
| `manuscript_v0_2.md` | L197 | "We do not claim production deployment validation." | ✅ Negative disclaimer |
| `data_authenticity_statement.md` | L68 | "We do not claim production deployment validation." | ✅ Negative disclaimer |
| `dataset_card.md` | L131 | "Production deployment: The benchmarks are for research only" | ✅ Negative disclaimer |
| `manuscript_v0_2_revision_checklist.md` | L77, L99, L143 | Search instructions for prohibited term | ℹ️ Meta-documentation |

**Summary**: ✅ No positive "production validation" claims found. All occurrences are explicit disclaimers or meta-documentation.

---

## 5. "Emotional Intelligence" Claims Check

### Project-wide search results

| File | Line | Context | Classification |
|------|------|---------|----------------|
| `related_work_v0_3.md` | L19 | "nor do we claim that our agent possesses emotional intelligence" | ⚠️ Negative disclaimer, but uses the prohibited phrase verbatim |
| `materials_for_manuscript_v0_1.md` | L312 | "Our agent has emotional intelligence" — listed as prohibited claim X2 | ℹ️ Correctly flagged as prohibited |
| `manuscript_v0_2.md` | L210 | "not general affective intelligence" | ✅ Uses "affective intelligence" in negative context |
| `manuscript_v0_2_revision_checklist.md` | L76, L98, L143 | Search instructions for prohibited term | ℹ️ Meta-documentation |

**Summary**: ⚠️ `related_work_v0_3.md` L19 contains the exact phrase "emotional intelligence" in a negative disclaimer. While this is not a positive claim, the revision checklist (§5.2.1) requires "Zero occurrences of 'emotional intelligence' in the manuscript." If this text is incorporated into the manuscript, the phrase should be rephrased — e.g., "nor do we claim that our agent possesses general affective understanding" or similar. The manuscript itself (`manuscript_v0_2.md`) is clean.

---

## 6. Sentences Requiring Modification

### 6.1 Active Residual Errors (must fix)

| # | File | Line | Current Text | Required Correction | Priority |
|---|------|------|-------------|---------------------|----------|
| 6.1.1 | `materials_for_manuscript_v0_1.md` | L300 | "reduced risky auto-execution by 93.6% compared to safe-keyword-first baseline (3.6% vs 62.4% on semi-real benchmark)" | "reduced risky auto-execution by 95.9% compared to safe-keyword-first baseline (3.6% vs 87.2% on semi-real benchmark)" | **HIGH** |

### 6.2 Prohibited Phrase in Draft Material (should fix before incorporation)

| # | File | Line | Current Text | Required Correction | Priority |
|---|------|------|-------------|---------------------|----------|
| 6.2.1 | `related_work_v0_3.md` | L19 | "nor do we claim that our agent possesses emotional intelligence" | "nor do we claim that our agent possesses general affective understanding" (or similar rephrasing that avoids the exact phrase) | **MEDIUM** |

### 6.3 V0.1 Audit and Revision Checklist (informational — no action needed)

The following files contain "0.624" and "93.6%" only in error-documentation context (identifying the original error and its correction). These are acceptable as historical audit records:

- `numeric_consistency_audit.md` (v0.1): Documents the 0.624 → 0.872 and 93.6% → 95.9% corrections.
- `manuscript_v0_2_revision_checklist.md`: Tracks the correction tasks.

No modifications needed for these files.

---

## 7. Additional Cross-Checks

### 7.1 Figure 4 Caption — "16.3% lower risky auto-execution"

`figure_captions.md` L17 states: "16.3% lower risky auto-execution than no memory (3.6% vs 4.3%)".

Verification: (4.3 − 3.6) / 4.3 = 0.7 / 4.3 = 0.1628 ≈ 16.3%. ✅ Correct.

### 7.2 V1.0 Relative Reduction (not stated in manuscript)

`numeric_consistency_audit.md` (v0.1) L39: (0.8092 − 0.0461) / 0.8092 = 0.9431 = 94.3%.

This value does not appear in the manuscript. If it is ever cited, it should be 94.3%, not 93.6%.

### 7.3 Error Analysis Percentages

`manuscript_v0_2.md` L179–L184 error rates:

| Source Type | Cases | Errors | Stated Rate | Computed Rate | Match? |
|-------------|-------|--------|-------------|---------------|--------|
| coding_agent_trace | 100 | 31 | 31.0% | 31.0% | ✅ |
| affective_pressure_trace | 60 | 17 | 28.3% | 28.33% | ✅ |
| tool_use_risk_trace | 80 | 15 | 18.8% | 18.75% | ✅ |
| experience_failure_trace | 20 | 6 | 30.0% | 30.0% | ✅ |
| safe_low_risk_trace | 40 | 5 | 12.5% | 12.5% | ✅ |

### 7.4 Source Type Distribution Sums

**Affective-Agent-Safety-300**: 100 + 80 + 60 + 40 + 20 = 300. ✅

**Affective-Safety-200**: 40 + 35 + 30 + 30 + 25 + 25 + 15 = 200. ✅

Both confirmed in `manuscript_v0_2.md` L98–L103 and `dataset_card.md` L39–L45, L49–L55.

### 7.5 Bootstrap Confidence Intervals

`manuscript_v0_2.md` L160–L161 and `reproducibility_audit.md` L114–L115 both report:

| Metric | Mean | 95% CI Lower | 95% CI Upper |
|--------|------|-------------|-------------|
| Action Accuracy | 0.753 | 0.703 | 0.800 |
| Composite Score | 0.860 | 0.826 | 0.892 |

✅ Consistent.

### 7.6 McNemar Test Results

`manuscript_v0_2.md` L167–L170 and `reproducibility_audit.md` L121–L124 both report identical χ² and p-values. ✅ Consistent.

---

## 8. Summary Verdict

| Check | Status | Detail |
|-------|--------|--------|
| FullCalibratorAdapter semi-real numbers | ✅ Consistent | 0.753 / 0.036 / 0.860 across all files |
| SafeKeywordFirstBaseline semi-real Risky Auto-Exec | ⚠️ 1 residual | `materials_for_manuscript_v0_1.md` L300 still says "62.4%" |
| Relative reduction | ⚠️ 1 residual | `materials_for_manuscript_v0_1.md` L300 still says "93.6%" |
| Longitudinal memory numbers | ✅ Consistent | 0.043 / 0.036 / 0.000 across all files |
| Test counts | ✅ Consistent | 290/290, 249/249, 16/16, 25/25 across all files |
| V1.0 FullCalibratorAdapter | ✅ Consistent | 0.046 / 0.757 across all files |
| V1.0 SafeKeywordFirstBaseline | ✅ Consistent | 0.809 across all files |
| "0.624" residuals | ⚠️ 1 active | `materials_for_manuscript_v0_1.md` L300 |
| "93.6%" residuals | ⚠️ 1 active | `materials_for_manuscript_v0_1.md` L300 |
| "production validation" claims | ✅ Clean | Only disclaimers found |
| "emotional intelligence" claims | ⚠️ 1 phrase | `related_work_v0_3.md` L19 (negative context, but uses exact prohibited phrase) |
| Manuscript (`manuscript_v0_2.md`) | ✅ Clean | No residual errors, no prohibited claims |

---

## 9. Action Items

| # | Action | File | Priority |
|---|--------|------|----------|
| 1 | Replace "93.6%" with "95.9%" and "62.4%" with "87.2%" in Claim C1 | `materials_for_manuscript_v0_1.md` L300 | HIGH |
| 2 | Rephrase "emotional intelligence" in negative disclaimer if this text is to be incorporated into the manuscript | `related_work_v0_3.md` L19 | MEDIUM |
| 3 | After corrections, re-run project-wide search for `0.624`, `93.6`, `emotional intelligence`, and `production validation` to confirm zero active residuals | Project-wide | HIGH |

---

*End of v0.3 numeric consistency audit.*
