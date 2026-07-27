---
page: 2.6
name: VIP 管理
route: /user/vip
module: M2
permission: user:vip:adjust
priority: P1
status: 需改造
estimate_days: 5
---

# 2.6 · VIP 管理

> **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
查询玩家 VIP 等级与进度,支持手动调级。**双 VIP 决策未定前无法定稿。**

## 2. 入口
菜单:用户管理 → VIP 管理

## 3. 字段清单
 待补

## 4. 操作与权限
主权限码 `user:vip:adjust`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态  待补

## 6. 交互流程
 待补

## 7. 涉及表
`Level` `VipLevel`(owner) → `../表设计.prisma`

## 8. 关联页面
用户列表(2.1)· VIP 配置(M4.9)
