# Manuscript Revision Checklist — v0.2

**Paper:** Experience-Shaped Affective Safety Calibration for Autonomous Agents
**Revision Target:** v0.1 → v0.2
**Date:** 2026-05-27
**Scope:** Numeric corrections, figure/table placement, claims verification, sentence convergence, baseline recommendation

---

## 1. Numeric Consistency Revisions

> **Root cause:** SafeKeywordFirstBaseline Risky Auto-Exec was originally reported as 0.624; verified value is **0.872**. All downstream percentages derived from this figure must be recalculated.

| # | Source File | Location | Current Value | Corrected Value | Status |
|---|-------------|----------|---------------|-----------------|--------|
| 1.1 | `sci_claim_evidence_map.md` | Claim 1 — baseline Risky Auto-Exec | 0.624 | **0.872** | ☐ Pending |
| 1.2 | `sci_claim_evidence_map.md` | Claim 1 — relative reduction | 93.6% | **95.9%** | ☐ Pending |
| 1.3 | `materials_for_manuscript_v0_1.md` | Part E1, Claim 1 — relative reduction | 93.6% | **95.9%** | ☐ Pending |
| 1.4 | `v1_1_paper_tables.md` | Table 2 — SafeKeywordFirstBaseline row, Risky Auto-Exec column | verify | must read **0.872** | ☐ Pending |
| 1.5 | `v1_1_paper_tables.md` | Table 6 — V1.0 results, if SafeKeywordFirstBaseline appears | verify | must read **0.872** | ☐ Pending |
| 1.6 | Any caption or in-text reference to "93.6% reduction" | manuscript body / abstract / conclusions | 93.6% | **95.9%** | ☐ Pending |
| 1.7 | Any caption or in-text reference to "0.624" baseline | manuscript body / abstract / conclusions | 0.624 | **0.872** | ☐ Pending |

**Verification step:** After all edits, run a project-wide search for `0.624` and `93.6` to confirm zero residual occurrences.

---

## 2. Figure Insertion Recommendations

| Figure | Asset Name | Manuscript Section | Sub-section | Placement Notes |
|--------|-----------|-------------------|-------------|-----------------|
| Figure 1 | `fig1_framework_architecture` | §3 Method | Architecture overview | First figure in §3; place after the system description paragraph, before sub-section 3.1 |
| Figure 2 | `fig2_three_tier_policy` | §3 Method | Calibration logic | After the three-tier policy explanation; readers should see the tier diagram alongside the formal description |
| Figure 3 | `fig3_risky_auto_exec_comparison` | §5 Results | Main comparison | Central to Claim 1; place immediately after the paragraph reporting the 95.9% reduction |
| Figure 4 | `fig4_longitudinal_memory_tradeoff` | §5 Results | Memory analysis | Supports Claims 3 & 4; place after the longitudinal memory paragraph, before the statistical tests sub-section |

**Cross-reference checklist:**
- ☐ Every figure is referenced in the body text before it appears.
- ☐ Figure numbering is sequential (1 → 2 → 3 → 4) with no gaps.
- ☐ Captions are self-contained (understandable without reading the main text).
- ☐ All axis labels, legends, and annotations are legible at single-column width.

---

## 3. Table Insertion Recommendations

| Table | Content | Manuscript Section | Sub-section | Placement Notes |
|-------|---------|-------------------|-------------|-----------------|
| Table 1 | Benchmark composition | §4 Experimental Setup | Datasets / Benchmarks | Defines the evaluation scope; place after the benchmark description paragraph |
| Table 2 | Main semi-real results | §5 Results | Main comparison | Primary evidence for Claims 1, 2, 5, 6; place alongside or immediately after Figure 3 |
| Table 3 | Longitudinal memory results | §5 Results | Memory analysis | Supports Claims 3 & 4; place alongside Figure 4 |
| Table 4 | Statistical tests | §5 Results | Statistical significance | Place after the main results discussion; readers should encounter significance tests before moving to Discussion |
| Table 5 | Error analysis | §6 Discussion | Error analysis | Qualitative complement to quantitative results; place in the error analysis sub-section of Discussion |
| Table 6 | V1.0 results | Appendix or Supplementary | — | Historical comparison only; does not belong in the main narrative. Add a one-line cross-reference in §5 if needed |

**Cross-reference checklist:**
- ☐ Every table is referenced in the body text before it appears.
- ☐ Table numbering is sequential (1 → 2 → 3 → 4 → 5) in the main body; Table 6 is Appendix Table A1 or similar.
- ☐ All abbreviations used in tables are defined in the table notes or caption.
- ☐ Bold/italic conventions for best results are applied consistently across all tables.

---

## 4. Claims Retention Assessment

