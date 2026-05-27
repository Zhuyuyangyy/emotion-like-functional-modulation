# Submission Readiness Checklist

**Paper**: Experience-Shaped Affective Safety Calibration for Autonomous Agent Execution
**Assessment Date**: 2026-05-27
**Assessor**: Automated readiness review based on project artifact audit

---

## Item 1: Verified References

**Status**: ✅ PASS (with 1 minor action item)

**Evidence**: `references_verified.md` — 37 entries across 6 categories (Tool-Using LLM Agents, Agent Safety, Human-in-the-Loop AI, Affective Computing, Memory/Experience Replay, Statistical Testing).

**Assessment**:

- 36 of 37 references are fully verified with confirmed DOIs, arXiv IDs, and venue information.
- Each entry includes a relevance statement explaining its connection to the paper's contribution.
- Reference categories are well-balanced: 7 agent architecture, 7 safety, 5 HITL, 6 affective computing, 5 memory/adaptive, 6 statistical methods.
- Foundational references are appropriately selected (Picard 1997, Lazarus 1991, McNemar 1947, Demšar 2006).
- Recent references (2024–2026) demonstrate currency and awareness of the field.

**Open Issue**:

| # | Reference | Issue | Action Required |
|---|-----------|-------|-----------------|
| 1 | [15] ToolSafe (Mou et al. 2026), arXiv:2601.10156 | Marked "needs verification" — 2026 arXiv ID; confirm publication status and venue | Verify whether this preprint has been accepted at a venue or remains an arXiv-only preprint. If unverified, consider replacing with an alternative verified reference on step-level safety guardrails, or retain with an explicit "preprint" label in the manuscript. |

**Risk Level**: Low. A single unverified entry does not compromise the reference list's integrity, but it must be resolved before submission to avoid reviewer credibility concerns.

---

## Item 2: Figures

**Status**: ✅ PASS

**Evidence**: `figures/` directory — 4 figures, each in PNG + PDF format.

| Figure | Filename | Type | Format | B&W Readable | SCI Style |
|--------|----------|------|--------|-------------|-----------|
| Figure 1 | `fig1_framework_architecture` | Architecture diagram | PNG + PDF | Yes | Yes |
| Figure 2 | `fig2_three_tier_policy` | Policy tier diagram | PNG + PDF | Yes | Yes |
| Figure 3 | `fig3_risky_auto_exec_comparison` | Bar chart (quantitative) | PNG + PDF | Yes | Yes |
| Figure 4 | `fig4_longitudinal_memory_tradeoff` | Trade-off chart (quantitative) | PNG + PDF | Yes | Yes |

**Assessment**:

- All 4 figures are available in both PNG (screen preview) and PDF (publication vector) formats, meeting standard SCI journal requirements.
- Figures 1–2 are deterministic hand-drawn diagrams; Figures 3–4 are data-driven and generated from stored experimental results via `generate_figures.py`.
- Black-and-white readability is confirmed — critical for print-only journals that do not guarantee color reproduction.
- Figure captions are documented in `figure_captions.md` with consistent numerical claims cross-verified in `numeric_consistency_audit_v0_3.md`.
- All figures are reproducible from code (confirmed in `reproducibility_audit.md`).

**Risk Level**: None. Figures are publication-ready.

---

## Item 3: Data Authenticity Statement

**Status**: ✅ PASS

**Evidence**: `data_authenticity_statement.md`

**Assessment**:

- The statement clearly defines the data type: "semi-real = structured simulations, not production logs."
- Explicit disclaimers are provided for what the data is NOT: no production deployment validation, no real-time emotion recognition, no enterprise production logs, no general agent safety claims, no state-of-the-art claims.
- The term "semi-real" is precisely defined: case structures derived from abstracted patterns of real scenarios, but traces are structured simulations, not collected from real user interactions.
- Data generation provenance is documented with source types and realism levels.
- Annotation process and gold decision determination rules are described.
- The statement explains why the data is still useful despite not being production-collected (controlled benchmark, more realistic than toy cases, broad coverage, reproducible and auditable).

**Risk Level**: Low. The statement is thorough and proactively addresses the most likely reviewer concern about data authenticity.

---

## Item 4: Dataset Card

**Status**: ✅ PASS

**Evidence**: `dataset_card.md`

**Assessment**:

