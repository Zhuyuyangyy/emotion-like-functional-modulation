# Final Sanity Check — v0.3 Manuscript

**Date**: 2026-05-27
**Scope**: manuscript_v0_3.md, manuscript_v0_3_blind.md, references_verified.md, related_work_v0_3.md, figure_captions.md, submission_readiness_checklist.md

---

## 1. 数字清零情况

| 搜索项 | 修复前状态 | 修复后状态 | 说明 |
|--------|-----------|-----------|------|
| `0.624` | ⚠️ 1 active residual in `materials_for_manuscript_v0_1.md` L300 | ✅ 已修正为 `0.872` | 其余出现均在 error-documentation 上下文中，可接受 |
| `93.6%` | ⚠️ 1 active residual in `materials_for_manuscript_v0_1.md` L300 | ✅ 已修正为 `95.9%` | 其余出现均在 error-documentation 上下文中，可接受 |

**主稿 (manuscript_v0_3.md)**: ✅ 无残留错误数字
**盲版 (manuscript_v0_3_blind.md)**: ✅ 无残留错误数字

---

## 2. Prohibited Phrase 清零情况

| 禁止短语 | 修复前状态 | 修复后状态 | 修复方式 |
|----------|-----------|-----------|---------|
| `emotional intelligence` | ⚠️ `related_work_v0_3.md` L19 出现（否定语境） | ✅ 已替换为 `general affective understanding` | "nor do we claim that our agent possesses general affective understanding" |
| `state-of-the-art` | ⚠️ 3处出现（均为否定语境） | ✅ 已替换为 `competitive baseline performance` | 修改了 manuscript_v0_3.md、manuscript_v0_3_blind.md、data_authenticity_statement.md |
| `production validation` | ✅ 仅出现在 disclaimers 和 meta-documentation 中 | ✅ 无需修改 | 所有出现均为否定声明，非正向声称 |
| `16 references unchanged` | ✅ 未出现 | ✅ 无需修改 | — |

**主稿**: ✅ 全部禁止短语已清零
**盲版**: ✅ 全部禁止短语已清零

---

## 3. References 一致性

| 文件 | References 数量 | 状态 |
|------|----------------|------|
| manuscript_v0_3.md | [1]–[37] (37 entries) | ✅ 完整 |
| manuscript_v0_3_blind.md | [1]–[37] (37 entries) | ✅ 已修复（原仅16条，现已与主稿一致） |
| references_verified.md | [1]–[37] (36 unique + 1 cross-reference) | ✅ 一致 |

**修复说明**: 盲版原有16条参考文献且使用 author-year 格式，与主稿的37条编号格式严重不一致。已重新生成盲版，完全对齐主稿内容和参考文献列表。

**待验证**: [15] ToolSafe (Mou et al. 2026), arXiv:2601.10156 — 标记为 "needs verification"，需确认发表状态。

---

## 4. Figure 文件检查

| Figure | PNG | PDF | 存在 | 说明 |
|--------|-----|-----|------|------|
| fig1_framework_architecture | ✅ | ✅ | ✅ | 架构图 |
| fig2_three_tier_policy | ✅ | ✅ | ✅ | 三层策略图 |
| fig3_risky_auto_exec_comparison | ✅ | ✅ | ✅ | 柱状图（定量） |
| fig4_longitudinal_memory_tradeoff | ✅ | ✅ | ✅ | 折衷图（定量） |

所有4张图均有 PNG + PDF 格式，满足 SCI 期刊投稿要求。

---

## 5. Blind Version 完整性

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 作者姓名/机构 | ✅ 已移除 | "Anonymous Authors" |
| GitHub URL / 仓库链接 | ✅ 已移除 | "An anonymized repository will be released upon acceptance." |
| 致谢信息 | ✅ 已匿名化 | "Withheld for double-anonymous review." |
| 自引匿名化 | ✅ 无自引 | 原稿无自引 |
| 参考文献完整性 | ✅ 37条 | 与主稿完全一致 |
| 内容一致性 | ✅ | 与主稿内容完全一致，仅做匿名化处理 |

---

## 6. RiskContextOracleBaseline 标注检查

| 文件 | 标注方式 | 状态 |
|------|---------|------|
| manuscript_v0_3.md §5.1 | "Oracle/upper-bound, not deployable" | ✅ |
| manuscript_v0_3.md §5.2 表格脚注 | "Oracle/upper-bound diagnostic baseline, not deployable" | ✅ |
| manuscript_v0_3.md §5.2 Figure 3 说明 | "not a deployable method and is included only as an upper-bound diagnostic reference" | ✅ |
| manuscript_v0_3.md §7 Limitations #5 | "diagnostic upper bound, not a competitor" | ✅ |
| manuscript_v0_3_blind.md | 同主稿 | ✅ |
| figure_captions.md Figure 3 | "not a deployable method" | ✅ |

所有出现均已正确标注为 oracle / upper-bound / not deployable。

---

## 7. Blocker 评估

| # | Blocker | 状态 | 说明 |
|---|---------|------|------|
| 1 | 0.624 / 93.6% 残留 | ✅ 已修复 | materials_for_manuscript_v0_1.md L300 已更正 |
| 2 | emotional intelligence 短语 | ✅ 已修复 | related_work_v0_3.md 已替换 |
| 3 | state-of-the-art 短语 | ✅ 已修复 | 3处已替换 |
| 4 | 盲版参考文献不一致 | ✅ 已修复 | 从16条重建为37条 |
| 5 | [15] ToolSafe 参考文献待验证 | ⚠️ 待处理 | 需确认 arXiv:2601.10156 发表状态，非 blocker 但需在投稿前解决 |

**当前 Blocker 数量**: 0

**剩余待处理项**: 1（[15] 参考文献验证，非 blocker）

---

## 修改文件清单

| 文件 | 修改内容 |
|------|---------|
| `materials_for_manuscript_v0_1.md` | L300: 0.624→0.872, 93.6%→95.9%, 62.4%→87.2% |
| `related_work_v0_3.md` | L19: "emotional intelligence" → "general affective understanding" |
| `manuscript_v0_3.md` | §6.3: "superior performance" → "competitive baseline performance" |
| `manuscript_v0_3_blind.md` | 完全重建：37条参考文献、匿名化处理、prohibited phrases 清零 |
| `data_authenticity_statement.md` | "state-of-the-art" → "competitive baseline performance" |

---

*Phase 0 Final Sanity Check 完成。无 blocker，可进入 Phase 1。*
