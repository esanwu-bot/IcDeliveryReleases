# 回复 Reviewer（delivery-20261101-V6）

> 基线：`delivery-20261101-V5`（元宝 8.6/10 复审）。
> 本版只做那份复审点名的 **P0 两件 + P1 七件**，不新增任何宏观功能。
> 每条都能在包内自证 —— 页码、`bbox`、`row_sha256`、覆盖率分子分母都在产物里，
> 且**清单里每个数都能用 `qc/bundle_selfcheck.py` 从包内文件重算**。

---

## 一、对外答复（可直接贴 GitHub）

> 感谢您用显微镜级别的审查，并亲自重算哈希抓出了我们在打包自证链上的漏洞。
> 对于 `manifest` 数值滞后和哈希未重算的问题，我们完全接受批评，
> 这是交付严谨性的底线失误。
>
> 针对 V6，我们做了如下彻底修复：
>
> 1. **自证链闭环**：重写了打包器，i18n 状态改为强依赖侧车文件；
>    所有侧车文件的 SHA-256 已重算对齐。最重要的是，我们在 `delivery_bundle.py`
>    里增加了一道**终极断言：只要清单记录的哈希与包内文件实际重算的哈希有任何一项
>    不符，打包直接失败。** 这从机制上杜绝了重出包漏更新清单的可能。
>    这道断言不复用打包器自己的哈希函数 —— 它用一份独立实现重算，
>    复核方可以跑同一条命令（`python qc/bundle_selfcheck.py --out <包根>`）复现结论。
> 2. **口径统一**：那 4 行的争议我们按「谁更严就听谁」的原则重新核了一遍 ——
>    结论是**方向与您预判的相反**：它们不是「该降级」，而是 V5 的判据过严把它们
>    误判成了「只到同页」。修好判据后事实表给的是 `verified_row`（带 `row_sha256`），
>    比 JSON 自述更强。所以最终动作是**事实表升级 + 页面完全跟事实表**，
>    而不再是两套标准。详细取证见 §三。
> 3. **归属声明补全**：ADS8568 板卡页的 Thermal / ESD / AC 三段已各补一句
>    「板载芯片参数，不代表整块评估板规格」，逐段印，不只印在页首。
> 4. **遗留清理**：ADS1201U 的 amax 已并入确定性列角色抽取（11 行里 9 行拿到
>    确定性结论、值一个字没改）；`2.0` 格式瑕疵已修；`pin_desc_exempt` 已改为布尔
>    `"true"/"false"`；README 已加 `release_state` 降级说明。
>
> V6 的数据完全由代码推导，哈希完全自洽，期待您的最终裁定。

> **⚠️ 上面第 2 条与您给的原始话术有一句不同**，原因写在 §三 ——
> 原始话术是「ENOB 等 4 行已按事实表强制降级」，实测方向相反（是升级不是降级）。
> 照原话发出去会变成一句可被包内 PDF 立刻推翻的错话，所以改成了现在的表述。

---

## 二、V5 → V6 改动一览

| # | 你提的 | 等级 | V5 | **V6** |
|---|---|---|---|---|
| 1 | `manifest` 的 i18n 与侧车矛盾 | P0 | `false / 0.9837` vs 侧车 `true / 1.0` | **强依赖侧车**，打包末尾重算比对 |
| 2 | 侧车文件 `sha256` 对不上 | P0 | 三种换行口径全不符 | **全部重算**，ZIP 内成员也重算 |
| 3 | 需要一道「对不上就中断」的断言 | P0 | 无 | **`qc/bundle_selfcheck.py`**，失败即 `RuntimeError` |
| 4 | JSON 状态与 `facts_audit` 不一致（4 行） | P1 | 两套口径 | **唯一状态推导机**，页面 `†` 跟事实表 |
| 5 | 板卡页 Thermal / ESD / AC 无归属声明 | P1 | 3 段全无 | **3 段各一句**（页面实测出现 3 次） |
| 6 | ADS1201U amax 11 行仍靠模型 | P1 | 7 unresolved + 4 model_unverified | **9 行确定性 / 1 待人工 / 1 无值** |
| 7 | `2 to 6.3` vs 原文 `2.0` | P1 | `2 to 6.3` | **`2.0 to 6.3`**（形态对齐原文，值未改） |
| 8 | `pin_desc_exempt` 是空串 | P1 | `""` | **`"true"` / `"false"`** |
| 9 | README 要说明 `release_state` 降级 | P1 | 无说明 | **已加**（见《交付说明.md》） |
| 10 | `risk_queue` 44 条 `human_review` | P2 | 61 行 / 44 人工 | **19 行 / 2 人工** |

**顺带说一句 `release_state`（你的【新-2】）**：V5 的集体降级确实是口径变严的结果，
但 V6 把锚定率补上去之后，主力件回到了 **`IDENTITY_APPROVED`**
（ADC / 两件 BOOST），`ADS8568EVM-PDK` 是 `DATA_VALIDATED`，
只有 `ADS1201U-1/1K` 停在 `PACKAGING_PASSED` —— 因为它 `46/50`，
那 4 行缺口我们**不打算靠调判据抹平**，就摆在 `data_anchor` 这一列上。
README 里已写明「降级是口径变化，不是数据退步」，并给出五件的实际卡点。

