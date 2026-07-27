---
page: 7.2
name: 角色权限
route: /system/role
module: M7
permission: system:role:view
priority: P0
status: 已有
estimate_days: 2
---

# 7.2 · 角色权限

## 1. 用途
定义角色及其权限集合。**权限粒度 = 菜单节点。**

## 2. 入口
菜单:权限审计 → 角色权限

## 3. 字段清单

**角色字段**
| 字段 | 类型 | 必填 |
|---|---|---|
| 角色名称 | text | ✅ |
| 角色类型 | select | ✅ |
| 备注 | textarea | — |
| 角色权限 | 勾选树 | ✅ |

**权限树结构**(顶层 = 8 大模块)
```
□ 全选
├─ □ M1 数据中心
│   ├─ □ 大盘概览      analytics:overview:view
│   └─ □ 导出报表      analytics:export
├─ □ M2 用户管理
│   ├─ □ 查看用户      user:list:view
│   ├─ □ 封禁/解封     user:ban
│   └─ ...
├─ □ M3 财务管理  ← 含高危权限,建议单独角色
│   ├─ □ 审核提现      finance:withdraw:review
│   ├─ □ 人工上下分    finance:manual:adjust
│   └─ □ 清空打码      finance:wager:clear
└─ ...
```
右侧「预览」实时显示已选权限清单。

**表格列**:`序号 | 角色名 | 类型 | 权限数 | 关联账号数 | 备注 | 操作`

## 4. 需求清单

| ID | 需求 | 验收标准 | 权限码 | 人日 |
|---|---|---|---|---|
| 7.2-R1 | 角色列表 | 显示角色名/类型/权限数/关联账号数 | `system:role:view` | 0.5 |
| 7.2-R2 | 权限勾选树 | 顶层 8 模块可展开到页面级;支持全选;右侧实时预览已选 | `system:role:edit` | 1 |
| 7.2-R3 | 角色 CRUD | 名称唯一;内置角色不可删;有关联账号时删除阻断 | `system:role:edit` | 0.5 |

## 5. 状态清单
空 / 加载 / 错误 / 无权限 / 内置角色(不可删)/ 有关联账号(删除阻断)

## 6. 交互流程
勾选父节点自动全选子节点;权限变更对已登录账号**下次请求生效**。

## 7. 涉及表
`Role` `Permission` `RolePermission`(owner)→ `../表设计.prisma`

## 8. 关联页面
跳出:后台账号(7.1)· 操作日志(7.3)
**权限点来源**:各模块 README 的「权限点汇总」段
