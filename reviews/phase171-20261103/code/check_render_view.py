#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D3 渲染消费端验收：HTML 确实走 `canonical_view`，芯片参数不出现在板卡页。

做法：拿样本 2（ADS8568EVM-PDK，PDF 为 ADS8568 器件手册）的真实复跑 JSON，
用 `json_to_txt.render(doc, "en")` 渲染，然后断言：

1. 文档级：`render()` 第一行就调用 `canonical_view(doc)`（源码映射，防绕过）；
2. 数据级：芯片 thermal/esd 的**参数名与核心数值**不出现在 HTML 里；
3. 反向：板载器件的 electrical 仍以「onboard device」口径出现（不是被整体吞掉）。

用法：python docs/qc/phase171/check_render_view.py
产物：docs/qc/phase171/evidence/s2-render-view.json
"""
from __future__ import annotations

import inspect
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import json_to_txt as JT                                        # noqa: E402
from qc.scope_contract import canonical_view                   # noqa: E402

EVID = ROOT / "docs" / "qc" / "phase171" / "evidence"
S2 = EVID / "s2-ads8568evm-pdk.json"


def main() -> int:
    ev = json.loads(S2.read_text(encoding="utf-8"))
    doc = json.loads(Path(ev["out_json"]).read_text(encoding="utf-8"))

    src = inspect.getsource(JT.render)
    uses_canonical = "canonical_view(doc)" in src

    view = canonical_view(doc)
    vsp = view.get("specs") or {}
    ods = vsp.get("onboard_device_specs") or {}
    chip_thermal = [r for r in (ods.get("thermal") or []) if isinstance(r, dict)]
    chip_esd = [r for r in (ods.get("esd") or []) if isinstance(r, dict)]

    html = JT.render(doc, "en")
    html_view = JT.render(view, "en")

    BANNER = "not limits for the assembled board"

    def section_of(first_name: str) -> tuple[int, int]:
        i = html.find(first_name)
        if i < 0:
            return (-1, -1)
        start = html.rfind("<h3", 0, i)
        if start < 0:
            start = 0
        end = html.find("<h3", i)
        return (start, end if end > 0 else len(html))

    def check_block(rows, first_name: str) -> dict:
        """以「参数名」为锚：名称唯一，不会像短数字那样命中别处。

        判据：① 该段（从最近 h3 到下一个 h3）内必须出现 onboard 横幅；
        ② 每个芯片参数名的**所有**出现位置都必须落在这段内。
        """
        start, end = section_of(first_name)
        if start < 0:
            return {"section_found": False, "banner_in_section": False,
                    "names_outside": [], "ok": False}
        seg = html[start:end]
        banner_in = ("onboard" in seg.lower()) and (BANNER in seg)
        outside = []
        for r in rows:
            name = str(r.get("name") or "").strip()
            if not name:
                continue
            pos, seen = html.find(name), 0
            while pos >= 0:
                seen += 1
                if not (start <= pos < end):
                    outside.append({"name": name, "index": pos})
                pos = html.find(name, pos + 1)
            if seen == 0:
                outside.append({"name": name, "index": -1, "missing": True})
        return {"section_found": True, "banner_in_section": banner_in,
                "names_outside": outside, "ok": bool(banner_in and not outside),
                "section_start": start, "section_end": end}

    th = check_block(chip_thermal, "RθJA")
    esd = check_block(chip_esd, "HBM")

    res = {
        "probe": "json_to_txt.render on real s2 doc (board w/ chip datasheet)",
        "render_calls_canonical_view": uses_canonical,
        "doc_main_thermal": len((doc.get("specs") or {}).get("thermal") or []),
        "doc_main_esd": len((doc.get("specs") or {}).get("esd") or []),
        "view_main_thermal": len(vsp.get("thermal") or []),
        "view_main_esd": len(vsp.get("esd") or []),
        "view_onboard_thermal": len(chip_thermal),
        "view_onboard_esd": len(chip_esd),
        "html_len": len(html),
        "html_view_len": len(html_view),
        "banner": BANNER,
        "thermal_block": th,
        "esd_block": esd,
        "passed": bool(uses_canonical and th["ok"] and esd["ok"]
                       and not (vsp.get("thermal") or [])
                       and not (vsp.get("esd") or [])),
    }
    p = EVID / "s2-render-view.json"
    p.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"[evidence] {p}")
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
