# 客户端 IP 透传修复与复测

> 后续更新：已按用户要求通过 Terraform apply 正式发布，并确认 Nginx 定向 plan 无剩余差异。见[Terraform 发布记录](../kan-185-terraform-reconcile-2026-09-12/README.md)。下文保留首次直接修改 ConfigMap 的过程。

2026-09-12 用户明确要求更新 IP 传递配置后实施。此前现象和 ALB 网卡归属见[反查记录](../kan-185-ip-trace-2026-09-12/README.md)。

**结果：共享 ingress-nginx 配置已更新并成功热加载。开发环境新注册、PC 登录、模拟手机登录均记录公网出口 IP，伪造 X-Forwarded-For / X-Real-IP 未改变最终地址，错误密码未覆盖成功登录记录。**

## 修改内容与发布范围

更新 `bingo-prod` Kubernetes context 中 `ingress-nginx/ingress-nginx-controller` ConfigMap 的五项配置：

- enable-real-ip=true
- use-forwarded-headers=true
- forwarded-for-header=X-Forwarded-For
- compute-full-forwarded-for=false
- proxy-real-ip-cidr：实际 ALB 所在三个子网，加 Cloudflare 官方 IPv4/IPv6 代理网段。

Nginx 递归识别可信代理链，将识别后的单个客户端 IP 传给后端。保留原始链用于排障，但不让应用直接依赖未经核验的第一个地址。没有开启信任所有来源，也没有写死单个 ALB 节点 IP。Cloudflare 网段于当日从官方 `/ips-v4`、`/ips-v6` 核对。

ALB 安全组实际仅允许 Cloudflare IPv4 网段访问 80/443。此次可信内网范围为现有 ALB 子网，同时也包含集群内部工作负载；这是现有信任边界，不代表已经实现工作负载之间的网络隔离。未新增公网入口、修改安全组、修改 ALB、切换后端镜像或修改后端环境变量。

这是共享入口，开发、生产及内部域名共同使用。2026-09-12 12:45:25 UTC，两个 controller 日志均记录 Backend successfully reloaded，Pod 保持 Ready、无重启。

发布采用带 resourceVersion 检查的 JSON Patch，先服务端 dry-run，再实际更新；发布前配置 data 为空并已备份。实际配置见[applied-config.json](applied-config.json)。

## 验证结果

测试使用专用账号 `qa_ip_fix_1789217170049`，只通过开发环境 API 注册和登录，在后台详情查看实际记录；未充值或下注。公网出口参照来自同一请求客户端访问 `dev-casino.bingox.io/cdn-cgi/trace`，并验证其为公网地址。仓库证据已脱敏 IP，不保存密码或会话令牌。

| 测试 | 结果 |
|---|---|
| 新注册及自动登录 | 成功；注册、自动登录 IP 均等于参照公网 IP，注册域名正确 |
| 普通 PC 登录 | HTTP 200；最新记录更新，IP 正确，PC / Chrome / macOS |
| 伪造 X-Forwarded-For=198.51.100.77、X-Real-IP=198.51.100.88 | HTTP 200；请求进入后端并生成新记录，保存的仍为参照公网 IP |
| 模拟 iPhone User-Agent 登录 | HTTP 200；IP 正确，Mobile / Safari / iOS。是请求级模拟，不是真机界面测试 |
| 错误密码登录 | HTTP 401；上一条成功登录记录的 IP、设备、时间等保持不变 |
| 六个开发/生产入口检查 | 发布前后均 HTTP 200，包括前端、后台和开发认证查询接口 |
| 两个 ingress controller | 成功热加载，均 Ready，无重启 |

早期同时伪造 CF-Connecting-IP 的尝试返回非 JSON 页面，未把该次尝试计为成功的后端防伪验证。表中防伪结果来自随后只伪造 X-Forwarded-For / X-Real-IP 且返回 200 的独立请求。

证据：[verification.json](verification.json)、[http-checks.json](http-checks.json)。没有跨公网网络、真实手机、生产会员登录、全部业务流程或并发登录测试。

## Terraform 同步与检查

本地修改 `bingo-terraform`：

- `modules/addons/ingress-nginx/main.tf`：通过 Helm values 配置真实 IP 识别。
- `modules/addons/ingress-nginx/variables.tf`：新增可信代理 CIDR 参数及校验，默认空列表保留其他调用方行为。
- `modules/cluster/aws-eks/outputs.tf`：输出实际子网 CIDR，避免依赖 ALB 动态 IP。
- `stacks/aws-prod/main.tf`：向入口模块传入子网和 Cloudflare 范围。
- `stacks/aws-prod/ingress-real-ip.tf`：Cloudflare 代理范围及信任边界说明。

Terraform fmt 检查、validate 和 git diff --check 通过；Nginx 候选 real-IP 配置在当前 controller 中 `nginx -t` 通过。定向 Terraform plan 因根模块部署变量缺失未能完成，没有执行 Terraform apply。本次线上生效来自上述 ConfigMap 更新，不是 Helm release 升级。

Terraform 修改未 commit/push。工作区原有的 withdrawal-hot KMS 配置修改保留，未纳入本次线上发布。后续从仓库部署前应提交本次配置，并在具备部署变量的环境完成 plan，避免旧仓库配置覆盖本次运行配置。

## 为什么当前仍保留 Nginx

ALB 负责公网负载均衡入口，Nginx 负责集群内按域名/路径路由。现有前端 Rollout 明确配置 `trafficRouting.nginx.stableIngress`，含 25%、50%、100% 灰度步骤及检查。内部 NLB 也指向 ingress-nginx，供内部域名访问。

ALB 能直接路由到服务，并不技术上强制需要 Nginx；但移除现有 Nginx 需要迁移 Ingress 路由、灰度发布及内部访问链路，不能只删除一个代理层。本次只修复 IP 传递，未实施入口架构迁移。
