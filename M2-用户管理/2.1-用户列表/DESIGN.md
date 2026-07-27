# M2.1 用户列表 · 设计交接

## Figma

工作稿：
[BINGO SAAS · Design System & 用户管理预览](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB)

界面节点：

- [用户列表 / Default](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=16-2)
- [用户列表 / Detail Drawer](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=22-145)

原始目标文件 `EAPQVmg3WkxGORMcdnGozN` 对当前 Figma MCP 身份为只读。本轮先在同团队工作稿完成设计，获得设计编辑权限后再迁回。

## 首版范围

- 1440 × 1024 桌面运营后台。
- 深色可折叠侧栏、64px 顶栏、面包屑和环境标识。
- 用户概览：今日新增、在线用户、异常用户、累计用户。
- 19 项筛选能力：首屏展示 10 项核心条件，其余 9 项通过“展开更多筛选”进入高级筛选。
- 12 列用户数据表、6 条真实感示例数据和分页。
- 520px 用户详情抽屉，包含 7 个业务 Tab。
- 抽屉首屏展示基础信息、钱包概览、风险快照和操作入口。

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
- 两张界面均无缺失字体。
- 默认态主内容最底部为 y=890，未超出内容区域。
- 抽屉宽度绑定 `layout/drawer/width`，遮罩透明度为 32%。
