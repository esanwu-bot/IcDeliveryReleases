# G1 · 服务器 Docker 五阶段同构复跑（2026-11-03）

**执行人**：WB（Trae 下线后接手） · **环境**：`159.89.190.225`（ubuntu-s-8vcpu-16gb-480gb-intel-nyc3-01）
**结论**：三件冻结样本在服务器容器内跑完五段；**生产数据指纹前后完全一致（零污染）**。
日志原件：`docs/qc/phase171/g1_server/`（15 份 worker 日志 + 3 份 probe 报告 + 3 份 run 日志 + 指纹前后文本）。

## 1. 基线

| 项 | 值 |
|---|---|
| 代码 | `git fetch origin main` → **`948c2c2d5eca8e2567b257bcb455affba39eee59`**（与本地 main 同源） |
| 代码落盘 | `git archive 948c2c2 \| tar -x -C /tmp/p171/code`（4641 文件，**不覆盖服务器工作区**） |
| 镜像 | `icpdf/app:latest` → `sha256:b85eff869971`，Created `2026-11-02 04:28:37 UTC` |
| 隔离 | Redis **DB8**；数据根 `/tmp/p171/data_s{1,2,3}`；容器 `p17-s{1,2,3}-{fetch,preprocess,llm,audit,render}` |
| 生产 | `icpdf-server/render/llm/fetch/redis` 一个都没重启 |

代码是**挂载覆盖** `/app` 的（镜像只提供依赖），所以跑的是 948c2c2 的代码，不是镜像里的旧代码。

## 2. 三件样本结果

| 样本 | 终态 | parse_count | 五段 | 关键产物 |
|---|---|---:|---|---|
| s1 `LM317` | **done** (100%) | 1 | preprocess ok 1651ms / llm ok 55490ms / audit ok 43393ms / render ok 265ms，attempts 全 1 | thermal **34**（36→34 确定性复核）、`llm_usage` 1 次 17043 tokens |
| s2 `ADS8568EVM-PDK` | **done** (100%) | 1 | preprocess ok 2169ms / llm ok 132269ms / audit ok 36057ms / render ok 77ms，attempts 全 1 | `onboard_device_specs` 13，主容器 thermal **0** → D3 datasheet 分支在服务器侧同样成立；`llm_usage` 1 次 27589 tokens |
| s3 `DAC8568EVM` | **skipped** | 0 | preprocess skipped | `NOT_A_DATASHEET`（User's Guide），**0 次模型调用** —— 与 Reviewer 的观察一致 |

PDF 实收 SHA256：s1 `1646fb2e4f8c…`（2,578,150 B）、s2 `79c029913ea9…`、s3 `a7e7253da4b3…`。
`idem_key` 每件各段都带 PDF SHA 前缀，重复投递可幂等判定。

## 3. 零污染证据（同一套命令，跑前跑后各一次）

```text
dir=/www/wwwroot/icpdfparser/data/parsed
  files=13539  bytes=281419444
  digest=acf8d167bb360afc933f0468840c08af2ec4fe410a93069c89deb808c9a1a6c4      ← 前后一致
db=/www/wwwroot/icpdfparser/data/workbench.sqlite3
  sha256=d93d65851f773169cace5754defdb326af616500d69cbda430adfb8c2bfa074c
  size=95834112  mtime=2026-11-01 10:51:53                                     ← 前后一致
icpdf-server restarts=0  started=2026-11-02T08:49:54Z                          ← 前后一致
icpdf-render restarts=0  started=2026-11-01T10:51:54Z
icpdf-llm    restarts=0  started=2026-11-01T10:51:54Z
icpdf-fetch  restarts=0  started=2026-11-01T10:51:54Z
icpdf-redis  restarts=0  started=2026-10-24T01:38:44Z
```

跑完 `diff prod_before.txt prod_after.txt` 在生产那一段 **无差异行**；
隔离容器已 `docker rm`，Redis DB8 只留 5 个 kombu 绑定键，DB0（生产）未动。

## 4. 两处必须如实说明的边界

1. **`fetch` 段没有独立的阶段行**：三件都是 `provider=manual`（给定 URL 直供下载），
   阶段表里是 `preprocess/llm/audit/render` 四行，采集记录在 `doc_source`
   （`provider=manual, stage=direct, ok=1, bytes=…`）。所以严格说是
   **采集 + 四段**，不是「网络抓取 + 五段」；不把 manual 直供写成爬虫抓取。
2. **生产 Redis DB0 的键数没取跑前基线**（只记了跑后 2581）。
   零污染结论以 `data/parsed` 全目录内容 SHA、sqlite 全文件 SHA、
   五个容器 `RestartCount`/`StartedAt` 三项为准，这三项都是前后一致的。

## 5. 与 LM317 引脚的分歧（见 D4 报告）

服务器 s1 的 LM317 最终 `pins=4`（模型稿含一条重复的 `OUTPUT 4`），
而本地同代码复跑是 `pins=3`。这不是环境问题，是模型输出差异触发了同一条判据的两个方向，
详见 `docs/qc/phase171/D4_PIN_VERIFY_20261103.md`。
