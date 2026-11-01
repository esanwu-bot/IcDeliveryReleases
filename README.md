# IcDeliveryReleases

IcPdfParser 项目的**交付产物发布仓库**。这里只放打包完成的交付包，不放源码、不放运行时数据。

> ## ⚠️ 复核前必读：CDN 有缓存，请用 raw 或固定 commit
>
> **GitHub CDN（`cdn.jsdelivr.net`、`raw.githack.com` 等）存在缓存，可能返回旧版本。**
> 复核时请务必使用 `raw.githubusercontent.com`，或直接固定 commit SHA 拉取：
>
> ```
> # 推荐：固定 commit（永不会被缓存改写）
> https://raw.githubusercontent.com/esanwu-bot/IcDeliveryReleases/<commit-sha>/delivery-YYYYMMDD-Vx/manifest.csv
>
> # 次选：raw + 分支（仍有边缘缓存，必要时加 ?t=$(date +%s)）
> https://raw.githubusercontent.com/esanwu-bot/IcDeliveryReleases/main/...
> ```
>
> 实测教训：V8 复核期间 `cdn.jsdelivr.net` 返回的根 README 是 **16872 字节的 V6 版**，
> 而 raw 源是 **26028 字节的 V8 版**。同一路径、两个内容 —— 复核方按 CDN 读会把
> 已经修好的问题重新提一遍。**不要用 `jsdelivr` 判定本仓库内容。**

## 目录命名规则

`delivery-YYYYMMDD`（当日首版）→ 同日再打包递增 `delivery-YYYYMMDD-V2` / `-V3` …
打包脚本：`delivery_bundle.py --acceptance-root <staging> --out data/delivery-YYYYMMDD[-Vx] --mpns <精确清单>`。
历史命名 `delivery-20261030-fixed` / `delivery-20261030-i18n` 属例外，不新增同类后缀名。
已推送的目录**只追加不修改**（可回溯是对外交付的底线）。

## 本仓库内容

