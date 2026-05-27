# Verified References

## Experience-Shaped Affective Safety Calibration for Autonomous Agents

---

## Category 1: Tool-Using LLM Agents

[1] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR 2023*. arXiv:2210.03629

**Relevance:** Foundational agent architecture that interleaves reasoning and acting. Our framework extends the ReAct loop by injecting affective pressure signals at each reasoning step, enabling risk-context-aware action selection rather than purely logical inference.

[2] Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. *NeurIPS 2023 (Oral)*. arXiv:2302.04761

**Relevance:** Demonstrates that LLMs can autonomously learn when and how to invoke external tools. Our work addresses the safety gap: Toolformer optimizes for task utility, while our affective calibration layer modulates tool invocation willingness under risk, preventing unsafe tool use that purely utility-driven agents would execute.

[3] Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J., Chen, Z., Tang, J., Chen, X., Lin, Y., Zhao, W.X., Wei, Z., & Wen, J. (2024). A Survey on Large Language Model Based Autonomous Agents. *Frontiers of Computer Science*. DOI:10.1007/s11704-024-40231-1

**Relevance:** Comprehensive taxonomy of LLM agent architectures, including memory, planning, and action modules. Our three-tier framework (risk context priority, affective pressure, experience memory) maps onto and extends the module taxonomy described here, particularly the memory and profiling components.

[4] Park, J.S., O'Brien, J., Cai, C.J., Morris, M.R., Liang, P., & Bernstein, M.S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST 2023*. arXiv:2304.03442

**Relevance:** Introduces a memory stream architecture for agents that retrieves and reflects on past experiences to guide behavior. Our experience memory component shares the retrieval-reflection pattern but is specifically designed for safety calibration: stored near-miss episodes are prioritized to shape future risk sensitivity.

[5] Qin, Y., Hu, S., Lin, Y., Chen, W., Ding, N., Cui, G., Zeng, Z., Feng, Y., Zhao, Y., Zhang, T., et al. (2024). ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs. *ICLR 2024*. arXiv:2307.16789

**Relevance:** Scales tool-use evaluation to thousands of real-world APIs. Our benchmarks (Agent-SafetyBench and AffectiveSafety) complement ToolLLM's utility-focused evaluation by introducing safety-oriented test cases where tool invocation should be refused or deferred, demonstrating that API mastery alone is insufficient without safety calibration.

[6] Shen, Y., Song, K., Tan, X., Li, D., Lu, W., & Zhuang, Y. (2024). HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face. *Computational Linguistics*. arXiv:2303.17580

**Relevance:** Presents a cascaded agent architecture where an LLM orchestrates multiple specialized models. Our affective pressure mechanism is particularly relevant for such multi-model pipelines: a risk signal generated at the orchestrator level can propagate downstream to gate unsafe model invocations, preventing cascading failures.

[7] Nakano, R., Hilton, J., Balaji, S., Wu, J., Ouyang, L., Kim, C., Hesse, C., Jain, S., Kosaraju, V., Saunders, W., et al. (2022). WebGPT: Browser-assisted question-answering with human feedback. arXiv:2112.09332

**Relevance:** Demonstrates that human feedback can shape agent browsing behavior. Our framework generalizes this principle: instead of post-hoc human feedback, we use structured affective pressure as an in-situ auxiliary signal that calibrates agent behavior in real time, reducing the need for expensive human annotation loops.

---

## Category 2: Agent Safety / AI Safety / Tool Governance

[8] Zhang, Z., Cui, S., Lu, Y., Zhou, J., Yang, J., Wang, H., & Huang, M. (2024). Agent-SafetyBench: Evaluating the Safety of LLM Agents. arXiv:2412.14470

**Relevance:** Primary benchmark for evaluating our framework. Agent-SafetyBench provides 349 environments and 2000+ test cases across multiple risk categories. We use it as one of our two evaluation benchmarks to demonstrate that affective calibration reduces risky auto-execution while preserving task completion rates.

