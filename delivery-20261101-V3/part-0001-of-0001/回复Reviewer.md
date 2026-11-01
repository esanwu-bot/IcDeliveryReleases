# 回复 Reviewer（1102）

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
| `absolute_max` | 15 | 3 `model_unverified` / 12 `unresolved` |
| `ac_performance` | 82 | 82 `audited_deterministic` |
| `thermal` / `esd` | 5 / 2 | 确定性抽取（无核验状态字段） |

页面上，未核验行带 `†` 角标（本件数据行 33 处），表头有提示条。
所以你现在能一眼看出「哪些是机器抽的、哪些是复现过的」，直接对照 PDF 找真值。

另外新增 `facts_audit.csv`：把 JSON 里每个数值**逐行**回打 PDF，给页码与结论 ——

- `verified` —— 确定性抽取复现，与 JSON 一致；
- `value_on_label_page` —— 数值与参数名**同页**（有出处）；
- `value_in_pdf` —— 数值只在别处出现，归属未证，**不算通过**；
- `partial` / `not_found` —— 需人工。

本包五件**零 `not_found`**：ADC 126 行、ADS1201U 48 行、ADS8568 8 行；
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
