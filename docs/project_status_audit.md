# Project Status Audit — Phase 0

**Date**: 2026-06-09
**Branch**: main (commit a8b7158)
**Auditor**: Agent (automated)
**Rule**: No results modified, no features added. Only paths, commands, and gaps verified.

---

## Q1: pytest 能否从零跑通？

**命令**: `python -m pytest tests/ -v`

**结果**: 125 passed, **1 failed**

**失败测试**:
- `tests/test_v0_3.py::TestEventSimilarity::test_encode_event_delete`
- 原因: 测试用 `"delete file /data/important.txt"` 期望 `data_loss_potential > 0.5`，但当前 `encode_event` 的 `data_loss_words` 不包含 `"file"` 或 `"/data/important.txt"` 中的任何词。这是我们在扩展关键词时移除了 `"all files"` 等多词短语后引入的回归。
- 修复方案: 在 `data_loss_words` 中添加 `"file"` 或修复测试用例以匹配当前词表。

**通过率**: 125/126 = 99.2%

---

## Q2: Semi-Real-300 原始 source JSON 是否存在？

**不存在。** 缺失。

- `AffectiveBenchmark` 类（`emotion_agent/affective_benchmark.py`）从**代码内嵌模板**动态生成 300 个任务，不是从外部 JSON 加载。
- 300 个任务只有 **60 个唯一描述字符串**（每个模板重复约 5 次）。
- 仓库中无 `semi_real_300.json` 或任何独立的 source JSON 文件。
- `dataset_card.md` 已明确标注："Original source JSON not available in current codebase"。

**缺口**: 没有独立于代码的数据文件。数据完全由 `AffectiveBenchmark.__init__` 中的模板列表 + `random.choice` 生成。

---

## Q3: 主表结果能否一键重跑？

**不能。**

| 结果 | 能否重跑 | 缺什么 |
|------|---------|--------|
| benchmark_v2 (5-fold CV) | ✅ 能 | `python experiments/benchmark_v2/run_real_benchmark.py` |
| R-Judge 外部验证 | ✅ 能 | `python experiments/benchmark_v2/run_rjudge_benchmark.py` |
| DeepSeek LLM baseline | ⚠️ 部分 | 需要有效 API key；脚本在 `experiments/llm_baseline/` |
| **论文主表 (FullCalibratorAdapter 等)** | ❌ 不能 | 原始结果来自 `scripts/generate_benchmark_results.py`，但该脚本使用 `DummyAgent`（agent 参数从未使用），结果由 baseline 字符串硬编码决定，不是真实组件输出 |
| 论文中的 Acc=0.753, Composite=0.860 | ❌ 不能 | 这些数字在当前代码中无法复现；`reproducibility_audit.md` 已承认："Main method results are reported from prior work and cannot be independently reproduced from the current codebase" |

**关键缺口**:
1. 论文主表数字与 benchmark_v2 真实管线结果**不一致**（主表是 DummyAgent 恒等映射，benchmark_v2 是真实组件）
2. 没有一键脚本同时产出论文所有表格和图
3. `scripts/generate_figures.py` 能出图，但数据来源是硬编码数字而非管线输出

---

## Q4: DeepSeek baseline 数据集定位

- **原始 DeepSeek baseline (100 条)**: `experiments/results/llm_baseline/` — gold_labels.json 有 100 条
- **Full-300 DeepSeek baseline**: `experiments/results/llm_baseline/full300/` — gold_labels.json 有 300 条
- 两者都使用 `AffectiveBenchmark(seed=42, size=100/300)` 生成的任务
- **与 Semi-Real-300 完全一致**: 同样的模板生成，同样的任务集
- `submission_pack_v0_4/llm_baseline_full300_report.md` 已将其定位为 "auxiliary stress test"
- `dataset_equivalence_audit_full300.md` 承认 AB-300 是 "regenerated, not equivalent" to Semi-Real-300