| 目录 | 日期 | 型号数 | 物料齐备 | 多语言 | 状态 |
|---|---|---|---|---|---|
| `delivery-20261030-fixed` | 2026-10-30 | 5 | 3/6（无 alts / seo） | 仅 en | review_candidate / not_approved |
| `delivery-20261030-i18n` | 2026-10-30 | 5 | 3/6（无 alts / seo） | 仅 en | review_candidate / not_approved |
| `delivery-20261031` | 2026-10-31 V1 | 5 | 3/6（无 alts / seo） | en + ja/ko/de/es（**叙述段英文回退**） | review_candidate / not_approved |
| `delivery-20261031-V2` | 2026-10-31 V2 | 5 | **6/6**（alts / seo 已实跑生成） | en + ja/ko/de/es（**叙述段英文回退**） | review_candidate / not_approved |
| `delivery-20261031-V3` | 2026-10-31 V3 | 5 | 5/6 ×4 + **6/6** ×1（4 件替代料门禁归零，`alt_html` 不落盘） | en + ja/ko/de/es（**叙述段英文回退**） | review_candidate / not_approved；`ADC12DJ5200SE` **BLOCKED** |
| `delivery-20261031-V4` | 2026-10-31 V4 | 5 | 5/6 ×4 + **6/6** ×1 | en + ja/ko/de/es | review_candidate / not_approved；核心字段**可复现** |
| `delivery-20261101` | 2026-11-01 V1 | 5 | 5/6 ×4 + **6/6** ×1 | en + ja/ko/de/es | review_candidate / not_approved；三个 P0 **已收口**（`gate`: 2×PATCHED / 3×CLEAN） |
| `delivery-20261101-V2` | 2026-11-01 V2 | 5 | 5/6 ×4 + **6/6** ×1 | en + ja/ko/de/es | review_candidate / not_approved；**原厂 PDF 随包** + 逐行事实表 + 身份硬门禁（`release_state` 最高 `IDENTITY_APPROVED`） |
| `delivery-20261101-V3` | 2026-11-01 V3 | 5 | 5/6 ×4 + **6/6** ×1 | en + ja/ko/de/es | 同上，**数据与物料字节未变**；补《回复Reviewer.md》+ 明写「已含全部原厂 PDF」承诺 |
| `delivery-20261101-V4` | 2026-11-01 V4 | 5 | 5/6 ×4 + **6/6** ×1 | en + ja/ko/de/es | review_candidate / not_approved；**AC 表 82→64 行、零重复、零伪造 MIN/MAX**；amax 15/15 列角色回验；热阻条件列改破折号；韩语模板句补齐 |
| `delivery-20261101-V5` | 2026-11-01 V5 | 5 | 7/8 ×4 + **8/8** ×1 | en + ja/ko/de/es（**覆盖率实测：三件 1.0 / 两件板卡 0.963~0.967**） | review_candidate / not_approved；**板卡参数拆三桶**、**分类面包屑上页面**、**韩语英文模板句清零**、`i18n_complete` 改实测、**`DATA_VALIDATED` 收紧为「每行须锚到具体表格行」** |
| `delivery-20261101-V6` | 2026-11-01 V6 | 5 | 7/8 ×4 + **8/8** ×1 | en + ja/ko/de/es（覆盖率实测：三件 **1.0** / 两件 BOOST `0.9661` / `0.9623`；内容审校 `not_reviewed`） | review_candidate / not_approved；**打包自证链闭环**（清单每个哈希/指标出包前重算，不符即中断）、**唯一状态推导机**、新增 `verified_paragraph`、amax 点线排版确定性抽取、板卡 Thermal/ESD/AC 三段归属声明 |
| `delivery-20261101-V7` | 2026-11-01 V7 | 5 | 7/8 ×4 + **8/8** ×1 | en + ja/ko/de/es（覆盖率：三件 **1.0** / BOOST `0.9661` / `0.9630`；内容审校 `not_reviewed`） | review_candidate / not_approved；**废止 `data_anchor`**，拆成 `row_anchor`/`paragraph_anchor`/`coord_no_fingerprint`/`container_verified` 四列 + `anchor_gate` 总闸；**分母补回隔离桶**（`ADS8568EVM-PDK` 14→49 行，闸门 `blocked`，`release_state` 退回 `PACKAGING_PASSED`）；**文档主体隔离**（`document_subject` / `subject_match`）；自证结论 38 项落盘；JSON 状态与事实表同步；`paragraph_sha256` 归一化口径文档化 |
| `delivery-20261101-V8` | 2026-11-01 V8 | 5 | 7/8 ×4 + **8/8** ×1 | en + ja/ko/de/es（同 V7：三件 **1.0** / BOOST `0.9661` / `0.9630`；内容审校仍 `not_reviewed`） | review_candidate / not_approved；**《交付说明.md》改为打包时按本包 manifest 渲染 + 自检逐格硬拦**（自检 38 → **39** 项）；`anchor_gate` 语义限定到「证据载体达门槛」，README 与包内说明各加**六级证据层级表**；页面五语种提示条补限定；`not_found` 全包 **1 → 0**；`ADS8568` `row_anchor` **19 → 28**、`weak` **28 → 20**；`ADS1201U` 缺列主动降级 → `anchor_gate` 由 pass 变 **blocked** |
| `delivery-20261101-V9` | 2026-11-01 V9 | 5 | 7/8 ×4 + **8/8** ×1 | en + ja/ko/de/es（同 V8，未重跑语言侧车） | review_candidate / not_approved；**三视图出图**（BGA 2D 球阵 + 3D 等轴测按原厂机械图绘制，共享封装图**内联**消除裂图）；**ADS8568EVM 补渲染 24 行板载电气**（页面 25 行/4 表 → **49 行/5 表**，13 条弱证据逐条带 `†`，分母与页面首次对齐）；`facts_verdict` 新增 **`partial_pass`**（`pass` + `blocked` 不再并存）；正向提示条改**按容器全页汇总**（37/108 → **108/108**）；`range` 结构**投毒收口**（`qc/range_guard.py`，全包抹除 1 条，顺带修掉 ADC 页 `to 26.25 dBm` 残句）；`BOOST-DRV8711` 卖点拆板级/器件两句；SEO 侧车注入 `data_subject` + `attribution`；自检 39 → **41** 项 |

**推荐以 `delivery-20261101-V9` 为准**（最新）。V9 处理 V8 全量复核
（工程质量体系 **9.4/10 / Not Approved**）指出的 5 条新发现，并给出「新-1 隐形 24 行」的定性。

**结论：新-1 是渲染层漏了，不是刻意不渲染。** `ADS8568EVM-PDK` 的 24 条板载电气行
以前**一条都没上页面**：表体走合并入口（主表 + 隔离桶），而「要不要渲染」的判断
用的是未合并的主表（该型号主表 0 条）—— `if elec:` 判空，整张表被跳过；
同一个隔离桶里的 `absolute_max` 走的是合并入口，照常印了 11 条。于是变成
**「审了、算进分母、卡住闸门，但读者看不见」**。V9 把两侧统一到同一个入口，
并加显式小节名 `On-board Device Electrical Specifications (ADS8568)`。

