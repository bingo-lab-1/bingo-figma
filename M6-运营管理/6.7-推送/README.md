---
page: 6.7
name: 推送
route: /ops/push
module: M6
permission: ops:push:send
priority: P2
status: 缺失
estimate_days: 8
---

# 6.7 · 推送

> ⚠️ **P2 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
极光/Web Push 推送任务的创建与定向发送。

## 2. 入口
菜单:运营管理 → 触达 → 推送(**「触达」是分组**)

## 3. 字段清单
⬜ 待补

## 4. 操作与权限
主权限码 `ops:push:send`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态 ⬜ 待补

## 6. 交互流程
⬜ 待补

## 7. 涉及表
`PushTask`(owner,新增)· 只读 `UserTag`(M2) → `../表设计.prisma`

## 8. 关联页面
站内信(6.1)· 用户标签(M2.5)
