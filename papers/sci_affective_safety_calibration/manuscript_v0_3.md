# Experience-Shaped Affective Safety Calibration for Autonomous Agent Execution

## Abstract

Autonomous agents that use large language models to operate tools and execute actions pose significant safety risks. Without careful calibration, agents may execute destructive, irreversible, or production-altering actions automatically. In this paper, we present a three-tier safety calibration framework that uses structured affective pressure signals and experience memory as auxiliary signals—not real-time emotion recognition outputs. On the semi-real Affective-Agent-Safety-300 benchmark, the framework reduced risky auto-execution from 87.2% under the safe-keyword-first baseline to 3.6%, corresponding to a 95.9% relative reduction. We also investigate longitudinal memory strategies, finding that single-failure memory achieves the best safety-utility balance, while accumulated failure memory causes severe over-caution collapse.

**Keywords**: autonomous agents, safety calibration, affective computing, experience memory, tool use

---

## 1. Introduction

Autonomous agents powered by large language models (LLMs) are increasingly capable of using tools, modifying code, and executing actions in real-world environments. While this capability enables powerful applications, it also introduces significant safety risks. An overly cautious agent may fail to accomplish tasks due to excessive human review requirements, while an under-cautious agent may execute dangerous actions automatically.

In this work, we present a three-tier safety calibration framework that balances safety and utility. Our key contributions are:

1. A three-tier calibration mechanism that prioritizes risk context over safe keyword detection.
2. The use of structured affective pressure signals as auxiliary calibration inputs.
3. An experience memory system that adjusts future decisions based on prior failures.
4. A controlled evaluation on two benchmarks (Affective-Safety-200 and Affective-Agent-Safety-300) demonstrating significant safety improvements.

---

## 2. Related Work

### 2.1 Tool-Using Autonomous Agents

The emergence of large language models as reasoning engines has driven substantial progress in tool-using autonomous agents. ReAct [1] introduced interleaved reasoning and acting as a general paradigm for LLM-based decision-making, while Toolformer [2] demonstrated that models can learn to invoke external APIs when trained on self-supervised tool-use data. At greater scale, ToolLLM [5] trained models across 16,000 real-world APIs, and HuggingGPT [6] orchestrated heterogeneous models through natural language planning. WebGPT [7] showed that browser-based navigation and information retrieval can be guided by human feedback, and Generative Agents [4] illustrated how persistent memory and reflection enable believable social simulation over extended time horizons.

These works share a common orientation: they expand what autonomous agents can do. Our work proceeds from a different premise. Rather than improving tool-use capability, we address the question of when an agent should decline to act. The agents above execute tool calls with minimal hesitation once a plan is formed, which is appropriate in benign environments but hazardous when actions carry irreversible consequences. Our three-tier calibration mechanism operates as a safety layer orthogonal to capability—it does not enhance planning or tool selection, but modulates execution confidence based on risk context, affective pressure, and experience memory.

### 2.2 Safety Calibration and Human Oversight

Safety evaluation and guardrail design for autonomous agents have received growing attention. Agent-SafetyBench [8] provided a systematic benchmark measuring LLM-agent safety across multiple risk categories, revealing that current agents frequently execute unsafe actions even when the risk is apparent. ToolSafety [9] and SafeToolBench [14] examined safety in tool-use scenarios specifically, while ToolSafe [15] and Agent Security Bench [13] expanded the scope to adversarial and security-oriented evaluations. On the intervention side, TrustAgent [11] proposed trust-aware oversight mechanisms, Constitutional AI [10] introduced rule-based self-correction through constitutional principles, and VeriGuard [12] combined formal verification with runtime monitoring for agent actions.

These contributions establish that safety is a meaningful and measurable problem for autonomous agents, and they propose various guardrails ranging from constitutional rules to formal verification. Our approach differs in two respects. First, rather than relying solely on keyword-based safety detection or constitutional prompting, we prioritize risk context as the primary calibration signal—our mechanism demotes safe-keyword matches when the situational context indicates elevated risk. Second, we incorporate structured affective pressure signals and experience memory as auxiliary calibration inputs, neither of which appears in the safety frameworks above. This combination yields a 95.9% relative reduction in risky auto-execution on our benchmarks compared to a safe-keyword-first baseline, though we emphasize this result is benchmark-specific and does not constitute a general safety guarantee.

