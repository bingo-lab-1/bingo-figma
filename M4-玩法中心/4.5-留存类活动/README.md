---
page: 4.5
name: 留存类活动
route: /game/activity/retention
module: M4
permission: game:activity:edit
priority: P1
status: 缺失
estimate_days: 8
---

# 4.5 · 留存类活动

> ⚠️ **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
签到、通行证、返现等留存类活动配置(活动引擎的分类视图)。

## 2. 入口
菜单:玩法中心 → 活动 → 留存类活动(**「活动」是分组**)

## 3. 字段清单
⬜ 待补

## 4. 操作与权限
主权限码 `game:activity:edit`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态 ⬜ 待补

## 6. 交互流程
⬜ 待补

## 7. 涉及表
`Activity` `ActivityClaim`(owner) → `../表设计.prisma`

## 8. 关联页面
活动引擎(4.1)· 领取记录(4.3)
