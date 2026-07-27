---
page: 2.8
name: 点控记录
route: /user/point-control
module: M2
permission: user:point-control:view
priority: P2
status: 缺失
estimate_days: 3
---

# 2.8 · 点控记录

> **P2 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
查询对特定玩家的赢率干预记录。

## 2. 入口
菜单:用户管理 → 风控 → 点控记录(**「风控」是分组**)

## 3. 字段清单
 待补

## 4. 操作与权限
主权限码 `user:point-control:view`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态  待补

## 6. 交互流程
 待补

## 7. 涉及表
`PointControlRecord`(owner,新增) → `../表设计.prisma`

## 8. 关联页面
用户列表(2.1)· 投注明细(2.3)
