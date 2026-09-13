# 多仓库拉取、整理与查看

本目录是第三方 Skill、工具和资料仓库的本地集合；根聚合仓库只跟踪索引、说明和维护脚本，不重复上传第三方仓库工作树。

## 推荐组合

| 需求 | 工具 | 结论 |
|------|------|------|
| 批量检查和更新一级 Git 仓库 | [`scripts/Sync-RepositoryCatalog.ps1`](scripts/Sync-RepositoryCatalog.ps1) | 为当前目录定制；默认只读检查，显式 `-Pull` 才执行 `git pull --ff-only --prune`，自动跳过本地修改和无 upstream 的仓库，不写全局 Git 配置 |
| 精确查找文件、路径和文本 | `rg` / `rg --files` | 零索引、结果可直接定位；已知关键词时优先使用 |
| 不知道原文或位置时做语义检索 | [zvec-ai/zvec-grep](https://github.com/zvec-ai/zvec-grep) | ripgrep、BM25 和向量检索统一入口，支持 Codex MCP；安装会修改 Codex 配置，本目录当前只保存源码 |
| 理解跨文件关系、调用路径和架构 | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 将代码、文档和媒体转换为持久知识图谱；适合关系问题，不替代精确全文搜索 |
| 统一执行多仓库自定义命令 | [alajmo/mani](https://github.com/alajmo/mani) | Go 编写的多仓库 CLI，适合已有项目清单和重复命令；当前自定义脚本已覆盖安全同步，因此暂不重复克隆 |
| 批量克隆组织或用户的仓库 | [gabrie30/ghorg](https://github.com/gabrie30/ghorg) | 适合 GitHub/GitLab/Bitbucket 组织级镜像或备份；本目录来源分散，日常更新并不需要它 |

## 运行时升级与可观测性

本目录没有安装 OpenTelemetry Java Agent、OpenTelemetry Collector、HBase 或 ClickHouse。需要评估 Java/Spring 升级、Java Agent 或新数据存储时，先阅读 `SKILLS_INDEX.md` 的“Java 升级、可观测性与数据存储路由”，再在目标项目的隔离环境完成兼容、性能、敏感数据、恢复和回滚验证。

`gortex` 和 Graphify 能辅助定位跨模块影响，但建立索引或启动守护进程会写入本机状态，必须另行批准。浏览器工具只提供运行证据，不读取已有浏览器会话，也不能证明服务端授权或数据一致性。

## 使用同步脚本

只检查，不访问远程：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Sync-RepositoryCatalog.ps1
```

更新所有干净且有 upstream 的一级仓库，并保存 JSON 结果：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Sync-RepositoryCatalog.ps1 `
  -Pull `
  -JsonPath .\repository-sync.json
```

脚本只扫描 `E:\aimodel` 的直接子目录；默认不进入隐藏目录，也不递归更新子模块或嵌套仓库。失败、分叉和本地修改只记录，不自动 merge、rebase、reset、stash 或覆盖。

## 查看目录的建议顺序

1. 在 [`REPOSITORIES.md`](REPOSITORIES.md) 查看一级仓库来源、分支、HEAD 和同步状态。
2. 在 [`SKILLS_INDEX.md`](SKILLS_INDEX.md) 按能力查找正式 Skill、工具与研究资料。
3. 已知名称、路径或字面文本时使用 `rg`；语义不明确时再考虑 zvec-grep。
4. 需要回答调用链、模块关系、社区结构等问题时，为目标仓库生成 Graphify 图谱。

## 边界

- `zvec-grep`、Graphify、mani 和 ghorg 都是可选工具；保存源码不代表已经安装或授权修改全局配置。
- 批量更新只允许 fast-forward。出现本地修改或分叉时应单独审查，不能为了“同步”而重置用户内容。
- Terraform 等第三方仓库可能采用非宽松许可证；聚合目录只记录上游和本地版本，不改变原项目许可。
