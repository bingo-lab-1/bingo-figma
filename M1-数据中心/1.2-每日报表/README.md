---
page: 1.2
name: 每日报表
route: /analytics/daily
module: M1
permission: analytics:report:view
priority: P1
status: 缺失
estimate_days: 5
---

# 1.2 · 每日报表

> ⚠️ P1 页面,当前为精简规格。排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
按日粒度查看全站经营数据,支持多日对比。

## 2. 入口
菜单:数据中心 → 报表 → 每日报表(**「报表」是分组,非页面**)
跳入:大盘概览指标卡下钻

## 3. 字段清单(草案)
**表格列**:`日期 | 注册 | 首充人数 | 充值金额 | 充值人数 | 提现金额 | 投注额 | 派彩 | GGR | NGR | 彩金成本 | 活跃`
口径与 1.1 完全一致(⬜ 待统一口径后锁定)

## 4. 操作与权限
`analytics:report:view` 查看 · `analytics:export` 导出

## 5. 状态清单
空 / 加载 / 错误 / 无权限 / 数据延迟提示

## 6. 涉及表
`DailySummary` `ChannelDailySummary`(只读)→ `../表设计.prisma`

## 7. 关联页面
大盘概览(1.1)· 月度报表(1.3)· 渠道报表(1.4)
