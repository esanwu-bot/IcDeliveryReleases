# 五型号独立目录交付包

## 状态与使用边界

**打包校验通过不等于工程验收通过，不应直接上线或用于电路设计。**
本模式只装配指定验收根里已经生成的物料，不查数据库、不在打包时重渲染。
参数是否已按指定页缓存修订，以随包《交付说明.md》和 manifest 的 release_status 为准。
TXT内容原字节复制为HTML，symbols文件统一为.symbols.html。
《修复方案.md》是审计要求；它本身不是修复已经完成的证明。
原47/47或83/83报告不沿用，打包校验通过不代表工程参数、对象归属或本地化验收通过。

## 组织格式

```text
manifest.csv                    五型号总清单（UTF-8 BOM，Excel可打开）
manifest.json                   每件状态/缺项、物料来源与SHA-256
README.md                       本说明
修复方案.md                     已有复核方案
包校验报告.json                 ZIP路径/源哈希/CRC校验（仅打包层）
facts_audit.csv / facts_audit.json  逐行 PDF 事实验收表（有则随包）
part-0001-of-0001.zip            五件一卷，内含五个型号独立目录
part-0001-of-0001/               与ZIP相同的解压检查目录
  <型号>/<型号>.json
  <型号>/<型号>.html
  <型号>/<型号>.symbols.html
  <型号>/<型号>.pdf              原厂 PDF 原件（1102 起必带）
```

分卷根同时带总清单、说明及已有修复方案。每型号的物料集中于其独立文件夹，
不再使用parsed/txt/symbols三个平行交付目录。原型号中斜杠仅在文件名中替换为下划线，
例如ADS1201U-1/1K对应ADS1201U-1_1K；JSON和总清单保留请求型号。

## 原厂 PDF 随包（1102 起）

**本包已包含全部原厂 PDF 原件，复核方可对照包内 PDF 逐行复核任意一条参数。**

每个型号目录内附原厂 PDF 原件，复核方可**独立**重算哈希、翻到指定页逐行对照，
不必依赖清单里的 `pdf_sha256_recorded` 自证。清单同时给出两个哈希：

- `pdf_sha256_recorded` —— 源 JSON 解析时记录的哈希；
- `pdf_sha256_packaged` —— 本包内 PDF 的实测哈希（原始字节，不做换行归一）；
- `pdf_hash_match` —— 两者是否一致。**不一致即 `gate=BLOCKED`**：随包原件与被解析的
  不是同一份文件时，它的存在比不放更有误导性。

PDF 是二进制，哈希按原始字节计算；文本物料仍按 `sha256(CRLF→LF)` 归一，
两者不可混用。

## 物料缺项与语言

本批实际存在的物料以manifest为准。未发现的.alts.json、.alts.html、.seo.json
不从全局旧目录补齐，不伪造替代料或图片SEO侧车。JSON内seo/alternatives不等于这些独立物料。
PDF原件随包，清单给出记录哈希、实测哈希与是否一致三项；随包PDF哈希不一致直接BLOCKED。
源JSON可含multi_language内容，但是否已有独立ja/ko/de/es页面另列；目录名i18n是命名约定，
不是五语完整性声明。语言未检查状态为not_checked，缺少变体明确列为missing_html_languages。

### `.alts.html` 缺失时的前端契约（V6 明确）

部分型号在站内目录里**没有合格替代料**（`only_linked=True` 会滤掉所有未命中目录的
型号），此时只产出 `<型号>.alts.json`，**不生成** `<型号>.alts.html`。这不是缺件：

- `.alts.json` 是数据契约（`alternatives[]` 数组，含 `mpn` / `brand` / `url` / `relation`）；
- `.alts.html` 只是同一份数据的**静态片段**，方便直接贴进页面。

**前端请直接读取 `.alts.json` 动态渲染。** 把 `.alts.html` 当必需物料会在这些型号上
得到「缺失」的假告警；`manifest` 的 `missing` 列里 `alt_html` 就是这个含义。
无替代料时**不要**回退到全站搜索或上一批的旧片段 —— 那是把「没有」说成「有」。

### `i18n_complete` 与 `i18n_coverage`（V5 起为实测值）

V4 及之前 `i18n_complete` 恒为 `not_checked` —— 那是个占位符，不是结论。
V5 起由渲染层落盘 `<型号>.i18n.json` 侧车，打包器只读不重算（打包是「装配已有物料」模式）：

- `i18n_complete` —— `true` / `false` / `not_checked`（无侧车）。**所有语言**都无回退才为 `true`；
- `i18n_coverage` —— 实测覆盖率，取**所有语言里最低**的那个（只报最好看的数字等于没报）。
  分母 = 静态词条调用次数 + 叙述块数，分子 = 真的落到目标语言的。

### 两件事被拆开了：`i18n_coverage` 与 `i18n_content_review`（V6）

