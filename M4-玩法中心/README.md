---
模块: M4
名称: 玩法中心
负责人: 待定
状态: 设计中
更新: 2026-07-27
---

# M4 · 玩法中心

## 1. 定位与边界

**做什么**:游戏内容编排 + 活动配置。**运营日常使用频率最高的模块。**

**不做什么**
- 不直接改余额 —— 发钱调 M3 的账变接口
- 不管展示位素材 —— Banner/弹窗归 M6,本模块只引用展示位 ID
- 不做活动 ROI 报表(归 M1,本模块只产生 `ActivityClaim` 原始数据)

**铁律**:活动配置的写操作必须留痕。发钱走 M3 接口,**M3 不得反向依赖本模块**。

## 2. 术语表

| 术语 | 定义 | 代码标识 |
|---|---|---|
| 活动 | 一次可配置的奖励规则 | `Activity` |
| 活动编码 | 活动的业务唯一标识 | `Activity.code` |
| 领取记录 | 用户从活动获得奖励的流水 | `ActivityClaim` |
| 资格圈人 | 谁能参与(渠道/标签/VIP) | `eligibility` |
| 奖励结构 | 档位/矩阵/日历/里程碑四态 | `rewardKind` |
| 厂商 | 第三方游戏提供商 | `GamePlatform` |
| 公平性 | provably fair 种子验证 | `Fairness` |

## 3. 依赖关系

**上游依赖(我引用)**
- `M2-用户管理`:`User` `UserTag` `VipLevel`(资格圈人)
- `M5-代理渠道`:`Channel` `Agent`(按渠道/代理差异化)
- `M3-财务管理`:发彩金写 `Transaction`、挂 `WagerRequirement`

**下游被依赖(谁引用我)**
- `M3-财务管理`:`WagerRequirement.sourceId` 以**元数据 ID** 引用活动(非外键)
- `M1-数据中心`:`ActivityClaim` `BetRecords`
- `M6-运营管理`:Banner/弹窗引用 `Activity.id`

## 4. 数据模型

**拥有的表**

| 表 | 说明 | 现状 |
|---|---|---|
| `Activity` | 活动主表 | 需改造 · **待重构为配置化引擎** |
| `ActivityClaim` | 统一领取记录 | 新增 |
| ~~9 张 `*Config` 表~~ | 一活动一表 | 大缺口 · **待合并进引擎** |
| `GamePlatform` / `GameType` / `SubGame` | 游戏与厂商 | 已有 |
| `GameHot` | 热门位 | 已有 |
| `Fairness` / `FairnessHistory` | 公平性 | 已有 |
| `BetRecords` | 投注记录 | 已有 |
| `LobbyLayout` | 大厅布局 | 新增 |

详见 `表设计.prisma`

### 核心问题:活动是「改造」不是「新建」
现有 9 个 resolver = **每加一个活动就加一张表 + 一次发版**。竞品沿此路已到 159 个 action_type。
**目标**:新增活动仅靠配置,不改 schema、不发版。
**验收**:用引擎表达 10 个活动(现有 6 个 `ActivityCode` + 竞品实测 4 个),全部能表达才通过。

## 5. 菜单结构与页面索引

```
玩法中心
├─ 活动  (分组)
│   ├─ 活动引擎配置    → 4.1
│   ├─ 充值类活动      → 4.2
│   ├─ 留存类活动      → 4.5
│   ├─ 打码类活动      → 4.6
│   └─ 活动领取记录    → 4.3
├─ 游戏  (分组)
│   ├─ 游戏列表        → 4.4
│   ├─ 大厅编排        → 4.7
│   └─ 公平性查询      → 4.8
└─ VIP 配置            → 4.9
```

| 编号 | 页面 | 路由 | 优先级 | 现状 | 人日 |
|---|---|---|---|---|---|
| 4.1 | 活动引擎配置 | `/game/activity/engine` | **P0** | 重构 | 15 |
| 4.2 | 充值类活动 | `/game/activity/recharge` | **P0** | 需改造 · 9 个硬编码 | 8 |
| 4.3 | 活动领取记录 | `/game/activity/claim` | **P0** | 缺失 | 4 |
| 4.4 | 游戏列表与品牌 | `/game/list` | **P0** | 已有 | 2 |
| 4.5 | 留存类活动 | `/game/activity/retention` | P1 | 缺失 | 8 |
| 4.6 | 打码类活动 | `/game/activity/wagering` | P1 | 需改造 | 5 |
| 4.7 | 大厅编排 | `/game/lobby` | P1 | 需改造 · 仅 `GameHot` | 5 |
| 4.8 | 公平性查询 | `/game/fairness` | P1 | 已有 | 2 |
| 4.9 | VIP 配置 | `/game/vip` | P1 | 大缺口 · 双轨待定 | 8 |
| 4.10 | 任务系统 | `/game/task` | P2 | 缺失 | 10 |
| 4.11 | 道具卡配置 | `/game/item-card` | P2 | 缺失 | 5 |

## 6. 权限点汇总

| 权限码 | 名称 | 页面 | 二次确认 |
|---|---|---|---|
| `game:activity:view` | 查看活动配置 | 4.1-4.2 | — |
| `game:activity:edit` | **编辑活动配置** | 4.1-4.2 | 是 |
| `game:activity:toggle` | **启用/停用活动** | 4.1-4.2 | 已有 |
| `game:claim:view` | 查看领取记录 | 4.3 | — |
| `game:list:view` | 查看游戏列表 | 4.4 | — |
| `game:list:edit` | 编辑游戏/品牌 | 4.4 | — |
| `game:vip:edit` | 编辑 VIP 配置 | 4.9 | 已有 |
