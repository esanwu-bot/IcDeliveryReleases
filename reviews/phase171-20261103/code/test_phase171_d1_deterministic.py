#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 1.7.1 · D1：V2 的 `parse_pdf` 必须复用 Legacy 的确定性后处理。

背景（Phase 1.7 灰度，样本 1）：
同一份 LM317 PDF（SHA `1646fb2e…`）——
* Legacy（`parse_datasheets.parse_one`）→ thermal **34** 行 / 引脚 **3** 条；
* V2（`app/services/pipeline.parse_pdf`）→ thermal **36** 行（含 `NA`/`—`）/ 引脚 **4** 条（重复 OUTPUT）。

根因不是模型方差：V2 的 `parse_pdf` **没有调用** `apply_deterministic`。
本文件先把这条差异写成会失败的用例，再要求实现复用**同一份**函数（不许复制判据）。
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import parse_datasheets as pd                                   # noqa: E402
from app.services import pipeline as P                          # noqa: E402
from qc import deterministic_extract as DE                      # noqa: E402

PDF = ROOT / "data" / "pdfs" / "LM317__lm317.pdf"
pytestmark = pytest.mark.skipif(not PDF.exists(), reason="缺少 LM317 标尺 PDF")

#: 模型在一次真实运行中给出的形态：按封装分组、占位符照样落行、引脚多一条重复。
CANNED = {
    "basic_info": {"mpn": "LM317", "manufacturer": "Texas Instruments",
                   "identity": "chip",
                   "datasheet_url": "https://www.ti.com.cn/lit/ds/symlink/lm317.pdf",
                   "description": "3-Pin Adjustable Regulator"},
    "specs": {
        "electrical": [
            {"name": "Reference voltage", "value": "1.25", "unit": "V", "condition": ""},
            {"name": "Line regulation", "value": "0.01", "unit": "%/V", "condition": ""},
            {"name": "Load regulation", "value": "0.1", "unit": "%VO", "condition": ""},
        ],
        "absolute_max": [],
        "thermal": [
            {"name": "RθJA", "value": "66.8", "unit": "°C/W",
             "condition": "Legacy Chip; DCY (SOT-223) 4 PINS"},
            {"name": "RθJC(top)", "value": "43.2", "unit": "°C/W",
             "condition": "Legacy Chip; DCY (SOT-223) 4 PINS"},
            {"name": "RθJC(bot)", "value": "NA", "unit": "°C/W",
             "condition": "Legacy Chip; DCY (SOT-223) 4 PINS"},
            {"name": "RθJA", "value": "23.5", "unit": "°C/W",
             "condition": "Legacy Chip; KCS (TO-220) 3 PINS"},
            {"name": "RθJC(bot)", "value": "0.1", "unit": "°C/W",
             "condition": "Legacy Chip; KCS (TO-220) 3 PINS"},
            {"name": "RθJC(bot)", "value": "—", "unit": "°C/W",
             "condition": "New Chip; DCY (SOT-223) 4 PINS"},
            {"name": "RθJC(top)", "value": "43.6", "unit": "°C/W",
             "condition": "New Chip; KTT (TO-263) 3 PINS"},
        ],
        "esd": [],
        "package": {"type": "SOT-223", "pins": 4, "dimensions": ""},
        "temperature": {"operating": "-40°C to 125°C", "storage": "-65°C to 150°C"},
    },
    "pin_configuration": [
        {"pin": "1", "name": "ADJUST", "description": "Output voltage adjustment pin."},
        {"pin": "2", "name": "OUTPUT", "description": "Output voltage pin."},
        {"pin": "3", "name": "INPUT", "description": "Input voltage pin."},
        {"pin": "4", "name": "OUTPUT", "description": "Output voltage pin."},
    ],
    "features": [], "applications": [],
    "ordering_info": [{"mpn": "LM317DCYR", "package": "SOT-223", "pins": 4,
                       "status": "Active"}],
    "alternatives": [], "seo": {}, "metadata": {"confidence": 0.95},
}


def _stub_chat(monkeypatch):
    """模型调用固定返回同一份 CANNED（不碰网络、不引入模型方差）。"""
    def fake_chat(messages, **kw):
        return json.dumps(CANNED, ensure_ascii=False), {
            "prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150,
            "_model": "qwen-flash-stub", "_base": "https://stub.local/v1"}
    monkeypatch.setattr(pd, "chat", fake_chat)