- Follows standard dataset card format with 11 sections: Dataset Name, Version, Number of Cases, Source Type Distribution, Label Space, Input Fields, Intended Use, Out-of-Scope Use, Known Limitations, Ethical Considerations, Reproducibility Information.
- Both benchmarks are documented: Affective-Safety-200 (200 cases, 7 categories) and Affective-Agent-Safety-300 (300 cases, 5 source types).
- The four-level safety decision taxonomy (AUTO_EXECUTE, SIMULATE_FIRST, HUMAN_REVIEW, BLOCK) is clearly defined.
- Input field schemas are specified for both benchmarks with types and descriptions.
- Out-of-scope uses are explicitly listed (production deployment, general agent safety claims, real-time emotion recognition, real-world effectiveness claims).
- Known limitations are enumerated (synthetic construction, limited domains, structured signals, no real user data, static cases).
- Ethical considerations include benefits, potential risks, and mitigations.
- Reproducibility information includes generation scripts, evaluation scripts, test status (290/290), and data file locations.

**Risk Level**: None. The dataset card meets community standards for transparency and responsible data documentation.

---

## Item 5: Reproducibility Audit

**Status**: ✅ PASS

**Evidence**: `reproducibility_audit.md`

**Assessment**:

- All benchmarks, experiments, figures, and tables are confirmed reproducible from code.
- 290/290 tests pass (249 core + 16 V1.0 + 25 V1.1).
- Core numerical values are cross-verified against stored JSON results.
- Statistical analysis (bootstrap 95% CI, McNemar paired comparisons) is reproducible with seeded randomness.
- Figure generation is fully automated via `generate_figures.py`.
- Table data matches stored results across all 6 paper tables.
- Step-by-step reproduction instructions are provided (environment setup, benchmark regeneration, experiment execution, figure regeneration, test verification).
- No external API calls are required; all computation is local.
- No manual editing of results or figures has occurred.

**Cross-verification with `numeric_consistency_audit_v0_3.md`**:

- FullCalibratorAdapter semi-real numbers (0.753 / 0.036 / 0.860) are consistent across all files.
- Relative reduction (95.9%) is consistent across manuscript, audit, and figure captions.
- Longitudinal memory numbers (0.043 / 0.036 / 0.000) are consistent across all files.
- One residual error exists in `materials_for_manuscript_v0_1.md` L300 (0.624 → 0.872, 93.6% → 95.9%), but the manuscript itself is clean.

**Risk Level**: Low. The residual error in `materials_for_manuscript_v0_1.md` does not affect the manuscript or any submission artifact, but should be corrected for project hygiene.

---

## Item 6: Limitations

**Status**: ✅ PASS

**Evidence**: `docs/demo_evidence_v1_1/v1_1_sci_limitations.md` — 8 limitations listed; manuscript contains 7 in the main text.

**Limitations Coverage**:

| # | Limitation | Severity | Reviewer Impact |
|---|-----------|----------|-----------------|
| 1 | Semi-real traces are not enterprise production logs | High | Major — most likely reviewer concern |
| 2 | Affective pressure is structured annotations, not real emotion recognition | High | Major — boundary on affective computing claims |
| 3 | Experience memory's optimal intensity requires further calibration | Medium | Moderate — acknowledges parameter sensitivity |
| 4 | Accumulated memory causes severe over-caution collapse | Medium | Moderate — but demonstrates awareness of failure mode |
| 5 | Current results prove safety calibration, not general affective intelligence | High | Major — preempts overclaiming |
| 6 | RiskContextOracleBaseline is a diagnostic upper bound, not a competitor | Low | Minor — prevents misinterpretation |
| 7 | Limited generalizability across platforms, domains, and languages | High | Major — standard limitation for controlled benchmarks |
| 8 | No external validation from real deployments | High | Major — complements Limitation 1 |

**Assessment**:

- The limitations section is comprehensive and honest, covering the key weaknesses that reviewers would identify.
- Limitations 1, 2, 5, 7, and 8 directly address the most likely reviewer objections.
- Limitation 4 (over-caution collapse) is a strength disguised as a limitation — it demonstrates thorough analysis of failure modes.
- Limitation 6 (oracle baseline) prevents a common misinterpretation.
- The limitations are specific and actionable, not generic filler.

**Risk Level**: Low. The limitations section is above-average in honesty and specificity for an SCI submission.

---

## Item 7: Blind Version

**Status**: ⚠️ ACTION REQUIRED

**Evidence**: `manuscript_v0_3_blind.md` — **file does not exist** as of assessment date.

**Assessment**:

