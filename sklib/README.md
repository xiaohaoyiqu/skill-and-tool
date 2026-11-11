# SKLIB

面向 Agent 和人的本地 Skill / 项目资料检索工具。扫描本地目录，返回带来源与原文依据的候选；选定后读取完整技能及配套文件。CLI、stdio MCP 和手动界面共用同一个应用核心。

本工程源码收录于 [skill-and-tool](https://github.com/xiaohaoyiqu/skill-and-tool) 的 `sklib/` 子目录。克隆聚合仓库后进入该子目录使用；下文的 `E:\aimodel\sklib` 是开发机路径，应替换为自己的实际目录。虚拟环境、索引与个人整理数据、模型和构建产物不包含在源码中。

当前实现：中文/英文词法检索、可解释查询扩展、技能内容副本折叠、来源与版本、增量索引、标签/备注/收藏、多语言项目清单与文档检索、资源分类与分页、UTF/BOM 和显式旧编码支持、可选本地 Ollama 语义/混合检索、独立 Git 记录仓库。

库内分拣可直接浏览全部条目、未分类、待复核、有警告和重复技能五个队列，按来源、程序类型、个人标签和状态筛选。完整说明及逐功能的失败恢复表见 [分拣与故障处理](docs/SORTING_AND_RECOVERY.md)。

最新整体检查、5000 条资料的实测性能、易用性缺口和客户端兼容矩阵见 [整体检查](docs/SYSTEM_REVIEW.md)。已用官方 MCP Python SDK 完成真实子进程联调；具体模型和宿主安装验收仍单独区分。

本工作区已经在 .venv 安装项目与运行依赖，TOML 解析可用；手动扫描已支持后台队列、进度、取消与结果保留。安装、启动、任务状态与失败恢复见 [独立环境与后台扫描](docs/SETUP_AND_TASKS.md)。

现在可跨页勾选最多 100 个位置，原子批量修改标签、状态和收藏。笔记草稿支持当前浏览器内的刷新与新页面恢复、草稿箱和导出，正式保存与批量操作带版本冲突检查。范围和失败处理见 [批量分拣与浏览器草稿](docs/BATCH_AND_DRAFTS.md)。

## 运行条件与开发状态

- Python 3.10+，带 SQLite FTS5；PyYAML 6.x。Python 3.10 的 TOML 元数据使用 tomli 2.x，Python 3.11+ 使用标准库 tomllib。依赖在 pyproject.toml 中声明。
- 当前是源码开发版本；没有安装全局命令、修改 Agent 配置、启动守护进程或下载模型。
- 从本目录直接执行 `python -m sklib`。打包安装后入口为 `sklib`。
- 测试使用临时目录、临时 HTTP 服务和独立 Git fixture；不会提交真实项目或修改技能来源。

当前工作区直接启动：

```powershell
cd E:\aimodel\sklib
.\.venv\Scripts\sklib.exe --home E:\aimodel\sklib\.sklib doctor
.\.venv\Scripts\sklib.exe --home E:\aimodel\sklib\.sklib ui --port 8765
```

以下源码命令中的 python 请使用本项目 .venv 的解释器，或将 python -m sklib 替换为 .\.venv\Scripts\sklib.exe。

```powershell
cd E:\aimodel\sklib
python -m sklib --help

# 状态目录显式传入；也可设置 SKLIB_HOME。
python -m sklib --home .\.sklib index E:\aimodel --max-files 1000000
python -m sklib --home .\.sklib search "PDF 表格提取" --json
python -m sklib --home .\.sklib search "Vue 页面性能优化" --limit 5
python -m sklib --home .\.sklib browse --queue unclassified --kind all
python -m sklib --home .\.sklib show <skill-id> --json
python -m sklib --home .\.sklib read <skill-id> references/guide.md --max-lines 200
python -m sklib --home .\.sklib status

# 仅显式运行时启动，Ctrl+C 停止；不会自动打开浏览器。
python -m sklib --home .\.sklib ui --port 8765
```

`--home` 是全局参数，放在子命令之前。默认状态目录是当前工作目录的 `.sklib`，不写入用户主目录。索引包含资料原文，个人笔记也可能包含私有信息；选择适当的本地目录保存。

## 扫描与查询

- 默认发现 `SKILL.md`、11 类语言生态的项目清单，以及根/直接子目录/实际仓库根/含清单目录的 README；README 支持无扩展名、MD/RST/TXT 等格式。`--include-docs` 可索引其余 MD/Markdown/MDX/RST/TXT/AsciiDoc 文档。完整范围见 [兼容性说明](docs/COMPATIBILITY.md)。
- 默认不进入 `.git`、依赖目录、构建输出、测试夹具、目录链接和应用状态目录。不会按聚合仓库的 `.gitignore` 排除第三方收藏仓库。
- 单文件最多 2 MiB，默认最多检查 100000 个文件、深度 30；可通过参数调整。超出文件数量时整次索引不写入。深度或读取错误导致的部分扫描不会清理未见条目。
- 手动界面新来源的扫描上限为 1000000 个文件；HTTP 索引请求可显式指定 `max_files` / `max_depth`。重扫沿用来源设置，CLI 省略选项也会保留文档范围、编码和扫描限制；`--no-include-docs` / `--clear-excludes` 可清除相应配置。
- 界面扫描使用后台任务，最多 10 项未结束任务、同一来源不重复排队。进度和结果可在刷新后找回；取消在安全检查点回滚未提交修改。异常重启后的未确认任务标记 interrupted，核对来源报告后手动重扫。原同步 HTTP /api/index 保留。
- 重扫依据大小与纳秒时间判断变化；`--verify` 重新读取并哈希，适用于保留了时间戳的外部编辑。
- 大目录可加 `--progress`，进度输出到 stderr，最终 JSON 保持在 stdout；Ctrl+C 取消返回退出码 130，未提交的索引事务会回滚。
- 完整扫描返回 0；部分扫描返回 3，并输出 complete=false 和失败明细；运行错误返回 2。失败明细包含路径、错误码和恢复建议，最多保留前 200 项并提供 failure_count。单条可隔离失败回滚其正文与 FTS，SQLite 写入失败则回滚本轮事务。
- 同一状态库的根目录不能重叠。可先 `remove-root <旧目录>` 再索引父目录；只移除索引，保留源文件与个人注释。
- 同一来源在扫描期间被另一次扫描或移除操作改变时，旧扫描会拒绝写回并提示重扫，避免覆盖较新的条目或重新加入已移除来源。
- YAML 不合法的技能仍收录，并附警告；其语法异常不阻断整个资料库。
- 内容哈希归一化 CRLF/LF，技能副本分组只针对实际相同内容；同名不同内容保持独立。项目资料各自保留，避免不同项目的相同模板被折叠。每个位置有独立 ID 和注释。
- 搜索结果是有界候选池，`candidate_groups` 不是全库精确命中总数。默认池大小 200，分页最大 offset 500。`max_chars` 约束结果条目的总字符预算，不含结果外层统计。
- 中文任务中出现明确 ASCII 名称时，词法候选需要包含至少一个这样的名称，避免 Vue 不存在时只返回泛泛的“优化”技能。
- 显式选 `document` 且中英混合查询含至少三个 ASCII 检索词时，词法候选须同时匹配这些词。Markdown 证据优先取匹配章节内的正文，保留原文行号。

```powershell
python -m sklib annotate <skill-id> --tag 前端 --tag 性能 --note "适用于页面排查" --favorite --state useful
python -m sklib search "页面优化" --tag 前端 --favorite --state useful --json
python -m sklib search "架构" --kind project --json
python -m sklib search "project" --kind project --project-type python --json
python -m sklib index E:\project --include-docs --verify
python -m sklib index E:\legacy --encoding gb18030
python -m sklib history
```

状态：`unreviewed`、`to_try`、`useful`、`not_recommended`。`--clear-tags` 清空标签，`--no-favorite` 取消收藏。

## Agent 接入

启动命令：`python -m sklib --home <绝对状态路径> mcp`。宿主应将工作目录设为此项目，或先在独立环境安装本项目。

以下是采用 mcpServers 格式的进程配置示意，不自动修改任何客户端配置。使用项目内已安装环境，不依赖宿主的工作目录：

```json
{
  "mcpServers": {
    "sklib": {
      "command": "E:/aimodel/sklib/.venv/Scripts/python.exe",
      "args": ["-m", "sklib", "--home", "E:/aimodel/sklib/.sklib", "mcp"]
    }
  }
}
```

Codex 使用 TOML 配置；[各客户端样例](examples/mcp)分别提供 Codex、Claude Code、Gemini CLI 和 VS Code 格式。各入口应传入相同的绝对 --home，避免连接到不同或空的资料库。也可以使用独立环境中已安装的 sklib 命令。

| 工具 | 行为 |
|---|---|
| `search_skills(query, kind?, queue?, required_terms?, limit?, offset?, tags?, favorite?, state?, root?, project_type?, max_chars?)` | 词法检索；`kind` 支持 skill/project/document/all，可限制分拣队列和程序类型 |
| `list_library(queue?, kind?, sort?, root?, project_type?, tags?, favorite?, state?, limit?, offset?, max_chars?)` | 无需关键词的分拣浏览；逐位置列出，返回计数和下一页 |
| `get_skill(id, expected_revision?, start_char?, max_chars?, expected_content_revision?)` | 默认读取最多 24000 个正文字元，按 next 跟随至完整；附当前与索引版本、过期标记和最多 256 项资源清单，file_details 附带类型、大小与文本读取能力 |
| `read_skill_file(id, relative_path, start_line?, max_lines?, max_chars?, expected_revision?, encoding?)` | 有边界地读取资源，返回下一页起始行、实际编码和内容版本；二进制只列信息 |
| `check_source(root, verify?, max_changes?)` | 只读检查一个已登记来源的新增、修改、删除和完整性，不自动更新索引 |

stdio 服务实现 MCP 2025-11-25、2025-06-18、2025-03-26、2024-11-05 的生命周期、ping 和工具子集。只声明工具能力；无 HTTP MCP、资源订阅、采样或脚本执行能力。2025-06-18 起提供结构化对象及文本兼容输出，旧版省略尚不存在的字段；2025-03-26 支持最多 100 条消息的批次，其他版本不接受批次。单次工具响应最多 1 MiB，超出返回工具错误。异常 Unicode、非有限数值和过深嵌套的 JSON 输入会返回错误，并继续处理后续请求。初始说明提醒 Agent 先检索、再读完整指令；宿主仍决定是否调用和如何采用第三方内容。

`get_skill` 读取当前磁盘正文；与索引版本不同时 stale=true，并重新解析当前元数据。首次可传入搜索得到的 expected_revision 拒绝过期选择。正文续页直接采用 next 提供的参数；content_revision 额外检测换行变化，避免字符偏移错位。CLI 和界面仍读取完整正文。参考文件每次读取独立校验版本，分页可传回上一页 revision。空结果可能表示未索引，不能推断整个文件系统没有相关技能。

## 可选语义检索

词法检索不需要模型或外部服务。已有本地 Ollama 与嵌入模型时，可显式使用：

```powershell
python -m sklib embed --model <已有的多语言嵌入模型名>
python -m sklib search "将论文整理成结构化笔记" --mode semantic --model <同一模型名> --json
python -m sklib search "将论文整理成结构化笔记" --mode hybrid --model <同一模型名> --json
# 缓存损坏或需要重建时，显式覆盖匹配的向量。
python -m sklib embed --model <同一模型名> --force
```

不会下载或拉取模型。嵌入仅允许显式配置的 loopback HTTP 地址，默认 `http://127.0.0.1:11434`；禁用代理与跳转。当前只在 CLI/API 开放语义模式，MCP 和界面使用词法检索。模型、端点和文档版本不匹配的向量不参与检索，`semantic_coverage` 明示覆盖量。文本使用名称、描述和前 12000 字符正文，Ollama 按自身上下文上限截断；向量排序不是兼容性或正确率证明。跨进程迁移不同字节序机器时重新生成向量。

## Git 记录功能

记录仓库固定在 `<home>/records/`，与技能来源、源码仓库和索引缓存分开。只提交 `catalog.json`：来源、扫描设置、相对路径、内容哈希、标签、笔记、收藏、使用状态。已移除来源的笔记另存于 `orphaned_annotations`，保留其 ID、标签和状态。不会提交技能正文、SQLite、向量或日志，也不会 push。

```powershell
python -m sklib records init
python -m sklib records export
python -m sklib records preview
python -m sklib records commit -m "整理前端技能并补充使用笔记"
python -m sklib records log
python -m sklib records status
```

Git 身份沿用现有配置；需要时自行在记录仓库内配置 `user.name` 与 `user.email`。程序不修改全局 Git 配置。提交使用 `--only -- catalog.json`，保留其他已暂存内容；失败时按 Git 本身行为，catalog 可能保持已暂存。无变化不创建空提交。记录快照含本地路径和个人笔记，是否对外共享由你决定。

记录操作使用跨进程锁，等待超过 10 秒时报告忙碌。界面提交会携带预览校验值；快照或 Git HEAD 已变化时拒绝提交，需要重新预览。CLI 可将 `records preview` 返回的 `preview_token` 通过 `records commit --preview-token <值> -m <说明>` 传回以启用同样的校验；省略时表示提交当次生成的最新快照。Git 超时会给出检查状态/历史的提示，不自动重试提交。

records status 只检查 Git，不生成快照，也不依赖索引数据库。Git 已提交但 SQLite 活动日志失败时仍返回 committed=true 和警告，避免误导用户重复提交。CLI、HTTP 和 MCP 的预期运行错误包含 code、retryable、outcome、recovery；写请求通信中断时应先确认状态，程序不会自动重发。

## 检查与评测

来源界面可手动或定时检测变化，并选择自动增量刷新；记录界面可下载整理快照、预览导入、处理冲突及迁移路径。见 [来源检测与备份恢复](docs/SOURCES_AND_RESTORE.md)。CLI 示例：

```powershell
python -m sklib sources check --verify
python -m sklib sources watch --interval 60 --refresh
python -m sklib records snapshot --output E:\backups\sklib-records.json
python -m sklib records import E:\backups\sklib-records.json
# 核对预览后再应用；目标变化时拒绝旧令牌。
python -m sklib records import E:\backups\sklib-records.json --apply --preview-token <预览值>
```

```powershell
python -m unittest discover -s tests -p test_library.py -v
python -m unittest discover -s tests -p test_review_regressions.py -v
python -m unittest discover -s tests -p test_compatibility.py -v
python -m unittest discover -s tests -p test_sorting_recovery.py -v
python -m unittest discover -s tests -p test_system_audit.py -v
python -m unittest discover -s tests -p test_scan_jobs.py -v
python -m unittest discover -s tests -p test_classification_drafts.py -v
python -m unittest discover -s tests -p test_retrieval_quality.py -v
python -m unittest discover -s tests -p test_sources_restore.py -v
python -m unittest discover -s tests -p test_connection_templates.py -v
node --check sklib/static/app.js

# 可选真实浏览器检查；需已有 Playwright 和 Chromium/Edge，不自动安装。
python -m unittest discover -s tests -p test_browser.py -v
python -m unittest discover -s tests -p test_management_browser.py -v

# 在临时状态库中检查选定真实来源，不留索引或常驻服务。
python scripts/check_local_corpus.py E:\aimodel\anthropic-skills E:\aimodel\vue-skills-full

# 真实标注任务：relevant 为预期技能名或稳定 ID。
python -m sklib eval examples/evaluation.json --k 5
python -m sklib eval examples/evaluation-expanded.json --k 5
python -m sklib eval examples/evaluation-constrained.json --k 5
python -m sklib eval examples/evaluation-workflows.json --k 3

# 为技术名增加明确约束，多个 --require-term 都必须匹配。
python -m sklib search "Vue rendering performance" --require-term Vue --json

# 临时合成库的性能与并发检查；不调用模型。
python scripts/audit_performance.py --entries 5000 --repetitions 20
python scripts/audit_semantic.py --entries 3000 --dimension 256
# 可选官方 MCP Python SDK v1 的实际 stdio 检查；SDK 另行准备。
python scripts/check_mcp_client.py --sdk-path .audit-client
```

评测输出 Hit@K、MRR@K、Recall@K、Precision@K、负例误命中率、P95 查询耗时和每条任务的实际候选。`relevant` 可填技能名、文档标题或稳定 ID，空数组表示预期没有相关资料。正例可用 `evidence_contains` 单独衡量正文摘录是否包含标注短语。可用 `--mode semantic/hybrid --model <本机已有模型>` 比较检索模式。工作流样例需先索引 SKLIB 的 `docs/`（启用 `--include-docs`）与 Superpowers 的 `skills/`，其余样例所需来源见 [检索复查](docs/RETRIEVAL_REVIEW.md)。不存在的预期项计为失败。Precision 以标注范围为准。

界面“必含词”、CLI `--require-term` 和 MCP `search_skills.required_terms` 共用检索约束，最多 8 个词，全部需在索引中匹配。用它明确指定技术名，可以减少通用任务词带来的误命中。实测、指标解释和扩展边界见 [检索复查](docs/RETRIEVAL_REVIEW.md)。

设计与参考资料见 [docs/DESIGN.md](docs/DESIGN.md)，验证范围与结果见 [docs/VALIDATION.md](docs/VALIDATION.md)。Codex 宿主工具调用和真实向量样本已验证；Codex 模型驱动会话超时、Claude 按用户选择待登录、Gemini/VS Code 尚未完成宿主模型会话验收，详见 [宿主与模型验收](docs/HOST_AND_MODEL_ACCEPTANCE.md)。可检索不等同于技能必然可执行。
