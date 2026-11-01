# 回复 Reviewer —— `delivery-20261101-V7`

> 本文只回答「你提的哪一条、怎么改的、改到什么程度、哪一条没改」。
> 所有数字都能用包内 `facts_audit.csv` / `risk_queue.csv` / `包校验报告.json` 重算。

---

## 一、8.9 分复审（`data_anchor` 口径）—— 已彻底拆分

**你指出的问题**：`verified`（容器级复现，无坐标）被计入 `data_anchor`，
于是 `ADS8568EVM-PDK` 14 行**一条坐标都没有**却拿到 `14/14` 并进入 `DATA_VALIDATED`。
「弱证据冒充强证据」。

**V7 的做法**：

1. **`data_anchor` 废止**。`manifest.csv` 拆成四列 + 一个闸门：
   `row_anchor` / `paragraph_anchor` / `container_verified` / `coord_anchor` / `anchor_gate`。
   `container_verified` 单独成列，**永远不计入达标**。
2. **门槛按载体分流**：表格参数须 `row_anchor`；正文参数（板卡 bullet、
   Features 条目、点线排版 amax）须 `paragraph_anchor`。`REQUIREMENT` 是唯一来源。
3. **`DATA_VALIDATED` 只认 `anchor_gate=pass`**；原来那个由打包器现算的
   `anchored_all` 已删除 —— 打包器不再自己给自己发合格证。
4. **载体判定不许用结论反推**：只读 JSON 的载体声明；同步回写的状态带
   `status_source` 标记，判载体时忽略它，否则会出现「升级状态→降低门槛」的自证回路。

---

## 二、但你指出的口径问题**比表面更深 —— 分母本身漏行**

补完上面三条之后，我们复查了「分母从哪来」，发现一个更难看的事实：

> **V6 的 `ADS8568EVM-PDK 14/14`，是 49 行里的 14 行。**

板卡件的板载器件参数在 `specs.onboard_device_specs`（隔离桶）里，渲染层会把它并回页面
（`json_to_txt._spec_rows`），而 **事实审计只遍历了主表** —— 页面上 11 条绝对最大值、
24 条板载器件电气行，从来没进过分母。

V7 把隔离桶纳入遍历（`BUCKETS` + `iter_container_rows`），ADS8568 的分母从 14 变成 49：

| 型号 | 页面行数 | `row_anchor` | `paragraph_anchor` | 弱证据 | `anchor_gate` |
|---|---|---|---|---|---|
| ADC12DJ5200SE | 108 | 99 | 9 | 0 | **pass** |
| ADS1201U-1/1K | 50（分母 48） | 37 | 11 | 0 | **pass** |
| **ADS8568EVM-PDK** | **49** | **19** | **2** | **28** | **blocked** |
| BOOST-DRV8711 | 2 | 0 | 2 | 0 | pass |
| BOOSTXL-C2KLED | 5 | 0 | 5 | 0 | pass |

`ADS8568EVM-PDK` 因此**退回 `PACKAGING_PASSED`**，28 行按弱证据如实印 †。
这不是「改坏了」，是那张虚高的 `14/14` 本来就不该存在。

---

## 三、V6 复审 新-1：自证脚本不在包内 —— 改为「结论落盘」

**声明与产物不符**这一点我们认。V6 的 README 写「脚本就在包里」，包里 62 个成员没有 `.py`。

V7：

* `qc/bundle_selfcheck.py::report()` 产出逐项 `{item, expected, actual, ok}` + `passed`；
* 整块写进 **`包校验报告.json::selfcheck`**，未通过直接拒绝出包；
* README 改成：「脚本本体不进包（仓库只放交付物），**结论逐项落盘**，
  复核方可挑任意一条自己核」。

---

## 四、V6 复审 新-2：JSON 自述未随事实表升级 —— 已同步

`qc/fact_status_sync.py`：`label_value_same_page` → `audited_paragraph` 这类
「过程性描述被更强结论取代」的升级做了；`model_unverified` / `unresolved`
**永不升级**（那是出处不可信，事实表只能证明数值在原文出现过）。
每行另写 `fact_verdict` / `fact_grade` / `fact_source`，下游不必 join CSV。