| 项 | V8 | V9 |
|---|---|---|
| ADS8568EVM 页面表数 / 行数 | 4 表 / 25 行 | **5 表 / 49 行** |
| 板载电气行 | **0**（JSON 有 24） | **24**（13 条带 `†`） |
| 分母 vs 页面 | 49 vs 25 | **49 vs 49** |
| `259.7` / `36.6` / `IAVDD` / `Isolation` | 0 命中 | **全部命中** |
| ADC 页正向提示覆盖 | 37/108 | **108/108**（含 64 条 AC） |
| ADC 页 `to 26.25 dBm` 残句 | 有 | 无 |
| 自检项 | 39 | **41**（新增事实表/风险队列行数） |

其余四条：`facts_verdict` 新增 `partial_pass`（不再出现 pass + blocked 并存）；
正向提示条按容器全页汇总；`BOOST-DRV8711` 卖点把板级供电与器件能力拆成两句；
SEO 侧车注入 `data_subject` / `attribution`；根 README 顶部加 **CDN 缓存警告**。

`delivery-20261101-V8` 是上一版**收尾版**：不扩张功能，
把 V7 复审（工程质量体系 **9.2/10 / Not Approved**）列的问题做实。

- **P0-1 交付说明与清单割裂 —— 改成生成式 + 硬拦**。V7 包根那份《交付说明.md》
  还是 V6 模板：标题写 `delivery-20261101-V6`、正文写 `ADS8568EVM-PDK 14/14 / DATA_VALIDATED`、
  仍在讲已废止的 `data_anchor`、还把 `ADS1201U` 写成停在 `PACKAGING_PASSED`。
  根因不是"忘了改"，而是它一直**从验收根原样复制** —— 手写文档靠"下次记得改"，
  就一定会有忘的那一次。V8 改两条：
  `delivery_bundle.render_delivery_note()` 使全文由本包 `manifest` + `facts_audit`
  实测值渲染；`qc/bundle_selfcheck.py::_check_delivery_note()` **硬拦** ——
  标题须含本包名、禁止 `data_anchor`、表格逐型号比对 `n_rows` / `row_anchor` /
  `paragraph_anchor` / `weak` / `anchor_gate` / `release_state` 六列，任一项不符即不出包。
  表头抽成 `NOTE_TABLE_HEAD` 常量，生成侧与校验侧同源。
- **P0-2 `anchor_gate=pass` 被读大** —— 新规则明确规定：**`anchor_gate=pass` 只表示
  「证据载体达到门槛」，不等于参数事实已完全正确**。README 与包内说明各加一张
  **六级证据层级表**（坐标定位 → 行/段落指纹 → 列语义核验 → 条件核验 →
  身份与范围核验 → 人工签核），每级写明「证明了什么 / 不证明什么」。
  BOOST 两件的 `paragraph_anchor` 只说明正文段落对得上，
  **不**代表板卡参数的测试条件、供电配置、适用场景已逐条核过。
  页面正向提示条（五语种）同步补限定。
- **P1 弱证据一条都没升级** —— `ADS8568EVM-PDK` 保持 `blocked` / `PACKAGING_PASSED`。
  `row_anchor` 19 → 28 的 9 行是**新拿到坐标**（几何行带锚定），不是放宽门槛：
  每行都按 bbox 回读原文核过，标签与数值同格同值。剩余 20 条弱证据逐条留在 `risk_queue.csv`。
- **一处反向收紧** —— `ADS1201U` 的 `Differential Input Voltage Range` 因
  `missing_cols=min,max` 主动**降级** `verified_row → verified_value`，
  于是该型号 `anchor_gate` 由 `pass` 变 **`blocked`**、`release_state` 退回 `PACKAGING_PASSED`。
  原因：该行 JSON 的 `2 / -20 / +20` 里，`2` 是脚注「See Note 2」的编号被当成了 MIN。
  **指纹一致只能证明整行文本对得上，不能证明值落在哪一列。**
- **自证侧新增**：`facts_audit.csv` 补 `cond` 列（同步键 `(label, cond)` 此前永远对不上，
  ADC 74 行永不同步），升级 78 行；新增 `sha_input` 列，`sha256(sha_input)` 即该行指纹。

