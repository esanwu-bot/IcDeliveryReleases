# D4 · `PIN|FUNCTION` 布局独立验收（2026-11-03，本地 HEAD `948c2c2`）

**结论：不通过竣工验收，D4 维持 PENDING。** 本地复跑 LM317 得到 3 脚（与 PDF 一致 ✓），
但在**同一份代码**的服务器同构复跑里得到 4 脚（多出一条重复的 `OUTPUT 4`），
且确定性侧抽到的 3 条**没有纠正**它。这说明引脚数仍受模型稿影响，
不能把「某一次跑出 3 脚」当成 D4 已验收。

## 1. 本地独立复跑（HEAD `948c2c2`，真实模型）

```text
mpn=LM317  pdf_sha256=1646fb2e4f8cf8c2cbd93aaf22edad368571619ad062476deca8ee29f95c65d3
status=ok  llm_calls=1  elapsed=51.5s  thermal_rows=34
deterministic_extract.pins = {"skipped": "model_pins_complete", "kept": 3, "det_pins": 3, "ordered": "numeric_asc"}
pin_configuration:
  {"pin": 1, "name": "ADJUST"}
  {"pin": 2, "name": "OUTPUT"}
  {"pin": 3, "name": "INPUT"}
```

LM317（TO-220）的真实脚表就是 3 脚，与 PDF 一致。**这一次是对的。**

## 2. 服务器同构复跑（同一 commit，同一镜像依赖，Redis DB8 隔离）

```text
pins_count = 4
  {"pin": "1", "name": "ADJUST", "description": "Output voltage adjustment pin. …"}
  {"pin": "2", "name": "OUTPUT", "description": "Output voltage pin for the regulator."}
  {"pin": "3", "name": "INPUT",  "description": "Input voltage pin for the regulator."}
  {"pin": "4", "name": "OUTPUT", "description": "Output voltage pin for the regulator."}   ← 多出来的重复行
deterministic_extract.pins = {"skipped": "model_pins_complete", "kept": 4, "det_pins": 3, "ordered": "numeric_asc"}
```

证据文件：`docs/qc/phase171/g1_server/s1.json`（`report.doc.deterministic_extract.pins`）。

## 3. 根因（不是环境问题）

`apply_deterministic()` 的引脚闸门是**单向**的：

- G2（`948c2c2`）加的补脚条件是 `len(det_pins) > len(existing)` —— 只覆盖
  「模型少脚」的方向（ADS42 33→64、LM358 2→8 就是靠它）；
- 「模型**多**脚」的方向没有任何判据：只要模型的脚号是 `1..N` 连续递增，
  就被判 `model_pins_complete` 而**整份保留**。LM317 这次模型给了 1..4，
  于是 `kept=4`，确定性侧的 3 条（`det_pins=3`）反而被当作「更少的那一份」丢弃。

也就是说：`model_pins_complete` 只验证了「编号连续」，**没有验证「脚数正确」**，
更没有检查重复脚名。LM317 的 4 脚里 `OUTPUT` 出现两次，肉眼可见是错的，
但当前没有任何一条规则会拦它。

## 4. 因此

- D4 维持 **PENDING**；本包（V3-CANDIDATE）里所有**来自模型稿的引脚行**
  都应视为**未验证字段**，`pins` 计数不得作为验收通过的证据。
- 建议的最小修法（本轮不做，避免与 G2 混在一起改）：
  在 `model_pins_complete` 分支里补一条 `det_pins` 数量的**一致性校验** ——
  `det_pins` 非空且 `len(existing) != len(det_pins)` 时不走 `skipped`，
  改走逐条比对（并显式记录冲突），而不是无条件保留模型稿。
- 已验证的部分只有：LM317 在**本地**这一轮跑出 3 脚，
  以及 ADS42 64 / LM358 8 / NE555 8 在本包物料里已生效（见 `G2_PIN_FIX.md`）。
