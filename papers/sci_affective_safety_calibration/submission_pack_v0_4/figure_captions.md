# Figure Captions

**Date**: 2026-05-28
**Version**: v0.4
**Paper**: Experience-Shaped Affective Safety Calibration for Autonomous Agents

---

## Figure 1: Framework Architecture

**File**: `figures/fig1_framework_architecture.png` / `.pdf`

**Caption**:
Overview of the proposed affective safety calibration framework. The system comprises three core components: (1) a Cognitive Appraisal Vector that evaluates consequences along dimensions of controllability, source, and risk type; (2) an Affective Memory module that stores severity-weighted experience traces with similarity-based generalization and interoceptive self-state tracking; and (3) a Hesitation Policy that selects intermediate actions (simulate, escalate, or block) for high-conflict scenarios. The Cognitive Appraisal Vector feeds into the Affective Memory, which in turn modulates the Hesitation Policy's decision threshold, enabling experience-shaped safety calibration.

---

## Figure 2: Three-Tier Policy Architecture

**File**: `figures/fig2_three_tier_policy.png` / `.pdf`

**Caption**:
The three-tier safety decision policy. Tier 1 (Auto-Execute) applies to low-risk operations (e.g., read-only queries, safe configuration checks) where the agent proceeds without additional verification. Tier 2 (Simulate-First) applies to moderate-risk operations (e.g., configuration changes, dependency updates) where a dry-run or preview is required before execution. Tier 3 (Human-Review / Block) applies to high-risk and critical operations (e.g., irreversible file deletions, production database modifications) where human approval is mandatory or the operation is blocked entirely. The threshold between tiers is dynamically adjusted by the Affective Memory module based on accumulated experience.

---

## Figure 3: Risky Auto-Execution Rate Comparison

**File**: `figures/fig3_risky_auto_exec_comparison.png` / `.pdf`

**Caption**:
Comparison of risky auto-execution rates across methods on the Affective-Agent-Safety-300 benchmark. The FullCalibratorAdapter achieves a risky auto-execution rate of 0.036 (3.6%), representing a 95.9% relative reduction compared to the SafeKeywordFirstBaseline (0.872, 87.2%). The KeywordRuleBaseline exhibits a risky auto-execution rate of 0.780 (78.0%). The RiskContextOracleBaseline (non-deployable diagnostic reference) achieves 0.064 (6.4%). The DeepSeek-v4-flash zero-shot LLM judge on the auxiliary AffectiveBenchmark-300 stress set achieves 0.000 (0%) but at the cost of 92.35% false caution. Lower values indicate better safety performance.

---

## Figure 4: Longitudinal Memory Tradeoff

**File**: `figures/fig4_longitudinal_memory_tradeoff.png` / `.pdf`

**Caption**:
Longitudinal analysis of risky auto-execution rate under different memory configurations. The no-memory condition maintains a risky auto-execution rate of 0.043 throughout evaluation. The single-failure memory condition reduces the rate to 0.036 after one failure experience. The accumulated-experience condition further reduces the rate to 0.000 as the agent accumulates failure traces across multiple episodes. This demonstrates that experience-shaped memory enables progressive safety improvement, though at the potential cost of increased false caution in later episodes. The tradeoff between safety improvement and operational utility is a key consideration for deployment.
