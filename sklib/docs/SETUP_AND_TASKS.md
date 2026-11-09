# 独立环境安装与后台扫描

本工作区已在 `E:/aimodel/sklib/.venv` 安装开发版，使用 Python 3.10.0。运行依赖是 PyYAML 6.0.3 和 tomli 2.5.0，pip check 通过；Python 3.10 的 TOML 清单解析已可用。没有修改全局 Python、PATH、模型配置或 Agent 配置。复现版本见 [constraints.txt](../constraints.txt)。

## 使用已安装的程序

```powershell
cd E:\aimodel\sklib
.\.venv\Scripts\sklib.exe --home E:\aimodel\sklib\.sklib doctor
.\.venv\Scripts\sklib.exe --home E:\aimodel\sklib\.sklib ui --port 8765
```

打开程序打印的本机地址，在“资料来源”输入目录并开始扫描。扫描由服务进程执行，关闭浏览器标签不停止任务；Ctrl+C 停止服务。服务不会自行开机启动或下载模型。这里没有预先为整个收藏目录建立正式索引，第一次使用时选择需要的来源即可。

doctor 检查解释器、隔离环境、依赖、SQLite FTS5/JSON 能力，并输出当前解释器对应的 MCP 启动参数。它不会创建空索引。已有资料库可加 `--check-index`，以只读方式检查现有索引及 schema 版本。环境可用返回 0，需要处理失败项返回 2。没有 Git 时提示记录功能缺失，词法检索仍可用。

新机器或重新创建环境时：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install -c constraints.txt -e .
.\.venv\Scripts\sklib.exe doctor
```

旧 Python 3.10 自带的 pip 21.2.3 不支持本项目的 pyproject 开发安装，应先更新隔离环境内的安装工具。移动项目后需要重新创建虚拟环境，调整 MCP 配置中的路径。

## 后台任务的行为

手动界面的扫描现在加入后台队列，显示扫描阶段、已检查文件数和索引处理数。发现阶段的总量未知，进度条保持不定长；建立索引阶段才按候选数显示进度。刷新页面会从服务重新读取任务记录，不依赖浏览器内存。

每个状态目录由一个后台 worker 串行执行任务，最多 10 个未结束任务，同一来源不重复入队。最近 200 个已结束任务保留在状态目录的 jobs.sqlite3，界面/API 列出最近 30 个。同一状态目录的其他 UI 实例仍可检索，但后台任务入口会提示使用原服务。

| 状态 | 含义与下一步 |
|---|---|
| queued | 尚未执行，可直接取消 |
| running | 正在发现文件或建立索引，可请求取消并继续检索 |
| cancelling | 取消信号已发出，等待安全检查点；磁盘或 Git 调用不会被强行终止 |
| succeeded | 已完整提交索引，以 report 为准 |
| partial | 已提交可读部分，保留未确认缺失的旧记录；查看来源失败明细后修正重扫 |
| cancelled | 本轮未提交的索引已回滚，已有资料和注释保留 |
| failed | 查看 error.code 和 recovery；任务结束不会阻止下一项任务 |
| interrupted | 服务重启时发现上轮结果未记录；先核对来源最近扫描报告，需要时手动重扫 |

取消在逐目录、逐文件、逐索引条目及提交前检查；事务中的修改统一回滚。若取消请求晚于实际提交，则保留 succeeded/partial 及真实报告，并显示取消请求晚于提交。排队之后来源被移除或另行扫描，旧任务会因 source_conflict 拒绝执行，避免把已移除来源重新加回来。

任务日志使用独立数据库，避免索引写事务挡住状态查询和取消。日志启动失败时已有资料检索仍可使用，后台扫描显示不可用。若索引已提交但最终任务记录写入失败，本进程保留实际成功结果并给出 status_warning；重启后无法确认的记录标为 interrupted，不能据此自动重复扫描。不要删除锁文件或数据库来“解锁”。

任务历史不会自动恢复执行。服务正常停止时请求取消已有任务；异常退出后的结果需要核对。关闭网页不等于停止服务，也不等于取消任务。

## 本机 HTTP 接口

这些是手动界面 API，不是 HTTP MCP。写请求继续要求当前服务的本机会话令牌和来源校验。

| 接口 | 行为 |
|---|---|
| POST /api/index-jobs | root 加扫描选项，创建任务并返回 id/state；可传 request_id |
| GET /api/index-jobs | 列出最近任务、进度、报告和恢复建议 |
| GET /api/index-job?id=... | 查询一个任务 |
| POST /api/index-jobs/cancel | 传入 id 请求取消；已结束任务直接返回现有结果 |

request_id 允许 1..80 个字母、数字、下划线或连字符。同一 request_id 和相同参数返回原任务，即使已经完成；同一 key 改变参数会拒绝。界面收到响应丢失时查询已有任务，不自动重发创建请求。确需新扫描时使用新的 request_id。原来的同步 POST /api/index 保留，CLI 索引仍同步执行并支持进度和 Ctrl+C。

## Agent 与打包检查

[Codex](../examples/mcp/codex.toml)、[Claude Code](../examples/mcp/claude.json)、[Gemini CLI](../examples/mcp/gemini.json) 样例已改用本工作区的 .venv 解释器与已安装模块，不依赖 cwd。所有入口使用同一个绝对 --home。样例仅保存在项目内，没有改动用户客户端配置。

官方 MCP SDK 已用已安装模块从临时工作目录验证四个只读工具，结果见 [mcp-installed-check.json](mcp-installed-check.json)。MCP 仍只提供检索和读取，不暴露后台扫描写操作。

构建产物是 `dist/sklib_local-0.1.0-py3-none-any.whl`。检查脚本将 wheel 安装到临时目录，确认实际导入 wheel 中的模块，并验证静态界面、TOML 项目索引与 doctor。它使用已有运行依赖，不做全局安装，结果见 [package-check.json](package-check.json)。

```powershell
.\.venv\Scripts\python.exe -m pip wheel --no-deps --no-build-isolation --wheel-dir dist .
.\.venv\Scripts\python.exe scripts/check_package.py dist/sklib_local-0.1.0-py3-none-any.whl
.\.venv\Scripts\python.exe scripts/check_mcp_client.py --sdk-path .audit-client --installed
```

后续已实现批量标签/状态/收藏与浏览器持久化草稿，见 [BATCH_AND_DRAFTS.md](BATCH_AND_DRAFTS.md)。任务记录保存在状态目录，笔记草稿保存在当前浏览器；草稿需正式保存后才进入资料库和 Git 记录。各客户端的实际模型会话验收与真实嵌入效果评测仍未完成。
