# 回复 Reviewer（V10）

致复核方：V9 终审的四项，逐条回。**两项 P0 是我方防线失效，不是口径分歧**，
这一版先承认、再给证据。

---

## 1. 【P0-1】ADS8568EVM 身份与「篡改疑云」

> 你的指控：这块板在页面上既不说自己是谁家的，也不给手册出处，只留一句
> 「The source document … is the datasheet of the onboard ADS8568」——
> 读者无从核对，等于要求复核方**相信**。

**你说得对，而且比「渲染缺失」更严重：数据本来是全的，是我们没印出来。**

链条是这样断的：

1. `qc/identity_scope.py` 把 `basic_info.datasheet_url` 搬进
   `device_datasheet_url` 并清空原字段 —— 板卡的主文档是 User Guide，
   芯片手册本就该降级，这步没错。
2. 但 `json_to_txt.py` 板卡分支渲染时，把 `values_source` 当**纯文本**印，
   不跟随链接 —— 于是那个被降级的地址**整句被吞掉**。
3. `data_subject` / `subject_match` 只写进 manifest 做核验元数据，
   **不参与渲染**。所以不存在「判定身份不符→过滤整块」这种事，
   是**从头到尾没写过这句话**。

**V10 修法**（只加渲染，不改数据）：板卡首屏补两段 —— 身份句 + 溯源句，
后者带原厂手册直链（`rel="nofollow"`）。

实测 `ADS8568EVM-PDK` 页面：

| 指标 | V9 | V10 |
|---|---|---|
| 身份句首次出现位置 | HTML 21397（页脚 Manufacturer） | **1247（首屏）** |
| 全页 `ti.com` 链接 | 1 | **2** |
| `<a href>` 总数 | 1 | **2** |

> 关于「篡改」：`pdf_sha256_recorded == pdf_sha256_packaged`，五件全 `True`；
> `pdf_hash_match=false` 会直接 `gate=BLOCKED`（§16.8 口径 1）。
> 随包 PDF 就是被解析的那一份，你可以自己 `sha256sum` 重算。

---

## 2. 【P0-2】AC 表列语义：闸门写好了，但**从来没执行过**

> 你的指控：`SNR` 行 `min="73.9" / max="dB"` —— 单位占了 MAX 格、数值塞进 MIN 格，
> 却拿到 `verified_row` 绿灯。

**这是本次最难看的一处：闸门早就有，测试还是绿的。**

三段链路，每段都足以单独否决，实际三段同时失守：

1. **闸门没跑**：`deterministic_extract.check_core()` 的板卡分支在
   `check_ac_integrity()` **之前**就 `return errs`。豁免板卡的引脚/thermal/ESD 是对的，
   但顺手把 AC 列角色闸门一起豁免了。
2. **判据太宽**：`check_ac_integrity()` 只比对 `value_shape`（原表填了哪几格）
   与实际填充是否自洽。填了两格 → `filled="LH"` 与 `shape="LH"` 一致 → 放行。
   **它从没问过「这两格里填的是不是数」。**
3. **下游兜不住**：`fact_acceptance._derive()` 只看指纹 + 坐标；
   `_downgrade_for_missing_cols()` 只认 `missing_cols`（本例为空 —— 列都在，
   只是内容错位），于是给了干净绿灯。

**更难看的是测试**：`test_check_core_skips_board_pages` 只断言
`check_core(d) == []`，夹具里**根本没有 `ac_performance`**。
闸门失效那段时间，这条用例一直是绿的 —— 它测的是「没输入时不报错」。

**V10 修法**：闸门提前执行 + 给 MIN/TYP/MAX 加**数值格判据**（`±`/`+`/`−`/科学计数法
合法，单位与脚注非法）。用例改成喂脏 AC + 双断言（既不能冤枉板卡该豁免的项，
又必须抓到 `MAX='dB'`）。

实测 `ADS8568EVM-PDK` 的 `metadata.core_validation`：V9 = `"pass"`（字符串）
→ V10 = **6 条显式报错**，覆盖 SNR/SFDR 三组条件。

**但要把边界说清楚**：V10 **只让闸门亮灯，没有修数据**。
数据要修必须重解该页 PDF，那越过「V10 不重解」的红线，也拿不到原厂列语义确认。
所以现在交付的是「**有据可查的错**」——这 6 行仍渲染，但 `core_validation` 明写错在哪。

---

## 3. 【P1-3】ESD `±` 丢失：全库复扫，未复现

对全交付包逐条扫 `specs.esd[].value`：**40/40 全部带 `±`**。

`ADS1201U-1/1K` 单独说明：该型号 `specs.esd` 为空 —— **不是符号被吃**，
是源文档只有 ESD 免责声明、没有额定值表；全库 44 份 `ADS1201U` 产物一致为空。
如实留空，不编造。若你要一个「必须显示 ESD」的判据，那是**源文档缺项**，
请按 §16.9 记 `unchecked`，不要当成符号丢失。

---

## 4. 灰度压测（1000 件，seed 20261101，40 片全 rc=0）

| verdict | 行数 | 占比 |
|---|---|---|
| `verified_row` | 25647 | 51.21% |
| `value_on_label_page` | 13772 | 27.50% |
| `verified_paragraph` | 5025 | 10.03% |
| `value_in_pdf` | 4842 | 9.67% |
| `unchecked` | 639 | 1.28% |
| `not_found` | 97 | 0.19% |
| `partial` | 59 | 0.12% |

逐件 `anchor_gate`：**pass 7（0.7%）/ blocked 993（99.30%）**。
逐件锚点组合：行级+段级 81.30% / 仅行级 16.20% / 仅段级 2.30% / 无锚点 0.20%；
**全行都是行级锚点的仅 1 件（0.10%）**。

结论我们认：**瓶颈是证据载体，不是闸门松紧**。
按这个分布推 10 万件，真正要人工的硬骨头约 9.9%（`not_found` + `value_in_pdf`）；
`value_on_label_page` 那 27.5% 是「同页命中」的弱证据，要靠
`promote_to_deterministic` 转强，而不是放宽判据。

---

## 5. 自证链

`qc/bundle_selfcheck.py` 从包内文件**独立重算**：**41/41 全绿，`self_check=pass`**。
物料口径 `7/8 ×4 + 8/8 ×1`（缺 `alt_html`，V9 同样缺；`ADS1201U` 的替代料页面
从 V9 包原样沿用，未重新生成 —— 不做「为了凑齐而生成」）。

测试：容器内挂真实数据全量 **1387 passed / 21 skipped / 0 failed**。
