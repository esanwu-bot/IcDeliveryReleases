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

**推荐以 `delivery-20261031-V2` 为准**：它是唯一补齐 6/6 物料的一版，
替代料由 `qwen-flash`（百炼）实跑、图片 SEO 由 `seo_image.build()` 实跑。

### V2 的替代料质量边界（必须读）

5 件里 **4 件站内目录零内链**，其 `alt_html` 是**合法空结构**（明写 "No qualified alternative is
published … / N candidate(s) matched the on-site catalog"），**不是已验证的替代料推荐**；
只有 `ADS1201U-1_1K` 命中站内目录（3 条内链 / 3 条 verified），`alt_html` 是真实表格。
AI 候选保留在各件的 `.alts.json` 里供人工复核，字段 `internal` / `verified` / `similarity` / `basis` 可逐条查。

## 使用边界（每个包内的《交付说明.md》为准）

**打包校验通过 ≠ 工程验收通过。** 全部包均为 `release_status = not_approved`，
**不得直接上线、不得用于电路设计**。`approved` 属人工专属签核，机器不得写入。
包内不含 PDF 原件；`pdf_sha256_recorded` 仅沿用源 JSON 记录，不代表本包对 PDF 重新取证。
四语变体均已生成，但**叙述段存在英文回退**（V2 的 `ADC12DJ5200SE` 88 长段中 73 段仍为英文），
`i18n_complete = not_checked`，**未通过本地化验收**。

## 追溯

源码与全部审计记录在主仓库（Codeup）的 `HANDOFF.md`；本仓库每个包内的
`manifest.json` / `包校验报告.json` 记录逐成员 SHA-256 与最终 ZIP/RAR 哈希。
