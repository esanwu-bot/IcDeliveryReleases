# 回复 Reviewer（delivery-20261101-V5）

> 基线是 `delivery-20261101-V4`（元宝 8.0 分复审 / ChatGPT 8.0 分终审）。
> 本版只做那两份复审点名的三件事 + 两处 P1，**不新增任何宏观功能**。
> 每条都能在包内自证 —— 页码、`bbox`、`row_sha256`、覆盖率分子分母都在产物里。

---

## 一、V5 改了什么（一张表看完）

| # | 你提的 | 等级 | V4 | V5 |
|---|---|---|---|---|
| 1 | 韩语页 6 段英文模板句 | P1 | 6 段 | **0 段**（`key_fallbacks=0`） |
| 2 | `category_path` 没上页面 | P1 | 0 命中 | **面包屑已渲染** |
| 3 | 板载芯片参数混进整板规格 | P1 | 混在一张表 | **三桶分表** |
| 4 | `i18n_complete` 是自述 | P1 | 恒 `not_checked` | **实测覆盖率** |
| 5 | 管脚描述被判未翻译残留 | P2 | 无豁免声明 | **`pin_desc_exempt: true`** + 页面小字 |
| 6 | `release_state` 口径过宽 | P1 | `pass` 即可 `DATA_VALIDATED` | **每行须锚到具体表格行** |
| 7 | 文档自相矛盾 | P2 | §6.4 说做了、§四说没做 | **统一**（见 §四） |
| 8 | `†` 计数「33 处」 | P2 | 估的 | **实测**（见 §三） |

---

## 二、参数来源透明化（更新到 V5）

`ADC12DJ5200SE` 本包的实际分布（`<型号>.json` 里逐行可查）：

| 容器 | 行数 | 核验状态 |
|---|---|---|
| `electrical` | 22 | 9 `audited_row_anchored` / 4 `audited_deterministic` / 9 `label_value_same_page` |
| `absolute_max` | 15 | 15 `audited_deterministic`（`column_roles_verified`，带 bbox） |
| `ac_performance` | 64 | 64 `audited_deterministic`（`value_shape` 佐证列角色） |
| `thermal` / `esd` | 5 / 2 | 确定性抽取 |

V5 的分档比 V4 细了一级：

- `audited_row_anchored` —— 锚到**原厂表的具体行**，带 `bbox` + `row_sha256`，
  可从 PDF 重放；
- `label_value_same_page` —— 数值与参数名**同页**，但行/列对应未证，页面打 `†`。

这 9 行 `label_value_same_page` 是：`Sampling Rate`（10.4 / 5.2 GSPS）、
`Noise Floor`（-149 / -151.5）、`Noiseless Aperture Delay Step`、`Maximum Lane Rate`、
`Decimation Options`、`NCOs per DDC`、`Power Consumption`。
锚不到的原因分两类：多子行拼一个区间（如 `Input bandwidth -3dB range` 在 p17 是
Low 2.0 / High 6.3 两行，JSON 写 `2 to 6.3`，行身份确定但**列角色不成立**），
或参数名与原表符号差异过大。已全部进 `risk_queue.csv` 的 `human_review` 队列。

`ADS1201U-1/1K` 电气行：**33 `audited_row_anchored` + 4 `audited_deterministic` +
2 `model_unverified`**（V4 是 0 verified / 46 same_page / 2 unchecked）。

---

## 三、`†` 角标计数更正（原先的「33 处」是估的）

V4 说明里写「本件数据行 33 处」。**这个数从来没被测过。**

实测口径：`†` 字符在英文页出现总次数 = 单元格角标数 + 提示条里那一个。

| 型号 | V4 | V5 |
|---|---|---|
| `ADC12DJ5200SE` | 19（18 行 + 1 条提示） | **10（9 行 + 1 条提示）** |
| `ADS1201U-1/1K` | 50（48 行 + 2 条提示） | **15（13 行 + 2 条提示）** |
| `ADS8568EVM-PDK` | 0 | **0** |
| `BOOST-DRV8711` | 3（2 行 + 1 条提示） | **4（2 行 + 2 条提示）** |
| `BOOSTXL-C2KLED` | 6（5 行 + 1 条提示） | **6（5 行 + 1 条提示）** |

`BOOST-DRV8711` 从 3 涨到 4，是因为电气表现在拆成「整板」与「板载器件」两张，
各带一条提示条 —— 不是退步。

---

## 四、仍然没做的（不藏，且与上表不矛盾）

1. **SINAD / ENOB / NF 没进 AC 表**。`_AC_SYMBOLS` 是白名单，加符号会连带引入
   未经验收的行；ENOB 8.5 目前只在 Features 里出现。