def _v2_run(monkeypatch, tmp_path: Path) -> dict:
    _stub_chat(monkeypatch)
    return P.parse_pdf(PDF, "LM317", "https://www.ti.com.cn/lit/ds/symlink/lm317.pdf",
                       out_dir=tmp_path)


def _legacy_run(monkeypatch, tmp_path: Path) -> dict:
    _stub_chat(monkeypatch)
    tmp_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(pd, "OUT_DIR", tmp_path)
    # parse_one 末尾用 `out.relative_to(ROOT)` 生成 rec["out"]；测试的临时目录
    # 在仓库外，不一起改 ROOT 会抛 ValueError。
    monkeypatch.setattr(pd, "ROOT", tmp_path)
    rec = pd.parse_one(PDF, {})
    if rec.get("status") == "ok" and rec.get("out"):
        # Legacy 的 rec 不带 doc，落盘文件才是它的最终产物（含 identity_scope 改写）
        rec["doc"] = json.loads((tmp_path / rec["out"]).read_text(encoding="utf-8"))
    return rec


def _thermal_key(rows):
    return sorted((r.get("name"), str(r.get("value")),
                   str(r.get("condition") or "")) for r in rows)


def _pin_key(rows):
    return sorted((str(r.get("pin")), str(r.get("name"))) for r in rows)


# ---------------------------------------------------------------- D1 红先测试
def test_v2_parse_pdf_applies_deterministic(monkeypatch, tmp_path):
    """V2 落盘后：热阻 34 行、占位符不落行（否则就是 Phase 1.7 的 D1）。

    引脚：D4 之前 `extract_pins` 不认 LM317 的 `PIN | FUNCTION` 布局，模型给
    4 条会原样保留；D4 之后确定性层把它改成 3 条（ADJUST/INPUT/OUTPUT）。
    本用例同时守住这条覆盖关系：`deterministic_extract.pins` 必须是 4→3。
    """
    rec = _v2_run(monkeypatch, tmp_path)
    assert rec["status"] == "ok", rec.get("error")
    doc = rec["doc"]
    thermal = doc["specs"]["thermal"]
    assert len(thermal) == 34, f"实得 {len(thermal)} 行（模型原样是 36）"
    assert not [r for r in thermal
                if str(r.get("value")).strip().upper() in DE._PLACEHOLDERS]
    assert len(doc["pin_configuration"]) == 3
    # 记录可审计：走了哪条确定性路径、从多少行改到多少行
    det = (doc.get("metadata") or {}).get("deterministic_extract") or {}
    assert det.get("thermal", {}).get("to") == 34, det
    assert det.get("thermal", {}).get("from") == 7, det
    assert det.get("pins") == {"from": 4, "to": 3, "method": "deterministic"}, det


def test_repair_retry_keeps_deterministic_metadata(monkeypatch, tmp_path):
    """核心校验触发修复重试时，确定性摘要也不许丢（metadata 被换对象的坑）。

    V2 的 URL 由 fetch 传入；这里故意**不传** URL，强制走 `check_core` 失败 →
    修复重试路径。重试稿替换 doc 后，`meta` 若不重取，会把
    `deterministic_extract` 写进孤儿 metadata（灰度实测丢失）。
    """
    _stub_chat(monkeypatch)
    # CANNED 本身带 datasheet_url；这里要构造「模型没写 URL、调用方也没传」的形态。
    no_url = copy.deepcopy(CANNED)
    no_url["basic_info"].pop("datasheet_url", None)
    monkeypatch.setattr(pd, "chat", lambda messages, **kw: (
        json.dumps(no_url, ensure_ascii=False),
        {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150,
         "_model": "qwen-flash-stub", "_base": "https://stub.local/v1"}))
    rec = P.parse_pdf(PDF, "LM317", "", out_dir=tmp_path)
    assert rec["status"] == "ok", rec.get("error")
    doc = rec["doc"]
    assert len(doc["specs"]["thermal"]) == 34
    det = (doc.get("metadata") or {}).get("deterministic_extract") or {}
    assert det.get("thermal", {}).get("to") == 34, det
    assert (doc.get("metadata") or {}).get("core_validation") is not None
    assert len(rec["llm_calls"]) == 2, "没传 URL 应触发一次修复重试"


