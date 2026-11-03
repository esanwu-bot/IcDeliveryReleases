# 代码基线

```
HEAD=4572f4a  describe=delivery-20261102-V3-100-g4572f4a-dirty

4572f4a docs(qc): Phase 1.7.1 审查包生成器 + 渲染消费端证据 + D3 四分支用例
98b64a0 docs(qc): 验收报告补记 D4(19ef765) 引脚布局修复的未验证状态
56cdb97 docs(qc): Phase 1.7.1 验收报告 + 三件冻结样本复跑证据，总线转 Reviewer
19ef765 fix(pins): D4 支持 PIN|FUNCTION 多封装列布局，描述不得被误认成引脚名
9beeb7d fix(identity): D3 发布视图按行级 subject 隔离 thermal/esd（消费端闭环）
5d3a88c docs(qc): Phase 1.7.1 回归报告 —— D1/D2/D3 三项通过 + 冻结样本复跑证据
8b238c5 docs(qc): Phase 1.7.1 D1-D3 集成验收 —— 运行路径证据与三件冻结样本复跑
88d023e fix(pipeline): D1 复核修正 —— 早落 datasheet_url、重试后重取 metadata（避免白烧一次修复调用）
35d4e62 feat(identity): D3 板卡 thermal/esd 字段级主体归属（不搬容器、判不出即 ambiguous）
4951c4b fix(pipeline): D2 stage_llm 落 llm_usage（复用 _log_calls，缓存不记假账）
27bdd02 fix(pipeline): D1 parse_pdf 接入确定性后处理（复用 apply_deterministic）
a0a2ad0 docs(algorithm_lab): 总线刷新为 Phase 1.7.1（D1-D3 待集成，V3 HOLD）
```
