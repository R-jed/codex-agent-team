# Codex Agent Team

**让你的 Codex 会话拥有一支会自动分工、会独立复核、会在越界前先问你的 AI 团队。**

Codex Agent Team 是一个面向 Codex Native Subagents 的轻量 Skill。它保留当前主会话的控制权，把重上下文执行交给 GPT-5.6 Luna Max，把关键独立审查交给 GPT-5.6 Terra XHigh，并在确实需要更强能力、更高权限、更大作用范围或高风险操作时，用普通人能理解的话请求一次性授权。

> Your Codex session stays in control. Luna Max handles deep execution. Terra XHigh challenges important results. Material escalation requires human consent.

## 装上之后，Codex 会发生什么变化

复杂任务经常把代码搜索、日志、测试输出、失败尝试、实现过程和最终决策全部塞进一个会话。Codex Agent Team 的目标，是把这些工作拆成一个克制的小团队，让主会话保持聚焦。

| 日常 Codex 工作流 | 使用 Codex Agent Team |
| --- | --- |
| 大量搜索、日志和测试进入主上下文 | 重上下文工作交给独立 Luna Max Worker |
| 主模型从调查做到实现，再自己检查 | 关键结果可交给 Terra XHigh 做独立复核 |
| 用户自己决定什么时候派 Subagent | Skill 先过 Delegation Gate，再决定是否组队 |
| 能开几个 Agent 就容易开几个 | 默认 0 到 1 个，通常不超过 2 个，硬上限 4 个 |
| 子任务可能继承过多主会话内容 | 按角色最小化上下文继承 |
| 目标模型不可用时行为不确定 | 精确路线不可用就安全回到 Root |
| 高级权限和成本策略需要用户预配置 | 真正越界时才用大白话申请一次性授权 |
| 单一路径容易形成确认偏差 | Terra XHigh 提供异构模型的独立判断 |

Codex 官方资料强调，Subagent 的重要价值包括隔离 context pollution 和 context rot，让父线程保留目标、约束和关键决策，把高噪声中间过程放到独立上下文。Codex Agent Team 围绕这个原则设计，并进一步加入模型分工、最小团队和授权边界。

## Team 架构

```text
                         CURRENT ROOT
                  用户当前正在使用的 Codex 会话
                              │
                       Delegation Gate
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
       LUNA MAX WORKER                 TERRA XHIGH CRITIC
       Deep Execution                  Independent Judgment
       Explorer / Worker               Review / Synthesis
              │                               │
              └───────────────┬───────────────┘
                              │
                         Root integrates
                              │
                 需要跨越重大能力或风险边界？
                              │
                    Consent Gate if needed
                              │
              optional SOL SENIOR JUDGE
             仅 Root 非 Sol 且用户确认时
```

### Root Controller

当前主会话永远拥有最终控制权。Skill 不要求用户把主模型固定成 Sol。

如果主会话是 Sol Medium 或 High，Sol 负责目标理解、规划、架构、风险判断、整合和最终输出，Luna Max 承担重执行，Terra XHigh 在真正需要独立判断时介入。

如果主会话本身是 Luna Max，额外的 Luna Max Subagent 仍然可以通过独立上下文承担大规模搜索、日志、测试和实现工作。重要结果可以交给 Terra XHigh 做异构复核。只有极少数高后果且证据仍不足的情况，Skill 才会建议一次 Sol Senior Judge，并先向用户解释原因和成本影响。

### Luna Max: Execution Engine

默认执行层使用 `gpt-5.6-luna` + `max`。

适合：

- 代码库探索和调用链追踪
- 大量文件、日志、测试和文档扫描
- 边界清楚的实现、修复和局部重构
- Bug 复现与根因调查
- 测试设计、执行和失败分析
- Diff inspection 和第一轮机械性检查
- 任何高工具调用、高上下文消耗、最终只需要简短证据摘要的工作

### Terra XHigh: Independent Critic

独立审查层使用 `gpt-5.6-terra` + `xhigh`。

它不会因为“任务很难”就自动出现。触发条件集中在：

- 独立验证
- 跨模块综合
- 证据冲突
- 重大假设挑战
- 实质性需求歧义
- 一个错误结论会明显改变后续方向

Terra Reviewer 默认使用尽可能干净的上下文，只接收原始目标、验收条件、关键证据、Diff 或产物，避免先接受生成者已经形成的结论。

