---
page: 4.2
name: 充值类活动
route: /game/activity/recharge
module: M4
permission: game:activity:edit
priority: P0
status: 需改造
estimate_days: 8
---

# 4.2 · 充值类活动

## 1. 用途
充值类活动的配置入口(活动引擎的分类视图)。**MVP 只做首充 + 累充两类。**

## 2. 入口
菜单:玩法中心 → 活动 → 充值类活动

## 3. 字段清单
沿用 4.1 引擎字段。本页仅做**分类过滤 + 快捷入口**。

**列表列**:`活动编码 | 名称 | 奖励类型 | 启用 | 参与人数 | 发放金额 | 更新时间 | 操作`

**MVP 范围(P0 只做 2 个)**
| 活动 | 奖励类型 | 现有实现 |
|---|---|---|
| 账号首充 | `TIER` | `FirstRechargeConfig` |
| 每日/每周累计充值 | `TIER` | `Daily/WeeklyRechargeRewardConfig` |

**迁移目标**(现有 9 张表 → 引擎)
`FirstRechargeConfig` → TIER · `Rain*Config`(3张) → MATRIX · `RechargeLotteryConfig` → TIER · `ProvidentFundPlan*` → MILESTONE · `Daily/WeeklyRechargeRewardConfig` → TIER

## 4. 需求清单

| ID | 需求 | 验收标准 | 权限码 | 人日 |
|---|---|---|---|---|
| 4.2-R1 | 分类列表视图 | 仅显示 `category=recharge` 的活动;显示参与人数与发放金额 | `game:activity:view` | 1 |
| 4.2-R2 | 账号首充(TIER) | 按档位表发放;同一用户仅首次充值触发一次 | `game:activity:edit` | 2 |
| 4.2-R3 | 每日/每周累计充值(TIER) | 按周期累计额匹配档位;跨周期正确重置 | `game:activity:edit` | 2 |
| 4.2-R4 | 充值事件接入 | 接收 M3 充值到账事件,判定资格,幂等(同一订单不重复发) | — | 2 |
| 4.2-R5 | 发放链路 | 发彩金调 M3 写 `Transaction` → 挂 `WagerRequirement` → 写 `ActivityClaim` | — | 1 |

## 5. 状态清单
空 / 加载 / 错误 / 无权限 / 迁移中(双写期提示)

## 6. 交互流程
充值到账(M3.1)→ 发出充值事件 → 本模块判定资格 → 发彩金(调 M3)→ 挂打码(M3.7)→ 写 `ActivityClaim`

## 7. 涉及表
`Activity` `ActivityClaim`(owner)· 只读 `RechargeOrder`(M3) → `../表设计.prisma`

## 8. 关联页面
跳出:活动引擎(4.1)· 领取记录(4.3)· 充值订单(M3.1)· 打码核销(M3.7)
