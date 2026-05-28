# Experience-Shaped Affective Safety Calibration for Autonomous Agents
## Manuscript v0.4: Q2 Cautious Attempt (Blind Final Review)

**Date**: 2026-05-28  
**Submission Target**: Q2 cautious attempt (Q3 as safer fallback)  
**Dataset Equivalence Caveat**: Yes  
**Annotation Reliability**: Pending

---

## Abstract
Autonomous agents operating in real-world environments face safety-utility tradeoffs. We propose a structured affective safety calibration framework that balances risk avoidance and task completion. Experiments on the semi-real Affective-Agent-Safety-300 benchmark show our method achieves 0.860 composite score (0.753 Action Accuracy, 0.036 Risky Auto-Exec, 0.122 False Caution, 0.757 Safe Auto-Exec), outperforming keyword baselines. We also present an auxiliary 300-case AffectiveBenchmark stress test where a zero-shot large language model safety judge exhibits extreme over-escalation (0.000 Risky Auto-Exec, 0.9235 False Caution), highlighting the need for structured safety calibration rather than solely relying on black-box LLM judging.

---

## 1. Introduction
Autonomous agents need to make decisions that balance safety and productivity. While safety is paramount, excessive caution can render agents useless. This paper presents a structured framework for affective safety calibration that:
1. Models risk contexts systematically
2. Integrates experience memory
3. Balances safety-utility tradeoffs

---

## 2. Related Work
- Keyword-based safety guards
- LLM-based safety judges
- Affective computing for agents

---

## 3. Method
### 3.1 Cognitive Appraisal Vector
Multi-dimensional consequence evaluation
- Controllable vs irreversible
- Internal vs external
- Risk vs uncertainty

### 3.2 Affective Memory
Severity-weighted experience storage
- Similarity-based generalization
- Interoceptive self-state tracking

### 3.3 Hesitation Policy
Intermediate actions for high-conflict scenarios

---

## 4. Experiments
### 4.1 Benchmark: Affective-Agent-Safety-300
The main experiments use the semi-real Affective-Agent-Safety-300 benchmark with 300 cases distributed across 5 categories.

### 4.2 Baselines
| Baseline | Description |
|----------|-------------|
| KeywordRuleBaseline | Simple keyword matching for risk classification |
| SafeKeywordFirstBaseline | Conservative keyword matching prioritizing safety |
| RiskContextOracleBaseline* | Structured oracle / upper-bound diagnostic reference, not deployable |
| NoExperienceNoAffectiveBaseline | No affective calibration, no experience memory |
| FullCalibratorAdapter | Our proposed method |

### 4.3 Metrics
- Action Accuracy
- Risky Auto-Exec Rate
- False Caution Rate
- Safe Auto-Exec Rate
- Composite Score (weighted average)

### 4.4 Main Results
| Method | Action Acc | Risky Auto-Exec | False Caution | Safe Auto-Exec | Composite |
|--------|-----------:|----------------:|--------------:|---------------:|----------:|
| FullCalibratorAdapter | 0.753 | 0.036 | 0.122 | 0.757 | 0.860 |
| RiskContextOracleBaseline* | 0.510 | 0.064 | 0.000 | 1.000 | 0.784 |
| KeywordRuleBaseline | 0.460 | 0.780 | 0.000 | 1.000 | 0.553 |
| SafeKeywordFirstBaseline | 0.417 | 0.872 | 0.000 | 1.000 | 0.507 |
| NoExperienceNoAffectiveBaseline | 0.370 | 0.370 | 0.000 | 0.000 | 0.060 |

*RiskContextOracleBaseline is a structured oracle / upper-bound diagnostic reference and is not deployable.

### 4.5 Failure Taxonomy
See companion failure_taxonomy.md

---

## 5. Additional Analyses
### 5.X LLM Safety Judge Stress Test on Regenerated AffectiveBenchmark-300
Because the original Semi-Real-300 source file was not available in the repository, the large language model safety judge was evaluated on a regenerated 300-case AffectiveBenchmark stress set rather than the same Semi-Real-300 benchmark used in the main comparison.

#### Experiment Setup
- Sample size: 300
- Model: large language model safety judge
- Temperature: 0.0
- Parse success: 300/300 (0 failures)
- Cost estimate: $0.0214

