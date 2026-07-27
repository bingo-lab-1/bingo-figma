---
page: 3.9
name: 通道管理
route: /finance/channel
module: M3
permission: finance:channel:edit
priority: P1
status: 需改造
estimate_days: 5
---

# 3.9 · 通道管理

> **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
管理支付与提现通道,监控通道成功率。**当前仅支持加密币,法币待定。**

## 2. 入口
菜单:财务管理 → 通道管理

## 3. 字段清单
 待补

## 4. 操作与权限
主权限码 `finance:channel:edit`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态  待补

## 6. 交互流程
 待补

## 7. 涉及表
`PaymentChannel`(owner)· `CryptoCoins` `ChainNetwork`(M8 只读) → `../表设计.prisma`

## 8. 关联页面
充值订单(3.1)· 提现订单(3.2)· 币种汇率(M8.3)
