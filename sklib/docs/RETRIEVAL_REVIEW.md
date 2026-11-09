# 检索复查与扩展

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