> 反向验证：用 V8 的 `qc/bundle_selfcheck.py` 去打 V7 的包，正好红出上述 3 条 ——
> 标题版本号不符 / 仍引用 `data_anchor` / 缺本包实测表。规则确实能拦住这类复发。

实测（`manifest.csv`，2026-11-01 17:36 打包）：

| 型号 | 行数 | `row_anchor` | `paragraph_anchor` | `weak` | `anchor_gate` | `release_state` |
|---|---|---|---|---|---|---|
| `ADC12DJ5200SE` | 108 | 99 | 9 | 0 | pass | IDENTITY_APPROVED |
| `ADS1201U-1/1K` | 50 | 36 | 11 | 0 | **blocked** | **PACKAGING_PASSED** |
| `ADS8568EVM-PDK` | 49 | **28** | 1 | **20** | **blocked** | **PACKAGING_PASSED** |
| `BOOST-DRV8711` | 2 | 0 | 2 | 0 | pass | IDENTITY_APPROVED |
| `BOOSTXL-C2KLED` | 5 | 0 | 5 | 0 | pass | IDENTITY_APPROVED |

`selfcheck passed=true / n_items=39 / n_failed=0`，
`zip_sha256 = 84fcf25109aa5baf7bfd290d3579cc7a67e625883dd73e6a52dd1652be6cea0b`。

**V8 明确没做的事**：五型号人工内容签核（`CONTENT_APPROVED` / `RELEASE_APPROVED`）——
代码不代签；五语种人工语言审校（`i18n_content_review` 仍 `not_reviewed`）；
`ADS8568EVM-PDK` 的 `subject_match=false` 身份问题（缺评估板用户指南，
页面已明写只提供板载 `ADS8568` 芯片数据，**不制造整板参数**）。

### V7 相对 V6 的变化（保留以备追溯）

- **P0 `data_anchor` 口径作废** —— V6 的 `data_anchor` 把 `verified`（容器级复现、**无坐标**）
  也算作"锚定"，于是 `ADS8568EVM-PDK` 在零坐标证据下拉出 `14/14` 并进 `DATA_VALIDATED`。
  V7 拆成四级阶梯，**不是同一件事就不许并进一列**：
  `row_anchor`（行指纹：页 + 表标题 + 左上坐标 + 符号 + min/typ/max + 单位）
  > `paragraph_anchor`（段落指纹）
  > `coord_no_fingerprint`（有坐标无指纹）
  > `container_verified`（只在容器里重现，无坐标）。
  再加**载体分流门槛**：表格参数须 `row_anchor`，正文参数须 `paragraph_anchor`；
  `DATA_VALIDATED` 判据从 `anchored_all is True` 改成 `anchor_gate == "pass"`。
- **更深的洞：分母漏了隔离桶** —— 复审只看到"14/14 太漂亮"，追下去发现
  `onboard_device_specs` / `unresolved_specs` 两个隔离桶的行**根本没进分母**。
  补上后 `ADS8568EVM-PDK` 分母 14 → **49**，实测 19 行级 + 2 段落级，闸门 `blocked`。
  **这条是本版最重要的结论：不是把数字改小，是把分母改对。**
- **文档主体隔离（P0-2）** —— `ADS8568EVM-PDK` 的 PDF 讲的是板载 `ADS8568`，
  清单新增 `document_subject` / `data_subject` / `document_scope` / `subject_match`，
  该型号 `subject_match=false`；BOOST 板走 `device_mpn` 兜底，不误判。
- **自证结论落盘（P1-1）** —— V6 README 说"脚本就在包里"，但包内 62 个成员没有一个 `.py`。
  V7 改为把**逐项结论**写进 `包校验报告.json::selfcheck`：
  38 条 `{item, expected, actual, ok}` + `passed: true`，复核方不必跑代码也能看结论。
- **JSON 与事实表同步（P1-2）** —— 新增 `qc/fact_status_sync.py`，**只升不降**，
  `model_unverified` / `unresolved` 永不升级；`status_prev` 保留原值原样（空串不写占位符）。
  ADC 升级 29 行、ADS8568 8 行、ADS1201U 6 行，2 行保持模型抽取。
- **热阻/ESD 迁入行级锚定（P2-3）** —— 新增 `_raw_lines()`（不设长度阈值，
  修掉 `RθJA` / `23.9` 这类短行被丢弃）与 `_band_row()`（按**几何**找同行数值格：
  同一 y 带 ±6pt + 位于名称右侧 + 纯数值格 + 数值集合非段落超集，不依赖 PDF 阅读顺序）。
  ADC 99 + 9 = **108/108** 全坐标，`ADS8568EVM-PDK` 14/14 全坐标。

