# 最终审核裁决（RELEASE_APPROVED）

> **本文件的状态：结构已建好，Reviewer 原文待粘贴。**
>
> 下方「一、可核验事实」全部可由本仓库内的文件与 git 历史独立重算，已核对无误。
> 「二、Reviewer 原文」一栏**留空**——那段裁决文字产生于 Reviewer 与我方之外的会话，
> 我方无法凭记忆复述一段审核结论。**审核意见不能由被审核方代写**：代写的那一刻，
> 这份文件就不再是证据，而是伪造的证据。请把原文粘进第二节即可。

---

## 一、可核验事实（不依赖任何人的口头结论）

| 项 | 值 | 怎么自己验 |
|---|---|---|
| 封存提交 | `c8a2ab634bdffe2fda2a552374fef2d47956ed18` | `git rev-parse v3.1-release-approved^{commit}` |
| 批准标签 | `v3.1-release-approved`（附注 tag） | `git tag -n99 -l v3.1-release-approved` |
| 交付包 | `delivery-batch20-eval-V3-RELEASE-V3.1` | `ls` |
| ZIP 文件 | `part-0001-of-0001.zip` | — |
| ZIP 字节数 | `16460487` | `stat -c %s <zip>` |
| **ZIP SHA-256** | `7a8b9bed874796cd6113e9031dd83bff0c49036914e0e99216ca280e011590be` | `sha256sum <zip>` |
| `facts_audit.json` raw SHA-256 | `c20e1420e603721d5aca537aa9fd880e9ffdcfe32009f0d4a058935a7aaf080a` | `unzip -p <zip> facts_audit.json \| sha256sum` |
| `risk_queue.csv` raw SHA-256 | `f85ba0161ca88349638a761ca281631e97d905482429b1b9aaec1eebfbbaa6a6` | `unzip -p <zip> risk_queue.csv \| sha256sum` |
| 审计锚点文件 | `独立哈希复核记录.txt`（仓库根目录） | — |
| 锚点文件 SHA-256 | `1a3c777a906e84f3250134d208f392e051893cca80c2d84e991b95d0ac356f7e` | `sha256sum 独立哈希复核记录.txt` |
| 包内自检 | 42 项 / 0 失败 / pass | `python -c "import json;print(json.load(open('delivery-batch20-eval-V3-RELEASE-V3.1/包校验报告.json'))['selfcheck'])"` |

复核流程与逐条命令见 `独立哈希复核记录.txt` 第六节。

---

## 二、Reviewer 原文

<!-- ↓↓↓ 请在此处粘贴 Reviewer 给出的《最终审核裁决》全文，从「二进制取证通过」
         到「工程验收和未批准维度仍未通过」为止。粘贴后本节即成为本轮审核的正式记录。 -->

```
（待粘贴 Reviewer 原文）
```

---

## 三、裁决边界摘要（用户转述，待与原文核对）

在原文到位之前，先记下两条**必须同时成立**的边界，避免任何一方被单独引用：

1. **二进制取证通过** —— ZIP 的 SHA-256、字节数、内部成员哈希三项与提交的签核记录
   逐字节一致；证据链（提交 → 记录 → ZIP → 成员）无断点。
2. **工程验收与未批准维度仍未通过** —— `release_status` 与 `engineering_validation`
   仍为 `not_approved`；`anchor_gate` 仍为 `blocked`；
   `electrical_pin_mapping_unverified` 仍在每件的 `excluded_dimensions` 里；
   引脚使用边界警告继续生效。

> **这两条不能合成一条用。** 把 1 说成「全部通过」，是把取证合格洗成工程合格；
> 把 2 说成「没通过」，是把已批准的发布放行抹掉。二者量的是不同的东西。

---

## 四、本次批准**不**代表什么

- 不代表 `anchor_gate` 由 `blocked` 变为 `pass`——机器审计未获坐标级证据这一事实未变。
- 不代表引脚数据可用于自动接线、封装选型或逆向工程。
- 不代表未列入 `approved_dimensions` 的维度获得了任何形式的规格承诺。
- 不代表本包可作为完整规格书对外发布。

本包是**受限数据发布包**，批准范围逐件列在
`delivery-batch20-eval-V3-RELEASE-V3.1/交付说明.md` 与 `README.md` 的
「受限数据发布」小节。
