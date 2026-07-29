# M2.1 用户列表与详情 · 设计交接

## Figma

工作稿：[BINGO-SAAS](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB)，基线 Ant Design 6.5.2。

本页界面位于 [03 · M2.1 用户列表](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=2-8)（`2:8`）。Figma 页面与需求页面目录一一对应，M2.2 起依次占用 `04`、`05` …

| 界面 | Node | 尺寸 |
|---|---|---|
| [2.1 · 用户列表 / AntD 6.5.2](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=129-433) | `129:433` | 1440 × 1024 |
| [2.1 · 用户详情 / Modal](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=136-2) | `136:2` | 1440 × 1024 |

原始目标文件 `EAPQVmg3WkxGORMcdnGozN` 对当前 Figma MCP 身份为只读。本轮先在同团队工作稿完成设计，获得设计编辑权限后再迁回。

## 用户列表界面结构

| 区块 | Node | 内容 |
|---|---|---|
| [Page Header](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=129-512) | `129:512` | 面包屑、页标题、时区标注 |
| [Summary Statistics](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=129-513) | `129:513` | 4 张统计卡：今日新增、在线用户、异常用户、累计用户，各带环比 |
| [Filter Panel](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=129-514) | `129:514` | 首屏 10 项基础筛选 + 展开更多筛选（9 项）+ 重置 / 查询 |
| [Table Panel](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=129-515) | `129:515` | 工具条、表头、6 行示例数据、分页页脚 |

外壳由 `BINGO/AppShell` 实例提供：232px 深色侧栏 + 64px 顶栏 + 1208 × 960 内容槽。

首屏 10 项筛选：渠道、用户信息、在线状态、提现绑定手机、VIP 等级、时间、注册 IP、注册平台、充值金额（min–max，币种 R$）、是否充值。工具条标注“基础筛选 10 项 · 更多筛选 9 项”，与 README 的 19 项筛选能力一致。

表格默认显示 12 列（另有选择列）：序号、用户 ID、用户、渠道、VIP、真金余额、累计充值、累计提现、标签、状态、注册时间、操作。工具条“列设置 12/14”对应 README 定义的 14 列，邀请人与彩金默认关闭。默认按注册时间降序，分页 20 条/页。

## 用户详情界面结构

| 区块 | Node | 内容 |
|---|---|---|
| [Modal Mask](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=136-146) | `136:146` | 遮罩，覆盖 1440 × 1024 |
| [AntD/Modal.Shell XL](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=136-147) | `136:147` | 弹窗骨架 1200 × 896，Header 72 / Body 768 / Footer 56 |
| [UserIdentity.Summary](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=137-1144) | `137:1144` | 身份摘要条，1152 × 116 |
| [Detail Tabs](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=137-2743) | `137:2743` | 10 个业务 Tab |
| [Modal Scroll Body](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=138-1136) | `138:1136` | 当前 Tab 内容区，1152 × 604，独立滚动 |

10 个 Tab 依次为：用户详情、账户详情、风控数据、订单数据、提款记录、充值记录、资产变动、投注记录、资产走势、状态监控。逐 Tab 字段规格见同目录 `用户详情弹窗.md`。

详情为**弹窗（Modal）不是抽屉**。早期版本曾按右侧抽屉出图，已废弃，文档与实现均以弹窗为准。

## 复用结构

界面由 `02 · AntD Components`（`2:5`）的组件实例组装，不复制局部组件。本页用到的组件：

| 组件 | Node | 变体 | 用途 |
|---|---|---:|---|
| `BINGO/AppShell` | `118:437` | — | 侧栏 + 顶栏 + 内容槽外壳 |
| `BINGO/UserTable.Row` | `119:942` | 6 | 用户表格行 |
| `BINGO/UserIdentity.Summary` | `120:745` | — | 详情弹窗身份摘要条 |
| `AntD/Button/Core` | `102:519` | 30 | Primary / Default × 三尺寸 × 五状态 |
| `AntD/Button/Quiet` | `104:620` | 18 | Text / Link / Danger |
| `AntD/Input/Core` | `105:746` | 15 | 文本筛选字段 |
| `AntD/Input/Status` | `105:747` | 12 | Error / Warning 态 |
| `AntD/InputNumber` | `105:868` | 15 | 充值金额 min / max |
| `AntD/Select` | `105:1039` | 24 | 单选 / 多选筛选 |
| `AntD/DatePicker.Range` | `106:232` | 12 | 时间范围 |
| `AntD/Checkbox` | `106:710` | 12 | 行选择、列设置 |
| `AntD/Form.Item` | `108:855` | 6 | 筛选字段标签与校验位 |
| `AntD/Tag` | `108:963` | 12 | 用户标签 |
| `AntD/Badge.Status` | `108:982` | 6 | 在线 / 正常 / 测试 / 冻结 |
| `AntD/Avatar` | `108:1031` | 6 | 用户头像 |
| `AntD/Menu.Item` | `110:723` | 8 | 侧栏导航项 |
| `AntD/Tabs.Item` | `111:306` | 16 | 详情弹窗 Tab |
| `AntD/Table.HeaderCell` | `112:771` | 6 | 表头单元格 |
| `AntD/Table.Cell` | `112:865` | 18 | 表格单元格 |
| `AntD/Pagination.Item` | `112:930` | 16 | 分页 |
| `AntD/Statistic.Card` | `113:302` | 4 | 概览统计卡 |
| `AntD/Descriptions.Item` | `114:767` | 4 | 详情字段行 |
| `AntD/Modal.Shell` | `115:933` | 9 | 弹窗骨架 |
| `AntD/Alert` | `116:886` | 8 | 错误与无权限提示 |
| `AntD/Empty` | `117:462` | 4 | 空数据 |
| `AntD/Skeleton.Table` | `117:1064` | 6 | 加载态 |

颜色、尺寸、字体和阴影一律来自 Figma Variables（`AntD Alias` / `AntD Component` 两层）与 `AntD/Typography/*` 文字样式，界面内不写死数值。

## 状态覆盖

加载、空数据、错误、无权限四类状态以组件变体形式提供（`Skeleton.Table`、`Empty`、`Alert`），**不再有独立的状态参考画板**。测试账号、冻结账号在列表示例数据中体现。

异步导出目前只在工具条留有入口，尚无独立画板，规格见 README 的异步导出段落。

## 验收结果

盘点于 2026-07-29。

| 界面 | 组件实例 | 文本层 |
|---|---:|---:|
| 用户列表 | 188 | 219 |
| 用户详情弹窗 | 243 | 304 |
| 合计 | 431 | 523 |

无缺失字体。页面级数据同步记录在 `design-tokens/.figma-build-state.json`。
