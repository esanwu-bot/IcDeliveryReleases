# IcDeliveryReleases

IcPdfParser 项目的**交付产物发布仓库**。这里只放打包完成的交付包，不放源码、不放运行时数据。

## 目录命名规则

`delivery-YYYYMMDD`（当日首版）→ 同日再打包递增 `delivery-YYYYMMDD-V2` / `-V3` …
打包脚本：`delivery_bundle.py --acceptance-root <staging> --out data/delivery-YYYYMMDD[-Vx] --mpns <精确清单>`。

## 本仓库内容

| 目录 | 日期 | 型号数 | 物料 | 状态 |
|---|---|---|---|---|
| `delivery-20261030-fixed` | 2026-10-30 | 5 | 3/6（无 alts / seo） | review_candidate / not_approved |
| `delivery-20261030-i18n` | 2026-10-30 | 5 | 3/6（无 alts / seo） | review_candidate / not_approved |
| `delivery-20261031` | 2026-10-31 V1 | 5 | 3/6；四语变体已生成 | review_candidate / not_approved |

## 使用边界（每个包内的《交付说明.md》为准）

**打包校验通过 ≠ 工程验收通过。** 全部包均为 `release_status = not_approved`，
**不得直接上线、不得用于电路设计**。`approved` 属人工专属签核，机器不得写入。
包内不含 PDF 原件；`pdf_sha256_recorded` 仅沿用源 JSON 记录，不代表本包对 PDF 重新取证。

## 追溯

源码与全部审计记录在主仓库（Codeup）的 `HANDOFF.md`；本仓库每个包内的
`manifest.json` / `包校验报告.json` 记录逐成员 SHA-256 与最终 ZIP/RAR 哈希。