实测（`manifest.csv`，2026-11-01 16:30 打包）：

| 型号 | 行数 | `row_anchor` | `paragraph_anchor` | `anchor_gate` | `release_state` |
|---|---|---|---|---|---|
| `ADC12DJ5200SE` | 108 | 99 | 9 | pass | IDENTITY_APPROVED |
| `ADS1201U-1/1K` | 50 | 37 | 11 | pass | IDENTITY_APPROVED |
| `ADS8568EVM-PDK` | **49** | 19 | 2 | **blocked** | **PACKAGING_PASSED** |
| `BOOST-DRV8711` | 2 | 0 | 2 | pass | IDENTITY_APPROVED |
| `BOOSTXL-C2KLED` | 5 | 0 | 5 | pass | IDENTITY_APPROVED |

> 文本物料的 `sha256` **与 `manifest.json::members[].size`** 都按 **CRLF→LF 归一后**计算
> （PDF / ZIP 按原始字节）。这条口径由打包器与 `qc/bundle_selfcheck.py` 共用，
> 仓库根另有 `.gitattributes`（`* text=auto eol=lf`）让检出不再写回 CRLF ——
> 从 GitHub clone 或直接下载散装文件，算出来的哈希与字节数都与清单**一致**；拿 ZIP 更不会有歧义。
> （V7 首版发布后实测：`core.autocrlf=true` 的 Windows clone 会让三个 `.md` 从 11653 变 11856，
> 哈希对得上、大小对不上 —— 已按上述口径重出清单与 ZIP，包内 HTML/JSON/SEO/PDF 一字未改。）

`delivery-20261101-V6` 仍是「自证链闭环 + 唯一状态推导机」那一版，可对照 V7 在锚定层改了什么
（页面内容差异很小，主要差异在事实层与清单列）。

**V6 相对 V5 的要点（保留以备追溯）**：

- **P0 自证链闭环** —— V5 被判「自证链断裂」的原因是「同一天修订重出包，人漏了一步」：
  `manifest.json` 的 i18n 停在 `false / 0.9837`，侧车是 `true / 1.0`，侧车哈希也没重算。
  V6 把修法落到机器上：新增 `qc/bundle_selfcheck.py`（**独立实现，刻意不复用打包器的哈希函数**），
  出包前逐项重算 manifest 里每个 `sha256` 与关键指标，**有一项对不上就 `RuntimeError` 不出包**。
  复核方可跑同一条命令复现：`python qc/bundle_selfcheck.py --out <包根>`。
- **口径统一** —— `facts_audit` 与 JSON 不再各说各话：`qc/fact_acceptance.py` 收成
  唯一状态推导机（九级单调阶梯 + 字段白名单 + 两条不变式逐行核），页面 `†` 只认
  `facts_verdicts.json`。`data_anchor` 从 `88/108` 提到 **`108/108`**，
  `risk_queue` 从 61 行降到 **19 行**（`human_review` 44 → 2）。
- **一处方向修正**：元宝建议把 ENOB / Supply Voltage 那 4 行「降级为 `value_on_label_page`」。
  按同一原则复核后发现方向相反 —— 这 4 行**确实能重放出行指纹**，V5 判「只到同页」
  是因为旧判据用数值**全等**比对（MIN/TYP/MAX 三列行永远不可能全等）。
  修好判据后事实表给的是 `verified_row`（比 JSON 自述更强），所以最终动作是
  「**事实表升级 + 页面跟事实表**」，而不是降级。

`delivery-20261101-V5` 仍是「板卡三桶 + 面包屑 + 韩语清零」那一版，
可用于对照 V6 在打包层与事实层改了什么（页面内容差异很小）。

`delivery-20261101-V4` 是「AC 表去重 + amax 列角色」那一版，数据未变，可对照。
V4 重切行锚点后是 64 行、指纹与内容双唯一、零重复；amax 15 条也全部按
表头判定的列角色回验过（带 bbox 与 row_sha256）。

> **目录命名更正**：V2/V3 曾叫 `delivery-20261102` / `delivery-20261102-V2`。
> 按 AGENT.md §16.1，目录日期必须是打包当天，同一天迭代只递增 `-Vn` ——
> 1101 当天就该是 `-V2` / `-V3`。已改正，并加了 `check_delivery_name()` 硬拦未来日期。

