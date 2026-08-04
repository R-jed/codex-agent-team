<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo-light.svg">
    <img alt="Codex Delegate" src="docs/logo-dark.svg" width="128">
  </picture>
</p>

<h1 align="center">Codex Delegate</h1>

<p align="center">
  <a href="README_EN.md">English</a> · <a href="docs/plugin-installation.md">安装指南</a> · <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/version-0.6.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/status-pre--v1-orange.svg" alt="Status">
</p>

Codex Delegate 是 **Codex Native Subagents 之上的委派策略层**。它让当前 Codex 主会话继续掌握需求、架构、决策和最终验收，只把适合委派的、边界清楚的工作交给不同 Agent，并用实际 diff、测试和证据决定任务是否完成。

当前版本：`0.6.0`，pre-v1。

## 1. 这个项目是什么

直接使用 Codex Subagents 时，真正困难的通常不是“能不能再开一个 Agent”，而是下面这些问题：

- 什么工作值得委派，什么工作主会话自己做更好？
- 应该把实现、调查、判断分别交给谁？
- 多个 Agent 怎么避免重复搜索、重复实现和无意义并行？
- 一个 Agent 失败以后应该继续、重试、换上下文，还是升级到更强的技术调查？
- 高风险改动在完成前，怎样增加一次与实现过程隔离的独立复核？
- 怎么避免子 Agent 越权、改错范围、覆盖用户已有修改，或者因为“它说完成了”就直接接受？

Codex Delegate 解决的是这些 **orchestration / delegation policy** 问题。

它不会预设固定团队，也不会要求每个任务都走同一条模型流水线。项目的基本原则是：

```text
先理解任务
-> 找出仍未解决的依赖
-> 判断是否值得委派
-> 把责任编译成可验收合同
-> 选择最合适的执行 / 调查 / 判断资源
-> 检查实际产物和证据
-> 必要时恢复、升级或独立复核
-> 主会话最终验收
```

因此，Codex Delegate **没有固定 Agent 数量**。一个已经非常清楚的局部修改可以使用 `0` 个 Subagent；复杂任务也不会因为“复杂”就机械地把 Luna、Terra、Sol 全部调用一遍。

当前四个语义角色是：

| 角色 | 当前模型 | 主要职责 |
| --- | --- | --- |
| Luna Reader | GPT-5.6 Luna `max` | 搜索、调用链追踪、测试映射、证据收集 |
| Luna Worker | GPT-5.6 Luna `max` | 实现、调试、测试、局部重构 |
| Terra Investigator | GPT-5.6 Terra `xhigh` | 解决仍未完成的复杂技术 delta |
| Sol Advisor | GPT-5.6 Sol `high` | 高价值判断、选择性复核、风险触发的独立最终复核 |

模型是计算资源，主会话才是控制平面。更强的模型不会自动获得更大的产品、架构、权限或范围决策权。

## 2. 怎么安装

Codex Delegate 只通过 Codex 原生 Plugin 系统分发。

首次安装时，注册这个 Git marketplace：

```bash
codex plugin marketplace add R-jed/codex-agent-team --ref main \
  --sparse .agents/plugins \
  --sparse plugins/codex-agent-team
```

然后安装 Plugin：

```bash
codex plugin add codex-agent-team@codex-agent-team
```

安装后启动一个 **新的 Codex thread**，然后直接使用：

```text
/codex-delegate 修复这个 bug，并运行相关测试。
```

如果已经安装过，需要更新时先刷新 marketplace snapshot：

```bash
codex plugin marketplace upgrade codex-agent-team
codex plugin add codex-agent-team@codex-agent-team
```

更新后同样启动新的 Codex thread。

### 第一次需要模型专用 Agent 时

Plugin 本身负责分发 Skill 和项目文件。四个自定义 Agent profile 属于 Codex 的另一套配置表面，默认安装在：

```text
$CODEX_HOME/agents
```

通常也就是：

```text
~/.codex/agents
```

Codex Delegate 不会在 Plugin 安装时偷偷写这些 profile。只有某个任务真正需要 Luna / Terra / Sol 专用角色，而且当前 profile 尚未准备好时，它才会说明准备写入的项目管理路径并请求授权。

授权后的 installer 只管理四个 Codex Delegate profile 和自己的 ownership manifest，并提供非修改性的 `--check` 验证。它不会修改凭据、MCP、仓库、`config.toml` 或无关 Agent profile。

**Plugin manifest 不声明不存在的 `agents` 组件**。Plugin 分发和 custom-Agent provisioning 是两个明确分开的步骤。

更完整的首次安装、升级、旧版本迁移和失败处理见 [Plugin Installation](docs/plugin-installation.md)。

## 3. 它能干什么

Codex Delegate 适合日常软件开发中需要“让 Codex 自己决定怎么合理使用 Subagents”的任务，例如：