### 2.3 Affective Computing as Structured Interaction Signal

Affective computing, since Picard's foundational work [21], has primarily concerned itself with recognizing, interpreting, and generating human emotional states. Recent surveys by Afzal et al. [22] and Pei et al. [23] document substantial progress in multimodal emotion recognition and affect-aware dialogue systems, while theoretical frameworks from Lazarus [24] and appraisal models such as Smith and Ellsworth [25] have provided cognitive accounts of how emotions relate to situational evaluation and decision-making.

We draw on the theoretical insight that affective states carry information about situational risk, but we depart from the mainstream affective computing agenda in a deliberate way. We do not perform real-time emotion recognition, nor do we claim that our agent possesses general affective understanding. Instead, we treat affective pressure as a structured annotation—a categorical signal indicating the intensity and valence of human affective responses in a given interaction context—that serves as an auxiliary input to a rule-based calibrator. This design choice reflects a pragmatic stance: structured signals are reproducible, auditable, and do not depend on the reliability of emotion classifiers, which remains an open research problem. Our use of affective signals is thus closer to structured risk labeling than to affective computing in its traditional sense.

### 2.4 Experience Memory and Adaptive Safety

Experience replay and reflection mechanisms have proven effective for improving agent performance on task-oriented benchmarks. Reflexion [27] demonstrated that verbal self-reflection on failed trajectories enables LLM agents to correct errors in subsequent attempts, while ECHO [28] extended this idea with hierarchical experience organization. In reinforcement learning, Prioritized Experience Replay [29] showed that sampling experiences proportional to their temporal-difference error accelerates learning, and Hindsight Experience Replay [30] reframed failed episodes as successful ones toward alternative goals to improve sample efficiency.

These works use memory to improve task success rates. We use memory for a different purpose: safety calibration. Our experience memory stores prior failure cases—specifically, instances where the agent executed an action that was later judged unsafe—and adjusts future calibration thresholds accordingly. A notable finding from our experiments is that the relationship between memory size and safety is non-monotonic: single-failure memory improves the safety-utility balance, but accumulated memory causes what we term over-caution collapse, where the agent declines safe actions at rates that degrade utility unacceptably. This observation suggests that experience-based safety calibration requires careful memory management, a concern that does not arise in task-oriented experience replay where more memory generally helps.

### 2.5 Positioning of This Work

The preceding sections place our work at the intersection of agent safety, structured affective signaling, and experience-based adaptation, but with clear boundaries. We do not advance tool-use capability (Section 2.1), nor do we propose a general framework for autonomous agent safety (Section 2.2). We do not solve the emotion recognition problem or claim affective understanding (Section 2.3), and we do not present a general experience replay architecture (Section 2.4).

What we contribute is a specific mechanism—three-tier calibration that prioritizes risk context over safe-keyword detection, augmented by structured affective pressure signals and single-failure experience memory—and an empirical evaluation of this mechanism on two controlled benchmarks: Affective-Safety-200 and Affective-Agent-Safety-300. Our results demonstrate that the proposed calibration substantially reduces risky auto-execution relative to a safe-keyword-first baseline, and they reveal the over-caution collapse phenomenon that accompanies unbounded experience accumulation. These findings are benchmark-specific and mechanism-specific; they do not establish that our approach generalizes to open-ended agent deployments or to safety threats beyond the categories covered in our evaluation. We present them as a controlled study of a particular design choice, with the hope that the design principles—context-first calibration, structured auxiliary signals, and bounded experience memory—may inform broader efforts in agent safety.

---

## 3. Method

### 3.1 Framework Overview

> **Figure 1.** Overview of the proposed experience-shaped affective safety calibration framework. Structured affective pressure and bounded experience memory are used as auxiliary calibration signals rather than real-time emotion recognition outputs. The three-tier SafeActionCalibrator evaluates strict risk context before safe keywords, preventing dangerous actions from being auto-executed due to the presence of safe-sounding verbs.

Our experience-shaped affective safety calibration framework takes user requests and task context as input, processes them through an action/event parser and risk context detector, and then applies three-tier calibration using affective pressure signals and experience memory to produce a safety decision: AUTO_EXECUTE, SIMULATE_FIRST, HUMAN_REVIEW, or BLOCK. The outcome of the decision updates the experience memory for future cases.

### 3.2 Three-Tier Calibration Policy

