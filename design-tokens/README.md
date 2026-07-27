# Bingo SaaS Admin Design Tokens

本目录是运营后台视觉系统的单一事实源，服务于 Figma、前端实现和设计评审。

当前可编辑工作稿：
[BINGO SAAS · Design System & 用户管理预览](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB)

原始目标文件 `EAPQVmg3WkxGORMcdnGozN` 对当前 Figma MCP 身份为只读，因此本轮先在同团队工作稿完成变量、组件和界面；获得设计编辑权限后再迁回目标文件。

## 文件

| 文件 | 用途 |
|---|---|
| `bingo-saas.tokens.json` | Token 源定义，包含集合、模式、作用域、文字样式和阴影样式 |
| `tokens.css` | Web 端可直接消费的 CSS Variables |

## 架构

```text
Primitives
  ↓ alias
Semantic Color (Light / Dark)
  ↓ bind
Components
  ↓ instance
Screens
```

- 页面和组件只能使用 Semantic Color，不直接引用颜色原语。
- 间距、圆角、控件高度和布局尺寸必须使用 Dimensions。
- 中文界面使用 Noto Sans SC，表格金额、ID 和统计数字使用 Inter。
- Figma 变量使用 slash 命名，例如 `color/bg/canvas`。
- Web Code Syntax 使用同名 CSS 变量，例如 `var(--color-bg-canvas)`。

## 主题

默认主题为 Light。Dark 模式通过以下属性启用：

```html
<html data-theme="dark">
```

## 修改规则

1. 先修改 `bingo-saas.tokens.json`。
2. 同步更新 `tokens.css`。
3. 同步更新 Figma 中的同名变量。
4. 修改后检查 Token 名称、模式和值是否三方一致。

禁止在页面文档或设计稿中复制一套独立的颜色值。

## Figma 同步状态

- 4 个变量集合，106 个 Variables。
- `Semantic Color` 含 Light / Dark 两个模式，共 60 个 alias mode values。
- 9 个 Text Styles，3 个 Effect Styles。
- 组件：Status Badge、Button、Field、Nav Item、Stat Card、User Table Row。
- 首个业务界面：M2.1 用户列表默认态与详情抽屉态。

关键节点：

- [Foundations](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=3-40)
- [Components](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=2-5)
- [用户列表默认态](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=16-2)
- [用户详情抽屉态](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=22-145)