[9] Xie, Y., Yuan, Y., Wang, W., Mo, F., Guo, J., & He, P. (2025). ToolSafety: A Comprehensive Dataset for Enhancing Safety in LLM-Based Agent Tool Invocations. *EMNLP 2025*. DOI:10.18653/v1/2025.emnlp-main.714

**Relevance:** Provides a taxonomy of unsafe tool invocations (e.g., data leakage, unauthorized access, harmful content generation). Our risk context priority tier directly operationalizes ToolSafety's taxonomy by assigning higher priority to risk-context signals over safe-keyword heuristics that agents might otherwise rely on.

[10] Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J., Jones, A., Chen, A., Goldie, A., Mirhoseini, A., McKinnon, C., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073

**Relevance:** Proposes rule-based self-correction via constitutional principles. Our framework differs in a key aspect: rather than static constitutional rules, we use dynamically calibrated affective pressure that adjusts based on situational risk and accumulated experience, enabling more nuanced safety decisions than binary rule compliance.

[11] Hua, W., Yang, X., Jin, M., Li, Z., Cheng, W., Tang, R., & Zhang, Y. (2024). TrustAgent: Towards Safe and Trustworthy LLM-based Agents. *EMNLP 2024 Findings*. arXiv:2312.06698

**Relevance:** Introduces trust-aware agent design with safety constraints. Our affective pressure mechanism complements TrustAgent's trust framework: while TrustAgent models trust as a static property, our affective calibration treats trust as a dynamic, experience-shaped variable that can collapse under risk and recover through safe interactions.

[12] Miculicich, L., Parmar, M., Palangi, H., Dj Dvijotham, K., Montanari, M., Pfister, T., & Le, L.T. (2025). VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation. arXiv:2510.05156

**Relevance:** Uses formal verification to ensure agent-generated code is safe. Our approach is complementary: VeriGuard provides hard guarantees on code safety, while our affective calibration provides soft, experience-shaped risk modulation that operates at the decision level before code is generated, potentially reducing the burden on downstream verification.

[13] Zhang, H., Huang, J., Mei, K., Yao, Y., Wang, Z., Zhan, C., Wang, H., & Zhang, Y. (2025). Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents. *ICLR 2025*. arXiv:2410.02644

**Relevance:** Formalizes attack surfaces specific to LLM agents (prompt injection, tool misuse, data exfiltration). Our affective pressure signals serve as a defense mechanism against these attack vectors: elevated affective pressure under adversarial conditions triggers hesitation or escalation, providing a proactive safety layer distinct from ASB's reactive defenses.

[14] Xia, H., Wang, H., Liu, Z., Yu, Q., Guo, Y., & Wang, H. (2025). SafeToolBench: Pioneering a Prospective Benchmark to Evaluating Tool Utilization Safety in LLMs. arXiv:2509.07316

**Relevance:** Evaluates whether LLMs can distinguish safe from unsafe tool uses. Our framework addresses a limitation identified in SafeToolBench: agents that rely on safe-keyword matching fail on context-dependent risks. Our risk context priority tier explicitly overrides safe-keyword heuristics when contextual risk signals are present.

[15] Mou, Y., Xue, Z., Li, L., Liu, P., Zhang, S., Ye, W., & Shao, J. (2026). ToolSafe: Enhancing Tool Invocation Safety of LLM-based agents via Proactive Step-level Guardrail and Feedback. arXiv:2601.10156

**Relevance:** Proposes step-level guardrails for tool invocation safety. Our affective calibration shares the step-level intervention philosophy but differs in mechanism: ToolSafe uses explicit guardrail rules, while our affective pressure operates as a continuous auxiliary signal that modulates action propensity, enabling smoother and more context-sensitive safety adjustments. *(needs verification — 2026 arXiv ID; confirm publication status)*

---

## Category 3: Human-in-the-Loop AI

[16] Lazaros, K., Vrahatis, A.G., & Kotsiantis, S. (2026). Human-in-the-Loop Artificial Intelligence: A Systematic Review of Concepts, Methods, and Applications. *Entropy*, 28(4), 377. DOI:10.3390/e28040377