> **Figure 2.** Three-tier calibration policy with strict context priority. Tier 1 (Strict Review) is evaluated first: if any destructive, sensitive, security-related, irreversible, or production context is detected, the action is routed to human review or blocked. Tier 2 (Safe Auto-Execute) applies only when a safe verb is present and no Tier 1 context is matched. Tier 3 (Ambiguous Default Cautious) handles all remaining cases with simulation-first verification. The priority order ensures that safe keywords cannot override risk context.

The three-tier calibration policy operates as follows:

**Tier 1: Strict Review (Highest Priority)**
If the action involves destructive operations, sensitive data, security-related actions, irreversible changes, or affects a production environment, the agent requires human review. If the action is both destructive, irreversible, and in a production environment, the action is blocked entirely.

**Tier 2: Safe Auto-Execute**
If the action has a safe verb (e.g., "list", "read", "view") and no Tier 1 risk context, the action is executed automatically. However, this decision may be overridden by high affective pressure or prior failure memory, which downgrades the decision to SIMULATE_FIRST.

**Tier 3: Ambiguous Default Cautious**
If the action is ambiguous (unclear intent, insufficient safety evidence), the agent defaults to a cautious approach, requiring simulation before execution.

### 3.3 Affective Pressure Signal

The affective pressure signal is a structured annotation (not real-time emotion recognition) that indicates the urgency, anxiety, or stress level of the user. When the pressure is high, Tier 2 safe actions are downgraded to SIMULATE_FIRST, adding an extra layer of caution in high-pressure situations.

### 3.4 Experience Memory

The experience memory system tracks prior failures and adjusts future decisions accordingly. We investigate three memory strategies:
- **No memory**: No adjustment based on prior failures.
- **Single-failure memory**: If a similar case failed before, downgrade Tier 2 safe actions to SIMULATE_FIRST.
- **Accumulated failure memory**: Accumulate all failures over time; leads to over-caution collapse.

---

## 4. Benchmark

### 4.1 Dataset Description

We use two benchmarks in this work:

1. **Affective-Safety-200**: A controlled synthetic benchmark with 200 cases spanning 7 categories.
2. **Affective-Agent-Safety-300**: A semi-real simulated trace benchmark with 300 cases spanning 5 source types.

We define the term *semi-real* as follows: the traces in Affective-Agent-Safety-300 are structured simulations derived from common agent-assisted development workflows and tool-use risk scenarios. They are not collected from production enterprise deployments. The scenarios are constructed to reflect realistic action sequences, risk contexts, and affective pressure conditions that autonomous agents may encounter, but they are authored rather than logged. This design allows controlled, reproducible evaluation of safety calibration mechanisms, while limiting claims about real-world generalization. The semi-real designation is intended to distinguish these traces from purely synthetic benchmarks (where scenarios may lack ecological validity) and from production logs (which are unavailable due to privacy and safety constraints).

### 4.2 Source Type Distribution

| Source Type | Count |
|---|---|
| coding_agent_trace | 100 |
| tool_use_risk_trace | 80 |
| affective_pressure_trace | 60 |
| safe_low_risk_trace | 40 |
| experience_failure_trace | 20 |

### 4.3 Label Space

Both benchmarks use a four-level safety decision taxonomy:
- AUTO_EXECUTE: Action is safe to execute automatically.
- SIMULATE_FIRST: Action should be simulated first before execution.
- HUMAN_REVIEW: Action requires human review before execution.
- BLOCK: Action must be blocked entirely.

---

## 5. Experiments

### 5.1 Baselines

We compare our FullCalibratorAdapter against four baselines:

1. **KeywordRuleBaseline**: Simple keyword matching—risky keywords trigger review.
2. **SafeKeywordFirstBaseline**: Safe keywords override risk context (pre-V0.9.1 bug behavior).
3. **RiskContextOracleBaseline (Oracle/upper-bound, not deployable)**: Directly reads structured risk context; diagnostic upper bound only.
4. **NoExperienceNoAffectiveBaseline**: Real calibration without affective/memory signals.

### 5.2 Main Semi-Real Results

