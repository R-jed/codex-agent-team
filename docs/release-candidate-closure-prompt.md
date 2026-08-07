# Local Agent Prompt: Release Candidate Closure

你现在负责 `R-jed/subagents-dispatch` 的 version tag / GitHub Release 前最终收口。

先完整阅读：

```text
docs/deep-review-report.md
README.md
README_EN.md
README_AI.md
docs/plugin-installation.md
plugins/subagents-dispatch/.codex-plugin/plugin.json
.agents/plugins/marketplace.json
plugins/subagents-dispatch/skills/dispatch/SKILL.md
plugins/subagents-dispatch/skills/doctor/SKILL.md
plugins/subagents-dispatch/scripts/install-agents.py
plugins/subagents-dispatch/scripts/legacy_migration.py
plugins/subagents-dispatch/scripts/doctor.py
scripts/pre-push-ci.sh
.github/workflows/ci.yml
```

把 `docs/deep-review-report.md` 第十节视为当前最高优先级 release review。前文是历史审查记录，其中部分结论已经被后续证据推翻。不要机械执行旧 P0/P1/P2。

## 已确认的运行事实

真实 Codex 当前运行界面已经验证：

```text
用户命令：/dispatch
用户命令：/doctor
```

Codex command picker 显示 `Dispatch` 和 `Doctor`。选择 `/dispatch` 后，host 会在 composer 中注入 namespaced Skill prompt，例如：

```text
/subagents-dispatch:dispatch ...
```

因此严格区分：

```text
Plugin ID          subagents-dispatch
Skill identity     subagents-dispatch:dispatch / subagents-dispatch:doctor
User command       /dispatch /doctor
Host namespaced    /subagents-dispatch:dispatch /subagents-dispatch:doctor
```

不要把用户文档改成 `$subagents-dispatch:...`。不要为了让用户命令变短，机械修改 Plugin metadata 内部 host namespaced identity。

## 工作目标

完成一个可冻结的 Release Candidate。当前不要创建、移动或删除 version tag，不要创建 GitHub Release。涉及现有 `v1.0.0` tag 的任何破坏性操作必须停下来向用户报告证据并等待明确授权。

按下面顺序执行。每一步都先验证当前事实，再修改。不要根据 `docs/deep-review-report.md` 的文字直接假设代码仍是那个状态。

### 1. 固定 command surface

用户文档统一使用：

```text
/dispatch <task>
/doctor <diagnostic or maintenance request>
```

保留 `/skills` picker。

检查 README、README_EN、README_AI、安装文档、Doctor 文档和测试。区分用户调用文本与 Plugin 内部 namespaced identity。修改后增加能够防止这两层再次混淆的 contract tests。

### 2. 修 Marketplace source contract

根据当前 OpenAI Plugin 官方文档重新验证 `.agents/plugins/marketplace.json`。

Plugin 实际位于：

```text
plugins/subagents-dispatch/
```

若当前官方规范仍要求子目录 Plugin 使用 `git-subdir + path`，按规范修复 source。不要只做 JSON syntax test。更新 packaging tests，使其验证平台语义。

随后完成真实 clean install smoke test。如果本机 Codex 可用，记录：

```text
codex version
marketplace add result
plugin add result
fresh session requirement
Dispatch/Doctor command picker presence
/dispatch selection result
/doctor selection result
```

若某一步无法自动化，明确记录 `UNKNOWN`，不要伪造 PASS。

### 3. 把 legacy migration 接入正常 upgrade flow

审查 `legacy_migration.py`、installer 和 Doctor。

要求老 `codex-delegate` 用户通过正常 Doctor upgrade / repair path 能发现并安全处理 legacy state。不要要求用户预先知道隐藏 CLI 参数。

`--check` 保持只读。mutation 必须来自明确的 repair/upgrade intent。

覆盖状态：

```text
legacy_only
current_only
mixed
legacy_modified
partial
corrupt legacy manifest
migration_complete
```

### 4. 解决跨代锁竞争

旧 installer 使用 `.codex-delegate-agents.lock`，新 installer 使用 `.subagents-dispatch-agents.lock`。

设计清晰的 migration lock ordering，使 migration 期间旧 installer 与新 installer 不会同时修改同一个 `CODEX_HOME/agents`。

新增真实 contention test：必须有另一个进程实际持有 legacy lock。单纯创建 lock 文件不算测试。

### 5. 修 legacy ownership acceptance tests

修正 `test_modified_legacy_profile_preserved` 的 fixture。

正确顺序：

```text
legacy install
manifest records original hash
user modifies profile after install
migration detects hash mismatch
modified legacy profile preserved
warning emitted
current profiles installed safely
rerun idempotent
```

补 corrupt manifest、partial ownership、symlink 和必要 rollback/fault-injection 边界。

不要为了覆盖率数字进行大面积测试重构。只对安全关键状态机补测试。

### 6. 收敛 Doctor managed-profile truth

`install-agents.py --check` 应是 managed profile exact health 的 canonical verifier。

审查 `doctor.py` 是否自己维护了较弱 validator。如果会出现 installer FAIL 但 Doctor healthy 的情况，删除这种第二真相源。

至少故障注入：

