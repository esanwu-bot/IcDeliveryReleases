# 回复 Reviewer（V9）

致复核方：先把你这轮的**自我更正**接住，再逐条回。

---

## 0. 关于「en-dash 归因错误」

你更正得对，我们这边也没有异议 —— 但要把**责任分清楚**，别把结论写成「双方都没错」。

- 你的原始归因（`PDF 用 en-dash、审计器拿 ASCII 比`）确实不成立。我们 V4 起就做了
  `_DASHES` 归一（U+2013 / 2014 / 2212 / 2012 / FE63 五码位），V7 里 `-94`、`-4/4`、
  `-0.3/18` 都能命中，就是证据。
- 真因是你说的第二条：`_num_keys()` 把 `-5.0` 收成 `-5`，而旧正则 `(?<![\d.])-5(?![\d.])`
  被原文 `–5.0` 里的 `.` 挡住 —— **两个数只命中一个**，再加 `_derive()` 要求「全中」，
  于是落 `not_found`。
- 但这里我们**没有资格说「所以是误报」**：同一份数据里出现「一个数找到、一个数找不到」，
  交付方就该怀疑自己的匹配口径，而不是等复核方反证。V8 修的是匹配口径，
  同时补了两条用例把「部分命中 ≠ 全部命中」钉死
  （`test_token_pages_matches_padded_zero` / `test_dash_normalisation_covers_all_five_variants`）。

HVSS 现在 `verified_row`、bbox 覆盖整行、全包 `not_found` **1 → 0**，与你的实测一致。

---

## 1. 【新-1】ADS8568EVM 少渲染 24 行 —— 你要求「挑一个」，我们选**第一种**

> 「要么渲染层漏了（那是内容缺失，得补），要么刻意不渲染（那这 24 行就不该进分母、更不该让 13 条弱证据把 anchor_gate 卡成 blocked）」

**定性：渲染层漏了。** 不是刻意的，也不是「审了但不必给人看」。

### 根因（一行代码，两种取数口径）

`json_to_txt.py` 的规格区里，电气表**表体**走的是合并后的取数函数：

```python
_grp = _bucket_groups(_spec_rows(specs, "electrical", is_board))   # 主表 + 隔离桶
```

而**是否渲染**的判断用的是未合并的主表变量：

```python
elec = specs.get("electrical") or []      # ← ADS8568EVM 这里是 []
...
if elec:                                  # ← 于是整张表被跳过
```

ADS8568EVM 的主表 `electrical` 被合同层整锅搬进 `onboard_device_specs`（主表 0 条），
所以 `if elec:` 判空 → 24 条一条都不印。
**同一个隔离桶里，`absolute_max` 走的是 `_spec_rows`，照常印了 11 条** ——
这就是你观察到的「amax 渲染了、electrical 没有」。

### 修法

1. 判断与表体统一走同一个入口：`_elec_all = _spec_rows(specs, "electrical", is_board)`。
2. 页面加显式小节名：**`On-board Device Electrical Specifications (ADS8568)`**（器件名取自数据，五语种）。
3. 归属声明保留并补强：整板限值未给（`Board-level electrical specifications are not stated…`）
   **与**「以下是板载器件、不是整板限值」两句**同时**印 —— 只印前一句会变成「一句声明 + 一片空白」，
   那正是客户验收说「这不是没做完吗」的那一版；只印表不印声明则会回到 `-40~125°C` 那个幻觉。

### 实测（包内 `txt/ADS8568EVM-PDK.txt`，en）

| 项 | V8 | V9 |
|---|---|---|
| 页面表数 | 4 张 / 25 行 | **5 张 / 49 行** |
| 板载电气行 | **0**（JSON 有 24） | **24** |
| `259.7`（功耗）/ `36.6`（IAVDD） | 0 命中 | **各 1 命中** |
| `Power Dissipation` / `IAVDD` / `Isolation` | 0 命中 | **各 1 命中** |
| 页面上「未核验」计数 | 无 | **13 of 24（电气）+ 7 of 11（绝大）** |
| 页面上 `†` | 0 | **22**（表内 20 + 图例 2） |

逐表：