- The blind version is listed as a required submission artifact but has not yet been created.
- Based on the revision checklist pattern (v0_2 → v0_3), the blind version should be derived from the latest manuscript with the following modifications:
  - Remove all author names and affiliations
  - Remove all GitHub URLs and repository links
  - Remove any identifying information in acknowledgments
  - Replace self-referential citations with anonymized format (e.g., "Author, 2026" or "[Anonymous]")
  - Remove any institutional identifiers in funding statements

**Action Required**:

| # | Task | Priority |
|---|------|----------|
| 1 | Create `manuscript_v0_3_blind.md` from the latest manuscript version | HIGH |
| 2 | Verify zero author-identifying information remains | HIGH |
| 3 | Test by searching for author names, institution names, GitHub URLs, and project-specific identifiers | HIGH |

**Risk Level**: Medium. This is a blocking requirement for double-anonymous submission venues. Must be completed before submission.

---

## Item 8: Overclaim Check

**Status**: ✅ PASS (with 1 minor cleanup item)

**Evidence**: Project-wide search in `numeric_consistency_audit_v0_3.md` (Sections 4–5).

**Prohibited Claim Categories**:

| Claim Category | Found in Manuscript? | Found in Supporting Docs? | Status |
|---------------|---------------------|--------------------------|--------|
| "Emotional intelligence" (positive claim) | No | No | ✅ Clean |
| "Production validation" (positive claim) | No | No | ✅ Clean |
| "State-of-the-art" | No | No | ✅ Clean |
| "General agent safety" | No | No | ✅ Clean |
| RiskContextOracleBaseline as competitor | No — clearly marked as oracle/diagnostic | No | ✅ Clean |

**Minor Issue**:

| # | File | Line | Issue | Action |
|---|------|------|-------|--------|
| 1 | `related_work_v0_3.md` | L19 | Uses exact phrase "emotional intelligence" in a negative disclaimer ("nor do we claim that our agent possesses emotional intelligence") | Rephrase to avoid the exact prohibited phrase, e.g., "nor do we claim that our agent possesses general affective understanding" — only if this text is incorporated into the manuscript |

**Assessment**:

- The manuscript itself is clean of all prohibited claims.
- All "production validation" occurrences are explicit disclaimers, not positive claims.
- The RiskContextOracleBaseline is consistently labeled as an oracle/diagnostic upper bound across all documents.
- The `data_authenticity_statement.md` explicitly lists 5 claims the paper does NOT make.
- The `dataset_card.md` lists 4 inappropriate uses that should not be claimed.

**Risk Level**: Low. The manuscript is clean; the minor issue in `related_work_v0_3.md` only matters if that text is incorporated into the final manuscript.

---

## Item 9: LLM Baseline

**Status**: ⚠️ ACKNOWLEDGED GAP (design exists, not implemented)

**Evidence**: `optional_llm_baseline_design.md`

**Assessment**:

- A thorough design document exists for an `LLMSafetyJudgeBaseline` that would compare the rule-based calibrator against an LLM-based safety classifier.
- The design is well-considered: it defines input/output schema, prompt template with few-shot examples, evaluation protocol (3 runs, temperature=0, McNemar comparison), cost estimate ($9.45 for 3 GPT-4 runs), leakage prevention rules, and risk assessment.
- The design explicitly states "DO NOT IMPLEMENT" without explicit reviewer request and author consensus.
- The design document anticipates two scientifically informative outcomes (LLM performs well → validates benchmark; LLM performs poorly → validates structured calibration).
- The design addresses the most natural reviewer question: "Why not just use an LLM to judge safety?"

**Gap Analysis**:

| Dimension | With LLM Baseline | Without LLM Baseline |
|-----------|-------------------|---------------------|
| Reviewer defense | Strong — directly answers "why not just use an LLM?" | Moderate — must argue conceptually |
| Experimental completeness | Full spectrum (rule-based → neural → oracle) | Gap between rule-based baselines and oracle |
| Risk of revision request | Lower | Moderate — likely to be requested |
| Implementation cost | ~$10 + 1–2 days | $0 |
| Contamination risk | Present (LLM training data) | None |

**Recommendation**:

- **For initial submission**: Mention the LLM baseline design in the paper's limitations or future work section, noting that it is a planned comparison. This signals awareness without requiring implementation.
- **For revision**: If reviewers request the LLM baseline, the design document provides a complete implementation plan that can be executed within 1–2 days.
- **Alternative**: Include a brief appendix paragraph describing the designed LLM baseline and explaining why it was deferred (cost, contamination risk, scope), which proactively addresses the concern.

