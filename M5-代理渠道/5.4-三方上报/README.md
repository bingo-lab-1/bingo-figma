---
page: 5.4
name: 三方上报
route: /channel/postback
module: M5
permission: channel:postback:edit
priority: P1
status: 缺失
estimate_days: 5
---

# 5.4 · 三方上报

> **P1 页面,当前为精简规格。** 排期时按 10 段模板补全(见 `00-公共约定/README.md`)。

## 1. 用途
配置 FB/Google/Kwai 等平台的转化事件回传,支撑投放优化。

## 2. 入口
菜单:代理渠道 → 三方上报

## 3. 字段清单
 待补

## 4. 操作与权限
主权限码 `channel:postback:edit`;完整权限点见 `../README.md` 第 6 段。

## 5. 状态清单
空 / 加载 / 错误 / 无权限 —— 特殊态  待补

## 6. 交互流程
 待补

## 7. 涉及表
`ThirdPartyPostback`(owner,新增)· `Channel` → `../表设计.prisma`

## 8. 关联页面
渠道管理(5.3)· 渠道报表(M1.4)
