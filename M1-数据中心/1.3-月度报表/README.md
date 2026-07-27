---
page: 1.3
name: 月度报表
route: /analytics/monthly
module: M1
permission: analytics:report:view
priority: P1
status: 缺失
estimate_days: 3
---

# 1.3 · 月度报表

> ⚠️ P1 页面,当前为精简规格。排期时按 10 段模板补全。

## 1. 用途
按月粒度看长期趋势,供管理层与投资人使用。

## 2. 入口
菜单:数据中心 → 报表 → 月度报表(**「报表」是分组**)

## 3. 字段清单(草案)
**表格列**:`月份 | 注册 | 首充人数 | 充值 | 提现 | 净充值 | 投注额 | GGR | NGR | 活跃 | 月留存`
在 1.2 基础上增加同比/环比列。

## 4. 操作与权限
`analytics:report:view` 查看 · `analytics:export` 导出

## 5. 状态清单
空 / 加载 / 错误 / 无权限 / 当月数据未完整(提示)

## 6. 涉及表
`DailySummary`(按月聚合,只读)→ `../表设计.prisma`

## 7. 关联页面
每日报表(1.2)· 大盘概览(1.1)