**Risk Level**: Medium. The absence of an LLM baseline is the most likely trigger for a "major revision" decision. However, the design document and a well-crafted limitations/future-work mention can mitigate this risk.

---

## Item 10: Recommended Submission Venues

**Status**: ✅ ASSESSED

### Venue Risk–Benefit Analysis

#### Tier 1: EI-Indexed Journals (Low Risk, Moderate Prestige)

| Venue | Scope Fit | Risk Tolerance for Synthetic Data | LLM Baseline Expectation | Overall Risk |
|-------|-----------|----------------------------------|--------------------------|-------------|
| Journal of Intelligent Information Systems | High — agent safety, tool governance | Moderate — accepts controlled benchmarks | Moderate | Low–Medium |
| AI and Ethics | Moderate — ethical dimensions of agent safety | High — values transparency and limitations | Low | Low |
| Intelligent Systems with Applications | High — applied AI safety | High — application-oriented | Low | Low |

#### Tier 2: SCI Q3 Journals (Moderate Risk, Good Prestige)

| Venue | Scope Fit | Risk Tolerance for Synthetic Data | LLM Baseline Expectation | Overall Risk |
|-------|-----------|----------------------------------|--------------------------|-------------|
| Journal of Intelligent Information Systems (Q3) | High | Moderate | Moderate | Medium |
| Knowledge-Based Systems (Q2–Q3 boundary) | Moderate — requires stronger novelty framing | Low–Moderate | High | Medium–High |
| Information Processing & Management (Q2–Q3) | Low–Moderate — information retrieval focus | Low | High | High |

#### Tier 3: SCI Q2 Journals (Higher Risk, Higher Prestige)

| Venue | Scope Fit | Risk Tolerance for Synthetic Data | LLM Baseline Expectation | Overall Risk |
|-------|-----------|----------------------------------|--------------------------|-------------|
| ACM Transactions on Intelligent Systems and Technology (ACM TOIT) | High — intelligent systems | Low | High | High |
| Artificial Intelligence Review | Moderate — requires broad impact framing | Low | High | High |
| Neural Computing and Applications | Moderate — requires neural component emphasis | Moderate | High | Medium–High |

### Paper Strengths and Weaknesses Summary

**Strengths**:

1. **Novel mechanism**: Experience-shaped affective safety calibration is a genuinely novel contribution that bridges affective computing and agent safety — no prior work combines these two domains.
2. **Controlled evaluation**: Two benchmarks (500 total cases), 5 baselines, 6 ablations, longitudinal memory experiment — above-average experimental rigor for Q3.
3. **Reproducible**: 290/290 tests pass, all results reproducible from code, full numeric consistency audit.
4. **Honest limitations**: 7–8 explicit limitations, data authenticity statement, overclaim checks — demonstrates scientific maturity.
5. **Statistical rigor**: Bootstrap 95% CI, McNemar paired comparisons, effect sizes — meets SCI statistical standards.

**Weaknesses**:

1. **Synthetic data only**: No real deployment validation — the single most likely reviewer objection.
2. **No LLM baseline**: The gap between rule-based baselines and the oracle leaves a modern neural baseline missing.
3. **Domain specificity**: Results are limited to software development and tool-use scenarios; generalizability is untested.
4. **Structured signals**: Affective pressure and risk context are provided as structured annotations, not inferred from natural language — limits real-world applicability claims.

### Venue Recommendation

| Priority | Venue | Rationale |
|----------|-------|-----------|
| **1st Choice** | Journal of Intelligent Information Systems (SCI Q3) | Best scope fit (agent safety, tool governance), moderate tolerance for synthetic data, EI-indexed backup. The paper's novelty and reproducibility are strong selling points for this venue. |
| **2nd Choice** | AI and Ethics | High tolerance for transparent limitations, values ethical dimensions of safety, lower LLM baseline expectation. The paper's honest limitations and data authenticity statement align with this venue's values. |
| **3rd Choice** | Intelligent Systems with Applications | Application-oriented venue that values practical safety mechanisms, lower bar for real-world validation. |
| **Backup** | EI-indexed venues (if SCI rejection) | Lower prestige but higher acceptance probability; useful for establishing publication record before resubmitting to SCI venues. |

**Overall Strategy**: Target SCI Q3 journals first, with EI-indexed venues as fallback. Do not target Q2 journals in this submission cycle — the synthetic-data-only limitation and missing LLM baseline make Q2 acceptance unlikely without revision. After gaining reviewer feedback from Q3 submission (which may request the LLM baseline), implement the LLM baseline and resubmit to a Q2 venue with strengthened evidence.

