# 检索复查与扩展

## 工作流查询与原文证据复查（2026-11-11）

- “完成前验证”“提交前验证”“系统化调试”“测试驱动开发”扩展为相应英文技能名。扩展把技能名作为完整的 FTS 短语，并通过 `expanded_terms` 返回。
- 中英混合查询显式选 `document`、且包含至少三个长度不小于 3 的 ASCII 检索词时，词法候选要求这些词同时命中。短查询保留原行为，允许资料库名仅作为上下文。三词门槛来自本地开发对照，两个词就收紧会漏掉已有 MCP 验收记录。混合模式的向量候选仍按其原有规则筛选，跨模式字面限制继续使用 `required_terms`。
- Markdown 摘录合并当前标题与候选行的检索词覆盖，同等覆盖优先正文。忽略独占一行的空 HTML 锚点，围栏内的 `#` 按代码原文处理。摘录仍来自单条物理行，保留 `line` 和行内 `match_count`。标题参与选段时返回 `evidence.heading`，较紧的结果预算可以省略标题。
- `eval` 增加文档标题匹配及 `returned_titles`。正例可写 `evidence_contains`，同一相关结果的正文摘录须包含全部标注短语才计入 `evidence_hit_at_k`，按 Unicode 归一化和大小写折叠比较。只用有摘要标注的案例计算此指标。

前后对照共用一个隔离词法索引，收录 SKLIB 文档、Superpowers 技能和 QQBot 独立文档，共 49 份文档、1 个项目说明、14 个技能。`K=3`，相同标注和评测器运行原版与更新版。

| 样例 | 正例命中 | 正确正文证据 | 负例误命中 |
|---|---:|---:|---:|
| 12 条公开工作流样例 | 6/9 → 9/9 | 1/3 → 1/3 | 3/3 → 1/3 |
| 6 条本机项目任务 | 4/4 → 4/4 | 2/4 → 3/4 | 2/2 → 0/2 |

当前样本用于开发回归。公开样例仍有一条未知技能名因通用词命中，两条工作流与一条项目查询的摘录仍未覆盖标注句。用 `sklib eval examples/evaluation-workflows.json --k 3` 可在已登记 SKLIB `docs/` 和 Superpowers `skills/` 的资料库复现公开样例，排名会随资料范围变化。

