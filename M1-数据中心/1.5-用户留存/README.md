---
page: 1.5
name: 用户留存
route: /analytics/retention
module: M1
permission: analytics:report:view
priority: P1
status: 缺失
estimate_days: 5
---

# 1.5 · 用户留存

> ⚠️ P1 页面,当前为精简规格。排期时按 10 段模板补全。

## 1. 用途
按注册批次看留存曲线,评估拉新质量与产品粘性。

## 2. 入口
菜单:数据中心 → 玩家分析 → 用户留存(**「玩家分析」是分组**)

## 3. 字段清单(草案)
**矩阵列**:`注册日 | 注册人数 | D1 | D3 | D7 | D14 | D30`,单元格显示 `人数 (百分比)`
**留存定义**(⬜ 待定):回访 = 登录?还是投注?两者留存率差异很大

## 4. 操作与权限
`analytics:report:view` 查看 · `analytics:export` 导出

## 5. 状态清单
空 / 加载 / 错误 / 无权限 / 数据未成熟(D30 需等 30 天,灰显)

## 6. 涉及表
`UserRetentionFact`(只读)→ `../表设计.prisma`

## 7. 关联页面
用户流失(1.6)· 渠道报表(1.4)· 用户列表(M2.1)
