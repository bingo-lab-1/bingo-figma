# 活动中心 · Promotions页面

## 1. 用途

底部导航Promotions和Account的Rewards进入本页，玩家在这里进入常用活动、打开充值弹窗并领取VIP升级奖励。本页不是全部活动的目录，各活动的资格、奖励和领取规则由[M4 活动管理](../../M4-活动管理/README.md)维护。

本页不需要登录即可打开。VIP升级奖励、充值和活动操作需要登录会话，自动建号的游客有登录会话。金额币种以活动配置为准，界面支持英文和繁体中文。

本版不提供个人奖励聚合列表、可领数量、跨活动一键领取和打码任务列表。

## 2. 查询条件

本页没有筛选条件。VIP升级奖励固定查询当前玩家本人的记录，页面打开期间每30秒刷新。

| 条件 | 含义和填写规则 |
|---|---|
| 登录状态 | 没有登录会话时不显示VIP升级奖励区域 |

## 3. 结果字段

| 字段 | 含义 |
|---|---|
| 活动入口 | 排行榜、七日签到、每日签到三个链接，进入对应活动页 |
| Bonus区域 | 累计奖金、存款奖励进度、结束时间等为固定展示内容，不代表玩家实际数据；Details按钮没有操作 |
| Deposit Now | 打开充值弹窗，包含Crypto deposit和Recharge offers两个页签 |
| Bonus T&C | 打开存款奖励规则说明，内容为固定展示，不随活动配置变化 |
| VIP升级奖励 | 按奖励生成时间倒序，按等级列出奖励基础金额、全额领取条件、领取时间段、当前可领金额和状态；当前可领金额只在可领取状态显示 |
| VIP等级区域 | 显示当前等级和累计投注相对下一等级投注门槛的进度，累计投注超过门槛时按门槛显示；没有下一等级或查询不到等级时进度显示0/0；累计领取金额及周、月返现卡片为固定展示内容，View Level Up Details和Available at按钮没有操作 |
| Lucky spin | 进入幸运转盘 |
| Daily Bonus | 卡片按钮显示Claim，点击打开每日奖励说明弹窗，弹窗内容为示例，不代表玩家签到记录，也不能领取；信息图标打开规则说明；Reach VIP 10为固定展示内容 |

VIP升级奖励状态：

| 状态 | 按钮显示 |
|---|---|
| 可领取 | Claim |
| 已领取 | Claimed |
| 已过期 | Expired |
| 已暂停 | Paused |
| 未开放 | Not open yet |
| 计算金额为0 | No amount available · deposit requirement not met or reward is zero |
| 账号受限 | Account restricted |
| 缺少参与标签 | Participation tags required |
| 奖励币种不可用 | Reward currency unavailable |
| 奖励钱包不可用 | Reward wallet unavailable |
| 无法判断资格 | Eligibility unavailable · please retry |

## 4. 操作规则

**领取VIP升级奖励。** 只有状态为可领取的奖励可以点击，列表加载中或加载失败时也不可点。领取时同一时间只处理一笔，成功后提示到账金额并刷新列表；刷新失败时提示奖励已到账、请刷新查看。领取失败时显示服务端原因并刷新列表。充值未达到全额门槛时按当前可领金额发放，之后不补差。升级、领取和金额规则见[VIP配置](../../M4-活动管理/4.6-VIP配置/README.md)。

**充值。** Deposit Now打开的弹窗规则见[Account](../Account/README.md)和[Crypto入金](../../M5-财务管理/5.14-Crypto入金/README.md)。

列表加载失败时提示Could not load rewards并提供重试；没有记录时提示No upgrade rewards yet。

## 5. 验收场景

| 需求编号 | 场景与操作 | 预期结果 |
|---|---|---|
| 活动中心-R1 | 从底部Promotions或Account的Rewards进入 | 打开本页，显示活动入口、Bonus、VIP Bonus和General Bonus区域 |
| 活动中心-R2 | 没有登录会话打开本页 | 页面可查看，不显示VIP升级奖励区域 |
| 活动中心-R3 | 有一笔可领取的VIP升级奖励，点击领取 | 只到账一次，提示金额，列表更新为已领取 |
| 活动中心-R4 | 连续点击领取，或领取失败 | 只提交一次；失败时显示原因并刷新状态 |
| 活动中心-R5 | 奖励未开放、已过期或账号受限 | 按钮不可点，显示对应状态 |
| 活动中心-R6 | 点击Deposit Now | 打开充值弹窗，默认Crypto deposit页签 |
| 活动中心-R7 | 查看Bonus区域的累计奖金和Daily Bonus弹窗 | 内容与玩家实际账户无关，不提供领取 |

## 6. 相关资料

- 入口：底部导航Promotions、Account快捷入口Rewards、邀请页Rewards页签、侧边栏。
- 权限：页面公开；领取和充值使用本人登录会话，不使用后台权限码。
- 数据归属：VIP奖励归[VIP配置](../../M4-活动管理/4.6-VIP配置/README.md)，活动规则归M4，入账结果归M5。
- Jira：见活动中心对应任务。
