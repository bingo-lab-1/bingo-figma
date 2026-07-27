---
page: 4.7
name: 大厅编排
route: /game/lobby
module: M4
permission: game:lobby:edit
priority: P1
status: 需改造
estimate_days: 5
---

# 4.7 · 大厅编排

> **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
配置首页游戏分类、推荐位、热门排序。

## 2. 入口
菜单:玩法中心 → 游戏 → 大厅编排(**「游戏」是分组**)

## 3. 字段清单
 待补

## 4. 操作与权限
主权限码 `game:lobby:edit`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态  待补

## 6. 交互流程
 待补

## 7. 涉及表
`LobbyLayout`(owner,新增)· `GameHot` `SubGame` → `../表设计.prisma`

## 8. 关联页面
游戏列表(4.4)· 展示位管理(M6.2)
