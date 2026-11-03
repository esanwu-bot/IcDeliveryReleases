# Phase 1.7.1 最终验收报告（D1 / D2 / D3）

| 项 | 值 |
|---|---|
| 角色 | 架构 Agent（Implementation + 本地复跑） |
| 日期 | 2026-11-03 |
| 范围 | V2 五阶段：确定性对齐（D1）/ LLM Usage（D2）/ 板卡字段归属（D3）+ 三件冻结样本复跑 |
| **结论** | **三项达成；不批准 V2 生产灰度；未生成 V3；交独立 Reviewer 终审** |

> 边界：本报告只给工程结论，**不改** `release_status`、不改人工签核、不扩灰度、不打包。
> `PIPELINE_PASS` ≠ `CONTENT_APPROVED` ≠ `RELEASE_APPROVED`。

---

## 一、结论摘要

| 验收项 | 结果 | 证据 |
|---|---|---|
| D1 确定性后处理接入 V2 | **PASS** | `s1-lm317.json`（34 行 / 0 占位符）+ 五阶段链路用例 |
| D2 LLM Usage 记账 | **PASS** | `d2-llm-usage.json`（2 条真实调用，含失败重试；缓存 0 新增） |
| D3 板卡字段级主体归属 | **PASS** | `s2-ads8568evm-pdk.json`（thermal 11 / esd 2 全 `onboard_device`，发布视图主容器 0/0） |
| 冻结样本 1 LM317 | **PASS** | 热阻 34、`RθJC(bot)` NA/— 不落行、pins 3 |
| 冻结样本 2 ADS8568EVM-PDK | **PASS** | identity=`evaluation_board`、device=`ADS8568`、芯片表入 `onboard_device_specs` |
| 冻结样本 3 DAC8568EVM | **PASS** | `is_datasheet=False` → `skipped`、**0 次模型调用**、无 JSON |
| 生产零污染 | **PASS** | `data/parsed` 文件数/字节/最新 mtime/摘要 **复跑前后完全一致** |
| 本地测试 | **PASS** | 受影响面 **205 passed**（+ `test_scope_contract.py` 36 passed） |

---

## 二、D1 —— 确定性后处理接入 V2

| 项 | 内容 |
|---|---|
| 提交 | `27bdd02`（接入）、`88d023e`（复核修正：早落 `datasheet_url`、重试后重取 metadata） |
| 文件 | `app/services/pipeline.py`（+42 / +22−4）、`tests/test_phase171_d1_deterministic.py` |
| 调用链 | `stage_llm`（默认 `llm_fn = PLATFORM.parse_pdf`）→ `parse_pdf`：模型输出校验 → `DE.apply_deterministic` → `core_validation` → 修复重试 → **再覆盖一次** → 指纹 |
| 复用口径 | 只调用 `qc.deterministic_extract.apply_deterministic`，未复制判据；与 Legacy `parse_one` 同一实现 |
| 测试 | 6 passed（含新增五阶段链路证明：不传 `llm_fn` 走默认实现，落盘 JSON 必带 `metadata.deterministic_extract`，thermal→34） |
| 真实样本 | `docs/qc/phase171/evidence/s1-lm317.json`：status=ok、thermal **34**、placeholder **0**、pins **3**、llm_calls=1 |
| 与 Legacy 差异 | 同一份冻结 PDF + 同一模型输出下 thermal/pins 逐条一致（`test_v2_and_legacy_deterministic_agree`） |
| 风险 | 本轮复跑时 `extract_pins` 对 `PIN | FUNCTION` 两列布局无改写权（LM317 pins 取模型值 3）；并发提交 `19ef765`（D4）已声明支持该布局，但**未在本轮证据中复跑验证**，请 Reviewer 一并核对 |
| 回滚 | `git revert 88d023e 27bdd02`（先撤复核修正再撤接入） |

---

## 三、D2 —— V2 LLM Usage 记账

| 项 | 内容 |
|---|---|
| 提交 | `4951c4b` |
| 文件 | `app/pipeline/stages.py`（+24）、`tests/test_phase171_d2_usage.py` |
| 调用链 | `stage_llm` → 收集本次阶段真实 `llm_calls` → `PLATFORM._log_calls(item_id, mpn_key, calls)`（复用 Legacy，不新写一份） |
| 判据 | 多次调用分别落行；失败调用带 `ok=0` + error；**缓存命中不落任何行**；记账失败只留痕、不拖垮解析 |
| 证据 | `docs/qc/phase171/evidence/d2-llm-usage.json`：`llm_usage_rows` = 2（`parse` attempt1 ok=1、`repair` attempt2 ok=0 `JSONDecodeError: truncated`）；第二次 `stage_llm` = `cached`，行数不增 |
| 测试 | 4 passed（含缓存不记假账、失败不静默丢失、重试两条分别记录） |
| 风险 | `item_id` 依赖任务上下文；脱离 worker 直接调阶段时按 0 记账（已在用例中固定该口径） |
| 回滚 | `git revert 4951c4b` |

---

## 四、D3 —— 板卡字段级主体归属

