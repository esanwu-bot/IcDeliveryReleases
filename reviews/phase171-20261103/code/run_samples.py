#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 1.7.1 三件冻结样本复跑器（本地、隔离写入、生产零污染）。

样本（与原冻结单一致，不改 MPN / 来源 / PDF）：
  s1 LM317            → V2 parse_pdf 真实模型；验收 thermal=34、占位符不落行
  s2 ADS8568EVM-PDK   → V2 parse_pdf 真实模型；验收 identity/主体归属字段级
  s3 DAC8568EVM       → 非 Datasheet（User's Guide）；验收异常短路、零模型调用

用法：
  python docs/qc/phase171/run_samples.py --sample 1
  python docs/qc/phase171/run_samples.py --sample 3
  python docs/qc/phase171/run_samples.py --sample 2

产物：docs/qc/phase171/evidence/s{N}-*.json（只写证据目录与系统临时目录）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import pymupdf                                                    # noqa: E402
import parse_datasheets as pd                                     # noqa: E402
from app.services import pipeline as P                            # noqa: E402
from qc.scope_contract import canonical_view                      # noqa: E402

EVID = ROOT / "docs" / "qc" / "phase171" / "evidence"
PARSED = ROOT / "data" / "parsed"

SAMPLES = {
    1: ("LM317", "LM317__lm317.pdf",
        "https://www.ti.com.cn/lit/ds/symlink/lm317.pdf"),
    2: ("ADS8568EVM-PDK", "ADS8568EVM-PDK__sbas543c.pdf",
        "https://www.ti.com/lit/ds/sbas543c/sbas543c.pdf"),
    3: ("DAC8568EVM", "DAC8568EVM__slau301.pdf",
        "https://www.ti.com/lit/ug/slau301/slau301.pdf"),
}


def prod_guard() -> dict:
    """生产 data/parsed 的轻量指纹：文件数 + 总字节 + 最新 mtime。

    不做全量 sha（13k 文件 280MB 太慢）；本轮的判据是「复跑期间没有新增写入」，
    文件数/字节数/最大 mtime 三项不变即成立，且对新增文件敏感。
    """
    files = list(PARSED.glob("*.json"))
    total = sum(f.stat().st_size for f in files)
    newest = max((f.stat().st_mtime for f in files), default=0)
    digest = hashlib.sha256(
        "|".join(f"{f.name}:{f.stat().st_size}:{int(f.stat().st_mtime)}"
                 for f in sorted(files)).encode()).hexdigest()
    return {"files": len(files), "bytes": total,
            "newest_mtime": time.strftime("%Y-%m-%d %H:%M:%S",
                                          time.localtime(newest)),
            "digest": digest}


def _pdf_text(path: Path) -> tuple[str, int]:
    with pymupdf.open(str(path)) as d:
        return "".join(p.get_text() for p in d), len(d)


def run_s1(out: Path) -> dict:
    mpn, fname, url = SAMPLES[1]
    pdf = ROOT / "data" / "pdfs" / fname
    t0 = time.time()
    rec = P.parse_pdf(pdf, mpn, url, out_dir=out)
    doc = rec.get("doc") or {}
    th = (doc.get("specs") or {}).get("thermal") or []
    placeholders = [r for r in th
                    if str(r.get("value")).strip().upper() in {"NA", "N/A", "—", "–"}]
    det = (doc.get("metadata") or {}).get("deterministic_extract") or {}
    return {
        "sample": "s1", "mpn": mpn, "pdf": fname,
        "pdf_sha256": doc.get("metadata", {}).get("pdf_hash"),
        "status": rec.get("status"), "error": rec.get("error"),
        "elapsed_s": round(time.time() - t0, 1),
        "thermal_rows": len(th),
        "thermal_names": sorted({r.get("name") for r in th if isinstance(r, dict)}),
        "placeholder_rows": len(placeholders),
        "pins": len(doc.get("pin_configuration") or []),
        "deterministic_extract": det,
        "llm_calls": len(rec.get("llm_calls") or []),
        "expect_thermal_34": len(th) == 34,
        "expect_no_placeholder": not placeholders,
        "expect_det_to_34": (det.get("thermal") or {}).get("to") == 34,
        "passed": bool(len(th) == 34 and not placeholders
                       and (det.get("thermal") or {}).get("to") == 34),
        "out_json": str(rec.get("json_path") or ""),
    }


