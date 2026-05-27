# Figure Captions

## Figure 1

**Figure 1.** Overview of the proposed experience-shaped affective safety calibration framework. Structured affective pressure and bounded experience memory are used as auxiliary calibration signals rather than real-time emotion recognition outputs. The three-tier SafeActionCalibrator evaluates strict risk context before safe keywords, preventing dangerous actions from being auto-executed due to the presence of safe-sounding verbs.

## Figure 2

**Figure 2.** Three-tier calibration policy with strict context priority. Tier 1 (Strict Review) is evaluated first: if any destructive, sensitive, security-related, irreversible, or production context is detected, the action is routed to human review or blocked. Tier 2 (Safe Auto-Execute) applies only when a safe verb is present and no Tier 1 context is matched. Tier 3 (Ambiguous Default Cautious) handles all remaining cases with simulation-first verification. The priority order ensures that safe keywords cannot override risk context.

## Figure 3

**Figure 3.** Risky auto-execution rate comparison across methods on the Affective-Agent-Safety-300 semi-real benchmark (N=300). FullCalibratorAdapter achieves 3.6% risky auto-execution, below the 5% target threshold (dashed red line). SafeKeywordFirstBaseline and KeywordRuleBaseline exhibit catastrophically high risky auto-execution rates (87.2% and 78.0% respectively), demonstrating the danger of evaluating safe keywords before risk context. RiskContextOracleBaseline (marked with asterisk) is a structured oracle that directly reads risk context from the benchmark; it is not a deployable method and is included only as an upper-bound diagnostic reference.

## Figure 4

**Figure 4.** Longitudinal experience memory trade-off across three configurations on the Affective-Agent-Safety-300 benchmark. Single-failure memory achieves the best safety-utility balance: 16.3% lower risky auto-execution than no memory (3.6% vs 4.3%) while maintaining identical safe auto-execution accuracy (0.757). Accumulated failure memory eliminates risky auto-execution entirely (0.000) but causes over-caution collapse, reducing safe auto-execution accuracy to 0.000. This demonstrates that bounded, calibrated experience memory is preferable to unbounded accumulation.
