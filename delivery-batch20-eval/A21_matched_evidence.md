# A21 · 改表 / 新增 matched 逐条证据（只读核对表）

> 用途：人工核对 `Table Match Precision`。**本表不参与任何闸门判定，不阻断打包。**
> 生成源：`data/_tmp_ab_a21_final.json`（A/B 同 cohort，19 件可评 / 770 条）。
> 生成脚本：`data/_gen_a21_evidence_md.py`（一次性工具，不入库）。

## 口径

收录条件 = **v4 判 `matched`，且「v3 不是同表 matched」**。
即：A21 把这条参数**换了表**，或者 v3 当时根本是 `ambiguous_tie` / 无表。
v3 与 v4 落在同一张表的条目**不计入**（那不是 A21 的收益）。

| 项 | 值 |
|---|---|
| 条目总数 | **112** |
| 涉及型号 | **16** |
| cohort | 23 件（含缺件），可评 770 条 |
| v3 基线 | matched 601 / ambiguous 110 / unmatched 59 |
| v4 (A21) | matched 616 / ambiguous 95 / unmatched 59 |

**列说明**

- `v3 指向页`：v3 臂把该条参数落到的 PDF 页码；`ambiguous_tie` 表示 v3 当时也没定下来。
- `v4 指向页` / `行号`：v4 臂落到的页码与该页表内的行下标 `ri`（0 基）。
- `表号`：**当前 A/B 工具未记录**（原始 txt 里显示为 `t?`），因此本表留空 `—`；
  核对时以「页 + 行号」定位即可，同页多表的情况需人工看原表标题。

## 分型号计数

| MPN | 条数 |
|---|---:|
| `74LVC1G132DCKTG4` | 28 |
| `AM26C32IDG4` | 10 |
| `BUF634PG4` | 5 |
| `CD74FCT244SM96` | 5 |
| `CY74FCT245ATSOCT` | 5 |
| `DAC8555IPWG4` | 2 |
| `2MTR-DYNO` | 11 |
| `ADC08B200EB` | 5 |
| `ADC128D818EB_NOPB` | 1 |
| `ADS1675REF` | 4 |
| `ADS42JB49SEK` | 10 |
| `CDC6CE025000ADLER` | 6 |
| `CDC6CE025000ADLET` | 6 |
| `CDC6CE025000ADLFR` | 6 |
| `CDC6CE025000ADLYR` | 6 |
| `CDC6CE040000ADLFR` | 2 |
| **合计** | **112** |

## 逐条明细