**问题**: 论文主表中的 "Semi-Real-300" 实际上就是 `AffectiveBenchmark(size=300)` 生成的合成模板数据，不是真正的半真实数据。DeepSeek baseline 跑在完全相同的数据上，但 gold labels 来自 `RISK_TO_DECISION` 规则映射（循环验证风险）。

---

## Q5: annotation reliability 完成状态

**未完成。**

- 没有第二标注者的标注结果
- Cohen's kappa 未生成
- `blind_annotation_sample_100.csv` 的 `annotator_label` 和 `annotator_rationale` 列全部为空
- `annotation_reliability_pending_report.md` 已承认 "pending"
- `annotation_protocol_v1.md` 存在但未被执行

---

## Q6: blind annotation / gold / kappa script 路径

| 文件 | 路径 | 状态 |
|------|------|------|
| Gold reference (hidden) | `experiments/annotation/gold_reference_hidden.json` | ✅ 存在，100 条 |
| Blind sample | `experiments/annotation/blind_annotation_sample_100.csv` | ✅ 存在，但标注列为空 |
| Blind sample (with gold hidden) | `experiments/annotation/blind_annotation_sample_100_with_gold_hidden_reference.csv` | ✅ 存在 |
| Generate gold script | `experiments/annotation/generate_gold_reference.py` | ✅ 存在 |
| Generate blind sample script | `experiments/annotation/generate_blind_sample.py` | ✅ 存在 |
| Compute kappa script | `experiments/annotation/compute_kappa.py` | ✅ 存在，但无输入数据（第二标注者标注为空） |

**缺口**: 第二标注者标注结果。没有标注数据，kappa 脚本无法运行。

---

## Q7: README / paper / audit / dataset_card 表述一致性

**基本一致，但有几处微妙差异：**

| 主题 | README | dataset_card | reproducibility_audit |
|------|--------|-------------|----------------------|
| 数据来源 | "Semi-Real-300 benchmark" | "semi-real, template-generated" | "Original source JSON not available" |
| Kappa | "pending" | "pending" | "not completed" |
| DeepSeek 定位 | "auxiliary stress test" | "auxiliary" | "can be fully reproduced" |
| 主表可复现 | 未明确说不可复现 | — | "cannot be independently reproduced" |

**不一致处**:
1. README 暗示 Semi-Real-300 是半真实数据，但 `AffectiveBenchmark` 实际是纯模板生成。`dataset_card` 更诚实（"semi-real, template-generated"），但 "semi-real" 这个词仍然有误导性——60 个手写模板重复 5 次不是 "semi-real"。
2. README 没有明确说主表结果不可复现，但 `reproducibility_audit` 承认了这一点。

---

## Q8: LICENSE / pyproject.toml / requirements / CI

| 项目 | 状态 |
|------|------|
| LICENSE | ❌ 不存在 |
| pyproject.toml | ❌ 不存在 |
| requirements.txt | ❌ 不存在 |
| requirements-dev.txt | ❌ 不存在 |
| setup.py | ✅ 存在（`/workspace/setup.py`） |
| CI workflow (.github/workflows/) | ❌ 不存在 |
| .gitignore | ✅ 存在 |

**严重缺口**: 没有 LICENSE 意味着法律上他人无权使用代码；没有 requirements.txt 意味着无法一键安装依赖；没有 CI 意味着测试通过徽章是假的。

---

## Q9: 根目录临时文件 / zip / 重复包

| 文件 | 大小 | 性质 | 建议 |
|------|------|------|------|
| `files.zip` | 10KB | 临时传输包（benchmark_v2 原始文件） | 删除或移到 archive |
| `revised_files.zip` | 27KB | 临时传输包（修改后的模块） | 删除或移到 archive |
| `rjudge_data/` | — | R-Judge 克隆（第三方数据） | 不应提交到仓库，已加入 .gitignore |

**注意**: 之前的 `dist/*.zip`（teacher_review_pack 和 full_archive）在当前工作目录中不存在，可能已被清理或仅在 origin/main 上。

