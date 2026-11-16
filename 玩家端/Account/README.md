# Account · 玩家账户、Profile 与钱包

## 1. 用途

本文以玩家仓库 `main` 为准。当前个人资料入口是顶部用户菜单中的 Profile，进入 `/profile/general-setting`；钱包由顶部钱包按钮打开弹窗。代码没有 `/account` 及其二级路由。目录名 Account 用于本需求的编号和跨页引用，不代表已交付同名页面。

玩家主分支提供英文 `en` 和繁体中文 `tc`。钱包按币种分开，可切换；第三方游戏使用 USD 钱包。业务时间窗口由服务端按平台业务时区计算，Profile 记录、提现历史及 VIP 升级奖励窗口的显示使用浏览器本地时间，不能统称为业务时区显示。

资金事实归 M5 和资金模型，活动资格与 VIP 归 M4，邀请佣金归 M7。下文区分已接入页面、后端能力及静态展示；验收场景是源码行为的检查依据，不是本轮已执行的运行测试。

## 2. 查询与处理信息

| 入口 | 当前内容 |
|---|---|
| 顶部钱包 | 当前币种的本金与彩金合计、币种选择；打开 Deposit、Withdraw、Scratch card 三个页签 |
| Deposit / Crypto | 资产、网络、充值地址及二维码、最低入金、确认数、本金打码倍数 |
| Deposit / Products | 商品档位、售价、本金、赠金估算、剩余赠送次数、后续阶梯及本金/赠金流水；最近订单 |
| Withdraw | Crypto 资产和网络、保存地址或新地址、金额、可用余额、手续费、预计到账及最近五笔申请 |
| General setting | 当前邮箱及验证状态、联系手机号、Bank Card/PayPal 收款资料 |
| My bets | All、Only wins、Lucky wins；游戏、时间、下注、派彩倍数及派彩，分页查询 |
| Transactions | All、Deposit、Withdraw；钱包币种、原币金额、账变类型、时间、关联编号及 USD 标准金额状态 |
| Preferences | 隐私、社区、营销开关的本地表单；没有保存接口 |
| Bonus / VIP Club | Bonus 内有真实 VIP 升级奖励列表；VIP Club 等级表和进度仍有静态展示 |
| Affiliate | Dashboard、My rewards、Rate rules，查询代理概览、奖励记录与规则并领取可领佣金 |

没有完整的个人统计页、统一打码任务页、统一奖励历史页、法币提现提交页或身份核验页。后端存在相关模型或查询不代表这些页面已经接入。

## 3. 处理规则

### Account-R1 · 登录、本人数据与页面恢复

AuthChecker 查询已有会话，不会在首次访问自动创建游客。登录使用邮箱和密码；注册填写用户名、显示名称、邮箱和 8 至 128 位密码，并勾选条款与年龄条件，邀请码可填写。用户名为 3 至 30 位字母、数字或下划线。Google 等图标按钮没有接入认证操作。退出调用登出并清空当前用户；服务端撤销会话时客户端使会话失效。游客接口与主分支入口边界见[游客账号](游客账号.md)。

### Account-R2 · 首页摘要

主分支没有 Account 首页、UID 缩略展示、审核中提现横幅或 History/Rewards/Invite/Support 四项快捷摘要。资料、钱包、活动和代理入口分散在导航、顶部菜单及对应页面。

### Account-R3 · 钱包与提现条件

顶部余额为所选币种的本金加彩金，包含尚未扣除的占用；它不是可提余额。Crypto 提现表单的可用余额为本金减本金占用，加彩金减彩金占用。该显示值仍须经过服务端余额、打码、限制、配置及审核校验，不保证一定受理。钱包变化通过查询和订阅更新；顶部移动端金额采用组件内按数值大小缩短的小数位规则，并非所有位置均按后台币种精度统一格式化。

### Account-R4 · 打码任务明细

没有独立打码任务列表和历史页。充值商品展示本次本金、赠金的倍数及需要完成的流水；活动页可展示所属奖励的信息。服务端继续按资金模型维护任务，不能把缺少任务页理解成没有流水限制。

### Account-R5 · 充值

Deposit 默认打开 Crypto，可切到 Products。Crypto 选择当前可用资产和网络，读取当前账号地址并提供二维码及复制。地址查询不使用缓存；全局入口关闭后，主分支钱包按钮仍在，选项或申请由后端拒绝/过滤，不承诺自动隐藏整个入口。

Products 按接口返回的商品显示币种与售价，选中后展示赠送估算、剩余次数、下一阶梯、本金和赠金打码要求。预览与订单每 5 秒查询；创建订单后保留价格和赠送快照。同一选中商品使用请求编号防重复，实际支付链接返回后由玩家打开新窗口。支付未开放时确认按钮不可用。订单结算后刷新钱包，最近订单显示本金、处理状态和实际赠送结果；具体资格与快照规则见[充值商品与赠送](../../M5-财务管理/5.5-充值商品与赠送/README.md)。