| 项 | 内容 |
|---|---|
| 提交 | `35d4e62`（行级标注）、`9beeb7d`（**消费端闭环**：发布视图按 subject 隔离） |
| 文件 | `qc/identity_scope.py`（+45）、`qc/scope_contract.py`（`_row_scope` 认 `subject`；`canonical_view` 分桶扩到 thermal/esd）、两个测试文件 |
| 判据 | 主体只认**文档证据**：`onboard_device_datasheet`→`onboard_device`；`board_user_guide`→`board`；判不出→`ambiguous`（`subject_review=needs_human`）。不按参数名/数值猜 |
| 消费端 | `canonical_view`（渲染层实际读取的发布视图）把 `subject=onboard_device` 的 thermal/esd 归入 `onboard_device_specs`；`board` 行保留主容器；`ambiguous` 归 `unresolved_specs` |
| 真实样本 | `docs/qc/phase171/evidence/s2-ads8568evm-pdk.json`：document_scope=`onboard_device_datasheet`；identity=`evaluation_board`/device=`ADS8568`；thermal **11**、esd **2**，`subject` 全为 `onboard_device`、未标注 **0**；发布视图主容器 thermal/esd **0/0**，onboard **11/2**；芯片 electrical/absolute_max 已搬入隔离桶 |
| 测试 | D3 **10 passed**（板载隔离 / 整板保留 / ambiguous 归档 / 缺主体兼容 / 幂等不改源 doc） |
| 渲染消费端 | `docs/qc/phase171/evidence/s2-render-view.json`：`render()` 源码第一行即 `canonical_view(doc)`；芯片 thermal/esd 的**参数名全部只出现在 onboard 横幅段内**（段外 0 处），横幅原文 `The values below describe the onboard ADS8568 device; they are not limits for the assembled board` |
| 风险 | 主体判定依赖 `document_scope`；该字段若误判会连带错归属——本轮以 PDF 首页标题证据复核（SBAS543 确为 ADS8568 器件手册）。板卡 UG 场景由单测覆盖，本轮无真实 UG 样本 |
| 回滚 | `git revert 9beeb7d 35d4e62` |

---

## 五、三件冻结样本复跑

样本与冻结单一致（MPN / URL / PDF 未改）：

| 样本 | PDF | 结果 |
|---|---|---|
| LM317 | `LM317__lm317.pdf`（sha `1646fb2e…`） | ok；thermal 34；placeholder 0；pins 3；1 次模型调用 |
| ADS8568EVM-PDK | `ADS8568EVM-PDK__sbas543c.pdf`（sha `79c02991…`） | ok；identity/device 正确；thermal 11 + esd 2 全主体标注；发布视图隔离完成 |
| DAC8568EVM | `DAC8568EVM__slau301.pdf`（User's Guide） | `is_datasheet=False` → `skipped`（`NOT_A_DATASHEET`）；**0 次模型调用**；**未写 JSON**；不进入 Audit/Render |

生产零污染（三次复跑前后一致）：

```
files=8992  bytes=129255042  newest=2026-11-03 14:06:59
digest=9a089c9c73d3aae61e7855c77924c3ed4c15a90618a6333fdb88ed67aefb3738
```

复跑器：`docs/qc/phase171/run_samples.py`（隔离输出到系统临时目录，生产目录只读）。

---

## 六、测试实跑

```
205 passed, 4 deselected   # pipeline_stages + phase171 D1/D2/D3 + board/identity/bucket/thermal 夹具
 36 passed                 # tests/test_scope_contract.py
 10 passed                 # tests/test_phase171_d3_subject.py（四分支 + 幂等 + 发布视图）
  6 passed                 # tests/test_phase171_d1_deterministic.py（含五阶段链路证明）
```

渲染消费端证据：`docs/qc/phase171/evidence/s2-render-view.json`
（`python docs/qc/phase171/check_render_view.py`；判据是「出现必须被 onboard 横幅覆盖」，
不是「一律不许出现」——板载器件参数在板卡页上属于合法展示，冒充板级限值才是缺陷）。

原始输出：`docs/qc/phase171/evidence/tests-phase171.txt`。

---

## 七、未覆盖项与残差风险（交 Reviewer 判定）

1. **服务器 Docker 五阶段编排未在本机重跑**：`docs/qc/phase17/harness/p17.sh` 依赖服务器
   `/tmp/p17` + `icpdf/app:latest` + Redis DB8。本机以「阶段单元测试 + 真实 PDF 单件复跑」
   替代；`fetch 幂等 / 五阶段接力 / 状态流转` 由 `tests/test_pipeline_stages.py` 覆盖，
   但**生产同构复跑仍需在服务器执行一次**（Reviewer 验收清单第 1 条）。
2. **D3 无真实板卡 UG 样本**：本轮冻结件 ADS8568EVM-PDK 的 PDF 是器件手册；`board_user_guide`
   分支仅有单测覆盖。建议 Reviewer 追加一件真实 EVM UG（如 ADS8568EVM 的 SBAU193E）。
3. **`onboard_electrical` 行数随模型波动**（本轮 71，历史 21/136）：确定性层不治理 electrical
   抽取完整度，属既有风险，不在 D1–D3 范围内。
4. **D3 主体判据粒度**：以 `document_scope` 为证据，而非逐参数查原文段落；若同一 PDF 混有
   板级与器件级参数（部分 EVM UG 附录），仍会被整体归为一类。已记为待办。

---

## 八、发布边界（再次声明）

- 不批准 V2 提升 / 生产灰度；
- 不生成 `delivery-batch20-eval-V3`；
- 不修改 `release_status` / 人工签核；
- 等独立 Reviewer 按本报告逐条复核后，再决定是否进入「8 件重渲染 → V3 打包」。