2. **`technical_insight` / `faq` 只有英文**。这两块是**生成式内容**，不是硬编码模板，
   要走 `multi_language` 补齐。它们目前**整段不渲染**（不是渲染成英文），
   所以页面没有英文残留；但也不算已本地化，`i18n_complete` 因此是 `false`。
   实测覆盖率 0.9794~0.9837。
3. **ADC 20 行仍是 `value_on_label_page`**。锚不到具体表格行的，已进
   `risk_queue.csv` 的 `human_review` 队列。不猜、不硬凑。
4. **BOOST 两件有 `value_in_pdf`**（1 / 3 行）。板卡件本来就没有器件级参数表，
   这些值散落在正文段落里，无法锚到表格行，`verdict=partial` 如实标注。

> **上一版 §四 与 §6.4 自相矛盾**：§6.4 说「韩语页残留英文模板句 0」，
> §四 却说「ko 页 5/16 长段英文，本版没做」。两句都是我们写的，只能有一句对。
> 事实是 V4 没做、V5 做了（`key_fallbacks=0`）。本节只列**V5 真的没做**的，
> 已做的都放在 §六 逐条说明，两边不再各说一套。

---

## 五、状态

`release_status` 保持 `not_approved`。`CONTENT_APPROVED` / `RELEASE_APPROVED`
两级只认 `signoff.json`，机器不会代填。

**V5 起 `DATA_VALIDATED` 收紧了，请注意看 `data_anchor` 列。**
`facts_verdict=pass` 不等于参数全对 —— 它只表示没有编造的数值。
现在 `DATA_VALIDATED` 还要求每一行有数值的工程参数都锚定到原厂表的具体行：

| 型号 | `data_anchor` | `release_state` |
|---|---|---|
| `ADC12DJ5200SE` | 88/108 | `PACKAGING_PASSED` |
| `ADS1201U-1/1K` | 31/50 | `PACKAGING_PASSED` |
| `ADS8568EVM-PDK` | 14/14 | `DATA_VALIDATED`（身份未审核，止步于此） |
| `BOOST-DRV8711` | 0/2 | `PACKAGING_PASSED`（`verdict=partial`） |
| `BOOSTXL-C2KLED` | 0/5 | `PACKAGING_PASSED`（`verdict=partial`） |

这看起来像「退步」，其实不是：V4 的 `pass` 覆盖了 `value_on_label_page`
（同页命中）这一档，读者会把它读成「已逐行核对」。V5 不再允许这种读法。

---

## 六、V5 对两份 8.0 分复审的逐条答复

### 6.1 「板载芯片参数不能漏进整板规格」—— 成立，已拆三桶

`specs.scope` 只有一个值，盖不住用户指南里两类参数都有的情况。
新增 `qc/board_scope.py`，按四条判据给每行打 `attribution`：

1. 源文档是器件数据手册 → 全部 `onboard_device`；
2. 用户指南 + 命中整板接口词汇（电源输入 / 连接器 / 跳线 / 指示灯 / 散热 / 外形）→ `board_level`；
3. 命中片内模块词汇（H 桥 / 栅极驱动 / 电荷泵 / 步进细分）→ `onboard_device`；
4. 其余 → `unresolved`，不猜。

板级判据**先**过：`Power Input Voltage` 里也有 `voltage`，顺序反了会判错。

实测：

| 型号 | 源文档 | 整板 | 板载器件 | 未定 |
|---|---|---|---|---|
| `BOOST-DRV8711` | User's Guide | 1 | 1 | 0 |
| `BOOSTXL-C2KLED` | User's Guide | 5 | 0 | 0 |
| `ADS8568EVM-PDK` | **SBAS543 器件手册** | 0 | 14 | 0 |

`ADS8568EVM-PDK` 挂的 PDF 是 ADS8568 的器件手册，整板的电源/连接器规格
**根本不在那份文件里**。所以它一行整板参数都没有 —— 页面段首明写这一点，
不假装有。

页面上 `BOOST-DRV8711` 现在出两张表：

```
Board-level parameters
  Voltage Range                    8.2 to 52 V    External power supply input

On-board device parameters
  Continuous Current per H-Bridge  4.5 A          Max continuous
```

**踩到的坑，一并说清楚**：第一版把 `board_level` 写进 `row["scope"]`，
而 `scope` 是合同层已占用的键（词表只有 `device`/`board`/`onboard_device`/`unresolved`）。
`normalize_scope()` 不认识 `board_level` → 归一成 `unresolved` → 合同层判定冲突 →
**两行全被搬进 `unresolved_specs`**，`Voltage Range 8.2 to 52 V` 从页面上消失，
不报错、不告警，表只是空了。改法是换键名（`attribution`），并加回归测试锁死。

### 6.2 「`category_path` 已进 JSON 但页面 0 命中」—— 成立，已渲染