---

## Q10: experiments/ 一键复现

**不能。**

现有脚本：
- `experiments/benchmark_v2/run_real_benchmark.py` — 能跑 5-fold CV，但产出的是 benchmark_v2 结果，不是论文主表
- `experiments/benchmark_v2/run_rjudge_benchmark.py` — 能跑 R-Judge 外部验证
- `scripts/generate_benchmark_results.py` — 使用 DummyAgent，结果不反映真实组件
- `scripts/generate_figures.py` — 用硬编码数字生成图

**缺口**:
1. 没有 `experiments/reproduce/reproduce_main_tables.py`
2. 没有 `experiments/reproduce/reproduce_figures.py`
3. 论文主表数字与 benchmark_v2 数字不一致，无法统一

---

## Q11: 数据类型和条数

| 数据集 | 类型 | 条数 | 唯一模板 | 来源 |
|--------|------|------|---------|------|
| AffectiveBenchmark-300 | 模板生成（合成） | 300 | 60 | 代码内嵌模板 + random.choice |
| AffectiveBenchmark-100 | 模板生成（合成） | 100 | ~60 | 同上，size=100 |
| DeepSeek LLM baseline (100) | 同上 | 100 | — | AffectiveBenchmark(size=100) |
| DeepSeek LLM baseline (full300) | 同上 | 300 | — | AffectiveBenchmark(size=300) |
| R-Judge (外部) | 真实人工标注 | 571 | 571 | 第三方公开数据集 |
| Blind annotation sample | 模板生成子集 | 100 | — | 从 AffectiveBenchmark 抽样 |

**关键事实**: 所有"主实验"数据都是 60 个手写模板的重复。没有任何真正的半真实或真实部署数据。

---

## Q12: Q2 投稿三大 reviewer attack point

### Attack 1: 主实验是同义反复（致命级）
原始 benchmark 使用 `DummyAgent`，action 完全由 baseline 字符串决定，agent 参数从未使用。消融对照是恒等映射，不是真实机制对比。benchmark_v2 修复了这个问题，但暴露出更深层问题：risk 通路 ≈ 关键词检测器预测按关键词标的标签。5-fold CV 证实 memory 净负、affect 落在噪声里。

### Attack 2: 无独立标注，gold 标签循环验证（致命级）
gold labels 来自 `RISK_TO_DECISION` 规则映射（项目自己写的确定性规则），不是独立人工标注。Cohen's kappa 未完成（第二标注者标注为空）。DeepSeek baseline 的 gold 也是同一套规则。审稿人会指出：你在测"系统能不能复现你自己写的规则"。

### Attack 3: R-Judge 外部验证全面失效（严重级）
在 571 条真人标注的真实数据上，整个框架 unsafe recall = 0.000（risk/memory）或 0.030（full）。关键词检测器对社会工程/钓鱼/隐私泄露类风险完全无效。这直接否定框架的外部效度。

---

## 缺口汇总（按严重程度排序）

| # | 缺口 | 严重程度 | 修复难度 |
|---|------|---------|---------|
| 1 | 主表结果不可复现（DummyAgent 恒等映射 vs 真实组件结果不一致） | 致命 | 高 |
| 2 | 无独立标注，kappa 未完成 | 致命 | 中（需找人标注） |
| 3 | R-Judge 外部验证全面失效 | 致命 | 极高（需重写 risk encoder） |
| 4 | 无 LICENSE | 严重 | 低 |
| 5 | 无 requirements.txt / pyproject.toml | 严重 | 低 |
| 6 | 无 CI workflow | 严重 | 低 |
| 7 | 1 个 pytest 失败（encode_event 回归） | 中等 | 低 |
| 8 | 根目录临时 zip 文件 | 低 | 低 |
| 9 | "Semi-Real-300" 命名误导（实为纯模板生成） | 中等 | 低（改名即可） |
| 10 | 无一键复现脚本 | 中等 | 中 |
