# 回复 Reviewer（delivery-20261101-V4）

> 针对 1101 复审的核心指控 ——「**这个包不能视为重新核验**，包内没有原件，
> 只能相信 `pdf_sha256_recorded`」——本包做了三件事。下面每条都能在包内自证。

## 一、PDF 原件已入包

五个型号目录下各带该型号原厂 PDF 原件：`<型号>/<型号>.pdf`。

`manifest.csv` 给四项，五件全部 `pdf_hash_match = true`：

| 字段 | 含义 |
|---|---|
| `pdf_included` | 是否随包（本包五件全 `true`） |
| `pdf_sha256_recorded` | 源 JSON 解析时记录的哈希 |
| `pdf_sha256_packaged` | **本包内该 PDF 实测**的哈希（原始字节，不做换行归一） |
| `pdf_hash_match` | 两者是否一致；`false` 直接 `gate=BLOCKED` |

你现在可以：

1. 直接翻包内 PDF 核对任意一条参数；
2. 用 `sha256sum` 独立重算，与 `pdf_sha256_packaged` 对照 —— 口径是**原始字节**，
   不是归一化后的值，所以标准工具算出来就该一样；
3. 若 `pdf_hash_match` 为 `false`，说明随包件与被解析的不是同一份文件，
   那种情况下它的存在比不放更误导，所以闸门直接判 `BLOCKED`。

## 二、门禁逻辑收紧

`IDENTITY_REVIEW` 不再能落 `CLEAN`。

1101 的 `ADS8568EVM-PDK` 带着 `identity_state=IDENTITY_REVIEW` 却标了 `CLEAN`，
根因不是标注疏忽 —— `_gate()` 原先**根本不读身份字段**。现已改为：

- 身份必须 ∈ `{IDENTITY_SUPPORTED, BOARD_CONFIRMED}`，否则 `gate=UNRESOLVED`，
  理由写 `identity_state=...`；
- 本包该件已由 `CLEAN` → `UNRESOLVED`。

同时新增 `release_state` 五级阶梯（`PACKAGING_PASSED → DATA_VALIDATED →
IDENTITY_APPROVED → CONTENT_APPROVED → RELEASE_APPROVED`），
前三级自动，后两级**只读 `signoff.json`**，代码不代签。本包最高 `IDENTITY_APPROVED`。

README 里也补了 `gate` 四态语义表，明确 **`PATCHED` / `CLEAN` 都不代表参数正确**：
`CLEAN` 只表示「没动过、没拦下」。

## 三、参数来源透明化

`ADC12DJ5200SE` 本包的实际分布（`<型号>.json` 里逐行可查）：

| 容器 | 行数 | 核验状态 |
|---|---|---|
| `electrical` | 22 | 4 `audited_deterministic` / 14 `model_unverified` / 4 `unresolved` |
| `absolute_max` | 15 | 15 `audited_deterministic`（`column_roles_verified`，带 bbox） |
| `ac_performance` | 64 | 64 `audited_deterministic`（`value_shape` 佐证列角色） |
| `thermal` / `esd` | 5 / 2 | 确定性抽取（无核验状态字段） |

页面上，未核验行带 `†` 角标（本件数据行 33 处），表头有提示条。
所以你现在能一眼看出「哪些是机器抽的、哪些是复现过的」，直接对照 PDF 找真值。

另外新增 `facts_audit.csv`：把 JSON 里每个数值**逐行**回打 PDF，给页码与结论 ——

- `verified` —— 确定性抽取复现，与 JSON 一致；
- `value_on_label_page` —— 数值与参数名**同页**（有出处）；
- `value_in_pdf` —— 数值只在别处出现，归属未证，**不算通过**；
- `partial` / `not_found` —— 需人工。

本包五件**零 `not_found`**：ADC 108 行、ADS1201U 48 行、ADS8568 8 行；
BOOST 两件标 `partial`（板卡件本来就没有器件级参数，不装作有）。
`risk_queue.csv` 100 行是待处理清单，每行带 `suggested_action`。

## 四、仍然没改的两条（不藏）

1. **amax 列角色**：p8 那张表 `find_tables` 识别不出，表头在 p9 续页。
   跨页拼接的错位风险大于收益，本版没做，仍按既有三条判据处理应力行。
2. **ko 页 5/16 长段英文**：已定位到五句，根因是渲染器拼的叙述句缺五语模板，
   不是翻译失败。要修得加模板，本版没做。

## 五、状态

`release_status` 保持 `not_approved` 不变。我们等你的核对结果再做正式发布签核 ——
`CONTENT_APPROVED` / `RELEASE_APPROVED` 这两级只认 `signoff.json`，机器不会代填。

## 六、V4 对两份 7.5 分复审的逐条答复

### 6.1 「82 行里 48 行 `min == typ == max`，18 行逐字节重复」—— 成立，已根治

指控我们独立复现过：`Counter({'mintypmax': 48, 'typ': 31, 'mintyp': 3})`。

根因不在模型，在**切行方式**：按文本 y 聚类会把「条件列合并单元格里的多行文本」
当成多行数据，一条逻辑行裂成 3~4 条，叠上单值纵向传播就变成 4 条相同记录。

现行做法是「行 = 所有单元格 y 边界的排序并集」的相邻对，网格线即行线，不重叠。
结果 **82 → 64 行，指纹唯一 64、内容唯一 64、重复 0**，与你们算出的
「64 个唯一组合」一致。列角色也不再传播：单值行只填 TYP，MIN/MAX 留空。

闸门 `check_ac_integrity()` 已进 `check_core()`：`MIN=TYP=MAX`、`MIN=MAX` 无
`value_shape` 佐证、`value_shape` 与实填不符、`row_sha256` 撞车，四条任一命中即判失败。
拿旧 82 行数据喂进去是 96 条错误，新 64 行是 0 条。

### 6.2 「amax 15 条列角色仍未由代码确认」—— 已确认

`fill_absolute_max()` 改为「参数名 token 求交 + 数值全等」双路匹配，
**15/15 全部升级为 `column_roles_verified`，0 unmatched**，
每行带 `bbox` 与 `row_sha256`。单值行（Tj / PMAX / IMAX(ALL)）只填 MAX。

### 6.3 「热阻表 7 处 `Datasheet conditions apply.` 没改」—— 确实漏了，已改

上一版说明称改了 17 处，实际只改了电气表 10 处。现在热阻 + ESD 与电气表统一：
无条件印破折号，表末一条汇总。实测出现次数 0。

### 6.4 「ko 五句模板」—— 已补，且找到根因

根因是**渲染器拼接句**（技术洞察的 9 组设计检查点硬编码英文），不是
`multi_language` 缺 key。现全部进 `STATIC_I18N`，ja/ko/de/es 齐备；
板卡器件短语也一并进词表。韩语页残留英文模板句 0。

### 6.5 「受控分类表 / ADC 细粒度」—— 已做

新增 `qc/taxonomy.py`：`Data Converters` → `Data Acquisition / ADCs`，
判据是型号前缀 + 描述词，两者都指向不同结论时**不猜**。
输出 `basic_info.category_path`，不改 `subcategory`（它已进 H1 句子）。

### 6.6 仍然没做（不藏）

* **SINAD / ENOB / NF 没进 AC 表**。`_AC_SYMBOLS` 是白名单，加符号会连带
  引入未经验收的行；ENOB 8.5 目前只在 Features 里出现。
* 生命周期 / RoHS / REACH / MSL 未补。
* `facts_audit` 的 `value_on_label_page` 占比仍高，本轮只把 AC 与 amax
  迁进确定性抽取。