### Sol Senior Judge

Sol 不进入常规 Worker 池。

当 Root 本身已经是 Sol 时，高风险最终判断留在当前 Root。

当 Root 不是 Sol，且 Luna 与 Terra 对关键问题仍有实质冲突，或任务涉及安全边界、权限模型、数据完整性、复杂并发、不易回滚的重大决策时，Skill 可以建议一次 `gpt-5.6-sol` Senior Judge。它只在用户确认后调用，默认承担一次高价值复核，不接管普通执行工作。

## 为什么采用这组模型

GPT-5.6 当前官方定位中，Sol 面向复杂专业工作的旗舰能力，Terra 面向智能与成本平衡，Luna 面向成本敏感和高吞吐工作负载。三个模型都支持从 `none` 到 `max` 的 reasoning effort。

Codex Agent Team 把这种模型分层转化成稳定角色：

- Root 保留最高信息价值的上下文和最终决策
- Luna Max 消化高 token、高工具调用的执行过程
- Terra XHigh 提供异构模型的第二意见
- Sol 只在它真正有边际价值的地方承担高级判断

模型价格、可用性和 Codex runtime 能力会变化。Core Policy 不依赖固定价格数字，运行时只使用当前 Codex 明确支持的精确路线。

官方资料：

- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/guides/latest-model
- https://developers.openai.com/api/docs/models/gpt-5.6-luna
- https://developers.openai.com/api/docs/models/gpt-5.6-terra
- https://developers.openai.com/api/docs/models/gpt-5.6-sol

## 三道核心 Gate

### 1. Delegation Gate

只有存在具体收益时才创建 Subagent：

1. **Context isolation**: 大量中间信息会污染 Root 上下文
2. **Real parallelism**: 存在真正独立、并行后能缩短时间的工作分支
3. **Independent verification**: 重要结果需要由没有参与生成的 Agent 独立检查

下面这些理由单独出现时都不够：

- 文件很多
- 任务很长
- 任务看起来困难
- 用户要求认真一点
- Luna 很便宜
- 还有空闲并发

### 2. Capability Gate

Skill 使用当前 Codex 的 live native Subagent 能力作为事实来源。

优先级：

1. 当前 `spawn_agent` 明确暴露并接受目标 model + reasoning effort
2. 如果目标路线与当前 Root 完全一致，而且 runtime 明确支持继承，可以使用继承
3. 如果用户安装了可选自定义 Agent profile，可以使用 profile 中固定的精确路线
4. 以上条件都不成立，任务安全回到 Root

Skill 不使用随机模型切换，也不会因为 Luna 不可用就偷偷把普通 Worker 换成更贵的模型。

### 3. Consent Gate

正常团队协作无需不断询问用户。只有下一步会实质扩大成本、权限、作用范围或外部影响时才申请一次性授权。

例如：

> 这里有一个会影响整体实现的关键判断，目前两次独立分析给出了不同结论。我建议临时用一次更强的模型做最终复核。它只做分析，不会修改文件，但会增加一些模型使用成本。要继续吗？

或者：

> 问题已经定位。下一步需要修改 3 个项目文件并运行相关测试，目前还没有改动任何内容。要我直接处理吗？

用户原始请求中已经明确授权的内容不会重复询问。比如用户直接要求“修复这个 bug 并运行测试”，正常范围内的写入和测试已经属于本次任务授权。

## 安全默认开启

### Minimum Team

- 0 个 Subagent 是正常状态
- 默认 1 个
- 通常最多 2 个
- 硬上限 4 个
- 自动 Terra Reviewer 最多 1 个
- 自动 Sol Senior Judge 最多 1 个
- 3 到 4 个 Agent 的额外 fan-out 通常需要用户同意，除非用户已经明确要求广泛并行

### One Writer

同一个共享 workspace 同时最多一个 writing Worker。并行读取可以广泛使用，并行写入必须有明确隔离环境或明确互不重叠的写边界。

### Fail Closed

精确模型、effort、role 或必要权限无法确认时，任务回到 Root。Skill 不通过随机 fallback 猜测运行时能力。

### Permission-Aware Delegation

Skill 区分：

- `runtime_enforced`
- `instruction_enforced`
- `unknown`