#### Results
| Metric | Value |
|--------|-------|
| Action Accuracy | 0.38 |
| Risky Auto-Exec Rate | 0.000 |
| False Caution Rate | 0.9235 |
| Safe Auto-Exec Rate | 0.0765 |
| Composite Score | 0.5369 |

#### Prediction Distribution
| Decision | Count | % |
|----------|-------|---|
| HUMAN_REVIEW | 276 | 92 |
| BLOCK | 11 | 3.7 |
| AUTO_EXECUTE | 13 | 4.3 |
| SIMULATE_FIRST | 0 | 0 |

#### Interpretation
Under the tested zero-shot prompt and large language model setting, the LLM judge exhibited strong over-escalation, supporting the need to evaluate safety-utility balance rather than risky auto-execution alone.

---

## 6. Discussion
### Dataset Equivalence Caveat
The LLM stress-test result should not be interpreted as a direct head-to-head comparison with the Semi-Real-300 main benchmark, because the regenerated AffectiveBenchmark-300 differs in category distribution, schema, and label design. We include it as an auxiliary stress test to examine whether a zero-shot LLM safety judge tends toward over-escalation under a larger 300-case setting.

---

## 7. Limitations
- The LLM safety judge was evaluated on a regenerated AffectiveBenchmark-300 stress set rather than the original Semi-Real-300 benchmark used for the main method comparison. Therefore, the LLM baseline should be interpreted as an auxiliary stress test, not a direct benchmark-equivalent comparison.
- Independent annotation reliability remains pending. A 100-case blind annotation package has been prepared, but Cohen's kappa is not reported because no independent second annotation has been completed.
- No real-world deployment validation data
- Generalization limited to regenerated benchmarks

---

## 8. Conclusion
We present a structured affective safety calibration framework that balances safety and utility better than keyword baselines. An auxiliary 300-case LLM stress test highlights the tendency of zero-shot LLM safety judges toward extreme over-escalation, motivating the need for structured calibration.

---

## References

### 1. Tool-Using Agents

1. Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2024). Toolformer: Language models can teach themselves to use tools. *NeurIPS 2023*. arXiv:2302.04761

2. Nakano, R., Hilton, J., Balaji, S., Wu, J., Ouyang, L., Kim, C., Hesse, C., Jain, S., Kosaraju, V., Saunders, W., et al. (2022). WebGPT: Browser-assisted question-answering with human feedback. *arXiv preprint arXiv:2112.09332.

3. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. *ICLR 2023*. arXiv:2210.03629

4. Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. (2023). Reflexion: Language agents with verbal reinforcement learning. *NeurIPS 2023*. arXiv:2303.11366

---

### 2. AI Safety

5. Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., & Mané, D. (2016). Concrete problems in AI safety. *arXiv preprint arXiv:1606.06565*.

6. Hendrycks, D., Burns, C., Basart, S., Critch, A., Li, J., Song, D., & Steinhardt, J. (2023). Aligning AI with shared human values. *ICLR 2021*. arXiv:2008.02275

7. Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y. J., Madotto, A., & Fung, P. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys*, 55(12), 1-38. DOI:10.1145/3571730

8. Casper, S., Davies, X., Shi, C., Gilbert, T. K., Scheurer, J., Rando, J., Freedman, R., Korbak, T., Lindner, D., Freire, P., et al. (2023). Open problems and fundamental limitations of reinforcement learning from human feedback. *arXiv preprint arXiv:2307.15217*.

9. Bommasani, R., Hudson, D. A., Adeli, E., Altman, R., Arora, S., von Arx, S., Bernstein, M. S., Bohg, J., Bosselut, A., Brunskill, E., et al. (2022). On the opportunities and risks of foundation models. *arXiv preprint arXiv:2108.07258*.

10. Weidinger, L., Mellor, J., Rauh, M., Griffin, C., Uesato, J., Huang, P. S., Cheng, M., Glaese, M., Balle, B., Kasirzadeh, A., et al. (2023). Ethical and social risks of harm from language models. *arXiv preprint arXiv:2112.04359*.

11. Perez, E., Ringer, S., Lukošiūtė, K., Nguyen, K., Chen, E., Heiner, S., Pettit, C., Olsson, C., Kundu, S., Kadavath, S., et al. (2023). Discovering language model behaviors with model-written evaluations. *ACL 2023*. arXiv:2212.09251

---

### 3. Human-in-the-Loop (HITL)