- 修 bug，同时定位调用链和补测试；
- 实现功能，但保持 public API / schema / compatibility 不变；
- 跨模块重构，并把搜索、实现和验证拆成不同依赖；
- 复杂故障排查，把真正未解决的技术难点单独交给 Terra；
- 在长任务里复用已经确认的 repository facts 和测试证据，减少重复扫描；
- 对 security、authorization、migration、data integrity、concurrency、public contract 等高风险交付物增加 Fresh Sol 独立最终复核；
- 在存在多个独立依赖时并行处理，但不为了“用满 Agent”而制造重复工作。

### 一个实际运作案例

假设你输入：

```text
/codex-delegate 修复登录重试在并发请求下重复刷新 token 的问题，保持 public API 不变，并补回归测试。
```

一次典型执行可能是这样的。

**主会话先定义任务真相。** 它不会马上选择模型，而是确认验收条件：并发请求不能重复执行 refresh；现有 public API 不变；相关测试必须通过；用户已有修改不能被覆盖。然后把未解决事项放进当前会话的 Dependency Ledger。

```text
D1  找到 refresh 的真实调用链和已有测试
D2  实现去重 / 同步修复并补回归测试
D3  证明并发语义和兼容性满足验收
D4  高风险最终复核（如触发）
```

**Luna Reader 处理 D1。** 它只负责搜索和建立证据，例如找到 refresh 入口、共享状态、相关测试和 public API 边界。主会话把这些已经确认的事实保存为可复用证据，后续 Agent 不需要从头再搜一遍。

**Luna Worker 处理 D2。** 主会话不会把原始一句话直接扔给 Worker，而是给一个有范围、接口、不变量、验收条件和验证命令的 Delegation Contract。Worker 可以决定具体怎么实现，但不能擅自改变 public API、扩大产品范围或重写无关模块。

假设第一次实现后测试暴露出一个更深的 lock ordering / race condition。此时 **未通过验收和需要改变执行方式是两个不同判断**。如果新证据仍在缩小问题，Codex Delegate 可以继续当前责任；如果已经形成真正的技术能力缺口，才进入 Intervention Gate。

**Terra Investigator 只接收那个尚未解决的并发技术 delta。** 它不会把整个任务重新做一遍，也不是“Luna 不够强就全量升级”。Terra 默认只读，负责解释 race 的根因、必要的不变量以及可验证的修复约束。主会话据此更新合同，再让 Luna Worker 完成有边界的修正。

如果执行过程中出现过无效尝试，主会话会把有意义的失败签名、修正假设和新证据保存在精简的 **Recovery Ledger** 里。它不会使用固定重试次数，也不会把完整对话或私有推理当成恢复状态带入新上下文。

实现完成后，**主会话自己检查实际 diff、修改范围和测试结果**。Agent 的“完成”报告只是一项声明，不是验收证据。

这个案例涉及 authorization token、concurrency，而且如果 Terra 的调查实质影响了最终方案，Final Review Gate 会被提升为 `required`。

### 高风险改动的最终质量门

**Sol 不是所有任务的固定阶段**。低风险局部改动可以在主会话检查实际 diff 并完成确定性验证后结束。

当任务涉及 public contract、persistent state、security / authorization、data integrity、concurrency、migration、wide blast radius，或者执行过程中发生 material Terra escalation、material recovery、重要 verification gap，Final Review Gate 可以变成 `required`。

在上面的案例中，主会话验证通过后只能进入：

```text
Candidate Ready
```

随后用 `review-artifact.py` 给当前最终交付物生成确定性的：

```text
review_artifact_id
```

再启动一个 fresh-context Sol Advisor。它不继承实现过程中的长对话和失败叙事，而是拿到目标、验收条件、有效证据、实际 artifact 和 review focus，独立检查最终结果。

它的完成性 verdict 是：

```text
ship       -> 当前 artifact 可以完成
fix-first  -> 先修复，再重新验证，并启动新的 fresh review
rethink    -> 当前架构、合同或关键假设需要重新处理
```

如果证据不足以可靠判断，Advisor 可以返回：

```text
INSUFFICIENT_EVIDENCE
```

此时 gate 仍未满足，需要补齐明确缺失的证据后再启动一次新的 Fresh Sol review。

如果 Sol 给出 `ship` 后任何交付文件又发生变化，当前 artifact 就不再匹配原来的 `review_artifact_id`，旧 verdict 自动失效。这避免出现“review 过 A，最后却交付 B”的情况。

如果这是一个简单 typo，上面的 Reader、Terra、Sol 都可能完全不会出现。Codex Delegate 的目标是构建**最小但足够的计算图**，而不是展示一个固定多 Agent 流程。

### 卡住时如何处理