> **Figure 3.** Risky auto-execution rate comparison across methods on the Affective-Agent-Safety-300 semi-real benchmark (N=300). FullCalibratorAdapter achieves 3.6% risky auto-execution, below the 5% target threshold (dashed red line). SafeKeywordFirstBaseline and KeywordRuleBaseline exhibit catastrophically high risky auto-execution rates (87.2% and 78.0% respectively), demonstrating the danger of evaluating safe keywords before risk context. RiskContextOracleBaseline (marked with asterisk) is a structured oracle that directly reads risk context from the benchmark; it is not a deployable method and is included only as an upper-bound diagnostic reference.

| Method | Action Accuracy | Risky Auto-Exec ↓ | False Caution ↓ | Safe Auto-Exec Acc ↑ | Composite ↑ |
|---|---|---|---|---|---|
| FullCalibratorAdapter | **0.753** | **0.036** | 0.122 | **0.757** | **0.860** |
| KeywordRuleBaseline | 0.460 | 0.780 | 0.000 | 1.000 | 0.553 |
| SafeKeywordFirstBaseline | 0.417 | 0.872 | 0.000 | 1.000 | 0.507 |
| RiskContextOracleBaseline* | 0.510 | 0.064 | 0.000 | 1.000 | 0.784 |
| NoExperienceNoAffectiveBaseline | 0.717 | 0.043 | 0.122 | 0.757 | 0.844 |

\*Oracle/upper-bound diagnostic baseline, not deployable. Directly reads risk context from benchmark.

Our FullCalibratorAdapter achieves 3.6% risky auto-execution, compared to 87.2% for the SafeKeywordFirstBaseline—a 95.9% relative reduction.

### 5.3 Longitudinal Memory Experiment

> **Figure 4.** Longitudinal experience memory trade-off across three configurations on the Affective-Agent-Safety-300 benchmark. Single-failure memory achieves the best safety-utility balance: 16.3% lower risky auto-execution than no memory (3.6% vs 4.3%) while maintaining identical safe auto-execution accuracy (0.757). Accumulated failure memory eliminates risky auto-execution entirely (0.000) but causes over-caution collapse, reducing safe auto-execution accuracy to 0.000. This demonstrates that bounded, calibrated experience memory is preferable to unbounded accumulation.

| Group | Action Accuracy | Risky Auto-Exec ↓ | Safe Auto-Exec Acc ↑ | Composite ↑ |
|---|---|---|---|---|
| no_memory | 0.747 | 0.043 | 0.757 | 0.830 |
| single_failure_memory | **0.753** | **0.036** | **0.757** | **0.835** |
| accumulated_failure_memory | 0.520 | **0.000** | **0.000** | 0.716 |

Single-failure memory achieves the best safety-utility balance, while accumulated failure memory causes severe over-caution collapse, reducing safe auto-execution accuracy from 0.757 to 0.000.

### 5.4 Statistical Analysis

#### Bootstrap 95% Confidence Intervals (FullCalibratorAdapter)

| Metric | Mean | 95% CI Lower | 95% CI Upper |
|---|---|---|---|
| Action Accuracy | 0.753 | 0.703 | 0.800 |
| Composite Score | 0.860 | 0.826 | 0.892 |

#### McNemar Paired Comparisons

| Comparison | χ² | p-value | Significant at α=0.05? |
|---|---|---|---|
| Full vs KeywordRuleBaseline | 53.92 | < 0.001 | Yes |
| Full vs SafeKeywordFirstBaseline | 66.01 | < 0.001 | Yes |
| Full vs RiskContextOracleBaseline | 37.28 | < 0.001 | Yes |
| Full vs NoExperienceNoAffectiveBaseline | 10.02 | 0.439 | No |

---

## 6. Discussion

### 6.1 Error Analysis

| Source Type | Total Cases | Errors | Error Rate | Risky Auto-Exec Count | False Over-Caution Count |
|---|---|---|---|---|---|
| coding_agent_trace | 100 | 31 | 31.0% | 1 | 11 |
| affective_pressure_trace | 60 | 17 | 28.3% | 0 | 2 |
| tool_use_risk_trace | 80 | 15 | 18.8% | 5 | 1 |
| experience_failure_trace | 20 | 6 | 30.0% | 0 | 0 |
| safe_low_risk_trace | 40 | 5 | 12.5% | 0 | 0 |

Most errors come from coding agent trace scenarios, where the complexity of code-related actions makes safety classification more challenging.

### 6.2 Key Findings

