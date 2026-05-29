# Submission Pack v0.4 — Teacher Review Pack

**Date**: 2026-05-28
**Q2 Readiness**: BORDERLINE+
**Recommendation**: Q2 cautious attempt / Q3 safer route

---

## 1. File List

| # | File | Category | Description |
|---|------|----------|-------------|
| 1 | manuscript_v0_4_q2_attempt_final_review.md | **Main manuscript** | Final review manuscript with all sections |
| 2 | manuscript_v0_4_q2_attempt_blind_final_review.md | **Blind manuscript** | Anonymous final review version for double-blind peer review |
| 3 | teacher_review_checklist.md | **Review** | Teacher review checklist for v0.4 final submission pack |
| 4 | final_review_pack_acceptance_report.md | **Review** | Final review pack acceptance report |
| 5 | cover_letter_draft.md | **Submission** | Cover letter for journal submission |
| 6 | 论文投稿说明_中文.md | **Submission** | Chinese submission guide for advisor review |
| 7 | q2_submission_strategy.md | **Strategy** | Q2/Q3 submission strategy |
| 8 | q2_acceptance_gate.md | **Audit** | Acceptance gate status report |
| 9 | phase5_acceptance_audit.md | **Audit** | Phase 5 acceptance audit results |
| 10 | dataset_equivalence_audit_full300.md | **Audit** | Dataset equivalence audit for LLM baseline |
| 11 | llm_baseline_full300_report.md | **Supplementary** | DeepSeek-v4-flash 300-case stress test report |
| 12 | q2_blocker_closure_report.md | **Audit** | Q2 blocker closure status |
| 13 | annotation_reliability_pending_report.md | **Supplementary** | Annotation reliability pending report |
| 14 | annotation_protocol_v1.md | **Supplementary** | Annotation protocol for independent annotators |
| 15 | data_authenticity_statement.md | **Evidence** | Data origin and authenticity declaration |
| 16 | dataset_card.md | **Evidence** | Dataset documentation (schema, labels, limitations) |
| 17 | reproducibility_audit.md | **Evidence** | Reproducibility audit (commands, results, seeds) |
| 18 | references_final.md | **Evidence** | 38 verified final references |
| 19 | references_verified.md | **Evidence** | 50 verified references with DOI/arXiv (38 verified, 12 removed) |
| 20 | references_verification_audit.md | **Evidence** | References verification audit log |
| 21 | references_removed_or_unverified.md | **Evidence** | 12 removed/unverified references |
| 22 | figure_captions.md | **Evidence** | Captions for all 4 figures |
| 23 | final_sanity_check_v0_3.md | **Evidence** | Final sanity check (prohibited phrases, consistency) |
| 24 | numeric_consistency_audit_v0_3.md | **Evidence** | Numeric consistency cross-check |
| 25 | figures/ | **Figures** | 4 figures (PNG + PDF each) |
| 26 | manuscript_v0_4_q2_attempt.md | **Legacy manuscript** | Pre-review manuscript version |
| 27 | manuscript_v0_4_q2_attempt_blind.md | **Legacy blind** | Pre-review blind manuscript version |

---

## 2. Which is the Main Manuscript?
**manuscript_v0_4_q2_attempt_final_review.md** — the final review manuscript with all sections, tables, caveats, and verified references.

---

## 3. Which is the Blind Manuscript?
**manuscript_v0_4_q2_attempt_blind_final_review.md** — anonymous final review version with model names replaced by generic descriptions, suitable for double-blind peer review.

---

## 4. Supplementary Materials
| File | Content |
|------|---------|
| llm_baseline_full300_report.md | DeepSeek-v4-flash 300-case LLM stress test results |
| annotation_reliability_pending_report.md | Annotation reliability status and preparation |
| annotation_protocol_v1.md | Protocol for independent second annotator |

---

## 5. Audit Materials
| File | Content |
|------|---------|
| phase5_acceptance_audit.md | Phase 5 acceptance audit (PASS) |
| dataset_equivalence_audit_full300.md | Dataset equivalence audit (PARTIALLY COMPARABLE) |
| q2_acceptance_gate.md | Acceptance gate status (BORDERLINE+) |
| q2_blocker_closure_report.md | Q2 blocker closure status |
| reproducibility_audit.md | Reproducibility audit (commands, seeds, result files) |
| numeric_consistency_audit_v0_3.md | Numeric consistency cross-check across all reported values |
| final_sanity_check_v0_3.md | Prohibited phrases cleanup and completeness verification |

---

## 6. Evidence Materials
| File | Content |
|------|---------|
| data_authenticity_statement.md | Data origin, nature, and authenticity declaration |
| dataset_card.md | Dataset documentation (names, schema, labels, intended use, limitations) |
| references_final.md | 38 verified final references used in manuscript |
| references_verified.md | Full verification status of all 50 original references |
| references_verification_audit.md | Audit log of reference verification process |
| references_removed_or_unverified.md | 12 references removed due to unverifiable DOI/arXiv |
| figure_captions.md | Captions for Figures 1–4 |

---

## 7. Figures
| Figure | File | Description |
|--------|------|-------------|
| Fig 1 | figures/fig1_framework_architecture.png/.pdf | Framework architecture overview |
| Fig 2 | figures/fig2_three_tier_policy.png/.pdf | Three-tier safety decision policy |
| Fig 3 | figures/fig3_risky_auto_exec_comparison.png/.pdf | Risky auto-execution rate comparison |
| Fig 4 | figures/fig4_longitudinal_memory_tradeoff.png/.pdf | Longitudinal memory tradeoff |

---

## 8. Files for Advisor Review
- 论文投稿说明_中文.md — Chinese overview for advisor
- manuscript_v0_4_q2_attempt_final_review.md — Final review manuscript
- teacher_review_checklist.md — Review checklist
- final_review_pack_acceptance_report.md — Acceptance report
- q2_acceptance_gate.md — Readiness assessment
- q2_submission_strategy.md — Submission strategy
- data_authenticity_statement.md — Data authenticity declaration
- dataset_card.md — Dataset documentation

---

## 9. Files for Journal Submission
- manuscript_v0_4_q2_attempt_blind_final_review.md — Blind final review manuscript (for double-blind review)
- manuscript_v0_4_q2_attempt_final_review.md — Non-blind final review manuscript (if single-blind)
- cover_letter_draft.md — Cover letter
- figures/ — All figures (PNG + PDF)
- figure_captions.md — Figure captions

---

## 10. Research Limitations

The following are genuine research limitations, not missing files:

| Limitation | Status |
|------------|--------|
| Annotation kappa pending | Independent second annotation not yet completed; Cohen's kappa not reported |
| No real enterprise deployment traces | No production or real-world deployment data available |
| No real-world deployment evidence | Generalization limited to simulated/semi-real benchmarks |
| No independent annotation result | Annotation package prepared but not yet executed by second annotator |
| DeepSeek full-300 is auxiliary stress test | DeepSeek-v4-flash results are on regenerated AffectiveBenchmark-300, not directly comparable to Semi-Real-300 |