Codex Delegate 把“测试还没通过”和“当前执行方式已经不值得继续”分开处理。

只要 artifact、测试、repository fact 或 unresolved delta 显示任务仍在向前推进，就不会因为一次失败机械升级模型。只有证据支持 intervention 时才分类处理：

```text
局部机械问题
-> Luna 做有明确假设的针对性修正

合同不完整
-> 主会话修合同

上下文污染 / 无效循环
-> 用当前 artifact + 有效证据 + Recovery Ledger 启动干净的同级上下文

真实技术能力缺口
-> Terra 只处理 unresolved technical delta

高价值判断缺口
-> 主会话决定，或在有价值时使用 Sol
```

## 4. 架构是怎么设计的

Codex Delegate 没有额外的后台 scheduler、持久化 DAG 服务或第二套 Agent runtime。它是一层运行在当前 Codex 会话里的 policy system。

整体结构可以理解为：

```text
                         User Task
                             |
                             v
                       Main Session
                  intent / scope / decisions
                             |
                             v
                      Dependency Ledger
                             |
              +--------------+--------------+
              |                             |
      Delegation Benefit Gate        Contractability Gate
              |                             |
              +--------------+--------------+
                             |
                             v
                       Ready Frontier
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
     Luna Reader        Luna Worker      Terra Investigator
      evidence          implementation      tech delta
          \                  |                  /
           +-----------------+-----------------+
                             |
                             v
                 Main inspection + verification
                             |
                             v
                    Final Review Gate
                       /            \
              not required        required
                    |                 |
                    v                 v
                  DONE       Fresh Sol Advisor
                                      |
                         ship / fix-first / rethink
```

这里有几个关键设计。

### 主会话始终是控制平面

主会话拥有：用户意图、scope、架构、Dependency Ledger、调度、证据、恢复、integration、acceptance 和最终回复。

子 Agent 解决的是一个有边界的 dependency，不拥有整个任务。

### Dependency Ledger 只追踪“还缺什么”

每个重要依赖至少包含 outcome、状态、前置条件、预期产物、write intent、workspace 和 acceptance。

```text
pending -> ready -> running -> satisfied
                    |
                    +-> blocked / invalidated
```

只有真正 ready 且仍未解决的 dependency 才有资格被调度。已经 satisfied 的工作不会因为还有空闲 slot 就重复调用模型。

### 两道 gate 决定“该不该委派”

Delegation Benefit Gate 要求委派至少产生一种明确价值：context isolation、真正的并行收益、专门能力，或者独立判断。

Contractability Gate 要求写入任务在交给 Worker 前已经明确 scope、interface、invariant、decision rights、acceptance oracle、verification 和 stop / escalate 条件。

### Routing 看责任，不看模型等级

Luna 是默认执行资源；Terra 处理真正剩下的复杂技术 delta；Sol 处理高价值 judgment 和必要的独立 review。

合法图可以是：

```text
main
main -> Luna -> main
main -> Terra -> Luna -> main
main -> Luna -> Sol -> main
main -> Sol -> main
```

不存在强制的 `Luna -> Terra -> Sol` 模型阶梯。

### 并行由依赖、授权和 runtime 共同决定

显式 `/codex-delegate` 使用时，**最多两个同时活跃**且确有价值的 child Agents 属于正常无需再次确认的资源范围。超过这个并发范围，或者串行调用已经形成明显的额外计算成本时，需要重新经过 consent。

这个“2”只是 consent boundary，不是团队目标，也不是产品硬上限。真正能同时运行多少还取决于 ready dependencies、workspace safety 和 Codex runtime 当前可用 child slots。

同一个 **physical checkout** 同时最多一个 Writing Worker。不同且真正隔离的 worktree / workspace 才能各自拥有 writer。

### Shared Evidence State 避免重复工作

确定性测试结果、repository fact、接口事实等证据可以在依赖仍有效时继续复用。文件或运行状态变化时，只使真正依赖它的证据失效，而不是整仓重新扫描。

model judgment 始终只是可质疑的判断，不会因为被缓存就升级成事实。

### Intervention Gate 负责恢复，不负责机械升级

执行失败后先判断是否仍有 evidence-supported progress。只有真正需要改变执行方式时，才进入恢复分类。

这也是 Recovery Ledger 存在的原因：记录有意义的尝试、failure signature、修正假设和 unresolved delta，让 fresh context 不再重复已经证实无效的路线。

### Final Review Gate 把“主会话认为完成”和“高风险交付可发布”分开

普通任务不必增加 Sol 成本。高风险任务则在主会话 verification 之后增加一个 fresh-context 独立质量门，并把 verdict 和确切 artifact 绑定。

这样可以保留自适应计算的成本优势，同时给高后果改动增加最后一道独立否决权。

## 5. 安全性怎么样

