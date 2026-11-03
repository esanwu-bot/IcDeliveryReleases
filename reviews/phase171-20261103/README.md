# Phase 1.7.1 独立审查包（20261103）

> 目标：让 Reviewer 不依赖 GitHub 代码仓库权限，也能完成逐项复核。
> 本包是**自包含**的：基线提交、全部 diff、被测代码、测试、真实样本证据、待验清单。

## 1. 基线（本包对应的代码状态）

```
HEAD = 4572f4a
- `27bdd02` — D1 parse_pdf 接入确定性后处理
- `4951c4b` — D2 stage_llm 落 llm_usage
- `35d4e62` — D3 板卡 thermal/esd 字段级主体归属
- `88d023e` — D1 复核修正（早落 URL / 重试后重取 metadata）
- `9beeb7d` — D3 消费端闭环（canonical_view 按 subject 隔离）
- `19ef765` — D4 PIN|FUNCTION 多封装列布局（待独立验收）
```

> 报告中的测试结果均对应上述基线；`19ef765`（D4）是独立项，**未被本轮 D1–D3 证据复跑覆盖**。

## 2. 先读什么

| 顺序 | 文件 | 用途 |
|---|---|---|
| 1 | `VERDICT.md` | 工程结论、逐项证据、风险与回滚 |
| 2 | `PENDING.md` | 三项未验证内容（服务器五段 / 真实 UG / D4） |
| 3 | `diffs/9beeb7d.diff` | **本轮最关键的新增修复**：D3 消费端闭环 |
| 4 | `diffs/35d4e62.diff` | D3 行级主体标注（上一环） |
| 5 | `code/test_phase171_d3_subject.py` | 四种主体分支 + 幂等 + 发布视图用例 |
| 6 | `evidence/s2-ads8568evm-pdk.json` | 真实 PDF 复跑：11 thermal / 2 esd 全 onboard_device |
| 7 | `evidence/s2-render-view.json` | **HTML 消费端**：芯片参数只在 onboard 横幅段内出现（段外 0 处） |
| 8 | `evidence/tests-phase171.txt` | 测试实跑输出 |

## 3. 代码链路（Reviewer 重点）

```
identity_scope.apply
  → _stamp_row_subjects(): row.subject / subject_source / subject_review
  → scope_contract._row_scope(): 把行级 subject 计入 scope 证据
  → canonical_view(): thermal/esd 与 electrical/absmax 同口径分桶
      onboard_device → specs.onboard_device_specs
      board          → 保留主容器
      ambiguous      → specs.unresolved_specs（待人工）
  → json_to_txt.render(): 入参第一行即 doc = canonical_view(doc)
```

## 4. 四种行级主体（对应 Reviewer 要求）

| 行级主体 | 预期 | 用例 |
|---|---|---|
| `onboard_device` | 移入隔离桶，主容器不再出现 | `test_publication_view_isolates_onboard_thermal_esd` |
| `board` | 保留主容器，不被误隔离 | `test_publication_view_keeps_board_level_thermal` |
| `ambiguous` | 进 `unresolved_specs`，不进任一正式容器 | `test_publication_view_archives_ambiguous_rows` |
| 缺少 `subject` | 按文档 scope 兼容归档，行内容原样保留 | `test_rows_without_subject_follow_doc_scope_without_loss` |
| 重复执行 | 不重复搬迁、不丢行、不改原始 doc | `test_canonical_view_is_idempotent_and_does_not_mutate_source` |

## 5. 复现命令（本机 Windows / Python 3.11+）

```powershell
python -m pytest tests/test_phase171_d3_subject.py -q          # 10 passed
python -m pytest tests/test_scope_contract.py -q               # 36 passed
python docs/qc/phase171/run_samples.py --sample 1              # LM317
python docs/qc/phase171/run_samples.py --sample 2              # ADS8568EVM-PDK
python docs/qc/phase171/run_samples.py --sample 3              # DAC8568EVM 短路
```

> 样本 1/2 会调用真实模型（DashScope），样本 3 断言 0 次调用；三者都把产物写到
> 系统临时目录，并核对 `data/parsed` 指纹（零污染）。

## 6. 不在本包范围内

- 服务器 Docker 同构五阶段复跑（需 Reviewer 在 `/tmp/p17` 执行）；
- 真实 `board_user_guide` PDF（建议 SBAU193E）；
- D4（`19ef765`）的独立验收。

详见 `PENDING.md`。
