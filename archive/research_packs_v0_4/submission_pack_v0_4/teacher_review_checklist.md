# Teacher Review Checklist: v0.4 Final Submission Pack

**Date**: 2026-05-28  
**Pack Status**: Q2 cautious attempt (Q3 as safer fallback)

---

## 1. Paper Positioning
- [ ] Q2 cautious attempt
- [ ] Q3 safer route (primary fallback)

---

## 2. Completed Materials (✅ Present)

### Manuscripts
- [x] manuscript_v0_4_q2_attempt_final_review.md (full author version)
- [x] manuscript_v0_4_q2_attempt_blind_final_review.md (anonymous version)

### Supporting Evidence
- [x] figures/ directory with 4 figures (PNG + PDF each)
- [x] figure_captions.md
- [x] data_authenticity_statement.md
- [x] dataset_card.md
- [x] reproducibility_audit.md
- [x] numeric_consistency_audit_v0_3.md
- [x] final_sanity_check_v0_3.md
- [x] references_final.md (38 verified references)
- [x] references_verification_audit.md
- [x] references_removed_or_unverified.md

### Supplementary Materials
- [x] annotation_protocol_v1.md
- [x] annotation_reliability_pending_report.md
- [x] dataset_equivalence_audit_full300.md
- [x] llm_baseline_full300_report.md

### Administrative
- [x] cover_letter_draft.md
- [x] README.md (no file gaps)
- [x] 论文投稿说明_中文.md
- [x] q2_submission_strategy.md
- [x] q2_acceptance_gate.md
- [x] phase5_acceptance_audit.md
- [x] q2_blocker_closure_report.md

---

## 3. Items Requiring Teacher Judgment

### Dataset Boundary Acceptance
- [ ] Accept semi-real/regenerated benchmark distinction
- [ ] Accept that DeepSeek stress test is auxiliary only
- [ ] Accept no direct comparison between the two

### Annotation Reliability
- [ ] Accept "annotation pending" (no Cohen's kappa)
- [ ] Accept that blind annotation package is prepared but not executed
- [ ] Recommendation: find second annotator?

### Submission Strategy
- [ ] Prioritize Q2 cautious attempt
- [ ] Prioritize Q3 safer route
- [ ] Wait for annotation completion before submission

### References
- [ ] Verify references_final.md (38 entries)
- [ ] Check if any removed references should be restored
- [ ] Double-check arXiv/DOIs before submission

---

## 4. Three-Sentence Summary for Teacher
1. This paper is about affective safety calibration for autonomous agents—not emotional intelligence—and it uses the semi-real Affective-Agent-Safety-300 benchmark for the main experiments.
2. The FullCalibratorAdapter achieves 0.753 accuracy and 0.036 risky auto-execution rate, with 95.9% relative reduction vs SafeKeywordFirstBaseline.
3. The DeepSeek-v4-flash judge was tested on a separate regenerated AffectiveBenchmark-300 stress set (not Semi-Real-300) and shows extreme over-escalation, highlighting the need for structured calibration.

---

## 5. Known Hard Limitations (Cannot Fix Right Now)
- No independent annotation result
- No real-world enterprise deployment traces
- Semi-Real-300 source JSON not available in repo
- Cannot re-run original main method experiments from code
