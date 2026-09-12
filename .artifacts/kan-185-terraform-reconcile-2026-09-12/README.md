# Nginx 配置通过 Terraform 正式发布

2026-09-12，按用户要求，消除此前直接修改 ConfigMap 导致的管理状态差异。后续基础设施修改必须通过资源现有归属的 Terraform apply 或 GitOps 流程执行。

**本次已经执行 Terraform apply，不是直接修改 Kubernetes，也不是仅修改本地文件。**

## 执行与结果

使用 `bingo-terraform/stacks/aws-prod`，AWS profile `bingo-aws`。部署凭证按仓库 Makefile 的来源从 `.secrets` 和已登录 gh 读取，仅注入进程环境，没有打印凭证或写入仓库。

1. 定向生成 `module.ingress_nginx.helm_release.ingress_nginx` 的保存计划，检查结果只有该资源 update；chart 版本保持 4.15.1，修改字段只有 values 及对应计算产生的 metadata。
2. 执行保存计划：`terraform apply -input=false -no-color /tmp/kan185-terraform-reconcile/nginx.tfplan`。
3. apply 成功，结果为 **0 added, 1 changed, 0 destroyed**。远程 Terraform state 正常更新。
4. Helm release 从 revision 3 更新为 **revision 4**，状态 deployed。
5. 对比保存计划中的五项配置、Helm get values 返回的配置和集群 ConfigMap，三者完全相等。
6. 再次执行 Nginx 定向 plan，`-detailed-exitcode` 返回 **0**，输出 **No changes. Your infrastructure matches the configuration.**
7. 六个开发/生产入口检查均为 HTTP 200。

使用定向计划是为了纠正这一次 Nginx 漂移，避免应用其他资源的修改。没有把本次结果描述为全栈无漂移。工作区原有 withdrawal-hot KMS 修改没有发布。

证据：[计划范围](plan-summary.json)、[配置一致性](reconciliation.json)、[入口检查](http-checks.json)。完整 Terraform plan/state 可能包含敏感数据，因此不放入仓库。

## 管理边界

Nginx 的管理链路仍是 Terraform → Helm → Kubernetes。仓库的 `docs/LAYER3-PLAN.md` 原本将集群、Nginx、ArgoCD 定为 Terraform 管理的基础组件，由 ArgoCD 管理其上的应用。此次没有迁移管理权或增加第二个管理方。

Terraform 代码已同步并正式 apply，并按用户要求单独提交至 `bingo-terraform` 的 `fix/ingress-client-ip` 分支，提交为 [74b5928](https://github.com/bingo-lab-1/bingo-terraform/commit/74b5928)。该分支尚未合并 main；后续部署应使用包含本次修复的代码版本，避免仓库旧配置覆盖已验证的 IP 传递规则。运行配置与本次声明、Helm 发布记录及 Terraform 定向计划已一致。