Codex Delegate 的安全设计核心是 **最小权限、明确责任、实际证据、fail closed**。它不是通过“模型应该听话”来建立安全保证。

### 权限意图和 runtime 保证分开

Reader、Investigator、Advisor 的 profile 可以声明 read-only，但配置文本本身不等于 host 已经真正强制只读。

项目区分：

```text
write_intent
requires_enforced_read_only
permission_guarantee
```

如果某项安全要求必须依赖 host-enforced read-only，而当前 runtime 又无法证明有效 sandbox，Codex Delegate 会把这项责任留在主会话，而不是伪装成已经获得硬隔离。

### 子 Agent 不能继续创建 Agent

delegation depth 固定为一层。Child 不允许继续 spawn Subagent、后台 Agent team 或持久委派任务。

### 一个 physical checkout 只有一个 writer

Writing Worker 必须保留用户或其他会话已经存在的无关修改，不允许为了恢复“预期初始状态”而 revert 未知变化。

如果 workspace drift 让 scope、interface、invariant 或 acceptance 失效，Worker 应停止并把控制权交回主会话。

### Prompt injection 被当作不可信数据

源码、网页、日志、issue、测试 fixture、生成内容以及其他 Agent 输出里的指令，都不能自行改变：

- 用户真正要求的 outcome；
- scope / acceptance；
- Agent route；
- permission；
- consent；
- Dependency Ledger；
- evidence validity；
- Final Review Gate；
- 外部副作用授权。

它们可以成为“需要报告的内容”，但不能成为 orchestration policy。

### Exact route 不可用时 fail closed

需要专用 Luna / Terra / Sol route 时，必须能看到匹配的项目 profile。缺失、冲突或版本不一致时，对应 delegation 停回主会话，不会偷偷换成一个“差不多”的模型继续跑。

### Agent 报告不是完成证明

Worker 说“已经改好”、Reviewer 说“看起来没问题”、多个模型一致同意，都不能单独成为 acceptance。

主会话必须检查实际 artifact、changed files、diff、测试和可复现 evidence。高风险 Final Review 还要验证最终 artifact 和收到 `ship` 的 `review_artifact_id` 仍然一致。

### 高影响外部动作仍留在主会话

Child Agents 不负责 production deployment、破坏性数据删除、支付、第三方消息发布、账号权限管理或其他不可逆外部副作用。这些动作仍然由主会话和用户授权边界控制。

### Installer 采用 ownership / exactness 防护

profile installer 只管理项目自己的文件；遇到用户修改过或无法证明由本项目拥有的 profile 会拒绝覆盖。它还拒绝 symlinked managed destinations，并支持非修改性的 `--check`。

需要注意，这些机制提高了安全性，但并不代表所有 runtime / 多进程边界已经获得实测证明。当前已知验证状态见下一节。

## 6. 使用前需要注意什么

Codex Delegate `0.6.0` 已进入 `main`，仓库的最终 v0.6.0 合并候选通过 Ubuntu / Python 3.11、Ubuntu / Python 3.12、macOS / Python 3.11、pinned official OpenAI Plugin validator，以及 `167` 个 pytest。

但它仍然是 **pre-v1**。以下行为仍在 current Codex runtime 上完成正式 live validation，因此不要把仓库静态测试理解成对所有 runtime 行为的保证：

- Worker / Investigator / Advisor 的 exact live route；
- required Final Review Gate 的 Fresh Sol route、artifact handoff 和完整 verdict lifecycle；
- 跨独立主会话对同一 physical checkout 的 writer exclusion；
- concurrent same-`CODEX_HOME` installer 行为；
- 正式 release 前的 current official Plugin validator 与真实 marketplace install / upgrade 路径。

实际使用时还应注意：

- 安装、升级或重新安装 Plugin 后，使用新的 Codex thread；
- profile provisioning 成功但当前任务仍看不到新角色时，也新开一个任务再调用 `/codex-delegate`；
- 多个独立 Codex 会话暂时不要同时写同一个 physical checkout；
- 四个 managed Agent profile 是 `CODEX_HOME` 级共享状态，不是每个项目各有一份；
- 当前没有跨独立会话持久共享的全局 Evidence Store；
- 当前没有额外后台 scheduler 或持久 DAG 服务；
- 更大并行和明显增加的多轮 Agent 调用可能增加 token / latency 成本，并受 Consent Gate 约束；
- Final Review Gate 是风险触发机制，不代表每个普通修改都会支付一次 Sol review 成本；
- 如果你要求的是硬性的 host-enforced read-only、精确模型 route 证明或其他 runtime 安全属性，应以实际 runtime evidence 为准，而不是只看 profile / prompt 配置。

如果你希望了解更详细的安装、迁移和 profile ownership 规则，请阅读 [安装指南](docs/plugin-installation.md)。

## License

[MIT](LICENSE)
