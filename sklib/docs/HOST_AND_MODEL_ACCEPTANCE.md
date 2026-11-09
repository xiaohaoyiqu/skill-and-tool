# 宿主和真实向量模型验收

本轮按 OpenAI Docs、Claude Code、Gemini CLI 和 VS Code 的官方接口资料核对配置，并将协议调用、宿主调用和模型推理分开记录。没有向日常宿主配置写入测试设置。

## 验收状态

| 项目 | 实际结果 | 范围 |
|---|---|---|
| 官方 MCP Python SDK 1.30.0 | 通过 | 5 个工具的 schema、来源检测、检索约束、完整读取/续页、结构化/文本一致、错误后恢复 |
| Codex 0.166.0 app-server | 通过 | 临时只读会话中，通过宿主实际调用 5 个工具，并读取临时随机校验值；错误后继续调用成功 |
| Codex CLI 模型驱动会话 | 未完成 | 在工具调用前持续重连并超时；已隔离其他 MCP 服务、移除注入的无效代理并尝试系统代理，未把它计为通过 |
| Claude Code 2.1.69 | 按用户选择待验收 | 已安装、当前未登录；用户选择暂不登录，不继续发起模型验收 |
| Gemini CLI | 配置启动命令通过，宿主待验收 | 本机未安装 Gemini CLI，没有运行其真实模型会话 |
| VS Code | 配置启动命令通过，宿主待验收 | 本机已安装；未在 Copilot/Agent 界面逐工具实装验收 |
| Ollama EmbeddingGemma | 真实推理通过，已删除模型 | 双语样例和 203 条实际资料完成建向量及三种模式评测 |

四份示例配置的 Python/args 已分别在无关中文工作目录中启动真实 stdio 服务，验证列出五个工具、工具错误及后续 ping。该检查证明启动命令可用，不代替各宿主的权限、上下文和模型行为验收。

配置样例：

- [Codex TOML](../examples/mcp/codex.toml)
- [Claude Code JSON](../examples/mcp/claude.json)
- [Gemini CLI JSON](../examples/mcp/gemini.json)
- [VS Code JSON](../examples/mcp/vscode.json)

换机器时同时调整解释器、源码和状态目录路径。MCP 的五个工具均为只读：search_skills、list_library、get_skill、read_skill_file、check_source；写入整理记录仍通过本地界面或 CLI。

## 真实宿主检查脚本

```powershell
# 通过 Codex 自身直接执行 MCP 工具，不调用模型。
.\.venv\Scripts\python.exe scripts/check_codex_mcp.py --output docs/codex-mcp-check.json
# 需要已登录、可访问模型的本机账号；仅临时配置和短任务。
.\.venv\Scripts\python.exe scripts/check_hosts.py --host codex --output docs/host-codex-check.json
# Claude 当前按用户要求保留待登录状态；以后主动登录后可运行。
.\.venv\Scripts\python.exe scripts/check_hosts.py --host claude
```

检查使用临时目录、独立索引和只存在于参考文件中的随机值，核对真实工具调用链。模型驱动脚本保留配置覆盖在当前进程，结束后清理临时文件；Windows 上只终止本次启动的超时进程树。报告不保存账号凭据或宿主的原始私密输出。

当运行器注入 127.0.0.1:9 无效代理时，宿主验收脚本在调用者已允许网络执行的前提下，移除该注入项并沿用 Windows 已有系统代理；不修改环境注册表或全局配置。模型会话超时仍应检查账号、模型访问和网络，不能据 MCP 工具层通过推断其模型调用也已通过。

报告：[codex-mcp-check.json](codex-mcp-check.json)、[host-codex-check.json](host-codex-check.json)、[mcp-installed-check.json](mcp-installed-check.json)。

## 向量模型实测

显式下载并使用 EmbeddingGemma（约 622 MB，官方标为 300M，本机元数据 307.58M、BF16），产生 768 维向量。产品运行时仍不自动下载模型。

先以 5 个双语技能、10 个中英文任务验证接口、向量缓存和三种检索模式，再在 anthropic-skills、vue-skills-full、Humanizer-zh、obsidian-skills、scientific-agent-skills 的临时索引上实测：197 个技能、6 个项目说明，共建 203 条向量。第二次建库更新 0 条，缓存匹配通过。

实际资料使用 --batch-size 4 --timeout 120，建向量约 32.592 秒。5 个正例的 Hit@5/MRR@5/Recall@5 在词法、语义、混合三种模式均为 1；4 个显式技术名约束负例均为空。任务很少、标签不穷尽，约束来自调用者，不能当成通用相关性或自动拒答保证。

| 本机 9 条开发任务 | 词法 | 语义 | 混合 |
|---|---:|---:|---:|
| P95 查询延迟 | 50.15 ms | 3255.54 ms | 123.64 ms |

这是一次按顺序的功能验收，包含模型冷暖状态差异，不把三列差值解释为受控性能提升。最初较大的冷启动批次触及默认 60 秒超时，未完成该轮；降低批次、显式增大超时后完成真实资料验收。embed/search/eval 现可设置 --timeout 1..600，默认仍为 60；embed 的 --batch-size 范围为 1..64。

复现脚本只使用显式指定、已安装的本机模型：

```powershell
.\.venv\Scripts\python.exe scripts/check_local_model.py --model <已有向量模型> --batch-size 4 --timeout 120
# 真实资料可另传重复的 --root 和 --dataset；默认使用临时双语样例。
```

结果见 [local-model-check.json](local-model-check.json) 和 [local-corpus-model-check.json](local-corpus-model-check.json)。

## 模型清理

用户要求测试后删除，已执行卸载与 `ollama rm embeddinggemma`，并通过模型列表确认它已不存在。原有 deepseek-r1:latest 和 deepseek-r1:8b 保留；测试索引和临时资料由 TemporaryDirectory 清理。仅保留代码和报告，见 [model-cleanup.json](model-cleanup.json)。

## 官方参考

- OpenAI Docs：[Codex MCP](https://learn.chatgpt.com/docs/extend/mcp)、[Codex app-server](https://learn.chatgpt.com/docs/app-server)、[非交互模式](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Claude Code CLI](https://code.claude.com/docs/en/cli-reference)
- [Gemini CLI MCP](https://geminicli.com/docs/tools/mcp-server/)
- [VS Code MCP](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
- [Ollama embed API](https://docs.ollama.com/api/embed)、[EmbeddingGemma 模型说明](https://ollama.com/library/embeddinggemma)
