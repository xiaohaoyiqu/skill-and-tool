# 实现设计与参考依据

## 目标与边界

面向本机资料收藏的能力发现服务。输入是本地 Skill 目录和项目文档，输出是候选、原文依据和后续读取入口。索引、注释和版本记录独立于来源目录。当前开发不安装全局集成、不修改第三方仓库、不启动常驻服务。

## 模块与扩展点

| 模块 | 职责 |
|---|---|
| `indexer.py` | 有界文件发现、宽容元数据解析、Git 来源、增量索引与安全清理 |
| `files.py` / `projects.py` | 静态程序类型识别、清单解析、文件能力分类、严格编码与物理换行 |
| `catalog.py` / `failures.py` | 无关键词分拣队列、共用筛选、错误码、结果状态与恢复提示 |
| `storage.py` | SQLite/WAL、表结构版本、事务与连接生命周期 |
| `text.py` | 中英分词、显式查询扩展、哈希归一化、证据片段 |
| `service.py` | 检索、排序、副本分组、完整加载、资源读取、注释与快照 |
| `semantic.py` | 可选本地嵌入与增量向量存储；提供 `encode/pack/similarity/model` 的后端可替换 |
| `mcp.py` | 四个读取工具，严格输入校验、有界 JSON-RPC stdio 帧 |
| `web.py` / `static/` | 同源本地界面；显式写操作需会话令牌 |
| `records.py` | 原子导出记录、独立 Git 仓库、预览与显式提交 |
| `evaluation.py` | 任务标注检索指标，逐任务输出命中与失败 |

文档 ID 是规范化根路径与相对路径的哈希，不以 `name` 作为主键。位置身份和内容身份分开；内容相同的多个位置可折叠但不删除。注释随位置 ID 保留，即使暂时移除来源，也可在同路径重新收录后恢复。跨机器路径重定位与注释导入尚未实现。

每个来源在 meta 中维护操作版本。扫描开始读取版本，数据库写事务内再核对，变化时拒绝旧扫描写回；来源移除也推进版本。同次检索的多路召回及正文读取使用同一 WAL 读快照。导出包括暂时无来源条目的注释，避免来源管理操作让 Git 记录丢掉笔记。

词法索引存入预分词文本，SQLite FTS5 unicode61/BM25 负责候选排名。中文使用单字与双字片段，查询避免长句大量单字造成泛匹配。原始词与显式扩展词分别召回，经 RRF 合并并加上有界的名称/描述覆盖加分。返回分数只用于本次相对排序。

FTS 行号绑定到 documents 的 SQLite rowid，刷新与删除直接按行定位，避免每个条目都按 UNINDEXED 文本 ID 全表查找。数据库 schema 为 2；早期开发缓存 schema 1 不自动打开。目录扫描使用 lstat 识别 Windows reparse point/POSIX 链接，从已解析的根逐级排除链接，避免对每个候选重复解析整条祖先路径。读取接口仍对请求资源单独核对真实路径。

可选混合检索将语义候选加入融合。语义模式单独可选，用于比较两条检索路径；不宣称混合一定更好。向量建库在网络调用期间不持有数据库事务，写入前重新验证文档版本。词法检索默认不发送网络请求。

纯语义模式不叠加名称或关键词覆盖加分。记录导出/预览/提交/日志使用 OS 跨进程锁；预览值绑定快照内容与 Git HEAD，界面提交必须携带该值。该锁协调应用自身操作，不替代 Git 对外部命令的锁机制。

## 规范、项目、讨论和论文

下列资料用于设计与检查，未复制第三方实现。

