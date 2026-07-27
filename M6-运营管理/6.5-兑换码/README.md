---
page: 6.5
name: 兑换码
route: /ops/redeem-code
module: M6
permission: ops:redeem:create
priority: P1
status: 缺失
estimate_days: 5
---

# 6.5 · 兑换码

> ⚠️ **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
生成与管理兑换码批次,追踪核销情况。

## 2. 入口
菜单:运营管理 → 兑换码

## 3. 字段清单
⬜ 待补

## 4. 操作与权限
主权限码 `ops:redeem:create`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态 ⬜ 待补

## 6. 交互流程
⬜ 待补

## 7. 涉及表
`RedeemCodeBatch` `RedeemCode`(owner,新增) → `../表设计.prisma`

## 8. 关联页面
站内信(6.1)· 活动领取记录(M4.3)
