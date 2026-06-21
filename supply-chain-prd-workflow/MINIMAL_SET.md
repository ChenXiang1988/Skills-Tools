# 最小必需集合

## 结论

如果目标是完成一条供应链后台文档闭环，最小必需集合是：

1. `supply-chain-prd-writer`
2. `strategy-red-team`
3. `pre-mortem`
4. `release-notes`

## 为什么是这四个

- `supply-chain-prd-writer` 负责主流程，不可少
- `strategy-red-team` 负责在定稿前找逻辑漏洞
- `pre-mortem` 负责在上线前找真实风险
- `release-notes` 负责把结果交给业务侧

## 推荐但非必需

- `problem-statement`：当输入很散、问题不清时先用

## 可选扩展

- `prd-development`
- `create-prd`
- `workshop-facilitation`
- `jobs-to-be-done`
- `proto-persona`

## 收缩原则

如果后续继续压缩，优先删掉可选扩展，不要动最小必需集合。
