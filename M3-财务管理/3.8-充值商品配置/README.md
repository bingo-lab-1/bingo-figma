---
page: 3.8
name: 充值商品配置
route: /finance/recharge/product
module: M3
permission: finance:product:edit
priority: P1
status: 缺失
estimate_days: 5
---

# 3.8 · 充值商品配置

> ⚠️ **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
配置充值档位 SKU,并绑定活动类型(如首充档位)。

## 2. 入口
菜单:财务管理 → 充值 → 充值商品配置(**「充值」是分组**)

## 3. 字段清单
⬜ 待补

## 4. 操作与权限
主权限码 `finance:product:edit`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态 ⬜ 待补

## 6. 交互流程
⬜ 待补

## 7. 涉及表
`RechargeProduct`(owner,新增) → `../表设计.prisma`

## 8. 关联页面
充值订单(3.1)· 活动引擎(M4.1)