1. [Agent Skills 接入指南](https://agentskills.io/client-implementation/adding-skills-support)：渐进加载、技能完整指令、引用资源、同名冲突和宽容解析。对应 search → get → read 三步接口。
2. [Agent Skills 格式规范](https://agentskills.io/specification)：`SKILL.md`、name/description、可选 scripts/references/assets。对应目录包模型、资源清单与警告。
3. [MCP 工具规范 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)、[生命周期](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)、[stdio 传输](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)：初始化、工具 schema、结果、错误和 stdout 约束。当前仅声明实现的 stdio 工具子集。
4. [SQLite FTS5](https://www.sqlite.org/fts5.html)：字段加权 BM25、分词与 MATCH 语法。预分词兼容本机 SQLite 3.35，不要求较新版本的 trigram；用户字符串不会直接成为 MATCH 操作符。
5. [zvec-grep](https://github.com/zvec-ai/zvec-grep) 与本地 `E:/aimodel/zvec-grep/docs/05-architecture.md`：共用检索核心、CLI/MCP 入口、精确/语义路径、有来源的紧凑结果。当前未启用其守护进程或修改其配置。
6. [QMD](https://github.com/tobi/qmd)：search/get 分离、JSON 输出、MCP、混合检索与评测参考。当前没有复制其依赖或宣称已复现其质量。
7. 本地 `skills-compat-manager/README.zh-CN.md`：技能 search/get 与依赖信息组织。其历史客户端能力表未作为当前事实采用。
8. [Vercel Skills #455](https://github.com/vercel-labs/skills/issues/455)：用户对更新覆盖本地内容的讨论。对应来源只读、个人记录与原文件分离；此 issue 不能证明所有当前版本都有相同行为。
9. [Skills Manager 更新日志](https://github.com/xingkongliang/skills-manager/blob/main/CHANGELOG.md)：副本重复计数、CRLF/LF 误报、检查失败误报更新等维护案例。对应内容归一化、位置/内容身份分离、未知与失败状态保留。
10. [BEIR，NeurIPS 2021](https://arxiv.org/abs/2104.08663)：跨任务评测中 BM25 是稳健基线，复杂检索器存在质量与计算代价权衡。对应先测词法基线，再测语义收益。
11. [Cormack 等，RRF，SIGIR 2009](https://research.google/pubs/reciprocal-rank-fusion-outperforms-condorcet-and-individual-rank-learning-methods/)：使用排名融合而不直接相加不同来源的不可比原始分数。当前 k=60，质量需本地任务集确认。
12. [The Fusion Tax，2026 预印本](https://arxiv.org/abs/2610.30612)：报告混合排序可能伤害部分查询。作为补充研究线索，不能替代本项目实测或视作普遍结论；因此保留独立 lexical/semantic/hybrid 模式。

## 检查重点

- 真实 CLI 子进程和 MCP stdio 帧：初始化、四个工具定义、工具调用、错误输入、通知无响应、坏帧恢复。
- 临时来源：中英任务、同名异内容、相同内容副本、注释、删除/恢复、扫描失败不误删、同大小/时间戳强制验证。
- 文件读取：版本变化、完整正文、分页、长行预算、Windows 路径及父目录逃逸、非技能记录不能借机读取整个项目。
- Git fixture：只提交 catalog，保留其他已暂存文件，无变化不创建提交，备注进入版本历史。
- HTTP 与浏览器：来源/Host 校验、写会话令牌、前端原文使用 textContent、完整搜索→资源→笔记→Git 链路和窄屏布局。
- 语义：可替换后端的增量与过期向量排除；Ollama 协议用本地测试服务验证。未下载真实模型或声明真实语义质量。

## 后续演进约束

项目和文件兼容性已扩展为独立模块，范围及格式依据见 [COMPATIBILITY.md](COMPATIBILITY.md)。项目清单只读取静态信息，不执行其脚本或动态配置；项目资料不会因为清单模板相同而跨目录折叠。检索、CLI、MCP、HTTP 与界面共用程序类型枚举。

来源报告保存文档范围、扫描预算、额外排除和编码设置，省略选项时重用；Git 快照包含这些设置。单条索引记录保存其解码设置，编码变更导致的读取失败不能因文件 stat 未变而被下一次扫描误认为成功。解析器能力签名改变时也会重读，覆盖 Python 3.10 后补 TOML 依赖的情况。

增加新资料解析器需保留原始来源与证据位置；增加嵌入后端需显式配置数据流向与模型版本；更换排序需用标注任务集比较；实际客户端接入需逐个验证配置位置与能力。自动更新来源、执行脚本、远程发布、跨机器同步和常驻进程均不在当前默认行为内。