1. **Strict context priority reduces risky auto-execution**: By checking risk context before safe keywords, we achieved a 95.9% relative reduction in risky auto-execution.
2. **Affective pressure improves safety without severe efficiency tradeoff**: The FullCalibratorAdapter had slightly lower risky auto-execution (0.036) than the NoExperienceNoAffectiveBaseline (0.043), while maintaining identical safe auto-execution accuracy (0.757).
3. **Single-failure memory achieves best safety-utility balance**: This strategy reduced risky auto-execution without sacrificing safe auto-execution accuracy.
4. **Accumulated memory causes severe over-caution collapse**: This strategy eliminated risky auto-execution entirely but also reduced safe auto-execution accuracy to 0.000, demonstrating an extreme caution tradeoff.

### 6.3 What We Do NOT Claim

- We do not claim production deployment validation.
- We do not claim real-time emotion recognition.
- We do not claim the traces are collected from real enterprise systems.
- We do not claim general autonomous agent safety.
- We do not claim competitive baseline performance against all safety systems.

---

## 7. Limitations

1. **Semi-real traces are not enterprise production logs**: Our benchmarks are synthetic/simulated, not collected from real deployments.
2. **Affective pressure is structured/rule-based annotations, not real emotion recognition**: Our affective signals are provided as structured inputs, not inferred from user behavior or text.
3. **Experience memory's optimal intensity requires further calibration**: The best memory strategy may vary across deployment contexts and risk tolerances.
4. **Current results prove safety calibration, not general affective understanding**: We demonstrate improved safety using structured signals, not general affective understanding.
5. **RiskContextOracleBaseline is a diagnostic upper bound, not a competitor**: This baseline has unfair access to structured risk context and is not deployable.
6. **Limited generalizability**: Our results are demonstrated on two controlled benchmarks; generalizability to other domains is untested.
7. **No external validation from real deployments**: All results are from offline benchmark evaluation.

---

## 8. Conclusion and Future Work

In this paper, we presented a three-tier safety calibration framework that uses affective pressure signals and experience memory to reduce risky auto-execution by 95.9% compared to a safe-keyword-first baseline. Our investigation of longitudinal memory strategies found that single-failure memory achieves the best safety-utility balance, while accumulated failure memory causes severe over-caution collapse.

For future work, an alternative approach is to employ an LLM as a direct safety classifier via prompted evaluation. While conceptually straightforward, such baselines introduce their own failure modes (prompt sensitivity, inconsistent calibration across contexts, and lack of experience-shaped adaptation). A systematic comparison with LLM-based safety classifiers is planned as future work.

---

## Data Availability Statement

The Affective-Safety-200 and Affective-Agent-Safety-300 benchmarks used in this study are available for research purposes upon reasonable request. The benchmarks contain structured simulation traces and do not include any personally identifiable information or proprietary enterprise data. Researchers interested in reproducing or extending our experiments may request access by contacting the corresponding author, subject to a usage agreement that prohibits deployment of the traces as real-world safety test cases.

## Code Availability Statement

The source code for the three-tier calibration framework, including the FullCalibratorAdapter, all baseline implementations, and the evaluation pipeline, is available at a publicly accessible repository. The URL will be provided upon publication. The code is released under an open-source license (MIT) to facilitate reproducibility and further research.

## Ethics Statement

This work involves the design and evaluation of safety calibration mechanisms for autonomous agents. All benchmarks are constructed from simulated scenarios and do not involve human subjects, personal data, or real enterprise systems. No production environments were accessed or affected during this research. The affective pressure signals used in our framework are structured annotations, not outputs of emotion recognition systems applied to real individuals. We acknowledge that safety mechanisms, if poorly calibrated, can themselves cause harm—either by permitting dangerous actions or by over-cautiously blocking benign ones. Our work aims to reduce both types of failure, but we do not claim that our framework eliminates all safety risks. The benchmarks and code are shared with the intention of advancing safety research and should not be used as deployment-ready safety systems without further validation.

---

## References

[1] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR 2023*. arXiv:2210.03629

[2] Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. *NeurIPS 2023 (Oral)*. arXiv:2302.04761

[3] Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J., Chen, Z., Tang, J., Chen, X., Lin, Y., Zhao, W.X., Wei, Z., & Wen, J. (2024). A Survey on Large Language Model Based Autonomous Agents. *Frontiers of Computer Science*. DOI:10.1007/s11704-024-40231-1