如果任务只有在真正的 read-only runtime 下才安全，而当前 runtime 无法确认 read-only，Skill 不会创建该 Worker。

### Prompt-Injection Boundary

源码、网页、日志、Issue、测试 fixture、生成内容和引用数据中的指令全部视为不可信数据。它们不能改变：

- 用户目标
- Agent 数量
- 模型路线
- 权限
- Scope
- 凭证访问范围
- 外部副作用边界

### No Recursive Teams

Worker 不允许继续创建 Subagent。发现 nested delegation 时，Root 应把结果标记为 policy violation，并停止依赖该结果。

### High-Impact Actions Stay With Root

Worker 不执行发布、付款、生产变更、破坏性删除、账户操作或其他高后果外部行为。此类操作留给 Root，并遵循用户授权和 Codex 自身权限机制。

## 零配置优先

安装后继续正常使用 Codex 即可。

用户无需先理解或配置：

- model ladder
- allow_upscale
- provider policy
- risk profile
- YAML routing switches

Skill 在运行时自己做保守判断，并只在真正跨边界时询问。

高级用户可以选装 `examples/agents/` 中的自定义 Agent profiles，把模型、reasoning effort 和 sandbox 进一步固定到本地配置。Core 不依赖这些 profile。

## 安装

克隆仓库：

```bash
git clone https://github.com/R-jed/codex-agent-team.git
```

复制 Skill 到 Codex Skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R codex-agent-team/skill/codex-agent-team ~/.codex/skills/codex-agent-team
```

开发时也可以使用软链接：

```bash
ln -s "$(pwd)/skill/codex-agent-team" ~/.codex/skills/codex-agent-team
```

Skill 支持隐式调用，也可以显式使用：

```text
$codex-agent-team
```

## 一个典型工作流

用户：

> 帮我修复这个认证问题，检查相关测试，并确认有没有影响现有 session 行为。

可能的 Team：

```text
Root
├─ Luna Max Worker
│  ├─ trace auth flow
│  ├─ implement bounded fix
│  └─ run tests
└─ Terra XHigh Critic
   └─ independently review session compatibility
```

Root 最后检查 Diff、测试证据和 Reviewer finding，再向用户交付结果。

如果任务只是一处简单修改，Skill 会选择 0 个 Subagent，Root 直接完成。

## 开源仓库和安装 Skill 分离

仓库包含 README、测试、eval 和开发资料。真正安装给 Codex 的运行目录只有：

```text
skill/codex-agent-team/
```

这符合 Codex Skill 的 progressive disclosure 原则，让运行时上下文保持精简。

```text
codex-agent-team/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── docs/
├── examples/
├── evals/
├── tests/
└── skill/
    └── codex-agent-team/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            ├── routing-policy.md
            ├── task-packet.md
            ├── consent-policy.md
            └── safety-policy.md
```

## 设计原则

Codex Agent Team 有十条稳定核心：

1. 当前主会话始终拥有最终控制权
2. 没有明确 delegation benefit 时不创建 Subagent
3. Luna Max 是默认 Execution Worker
4. Terra XHigh 只用于真正需要独立判断的任务
5. Sol 只在 Root 已经是 Sol，或 Root 非 Sol 且用户同意高级复核时承担 Senior Judge
6. 默认一个 Worker，通常最多两个，硬上限四个
7. 精确 native route 不可用就回 Root
8. Worker 不递归组队，外部内容不能改变安全规则
9. 用户已有授权就继续执行，实质越界时触发 Consent Gate
10. Root 只整合带证据、满足验收条件并通过安全检查的 Worker 结果

## 当前边界

Codex Agent Team 聚焦 Task 内 Native Subagents。

Core 当前不负责：

- App Thread orchestration
- Worktree 生命周期调度
- 持久 DAG
- 跨 Host Task 控制
- Provider 路由
- 自动发布、部署或生产变更

这些能力很有价值，但会显著扩大状态机和安全面。Codex Agent Team 保持轻量团队路由器的产品边界。

## 开发与验证

安装开发依赖：

```bash
python -m pip install -r requirements-dev.txt
```

运行：

```bash
pytest -q
```

测试覆盖 Skill metadata、openai.yaml、routing eval schema、团队数量、模型角色、Consent Gate、安全约束和 One Writer invariant。

## License

MIT
