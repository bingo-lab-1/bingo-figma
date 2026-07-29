# Bingo SaaS Admin Design Tokens

本目录是运营后台视觉系统的单一事实源，服务于 Figma、前端实现和设计评审。

当前可编辑工作稿：
[BINGO-SAAS](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB)

原始目标文件 `EAPQVmg3WkxGORMcdnGozN`（单页 `Desktop | wallet`）对当前 Figma MCP 身份为只读，因此本轮先在同团队工作稿完成变量、组件和界面；获得设计编辑权限后再迁回目标文件。

## 文件

| 文件 | 用途 |
|---|---|
| `bingo-saas.tokens.json` | Token 源定义，包含集合、模式、作用域、文字样式和阴影样式 |
| `tokens.css` | Web 端可直接消费的 CSS Variables |

## 架构

Figma 侧以 Ant Design 6.5.2 的四层 token 管线为准：

```text
AntD Seed        16 变量   品牌种子：主色、状态色、字号、圆角、间距基数
  ↓ 算法派生
AntD Map         76 变量   AntD 官方派生梯度，不手改
  ↓ 语义命名
AntD Alias       76 变量   设计消费层：背景、文字、边框、尺寸、控件高度
  ↓ 组件绑定
AntD Component   94 变量   13 个组件族的组件级 token
  ↓ instance
Screens
```

- 四个集合都带 `Light` / `Dark` 两个模式，Dark 在 Seed 层切换后逐层解析。
- 页面和组件只能使用 Alias 与 Component 层，不直接引用 Seed / Map。
- 间距、圆角、控件高度必须走变量，不写死数值。
- 文件内 Paint Style 为 0：颜色一律走 Variables，不建色板样式。
- 中文界面使用 Noto Sans SC；表格金额、ID 和统计数字走 `AntD/Typography/Data/Default`。
- Figma 变量的 Web Code Syntax 使用 AntD CSS 变量，例如 `var(--ant-color-bg-container)`、`var(--ant-control-height)`。

**未决项**：本目录的 `bingo-saas.tokens.json` 与 `tokens.css` 仍是上一版 `--color-*` 命名（Primitives / Semantic Color / Dimensions / Typography 四集合），与 Figma 现行的 `--ant-*` 不是同一套。两者对齐前，不要把 `tokens.css` 当作 Figma 的同步产物使用。

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

盘点于 2026-07-29，机器可读版本见 `.figma-build-state.json`。

| 项 | 数量 |
|---|---|
| 页面 | 3 |
| 变量集合 | 4（Seed 16 / Map 76 / Alias 76 / Component 94 = 262） |
| Text Styles | 9（`AntD/Typography/*`） |
| Effect Styles | 4（Primary Button Shadow + Focus Ring ×3） |
| Paint Styles | 0（颜色全部走 Variables） |
| 组件集 | 24（共 273 个变体） |
| 独立组件 | 20（18 个图标 + `BINGO/AppShell` + `BINGO/UserIdentity.Summary`） |
| 业务界面 | 2（均属 M2.1 用户列表） |

页面结构：

| 页面 | Node | 内容 |
|---|---|---|
| [01 · AntD Foundations](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=2-3) | `2:3` | Token 管线、Light / Dark 双板、基础标尺、13 个组件族 token、Effects |
| [02 · AntD Components](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=2-5) | `2:5` | 组件库总板 `AntD 6.5.2 / Components`（1440 × 16001） |
| [03 · M2.1 用户列表](https://www.figma.com/design/HM3qvKHVwFf8sGpml6Q8WB?node-id=2-8) | `2:8` | 用户列表 + 用户详情弹窗，交接说明见 `M2-用户管理/2.1-用户列表/DESIGN.md` |

**页面命名**：`01`、`02` 是设计系统底座；`03` 起一页对应一个需求页面目录，与仓库的「文件夹 = 页面」规则一一对应，M2.2 起依次占用 `04`、`05` …

尚未开始：M1、M3–M8 的任何界面，以及 M2.2–M2.7。
