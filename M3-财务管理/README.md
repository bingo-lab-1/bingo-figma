---
模块: M3
名称: 财务管理
负责人: 待定
状态: 设计中
更新: 2026-07-27
---

# M3 · 财务管理

## 1. 定位与边界

**做什么**:钱的进出与审核。`Wallet` / `Transaction` / 各类订单的唯一写入方。

**不做什么**
- 不判断"这笔钱因为哪个活动而发" —— 活动逻辑在 M4,本模块只认一笔账变
- 不做报表聚合(归 M1)
- 不做代理佣金计算(归 M5,M5 算完调本模块入账)

**铁律**
1. 任何写操作**必须**留痕(`M7 OperationLog`)
2. **不得反向依赖 M4 活动** —— 活动信息以**元数据 ID** 传入,不建外键

## 2. 术语表

| 术语 | 定义 | 代码标识 |
|---|---|---|
| 真金 | 充值进来的余额,**打码满 1 倍后可提现** | `balance` |
| 彩金 | 活动赠送,需打码达标才能转真金 | `bonusBalance` |
| 冻结 | 被锁定不可用的余额 | `frozenBalance` |
| 打码 / 流水 | 投注累计额,**真金与彩金都要打码才能提** | `wager` |
| 打码倍数 | 本金 × 倍数 = 需完成流水。充值真金固定 1 倍,彩金随活动配置 | `multiplier` |
| 首充 | 用户第一笔成功充值 | `isFirst` |
| 账变 | 任何余额变动的流水记录 | `Transaction` |

## 3. 依赖关系

**上游依赖(我引用)**
- `M2-用户管理`:`User`(订单归属)、`UserTag`(提现风控)
- `M5-代理渠道`:`Channel`(渠道归因)
- `M8-系统设置`:`CryptoCoins` `CodingMultiple`
- `00-公共约定`:`ReviewStatus` `CurrencyKind`

**下游被依赖(谁引用我)** ← 改表前先看这行
- `M1-数据中心`:`Transaction` 及订单表(充提报表)
- `M2-用户管理`:`Wallet` `Transaction`(用户详情展示)
- `M4-玩法中心`:发彩金 → 写 `Transaction`、挂 `WagerRequirement`
- `M5-代理渠道`:佣金结算 → 写 `Transaction`

## 4. 数据模型

**拥有的表**

| 表 | 说明 | 现状 |
|---|---|---|
| `Wallet` | 四分账余额 | 需改造 · 需加 `frozenBalance` |
| `Transaction` | 账变总账 | 已有 |
| `RechargeOrder` | 充值订单 | 新增 |
| `WithdrawOrder` | 提现订单 | 新增 |
| `WithdrawReviewRule` | 审核规则 | 新增 |
| `WithdrawConfig` | 提现全局配置 | 新增 |
| `ManualAdjustment` | 人工上下分 | 新增 |
| `WagerRequirement`  | 打码进度 | 新增 |
| `FreezeRecord`  | 冻结/解冻流水 | 新增 |
| `RechargeProduct` | 充值商品 SKU | 新增 |
| `PaymentChannel` | 支付/提现通道 | 需改造 · 仅加密 |

**只读引用**:`User` `UserTag`(M2)· `Channel`(M5)· `CodingMultiple`(M8)
详见 `表设计.prisma`

### 两个必补字段(全库 grep 命中 0)
| 缺口 | 后果 |
|---|---|
| `Wallet.frozenBalance` | 提现拒绝后冻不住钱,多路径解冻无处落地 |
| `WagerRequirement` | 有倍数配置但无进度追踪 → **充值与彩金都能不打码直接提走** |

## 5. 菜单结构与页面索引

```
财务管理
├─ 充值  (分组)
│   ├─ 充值订单        → 3.1
│   ├─ 人工充值        → 3.5
│   └─ 充值商品配置    → 3.8
├─ 提现  (分组)
│   ├─ 提现订单        → 3.2
│   ├─ 审核规则        → 3.3
│   └─ 提现配置        → 3.4
├─ 冻结解冻            → 3.6
├─ 打码核销            → 3.7
├─ 通道管理            → 3.9
└─ 对账                → 3.10
```

| 编号 | 页面 | 路由 | 优先级 | 现状 | 人日 |
|---|---|---|---|---|---|
| 3.1 | 充值订单 | `/finance/recharge/order` | **P0** | 缺失 | 5 |
| 3.2 | 提现订单与审核 | `/finance/withdraw/order` | **P0** | 缺失 | 8 |
| 3.3 | 审核规则 | `/finance/withdraw/rule` | **P0** | 缺失 | 8 |
| 3.4 | 提现配置 | `/finance/withdraw/config` | **P0** | 缺失 | 3 |
| 3.5 | 人工充值/扣款 | `/finance/manual-adjust` | **P0** | 缺失 | 4 |
| 3.6 | 冻结与解冻  | `/finance/freeze` | **P0** | 缺失 | 6 |
| 3.7 | 打码核销  | `/finance/wagering` | **P0** | 缺失 | 8 |
| 3.8 | 充值商品配置 | `/finance/recharge/product` | P1 | 缺失 | 5 |
| 3.9 | 通道管理 | `/finance/channel` | P1 | 需改造 · 仅加密 | 5 |
| 3.10 | 对账 | `/finance/reconciliation` | P2 | 缺失 | 10 |

## 6. 权限点汇总

| 权限码 | 名称 | 页面 | 二次确认 |
|---|---|---|---|
| `finance:recharge:view` | 查看充值订单 | 3.1 | — |
| `finance:withdraw:view` | 查看提现订单 | 3.2 | — |
| `finance:withdraw:review` | **审核提现** | 3.2 | 是 |
| `finance:withdraw:batch-review` | **批量审核** | 3.2 | 是 |
| `finance:rule:edit` | 编辑审核规则 | 3.3 | 是 |
| `finance:config:edit` | 编辑提现配置 | 3.4 | 是 |
| `finance:manual:adjust` | **人工上下分** | 3.5 | 是 |
| `finance:freeze:manage` | 冻结/解冻 | 3.6 | 是 |
| `finance:wager:clear` | **清空打码** | 3.7 | 是 |
| `finance:export` | 导出财务数据 | 全部 | — |