---

## 三、那 4 行到底该降级还是升级（与话术不同的那一处）

你在【新-3】里给的判断是「以更严的 `facts_audit` 为准 → 把 JSON 降级为
`value_on_label_page`」。方向我们完全接受（**唯一事实源**），但按同一原则复核后，
发现**严的那一边其实是判错了**，不是 JSON 撒谎。

### 取证

`ADC12DJ5200SE` 第 9 页 `VA19, analog 1.9-V supply(2)` 那一行，PDF 原文是：

```
VA19, analog 1.9-V supply(2)    1.8    1.9    2.0    V
```

JSON 写 `1.8 to 2.0`。V5 的事实表用**数值集合全等**比对：

```
JSON 数值集  {1.8, 2.0}
重放行数值集 {1.8, 1.9, 2.0, 19, 35}     ← 含 typ 1.9、脚注标号 (2)、行内其它数
→ 不全等 → 判「只到同页」
```

问题是：**重放行必然比 JSON 多印东西**（typ 值、脚注标号）。用全等比对，
只要原表是 MIN/TYP/MAX 三列，JSON 摘成 `min to max` 就永远不可能全等 ——
这条判据在结构上就把「三列行」全部排除了。

改成**子集判据**（JSON 的数值必须全在重放行里）并剥掉脚注标号后，同一行拿到的是
`verified_row`，且能给出该行的 `row_sha256` —— 这是**比 JSON 自述更强的证据**
（JSON 只说「我锚到了」，事实表现在能给出「锚到哪一行、重放出来是什么」）。

`ENOB`、`VA11`、`VD11` 同理，四行全部落到具体行。

### 所以最终动作

- **不是**把 JSON 降级，而是**把事实表升级**，然后**页面完全跟事实表**；
- 页面 `†` 由 `facts_verdicts.json` 统一驱动（键是 `label ␟ 条件`，
  因为 AC 表同一个 parameter 有 10 条，只按 label 打会把一条弱证据扩散成十次）；
- **不变式写进代码**：`row_sha256` 非空 ⟺ `verified_row`；`bbox` 非空 ⟺ 坐标级结论。
  `qc/fact_acceptance.py::_check_consistency()` 逐行核，违反直接让程序返回 3。

这一条对复核方的实际意义：**你现在可以用 `facts_audit.csv` 里的 `row_sha256`
独立重放那一行，而不是只看到一句「已锚定」。**

---

## 四、自证链：怎么证明「这次真的对上了」

V5 的断口不是数据错，是**人漏了一步**。所以 V6 的修法不是「下次记得」：

```
打包 → 写 manifest.json → 写 包校验报告.json
     → qc/bundle_selfcheck.py 独立重算全部成员与指标
     → 有任何一项不符 → RuntimeError，不出包
```

自检**刻意不复用** `delivery_bundle.py` 的哈希函数。理由：两边共用同一个函数，
那个函数写错了自检也会跟着一起错 —— 那不叫校验，叫复读。这里算的是
「一个不信任打包器的人会怎么算」。

| 重算项 | 依据 | 常见漏法 |
|---|---|---|
| 成员 `sha256` / `size` | 包内文件（文本 CRLF→LF，PDF/ZIP 原始字节） | 重出包忘了重算 |
| `i18n_complete` / `i18n_coverage` | 侧车 `.i18n.json`，取**所有语言最低** | 用了修订前的旧变量（V5 就是） |
| `data_anchor` | 随包 `facts_audit.csv` 逐行数 | 手写字符串 |
| `pdf_sha256_packaged` / `pdf_hash_match` | 包内 PDF 原始字节 | 复制的和被解析的不是同一份 |
| `artifacts` | 记录里 `present` 计数 | 加了一个物料没更新分母 |
| ZIP 成员哈希 / 非法路径 | 分卷 ZIP 本身 | 清单对、ZIP 里是旧的 |
| `zip_sha256` / `verified_members` | ZIP 实算 | 改了 ZIP 没重写报告 |

复核方复现：

```bash
python qc/bundle_selfcheck.py --out <解压后的包根目录>
# 通过 → 退出码 0；不一致 → 逐项打印差异，退出码 1
```

`包校验报告.json` 里 `self_check: "pass"` 即这一层已通过。

**这道断言在 V5 上跑会红** —— 我们拿 V5 包试过，它抓到的正是
`i18n_validation 仍是 not_checked，但清单已有实测覆盖率（口径自相矛盾）`。
一条能抓到旧版本真实缺陷的断言，才算真的在工作。

---

## 五、口径拆分：覆盖率 ≠ 内容审校

V5 把两件事塞进同一个 `i18n_validation` 字段，于是「覆盖率 1.0」被读成「多语已验收」。
V6 拆开：

