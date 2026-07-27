---
page: 8.3
name: 币种与汇率
route: /system/currency
module: M8
permission: system:currency:edit
priority: P1
status: 需改造
estimate_days: 4
---

# 8.3 · 币种与汇率

> **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
管理支持的币种与汇率。**当前仅加密币,法币(BRL)待决策。**

## 2. 入口
菜单:系统设置 → 币种与汇率

## 3. 字段清单
 待补

## 4. 操作与权限
主权限码 `system:currency:edit`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态  待补

## 6. 交互流程
 待补

## 7. 涉及表
`CryptoCoins` `ChainNetwork` `FiatCurrency`(owner,新增) → `../表设计.prisma`

## 8. 关联页面
通道管理(M3.9)· 提现配置(M3.4)
