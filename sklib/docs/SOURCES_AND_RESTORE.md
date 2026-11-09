# 来源检测、备份恢复与路径迁移

这些功能沿用原 SQLite 索引、注释和后台任务机制，不改变来源文件的位置，不执行来源脚本，也不自动注册快照中的目录。界面入口分别位于“资料来源”和“记录与版本”。

## 来源变动检测

界面点击“立即检测”，或启用“定时检测”。默认关闭；间隔为 30..86400 秒，设置在本次服务运行期间保留，刷新页面仍可查看，服务重启后关闭。可再启用“变化后自动刷新索引”，通过原后台队列逐个增量刷新。

检测复用索引器的类型识别、排除目录、文档收录和深度/文件数量上限。范围是能收录的 SKILL.md、项目清单、README 和已启用的文档；配套代码等资源在读取时取当前文件，不逐个建立独立索引。普通检测比较大小、修改时间和类型；内容校验可以发现大小和时间戳都未变化的修改：

```powershell
.\.venv\Scripts\python.exe -m sklib sources check
.\.venv\Scripts\python.exe -m sklib sources check --root E:\materials --verify
.\.venv\Scripts\python.exe -m sklib sources watch --interval 60
.\.venv\Scripts\python.exe -m sklib sources watch --interval 60 --refresh
```

| state | 含义 | 处理 |
|---|---|---|
| clean | 在本次检查范围内未检测到变化 | 不需要据此重扫；普通检查不保证发现同大小同时间戳的修改 |
| changed | 发现新增、修改、删除，或解析器/上次扫描状态需要刷新 | 手动刷新，或由已启用的自动刷新创建后台任务 |
| attention | 根目录不可用、权限、链接、深度/数量上限或并发变化导致检查不完整 | 阅读 failures；不把未见文件当作已删除，不自动刷新 |

返回完整计数和有限 changes/failures 明细。CLI 检查不完整时退出 3；MCP 的新增只读 `check_source` 接受 root、verify、max_changes，完整性由 complete/state 表示。未知来源返回 source_not_found。来源在检查期间被重扫/移除时标记 stale，自动任务还会核对来源版本，拒绝恢复已经移除的来源。

自动刷新对同一份磁盘变化只尝试一次；失败、部分完成或接受结果未确认时，不会在每次检测中反复入队。修正文件产生新变化后可再次自动刷新，也可以手动刷新。同一来源已有活动扫描或队列已满时显示原因。关闭定时检测不会撤销已入队的扫描，可在任务列表取消。

CLI watch 的 Ctrl+C 退出码为 130；已经完成的刷新保留，返回 partial 与已完成刷新次数，不回滚之前的轮次。文件系统调用只能在安全检查点取消，不承诺立即中断阻塞的系统 I/O。

## 整理快照备份

界面“下载整理快照”生成 UTF-8 JSON，包含来源定位、标签、笔记、收藏、状态和孤立注释，不包含源码正文、SQLite 文件或向量。尚未保存的浏览器草稿应另行从草稿箱导出。

CLI 建议直接写文件，避免旧版 PowerShell 重定向把原 UTF-8 输出改为 UTF-16：

```powershell
.\.venv\Scripts\python.exe -m sklib records snapshot --output E:\backups\sklib-records.json
.\.venv\Scripts\python.exe -m sklib records snapshot --annotated-only --output E:\backups\notes.json
.\.venv\Scripts\python.exe -m sklib records snapshot --root E:\materials --output E:\backups\materials.json
.\.venv\Scripts\python.exe -m sklib records snapshot --offset 0 --limit 1000 --output E:\backups\part-1.json
```

默认导出全部记录；显式分页时 selection 提供 total、returned、next_offset，可继续导出后续批次。输出必须是索引来源之外的 .json 文件。写入经过同目录临时文件、flush/fsync 和原子替换，替换前失败保留旧备份。

单次导入最多 16 MiB、20000 条记录。大库可按来源、已整理记录或 offset/limit 分批导出；不要为满足大小上限删除原数据。CLI 导入支持 UTF-8 及带 BOM 的 UTF-16/UTF-32；界面支持 UTF-8/UTF-16。UTF-32 文件可使用 CLI 导入。

## 导入与冲突处理

先扫描目标资料，再选快照、指定来源映射和冲突策略，点击预览。每页显示 20 项，可继续查看更多；CLI 可调整 offset/limit。预览会展示原位置、目标、当前值、导入值和最终动作。每条冲突可以选择保留/覆盖，也可以搜索并指定另一个目标条目。

匹配顺序为显式条目映射、根目录映射后的相对路径、稳定 ID/原路径；启用内容匹配后，还可匹配唯一的相同内容。资料类型必须一致。多个同内容目标不会任意选一个；未匹配的非空记录作为原 ID 的孤立注释保存，可指定目标或待同路径重新收录后恢复关联。

默认 keep 保留已有记录，即使已有值为空也不擅自覆盖。replace 使用导入值，包含以快照中的空值清空当前字段；应在预览中核对。多个源记录映射到一个目标、重复 ID、越界相对路径、错误字段类型和不支持的 schema 在写入前被拒绝。

```powershell
# 先预览，复制返回的 preview_token。
.\.venv\Scripts\python.exe -m sklib records import E:\backups\sklib-records.json
.\.venv\Scripts\python.exe -m sklib records import E:\backups\sklib-records.json --apply --preview-token <预览值>
```

可选 --root-map 指向旧根目录→已登记新根目录的 JSON 文件，--entry-map 指向源 ID→目标 ID，--resolutions 指向源 ID→keep/replace。例如：

```json
{"D:\\old-materials":"E:\\materials"}
```

全量计划共享同一个预览校验值，不因翻页改变。目标条目版本、整理记录、匹配结果或导入选择发生变化后，应用会返回 restore_preview_stale，要求重新预览。注释、全文索引和活动事件在一个写事务中更新，任一失败全部回滚。

发送后响应丢失时保留文件、映射和处理选择，消耗旧预览令牌，不自动重发；重新预览可以确认哪些值已保存。导入后原浏览器草稿继续保留，旧版本草稿保存时走已有冲突处理。

## 路径迁移

原、新来源都还登记在索引时，可在界面选择两者并预览，或：

```powershell
.\.venv\Scripts\python.exe -m sklib records migrate D:\old-materials E:\materials
.\.venv\Scripts\python.exe -m sklib records migrate D:\old-materials E:\materials --apply --preview-token <预览值>
```

这是整理记录的复制关联，原注释保留，源文件不移动。相对路径不同可使用 --match-content 或 --entry-map。原来源已经移出索引时，其孤立注释仍保留，但原路径信息可能不足；此时使用移除前的快照/catalog.json，或为孤立 ID 指定目标。程序不会按名称猜测并删除原记录。

导入/迁移不自动提交 Git。需要记录版本时，使用原来的预览和提交入口。浏览器草稿与正式记录的区别见 [BATCH_AND_DRAFTS.md](BATCH_AND_DRAFTS.md)。