---

## Overall Readiness Score

| Item | Weight | Score (0–10) | Weighted Score |
|------|--------|-------------|----------------|
| 1. Verified References | 10% | 9.5 | 0.95 |
| 2. Figures | 10% | 10.0 | 1.00 |
| 3. Data Authenticity Statement | 10% | 10.0 | 1.00 |
| 4. Dataset Card | 8% | 10.0 | 0.80 |
| 5. Reproducibility Audit | 12% | 9.5 | 1.14 |
| 6. Limitations | 10% | 9.0 | 0.90 |
| 7. Blind Version | 10% | 0.0 | 0.00 |
| 8. Overclaim Check | 10% | 9.5 | 0.95 |
| 9. LLM Baseline | 10% | 4.0 | 0.40 |
| 10. Venue Assessment | 10% | 9.0 | 0.90 |
| **Total** | **100%** | | **8.04 / 10** |

### **Overall Readiness Score: 80.4%**

**Interpretation**: The paper is substantially ready for submission but has two blocking/semi-blocking issues that must be addressed before the submission packet is complete.

---

## Top 3 Action Items Before Submission

### 1. Create the Double-Anonymous Manuscript Version (Blocking)

**Priority**: HIGH | **Effort**: Low (2–4 hours) | **Impact**: Blocking for double-anonymous venues

- Generate `manuscript_v0_3_blind.md` from the latest manuscript.
- Remove all author names, affiliations, GitHub URLs, repository links, and institutional identifiers.
- Replace self-referential citations with anonymized format.
- Verify by searching for: author names, institution names, "github.com", project-specific identifiers.
- This is a hard requirement — submission cannot proceed without it.

### 2. Resolve the Unverified Reference (Semi-Blocking)

**Priority**: HIGH | **Effort**: Low (30 minutes) | **Impact**: Reviewer credibility

- Verify [15] ToolSafe (Mou et al. 2026), arXiv:2601.10156.
- Confirm whether this preprint has been accepted at a peer-reviewed venue or remains an arXiv-only preprint.
- If unverified: either replace with an alternative verified reference on step-level safety guardrails, or retain with an explicit "preprint" label in the manuscript's reference list.
- A single unverified reference can undermine reviewer trust in the entire reference list.

### 3. Add LLM Baseline Mention to Limitations or Future Work (Recommended)

**Priority**: MEDIUM | **Effort**: Low (1–2 hours) | **Impact**: Preemptive reviewer defense

- Add a paragraph to the manuscript's limitations or future work section acknowledging that an LLM-based safety classifier baseline was designed but not implemented in this paper cycle.
- Briefly describe the design (LLM judge with natural-language-only input vs. structured calibration signals) and explain why it was deferred (scope, contamination risk, cost).
- State that this comparison is planned as future work.
- This does not require running the LLM baseline — it signals awareness and preempts the most likely reviewer objection.

---

## Recommended Next Steps

### Immediate (Before Submission)

1. **Create `manuscript_v0_3_blind.md`** — blocking requirement.
2. **Verify or replace reference [15]** — semi-blocking credibility issue.
3. **Add LLM baseline mention** to limitations/future work — defensive writing.
4. **Fix residual error** in `materials_for_manuscript_v0_1.md` L300 (0.624 → 0.872, 93.6% → 95.9%) — project hygiene.
5. **Rephrase "emotional intelligence"** in `related_work_v0_3.md` L19 if that text is incorporated into the manuscript — prohibited phrase avoidance.
6. **Final numeric consistency sweep** — search project-wide for `0.624`, `93.6`, `emotional intelligence`, and `production validation` to confirm zero active residuals in submission artifacts.

### During Review Period

7. **Implement the LLM baseline** following `optional_llm_baseline_design.md` — be prepared for reviewer request.
8. **Draft a real-world validation plan** — outline how production deployment validation would be conducted, even if not executed in this paper cycle.
9. **Prepare supplementary materials** — full prompt template for LLM baseline, additional ablation results, per-category error analysis.

### After First Review Cycle

10. **If LLM baseline is requested**: Implement and add results (1–2 days of work, ~$10 API cost).
11. **If real-world validation is requested**: Consider a small-scale pilot study with a coding assistant platform.
12. **If accepted at Q3**: Use the publication record and reviewer feedback to strengthen a Q2 resubmission with the LLM baseline and any additional experiments.

---

*End of submission readiness checklist.*
