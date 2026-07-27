---
page: 8.1
name: 数值配置
route: /system/config
module: M8
permission: system:config:view
priority: P0
status: 已有
estimate_days: 3
---

# 8.1 · 数值配置

## 1. 用途
全局参数的集中配置。**注意边界:业务配置归各自模块,别把这里变成配置垃圾桶。**

## 2. 入口
菜单:系统设置 → 数值配置

## 3. 字段清单

**配置项字段**(建议给 `Kv` 补的元信息)
| 字段 | 类型 | 说明 |
|---|---|---|
| Key | text | 唯一标识 |
| 值 | 随 valueType 渲染 | |
| **值类型** | select | string/number/boolean/json ← 待新增 |
| **分组** | select | system/risk/wager/other ← 待新增 |
| **描述** | text | 给运营看的说明 ← 待新增 |
| 最后修改人/时间 | 只读 | |

**表格列**:`Key | 描述 | 当前值 | 类型 | 分组 | 最后修改人 | 修改时间 | 操作`

**放这里 vs 建专表的判断**
| 场景 | 归属 |
|---|---|
| 被代码直接读取的单值 | 已有 · `Kv` |
| 有结构、要列表展示、要审核 | 缺失 · 建专表(如 `WithdrawConfig`) |

## 4. 需求清单

| ID | 需求 | 验收标准 | 权限码 | 人日 |
|---|---|---|---|---|
| 8.1-R1 | 按分组分 tab | 系统/风控/打码/其他分组,各显其配置项 | `system:config:view` | 0.5 |
| 8.1-R2 | Kv 元信息扩展 | 补 `valueType`/`group`/`description` 字段,后台按类型渲染表单控件 | `system:config:edit` | 1.5 |
| 8.1-R3 | 编辑与校验 | 按 valueType 校验;JSON 类型需语法校验 | `system:config:edit` | 0.5 |
| 8.1-R4 | 保存与留痕 | 二次确认显示变更 diff;写 `OperationLog` | `system:config:edit` | 0.5 |

## 5. 状态清单
加载 / 正常 / 保存中 / 保存成功 / 校验错误 / 无权限(只读)

## 6. 交互流程
保存即生效( 是否需发布流程待定),变更强制写 `OperationLog`。

## 7. 涉及表
`Kv`(owner,建议补分组/类型/描述字段)→ `../表设计.prisma`

## 8. 关联页面
跳出:操作日志(M7.3)· 提现配置(M3.4)· 币种汇率(8.3)