| 字段 | 含义 | 本包取值 |
|---|---|---|
| `i18n_coverage` | **机器实测**：多少 key 有译文、多少回退英文 | 三件 `1.0000`；两件 BOOST 板卡 `0.9661` / `0.9623` |
| `i18n_content_review` | **人工审校**：译文读起来对不对、术语是否统一 | 全部 `not_reviewed` |

**覆盖率 1.0 只证明「没有回退到英文」，不证明译文质量。** 这个区别必须写在清单里，
否则下一位复核方还会把它当验收结论。

---

## 六、板卡归属声明（新-4）

`ADS8568EVM-PDK` 挂的 PDF 是 **ADS8568 的器件手册（SBAS543C）**，整板的电源/连接器
规格根本不在那份文件里。V5 只在 Electrical 段印了声明，Thermal / ESD / AC 三段
直接渲染了板载芯片参数（`RθJA 22 °C/W`、`HBM ±2500 V`、`SNR 73/73.9 dB`）。

V6 起三段**各自**在表头印一次：

> These values are specified for the on-board ADS8568 device; they are not limits
> for the assembled board.

页面实测出现 **3 次**（热阻 / ESD / AC 各一）。**必须逐段印** —— 读者是跳着看的，
看到 RθJA 那一行时未必刚读过页首。

---

## 七、ADS1201U 的 amax（新-5）

V5 里 11 行是 `7 unresolved + 4 model_unverified`。根因不是「忘了推广」，
而是**推广了也没用**：

```
find_tables() 在这一页只识别出一个 2 行小表
```

因为该表是**点线排版**（`名称…………值`），PyMuPDF 的表格探测器看不见它。
所以 V6 做了两件事：

1. 同页**多表全试**，按匹配条数选表（不再取面积最大的那张）；
2. 无表时退回**点线行抽取**（`名称……值` 正则 + 二轮逐字核对）。

结果：**4 `audited_deterministic` + 5 `audited_paragraph` + 1 `model_unverified`
+ 1 `unresolved`，`replaced = 0`**（值一个字没改，只是把证据补上了）。

点线行抽取踩过两个真坑，都写进注释了：

- `REFIN Voltage to AGND` 只撞上一个 `AGND` 就 0.5 分命中 `AVDD to AGND`，
  会把 `-0.3 to 6` 写进去（**伪造**）→ 点线行要求撞上 **≥2 个编号词**；
- 未解析出值的点线行仍保留（供二轮逐字核对），但**一轮不许用它覆盖** ——
  否则 `Digital Input Voltage to DGND` 会认到 `DVDD to DGND`。

---

## 八、没做的（明确列出，不假装做了）

| 项 | 状态 | 为什么 |
|---|---|---|
| `risk_queue` 剩余 19 行 | 未清零 | 2 行需人工看图（`human_review`），17 行是可转确定性抽取的候选 |
| SINAD / ENOB / NF 进 AC 表 | 未做 | 需要扩 AC 表 schema，属内容口径变更，不在封板范围 |
| 生命周期 / RoHS / REACH / MSL | 未做 | 源 PDF 里没有，凭空写就是编造 |
| `CONTENT_APPROVED` / `RELEASE_APPROVED` | 不申请 | **只认 `signoff.json`，代码不代签** |
| 板卡整板规格 | 没有 | 源文档里没有，不假装有 |

---

## 九、复现命令

```bash
# ① 自证链：清单里每个数都能从包内文件重算
python qc/bundle_selfcheck.py --out <包根目录>
# → 自证链自检通过

# ② i18n 与侧车是否一致（V5 的断口）
python -c "
import json,hashlib
d=json.load(open('manifest.json'))
r=[x for x in d['records'] if x['safe_name']=='ADC12DJ5200SE'][0]
print('manifest:', r['i18n_complete'], r['i18n_coverage'])
j=json.load(open('ADC12DJ5200SE/ADC12DJ5200SE.i18n.json'))
print('侧车 ja :', j['languages']['ja']['i18n_complete'], j['languages']['ja']['i18n_coverage']['ratio'])
ms={m['member']:m['sha256'] for m in d['members']}
raw=open('ADC12DJ5200SE/ADC12DJ5200SE.i18n.json','rb').read()
print('哈希一致:', hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()
      == ms['ADC12DJ5200SE/ADC12DJ5200SE.i18n.json'])"
# → true 1.0000 / true 1.0 / 哈希一致: True

# ③ 不变式：有 row_sha256 就必须是 verified_row
python -c "
import csv
rows=list(csv.DictReader(open('facts_audit.csv',encoding='utf-8-sig')))
print('坏行:', sum(1 for r in rows if r['row_sha256'] and r['verdict']!='verified_row'))"
# → 坏行: 0

# ④ 板卡归属声明（三段各一次）
grep -c "not limits for the assembled board" ADS8568EVM-PDK/ADS8568EVM-PDK.html
# → 3

# ⑤ amax 格式对齐
python -c "
import json;d=json.load(open('ADC12DJ5200SE/ADC12DJ5200SE.json'))
for x in d['specs']['electrical']:
    if 'Frequency Range' in str(x.get('name','')): print(x['value'])"
# → 2.0 to 6.3
```
