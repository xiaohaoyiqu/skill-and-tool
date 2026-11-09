# 整体检查：性能、稳定性、易用性与模型接入

检查日期：2026-11-07。结论：当前适合作为本机个人资料库和 Agent 的只读检索服务试用；核心恢复路径已经有回归覆盖。尚未完成长期运行、十万条资料、逐个客户端安装和真实模型效果验收，不按这些范围承诺可用性。

后续已完成项目内独立环境安装、doctor 自检、后台扫描进度/取消与任务结果保留，并通过安装版 MCP 和 wheel 检查。当前状态见 [独立环境与后台扫描](SETUP_AND_TASKS.md)；下面第五轮性能样本保留原始测量范围。

再后续已完成原子批量分拣、浏览器持久化草稿和注释版本冲突处理，见 [批量与草稿说明](BATCH_AND_DRAFTS.md)。

最新复查增加必含词检索、正负例与三种检索模式评测，降低语义查询的候选内存消耗，并修复 Windows 客户端断连处理。实测与后续范围见 [检索复查与扩展](RETRIEVAL_REVIEW.md)。

再后续已实现来源变动检测、可选自动刷新、整理快照导入和路径迁移，见 [来源与恢复](SOURCES_AND_RESTORE.md)。Codex 宿主五工具和真实向量模型样本已验收；完整宿主状态见 [宿主与模型验收](HOST_AND_MODEL_ACCEPTANCE.md)，测试模型已按用户要求删除。

## 本轮实际修改

- 分拣的五个队列合并统计；当前页的技能副本改为一次批量统计，消除逐条扫描数据库的开销。不改变队列和位置记录的含义。
- MCP `get_skill` 默认返回最多 24000 个正文字元，可设 `max_chars=1500..100000`。按返回的 `next` 继续，直到 `next=null`，再采用完整指令。CLI 与手动界面仍可读取完整正文。
- 正文分页按字符切分，支持超长单行与 Unicode。索引的 revision 继续归一化换行；新增 content_revision 保留换行差异，防止 LF/CRLF 变化后字符偏移错位。续页必须携带 next 中的版本参数。
- MCP 单次工具响应限制为 1 MiB，超出返回可解释工具错误；不会输出一半 JSON。这个限制包含文本兼容输出与结构化输出，不等于模型 token 上限。
- 工具字段按协商的 MCP 版本输出。2024-11-05 不输出 annotations/outputSchema/structuredContent；2025-03-26 不输出后两项，支持最多 100 条消息的批次；2025-06-18 和 2025-11-25 保留结构化输出。新版不接受批次。请求字符串 ID 限 1024 字符。
- 新增源码启动器 `scripts/sklib_launcher.py`，绝对 Python 路径与启动器路径配合绝对 --home，不依赖客户端是否支持 cwd。
- Git 记录操作增加等待提示与按钮互斥，避免连续点击产生难以理解的状态。浏览器回归初次在并行负载下超过 5 秒等待；验收允许 Git 预览等待 15 秒，不将测试等待值当作服务超时保证。
- 切换条目后恢复当前页面内未确认保存的笔记草稿；保存失败或响应丢失时仍保留草稿。刷新、关闭页面或其他页面之间不会同步草稿。

## 性能实测

Windows，Python 3.10.0、SQLite 3.35.5；5000 条合成技能，正文约 30 行，包含 499 个副本位置。每项先预热，再测 20 次。计时为应用调用的实际耗时，不包含模型推理。原始结果：[修改前](performance-before.json)、[修改后](performance-after.json)。

| 操作 | 修改后中位数 | 修改后 P95 |
|---|---:|---:|
| 名称检索 | 94.33 ms | 136.36 ms |
| 宽泛英文检索 | 86.77 ms | 109.56 ms |
| 中文检索 | 86.59 ms | 131.62 ms |
| 全部浏览 | 125.17 ms | 142.02 ms |
| 重复技能队列 | 212.65 ms | 287.98 ms |
| 最近收录排序 | 207.78 ms | 277.82 ms |
| 读取一个小技能与资源清单 | 11.76 ms | 14.14 ms |

原全部浏览中位数为 1219.58 ms、P95 为 1587.96 ms。修改前后使用相同生成规则和数量，但各自是独立临时库，运行期间有其他检查负载；数据表明瓶颈改善，不把差值作为所有机器的加速比例。

修改后首次索引 16.248 秒，未变化重扫 5.272 秒，数据库约 42.8 MiB。四线程完成 100 次混合操作，其中 10 次注释写入，错误为 0，总耗时 5.929 秒，操作 P95 为 361.70 ms；SQLite quick_check 和 FTS integrity-check 均通过，正文和全文索引各 5000 行。

真实资料复查使用五个本地来源，共 197 个技能、6 项项目资料。两轮扫描均完整、无读取错误，第二轮全部识别为未变化；合计检查 2880 个文件。临时标记一条后，未分类与待复核队列均从 203 降至 202。五条已知开发任务 Hit@5、MRR@5、Recall@5 均为 1.0，P95 为 40.30 ms；这是很小的已知样本，不能证明其他任务的检索质量。

性能边界：未测冷缓存、持续内存占用、网络盘、十万条资料或数日运行。语义检索目前遍历可用向量计算相似度，未使用近似向量索引；本轮数据只覆盖词法检索，不覆盖真实嵌入模型延迟。后续已将界面索引改为后台队列，提供进度、取消和任务记录；没有后台任务的负载性能保证。

复现：

```powershell
python scripts/audit_performance.py --entries 5000 --repetitions 20 --output docs/performance-after.json
python -m unittest discover -s tests -p 'test_[clrs]*.py' -q
python -m unittest discover -s tests -p test_browser.py -v
```

