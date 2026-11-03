#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 1.7.1 · D2：V2 的 LLM 阶段必须落 `llm_usage` 账本。

背景（Phase 1.7 灰度）：V2 三件样本的 `llm_usage` 全是 0 行 ——
`_log_calls` 只在 Legacy 的 `pipeline.llm_stage` 里调用，`stage_llm` 没有。
灰度因此无法用数据库核对 Token 成本，只能回头翻网关账单。

本文件守三条口径（与裁决一致）：
1. **一次真实调用一条记录**，不按「阶段执行次数」代替调用次数；
2. **缓存命中不产生假记录**（命中走 stage_llm 的早返回，不进 `_run`）；
3. **重试/多次调用/失败返回都保留可追溯记录**（ok/error/attempt 原样）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import parse_datasheets as pd                                   # noqa: E402
from app.pipeline import preprocess as PP                       # noqa: E402
from app.pipeline import stages as S                             # noqa: E402
from app.pipeline.stage_state import StageStateStore             # noqa: E402
from app.services import pipeline as PLATFORM                    # noqa: E402

PDF = ROOT / "data" / "pdfs" / "LM317__lm317.pdf"
pytestmark = pytest.mark.skipif(not PDF.exists(), reason="缺少 LM317 标尺 PDF")

CALLS = [
    {"stage": "parse", "model": "qwen-flash", "provider": "dashscope.aliyuncs.com",
     "usage": {"prompt_tokens": 900, "completion_tokens": 400, "total_tokens": 1300},
     "latency_ms": 12000, "ok": True, "error": "", "attempt": 1},
    {"stage": "repair", "model": "qwen-flash", "provider": "dashscope.aliyuncs.com",
     "usage": {"prompt_tokens": 1100, "completion_tokens": 500, "total_tokens": 1600},
     "latency_ms": 9000, "ok": False, "error": "JSONDecodeError: truncated", "attempt": 2},
]


def _fake_llm(out_dir: Path, calls: list[dict]):
    def fn(pdf, mpn, url, *, text=None, pages_used=None, pages_total=None, out_dir=out_dir):
        target = Path(out_dir) / f"{mpn}_d2stub.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({"basic_info": {"mpn": mpn},
                                      "specs": {"electrical": [{"name": "x"}]}}),
                          encoding="utf-8")
        return {"status": "ok", "json_path": str(target), "ms": 21000,
                "confidence": 0.9, "electrical": 1, "pins": 0,
                "llm_calls": list(calls)}
    return fn


@pytest.fixture
def slice_ctx(tmp_path):
    slc, _ = PP.load_or_build(PDF, "LM317", root=tmp_path / "slices", pd_module=pd)
    return slc


def _run(tmp_path, slc, calls, spy):
    with StageStateStore(tmp_path / "state.sqlite3") as st:
        ctx = S.Ctx(mpn="LM317", mpn_key="lm317", pdf_path=PDF,
                    pdf_sha256=slc.pdf_sha256, slice=slc,
                    out_dir=tmp_path / "out", state=st, item={"id": 42})
        r1 = S.stage_llm(ctx, llm_fn=_fake_llm(tmp_path / "out", calls), pd_module=pd)
        r2 = S.stage_llm(ctx, llm_fn=_fake_llm(tmp_path / "out", calls), pd_module=pd)
        return r1, r2


def test_one_record_per_real_call_with_all_fields(monkeypatch, tmp_path, slice_ctx):
    """2 次调用 → 2 条记录，字段齐全（不是按阶段次数记 1 条）。"""
    rows: list[dict] = []
    monkeypatch.setattr(PLATFORM.usage, "record", lambda **kw: rows.append(kw))
    r1, _ = _run(tmp_path, slice_ctx, CALLS, None)
    assert r1.status == "ok"
    assert len(rows) == 2, rows
    first, second = rows
    assert first["item_id"] == 42 and first["mpn_key"] == "lm317"
    assert first["stage"] == "parse" and first["attempt"] == 1 and first["ok"] is True
    assert first["usage"]["total_tokens"] == 1300
    assert second["stage"] == "repair" and second["attempt"] == 2
    assert second["ok"] is False and "truncated" in second["error"]


def test_cache_hit_records_no_fake_call(monkeypatch, tmp_path, slice_ctx):
    """第二次是缓存命中 → 不新增记录（R2 必须是 cached）。"""
    rows: list[dict] = []
    monkeypatch.setattr(PLATFORM.usage, "record", lambda **kw: rows.append(kw))
    r1, r2 = _run(tmp_path, slice_ctx, CALLS, None)
    assert r1.status == "ok"
    assert r2.status == "cached", r2
    assert len(rows) == 2, f"缓存命中又写了 {len(rows) - 2} 条假记录"


def test_no_calls_no_records(monkeypatch, tmp_path, slice_ctx):
    """没有 llm_calls（如模型未调用）时不许凭空造账。"""
    rows: list[dict] = []
    monkeypatch.setattr(PLATFORM.usage, "record", lambda **kw: rows.append(kw))
    _run(tmp_path, slice_ctx, [], None)
    assert rows == []