V5 的 `包校验报告.json` 里只有一个 `i18n_validation`，同时被问两个问题，于是它答
`not_checked` —— 而清单里已经有实测覆盖率。复核方一眼看出这是**自相矛盾**。
根因是两件事被塞进了一个字段：

| 字段 | 谁给结论 | 含义 |
|---|---|---|
| `i18n_coverage` | 机器（渲染层侧车） | `measured` = 覆盖率已逐语言实测；`not_checked` = 没有侧车 |
| `i18n_content_review` | 人工语言审校 | `not_reviewed` = 本管线**不做**译文质量审校，只看覆盖率 |

**覆盖率不等于译文质量**：`ratio=1.0` 只说明「没有回退到英文」，不说明「译得对」。
需要语言审校时，它是一条独立工序，不能由这个字段代签。

### 自证链自检（V6 起强制）

打包最后一步会跑 `qc/bundle_selfcheck.py`：把 `manifest.json` 里的每个 `sha256`、
`i18n_complete` / `i18n_coverage` / `data_anchor` / `pdf_hash_match` / `artifacts`
都从**包内文件重算一遍**，任何一项对不上就中断打包。

复核方可以自己跑同一份脚本复核：

```bash
python qc/bundle_selfcheck.py --out delivery-20261101-V6
# 通过 → 退出码 0；不一致 → 逐项打印差异
```

它刻意不复用打包器的哈希函数 —— 共用同一个函数的话，函数写错了自检也会跟着错。

### `pin_desc_exempt`：管脚描述保留英文（豁免声明）

`pin_configuration` 的描述文字**按硬件工程标准保留英文原文**，不属于未翻译残留：
IEEE 器件手册与封装规格里，`VDD`, `AGND`, `SDO/SDI`, `No connect` 这类管脚名与
功能描述在业界按英文原样引用，译成目标语言反而与读者手上的 datasheet 对不上。

清单中 `pin_desc_exempt=true` 表示该型号适用此豁免。页面在非英文语种下也有一行小字说明，
不让读者误以为是漏翻。**除此之外的叙述段（features / applications / description /
technical insight / FAQ）不豁免**，仍按实测覆盖率考核。
V6 起该列恒为 `true` / `false` 两种取值：V5 把「不适用」写成空串，读者分不清
「不适用」和「没算」，与「`not_checked` 被当成结论」是同一类问题。
三块板的.symbols.html是板卡说明页，不伪造芯片三视图；两颗芯片符号仍须核对原厂。
应用图是站点共享素材，本包不复制公共图片，也不把图片路径视为芯片参数证据。

## 发布状态阶梯（release_state）

`gate` 只说「有没有待处理的硬伤」，`release_state` 说「走到哪一级了」。五级只进不退：
| 状态 | 判据 | 能否自动判定 |
|---|---|---|
| `PACKAGING_PASSED` | 四件必带物料齐备 + 随包PDF与记录哈希一致 | 是 |
| `DATA_VALIDATED` | `core_validation=pass` **且**事实验收表无 MISMATCH **且**每一行有数值的工程参数都锚定到原厂表的具体行（`data_anchor` 分子等于分母） | 是 |
| `IDENTITY_APPROVED` | `identity_state` 为 `IDENTITY_SUPPORTED` / `BOARD_CONFIRMED` | 是 |
| `CONTENT_APPROVED` | 页面与多语言通过人工审核 | **否，只认签核** |
| `RELEASE_APPROVED` | 人工签核放行 | **否，只认签核** |

代码**不会**自称通过内容审核或获准发布：后两级只读 `signoff.json`，
没有签核就停在 `IDENTITY_APPROVED`。`identity_state=IDENTITY_REVIEW` 的型号
不会落到 `IDENTITY_APPROVED`，也不会被 `gate` 判成 `CLEAN`。

### `DATA_VALIDATED` 自 V5 起收紧（必读）

**`facts_verdict=pass` 不等于参数全对。** 它只表示「没有编造出来的数值」——
一个数只要在同一页出现过就算 pass，而 180 页的手册里「同页」几乎是必然的。
ChatGPT 8.0 复审原话：「同页命中证明不了归属」。

所以 V5 起 `DATA_VALIDATED` 额外要求 `data_anchor` 的分子等于分母，即每一行
有数值的工程参数都锚定到了**原厂表的具体行**（带 `bbox` + `row_sha256`，可从 PDF 重放）。
达不到就停在 `PACKAGING_PASSED`，缺口在 `data_anchor` 列直接写成 `已锚定/总行数`。

### V5 起主力件降级是**口径变化**，不是数据退步（V6 补）

V4 的 `ADC12DJ5200SE` / `ADS1201U-1/1K` 是 `IDENTITY_APPROVED`，V5 掉到
`PACKAGING_PASSED`。**参数没有变差，是尺子变严了**：V4 把「数值与参数名同页」
算作通过（`facts_verdict=pass`），V5 起改判为「未锚定」，于是 `data_anchor`
从满格掉出缺口，阶梯自然下退。