### V5 相对 V4 的变化（两份 8.0 分复审的施工单）

- **板卡参数拆三桶**：`specs.scope` 只有一个值，盖不住「用户指南里整板参数与板载器件
  参数同时存在」。新增 `qc/board_scope.py`，按行打 `attribution`
  （`board_level` / `onboard_device` / `unresolved`），页面分表渲染。
  `BOOST-DRV8711` 现在出两张表：`Voltage Range 8.2 to 52 V`（整板）与
  `Continuous Current per H-Bridge 4.5 A`（板载 DRV8711）不再混在一起。
  `ADS8568EVM-PDK` 挂的是 **ADS8568 器件手册（SBAS543C）**，整板规格源文档里根本没有，
  14 行全归 `onboard_device`，页面段首明写这一点 —— **不假装有整板参数**。
  > 踩坑记录：第一版把 `board_level` 写进 `row["scope"]`，而 `scope` 是合同层
  > 已占用的键（词表只有 `device`/`board`/`onboard_device`/`unresolved`），
  > `normalize_scope()` 不认识 → 归一成 `unresolved` → 行被搬进隔离桶，
  > 唯一一条真整板参数从页面消失且不报错。改键名为 `attribution` 并加回归测试锁死。
- **分类粒度真正上页面**：`category_path` 在 V4 只进了 JSON，页面 0 命中。
  V5 加面包屑，实测 `Integrated Circuits (ICs) › Data Acquisition › ADCs`。
- **韩语页英文模板句清零**：根因不是翻译失败，是渲染器拼接句硬编码英文
  （技术洞察 9 组检查点、封装叙述句、4 组 FAQ 问答）。新增 `_SENTENCE_I18N`
  （五语 22 键）与 `_LIST_JOIN`（德语 `und` / 西语 `y` 不照搬英文逗号）。
  实测纯英文段落 **6 → 0**，静态词条 `key_fallbacks = 0`（109 个词条全命中）。
- **`i18n_complete` 改实测口径**：V4 是写死的 `not_checked` 占位符。V5 由渲染层落盘
  侧车 `<型号>.i18n.json`（随包），清单取**所有语言里最低**的比率。
  实测：`ADC12DJ5200SE` / `ADS1201U-1/1K` / `ADS8568EVM-PDK` **1.0**（`i18n_complete=true`），
  `BOOST-DRV8711` **0.9672** / `BOOSTXL-C2KLED` **0.9630**（缺口是 features / applications
  没有对应语种块，页面回退英文原文）。
  > **同日修订**：V5 初版把 `technical_insight` / `faq` 也判成英文回退（因为它们不在
  > `multi_language` 里），覆盖率被误压到 0.9455~0.9857、`i18n_complete` 全 false。
  > 实际这两块由 `STATIC_I18N` + `_SENTENCE_I18N` 拼出来，页面上是完整的目标语言。
  > 口径已改，包已按新口径重出 —— **指标算错比没有指标更糟**。
- **管脚描述豁免**：`pin_configuration` 的描述是管脚功能名，按 IEEE 器件手册惯例
  保留英文原文，不算未翻译残留。清单加 `pin_desc_exempt` 列，页面加一行小字。
  **豁免仅限引脚表**；features / applications / description / FAQ 不豁免。
- **`release_state` 收紧**：见上文 `data_anchor`。
- **ADS1201 输入范围根因**：V4 里 0 verified 当时归因为「表格太乱」，实际是一个
  `NameError` —— `_SRC_SPLIT_RE` / `_SRC_NUM_RE` 只写了用法没写定义，
  而 `normalize()` 是整段 try，一个拼写错误把后面 3 个确定性步骤全跳过了。
  补定义 + 加 `_step()` 步骤隔离（失败只影响自己，错误写进 JSON 不再静默吞掉）。
  现为 4 条子行、每条带真实 `bbox` + `row_sha256`，电气行 33 `audited_row_anchored`。
- **`†` 计数更正**：V4 说明写的「33 处」从来没被测过，是估的。实测 V4 为
  19 处（18 行 + 1 条提示），V5 为 **10 处（9 行 + 1 条提示）**。

### V2 相对 V1 的变化（评审回应）

ChatGPT 给 1101 打 6.5/10，核心指控是「**这个包不能视为重新核验**」——
包内没有原件，只能相信 `pdf_sha256_recorded`。V2 就是针对这一条做的。