| 表 | 数据行 | `†` |
|---|---|---|
| 电气（板载器件） | 24 | 13 |
| 绝对最大额定值 | 11 | 7 |
| 热阻 | 6 | 0 |
| ESD | 2 | 0 |
| AC 指标 | 6 | 0 |
| **合计** | **49** | **20** |

你担心的「审了、算进分母、卡住闸门，但读者看不见」现在不成立了：
**分母 49 = 页面 49**，13 条弱证据在页面上逐条带 `†`，并有一句
「13 of 24 entries below are marked unverified (†) — …Confirm against the original datasheet before design use.」
闸门为什么 `blocked`，读者在页面上自己就能读到。

> 附带说明：这 24 行里 **0 条**是 `verified_row`（行级指纹），28 条行级证据全部落在
> 另外四个容器。所以 `blocked` 不是新引入的，是这 24 行一直都在、只是以前不给人看。

---

## 2. 【新-2】`facts_verdict=pass` 与 `anchor_gate=blocked` 并存

改的是**措辞**，不是判定口径。两者量的不是一件事：

- `verdict`：有没有 MISMATCH（PDF 里查不到 / 查到的值与交付值对不上）；
- `anchor_gate`：每条是否达到**它那个载体**要求的证据等级。

ADS1201U 是典型：36 条行级 + 11 条正文级全对得上，但
`Differential Input Voltage Range (With VBIAS)` 只有坐标、没有可重放的行指纹。

V9 起 `facts_verdict` 增加第四个取值 **`partial_pass`**，并附一句人话：

```
facts_note = "core fields pass (no MISMATCH); 1 sub-item(s) below the required anchor grade -> anchor_gate=blocked"
```

manifest.csv 新增 `facts_note` 与 `facts_rows` 两列。包内 README 加了三行取值表，
明确写「**不要只看 `pass` 两个字**」。`pass` 现在真的意味着闸门也过了 ——
不会再出现同一行同时写 pass 与 blocked。

---

## 3. 【新-3】正向提示条只覆盖 37/108

你说的是对的，而且比「只覆盖 37 行」更糟：AC 表**连负向提示都没有**。
64 条 AC 参数在 `SYMBOL` 上打了 `†`，却没有任何一句话解释 `†` 是什么 ——
读者只会当成脚注编号。

改法是**按容器全页汇总 + 补负向分支**：

- 全页全锚定时，印一句动态计算的总账（数字由数据算，不写死）：
  `All 108 entries on this page are anchored to the source PDF (electrical 22, absolute maximum 15, thermal 5, ESD 2, AC 64).`
- 只有部分表干净时，正向提示落回**干净的那张表**（读者需要知道是哪一张）。
- AC 表补上负向分支：`{n} of {total} entries below are marked unverified (†)`。

实测：ADC 页 `All 108 entries … AC 64` 命中；ADS8568EVM 印 `13 of 24` 与 `7 of 11`；
ADS1201U 印 `2 of 39` 与 `All 11 entries below are anchored`。

---

## 4. 【新-4】自检不含 `risk_queue` 计数与事实表总行数

manifest 新增 `facts_summary`：

```json
{"facts_rows_total": 214, "facts_audit_rows": 214, "risk_queue_rows": 55,
 "n_mpns": 5, "anchor_gate_blocked": 3}
```

`qc/bundle_selfcheck.py` 新增第 ⑥ 项：拿**包内** `facts_audit.csv` / `risk_queue.csv`
重数一遍，与 `facts_summary` 逐项比对；并按型号核对 `facts_rows`。
对不上就中断出包。自检项：39 → 41。

---

## 5. 【新-5】CDN 缓存 —— 已写进仓库根 README 顶部

按你踩过的坑（jsdelivr 给 16872 字节的 V6 README、raw 是 26028 字节的 V8），
根 README 第一屏加了醒目警告，并给出**固定 commit** 的取法：

```
https://raw.githubusercontent.com/esanwu-bot/IcDeliveryReleases/<commit-sha>/delivery-YYYYMMDD-Vx/manifest.csv
```

> 我们这边也要认一句：**让复核方去分辨 CDN 与 raw，本身就是交付方的问题。**
> 所以另外把「固定 commit + 文件字节数」写进包内《交付说明》，复核方对不上就是我们的错。

---

## 6. 上一轮 P0/P1（V9 施工单）的落点