## 稳定性与易用性

本轮 Python 3.10/3.12 回归、真实 Edge 和 SDK 结果见 [验证记录](VALIDATION.md)。关键覆盖包括整轮/单条写入回滚、并发来源更新、损坏输入、读取版本变化、Git 预览失效、提交结果不确定、保存成功后响应丢失、资源分页和正文分页。没有进行断电与物理磁盘损坏测试。

界面已经能无关键词浏览、按来源/类型/标签/状态筛选、查看依据和文件能力、管理笔记和 Git 记录。390 像素窄屏与主流程通过浏览器检查；本轮补了条目切换草稿恢复和 Git 操作等待状态。

仍有明确的体验缺口：来源目录靠手动输入，没有自动更新来源；错误部分保留英文技术信息。批量分拣和浏览器持久化草稿已在后续补齐，草稿跨浏览器共享仍需导出。未进行屏幕阅读器完整验收或外部用户可用性测试。后续已在 .venv 安装运行依赖，并验证 Python wheel；尚无独立桌面安装器。

## 接入兼容性

模型通过宿主使用工具。SKLIB 的词法检索不调用模型 API；模型品牌不会改变数据库、搜索和文件读取逻辑。Agent 客户端能启动本机 stdio MCP、发现工具并执行工具调用，才具备直接接入条件。仅有聊天接口或 OpenAI 风格的模型 API，不会自动变成 MCP 客户端。

| 接入对象 | 当前情况 | 本轮证据与限制 |
|---|---|---|
| 官方 MCP Python SDK 1.30.0 | 实际联调通过 | 独立子进程、协议 2025-11-25、四个工具、schema 校验、两页完整正文、参考文件续读、错误后 ping；[原始结果](mcp-sdk-check.json) |
| 四个已声明 MCP 版本 | 工具子集通过本地回归 | 2024-11-05 / 2025-03-26 / 2025-06-18 / 2025-11-25；按版本检查字段和批次行为；未做全规范认证 |
| Codex、Claude Code、Gemini CLI | 官方文档支持本机 stdio，接入方式匹配 | 已给配置样例；没有写入用户配置或启动实际模型会话，不能标为宿主验收通过 |
| VS Code 的 MCP Agent | 官方文档提供 stdio 配置 | 配置入口与上述客户端不同；未安装验收 |
| Qwen、DeepSeek、Llama 等经 MCP Agent 调用 | 取决于宿主和模型工具调用能力 | 本工具没有模型白名单；未逐个模型测量选工具、填参和遵循工作流的正确率 |
| 不支持 MCP、但能运行本机命令的 Agent | 可调用 CLI JSON | 必须由宿主处理进程、退出码和 JSON；无专用模型 API function-calling 适配器 |
| 仅能连接远程 HTTP MCP 的宿主 | 当前不能直接连接此 stdio 服务 | 手动界面的 HTTP API 不是 Streamable HTTP MCP；需要单独实现受控适配或本地执行桥接 |
| Ollama 嵌入后端 | 可选 CLI/API 语义检索 | `/api/embed` 请求与失败恢复有模拟服务测试；真实模型质量未验收，MCP/界面仍用词法检索 |

官方 SDK 使用项目内隔离检查目录 `.audit-client`，没有安装为应用运行依赖或修改全局 Python 包。检查脚本为 `scripts/check_mcp_client.py`，已有 SDK 时可直接运行；隔离安装时用 `--sdk-path <目录>`。Windows 沙箱对异步管道的权限限制需要与服务器兼容性问题区分。

小上下文模型可从 `get_skill(..., max_chars=1500)` 开始，逐页读取。字符数和 estimated_tokens 都不能代替宿主的实际 tokenizer。先检索少量候选，再取正文与必要资源，避免把整个资料库塞入上下文。读取成功只证明拿到了资料；执行脚本仍取决于宿主权限、运行环境与技能自己的依赖。

## 配置方式与接入验收

可复制样例位于 [Codex](../examples/mcp/codex.toml)、[Claude Code](../examples/mcp/claude.json)、[Gemini CLI](../examples/mcp/gemini.json)。路径按本工作区提供，移动项目或更换 Python 时要一起调整。所有客户端必须使用同一个绝对 --home；MCP 不会自动扫描来源，首次需要手动或 CLI 添加资料。建议在独立 Python 环境安装项目依赖后再配置长期使用。

宿主验收应依次确认：能启动并列出四个工具 → list_library 能看到预期来源 → search_skills 检索中文任务 → get_skill 跟随 next 读完 → read_skill_file 续读成功 → 不存在的 ID 返回工具错误且后续请求正常。官方 SDK 已验证这条链路，宿主自己的权限、工具策略和上下文处理仍需逐个确认。

本轮未运行付费模型推理、下载嵌入模型或修改任何 Agent 配置。后台索引、批量分拣和浏览器草稿已在后续实现；剩余优先级是宿主实装验收，以及包含无相关项和易混淆任务的真实检索评测。

对接格式依据：[OpenAI Docs：MCP](https://learn.chatgpt.com/docs/extend/mcp)、[Claude Code MCP](https://code.claude.com/docs/en/mcp)、[Gemini CLI MCP](https://geminicli.com/docs/tools/mcp-server/)、[VS Code MCP](https://code.visualstudio.com/docs/agent-customization/mcp-servers)。

协议依据：[2025-06-18 结构化输出变更](https://modelcontextprotocol.io/specification/2025-06-18/changelog)、[2025-03-26 批次与工具注解变更](https://modelcontextprotocol.io/specification/2025-03-26/changelog)、[MCP 工具规范](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)。嵌入格式依据：[Ollama embed API](https://docs.ollama.com/api/embed)。