V6 又往前走了一步：`verified_paragraph`（正文条目级坐标）与更严的行指纹重放
把大部分行补了回来（`data_anchor` 见清单），但仍**不追认**「同页命中」。
所以看到主力件停在低档时，请对照 `data_anchor` 与 `risk_queue.csv`，
不要直接读成「这一版不如上一版」。

三档结论的口径：

| `data_anchor` | 含义 |
|---|---|
| `37/37` | 每一行都锚到了具体表格行 —— 可判 `DATA_VALIDATED` |
| `35/37` | 有 2 行只到「同页」或无可锚数值 —— 停在 `PACKAGING_PASSED`，缺口可见 |
| 空 | 本包没带 `facts_audit.json`，未检查 |

**这不是退步，是把原本藏在 `pass` 里的缺口摆到台面上。** V4 的
`facts_verdict=pass` 覆盖了 `value_on_label_page`（同页命中）这一档，
读者会把它读成「已逐行核对」。V5 不再允许这种读法。

## gate 四态的准确含义

`gate` 是**产物内证据的汇总**，不是验收结论。四态语义如下，请勿把 `CLEAN` 读成「已签核」：

| 取值 | 含义 | 是否可上线 |
|---|---|---|
| `BLOCKED` | 溯源链断（无源 PDF 链接）、引脚映射被隔离，或**随包 PDF 与记录的哈希不一致** | 否，不该出现在包内 |
| `UNRESOLVED` | 核心校验未过，或**身份未审核**（`IDENTITY_REVIEW` 等） | 待人工，不是通过 |
| `PATCHED` | 生成后经确定性归一改过（去应力行、补 URL、补温度单位、重建球位等），`gate_reasons` 列明改了什么 | 取决于 `release_state` |
| `CLEAN` | 上述硬伤与修补痕迹都没有 —— **只表示「没动过、没拦下」** | 仍需 `release_status` 与 `release_state` 判定 |

`PATCHED` 与 `CLEAN` 都不代表参数正确。真正的放行看 `release_status`
（本包全部为 `not_approved`）与 `release_state`（最高只到 `IDENTITY_APPROVED`，
`CONTENT_APPROVED` / `RELEASE_APPROVED` 必须人工签核）。

## 页面片段与 SEO 侧车（交付契约）

本包的 HTML **是内容片段，不是整页**：每个 `.html` 以 `<div class="pd-wrap">` 开头，
**不含** `<html>` / `<head>` / `<title>` / `<meta>` / `<link rel="canonical">` / `hreflang`。
这是契约，不是缺漏——片段由独立站前端框架套壳时注入头部。

因此：

- 标题、meta description、keywords、多语标题在 `<型号>.seo.json` 的 `page` 节点；
- 多语叙述段在 `<型号>.ja.html` / `.ko.html` / `.de.html` / `.es.html` 片段内；
- 片段里的 `<h1>` 已使用 `seo.json` 对应语种的标题（注入管线只接到 h1，未接 head）；
- 复核时**请勿**把「片段没有 `<title>`」判为缺陷，应判「框架是否注入」；
- 若需求方要求整页交付，须先改本契约并同步渲染层，不能靠片段自带头部。

## 核验状态与可复现性（V4 起）

- 电气表 / 绝对最大表里带 `†` 的行，表示**管线自己判定该行未核验**
  （`verification.status` 不是 `audited`）。表头上方给出「N 项未核验」提示条。
  这是披露，不是渲染缺陷。
- 每个 `<型号>.json` 的 `metadata.core_sha256` 记录四个核心字段
  （`pin_configuration` / `specs.thermal` / `specs.esd` / VCMI+VID）的 sha256。
  复跑同一份 PDF 后比这四个值即可判断产物是否可复现；不一致请拒收并回报。
- **绝对最大表自 V3 起可靠性降级**：V3 起多数行被标为未核验，
  V2 时代「6/6 正确」的结论不适用于 V3 及以后的包。

## 校验边界

包校验检查恰好五件、ZIP成员正斜杠无路径穿越、无重复成员、CRC正确、
源文件/独立目录/ZIP成员SHA-256相同，并保存最终ZIP的哈希。
校验报告存于ZIP外，以免报告引用最终ZIP哈希形成循环。
**哈希口径：文本物料 sha256 按 CRLF→LF 归一化后计算**，与平台无关；报告 `hash_rule` 字段
显式记录该口径。若直接对原始字节算哈希，Windows 写出的 CRLF 与 git clone 得到的 LF
会得出不同值（实测同一文件 752afff8… 与 df10bcd6…），那不是数据被改，是换行符差异。

**例外：PDF 与 ZIP 按原始字节哈希，不做归一。** 二进制里 0x0D 0x0A 是内容的一部分，
归一一次哈希就变了 —— 那会让复核方拿 `sha256sum` 算出的值永远对不上报告，
比不给哈希更误导。`zip_sha256` 记的就是 ZIP 文件的原始字节哈希。
