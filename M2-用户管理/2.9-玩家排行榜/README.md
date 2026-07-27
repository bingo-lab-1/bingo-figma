---
page: 2.9
name: 玩家排行榜
route: /user/rank
module: M2
permission: user:rank:view
priority: P2
status: 缺失
estimate_days: 3
---

# 2.9 · 玩家排行榜

> **P2 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
投注额/盈利额排行,供排行榜类活动使用。

## 2. 入口
菜单:用户管理 → 玩家排行榜

## 3. 字段清单
 待补

## 4. 操作与权限
主权限码 `user:rank:view`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态  待补

## 6. 交互流程
 待补

## 7. 涉及表
只读 `BetRecords`(M4) → `../表设计.prisma`

## 8. 关联页面
投注明细(2.3)· 活动引擎(M4.1)