`json_to_txt.py` 加了面包屑 `<nav class="pd-crumb">`，取 `basic_info.category_path`，
缺失时退回 `category › subcategory`，两者都没有就不印。

实测：`ADC12DJ5200SE` / `ADS1201U-1/1K` → `Integrated Circuits (ICs) › Data Acquisition › ADCs`；
`BOOST-DRV8711` → `Boards & Development Tools › Development Boards / Evaluation Boards`；
`BOOSTXL-C2KLED` → `Evaluation Boards & Kits › Power Management Evaluation Kits`。

### 6.3 「韩语页残留英文模板句」—— 已清零，根因是渲染器不是翻译

根因不是 `multi_language` 缺 key，是**渲染器拼接句硬编码英文**：
技术洞察的 9 组设计检查点、封装叙述句、4 组 FAQ 问答都写在 Python 里。

现新增 `_SENTENCE_I18N`（五语 22 键）与 `_LIST_JOIN`（连接词按语种，
德语的 `und`、西语的 `y` 不能照搬英文逗号）。6 段硬编码英文全部改模板。

实测：`ADC12DJ5200SE` 渲染后正则提取所有 `>40` 字符的 `<p>`，检测韩文字符 ——
**V4 是 6 段，V5 是 0 段**；静态词条 `key_fallbacks = 0`（109 个词条全部命中）。

**但覆盖率不是 100%，如实写**：`i18n_coverage = 0.9794~0.9837`，
缺口是 `technical_insight` 与 `faq` 两个生成式叙述块（只有英文，整段不渲染）。
所以 `i18n_complete = false`。这是实测，不是失败。

### 6.4 「63 个英文 `<li>` 是管脚描述」—— 判断为不该翻，加豁免声明

`pin_configuration` 的描述是管脚功能名（`VDD` / `AGND` / `SDO/SDI` / `No connect`）。
IEEE 器件手册与封装规格里这类文字按英文原样引用，译成目标语言反而与读者手上的
datasheet 对不上 —— 这是工程惯例，不是漏翻。

做法三条：

1. `manifest.csv` 新增 `pin_desc_exempt` 列，`true` 表示适用；
2. 非英文语种页面上印一行小字说明；
3. 豁免**仅限** `pin_configuration`。features / applications / description /
   technical insight / FAQ **不豁免**，仍按实测覆盖率考核。

三件板卡件 `pin_desc_exempt=false` —— 它们没有引脚表，没有可豁免的对象。

### 6.5 「`i18n_complete` 是自述不是实测」—— 已改口径

打包器是「只装配已有物料」模式，不允许打包时重渲染一遍来算覆盖率
（那会让清单里的数字与实际交付的 HTML 不是同一次渲染的产物）。
所以由渲染层落盘侧车 `<型号>.i18n.json`，打包器只读，
并取**所有语言里最低**的比率 —— 只报最好看的数字等于没报。

### 6.6 「`release_state` 释义要收紧」—— 已收紧

见 §五。新增 `data_anchor` 列，直接写「已锚定/总行数」，缺口不再藏在 `pass` 里。

### 6.7 「ADS1201 输入范围」—— 根因不是表格乱，是一个 `NameError`

V4 里 `ADS1201U-1/1K` 的 `facts_audit` 是 0 verified，当时归因为表格复杂。
实际根因：`_SRC_SPLIT_RE` / `_SRC_NUM_RE` 两个常量**只写了用法没写定义**，
`fill_row_sources()` 在参数名带括号的型号上抛 `NameError`；而 `normalize()`
那时是整段 try —— 一个 NameError 把后面 3 个确定性步骤
（`input_ranges` / `absolute_max_roles` / `row_anchors`）全部跳过了。

修法两条：补常量定义；加 `_step()` 步骤隔离（失败只影响自己，并把
`metadata.normalize.<step>_error` 写进 JSON，不再静默吞掉）。

实测 4 条子行，每条带真实 `bbox` + `row_sha256`：

| 参数 | 值 | 条件 | bbox |
|---|---|---|---|
| Absolute Input Voltage Range | 0 to +5 V | — | `[36.7, 115.8, 540.8, 125.8]` |
| Absolute Input Voltage Range | -10 to +10 V | With VBIAS(1) | `[36.7, 124.8, 540.8, 134.8]` |
| Differential Input Voltage Range | -5 to +5 V | — | `[36.7, 133.8, 540.8, 143.8]` |
| Differential Input Voltage Range | -20 to +20 V | With VBIAS(1) | `[36.7, 142.8, 540.8, 152.8]` |

`0 to +5` 与 `-10 to +10` 的 MIN/MAX 不再互相污染，`With VBIAS(1)`
只挂在真正带 VBIAS 的那两行。