```text
correct name + wrong model
correct name + wrong reasoning effort
correct name + wrong sandbox
modified developer instructions
modified bytes with same TOML name
```

Doctor 与 installer 结论必须一致。

### 7. 修 pre-push false green

`scripts/pre-push-ci.sh` 不得 ignore core tests，也不得 `|| true` 后靠 stdout regex 推断 pytest 是否成功。

要求：

```text
pytest failure -> nonzero
collection error -> nonzero
validator failure -> nonzero
installer smoke failure -> nonzero
all required checks pass -> zero
```

尽量让 local pre-push 与 GitHub CI 复用同一个 repo-level verification entry，减少两套逻辑漂移。

### 8. 统一安装与升级 contract

README、README_EN、README_AI、Doctor SKILL、`docs/plugin-installation.md` 必须只有一套 canonical install/update contract。

统一并测试：

```text
marketplace add
plugin add
upgrade
fresh session
legacy upgrade handling
/dispatch
/doctor
/skills
```

不要用“几个 substring 都存在”来证明一致性。测试应能在出现两套冲突命令时失败。

### 9. 清理 release tree

确认根目录 `skills-lock.json` 的真实用途。

如果它只描述维护者本机安装的 `mattpocock/skills`，且不是项目 build/test/runtime dependency，删除并加入合适 ignore。

处理已经确认的低风险问题：

```text
legacy unlink TOCTOU
corrupt manifest semantics
manifest loader duplication/inconsistency
requirements-dev reproducibility
```

低风险问题如果修改会显著扩大 release diff，可保留为 accepted risk，但必须写出理由。

### 10. 版本身份与仓库治理

验证 GitHub tags、manifest version、README badge/version、release 状态。

已知历史证据显示存在：

```text
v1.0.0 tag
目标 commit 内 plugin.json version = 2.0.0
```

重新获取 GitHub 当前事实。

不要自动删除、移动或重建这个 tag。输出：

```text
tag name
tag target SHA
该 SHA 内 Plugin version
是否已有 GitHub Release
建议处理方式
```

等待用户决定 tag 历史处理。

检查 `main` branch protection/ruleset。如果无法通过当前权限修改，写成 release 前人工 gate，不要假装已完成。

### 11. 冻结 Release Candidate

所有代码和文档修复完成后：

1. 确认 working tree clean。
2. push candidate commit。
3. 记录唯一 candidate SHA。
4. 不再对该 SHA 做内容修改。
5. 跑完整 GitHub Actions。
6. 运行可获得的真实 Codex install/runtime smoke。

要求的证据链：

```text
Ubuntu Python 3.11 PASS
Ubuntu Python 3.12 PASS
macOS Python 3.11 PASS
Windows Python 3.11 PASS
full pytest PASS
pinned official OpenAI Plugin validator PASS
managed profile lifecycle PASS
legacy migration acceptance PASS
real Plugin install smoke PASS or explicitly UNKNOWN with reason
/dispatch runtime smoke PASS
/doctor runtime smoke PASS
```

出现任何失败，candidate 作废。修复后产生新的 SHA，重新从完整 evidence chain 开始。

### 12. 最终对抗性审查并更新报告

重新从攻击者/失败路径视角审查 candidate，不要只确认自己刚改的代码。

重点反问：

```text
如果旧用户状态比 fixture 更脏会怎样？
如果两个 installer 同时启动会怎样？
如果 manifest 被截断、替换或 symlink 会怎样？
如果 Doctor 和 installer 看到不同证据会怎样？
如果 Marketplace JSON 合法但 host 不能安装会怎样？
如果 README 与 metadata 各自测试通过但互相矛盾会怎样？
如果 local gate green 而 GitHub CI red 会怎样？
如果 tag/version 不一致，用户如何知道实际安装版本？
```

把 `docs/deep-review-report.md` 更新为 candidate-bound 报告，必须写入：

```text
candidate SHA
Plugin version
GitHub Actions run
exact tests passed
OpenAI validator result
marketplace/install evidence
legacy migration evidence
/dispatch and /doctor runtime evidence
remaining accepted risks
version tag status and pending user decision
final verdict GO or NO-GO
```

## 约束

- 不创建 GitHub Release。
- 不创建新的 version tag。
- 不移动或删除现有 tag，除非用户之后明确授权。
- 不把测试覆盖率数字当产品质量本身。
- 不为了“统一”而复制第三套 policy 或 validator。
- 不降低 existing safety guardrails 来让测试通过。
- 不隐藏 `UNKNOWN`。
- 不因为本地测试 green 就跳过 GitHub Actions。
- 不因为 GitHub Actions green 就跳过 Marketplace / runtime smoke。
- 不使用“已经修了”作为证据。证据必须是实际文件状态、命令结果、测试、CI 或真实 Codex runtime。

## 完成标准

当且仅当所有可执行收口完成后，输出：

```text
Release Candidate SHA: <sha>
Verdict: GO | NO-GO
Blockers: <none or exact blockers>
CI: <run + result>
Tests: <exact count>
Validator: <result>
Marketplace install: <result>
Legacy migration: <result>
/dispatch: <result>
/doctor: <result>
Tag status: <current evidence + user decision still required if applicable>
```

如果 verdict 仍是 `NO-GO`，继续修复真正 blocker。不要创建 tag/release。
