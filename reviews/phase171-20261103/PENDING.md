# 待验证项（Reviewer 阻断清单）

| 项 | 级别 | 状态 | 要求 |
|---|---|---|---|
| 服务器同构五阶段复跑 | 阻断整体验收 | PENDING | 用服务器 Docker + Redis DB8 + `/tmp/p17` 跑 `p17.sh`/`run_s1..s3.sh`；核对状态流转、attempts、parse_count、重复投递、生产零污染 |
| 真实 `board_user_guide` PDF | 阻断 D3 完整性 | PENDING | 补 SBAU193E 或同类真实 UG：board 行留主容器、onboard 行隔离、ambiguous 进 unresolved |
| D4 `PIN\|FUNCTION` | 独立验收项 | PENDING | 对 `19ef765` 之后的 HEAD 重新跑真实 LM317 + 该布局夹具，不得引用旧提交结果 |

## 当前裁定建议（实现方自述，供 Reviewer 覆盖）

- D1 / D2 / D3(datasheet 分支)：按现有证据 PASS（待代码级独立复核）
- D3(board_user_guide 分支)：PENDING
- 五段服务器同构：PENDING
- D4：PENDING
- Phase 1.7.1 整体：WAITING_FOR_REVIEWER
- V2 全量启用：不批准
- V3 重建与打包：不启动
