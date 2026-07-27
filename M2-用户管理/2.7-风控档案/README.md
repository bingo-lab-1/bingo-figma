---
page: 2.7
name: 风控档案
route: /user/risk
module: M2
permission: user:risk:view
priority: P1
status: 需改造
estimate_days: 5
---

# 2.7 · 风控档案

> **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
查看玩家的注册 IP、设备、关联账号,识别多账号与异常。

## 2. 入口
菜单:用户管理 → 风控 → 风控档案(**「风控」是分组**)

## 3. 字段清单
 待补

## 4. 操作与权限
主权限码 `user:risk:view`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态  待补

## 6. 交互流程
 待补

## 7. 涉及表
`RegisterIpRecord` `RegisterDeviceRecord` `LoginRecord`(owner) → `../表设计.prisma`

## 8. 关联页面
用户列表(2.1)· 封禁管理(2.4)
