# 首页活动入口 · 主分支入口与 CMS 边界

## 1. 用途

当前主分支首页由通知、Live Wins、MoodBoard、Explore Bingo、Casino Games、Sports Book、Buy Crypto、投注表和介绍内容组成。活动通过固定导航及各活动页面进入。主分支没有读取后台四区首页活动配置的组件，不能将后台保存后的内容描述为已显示在首页 Hot Games 右侧。

后台和玩家 API 已支持轮播、四个固定快捷位、竖排入口及 Promotions 卡片，具体配置见[首页活动配置](../../M11-内容管理/11.4-首页活动配置/README.md)。本页区分该接口能力和现有主分支展示。

## 2. 查询条件

| 条件 | 当前行为 |
|---|---|
| 访问身份 | 首页可以打开；本人活动查询是否可用由各活动页及服务端鉴权决定 |
| 界面语言 | 主分支为 en/tc；CMS 名称为 en/zh，不是同一份语言清单 |
| 首页 CMS | 主分支没有发起轮播、快捷位、竖排活动及 Promotions 配置查询 |

## 3. 结果字段

| 内容 | 当前主分支 |
|---|---|
| 活动导航 | 固定入口包括签到、注册礼、首充补助、邀请宝箱、拼多多、幸运转盘、排行榜等；首充补助入口有自身显示判断 |
| VIP/Bonus/Affiliate | 分别进入 `/vip-club`、`/bonus`、`/affiliate` |
| CMS 图片、名称、顺序 | 后台可维护、接口可返回，但主分支首页不消费 |
| 可领奖励指示 | 不能依据后端存在指示接口宣称首页已显示跨活动可领数量 |

## 4. 操作规则

固定导航直接进入对应路由，活动开关、资格和金额由活动接口判定，不因为静态链接存在就保证活动开放。首页没有 CMS 竖排入口的关闭、恢复或排序交互，也没有 CMS 四个快捷位加 Support 的展示。

后端配置接口按各区规则返回：轮播为启用图片；活动竖排入口和 Promotions 卡片按所属运营商活动开关过滤；快捷位按自身开关，未配置时返回内置项。这些是已提供的接口契约，尚需玩家主分支接入。

## 5. 验收场景

| 需求编号 | 场景与操作 | 预期结果 |
|---|---|---|
| 首页活动入口-R1 | 查看主分支首页及导航 | 显示实际固定组件和入口，没有 CMS 竖排活动区 |
| 首页活动入口-R2 | 查找竖排活动关闭按钮 | 主分支没有该交互，不把功能分支截图当作已交付 |
| 首页活动入口-R3 | 后台清空竖排活动配置 | 接口返回空列表；主分支首页不因该配置发生对应布局变化 |
| 首页活动入口-R4 | CMS 配置接口失败 | 主分支没有依赖此查询，不存在该区的前端重试行为 |
| 首页活动入口-R5 | 从接口查询不同运营商的同一活动 | 按接口中的活动开关过滤，不能推导静态导航也被统一过滤 |
| 首页活动入口-R6 | 关闭快捷位或更新轮播 | 后台/API 结果改变，当前主分支尚未消费 |

## 6. 相关资料

- 入口：首页及固定侧边导航。
- 后台配置：[首页活动配置](../../M11-内容管理/11.4-首页活动配置/README.md)。
- 其他页面：[活动中心](../活动中心/README.md)、[游戏大厅](../游戏大厅/README.md)。
- 后续缺口：[未落地需求](../../未落地需求/README.md)。

代码依据（2026-11-16）：[玩家 main · page.tsx](https://github.com/bingo-lab-1/bingo-frontend/blob/07ca7406f3b0241b0960a6d7e7282f618ec460c3/apps/web/app/%5Blocale%5D/%28main%29/%28home%29/page.tsx)；[后端 · home-promotion.service.ts](https://github.com/bingo-lab-1/bingo-backend/blob/9ec8c3000e21a8fcb68753baf548559b409d3e93/apps/web-api/src/services/cms/home-promotion.service.ts)；[后端 · activity-reward-indicators.service.ts](https://github.com/bingo-lab-1/bingo-backend/blob/9ec8c3000e21a8fcb68753baf548559b409d3e93/apps/web-api/src/services/activity/activity-reward-indicators.service.ts)。版本与核对边界见[代码核对基线](../../00-公共约定/代码核对基线.md)。
