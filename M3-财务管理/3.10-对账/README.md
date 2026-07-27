---
page: 3.10
name: 对账
route: /finance/reconciliation
module: M3
permission: finance:reconcile:view
priority: P2
status: 缺失
estimate_days: 10
---

# 3.10 · 对账

> **P2 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
日终对账:平台账 vs 通道账 vs 链上账,发现差异。**资损兜底。**

## 2. 入口
菜单:财务管理 → 对账

## 3. 字段清单
 待补

## 4. 操作与权限
主权限码 `finance:reconcile:view`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态  待补

## 6. 交互流程
 待补

## 7. 涉及表
`Transaction` `RechargeOrder` `WithdrawOrder`(owner) → `../表设计.prisma`

## 8. 关联页面
充值订单(3.1)· 提现订单(3.2)· 通道管理(3.9)