- **原厂 PDF 随包**：每个型号目录带 `<型号>/<型号>.pdf`，manifest 给三个字段
  `pdf_included` / `pdf_sha256_recorded` / `pdf_sha256_packaged` + `pdf_hash_match`。
  五件全部 `match=true`。PDF 与 ZIP 用**原始字节哈希**（`sha256sum` 可直接复核），
  文本物料仍用 `sha256(CRLF→LF)` —— 二进制归一一次哈希就变了，那会让复核方
  永远对不上报告。`zip_sha256` 记的就是 ZIP 文件的原始字节哈希。
  缺件直接不出包（`bundle_acceptance` 抛错），不是「尽量带上」。
  PDF 版权归原厂，仅供本批验收复核，不得单独再分发。
- **逐行事实验收表**（`facts_audit.csv` / `facts_audit.json` / `risk_queue.csv`）：
  把 JSON 里每个数值回打原厂 PDF，分 `verified` / `value_on_label_page`（值与参数名同页）/
  `value_in_pdf`（只在别处出现，归属未证）/ `partial` / `not_found`。
  **五件零 `not_found`**；ADC 126 行、ADS1201 48 行、ADS8568 8 行。
  BOOST 两件标 `partial` —— 板卡件本来就没有器件级参数，不装作有。
- **身份审核成为硬门禁**：1101 的 `ADS8568EVM-PDK` 带着 `identity_state=IDENTITY_REVIEW`
  落了 `CLEAN`，根因是 `_gate()` 根本没读身份字段。现已改：未达
  `{IDENTITY_SUPPORTED, BOARD_CONFIRMED}` 一律 `UNRESOLVED`。该件本版从 `CLEAN` → `UNRESOLVED`。
- **发布状态阶梯**：新增 `release_state`（五级），前三级自动，后两级只读 `signoff.json`。
  `gate` 说「有没有硬伤」，`release_state` 说「走到哪一级」，两者别混读。
- **AC 性能补上**：SNR 24 / SFDR 23 / NSD 7 / IMD3 28（此前页面 0 命中），
  每条带 `fIN` / `AIN` / 模式等测试条件，逐条与 p14 原文核对一致。
- **页面事实一致性**：文档类型（datasheet vs user guide）按 URL 路径判定并落页面；
  修订号 `SLVSGH5C (Rev. C), revised APRIL 2025` 上页面；双句点收口；
  条件占位 17 处由 `unknown` 改破折号 + 一条汇总提示。
- **ADS1201U 链接改回原厂**：第三方镜像 → `ti.com` 直链（`ads1201.pdf`）。
- **仍没做**：ko 页 `technical_insight` / `faq` 两个生成式叙述块只有英文
  （整段不渲染，所以页面无英文残留，但也不算已本地化）、
  SINAD / ENOB / NF 未进 AC 表。详见包内《1101-V4_修复说明.md》§十。

- **新-1 源 PDF 链接恢复**：`datasheet_url` 查表键取了会变的前缀
  （`ADC12DJ5200SEAAV` vs manifest 的 `ADC12DJ5200SEEVM`）导致静默落空。
  现按 PDF 本体名 + TI 文档号两级解析，并**写进核心断言**：为空直接判失败。
  ADC 页 `ti.com` 链接 0 → **2**。
- **新-2 符号页恢复**：确定性抽取覆盖了 `pin_repair` 的成果，`source` 只剩
  `{page, method}`，符号页 fail-closed 退化成"待核"占位页。
  现 BGA 球位只由 `pin_repair` 负责，符号页换行归一后 **sha256 与 V3 完全相同**
  （`06ad6466…`），144 个 `<circle>`。
- **新-3 核验状态恢复**：电气 4/23 + 绝对最大 0/15 → **22/22 + 15/15**，
  页面 `†` 0 → **35**。新增 `model_unverified`（只陈述来源，不主张值错）。
- **指纹**：`pins 3695a8e4…`（与 V3 一致）/ `thermal 4dd75f75…` /
  `esd a594a1e8…` / `vcmi_vid e9baa1ab…`（与 V4 一致）。
- **manifest 补回 `gate` / `gate_reasons`**（V4 掉了这列，"是否已解 BLOCKED"无从判断）。
- **仍缺**：AC 性能（SNR/SFDR/NSD/IMD3）、模型行可复现性（`drift=24`）、
  ko 页 5/16 长段英文（渲染器拼的叙述句没有五语模板）、分类粒度、修订号标注。
  详见包内《1101_修复说明.md》§6。