**Relevance:** Systematic review of HITL paradigms. Our affective pressure mechanism can be viewed as an internalized form of human oversight: rather than requiring a human in the loop for every decision, the affective calibration layer encodes human-like risk sensitivity as an auxiliary signal, reducing the frequency of human intervention while maintaining safety.

[17] Vats, V., Nizam, M.B., Liu, M., & Wang, Z. (2024). A Survey on Human-AI Collaboration with Large Foundation Models. arXiv:2403.04931

**Relevance:** Surveys collaboration patterns between humans and foundation models. Our experience memory component enables a form of deferred human-AI collaboration: past human corrections and near-miss events are stored and replayed as affective pressure signals, allowing the agent to internalize human judgment without real-time human presence.

[18] Wu, X., Xiao, L., Sun, Y., Zhang, J., Ma, T., & He, L. (2021). A Survey of Human-in-the-Loop for Machine Learning. arXiv:2108.00941

**Relevance:** Comprehensive survey of HITL methods across the ML lifecycle. Our framework draws on the active learning principle from HITL: experience memory selectively stores and prioritizes high-information safety episodes (near-misses, corrections), functioning as an internalized active learning mechanism for safety calibration.

[19] Fails, J.A., & Olsen Jr, D.R. (2003). Interactive Machine Learning. *IUI 2003*. DOI:10.1145/604045.604056

**Relevance:** Seminal work on interactive ML where users provide real-time feedback to shape model behavior. Our affective pressure signals generalize this paradigm: instead of requiring explicit user feedback at each step, the affective calibration layer generates pressure signals autonomously based on risk context and accumulated experience, scaling interactive safety to settings where real-time human input is unavailable.

[20] Settles, B. (2010). Active Learning Literature Survey. *University of Wisconsin-Madison CS Technical Report 1648*. URL: https://minds.wisconsin.edu/handle/1793/60444

**Relevance:** Foundational survey on active learning strategies. Our experience memory component applies an active learning principle to safety: rather than uniformly storing all interactions, we prioritize storage of safety-critical episodes (high affective pressure events), ensuring that the most informative experiences shape future calibration.

---

## Category 4: Affective Computing

[21] Picard, R.W. (1997). *Affective Computing*. MIT Press. ISBN:978-0-262-16170-2

**Relevance:** Foundational text that defines affective computing as computing that relates to, arises from, or influences emotions. Our framework operationalizes Picard's vision in the agent safety domain: affective pressure signals are synthetic emotion-like states (fear, anxiety, caution) that modulate agent behavior, translating affective computing principles into concrete safety mechanisms for autonomous agents.

[22] Afzal, S., Khan, H.A., Khan, I.U., Piran, M.J., & Lee, J.W. (2023). A Comprehensive Survey on Affective Computing: Challenges, Trends, Applications, and Future Directions. arXiv:2305.07665

**Relevance:** Surveys the full landscape of affective computing including emotion recognition, generation, and application. Our work addresses a gap identified in this survey: while affective computing has been applied to human-computer interaction and healthcare, its application to autonomous agent safety remains underexplored. Our framework demonstrates that structured affective signals can serve as effective auxiliary calibration signals for safety.

[23] Pei, G., Li, H., Lu, Y., Wang, Y., Hua, S., & Li, T. (2024). Affective Computing: Recent Advances, Challenges, and Future Trends. *Intelligent Computing*. DOI:10.34133/icomputing.0076

**Relevance:** Reviews recent advances in affective computing with emphasis on multimodal emotion recognition and generation. Our affective pressure signals are a form of generated affective state: rather than recognizing human emotions, we generate synthetic affective pressure within the agent itself, applying affective generation techniques to the novel domain of safety calibration.

[24] Lazarus, R.S. (1991). *Emotion and Adaptation*. Oxford University Press. ISBN:978-0-19-506514-9

