---
module: M1
name: 数据中心
owner: 待定
status: 设计中
pages: 7
p0: 1
estimate_days: 8
updated: 2026-07-26
---

# M1 · 数据中心

## 1. 定位与边界

**做什么**:全平台经营数据的读侧,支撑运营决策。

**不做什么**
- 不产生任何业务动作(不改数据、不发钱、不审核)
- 不做实时大屏(延迟到分钟级即可)
- 不承担 BI 自助分析(复杂分析走数仓,不在后台)

**铁律**:**只读汇总表,禁止直连业务表** —— 否则数据量一大,后台查询会拖垮生产库。

## 2. 术语表

| 术语 | 定义 | 代码标识 |
|---|---|---|
| GGR | 毛收入 = 总投注 − 总派彩 | `ggr` |
| NGR | 净收入 = GGR − 彩金成本 − 返佣 | `ngr` |
| FTD | 首次充值(人数/金额) | `ftd` |
| 留存 | 某日注册用户在第 N 日回访占比 | `retention` |
| 统计日 | 按运营时区切日(时区待定,见决策清单 #4) | `statDate` |

## 3. 依赖关系

**上游依赖(我引用)** —— 全部只读
- `M2-用户管理`:`User` `LoginRecord`
- `M3-财务管理`:`Transaction` `RechargeOrder` `WithdrawOrder`
- `M4-玩法中心`:`BetRecords` `ActivityClaim`
- `M5-代理渠道`:`Channel` `Promoter`

**下游被依赖(谁引用我)**
- 无。本模块是终端消费者。

## 4. 数据模型

**拥有的表**(全部为汇总表)

| 表 | 说明 | 现状 |
|---|---|---|
| `DashboardTimeSummary` | 分时汇总 | 已有 |
| `DailySummary` | 全站每日汇总 | 新增 |
| `ChannelDailySummary` | 分渠道每日 | 新增 |
| `GameDailySummary` | 分游戏每日 | 新增 |
| `UserRetentionFact` | 留存事实表 | 新增 |
| `ActivityRoiDaily` | 活动 ROI 日报 | 新增 |

详见 `表设计.prisma`

## 5. 菜单结构与页面索引

```
数据中心
├─ 大盘概览            → 1.1
├─ 报表  (分组)
│   ├─ 每日报表        → 1.2
│   └─ 月度报表        → 1.3
├─ 渠道报表            → 1.4
├─ 玩家分析  (分组)
│   ├─ 用户留存        → 1.5
│   └─ 用户流失        → 1.6
└─ 活动 ROI            → 1.7
```

| 编号 | 页面 | 路由 | 优先级 | 现状 | 人日 |
|---|---|---|---|---|---|
| 1.1 | 大盘概览 | `/analytics` | **P0** | 需改造 · 仅 59 行 | 8 |
| 1.2 | 每日报表 | `/analytics/daily` | P1 | 缺失 | 5 |
| 1.3 | 月度报表 | `/analytics/monthly` | P1 | 缺失 | 3 |
| 1.4 | 渠道报表 | `/analytics/channel` | P1 | 缺失 | 5 |
| 1.5 | 用户留存 | `/analytics/retention` | P1 | 缺失 | 5 |
| 1.6 | 用户流失 | `/analytics/churn` | P1 | 缺失 | 3 |
| 1.7 | 活动 ROI | `/analytics/activity-roi` | P1 | 缺失 | 5 |

## 6. 权限点汇总

| 权限码 | 名称 | 页面 |
|---|---|---|
| `analytics:overview:view` | 查看大盘 | 1.1 |
| `analytics:report:view` | 查看报表 | 1.2-1.7 |
| `analytics:export` | 导出报表 | 全部 |