[4] Park, J.S., O'Brien, J., Cai, C.J., Morris, M.R., Liang, P., & Bernstein, M.S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST 2023*. arXiv:2304.03442

[5] Qin, Y., Hu, S., Lin, Y., Chen, W., Ding, N., Cui, G., Zeng, Z., Feng, Y., Zhao, Y., Zhang, T., et al. (2024). ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs. *ICLR 2024*. arXiv:2307.16789

[6] Shen, Y., Song, K., Tan, X., Li, D., Lu, W., & Zhuang, Y. (2024). HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face. *Computational Linguistics*. arXiv:2303.17580

[7] Nakano, R., Hilton, J., Balaji, S., Wu, J., Ouyang, L., Kim, C., Hesse, C., Jain, S., Kosaraju, V., Saunders, W., et al. (2022). WebGPT: Browser-assisted question-answering with human feedback. arXiv:2112.09332

[8] Zhang, Z., Cui, S., Lu, Y., Zhou, J., Yang, J., Wang, H., & Huang, M. (2024). Agent-SafetyBench: Evaluating the Safety of LLM Agents. arXiv:2412.14470

[9] Xie, Y., Yuan, Y., Wang, W., Mo, F., Guo, J., & He, P. (2025). ToolSafety: A Comprehensive Dataset for Enhancing Safety in LLM-Based Agent Tool Invocations. *EMNLP 2025*. DOI:10.18653/v1/2025.emnlp-main.714

[10] Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J., Jones, A., Chen, A., Goldie, A., Mirhoseini, A., McKinnon, C., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073

[11] Hua, W., Yang, X., Jin, M., Li, Z., Cheng, W., Tang, R., & Zhang, Y. (2024). TrustAgent: Towards Safe and Trustworthy LLM-based Agents. *EMNLP 2024 Findings*. arXiv:2312.06698

[12] Miculicich, L., Parmar, M., Palangi, H., Dj Dvijotham, K., Montanari, M., Pfister, T., & Le, L.T. (2025). VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation. arXiv:2510.05156

[13] Zhang, H., Huang, J., Mei, K., Yao, Y., Wang, Z., Zhan, C., Wang, H., & Zhang, Y. (2025). Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents. *ICLR 2025*. arXiv:2410.02644

[14] Xia, H., Wang, H., Liu, Z., Yu, Q., Guo, Y., & Wang, H. (2025). SafeToolBench: Pioneering a Prospective Benchmark to Evaluating Tool Utilization Safety in LLMs. arXiv:2509.07316

[15] Mou, Y., Xue, Z., Li, L., Liu, P., Zhang, S., Ye, W., & Shao, J. (2026). ToolSafe: Enhancing Tool Invocation Safety of LLM-based agents via Proactive Step-level Guardrail and Feedback. arXiv:2601.10156

[16] Lazaros, K., Vrahatis, A.G., & Kotsiantis, S. (2026). Human-in-the-Loop Artificial Intelligence: A Systematic Review of Concepts, Methods, and Applications. *Entropy*, 28(4), 377. DOI:10.3390/e28040377

[17] Vats, V., Nizam, M.B., Liu, M., & Wang, Z. (2024). A Survey on Human-AI Collaboration with Large Foundation Models. arXiv:2403.04931

[18] Wu, X., Xiao, L., Sun, Y., Zhang, J., Ma, T., & He, L. (2021). A Survey of Human-in-the-Loop for Machine Learning. arXiv:2108.00941

[19] Fails, J.A., & Olsen Jr, D.R. (2003). Interactive Machine Learning. *IUI 2003*. DOI:10.1145/604045.604056

[20] Settles, B. (2010). Active Learning Literature Survey. *University of Wisconsin-Madison CS Technical Report 1648*.

[21] Picard, R.W. (1997). *Affective Computing*. MIT Press. ISBN:978-0-262-16170-2

[22] Afzal, S., Khan, H.A., Khan, I.U., Piran, M.J., & Lee, J.W. (2023). A Comprehensive Survey on Affective Computing: Challenges, Trends, Applications, and Future Directions. arXiv:2305.07665

[23] Pei, G., Li, H., Lu, Y., Wang, Y., Hua, S., & Li, T. (2024). Affective Computing: Recent Advances, Challenges, and Future Trends. *Intelligent Computing*. DOI:10.34133/icomputing.0076