**实测**：ADC 升级 29 行、ADS8568 升级 8 行、ADS1201U 升级 6 行、保持 2 行（模型抽取）。

同步会改变内容，因此**同步之后重算 `core_sha256`**（不拿旧指纹给新内容背书），
`core_validation` 复算仍为 `pass`。

---

## 五、V6 复审 新-3：`paragraph_sha256` 口径未文档化 —— 已写清并给可跑片段

你按「原样 / 空白折叠 / 小写」三种归一各试一遍 0/9，是因为少了两步：
**破折号统一**与 **`page|` 前缀**。README 现在给出计算式与可直接运行的代码。
`facts_audit.csv` 另增 `sha_scheme` 列，标明这一行属于哪套指纹：

| `sha_scheme` | 计算式 |
|---|---|
| `row` | 抽取器表格行：page / 表标题 / 左上坐标 / 符号 / min / typ / max / unit |
| `band` | `sha256(page|名称格|数值格)` —— 热阻 / ESD 这种横向两格表 |
| `paragraph` | `sha256(page|归一化行文本)` |

---

## 六、V6 复审 新-7 / 新-4：热阻 / ESD 终于有行坐标

V4~V6 停在容器级的原因是三个技术事实：这两张表是**横向两格**、`find_tables()` 抽不出行、
`_page_lines()` 会把 <6 字符的行（`RθJA`、`23.9`）整行丢掉。

V7 新增**行带锚定**：同一 y 带（±6 pt）、位于名称右侧的纯数值格，坐标取两格并集，
指纹 `sha256(page|名称格|数值格)`；**唯一才认领**（多页或多行命中直接放弃）。

顺带修好 `_row_shas()` 只读 `source.row_sha256` 的问题（AC 表是平铺结构），
`ADS8568EVM-PDK` 的 6 条 AC 行因此恢复行级锚定。

---

## 七、V6 复审 新-5：全锚定时印正向结论

ADC 页 `†` = 0 是 108/108 全锚定的结果，但此前**正面结论没有展示**。
V7 起某张表全部达标时印一条正向提示（五语种齐备）：

> All 22 entries below are anchored to the source PDF — each value was replayed
> against a specific table row or text entry (page + bounding box + reproducible fingerprint).

---

## 八、七条反例：已变成测试（24 条用例全绿）

`tests/test_v7_anchor_gate.py` 逐条对应你列的反例：无坐标不计行级、正文证据不冒充行级、
同页多同名数值不认领、芯片手册用于评估板不冒充整板、MIN/TYP/MAX 丢列要报警、
`i18n_coverage=1.0` 不触发人工审校、无签核不得 `RELEASE_APPROVED`。
另有两条锁住「自检重算的锚定列必须与清单一致」和「只有容器级证据必须 blocked」。

---

## 九、仍然没做的（不粉饰）

| 项 | 状态 |
|---|---|
| 五型号人工签核 | 未做，`release_status` 全部 `not_approved` |
| 多语言人工审校 | 未做，`i18n_content_review = not_reviewed` |
| `ADS8568EVM-PDK` 28 行弱证据 | 未解决，已进 `risk_queue` 的 `human_review` |
| `Input Negative Supply Voltage (HVSS)` | 数值在原文未出现（`not_found`），列入 `exclude_or_verify` |
| ADS1201U `Offset Error` / `Gain Error` | 行内无数值，不进分母，也不假装已提取 |
| 生命周期 / RoHS / REACH / MSL | 未做 |

---

## 十、结论

**V7 不是一个「更绿的包」，是一个「更诚实的包」：**

* 锚定口径拆开了，容器级再也不能冒充坐标级；
* 分母补全了，`ADS8568EVM-PDK` 从 `14/14` 变成 `49 行里的 19+2`，闸门变红；
* 自证结论落盘，复核方不必相信「我们跑过了」；
* 热阻 / ESD 拿到了真正可重算的行带指纹。

`release_status` 仍为 `not_approved`，`DATA_VALIDATED` 只剩四件（且只描述文档对象）。
