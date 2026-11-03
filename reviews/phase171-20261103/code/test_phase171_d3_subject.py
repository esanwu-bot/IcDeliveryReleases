#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 1.7.1 · D3：板卡 `thermal` / `esd` 的字段级主体归属。

Phase 1.7 灰度暴露的问题：板卡分支只搬 `electrical / absolute_max`，
`thermal`（11 行）/ `esd`（2 行）仍留在主容器，仅靠 `specs.scope=onboard_device`
做整体标记 —— 消费者无法仅凭容器位置判断一行属于板卡还是板载芯片。

裁决要求：
* **不整体搬容器**（不能把所有 thermal/ESD 一律搬进板卡容器）；
* 每一行要有**可复算的来源证据** → `subject` + `subject_source`；
* 判不出主体的行保留并标 `ambiguous`，交人工，**不自动归属**。
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qc import identity_scope as IS                             # noqa: E402
from qc import scope_contract as SC                             # noqa: E402

THERMAL = [
    {"name": "RθJA", "value": "42.9", "unit": "°C/W", "condition": "64-Pin VQFN"},
    {"name": "RθJC(top)", "value": "18.2", "unit": "°C/W", "condition": "64-Pin VQFN"},
    {"name": "ψJT", "value": "9.1", "unit": "°C/W", "condition": "64-Pin VQFN"},
]
ESD = [
    {"name": "HBM", "value": "±2500", "unit": "V"},
    {"name": "CDM", "value": "±500", "unit": "V"},
]


def _board_doc() -> dict:
    return {
        "basic_info": {"mpn": "ADS8568EVM-PDK", "manufacturer": "Texas Instruments"},
        "specs": {
            "electrical": [{"name": "Resolution", "value": "16", "unit": "Bits"}],
            "absolute_max": [{"name": "Supply Voltage", "value": "-0.3 to 18", "unit": "V"}],
            "thermal": copy.deepcopy(THERMAL),
            "esd": copy.deepcopy(ESD),
            "package": {"type": "64-Pin VQFN", "pins": 64, "onboard_device": "ADS8568"},
            "temperature": {"operating": "-40°C to 125°C", "storage": "-65°C to 150°C"},
        },
        "ordering_info": [], "metadata": {},
    }


def test_device_datasheet_rows_are_marked_onboard_device():
    """器件手册来源：thermal/esd 每一行标 onboard_device，并归入隔离桶。

    2026-11-03 验收口径修正：原用例断言「不搬容器」只覆盖标注层，会让芯片热阻
    继续留在板卡主容器（渲染层读 `canonical_view`，照样当板级规格印出去）。
    正确契约是**按行证据搬**：`subject=onboard_device` → `onboard_device_specs`；
    `subject=board` 的整板参数仍留在主容器（见发布视图用例）。
    """
    doc = _board_doc()
    rec = IS.apply(doc, "ADS8568EVM-PDK",
                   pdf_text=("ADS8568EVM-PDK Evaluation Module\n"
                             "The ADS8568 is an 8-channel, 16-bit simultaneous-sampling ADC."),
                   pdf_path="data/pdfs/ADS8568EVM-PDK__sbas543c.pdf")
    assert rec["identity"] == "evaluation_board", rec
    assert doc["basic_info"]["document_scope"] == "onboard_device_datasheet", rec
    assert doc["specs"]["thermal"] == [], "芯片热阻不许留在板卡主容器"
    assert doc["specs"]["esd"] == []
    ods = doc["specs"]["onboard_device_specs"]
    assert len(ods["thermal"]) == len(THERMAL), "芯片热阻必须归入 onboard_device"
    assert len(ods["esd"]) == len(ESD)
    for row in ods["thermal"] + ods["esd"]:
        assert row["subject"] == "onboard_device", row
        assert row["subject_source"] == "onboard_device_datasheet", row
        assert "subject_review" not in row
    assert doc["specs"]["subject_summary"]["thermal"]["onboard_device"] == len(THERMAL)
    assert doc["specs"]["subject_summary"]["esd"]["onboard_device"] == len(ESD)
    # 电气/绝对最大值仍按原逻辑搬进隔离区（D3 不改这部分）
    assert doc["specs"]["electrical"] == []
    assert doc["specs"]["absolute_max"] == []


def test_board_guide_rows_are_marked_board():
    """与请求号绑定的板卡 UG：行主体是 board。"""
    doc = _board_doc()
    assert IS._stamp_row_subjects(doc, "board_user_guide") == len(THERMAL) + len(ESD)
    for row in doc["specs"]["thermal"] + doc["specs"]["esd"]:
        assert row["subject"] == "board"
        assert row["subject_source"] == "board_user_guide"


def test_unresolved_rows_are_ambiguous_and_keep_human_review():
    """主体判不出 → ambiguous + needs_human，行必须保留（不得猜、不得删）。"""
    doc = _board_doc()
    assert IS._stamp_row_subjects(doc, "") == len(THERMAL) + len(ESD)
    for row in doc["specs"]["thermal"] + doc["specs"]["esd"]:
        assert row["subject"] == "ambiguous"
        assert row["subject_source"] == "unresolved"
        assert row["subject_review"] == "needs_human"


def test_subject_stamping_is_idempotent():
    """同一份 doc 跑两次，主体不翻转（幂等）。"""
    doc = _board_doc()
    IS._stamp_row_subjects(doc, "onboard_device_datasheet")
    before = copy.deepcopy(doc["specs"]["thermal"])
    IS._stamp_row_subjects(doc, "board_user_guide")     # 第二次给了不同证据
    assert doc["specs"]["thermal"] == before, "已标过的行不许被第二次覆盖"