> V4 的定位不变：它是**第一次真正改对数据**的版本，四验收点（VCMI / VID / 热阻 /
> ESD / amax 15 条）经复审逐条核过全部正确。1101 只补它丢掉的溯源、球图、披露。

- **确定性抽取**：pins / 热阻 / ESD / VCMI / VID 不再由模型输出，改由
  `qc/deterministic_extract.py` 从 PDF 文本层强制抽取。四个指纹三次全等：
  `pins eb2145b8…` / `thermal 4dd75f75…` / `esd a594a1e8…` / `vcmi_vid e9baa1ab…`。
  每个 JSON 自带 `metadata.core_sha256`，复跑后比对即可，不需要装我们的工具。
- **页面侧补齐**：热阻与 ESD 此前**从未被渲染**（JSON 有、页面无，V3 P1-8 的另一半）；
  未核验行加 `†` 角标与表头提示条（五语）；en 页 `<h1>` 改用 `seo.json` 标题（新-5）。
- **验收点可执行**：`ACCEPTANCE_SPECS` / `check_acceptance()` 把四条验收点写成断言。
- **五件来源**：ADC12DJ5200SE / ADS1201U-1_1K / ADS8568EVM-PDK 为本次重解析；
  BOOST-DRV8711 / BOOSTXL-C2KLED 因 `is_datasheet()` 判为 User Guide 而**沿用 V3**
  （`_stage_report.json` 逐件记了 `source` 与 `reason`）。

**仍然不稳的部分**：电气表里模型抽的非核心行两次运行仍会有差异（行名措辞、个别值的写法），
详见包内《V4_修复说明.md》§5.1。这一条没有藏。

V3 逐件闸门判定：`ADC12DJ5200SE` **BLOCKED**（关键参数融合列）/ `ADS1201U-1_1K`、`BOOST-DRV8711`、
`BOOSTXL-C2KLED` UNRESOLVED / `ADS8568EVM-PDK` PATCHED。**没有一件 CLEAN，全部不得上线。**
（该判定针对 V3；V4 的验收口径以包内《V4_修复说明.md》为准。）


### V3 未修的那一条（必须知道）

`ADC12DJ5200SE` 的 `Input common-mode voltage` 仍是 **`0.3 to 0.55`**（原表 MIN 列被融合格吞掉，
应为 `0 to 0.55`）。后处理只动条件串、不动数值；要修只能拿 `PROMPT_VERSION=v3` **重新解析原 PDF**。
该件已被闸门 `fused_column_blocking` 阻断，不会静默流出。

### V2 的替代料质量边界（历史）

5 件里 **4 件站内目录零内链**，其 `alt_html` 是**合法空结构**（明写 "No qualified alternative is
published … / N candidate(s) matched the on-site catalog"），**不是已验证的替代料推荐**；
只有 `ADS1201U-1_1K` 命中站内目录（3 条内链 / 3 条 verified），`alt_html` 是真实表格。
V3 起这些未命中候选**不再进包**（`ADC12DJ5200SE` 的 `AD9680-1000` / `ADS8V11` 等幻觉已剔除），
审计记录留在主仓库 `data/alts/_rejected/`。

## 使用边界（每个包内的《交付说明.md》为准）

**打包校验通过 ≠ 工程验收通过。** 全部包均为 `release_status = not_approved`，
**不得直接上线、不得用于电路设计**。`approved` 属人工专属签核，机器不得写入。

**PDF 随包的版本边界**：`delivery-20261101-V2` 起包内自带原厂 PDF，
`pdf_sha256_packaged` 是对**包内实际文件**重算的哈希，可独立复核；
更早的包（含 1101 及以前）**不含 PDF 原件**，其中的 `pdf_sha256_recorded`
仅沿用源 JSON 记录，不代表该包对 PDF 重新取证。读旧包时不要拿它当证据。
随包 PDF 版权归原厂，仅供本批验收复核使用，**不得单独再分发**。

四语变体均已生成，但**叙述段存在英文回退**（V2 的 `ADC12DJ5200SE` 88 长段中 73 段仍为英文），
`i18n_complete = not_checked`，**未通过本地化验收**。

## 追溯

源码与全部审计记录在主仓库（Codeup）的 `HANDOFF.md`；本仓库每个包内的
`manifest.json` / `包校验报告.json` 记录逐成员 SHA-256 与最终 ZIP/RAR 哈希。

## Automation Verified

本节用于确认自动化流水线能端到端完成一次真实的改动：提交、推送分支、创建 Pull Request。