| Claim | Statement (Summary) | Verdict | Action Required |
|-------|---------------------|---------|-----------------|
| Claim 1 | Strict context priority reduces risky auto-exec by ~95.9% vs. SafeKeywordFirstBaseline | **Keep — update numbers** | Replace 0.624 → 0.872 and 93.6% → 95.9% wherever Claim 1 is stated |
| Claim 2 | Affective pressure improves safety without severe efficiency trade-off | **Keep as-is** | No changes needed |
| Claim 3 | Single-failure memory achieves the best safety–efficiency balance | **Keep as-is** | No changes needed |
| Claim 4 | Accumulated memory leads to over-caution collapse | **Keep as-is** | Must NOT be phrased as "accumulated memory is recommended"; ensure language is clearly cautionary |
| Claim 5 | RiskContextOracleBaseline is a diagnostic upper bound, not deployable | **Keep as-is** | Verify every Oracle mention carries the "oracle / upper-bound / not deployable" label |
| Claim 6 | Full method achieves strong safety performance on semi-real benchmarks | **Keep as-is** | Must NOT imply Full Method outperforms Oracle |

**Prohibited-claim sweep:**
- ☐ Zero occurrences of "emotional intelligence" in the manuscript.
- ☐ Zero occurrences of "production validation" or equivalent.
- ☐ Zero sentences stating Full Method outperforms Oracle.
- ☐ Zero sentences recommending accumulated memory.

---

## 5. Sentences to Converge

The following sentence-level issues must be resolved before v0.2 submission. Each item identifies the problem pattern and the required convergence action.

### 5.1 Numeric Errors

| # | Problem Pattern | Convergence Action | Verification |
|---|----------------|-------------------|--------------|
| 5.1.1 | Any sentence claiming "93.6% reduction" | Replace with **"95.9% reduction"** | ☐ Search `93.6` — zero hits |
| 5.1.2 | Any sentence citing baseline Risky Auto-Exec as 0.624 | Replace with **0.872** | ☐ Search `0.624` — zero hits |

### 5.2 Prohibited Terminology

| # | Problem Pattern | Convergence Action | Verification |
|---|----------------|-------------------|--------------|
| 5.2.1 | Any sentence using "emotional intelligence" | Remove or replace with **"affective pressure"** or **"experience-shaped affective calibration"** | ☐ Search `emotional intelligence` — zero hits |
| 5.2.2 | Any sentence implying "production validation" | Remove or rephrase as **"controlled semi-real evaluation"** | ☐ Search `production validation` — zero hits |

### 5.3 Prohibited Comparisons

| # | Problem Pattern | Convergence Action | Verification |
|---|----------------|-------------------|--------------|
| 5.3.1 | Any sentence comparing Full Method favorably over Oracle | Remove the comparison; Oracle is an upper bound by definition | ☐ Search `outperform.*Oracle` / `better than.*Oracle` — zero hits |
| 5.3.2 | Any sentence recommending accumulated memory | Rewrite to clearly state accumulated memory causes over-caution collapse and is **not recommended** | ☐ Search `accumulated.*recommend` — zero hits |

### 5.4 Oracle Labeling

| # | Problem Pattern | Convergence Action | Verification |
|---|----------------|-------------------|--------------|
| 5.4.1 | Any mention of RiskContextOracleBaseline without qualifier | Append **"(oracle, upper-bound, not deployable)"** on first mention; use "Oracle" with at least one qualifier thereafter | ☐ Every Oracle instance carries a qualifier |

---

## 6. LLM-based Safety Classifier Baseline Recommendation

| Item | Detail |
|------|--------|
| **Recommendation** | **YES — include as a future-work or appendix item** |
| **Rationale** | Reviewers in the safety-calibration space will likely ask how the proposed method compares to a direct LLM-based safety classifier (e.g., prompting an LLM to classify actions as safe/risky). Acknowledging this alternative demonstrates awareness and preempts a common reviewer concern. |
| **Design document** | `optional_llm_baseline_design.md` — already prepared |
| **Scope in this paper** | Textual discussion only (§7 Future Work or Appendix B). Do **NOT** run the LLM baseline experiment in this paper cycle; it would require additional compute, prompt-engineering iteration, and fairness calibration that are beyond the current scope. |
| **Suggested wording** | "An alternative approach is to employ an LLM as a direct safety classifier via prompted evaluation. While conceptually straightforward, such baselines introduce their own failure modes (prompt sensitivity, inconsistent calibration across contexts, and lack of experience-shaped adaptation). A systematic comparison with LLM-based safety classifiers is planned as future work." |

**Checklist:**
- ☐ Future-work paragraph added to §7 or Appendix.
- ☐ No experimental results for the LLM baseline are included.
- ☐ Reference to `optional_llm_baseline_design.md` is noted internally but not cited in the manuscript.

---

## Pre-submission Sign-off

| Check | Status |
|-------|--------|
| All numeric corrections applied and verified (§1) | ☐ |
| All figures placed and cross-referenced (§2) | ☐ |
| All tables placed and cross-referenced (§3) | ☐ |
| All claims verified against evidence (§4) | ☐ |
| All prohibited sentences converged (§5) | ☐ |
| LLM baseline future-work paragraph added (§6) | ☐ |
| Project-wide search for residual errors (`0.624`, `93.6`, `emotional intelligence`, `production validation`) returns zero hits | ☐ |

---

*End of v0.2 revision checklist.*
