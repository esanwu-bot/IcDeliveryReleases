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

**推荐以 `delivery-20261031-V4` 为准**（最新）：V3 复审的四条验收点在 **JSON 与页面两侧同时成立**，
且核心字段**三次独立解析逐字节一致**。

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
包内不含 PDF 原件；`pdf_sha256_recorded` 仅沿用源 JSON 记录，不代表本包对 PDF 重新取证。
四语变体均已生成，但**叙述段存在英文回退**（V2 的 `ADC12DJ5200SE` 88 长段中 73 段仍为英文），
`i18n_complete = not_checked`，**未通过本地化验收**。

## 追溯

源码与全部审计记录在主仓库（Codeup）的 `HANDOFF.md`；本仓库每个包内的
`manifest.json` / `包校验报告.json` 记录逐成员 SHA-256 与最终 ZIP/RAR 哈希。