def test_v2_and_legacy_deterministic_agree(monkeypatch, tmp_path):
    """同一冻结 PDF、同一份模型输出：V2 与 Legacy 的确定性结果必须逐条一致。"""
    v2 = _v2_run(monkeypatch, tmp_path / "v2")
    legacy = _legacy_run(monkeypatch, tmp_path / "legacy")
    assert legacy["status"] == "ok", legacy.get("error")
    # V2 的 doc 来自 rec；Legacy 的 doc 就是模型 + 确定性后的同一对象
    v2_doc = v2["doc"]
    legacy_doc = legacy["doc"]
    assert _thermal_key(v2_doc["specs"]["thermal"]) == _thermal_key(legacy_doc["specs"]["thermal"])
    assert _pin_key(v2_doc["pin_configuration"]) == _pin_key(legacy_doc["pin_configuration"])


def test_apply_deterministic_is_idempotent():
    """重复调用不得二次清洗 / 数据损坏（D1 验收第 3 条）。"""
    import pymupdf
    doc = copy.deepcopy(CANNED)
    with pymupdf.open(str(PDF)) as fd:
        DE.apply_deterministic(doc, fd)
        once_th = copy.deepcopy(doc["specs"]["thermal"])
        once_pins = copy.deepcopy(doc["pin_configuration"])
        DE.apply_deterministic(doc, fd)
    assert doc["specs"]["thermal"] == once_th
    assert doc["pin_configuration"] == once_pins
    assert len(doc["specs"]["thermal"]) == 34


def test_stage_llm_default_path_lands_deterministic(tmp_path, monkeypatch):
    """五阶段路径的补证：`stage_llm` **不传 llm_fn** 时走默认 `PLATFORM.parse_pdf`。

    D1 的验收第 5 条要求「证明五阶段实际调用了该函数，而不只是单测直调」：
    这里从阶段层进入（`Ctx` + 真实切片），让默认实现自己跑，落盘 JSON 必须带
    `metadata.deterministic_extract`（thermal 从模型原样 7 行改成 34 行）。
    """
    from app.pipeline import preprocess as PP
    from app.pipeline import stages as S
    from app.pipeline.stage_state import StageStateStore
    import parse_datasheets as pd

    slc, _ = PP.load_or_build(PDF, "LM317", root=tmp_path / "slices", pd_module=pd)
    _stub_chat(monkeypatch)
    with StageStateStore(tmp_path / "s.sqlite3") as st:
        ctx = S.Ctx(mpn="LM317", mpn_key="lm317", pdf_path=PDF,
                    pdf_sha256=slc.pdf_sha256, slice=slc,
                    out_dir=tmp_path / "out", state=st)
        r = S.stage_llm(ctx, pd_module=pd)          # 不给 llm_fn → 默认 parse_pdf
    assert r.status == "ok", (r.status, r.error)
    doc = json.loads(Path(r.artifact).read_text(encoding="utf-8"))
    assert len(doc["specs"]["thermal"]) == 34
    det = (doc.get("metadata") or {}).get("deterministic_extract") or {}
    assert det.get("thermal", {}).get("to") == 34, det


def test_placeholder_edges_are_consistent():
    """`NA`/`—` 不落行；KCS 的 0.1 不许冒充 DCY。

    引脚不在本用例断言范围（见上一条：LM317 的引脚布局不在 `extract_pins`
    覆盖范围，确定性层对它没有改写权，Legacy/V2 都保留模型的引脚）。
    """
    import pymupdf
    doc = copy.deepcopy(CANNED)
    with pymupdf.open(str(PDF)) as fd:
        DE.apply_deterministic(doc, fd)
    bot = [r for r in doc["specs"]["thermal"] if r["name"] == "RθJC(bot)"]
    assert not any("DCY" in r["condition"] and "Legacy" in r["condition"] for r in bot)
    assert any(r["value"] == "0.1" and "KCS" in r["condition"] for r in bot)
    assert all(str(r["value"]) not in ("NA", "N/A", "—") for r in bot)
