---
page: 4.6
name: 打码类活动
route: /game/activity/wagering
module: M4
permission: game:activity:edit
priority: P1
status: 需改造
estimate_days: 5
---

# 4.6 · 打码类活动

> ⚠️ **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
返水、洗码等按流水发放的活动配置。

## 2. 入口
菜单:玩法中心 → 活动 → 打码类活动(**「活动」是分组**)

## 3. 字段清单
⬜ 待补

## 4. 操作与权限
主权限码 `game:activity:edit`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态 ⬜ 待补

## 6. 交互流程
⬜ 待补

## 7. 涉及表
`Activity` `ActivityClaim`(owner)· `CodingMultiple`(M8) → `../表设计.prisma`

## 8. 关联页面
活动引擎(4.1)· 打码核销(M3.7)