**Relevance:** Foundational appraisal theory proposing that emotions arise from cognitive evaluation of situational meaning. Our affective pressure mechanism is directly inspired by Lazarus's appraisal theory: the agent evaluates risk context (primary appraisal) and its coping capacity (secondary appraisal), generating affective pressure proportional to the perceived threat, which then modulates action selection.

[25] Smith, C.A., & Ellsworth, P.C. (1985). Patterns of Cognitive Appraisal in Emotion. *Journal of Personality and Social Psychology*, 48(4), 813–838. DOI:10.1037/0022-3514.48.4.813

**Relevance:** Identifies distinct appraisal dimensions (attention, certainty, effort, pleasantness, responsibility) that differentiate emotional experiences. Our affective pressure signals are parameterized along analogous dimensions: risk salience (attention), confidence (certainty), and urgency (effort), enabling fine-grained affective modulation rather than binary safe/unsafe decisions.

[26] Majumder, N., Poria, S., Hazarika, D., Mihalcea, R., Gelbukh, A., & Cambria, E. (2020). Dialoguern: Emotion Recognition in Conversation. *ACM Computing Surveys*. DOI:10.1145/3394527

**Relevance:** Surveys emotion recognition in conversational contexts. Our framework leverages conversational affective signals as input to the affective pressure generator: when an agent detects emotional distress or urgency in user utterances, the resulting affective pressure can escalate safety precautions, creating a link between user affective state and agent safety behavior.

---

## Category 5: Memory / Experience Replay / Adaptive Agents

[27] Shinn, N., Cassano, F., Labash, A., Gopinath, A., Narasimhan, K., & Yao, S. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. *NeurIPS 2023*. arXiv:2303.11366

**Relevance:** Introduces verbal reinforcement learning where agents reflect on failures and store verbal summaries for future guidance. Our experience memory extends Reflexion's reflection mechanism by adding affective tagging: stored experiences carry affective pressure metadata that enables prioritized retrieval of safety-critical episodes, not just task-relevant ones.

[28] Hu, M.Y., Van Durme, B., Andreas, J., & Jhamtani, H. (2025). ECHO: Sample-Efficient Online Learning in LM Agents via Hindsight Trajectory Rewriting. arXiv:2510.10304

**Relevance:** Proposes hindsight trajectory rewriting for sample-efficient agent learning. Our experience memory component shares the hindsight optimization principle: after a near-miss event, the agent re-evaluates the trajectory with augmented affective pressure, storing the corrected decision path for future reference, improving safety without requiring additional environment interactions.

[29] Schaul, T., Quan, J., Antonoglou, I., & Silver, D. (2016). Prioritized Experience Replay. *ICLR 2016*. arXiv:1511.05952

**Relevance:** Introduces priority-based replay where experiences with higher TD-error are replayed more frequently. Our experience memory applies an analogous prioritization scheme for safety: experiences associated with high affective pressure (near-misses, safety violations) receive higher replay priority, ensuring that safety-critical episodes disproportionately shape future calibration.

[30] Andrychowicz, M., Wolski, F., Ray, A., Schneider, A., Fong, R., Welinder, P., McGrew, B., Tobin, J., Abbeel, P., & Zaremba, W. (2018). Hindsight Experience Replay. *NeurIPS 2017 / AAAI 2018*. arXiv:1707.01495

**Relevance:** Enables learning from failed episodes by relabeling them with achieved goals. Our experience memory uses a similar relabeling strategy for safety: when an agent avoids a near-miss, the experience is relabeled with the counterfactual outcome (what would have happened without hesitation), reinforcing the safety value of the affective pressure that prevented the violation.

[31] Wang, L., Ma, C., et al. (2024). A Survey on Large Language Model Based Autonomous Agents. *Frontiers of Computer Science*. DOI:10.1007/s11704-024-40231-1

**Relevance:** (Cross-referenced from Category 1 [3].) In the context of memory and adaptive agents, this survey's module taxonomy describes memory architectures (short-term, long-term, hybrid) used in current LLM agents. Our experience memory extends the hybrid memory paradigm by introducing affective-priority indexing, where memory retrieval is biased toward safety-critical episodes rather than purely recency or relevance.

