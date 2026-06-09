# Q2 Submission Strategy

> **Deprecated historical draft.** The claims in this file were written before the Phase 0–1R audit. Do not treat Semi-Real-300, Q2 BORDERLINE+, or the old main-table metrics as current reproducible evidence.

**Date**: 2026-05-28
**Readiness**: BORDERLINE+
**Recommendation**: Cautious Q2 attempt with Q3 fallback

---

## Overall Strategy
This manuscript is positioned as a **cautious Q2 attempt** with Q3 as a safer submission route. The key differentiator is that we include a real LLM baseline (though not on the exact same benchmark) and complete dataset equivalence audit, significantly strengthening the submission.

---

## Target Journals
### Q2 Options
- [list Q2 journal options]

### Q3 Options (Fallback)
- [list Q3 journal options]

---

## Key Strengths
1. Real LLM baseline (DeepSeek-v4-flash) 300-case stress test
2. Complete dataset equivalence audit (no hidden sampling bias)
3. Failure taxonomy
4. Data authenticity pack
5. Reproducibility audit
6. Blind version prepared
7. Annotation package ready

---

## Key Cautions
1. LLM baseline not on exact same Semi-Real-300 (clearly documented as stress test)
2. Annotation kappa still pending
3. No real enterprise data
4. No external-style dataset validation

---

## Manuscript Structure Guidance
### MUST FOLLOW
- Main table ONLY Semi-Real-300 results
- LLM stress test in its own separate section
- Explicit dataset equivalence caveat
- Explicit annotation reliability pending statement
- NO absolute claims about LLM judges being worse overall
- NO production validation claims

---

## Review Risk Mitigation
1. Preempt reviewer question about benchmark inconsistency by putting the caveat early
2. Position LLM stress test as an auxiliary analysis, not core comparison
3. Highlight reproducibility
4. Be honest about limitations

---

## Next Steps Before Submission
1. Generate references section
2. Double-check prohibited phrases
3. Complete abstract polishing
4. Consider adding an ablation study if time

---

## Fallback to Q3
If Q2 reviewers raise issues about benchmark equivalence or annotation reliability, this work is still strong enough for Q3 submission without major changes.