def run_s2(out: Path) -> dict:
    mpn, fname, url = SAMPLES[2]
    pdf = ROOT / "data" / "pdfs" / fname
    t0 = time.time()
    rec = P.parse_pdf(pdf, mpn, url, out_dir=out)
    doc = rec.get("doc") or {}
    sp = doc.get("specs") or {}
    bi = doc.get("basic_info") or {}
    ods = sp.get("onboard_device_specs") or {}
    rows = {k: (sp.get(k) or []) for k in ("thermal", "esd")}
    # 行可能已被发布视图搬进 onboard_device_specs（D3 的正确归入），
    # 未标注统计必须覆盖两个容器，否则「主容器为空」会让检查假通过。
    all_rows = {k: list(rows[k]) + list((sp.get("onboard_device_specs") or {}).get(k) or [])
                for k in ("thermal", "esd")}
    labeled = {k: [r for r in v if isinstance(r, dict) and r.get("subject")]
               for k, v in rows.items()}
    unlabeled = {k: [r for r in v if isinstance(r, dict) and not r.get("subject")]
                 for k, v in all_rows.items()}
    subjects = {k: sorted({r.get("subject") for r in v if isinstance(r, dict)})
                for k, v in all_rows.items()}
    summary = sp.get("subject_summary") or {}
    # 发布视图（渲染层真正消费的对象）：芯片热阻/ESD 必须已搬出主容器
    view = canonical_view(doc)
    vsp = view.get("specs") or {}
    vods = vsp.get("onboard_device_specs") or {}
    ok_identity = (str(bi.get("identity") or "") == "evaluation_board"
                   and str(bi.get("device_mpn") or "") == "ADS8568")
    ok_moved = bool(ods.get("electrical")) and not (sp.get("electrical") or [])
    ok_labeled = all(not v for v in unlabeled.values())
    ok_view = (not (vsp.get("thermal") or [])) and (not (vsp.get("esd") or []))
    return {
        "sample": "s2", "mpn": mpn, "pdf": fname,
        "pdf_sha256": (doc.get("metadata") or {}).get("pdf_hash"),
        "status": rec.get("status"), "error": rec.get("error"),
        "elapsed_s": round(time.time() - t0, 1),
        "identity": bi.get("identity"),
        "device_mpn": bi.get("device_mpn"),
        "document_scope": bi.get("document_scope"),
        "specs_scope": sp.get("scope"),
        "onboard_electrical": len(ods.get("electrical") or []),
        "onboard_absolute_max": len(ods.get("absolute_max") or []),
        "main_electrical": len(sp.get("electrical") or []),
        "main_absolute_max": len(sp.get("absolute_max") or []),
        "thermal_rows": len(rows["thermal"]),
        "esd_rows": len(rows["esd"]),
        "rows_total": {k: len(v) for k, v in all_rows.items()},
        "subjects": subjects,
        "subject_summary": summary,
        "unlabeled": {k: len(v) for k, v in unlabeled.items()},
        "view_main_thermal": len(vsp.get("thermal") or []),
        "view_main_esd": len(vsp.get("esd") or []),
        "view_onboard_thermal": len(vods.get("thermal") or []),
        "view_onboard_esd": len(vods.get("esd") or []),
        "thermal_first": rows["thermal"][:3],
        "esd_first": rows["esd"][:2],
        "expect_identity_board_ads8568": ok_identity,
        "expect_chip_specs_moved": ok_moved,
        "expect_every_row_labeled": ok_labeled,
        "expect_publication_view_isolated": ok_view,
        "passed": bool(ok_identity and ok_moved and ok_labeled and ok_view),
        "out_json": str(rec.get("json_path") or ""),
    }


def run_s3(out: Path) -> dict:
    mpn, fname, url = SAMPLES[3]
    pdf = ROOT / "data" / "pdfs" / fname
    text, pages = _pdf_text(pdf)
    calls = {"n": 0}

    def boom(*a, **k):
        calls["n"] += 1
        raise AssertionError("非 Datasheet 不得调用模型")

    orig = pd.chat
    pd.chat = boom
    try:
        rec = P.parse_pdf(pdf, mpn, url, out_dir=out)
    finally:
        pd.chat = orig
    return {
        "sample": "s3", "mpn": mpn, "pdf": fname, "pages": pages,
        "is_datasheet": pd.is_datasheet(text),
        "status": rec.get("status"), "error": rec.get("error"),
        "llm_calls": calls["n"],
        "json_written": bool(rec.get("json_path")),
        "expect_skipped": str(rec.get("status")) == "skipped",
        "expect_no_llm": calls["n"] == 0,
        "expect_no_json": not rec.get("json_path"),
        "passed": bool(str(rec.get("status")) == "skipped" and calls["n"] == 0
                       and not rec.get("json_path")),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", required=True, choices=["1", "2", "3"])
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    EVID.mkdir(parents=True, exist_ok=True)
    tmp = Path(a.out) if a.out else Path(tempfile.mkdtemp(prefix=f"p171_s{a.sample}_"))
    tmp.mkdir(parents=True, exist_ok=True)

    before = prod_guard()
    res = {1: run_s1, 2: run_s2, 3: run_s3}[int(a.sample)](tmp)
    after = prod_guard()
    res["production_guard"] = {
        "before": before, "after": after,
        "unchanged": {k: before[k] == after[k] for k in before},
        "clean": all(before[k] == after[k] for k in before),
    }
    res["isolated_out_dir"] = str(tmp)
    name = {1: "s1-lm317", 2: "s2-ads8568evm-pdk", 3: "s3-dac8568evm"}[int(a.sample)]
    p = EVID / f"{name}.json"
    p.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("thermal_first", "esd_first")},
                     ensure_ascii=False, indent=1))
    print(f"[evidence] {p}")
    return 0 if res.get("passed") and res["production_guard"]["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
