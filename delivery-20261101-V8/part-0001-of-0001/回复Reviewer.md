# 回复 Reviewer（V7 复审 → V8）

感谢 9.2/10 的评价。您认可的那句「主动暴露问题，而不是只负责生成通过报告」，
正是这套自动化的设计目标 —— 所以 V8 没有加新功能，只把您列的收尾项做实。

## 先说您点出的 P0：交付说明确实是 V6 的

您判断正确，而且比"标题没改"更严重：正文里 `14/14`、`DATA_VALIDATED`、
`data_anchor`、「ADS1201U 停在 PACKAGING_PASSED」全是 V6 的结论，
与 V7 的 manifest 正面冲突。

根因不是"忘了改"，而是 `交付说明.md` 一直**从验收根原样复制**。手写文档靠
「下次记得改」，就一定会有忘的那一次。V8 改成**打包时生成**：
`render_delivery_note()` 直接吃本包 `manifest` 与 `facts_audit` 的实测值渲染，
并在 `bundle_selfcheck.py` 里加了硬拦 —— 逐格比对标题版本号、审计行数、
`row_anchor` / `paragraph_anchor` / `weak` / `anchor_gate` / `release_state`，
再禁止出现 `data_anchor`。任一项不符，自检红、不出包。
自检项从 38 增至 39（`delivery_note.consistency`）。

## 您的第二条 P0：`anchor_gate=pass` 被读大

已在 README 与包内《交付说明.md》各加一张六级表：
坐标定位 → 行/段落指纹 → 列语义 → 条件核验 → 身份与范围 → 人工签核，
逐级写「证明了什么 / 不证明什么」。页面提示条也补了一句限定
（五语种）：锚定证明值绑定到该行，不证明列角色、测试条件、脚注已复核。

## 关于【新-1】，您的诊断和实测不一致，需要报告

您判断是「PDF 用 en-dash `–`，审计器拿 ASCII `-` 比」。**实测不成立** ——
`_page_index()` 从 V4 起就做了破折号归一，`-16.5` 在 p9/p11 都能查到。

真因是两层：
1. `_num_keys()` 把 JSON 的 `-5.0` 收成 `-5`，而 `_token_pages()` 的正则
   `(?<![\d.])-5(?![\d.])` 被原文 `–5.0` 里的 `.` 挡住 —— 两个数只命中一个。
2. `_derive()` 只认「全中」，剩下那个直接落 `not_found`，再配上
   `exclude_or_verify`。

修完两层之后，HVSS 那条不是变成 `partial`，而是**直接锚到了行**
（`p9`，bbox 覆盖名称格 + `–16.5 | –15.0 | –5.0` 三格）：因为 ABS MAX 表是
「一格一个数」，而旧 `_band_row()` 要求**单格**覆盖全部数值，整张表一条都锚不上。
改成「同一 y 带多格合起来覆盖」+ 名称分写法退让后，ADS8568 的 `row_anchor`
从 19 升到 28，`not_found` 全包 1 → 0。

顺带记一笔踩坑：第一版把三种名称写法混在一起收集候选，`Conversion Time`
因为最长实词 `conversion` 命中多行被判"歧义"，反而把**已经锚定**的两行打回同页。
所以退让必须**分写法、逐级判**。

## 【新-2】的根因也不是"漏了一组"，是少了一列

`fact_status_sync.py` 用 `(label, cond)` 对 JSON 的 `(parameter, conditions)`，
而 `facts_audit.csv` 的列清单里**根本没有 `cond`**（行字典有、写盘时被截掉）。
补列后 ADC 升级 70 行 —— 与您实测的 70/108 一致。

## 【新-3】【新-6】

- 缺列不得判 `verified_row`：`Differential Input Voltage Range` 已主动降为
  `verified_value`（`missing_cols=min,max`）。您的判断"指纹一致 ≠ 值解析正确"
  写进了代码注释与测试。
- `sha_input` 列：`sha256(sha_input)` 就是该行指纹，不必再猜行文本怎么取。

## 您要求"绝不自动升级"的部分

- ADS8568 保持 `blocked` / `PACKAGING_PASSED`，弱证据逐条留在风险队列。
- ADS1201 的 `Offset Error` / `Gain Error` 仍为空，不虚构。
- BOOST 板级与板载器件描述保持分离。
- `CONTENT_APPROVED` / `RELEASE_APPROVED` 仍未申请 —— 我们不会替人签核。

## 需要坦白的边界

您提到本轮没有独立下载 ZIP/PDF 复算、也没有本地跑自检。V8 这边能补上的是：
我们每次出包后都用「复核方视角」重新 `git clone` 发布仓库再跑一遍自检
（V7 就是这么发现三个 `.md` 的 `size` 与 `sha256` 口径分裂的：哈希按 CRLF→LF 归一、
大小却记原始字节，Windows clone 后 11653 → 11856）。这一项已在本版一并修掉。
