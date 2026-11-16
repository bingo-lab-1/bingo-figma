# 活动中心 · Bonus 页面

## 1. 用途

当前玩家主分支活动汇总页是 `/bonus`，包含固定活动入口、Bonus 内容、VIP 升级奖励和 General bonus。主分支没有 `/promotions` 路由，也没有按后台 Promotions 卡片配置生成的活动中心。

玩家可进入独立活动页参与；本文不把宣传组件中的固定数字、倒计时或按钮外观当作已接入奖励。

## 2. 查询条件

无活动卡片筛选。页面查询 VIP 等级列表；有登录用户时读取本人 VIP 等级及升级奖励。UpgradeRewards 使用本人接口每 30 秒刷新，匿名访问时不展示该领奖区。

## 3. 结果字段

| 区域 | 实际来源和边界 |
|---|---|
| 顶部活动链接 | 排行榜、常规七日签到、每日签到的固定链接 |
| Bonus/General bonus | 前端固定内容及已有组件，不读取 CMS Promotions 列表 |
| VIP 进度 | 查询等级及本人累计投注，按下一等级投注门槛展示；不是充值与有效投注双进度 |
| 已领 VIP 金额 | 页面当前传入固定值 1000，不是已领金额统计接口 |
| UpgradeRewards | 本人真实升级奖励，等级、基础额、门槛、窗口、当前可领金额与状态 |

## 4. 操作规则

升级奖励仅在 available 状态可领。请求、查询异常或刚确认领取时禁用对应操作；成功后使用服务端返回的奖励快照提示并刷新。领取窗口使用浏览器本地时间显示。服务端仍执行当前资格校验，展示可领不代表后续请求一定成功。

周奖励、月奖励和投注返现尚无主分支领取入口。VIP Club 还有静态等级表和进度，不是完整本人权益中心。后端 CMS 卡片、奖励历史与完整 VIP 概览已有能力，但当前 Bonus 不消费；没有跨活动一键领取。

## 5. 验收场景

| 需求编号 | 场景与操作 | 预期结果 |
|---|---|---|
| 活动中心-R1 | 从导航 Bonus 进入 | 打开 `/bonus` 的固定内容、活动链接和升级奖励区 |
| 活动中心-R2 | 无会话打开页面 | 可以浏览公共内容，不查询本人升级奖励 |
| 活动中心-R3 | 可领升级奖励并点击领取 | 调用真实领取接口，展示返回快照并刷新 |
| 活动中心-R4 | 升级奖励查询失败 | 该区显示错误和重试，不能提交领取 |
| 活动中心-R5 | 奖励已领、过期或资格受限 | 对应状态不可领取 |
| 活动中心-R6 | 点击顶部三个活动入口 | 进入对应独立活动页，按各自规则参与 |
| 活动中心-R7 | 后台更新 Promotions 卡片 | 当前主分支 Bonus 不读取该配置；固定已领金额不当作真实汇总 |

## 6. 相关资料

- 入口：导航 Bonus，路径 `/bonus`。
- 规则：[VIP 配置](../../M4-活动管理/4.6-VIP配置/README.md)、[活动管理](../../M4-活动管理/README.md)。
- 边界：[Account-R11](../Account/README.md#account-r11--vip中心)、[首页活动入口](../首页活动入口/README.md)。

代码依据（2026-11-16）：[玩家 main · page.tsx](https://github.com/bingo-lab-1/bingo-frontend/blob/07ca7406f3b0241b0960a6d7e7282f618ec460c3/apps/web/app/%5Blocale%5D/%28main%29/bonus/page.tsx)；[玩家 main · upgrade-rewards.tsx](https://github.com/bingo-lab-1/bingo-frontend/blob/07ca7406f3b0241b0960a6d7e7282f618ec460c3/apps/web/app/%5Blocale%5D/%28main%29/bonus/_components/vip-bonus-section/upgrade-rewards.tsx)；[后端 · promotion-campaign.service.ts](https://github.com/bingo-lab-1/bingo-backend/blob/9ec8c3000e21a8fcb68753baf548559b409d3e93/apps/web-api/src/services/cms/promotion-campaign.service.ts)。版本与核对边界见[代码核对基线](../../00-公共约定/代码核对基线.md)。