| # | MPN | 参数名 | v3 指向页 | v4 指向页 | 行号 | 表号 | 备注 |
|---:|---|---|---:|---:|---:|---|---|
| 1 | `74LVC1G132DCKTG4` | VOH High-level output voltage | p4 | p5 | 5 | — | A21 换表 |
| 2 | `74LVC1G132DCKTG4` | VOH High-level output voltage | p4 | p5 | 6 | — | A21 换表 |
| 3 | `74LVC1G132DCKTG4` | VOH High-level output voltage | p4 | p5 | 8 | — | A21 换表 |
| 4 | `74LVC1G132DCKTG4` | VOH High-level output voltage | p4 | p5 | 9 | — | A21 换表 |
| 5 | `74LVC1G132DCKTG4` | VOL Low-level output voltage | p4 | p5 | 10 | — | A21 换表 |
| 6 | `74LVC1G132DCKTG4` | VOL Low-level output voltage | p4 | p5 | 11 | — | A21 换表 |
| 7 | `74LVC1G132DCKTG4` | VOL Low-level output voltage | p4 | p5 | 13 | — | A21 换表 |
| 8 | `74LVC1G132DCKTG4` | VOL Low-level output voltage | p4 | p5 | 14 | — | A21 换表 |
| 9 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 0 | — | A21 换表 |
| 10 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 0 | — | A21 换表 |
| 11 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 1 | — | A21 换表 |
| 12 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 1 | — | A21 换表 |
| 13 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 2 | — | A21 换表 |
| 14 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 2 | — | A21 换表 |
| 15 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 3 | — | A21 换表 |
| 16 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 3 | — | A21 换表 |
| 17 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 4 | — | A21 换表 |
| 18 | `74LVC1G132DCKTG4` | VT+ Positive-going input threshold voltage | p4 | p6 | 4 | — | A21 换表 |
| 19 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 5 | — | A21 换表 |
| 20 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 5 | — | A21 换表 |
| 21 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 6 | — | A21 换表 |
| 22 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 6 | — | A21 换表 |
| 23 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 7 | — | A21 换表 |
| 24 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 7 | — | A21 换表 |
| 25 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 8 | — | A21 换表 |
| 26 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 8 | — | A21 换表 |
| 27 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 9 | — | A21 换表 |
| 28 | `74LVC1G132DCKTG4` | VT– Negative-going input threshold voltage | p4 | p6 | 9 | — | A21 换表 |
| 29 | `AM26C32IDG4` | Differential input high-threshold voltage (VIT+) | p3 | p4 | 4 | — | A21 换表 |
| 30 | `AM26C32IDG4` | Differential input high-threshold voltage (VIT+) | ambiguous_tie(p3) | p4 | 4 | — | A21 新增命中（v3 当时未定表） |
| 31 | `AM26C32IDG4` | Differential input low-threshold voltage (VIT–) | ambiguous_tie(p3) | p4 | 4 | — | A21 新增命中（v3 当时未定表） |
| 32 | `AM26C32IDG4` | Differential input low-threshold voltage (VIT–) | p3 | p4 | 4 | — | A21 换表 |
| 33 | `AM26C32IDG4` | Enable input clamp voltage (VIK) | p4 | p5 | 6 | — | A21 换表 |
| 34 | `AM26C32IDG4` | High-level output voltage (VOH) | p4 | p5 | 7 | — | A21 换表 |
| 35 | `AM26C32IDG4` | Low-level output voltage (VOL) | p4 | p5 | 8 | — | A21 换表 |
| 36 | `AM26C32IDG4` | OFF-state output current (IOZ) | p4 | p5 | 9 | — | A21 换表 |
| 37 | `AM26C32IDG4` | High-level enable current (IIH) | p4 | p5 | 12 | — | A21 换表 |
| 38 | `AM26C32IDG4` | Low-level enable current (IIL) | p4 | p5 | 13 | — | A21 换表 |
| 39 | `BUF634PG4` | Short-Circuit Current (Wide BW Mode) | p4 | p5 | 23 | — | A21 换表 |
| 40 | `BUF634PG4` | Slew Rate | p2 | p5 | 29 | — | A21 换表 |
| 41 | `BUF634PG4` | Voltage Noise | p2 | p7 | 9 | — | A21 换表 |
| 42 | `BUF634PG4` | Gain | ambiguous_tie(p2) | p7 | 19 | — | A21 新增命中（v3 当时未定表） |
| 43 | `BUF634PG4` | Thermal Shutdown Temperature | p6 | p7 | 37 | — | A21 换表 |
| 44 | `CD74FCT244SM96` | Cpd | ambiguous_tie(p1) | p3 | 1 | — | A21 新增命中（v3 当时未定表） |
| 45 | `CD74FCT244SM96` | VOL | p2 | p3 | 3 | — | A21 换表 |
| 46 | `CD74FCT244SM96` | II | p2 | p3 | 4 | — | A21 换表 |
| 47 | `CD74FCT244SM96` | Ci | p2 | p3 | 9 | — | A21 换表 |
| 48 | `CD74FCT244SM96` | Co | p2 | p3 | 10 | — | A21 换表 |
| 49 | `CY74FCT245ATSOCT` | VOL | p3 | p4 | 6 | — | A21 换表 |
| 50 | `CY74FCT245ATSOCT` | VOL | p3 | p4 | 6 | — | A21 换表 |
| 51 | `CY74FCT245ATSOCT` | IC# | ambiguous_tie(p2) | p4 | 24 | — | A21 新增命中（v3 当时未定表） |
| 52 | `CY74FCT245ATSOCT` | IC# | ambiguous_tie(p2) | p5 | 4 | — | A21 新增命中（v3 当时未定表） |
| 53 | `CY74FCT245ATSOCT` | Co | ambiguous_tie(p3) | p5 | 9 | — | A21 新增命中（v3 当时未定表） |
| 54 | `DAC8555IPWG4` | AVDD | ambiguous_tie(p2) | p3 | 28 | — | A21 新增命中（v3 当时未定表） |
| 55 | `DAC8555IPWG4` | AVDD | ambiguous_tie(p2) | p3 | 28 | — | A21 新增命中（v3 当时未定表） |
| 56 | `2MTR-DYNO` | Device supply voltage, I/O, VDDIO | ambiguous_tie(p15) | p23 | 1 | — | A21 新增命中（v3 当时未定表） |
| 57 | `2MTR-DYNO` | Device clock frequency (system clock) | p16 | p23 | 6 | — | A21 换表 |
| 58 | `2MTR-DYNO` | High-level input voltage, VIH (3.3 V) | p17 | p23 | 7 | — | A21 换表 |
| 59 | `2MTR-DYNO` | High-level output source current, VOH = VOH(MIN) | p17 | p23 | 9 | — | A21 换表 |
| 60 | `2MTR-DYNO` | IIH (Input Current High) | p17 | p23 | 9 | — | A21 换表 |
| 61 | `2MTR-DYNO` | High-level output source current, VOH = VOH(MIN) | p17 | p23 | 10 | — | A21 换表 |
| 62 | `2MTR-DYNO` | Low-level output sink current, VOL = VOL(MAX) | p13 | p23 | 11 | — | A21 换表 |
| 63 | `2MTR-DYNO` | Low-level output sink current, VOL = VOL(MAX) | ambiguous_tie(p13) | p23 | 12 | — | A21 新增命中（v3 当时未定表） |
| 64 | `2MTR-DYNO` | VOH | p23 | p28 | 1 | — | A21 换表 |
| 65 | `2MTR-DYNO` | VOH | p23 | p28 | 2 | — | A21 换表 |
| 66 | `2MTR-DYNO` | VOL | p7 | p28 | 3 | — | A21 换表 |
| 67 | `ADC08B200EB` | RIN | p4 | p6 | 11 | — | A21 换表 |
| 68 | `ADC08B200EB` | RREF | ambiguous_tie(p5) | p6 | 19 | — | A21 新增命中（v3 当时未定表） |
| 69 | `ADC08B200EB` | RREF | ambiguous_tie(p5) | p6 | 19 | — | A21 新增命中（v3 当时未定表） |
| 70 | `ADC08B200EB` | RREF | ambiguous_tie(p5) | p6 | 20 | — | A21 新增命中（v3 当时未定表） |
| 71 | `ADC08B200EB` | VOL | ambiguous_tie(p3) | p7 | 9 | — | A21 新增命中（v3 当时未定表） |
| 72 | `ADC128D818EB_NOPB` | IOH High Level Output Current (SDA) | p4 | p8 | 13 | — | A21 换表 |
| 73 | `ADS1675REF` | Reference input voltage (VREF) | p3 | p4 | 4 | — | A21 换表 |
| 74 | `ADS1675REF` | VOL | p3 | p4 | 16 | — | A21 换表 |
| 75 | `ADS1675REF` | AVDD | p2 | p4 | 28 | — | A21 换表 |
| 76 | `ADS1675REF` | DVDD | p2 | p4 | 29 | — | A21 换表 |
| 77 | `ADS42JB49SEK` | VID | p3 | p11 | 2 | — | A21 换表 |
| 78 | `ADS42JB49SEK` | VID | p3 | p11 | 3 | — | A21 换表 |
| 79 | `ADS42JB49SEK` | Analog input bandwidth | ambiguous_tie(p8) | p11 | 6 | — | A21 新增命中（v3 当时未定表） |
| 80 | `ADS42JB49SEK` | VCM | p6 | p11 | 7 | — | A21 换表 |
| 81 | `ADS42JB49SEK` | VCM output current capability | p6 | p11 | 8 | — | A21 换表 |
| 82 | `ADS42JB49SEK` | IOVDD | p6 | p11 | 18 | — | A21 换表 |
| 83 | `ADS42JB49SEK` | Analog power | p6 | p11 | 19 | — | A21 换表 |
| 84 | `ADS42JB49SEK` | Analog buffer power | p6 | p11 | 20 | — | A21 换表 |
| 85 | `ADS42JB49SEK` | Digital power | ambiguous_tie(p6) | p11 | 21 | — | A21 新增命中（v3 当时未定表） |
| 86 | `ADS42JB49SEK` | Global power-down | p6 | p11 | 24 | — | A21 换表 |
| 87 | `CDC6CE025000ADLER` | VOL | ambiguous_tie(p5) | p5 | 1 | — | A21 新增命中（v3 当时未定表） |
| 88 | `CDC6CE025000ADLER` | CL | p4 | p7 | 22 | — | A21 换表 |
| 89 | `CDC6CE025000ADLER` | CL | p4 | p7 | 23 | — | A21 换表 |
| 90 | `CDC6CE025000ADLER` | CIN | p5 | p7 | 32 | — | A21 换表 |
| 91 | `CDC6CE025000ADLER` | RJ | ambiguous_tie(p6) | p8 | 17 | — | A21 新增命中（v3 当时未定表） |
| 92 | `CDC6CE025000ADLER` | RJ | ambiguous_tie(p6) | p8 | 19 | — | A21 新增命中（v3 当时未定表） |
| 93 | `CDC6CE025000ADLET` | VOL | ambiguous_tie(p5) | p5 | 1 | — | A21 新增命中（v3 当时未定表） |
| 94 | `CDC6CE025000ADLET` | CL | p4 | p7 | 22 | — | A21 换表 |
| 95 | `CDC6CE025000ADLET` | CL | p4 | p7 | 23 | — | A21 换表 |
| 96 | `CDC6CE025000ADLET` | CIN | p5 | p7 | 32 | — | A21 换表 |
| 97 | `CDC6CE025000ADLET` | RJ | ambiguous_tie(p6) | p8 | 17 | — | A21 新增命中（v3 当时未定表） |
| 98 | `CDC6CE025000ADLET` | RJ | ambiguous_tie(p6) | p8 | 19 | — | A21 新增命中（v3 当时未定表） |
| 99 | `CDC6CE025000ADLFR` | VOL | ambiguous_tie(p5) | p5 | 1 | — | A21 新增命中（v3 当时未定表） |
| 100 | `CDC6CE025000ADLFR` | CL | p4 | p7 | 22 | — | A21 换表 |
| 101 | `CDC6CE025000ADLFR` | CL | p4 | p7 | 23 | — | A21 换表 |
| 102 | `CDC6CE025000ADLFR` | CIN | p5 | p7 | 32 | — | A21 换表 |
| 103 | `CDC6CE025000ADLFR` | RJ | ambiguous_tie(p6) | p8 | 17 | — | A21 新增命中（v3 当时未定表） |
| 104 | `CDC6CE025000ADLFR` | RJ | ambiguous_tie(p6) | p8 | 19 | — | A21 新增命中（v3 当时未定表） |
| 105 | `CDC6CE025000ADLYR` | VOL | ambiguous_tie(p5) | p5 | 1 | — | A21 新增命中（v3 当时未定表） |
| 106 | `CDC6CE025000ADLYR` | CL | p4 | p7 | 22 | — | A21 换表 |
| 107 | `CDC6CE025000ADLYR` | CL | p4 | p7 | 23 | — | A21 换表 |
| 108 | `CDC6CE025000ADLYR` | CIN | p5 | p7 | 32 | — | A21 换表 |
| 109 | `CDC6CE025000ADLYR` | RJ | ambiguous_tie(p6) | p8 | 17 | — | A21 新增命中（v3 当时未定表） |
| 110 | `CDC6CE025000ADLYR` | RJ | ambiguous_tie(p6) | p8 | 19 | — | A21 新增命中（v3 当时未定表） |
| 111 | `CDC6CE040000ADLFR` | VOL | ambiguous_tie(p5) | p5 | 1 | — | A21 新增命中（v3 当时未定表） |
| 112 | `CDC6CE040000ADLFR` | CL | p4 | p7 | 22 | — | A21 换表 |

## 怎么用

1. 抽任意一行，打开 `data/pdfs/<MPN>__*.pdf` 的第 `v4 指向页`。
2. 数到第 `行号` 条数据行（`ri` 是该页解析出的表内行下标，0 基，含表头偏移）。
3. 确认该行的参数名与数值确实对得上 —— 对得上记 ✓，对不上记 ✗ 并写下实际内容。
4. 全部核完再谈 `Table Match Precision`；**不要**拿本表当「已核对」的结论。

> ⚠️ 已知局限：`ri` 是**解析器视角**的行号，不是 PDF 印刷行号。
> 若解析器把多行并成一行（两级表头、跨页续表），`ri` 会与肉眼行数有偏移。
