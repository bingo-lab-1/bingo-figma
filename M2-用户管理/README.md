---
module: M2
name: 用户管理
owner: 待定
status: 设计中
pages: 9
p0: 5
estimate_days: 15.5
updated: 2026-07-26
---

# M2 · 用户管理

## 1. 定位与边界

**做什么**:玩家账号的查询、干预、分层。**`User` 的唯一写入方。**

**不做什么**
- 不做资金操作(充值/提现/上下分归 M3,本模块只读展示)
- 不做后台账号管理(那是 M7 的 `Account`)
- 不做风控规则引擎(只提供档案数据,规则判定另议)

**铁律**:封禁/解封/调级/打标等干预操作**必须**留痕(`M7 OperationLog`)。

## 2. 术语表

| 术语 | 定义 | 代码标识 |
|---|---|---|
| 玩家 | C 端用户 | `User` |
| 后台账号 | 运营人员账号,**不是玩家** | `Account`(M7) |
| 标签 | 运营圈人分类,**非风控结论** | `UserTag` |
| 实名 | KYC 认证 | `UserKyc` |
| 封禁 | 限制登录/出入金/投注 | `UserBanRecord` |
| 点控 | 赢率干预 | `PointControlRecord` |

## 3. 依赖关系

**上游依赖(我引用)**
- `M5-代理渠道`:`Channel`(注册渠道)、`Agent`(上级代理)
- `M3-财务管理`:`Wallet` `Transaction`(**只读**展示余额与账变)
- `00-公共约定`:`PlatformType`

**下游被依赖(谁引用我)** ← 改表前先看这行
- `M3-财务管理`:`User`(订单归属)、`UserTag`(提现风控)
- `M4-玩法中心`:`User` `UserTag` `VipLevel`(活动资格圈人)
- `M5-代理渠道`:`User`(代理下级、佣金归属)
- `M6-运营管理`:`UserTag`(弹窗/推送定向)
- `M1-数据中心`:`User` `LoginRecord`(拉新/留存)

> **`User` 和 `UserTag` 是全仓被引用最多的表**,改结构影响面最大。

## 4. 数据模型

**拥有的表**

| 表 | 说明 | 现状 |
|---|---|---|
| `User` | 玩家主表 | 已有 |
| `UserKyc` | 实名认证 | 已有 |
| `Tag` / `UserTag` | 标签与打标 | 已有 |
| `Level` / `VipLevel` | 等级/VIP | 需改造 · 双轨待定 |
| `LoginRecord` | 登录记录 | 已有 |
| `RegisterIpRecord` / `RegisterDeviceRecord` | 注册 IP/设备 | 已有 |
| `UserIdentity*`(3 张) | 身份体系 | 需改造 · 与 KYC/Tag 重叠 |
| `WithdrawalAccount` / `UserFiatAccount` / `UserCryptoAccount` | 收款账户 | 已有 |
| `UserFundSecurity` / `UserFundsSummary` | 资金安全/汇总 | 已有 |
| `UserBanRecord` | 封禁记录 | 新增 |
| `PointControlRecord` | 点控记录 | 新增 |

**只读引用**:`Wallet` `Transaction` `BetRecords`(owner 见 M3/M4)
详见 `表设计.prisma`

## 5. 菜单结构与页面索引

```
用户管理
├─ 用户列表            → 2.1
├─ 钱包账变            → 2.2
├─ 投注明细            → 2.3
├─ 封禁管理            → 2.4
├─ 用户标签            → 2.5
├─ VIP 管理            → 2.6
└─ 风控  (分组)
    ├─ 风控档案        → 2.7
    └─ 点控记录        → 2.8
```

| 编号 | 页面 | 路由 | 优先级 | 现状 | 人日 |
|---|---|---|---|---|---|
| 2.1 | 用户列表与详情 | `/user/list` | **P0** | 已有 | 3 |
| 2.2 | 钱包账变 | `/user/wallet` | **P0** | 需改造 · 缺彩金/冻结 | 3 |
| 2.3 | 投注明细 | `/user/bet-record` | **P0** | 已有 | 2 |
| 2.4 | 封禁管理 | `/user/ban` | **P0** | 缺失 | 5 |
| 2.5 | 用户标签 | `/user/tag` | **P0** | 已有 | 2.5 |
| 2.6 | VIP 管理 | `/user/vip` | P1 | 需改造 · 双轨待定 | 5 |
| 2.7 | 风控档案 | `/user/risk` | P1 | 需改造 · 有表无分析 | 5 |
| 2.8 | 点控记录 | `/user/point-control` | P2 | 缺失 | 3 |
| 2.9 | 玩家排行榜 | `/user/rank` | P2 | 缺失 | 3 |

## 6. 权限点汇总

| 权限码 | 名称 | 页面 |
|---|---|---|
| `user:list:view` | 查看用户列表 | 2.1 |
| `user:detail:view` | 查看用户详情 | 2.1 |
| `user:export` | 导出用户数据 | 2.1 |
| `user:wallet:view` | 查看余额与账变 | 2.2 |
| `user:bet:view` | 查看投注明细 | 2.3 |
| `user:ban` | 封禁/解封 | 2.4 |
| `user:tag:edit` | 打标/移除标签 | 2.5 |
| `user:vip:adjust` | 手动调级 | 2.6 |