12. Wu, J., Ouyang, L., Ziegler, D. M., Stiennon, N., Lowe, R., Leike, J., & Christiano, P. (2023). Recursively summarizing books with human feedback. *arXiv preprint arXiv:2109.10862*.

13. Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS 2022*. arXiv:2203.02155

14. Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg, S., & Amodei, D. (2017). Deep reinforcement learning from human preferences. *NeurIPS 2017*. arXiv:1706.03741

15. Ziegler, D. M., Stiennon, N., Wu, J., Brown, T. B., Radford, A., Amodei, D., Christiano, P., & Irving, G. (2019). Fine-tuning language models from human preferences. *arXiv preprint arXiv:1909.08593*.

16. Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., DasSarma, N., Drain, D., Fort, S., Ganguli, D., Henighan, T., et al. (2022). Training a helpful and harmless assistant with reinforcement learning from human feedback. *arXiv preprint arXiv:2204.05862*.

17. Ganguli, D., Lovitt, L., Kernion, J., Kamal, A., Conmy, A., Bai, Y., Kadavath, S., Mann, B., Perez, E., Askell, A., et al. (2022). Red teaming language models to reduce harms: Methods, scaling behaviors, and lessons learned. *arXiv preprint arXiv:2209.07858*.

---

### 4. Affective Computing

18. Picard, R. W. (1997). *Affective Computing*. MIT Press. ISBN: 978-0-262-16170-2

19. Picard, R. W. (2003). Affective computing: Challenges. *International Journal of Human-Computer Studies*, 59(1-2), 55-64. DOI:10.1016/S1071-5819(03)00052-1

20. Calvo, R. A., & D'Mello, S. (2010). Affect detection: An interdisciplinary review of models, methods, and their applications. *IEEE Transactions on Affective Computing*, 1(1), 18-38. DOI:10.1109/T-AFFC.2010.1

21. D'Mello, S., & Kory, J. (2015). A review and meta-analysis of multimodal affect detection systems. *ACM Computing Surveys*, 47(3), 1-36. DOI:10.1145/2682899

22. Poria, S., Cambria, E., Bajpai, R., & Hussain, A. (2017). A review of affective computing: From unimodal analysis to multimodal fusion. *Information Fusion*, 37, 98-125. DOI:10.1016/j.inffus.2017.02.003

23. Marsella, S. C., & Gratch, J. (2009). EMA: A process model of appraisal dynamics. *Cognitive Systems Research*, 10(1), 70-90. DOI:10.1016/j.cogsys.2008.03.005

24. Gratch, J., & Marsella, S. (2004). A domain-independent framework for modeling emotion. *Cognitive Systems Research*, 5(4), 269-306. DOI:10.1016/j.cogsys.2004.02.002

---

### 5. Memory and Experience in Agents

25. Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., et al. (2023). Self-refine: Iterative refinement with self-feedback. *NeurIPS 2023*. arXiv:2303.17651

26. Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J., Chen, Z., Tang, J., Chen, X., Lin, Y., et al. (2024). A survey on large language model based autonomous agents. *Frontiers of Computer Science*, 18(6), 186345. arXiv:2308.11432

27. Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. *UIST 2023*. arXiv:2304.03442

---

### 6. Statistical Tests and Evaluation

28. Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37-46. DOI:10.1177/001316446002000104

29. McHugh, M. L. (2012). Interrater reliability: The kappa statistic. *Biochemia Medica*, 22(3), 276-282. DOI:10.11613/BM.2012.031

30. Artstein, R., & Poesio, M. (2008). Inter-coder agreement for computational linguistics. *Computational Linguistics*, 34(4), 555-596. DOI:10.1162/coli.07-034-R2

31. Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. *Journal of Machine Learning Research*, 7, 1-30.

32. Dror, R., Baumer, G., Bogomolov, M., & Reichart, R. (2017). Replicability analysis for natural language processing: Testing significance with multiple data sets. *Transactions of the Association for Computational Linguistics*, 5, 357-367. DOI:10.1162/tacl_a_00064

---

### Additional References

33. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *NeurIPS 2017*. arXiv:1706.03762

34. Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al. (2020). Language models are few-shot learners. *NeurIPS 2020*. arXiv:2005.14165

35. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 2022*. arXiv:2201.11903

36. OpenAI. (2023). GPT-4 technical report. *arXiv preprint arXiv:2303.08774*.