### Account-R6 · 提现与收款资料

Withdraw 已接入 Crypto 提现。选择资产、网络、地址和金额，可填入最大可用余额；显示网络手续费及扣费后的预计到账。表单阻止金额低于最低值、超过可用余额、扣费后非正数或地址为空；新地址先保存，再提交提现。提交成功刷新钱包和最近五笔记录，清空金额并更换请求编号。失败显示服务端消息；重试沿用该请求编号。记录展示状态、时间、订单号和审核原因，可手动刷新，没有玩家取消申请按钮。

General setting 中可维护 Bank Card 或 PayPal 的户名和账号。这是收款资料能力，不能据此认定法币提现通道已经接通。

### Account-R7 · 投注记录、钱包记录

My bets 分页查询本人投注，按 All/Only wins/Lucky wins 分组展示；没有主分支中的日期区间筛选、跨日分组或注单详情。Transactions 查询本人钱包账变，Deposit/Withdraw 以账变原因过滤，不是完整充值、提现订单生命周期。原币金额与最新标准换算结果并列；换算缺失或待补全时显示 USD 待计算。时间按浏览器本地时间显示。Crypto 申请历史和充值商品订单仍在各自钱包页签查看。

### Account-R8 · 个人资料与联系方式

General setting 只在已有用户时查询，结果须匹配当前用户 ID。邮箱修改通过认证服务处理；需验证时显示等待邮箱验证并可重发邮件。手机号允许可选 `+`、首位非零的 7 至 15 位数字。收款户名最多 100 字符、账号最多 255 字符。保存后重新读取本人资料再提示结果；读取失败提供重试。没有主分支自助改昵称或上传头像表单。

### Account-R9 · 登录密码与提款密码

注册和登录使用登录密码，但 Profile 当前没有修改密码、提款密码、双重验证或设备管理表单。不能把账户服务已有密码能力写成已接入的个人设置操作。

### Account-R10 · 身份核验

没有 KYC 上传、审核进度或自助账号关闭页面。

### Account-R11 · VIP中心

`/bonus` 的 UpgradeRewards 查询本人升级奖励，每 30 秒刷新。展示等级、基础奖励、免费比例和月入款门槛、领取窗口、当前可领取金额及状态；仅 available 状态允许领取，提交期间阻止重复操作，领取成功读取资金快照并刷新。周奖励、月奖励、投注返现没有主分支领取入口。

Bonus 的等级进度读取当前等级和累计投注，但累计已领 VIP 金额仍固定传入 1000。`/vip-club` 的等级表、54/100 进度及未登录时的中奖展示含静态内容，没有真实双门槛、保级、全部 VIP 权益或每日提现剩余额度概览。服务端真实业务规则见[VIP 配置](../../M4-活动管理/4.6-VIP配置/README.md)。

### Account-R12 · 奖励记录

后端已提供统一成功奖励历史接口，主分支没有 `/account/rewards` 或跨活动奖励列表。Transactions 中的账变不能替代完整的活动奖励历史筛选。类型、日期及游标契约见[奖励记录接口与页面边界](奖励记录.md)。

### Account-R13 · 邀请与佣金

`/affiliate` 提供 Dashboard、My rewards、Rate rules，使用代理接口查询本人数据和规则、领取可领佣金。注册可读取落地链接保存的邀请码和渠道，也可在注册表单填写邀请码；已建账号的绑定以服务端为准，不因打开新链接自动改绑。邀请宝箱仍是独立活动。

### Account-R14 · 客服、通知与设置

首页通知以轮播展示全体及本人通知，见[通知管理](../../M11-内容管理/11.2-通知管理/README.md)。Support 浮动条仅展开 Email、Line、Talk、Telegram 图标文字，没有聊天或外部渠道动作。Preferences 开关只在当前表单中变化，没有持久化提交，见[在线客服](../在线客服/README.md)。

### Account-R15 · 能力提供与运营配置边界

后台配置、后端接口和玩家页面独立核实。首页 CMS、统一奖励历史、完整 VIP 概览和客服聊天虽有服务端能力，当前主分支尚未消费。不能用后台可配置、静态卡片或功能分支截图证明主分支已提供操作。

### Account-R16 · 个人统计

没有 `/account/statistics` 或等效综合统计页。个人投注、账变和代理指标分别在对应页面展示，不存在原设计中的统一充值、提款、净收益和活动领取统计视图。

## 4. 特殊情况

| 情况 | 当前行为与限制 |
|---|---|
| 没有会话 | 不自动建游客；需要本人数据的服务端操作受鉴权限制，各页面的登录提示并未完全统一 |
| Crypto 选项为空或读取失败 | 显示空状态或错误及重试，不伪造地址或可提现通道 |
| 下单/提现重复提交 | 服务端按请求编号幂等；客户端成功后更新请求状态 |
| USD 换算尚未完成 | 保留原币金额并提示待计算，不按零美元展示 |
| 后端配置为 en/zh，玩家选择 tc | 不保证读取到简体中文；通知与 Metadata 可取英文，语言差异见 M11 D113 |
| 静态展示或本地开关 | 不能当作真实奖励、真实权益或保存成功 |