| 项 | 状态 | 证据 |
|---|---|---|
| **P0-1** JSON `range` 投毒（`column_roles_verified` + `verified_value`） | 已修 | 源头不再产出（`_input_range_row`）；下游 `qc/range_guard.py` 读前校验 + `fact_status_sync` 物理抹除。ADS1201U 那条：`range` 已删、`range_origin=column_roles_unverified`、附 `range_note`。全包抹除 **1** 条 |
| **P1-1** `BOOST-DRV8711` 卖点把板级供电与器件能力混在一句 | 已修 | 拆成 `Board input voltage range: 8.2–52 V.` 与 `Onboard DRV8711 driver capability: up to 4.5 A per H-Bridge (subject to thermal conditions).` |
| **P1-2** ADS8568EVM 的 SEO / JSON-LD 归属 | 已修 | `data_subject: "ADS8568"` + `attribution: "onboard_device"` 强制注入，不依赖正文 |
| **P1-3** 三个反例测试 | 已完成 | `test_verified_value_forbids_column_roles_verified` / `test_onboard_device_forbids_board_level_claim` / `test_anchor_gate_pass_does_not_approve_content` |

`P0-1` 的连带收益：ADC 页面上原来印着 **`to 26.25 dBm`** 这种残句
（`range` 只有上限、下限空串被拼进 `min to max`），现在是 `26.25 dBm`。
这是同一处守卫顺手挡掉的，不在你这轮的清单里，但确实是页面上看得见的错。

---

## 7. 仍未做（如实挂着，不粉饰）

| 项 | 原因 |
|---|---|
| `ADS8568EVM-PDK` `anchor_gate=blocked` | 20 条弱证据（18 `value_on_label_page` + 2 `value_in_pdf`）。这些行的参数名与数值能在 PDF 里复现，但落不到具体表格行。**只能人工翻页定行**，机器做不了 |
| `ADS1201U-1/1K` `anchor_gate=blocked` | 1 条 `Differential Input Voltage Range (With VBIAS)`：原表 `TYP` 格是脚注 `See Note 2`，MIN/MAX 列角色推不出来。已降级并抹除 `range`，**待人工定列** |
| 五型号人工签核 | `CONTENT_APPROVED` / `RELEASE_APPROVED` 只认 `signoff.json`，代码不代签 |
| 五语种人工审校 | `i18n_complete` 只是机械覆盖率；`not_reviewed` 如实挂着 |
| ADS8568 20 条弱证据 | 同上，逐条在 `risk_queue.csv` 里，`suggested_action=human_review` |

**结论：维持 `not_approved`。** ADC 与两块 BOOST 板 `IDENTITY_APPROVED` + `anchor_gate=pass`；
ADS1201U 与 ADS8568EVM 停在 `PACKAGING_PASSED`。

---

## 8. 这一版新增的硬约束（防回退）

新增 `tests/test_v9_fixes.py`（15 条），把你这轮提的每一条都变成断言：

- `test_onboard_device_forbids_board_level_claim` —— 24 行必须在**且**必须声明归属，缺一个都红
- `test_chip_page_ignores_onboard_bucket` —— 隔离桶不回流芯片页
- `test_positive_note_is_page_wide_not_per_table` —— 108 行一句盖全，且 AC 64 要数进去
- `test_partial_page_keeps_per_table_note` —— 部分干净时提示落回干净那张表
- `test_single_ended_range_is_not_readable` —— `to 26.25` 这类残句不许再出现
- `test_anchor_gate_pass_does_not_approve_content` —— 闸门不代签内容审核
- `test_selfcheck_has_facts_and_risk_row_counts` —— 自检必须能重算行数口径

---

## 9. 复核指引（这次请这样取文件）

1. **用固定 commit**，不要用 `cdn.jsdelivr.net` / `raw.githack.com`。
2. 先看 `manifest.csv` 的 `anchor_gate` 与 `facts_verdict`（现在不会再自相矛盾），
   再看 `facts_note` 拿到缺口条数。
3. `ADS8568EVM-PDK` 页面请重点看 **`On-board Device Electrical Specifications (ADS8568)`** 这一节：
   24 行、13 个 `†`、以及紧随其后的那句「Confirm against the original datasheet before design use.」
4. `facts_audit.csv` 里 `verdict` 为 `value_on_label_page` 的行就是那 18 条，可逐条翻页。