def test_chip_docs_are_not_stamped():
    """芯片 doc 没有板卡主体问题，不许无端加 subject 字段。"""
    doc = {
        "basic_info": {"mpn": "LM317", "manufacturer": "Texas Instruments"},
        "specs": {"thermal": copy.deepcopy(THERMAL), "esd": copy.deepcopy(ESD),
                  "package": {"type": "SOT-223", "pins": 4}},
        "ordering_info": [{"mpn": "LM317DCYR", "package": "SOT-223"}],
    }
    rec = IS.apply(doc, "LM317", pdf_text="LM317 3-Pin Adjustable Regulator",
                   pdf_path="data/pdfs/LM317__lm317.pdf")
    assert rec["identity"] == "chip", rec
    assert "subject" not in doc["specs"]["thermal"][0]
    assert "subject_summary" not in doc["specs"]


# ---------------------------------------------------------------- 发布视图闭环
def _board_view_doc(scope: str, subject: str) -> dict:
    """最小板卡 doc：主容器直接放 thermal/esd，行级 `subject` 是唯一证据。"""
    rows = copy.deepcopy(THERMAL)
    esd = copy.deepcopy(ESD)
    for r in rows + esd:
        r["subject"] = subject
        r["subject_source"] = "board_user_guide" if subject == "board" else scope
    return {
        "basic_info": {"mpn": "ADS8568EVM-PDK", "manufacturer": "Texas Instruments",
                       "identity": "evaluation_board", "device_mpn": "ADS8568"},
        "specs": {
            "scope": scope,
            "electrical": [], "absolute_max": [],
            "thermal": rows, "esd": esd,
            "package": {"type": "Evaluation Board", "pins": 0,
                        "onboard_device": "ADS8568"},
            "temperature": {"operating": "not_specified", "storage": "not_specified"},
        },
        "pin_configuration": [], "ordering_info": [], "metadata": {},
    }


def test_publication_view_isolates_onboard_thermal_esd():
    """发布视图必须把 `subject=onboard_device` 的 thermal/esd 搬出主容器。

    这是 Phase 1.7.1 D3 的**消费端**验收：只标注不搬，板卡页仍会把芯片热阻
    当板级规格渲染（渲染层读的是 `canonical_view`，不是原 doc）。
    """
    doc = _board_doc()
    IS.apply(doc, "ADS8568EVM-PDK",
             pdf_text=("ADS8568EVM-PDK Evaluation Module\n"
                       "The ADS8568 is an 8-channel, 16-bit simultaneous-sampling ADC."),
             pdf_path="data/pdfs/ADS8568EVM-PDK__sbas543c.pdf")
    view = SC.canonical_view(doc)
    assert view["specs"]["thermal"] == [], "芯片热阻仍留在板卡主容器"
    assert view["specs"]["esd"] == []
    ods = view["specs"]["onboard_device_specs"]
    assert len(ods["thermal"]) == len(THERMAL)
    assert len(ods["esd"]) == len(ESD)
    assert {r["subject"] for r in ods["thermal"]} == {"onboard_device"}
    assert ods["device_mpn"] == "ADS8568"


def test_publication_view_keeps_board_level_thermal():
    """`subject=board` 的整板参数必须留在主容器 —— 不许一刀切搬走。"""
    doc = _board_view_doc("board", "board")
    view = SC.canonical_view(doc)
    assert len(view["specs"]["thermal"]) == len(THERMAL)
    assert len(view["specs"]["esd"]) == len(ESD)


def test_publication_view_archives_ambiguous_rows():
    """主体判不出的行进 `unresolved_specs`（待人工），不许当成板级规格发布。"""
    doc = _board_view_doc("board", "ambiguous")
    view = SC.canonical_view(doc)
    assert view["specs"]["thermal"] == []
    unresolved = view["specs"]["unresolved_specs"]
    assert len(unresolved["thermal"]) == len(THERMAL)
    assert unresolved["scope"] == "unresolved"


def test_rows_without_subject_follow_doc_scope_without_loss():
    """缺少 `subject` 的旧件按**文档 scope**兼容处理，且一行都不能静默丢。

    兼容策略（Reviewer 点名第 4 种情况）：没有行级证据时退回文档级 `scope`，
    归档到对应桶；行内容原样保留（不是删除，也不是默认塞进正式容器）。
    """
    doc = _board_view_doc("onboard_device", "")
    before = copy.deepcopy(doc["specs"]["thermal"])
    view = SC.canonical_view(doc)
    assert view["specs"]["thermal"] == [], "缺主体的行不许留在正式板卡容器"
    ods = view["specs"]["onboard_device_specs"]
    assert len(ods["thermal"]) == len(THERMAL), "缺主体的行被静默丢弃"
    assert ods["thermal"] == before, "归档必须原样保留，不许改写行内容"


def test_canonical_view_is_idempotent_and_does_not_mutate_source():
    """发布视图重复执行：不重复搬迁、不丢行、不改原始 doc。"""
    doc = _board_view_doc("board", "board")
    src_rows = copy.deepcopy(doc["specs"]["thermal"])
    v1 = SC.canonical_view(doc)
    assert len(v1["specs"]["thermal"]) == len(THERMAL)
    v2 = SC.canonical_view(copy.deepcopy(v1))
    assert len(v2["specs"]["thermal"]) == len(THERMAL), "重复执行把行搬走或搬重了"
    assert v2["specs"]["thermal"] == v1["specs"]["thermal"]
    assert not (v2["specs"].get("onboard_device_specs") or {}).get("thermal")
    assert doc["specs"]["thermal"] == src_rows, "canonical_view 改动了原始 doc"