## 5. 验收场景

| 需求编号 | 场景与操作 | 预期结果 |
|---|---|---|
| Account-R1 | 无会话首次打开主分支 | 查询会话，不自动调用游客建号；通过邮箱注册/登录 |
| Account-R2 | 查看顶部用户菜单 | Profile 进入 General setting，不出现不存在的 Account 摘要页 |
| Account-R3 | 切换有占用的币种 | 顶部总余额与提现可用余额按各自公式显示 |
| Account-R4 | 查看充值商品确认区 | 本金、赠金倍数和流水可见；没有统一任务页 |
| Account-R5 | 商品预览、通道未开放、已结算订单 | 预览含赠送和流水，未开放不可提交，结算后刷新钱包 |
| Account-R6 | 合规 Crypto 申请及不足最低额申请 | 前者走保存地址和提交链路；后者不能提交，最终仍由服务端校验 |
| Account-R7 | 打开 My bets 和 Transactions | 本人分页数据；账变金额保留币种，USD 待计算明确展示 |
| Account-R8 | 修改邮箱、手机号、收款资料 | 使用实际接口；待验证与保存失败分别反馈 |
| Account-R9 | 查看 Profile 设置 | 不把缺少的密码/提款密码界面描述为可操作 |
| Account-R10 | 检查个人菜单 | 没有已交付的 KYC 入口 |
| Account-R11 | 升级奖励 available、expired、已领取 | 只有可领状态允许提交，成功展示实际快照；VIP 静态内容不作资格依据 |
| Account-R12 | 检查奖励记录入口 | 主分支没有统一页面，后端接口范围单独说明 |
| Account-R13 | 打开 Affiliate 三个页签 | 显示代理接口数据和规则，佣金操作遵守 M7 |
| Account-R14 | 展开 Support、修改 Preferences | 前者只展开静态项目，后者不产生保存请求 |
| Account-R15 | 后台保存首页活动配置 | 不据此声称玩家主分支首页已经变化 |
| Account-R16 | 查找个人统计 | 仅现有分散记录页，不出现综合统计页 |

## 6. 相关资料

- 入口：顶部用户菜单、钱包弹窗、Profile、Bonus、VIP Club、Affiliate。
- 身份：本人会话；后台权限码不授予玩家操作能力。
- 业务依据：[资金模型](../../M2-会员管理/2.1-会员列表/资金模型.md)、[提现订单](../../M5-财务管理/5.1-提现订单/README.md)、[Crypto 入金](../../M5-财务管理/5.14-Crypto入金/README.md)、[VIP 配置](../../M4-活动管理/4.6-VIP配置/README.md)、[代理管理](../../M7-代理管理/README.md)。

代码依据（2026-11-16）：[玩家 main · profile](https://github.com/bingo-lab-1/bingo-frontend/tree/07ca7406f3b0241b0960a6d7e7282f618ec460c3/apps/web/app/%5Blocale%5D/%28main%29/profile)；[玩家 main · wallet.tsx](https://github.com/bingo-lab-1/bingo-frontend/blob/07ca7406f3b0241b0960a6d7e7282f618ec460c3/apps/web/components/layouts/main-layout/_components/header/wallet.tsx)；[玩家 main · crypto-withdrawal.tsx](https://github.com/bingo-lab-1/bingo-frontend/blob/07ca7406f3b0241b0960a6d7e7282f618ec460c3/apps/web/components/features/crypto-withdrawal/crypto-withdrawal.tsx)；[玩家 main · recharge-products.tsx](https://github.com/bingo-lab-1/bingo-frontend/blob/07ca7406f3b0241b0960a6d7e7282f618ec460c3/apps/web/components/features/recharge/recharge-products.tsx)；[玩家 main · upgrade-rewards.tsx](https://github.com/bingo-lab-1/bingo-frontend/blob/07ca7406f3b0241b0960a6d7e7282f618ec460c3/apps/web/app/%5Blocale%5D/%28main%29/bonus/_components/vip-bonus-section/upgrade-rewards.tsx)；[玩家 main · vip-club](https://github.com/bingo-lab-1/bingo-frontend/tree/07ca7406f3b0241b0960a6d7e7282f618ec460c3/apps/web/app/%5Blocale%5D/%28main%29/vip-club)；[后端 · user](https://github.com/bingo-lab-1/bingo-backend/tree/9ec8c3000e21a8fcb68753baf548559b409d3e93/apps/web-api/src/services/user)；[后端 · finance](https://github.com/bingo-lab-1/bingo-backend/tree/9ec8c3000e21a8fcb68753baf548559b409d3e93/apps/web-api/src/services/finance)。版本与核对边界见[代码核对基线](../../00-公共约定/代码核对基线.md)。