[24] Lazarus, R.S. (1991). *Emotion and Adaptation*. Oxford University Press. ISBN:978-0-19-506514-9

[25] Smith, C.A., & Ellsworth, P.C. (1985). Patterns of Cognitive Appraisal in Emotion. *Journal of Personality and Social Psychology*, 48(4), 813–838. DOI:10.1037/0022-3514.48.4.813

[26] Majumder, N., Poria, S., Hazarika, D., Mihalcea, R., Gelbukh, A., & Cambria, E. (2020). Dialoguern: Emotion Recognition in Conversation. *ACM Computing Surveys*. DOI:10.1145/3394527

[27] Shinn, N., Cassano, F., Labash, A., Gopinath, A., Narasimhan, K., & Yao, S. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. *NeurIPS 2023*. arXiv:2303.11366

[28] Hu, M.Y., Van Durme, B., Andreas, J., & Jhamtani, H. (2025). ECHO: Sample-Efficient Online Learning in LM Agents via Hindsight Trajectory Rewriting. arXiv:2510.10304

[29] Schaul, T., Quan, J., Antonoglou, I., & Silver, D. (2016). Prioritized Experience Replay. *ICLR 2016*. arXiv:1511.05952

[30] Andrychowicz, M., Wolski, F., Ray, A., Schneider, A., Fong, R., Welinder, P., McGrew, B., Tobin, J., Abbeel, P., & Zaremba, W. (2018). Hindsight Experience Replay. *NeurIPS 2017 / AAAI 2018*. arXiv:1707.01495

[31] Wang, L., Ma, C., et al. (2024). A Survey on Large Language Model Based Autonomous Agents. *Frontiers of Computer Science*. DOI:10.1007/s11704-024-40231-1

[32] Demšar, J. (2006). Statistical Comparisons of Classifiers over Multiple Data Sets. *Journal of Machine Learning Research*, 7, 1–30.

[33] Dietterich, T.G. (1998). Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms. *Neural Computation*, 10(7), 1895–1923. DOI:10.1162/089976698300017197

[34] Efron, B., & Tibshirani, R. (1986). Bootstrap Methods for Standard Errors, Confidence Intervals, and Other Measures of Statistical Accuracy. *Statistical Science*, 1(1), 54–75. DOI:10.1214/ss/1177013815

[35] Lorena, A.C., Garcia, L.P.F., Lehmann, J., Souto, M.C.P., & Ho, T.K. (2023). Time for a Change: A Tutorial for Comparing Classifiers on Multiple Data Sets. *ACM Computing Surveys*. DOI:10.1145/3575678

[36] Efron, B., & Tibshirani, R.J. (1994). *An Introduction to the Bootstrap*. Chapman and Hall/CRC. ISBN:978-0-412-04231-7

[37] McNemar, Q. (1947). Note on the Sampling Error of the Difference Between Correlated Proportions or Percentages. *Psychometrika*, 12(2), 153–157. DOI:10.1007/BF02289397

---

## Appendix

### A. Affective-Safety-200 V1.0 Results

| Method | Action Accuracy | Risky Auto-Exec ↓ | Composite ↑ |
|---|---|---|---|
| FullCalibratorAdapter | **0.605** | **0.046** | **0.757** |
| KeywordRuleBaseline | 0.340 | 0.776 | 0.458 |
| SafeKeywordFirstBaseline | 0.305 | 0.809 | 0.428 |
| RiskContextOracleBaseline* | 0.580 | 0.020 | 0.804 |
| NoExperienceNoAffectiveBaseline | 0.630 | 0.066 | 0.765 |

\*Oracle/upper-bound diagnostic baseline, not deployable.

### B. Ablation Study (V1.0)

| Variant | Action Accuracy | Risky Auto-Exec ↓ | Composite ↑ |
|---|---|---|---|
| full (canonical) | 0.605 | 0.046 | 0.757 |
| w/o_strict_context_priority | 0.595 | **0.112** | 0.748 |
| w/o_affective_pressure | 0.630 | 0.066 | 0.765 |
| w/o_experience_memory | 0.605 | 0.046 | 0.757 |
| w/o_case_level_reset | 0.600 | 0.007 | 0.764 |
| w/o_boundary_regex | 0.635 | 0.072 | 0.777 |
