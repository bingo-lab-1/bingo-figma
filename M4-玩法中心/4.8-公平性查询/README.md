---
page: 4.8
name: 公平性查询
route: /game/fairness
module: M4
permission: game:fairness:view
priority: P1
status: 已有
estimate_days: 2
---

# 4.8 · 公平性查询

> ⚠️ **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
provably fair 种子查询与验证,处理玩家公平性质疑。**这是产品卖点,别弱化。**

## 2. 入口
菜单:玩法中心 → 游戏 → 公平性查询(**「游戏」是分组**)

## 3. 字段清单
⬜ 待补

## 4. 操作与权限
主权限码 `game:fairness:view`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态 ⬜ 待补

## 6. 交互流程
⬜ 待补

## 7. 涉及表
`Fairness` `FairnessHistory`(owner) → `../表设计.prisma`

## 8. 关联页面
投注明细(M2.3)· 游戏列表(4.4)
