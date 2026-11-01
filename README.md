# IcDeliveryReleases

IcPdfParser 项目的**交付产物发布仓库**。这里只放打包完成的交付包，不放源码、不放运行时数据。

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
| `delivery-20261101` | 2026-11-01 | 5 | 5/6 ×4 + **6/6** ×1 | en + ja/ko/de/es | review_candidate / not_approved；三个 P0 **已收口**（`gate`: 2×PATCHED / 3×CLEAN） |
| `delivery-20261102` | 2026-11-02 | 5 | 5/6 ×4 + **6/6** ×1 | en + ja/ko/de/es | review_candidate / not_approved；**原厂 PDF 随包** + 逐行事实表 + 身份硬门禁（`release_state` 最高 `IDENTITY_APPROVED`） |

**推荐以 `delivery-20261102` 为准**（最新）：唯一一版**包内自带原件**的交付，
复核方可独立重算哈希、可逐行翻页对照，不再依赖发布说明。

### 1102 相对 1101 的变化（评审回应）

ChatGPT 给 1101 打 6.5/10，核心指控是「**这个包不能视为重新核验**」——
包内没有原件，只能相信 `pdf_sha256_recorded`。1102 就是针对这一条做的。

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
- **仍没做**：amax 列角色（p8 表 `find_tables` 识别不出，表头在 p9 续页，
  跨页拼接风险大于收益）、ko 页 5/16 长段英文（渲染器拼的叙述句缺五语模板）。
  详见包内《1102_修复说明.md》§十。

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

**PDF 随包的版本边界**：`delivery-20261102` 起包内自带原厂 PDF，
`pdf_sha256_packaged` 是对**包内实际文件**重算的哈希，可独立复核；
更早的包（含 1101 及以前）**不含 PDF 原件**，其中的 `pdf_sha256_recorded`
仅沿用源 JSON 记录，不代表该包对 PDF 重新取证。读旧包时不要拿它当证据。
随包 PDF 版权归原厂，仅供本批验收复核使用，**不得单独再分发**。

四语变体均已生成，但**叙述段存在英文回退**（V2 的 `ADC12DJ5200SE` 88 长段中 73 段仍为英文），
`i18n_complete = not_checked`，**未通过本地化验收**。

## 追溯

源码与全部审计记录在主仓库（Codeup）的 `HANDOFF.md`；本仓库每个包内的
`manifest.json` / `包校验报告.json` 记录逐成员 SHA-256 与最终 ZIP/RAR 哈希。
