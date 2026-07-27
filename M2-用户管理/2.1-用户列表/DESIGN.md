# M2.1 用户列表与详情 · 设计交接

## Figma

工作稿：
[BINGO SAAS · Design System & 用户管理预览](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB)

界面节点：

- [用户列表 / Default](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=16-2)
- [用户列表 / Detail Drawer](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=22-145)
- [用户列表 / Async Export](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=36-292)
- [M2.1 / State Reference](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=37-433)

原始目标文件 `EAPQVmg3WkxGORMcdnGozN` 对当前 Figma MCP 身份为只读。本轮先在同团队工作稿完成设计，获得设计编辑权限后再迁回。

## M2.1 同步范围

- 1440 × 1024 桌面运营后台。
- 深色可折叠侧栏、64px 顶栏、面包屑和巴西运营时区 `GMT−3 · America/Sao_Paulo`。
- 用户概览：今日新增、在线用户、异常用户、累计用户。
- 19 项筛选能力：首屏展示 10 项核心条件，其余 9 项通过“展开更多筛选”进入高级筛选；默认查询最近 90 天。
- 用户信息模糊查询最少输入 2 个字符；筛选字段已同步为提现绑定手机、注册设备、注册 / 登录平台、充值金额 min / max 等新命名。
- 表格定义 14 列，默认显示 12 列；邀请人、彩金可通过列设置开启，列设置按账号持久化。
- 表格默认按注册时间倒序，支持点击行进入详情；示例数据保留测试账号与已冻结账号标记。
- 520px 用户详情抽屉，包含基本信息、钱包与账变、投注记录、活动领取、代理关系、风控档案、操作记录 7 个业务 Tab。
- 抽屉首屏展示基础信息、钱包概览、风险快照和操作入口。
- 异步导出状态覆盖任务创建、生成进度、站内消息通知、默认剔除测试账号和 24 小时下载有效期。
- 状态参考覆盖加载、空数据、错误、无权限；测试、封禁和导出中状态分别在列表与独立画板中展示。

## 复用结构

| 组件 | Figma Node | 用途 |
|---|---:|---|
| Status Badge | `9:24` | 正常、在线、测试、冻结和风险状态 |
| Button | `11:8` | Primary、Secondary、Quiet 操作 |
| Field | `12:7` | Input / Select 筛选字段 |
| Nav Item | `13:8` | 深色侧栏默认 / 选中状态 |
| Stat Card | `14:5` | 概览统计卡 |
| User Table Row | `15:5` | 用户表格行，11 个可覆盖字段 |

页面由组件实例组装，不复制局部组件。颜色、尺寸、字体和阴影均来自 `design-tokens/` 与 Figma Variables。

## 验收结果

- 默认态：38 个组件实例，154 个文本层。
- 抽屉态：42 个组件实例，193 个文本层。
- 异步导出态：38 个组件实例，159 个文本层。
- 状态参考：4 张状态卡、18 个文本层。
- 四张画板合计 118 个组件实例、524 个文本层，无缺失字体。
- 新增异步导出画板包含 873 处变量绑定；状态参考画板包含 144 处变量绑定。
- 默认态主内容最底部为 y=890，未超出内容区域。
- 抽屉宽度绑定 `layout/drawer/width`，遮罩透明度为 32%。