SQLite FTS5 的短语及布尔匹配用于限制词法候选。Markdown 行识别参考 CommonMark 的 ATX 标题与围栏规则，并参考 QMD 以文档结构选择边界的做法。中英检索文献讨论了逐词翻译的歧义，因而本轮采用可审阅的任务短语扩展。BEIR 的跨数据集结果支持保留 BM25 作为对照，本机结果以实际任务标注为准。 [SQLite FTS5](https://www.sqlite.org/fts5.html#fts5_boolean_operators) · [CommonMark](https://spec.commonmark.org/0.31.2/#fenced-code-blocks) · [QMD](https://github.com/tobi/qmd#smart-chunking) · [中英跨语言检索](https://aclanthology.org/W00-1313/) · [BEIR](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html)

Agent 搜索后继续通过 `get_skill` 与资源读取接口获取完整内容。 [Agent Skills 渐进加载](https://agentskills.io/client-implementation/adding-skills-support)

## 前一轮检索复查

本轮沿用 SQLite、CLI、stdio MCP 和本地界面的架构，处理检索资源消耗、误命中检查及 Windows 请求断连问题，没有增加运行依赖或修改数据库格式。

## Agent 和手动检索的必含词

普通检索允许多个关键词中的部分命中。实际发现，`Flutter mobile application performance optimization` 会因通用性能词返回数据分析技能；`Elixir OTP 监督树容错` 会因只匹配 OTP 返回其他条目。排名分数不是适用概率。

新增可选 `required_terms`：每个指定词的字面分词都必须出现在索引中，不做同义词扩展。词法、语义和混合模式都先应用这个条件，再按各自规则排序。可匹配名称、描述、正文或个人标签/笔记；匹配本身仍不代表技能一定适用，需要读取证据和完整说明。

- 最多 8 个词，每个 1..80 字符；空白、无可检索字符、错误类型和超限会返回输入错误。
- 大小写和全角字符按现有规则归一化。多个词为 AND 关系，不接受用户提供的 FTS 布尔表达式。
- 界面新增“必含词”，用英文或中文逗号分隔；也可以只填必含词检索。清空关键词和必含词后进入分拣浏览。
- 返回空结果后，核对词语、筛选条件及来源扫描状态。空结果不代表整个磁盘上不存在资料。

CLI 示例，使用项目内解释器：

```powershell
.\.venv\Scripts\python.exe -m sklib search "Vue rendering performance" --require-term Vue --json
.\.venv\Scripts\python.exe -m sklib search "Elixir OTP 监督树容错" --require-term Elixir --require-term OTP --json
```

MCP `search_skills` 示例：

```json
{"query":"Flutter mobile application performance optimization","required_terms":["Flutter"],"limit":5}
```

参数使用已有 JSON Schema 类型，保留四种已支持协议的工具调用方式。官方 MCP SDK 1.30.0 已验证约束、非法值后的恢复、正文分页和文本/结构化结果一致；各宿主的实际权限及模型选词行为还需分别验收。

## 评测扩展

原 `examples/evaluation.json` 仍可使用。案例 `relevant` 为预期名称或 ID；显式空数组 `[]` 表示预期没有相关资料，`required_terms` 可选。整个文件在发出任何查询前校验，最多 1000 案例、文件 2 MiB。

```json
[
  {"query":"PDF 表格提取","relevant":["pdf"]},
  {"query":"Flutter mobile performance","required_terms":["Flutter"],"relevant":[]}
]
```

```powershell
.\.venv\Scripts\python.exe -m sklib eval examples/evaluation-expanded.json --k 5
.\.venv\Scripts\python.exe -m sklib eval examples/evaluation-constrained.json --k 5
# 先为本机已有模型建立向量；不自动下载模型。
.\.venv\Scripts\python.exe -m sklib eval examples/evaluation-expanded.json --mode hybrid --model <本机已有模型>
```

| 字段 | 含义 |
|---|---|
| hit_at_k / mrr_at_k / recall_at_k | 只在正例上取均值，负例不混入分母 |
| precision_at_k | 正例命中的结果数 / K，再按案例取均值；少返回时仍以 K 为分母 |
| returned_precision | 正例命中的结果数 / 实际返回数，再取均值；空返回记 0 |
| false_positive_rate | 预期为空的案例中，返回任意候选的案例比例 |
| correct_empty_rate | 预期为空的案例中，实际返回空结果的比例 |
| budget_limited_queries | 字符预算使返回不足 K、但仍有下一页的案例数；逐条明细也标记 |
| p95_ms | 按 nearest-rank 取第 ceil(0.95 × 案例数) 个延迟 |

没有正例或负例时，对应指标为 `null`。明细保留预期项、实际名称/ID、约束、耗时和误命中状态。评测使用 100000 字符预算；检索失败仍返回错误，不能把未完成的评测当作通过。

两份扩展样例面向本机选定的五份来源，不适合直接用于任意资料库。正例标签是已知预期项，未穷尽其他同样相关的技能，因此 Precision 只能表示对这份标签的符合程度，不能当作整体相关性质量。

## 实际复核结果

来源为 anthropic-skills、vue-skills-full、Humanizer-zh、obsidian-skills、scientific-agent-skills。临时索引扫描 2880 个文件，收录 197 个技能和 6 个项目说明；各来源完整扫描两次，第二次全部识别为未变化。详情见 [retrieval-corpus-check.json](retrieval-corpus-check.json)。

| 9 条开发任务 | 普通查询 | 对负例显式指定技术名 |
|---|---:|---:|
| 正例数量 | 5 | 5 |
| Hit@5 / MRR@5 / Recall@5 | 1 / 1 / 1 | 1 / 1 / 1 |
| 负例误命中 | 2 / 4 | 0 / 4 |
| 按已知标签的 Precision@5 | 0.32 | 0.32 |

这是同一临时索引上的小样本复现。约束列由调用者显式提供，不表示普通查询自动拒绝无关任务；约束词缺失或来源只顺带提到技术名时仍需复核。测量期间有其他检查负载，不使用两列延迟差推算提速比例。

语义检索改为逐条读取向量，用有界堆保留候选，再加载候选元数据；纯语义模式省去额外的词法排名查询。所有符合条件的向量仍逐条验证，低分向量损坏也返回可恢复错误。同分按 ID 排序，候选、正文和筛选保持同一数据库快照。

同一临时索引、3000 条合成向量、每条 256 维，交替执行五次，基线为源码提交 `730df72`。使用固定合成嵌入，不调用模型：

| 测量 | 基线 | 优化后 |
|---|---:|---:|
| 查询中位耗时 | 199.76 ms | 157.55 ms |
| Python 峰值分配 | 13957869 bytes | 753674 bytes |
| 前五项 ID / 分数 | 对比一致 | 对比一致 |

峰值分配不含 SQLite、系统和模型内存。该结果不代表端到端模型延迟；算法仍遍历符合条件的全部向量，未实现近似向量索引。完整结果见 [semantic-performance.json](semantic-performance.json)。复现命令：

```powershell
# baseline-ref 会执行可信本地历史版本的 service.py，用于比较。
.\.venv\Scripts\python.exe scripts/audit_semantic.py --baseline-ref 730df72 --output docs/semantic-performance.json
.\.venv\Scripts\python.exe scripts/check_local_corpus.py E:\aimodel\anthropic-skills E:\aimodel\vue-skills-full E:\aimodel\Humanizer-zh E:\aimodel\obsidian-skills E:\aimodel\scientific-agent-skills --evaluation examples/evaluation-expanded.json --compare-evaluation examples/evaluation-constrained.json --output docs/retrieval-corpus-check.json
```

## 稳定性与扩展边界

浏览器检查发现，Windows 快速切换筛选时，响应头和正文阶段都可能断连。HTTP 发送现在统一处理连接关闭和超时，结束当前连接，避免再次向断开的连接发送错误响应；不重新执行业务写入。故障注入覆盖响应头/正文阶段的断管、重置、中止和超时，触发该问题的真实浏览器流程复跑后无异常日志。

本轮验证：135 项非浏览器测试通过；新增检索的 17 项在 Python 3.12 通过；9 条 Edge 流程通过，断连修复后定向复跑通过；官方 MCP SDK 实际 stdio 与最终 wheel 安装检查通过。未运行真实模型推理或逐个宿主实装验收。

后续适合沿现有结构扩展的方向：来源变动检测与按来源增量刷新；整理快照导入及跨路径注释迁移的预览/冲突处理；更多人工判断的中英文任务集；各 Agent 宿主逐一实装及真实向量模型质量验收。来源自动更新、快照导入和迁移目前未实现。

以上为本轮结束时的后续清单；下一轮已补齐来源检测/自动刷新和快照恢复/迁移，见 [SOURCES_AND_RESTORE.md](SOURCES_AND_RESTORE.md)。宿主和真实向量模型的实际结果见 [HOST_AND_MODEL_ACCEPTANCE.md](HOST_AND_MODEL_ACCEPTANCE.md)。

实现参考：[Python 3.10 heapq](https://docs.python.org/3.10/library/heapq.html#heapq.nsmallest)、[SQLite FTS5 查询语法](https://www.sqlite.org/fts5.html#full_text_query_syntax)。