---

## Category 6: Statistical Testing / McNemar / Bootstrap CI

[32] Demšar, J. (2006). Statistical Comparisons of Classifiers over Multiple Data Sets. *Journal of Machine Learning Research*, 7, 1–30.

**Relevance:** Establishes the standard methodology for comparing classifiers across multiple data sets using Friedman test with post-hoc Nemenyi test. We follow Demšar's recommended protocol for comparing our affective calibration framework against baseline agents across multiple benchmark subsets, reporting average ranks and critical difference diagrams.

[33] Dietterich, T.G. (1998). Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms. *Neural Computation*, 10(7), 1895–1923. DOI:10.1162/089976698300017197

**Relevance:** Introduces the 5×2 cv paired t-test and discusses limitations of resampled t-tests. We adopt Dietterich's recommendations for paired comparison of safety calibration methods, using appropriate corrections for multiple comparisons when evaluating our framework against multiple baselines on the same benchmark data.

[34] Efron, B., & Tibshirani, R. (1986). Bootstrap Methods for Standard Errors, Confidence Intervals, and Other Measures of Statistical Accuracy. *Statistical Science*, 1(1), 54–75. DOI:10.1214/ss/1177013815

**Relevance:** Foundational paper on bootstrap methods for constructing confidence intervals without distributional assumptions. We use bootstrap resampling (10,000 iterations) to construct 95% confidence intervals for our primary safety metrics (risky auto-execution rate, task completion rate), providing non-parametric uncertainty quantification for our reported results.

[35] Lorena, A.C., Garcia, L.P.F., Lehmann, J., Souto, M.C.P., & Ho, T.K. (2023). Time for a Change: A Tutorial for Comparing Classifiers on Multiple Data Sets. *ACM Computing Surveys*. DOI:10.1145/3575678

**Relevance:** Modern tutorial updating Demšar's methodology with additional tests and visualizations. We follow Lorena et al.'s recommended workflow for our multi-benchmark evaluation: checking assumptions, applying appropriate paired tests (Wilcoxon signed-rank for pairwise, Friedman for multi-way), and reporting effect sizes alongside p-values.

[36] Efron, B., & Tibshirani, R.J. (1994). *An Introduction to the Bootstrap*. Chapman and Hall/CRC. ISBN:978-0-412-04231-7

**Relevance:** Comprehensive textbook on bootstrap methods. We reference this for the theoretical foundations of our bootstrap confidence interval procedure, particularly the bias-corrected and accelerated (BCa) bootstrap method used for our safety metric intervals when the bootstrap distribution exhibits skewness.

[37] McNemar, Q. (1947). Note on the Sampling Error of the Difference Between Correlated Proportions or Percentages. *Psychometrika*, 12(2), 153–157. DOI:10.1007/BF02289397

**Relevance:** Introduces McNemar's test for comparing correlated proportions. We apply McNemar's test to compare the binary safety outcomes (safe vs. unsafe action) of our affective calibration framework against each baseline agent on matched test instances, providing a rigorous paired statistical test for our primary safety comparison.

---

## Verification Status

| # | Entry | Status |
|---|-------|--------|
| [1] | ReAct (Yao et al. 2023) | Verified — ICLR 2023, arXiv:2210.03629 |
| [2] | Toolformer (Schick et al. 2023) | Verified — NeurIPS 2023 Oral, arXiv:2302.04761 |
| [3] | Survey on LLM Agents (Wang et al. 2024) | Verified — Frontiers of Computer Science, DOI confirmed |
| [4] | Generative Agents (Park et al. 2023) | Verified — UIST 2023, arXiv:2304.03442 |
| [5] | ToolLLM (Qin et al. 2024) | Verified — ICLR 2024, arXiv:2307.16789 |
| [6] | HuggingGPT (Shen et al. 2024) | Verified — Computational Linguistics, arXiv:2303.17580 |
| [7] | WebGPT (Nakano et al. 2022) | Verified — arXiv:2112.09332 |
| [8] | Agent-SafetyBench (Zhang et al. 2024) | Verified — arXiv:2412.14470 |
| [9] | ToolSafety (Xie et al. 2025) | Verified — EMNLP 2025, DOI:10.18653/v1/2025.emnlp-main.714 |
| [10] | Constitutional AI (Bai et al. 2022) | Verified — arXiv:2212.08073 |
| [11] | TrustAgent (Hua et al. 2024) | Verified — EMNLP 2024 Findings, arXiv:2312.06698 |
| [12] | VeriGuard (Miculicich et al. 2025) | Verified — arXiv:2510.05156 |
| [13] | Agent Security Bench (Zhang et al. 2025) | Verified — ICLR 2025, arXiv:2410.02644 |
| [14] | SafeToolBench (Xia et al. 2025) | Verified — arXiv:2509.07316 |
| [15] | ToolSafe (Mou et al. 2026) | **needs verification** — arXiv:2601.10156; confirm 2026 publication status and venue |
| [16] | HITL AI Review (Lazaros et al. 2026) | Verified — Entropy 28(4), DOI:10.3390/e28040377 |
| [17] | Human-AI Collaboration Survey (Vats et al. 2024) | Verified — arXiv:2403.04931 |
| [18] | HITL for ML Survey (Wu et al. 2021) | Verified — arXiv:2108.00941 |
| [19] | Interactive ML (Fails & Olsen 2003) | Verified — IUI 2003, DOI:10.1145/604045.604056 |
| [20] | Active Learning Survey (Settles 2010) | Verified — UW-Madison TR 1648 |
| [21] | Affective Computing (Picard 1997) | Verified — MIT Press, ISBN confirmed |
| [22] | AC Survey (Afzal et al. 2023) | Verified — arXiv:2305.07665 |
| [23] | AC Recent Advances (Pei et al. 2024) | Verified — Intelligent Computing, DOI:10.34133/icomputing.0076 |
| [24] | Emotion and Adaptation (Lazarus 1991) | Verified — Oxford University Press, ISBN confirmed |
| [25] | Cognitive Appraisal (Smith & Ellsworth 1985) | Verified — JPSP 48(4), DOI:10.1037/0022-3514.48.4.813 |
| [26] | Emotion in Conversation (Majumder et al. 2020) | Verified — ACM Computing Surveys, DOI:10.1145/3394527 |
| [27] | Reflexion (Shinn et al. 2023) | Verified — NeurIPS 2023, arXiv:2303.11366 |
| [28] | ECHO (Hu et al. 2025) | Verified — arXiv:2510.10304 |
| [29] | Prioritized Experience Replay (Schaul et al. 2016) | Verified — ICLR 2016, arXiv:1511.05952 |
| [30] | Hindsight Experience Replay (Andrychowicz et al. 2018) | Verified — NeurIPS 2017 / AAAI 2018, arXiv:1707.01495 |
| [31] | Survey on LLM Agents (Wang et al. 2024) | Verified — cross-reference of [3] |
| [32] | Demšar (2006) | Verified — JMLR 7, 1–30 |
| [33] | Dietterich (1998) | Verified — Neural Computation, DOI confirmed |
| [34] | Bootstrap Methods (Efron & Tibshirani 1986) | Verified — Statistical Science, DOI confirmed |
| [35] | Time for a Change (Lorena et al. 2023) | Verified — ACM Computing Surveys, DOI:10.1145/3575678 |
| [36] | Introduction to Bootstrap (Efron & Tibshirani 1994) | Verified — Chapman and Hall/CRC, ISBN confirmed |
| [37] | McNemar (1947) | Verified — Psychometrika, DOI:10.1007/BF02289397 |

**Total: 37 entries (36 unique + 1 cross-reference) across 6 categories**

**Entries requiring further verification: 1** ([15] ToolSafe — Mou et al. 2026)
