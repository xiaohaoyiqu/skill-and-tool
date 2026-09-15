# GitHub 仓库下载与配置台账

**最后整理**: 2026-09-15
**目录**: E:\aimodel
**定位**: GitHub 下载与配置历史台账；当前 skill 更新状态以 [SKILLS_INDEX.md](SKILLS_INDEX.md) 为准
**状态**: 只记录克隆和配置，不自动安装依赖、不写入全局 Codex skills
**Star 手动清单**: [GITHUB_STAR_LIST.md](GITHUB_STAR_LIST.md)

---

## 2026-09-15 代码审查、下载工具与手绘风格候选

| 仓库 | 类型与用途 | 本地处理 | 判断与边界 |
|------|------------|----------|------------|
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | AI 代码审查 CLI、Codex/Claude/Cursor Skill 与 CI 集成 | 浅克隆到 `E:\aimodel\open-code-review\`，HEAD `55899906` | Apache-2.0；2 个逻辑 Skill（源码与插件目录各保留一份），适合本目录长期保存；未安装 `ocr`、未配置模型或执行审查 |
| [XiaoYouChR/Ghost-Downloader-3](https://github.com/XiaoYouChR/Ghost-Downloader-3) | Python/PySide6 多协议下载器，支持 HTTP、BT、FTP、流媒体、GitHub 与 Hugging Face | 浅克隆到 `E:\aimodel\Ghost-Downloader-3\`，HEAD `601e2068`；浏览器扩展子模块固定为 `b34a7677` | GPL-3.0；属于工具源码而非 Skill，适合作为下载器实现参考；未安装 Python 依赖、浏览器扩展或桌面程序 |
| [yang0/handraw-style](https://github.com/yang0/handraw-style) | 001–261 手绘风格图集与双语提示词 Skill | 仅登记；审查用临时浅克隆已移除 | 仓库未提供许可证文件，且仅 340 个跟踪文件的浅克隆已约 195.1 MiB，主要体量来自参考图片；不在本地长期镜像，使用前应先取得清晰授权 |

### 静态核验

- `open-code-review` 与 `Ghost-Downloader-3` 均为 `--depth 1` 浅克隆、工作树干净，并通过 `git fsck --no-reflogs`；本地占用分别约 18.4 MiB 和 29.5 MiB。
- `Ghost-Downloader-3` 的 `browser_extension/upstream` 已检出父仓库锁定的 `xifangczy/cat-catch@b34a7677`，没有擅自跟随子模块最新 `master`。
- 扫描同时发现此前仅登记的 `3b1b/manim` 已在根目录形成 `master@fafa083a` 浅克隆；本轮只补正台账，不改动该工作树。
- 本轮没有执行候选仓库代码、安装依赖、写入全局 Codex Skills、启动服务或向第三方仓库推送。

---

## 2026-09-14 UI 组件库、动效 Skill 与写作 Skill

| 仓库 | 类型与用途 | 本地处理 | 边界 |
|------|------------|----------|------|
| [swamimalode07/rare-ui](https://github.com/swamimalode07/rare-ui) | React / Next.js / Tailwind / Motion 的 shadcn 动效组件 registry | 浅克隆到 `E:\aimodel\rare-ui\`，HEAD `d146c352` | MIT；0 个 `SKILL.md`，通过 shadcn CLI 按组件引入 |
| [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | 可组合、可访问、源码可定制的 UI 组件与 registry 工具链 | 浅克隆到 `E:\aimodel\shadcn-ui\`，HEAD `2b3e6d4f` | MIT；含 `shadcn` 与 `migrate-radix-to-base` 两个 Skill，未全局安装 |
| [slev12397/beautiful-ui](https://github.com/slev12397/beautiful-ui) | `beautifului.dev` 的 AI-native React 界面 primitives 与 shadcn registry | 浅克隆到 `E:\aimodel\beautiful-ui\`，HEAD `ff0f74d6` | MIT；`SidebarNav` 使用安装时校验许可证的商业图标包，使用前应替换图标或配置合法授权 |
| [starc007/ui-components](https://github.com/starc007/ui-components) | `beui.dev` 的 React 19 / Tailwind 4 / Motion 组件库 | 浅克隆到 `E:\aimodel\beui\`，HEAD `8d3fa7b4` | 公开部分 MIT；含 `beui` 与 `beui-pro` Skill，Pro 需要客户 token，未访问付费 registry |
| [Jakubantalik/transitions.dev](https://github.com/Jakubantalik/transitions.dev) | CSS UI 动效、动效 token、Agent Skill 与 Refine 工具 | 浅克隆到 `E:\aimodel\transitions-dev\`，HEAD `598d3d6a` | 含 `transitions-dev`、`transitions-polish`、`refine-live` 3 个 Skill；公开工具代码为 MIT，下载的 Pro 配方另受站点条款约束 |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | 检测并编辑 20+ 类模板化 AI 写作模式 | 浅克隆到 `E:\aimodel\no-ai-slop\`，HEAD `000650b1` | MIT；含 1 个正式 Skill、eval 和 Codex 插件清单，未全局安装 |

### 仅登记、未克隆

| 仓库 | 判断 |
|------|------|
| [jbiaojerry/ebook-treasure-chest](https://github.com/jbiaojerry/ebook-treasure-chest) | 主要聚合第三方电子书下载链接，GitHub 页面未显示明确许可证；本目录只保存来源链接，不镜像内容，也不对链接内容的版权或可用性背书。 |
| [3b1b/manim](https://github.com/3b1b/manim) | 3Blue1Brown 的 ManimGL 数学讲解动画引擎，MIT；按要求只登记。它与更偏稳定、测试和社区支持的 Manim Community 版是不同项目，安装说明不能混用。 |

### 静态核验

- 6 个新增仓库均为 `main` 分支、`--depth 1` 浅克隆、干净工作树，无 `.gitmodules` 和 Git LFS 规则，并通过 `git fsck --no-reflogs`。
- 本地占用约为：Rare UI 24.8 MiB、shadcn/ui 62.6 MiB、Beautiful UI 1.3 MiB、beUI 10.5 MiB、Transitions.dev 44.6 MiB、No AI Slop 0.5 MiB，合计约 144.3 MiB。
- 本轮只保存源码和索引，没有执行仓库代码、安装 npm/bun/Python 依赖、启动 Refine 服务、访问 Pro registry，或写入全局 Codex skills。
- 搜索中另发现 `Kainiko943/beautiful-ui`，但 `beautifului.dev` 官网对应的是 `slev12397/beautiful-ui`，因此未克隆前者。

---

## 2026-09-05 全目录同步与多仓库维护工具

| 检查项 | 结果 |
|------|------|
| 可见一级 Git 仓库 | 92 |
| 实际 fast-forward | 43 |
| 原本已是最新 | 47 |
| 默认分支迁移 | 1（`codetracer`: `main` → `stable`） |
| 本地修改跳过 | 1（`reverse-skill`） |

### 处理说明

- 新增 [`scripts/Sync-RepositoryCatalog.ps1`](scripts/Sync-RepositoryCatalog.ps1)：默认只读检查；显式 `-Pull` 时只运行 `git pull --ff-only --prune`，自动跳过 dirty/no-upstream 仓库，使用命令级 `safe.directory` 而不污染全局 Git 配置，并可输出已脱敏的 JSON 结果。
- 新增 [`REPOSITORY_MANAGEMENT.md`](REPOSITORY_MANAGEMENT.md)，记录本目录的拉取、整理和查看组合：`rg` 做精确搜索，zvec-grep 做语义/BM25/向量检索，Graphify 做关系与调用路径图谱；mani 和 ghorg 仅列为特定场景候选，暂不重复克隆。
- 首轮发生 3 次 GitHub TLS `unexpected EOF`，改用 HTTP/1.1 重试后 `mergration`、`scientific-agent-skills`、`taste-skill` 全部成功；这三项没有遗留失败。
- `Awesome-Agent-Skills-for-Empirical-Research` 快进后，将 `skills/69-Paper-WorkFlow` 子模块更新到父仓库锁定的 `ca36e316`，最终工作树干净。
- `codetracer` 上游已删除 `main` 并将默认分支改为 `stable`。本地旧 `main` 相对共同祖先保有 3 个独有提交；本轮保留该分支，新建并切换到跟踪 `origin/stable` 的本地 `stable`（`0478cb4f`），同时刷新 origin HEAD 和全分支 fetch refspec。
- `reverse-skill` 的上游 `main` 发生强制更新；本地当前有 3 个修改文件，且为 ahead 1 / behind 142。为避免覆盖用户内容，本轮只 fetch 远程引用，没有 pull、stash、reset、merge 或 rebase。
- 其余仓库保持原克隆形态；76 个浅克隆没有被批量扩成完整历史。除父仓库明确锁定的 Paper-WorkFlow 外，不递归更新嵌套仓库或子模块。

---

## 2026-09-05 Graphify、zvec-grep、Terraform 与中国专利 Skill

| 仓库 | 类型 | 本地目录 | Skill / 使用结论 | 状态 |
|------|------|----------|------------------|------|
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 代码、文档和媒体知识图谱工具 / Agent Skill | `E:\aimodel\graphify\` | 1 个小写 `graphify/skill.md`；擅长关系、调用路径、社区和跨文件架构理解，与语义检索互补 | 既有浅克隆已补成完整历史并快进；未安装 Python 包或 Agent 集成 |
| [zvec-ai/zvec-grep](https://github.com/zvec-ai/zvec-grep) | 本地优先的 ripgrep + BM25 + 向量混合检索 CLI / MCP | `E:\aimodel\zvec-grep\` | 0 个 `SKILL.md`；可通过 `zg install --target codex` 配置 Codex MCP，适合大型代码与资料库的语义发现 | 已完整克隆；未安装 npm 包、模型、服务或 MCP |
| [hashicorp/terraform](https://github.com/hashicorp/terraform) | 基础设施即代码 CLI 核心源码 | `E:\aimodel\terraform\` | 0 个 `SKILL.md`；适合作为 Terraform Core 实现、状态/计划/资源图与插件协议参考，不含 providers | 已完整克隆；未构建、未安装 Go 或 Terraform CLI |
| [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) | 中国专利全流程 Agent Skill | `E:\aimodel\patent-disclosure-skill\` | 1 个可调用路由 Skill + 6 个内部子技能；覆盖交底、申请文件、著录检索、解读、审查答复和政策简报 | 已完整克隆；未装 Python/Playwright/CAD/OA 依赖，未写入全局 Codex skills |

### 克隆记录

| 仓库 | Origin | HEAD | 分支 / 完整历史 |
|------|--------|------|-----------------|
| graphify | https://github.com/Graphify-Labs/graphify.git | `937e59a5` | `v8`；非浅克隆，1862 个提交、13 个远程引用、202 个 tags |
| zvec-grep | https://github.com/zvec-ai/zvec-grep.git | `52653951` | `main`；非浅克隆，271 个提交、5 个远程引用、5 个 tags |
| terraform | https://github.com/hashicorp/terraform.git | `7b8c301b` | `main`；非浅克隆，44947 个提交、883 个远程引用、471 个 tags |
| patent-disclosure-skill | https://github.com/handsomestWei/patent-disclosure-skill.git | `a0156905` | `main`；非浅克隆，40 个提交、7 个远程引用、0 个 tags |

### 静态核查结论

- 四个仓库均为完整、非 partial/非 shallow clone，工作树干净并与各自 upstream 为 0/0；均无 Git submodule 和 Git LFS 跟踪项，并通过 `git fsck --full --no-reflogs`。本地总占用约为 Graphify 31 MiB、zvec-grep 58 MiB、Terraform 388 MiB、专利 Skill 18 MiB。
- Graphify 已从旧的单分支浅克隆补齐完整对象、所有远程分支和 tags，fetch refspec 也改为持续跟踪全部远程分支。当前版本 `0.9.54`，要求 Python `>=3.10`；本机 Python 3.10/3.12 满足要求，但未安装 `uv` 或 `graphifyy`。
- zvec-grep 当前版本 `0.2.1`，要求 Node.js `>=22`；本机 Node.js `25.2.1` 满足要求。它默认可本地保存文件、索引和模型，远程 embedding 需另行授权；安装器会写 Codex 配置和 `AGENTS.md`，因此本轮只保留源码。
- Terraform 的完整 Git pack 约 359 MiB，是本批最大仓库；保留完整历史适合源码考古和版本差异分析，但日常只使用 CLI 时下载官方发行版更省空间。源码要求 Go `1.26.4`，本机未安装 Go；Terraform 1.6+ 源码采用 Business Source License 1.1，使用和再分发需按其条款核对。
- 专利 Skill 的根 `SKILL.md` 是唯一 `user-invocable: true` 的路由入口，6 个子技能均为内部路由。仓库要求 Python 3.9+，主路径还涉及 Playwright、系统 Chrome/Edge、Word/PPT 解析和可选 CAD/Obsidian/OA 向量库；适合按整仓安装，不能只拷一个子目录。它可辅助专利文稿和检索，但不替代专利代理师或法律审查。
- Graphify 与 zvec-grep 都值得保留：前者把显式关系和调用链做成持久图谱，后者偏语义发现、BM25 与精确检索路由；Terraform 只在需要 IaC 源码研究时体现完整历史价值；专利 Skill 领域明确、价值高，但建议在真实任务出现后再按整仓安装和补依赖。

---

## 2026-09-03 PDF Inspector、Effective HTML 与既有 Skills 复核

| 仓库 | 类型 | 本地目录 | Skill / 使用结论 | 状态 |
|------|------|----------|------------------|------|
| [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector) | Rust PDF 分类、文本抽取与 OCR 路由工具 | `E:\aimodel\pdf-inspector\` | 0 个 `SKILL.md`；可将 PDF 分类为 `TextBased`、`Scanned`、`ImageBased`、`Mixed`，返回置信度及逐页 OCR 路由，并可直接抽取结构化 Markdown | 已浅克隆；未编译、未安装 Python/Node/Rust 包或 OCR 运行时 |
| [plannotator/effective-html](https://github.com/plannotator/effective-html) | 自包含 HTML artifact Skills / Codex 插件 | `E:\aimodel\effective-html\` | 6 个 Skill：`html`、`design-artifact`、`html-wireframe`、`html-prototype`、`html-plan`、`html-diagram`；适合结构化报告、线框、原型、计划和关系图 | 已浅克隆；未安装为全局 Skill 或 Codex 插件 |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 精简 Agent 编码行为准则 | `E:\aimodel\andrej-karpathy-skills\` | 1 个 Skill；内容与当前 Codex 的最小改动、显式假设和验证闭环规则高度重合 | 已有克隆，不重复下载；保留作参考，不追加全局安装 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 工程与生产力 Skill 集合 | `E:\aimodel\mattpocock-skills\` | 当前本地 37 个 `SKILL.md`；覆盖需求澄清、TDD、诊断、架构、评审、研究与交接，适合按单项选用 | 已有干净克隆，不重复下载或全量安装；旧的 `backend-skills\mattpocock-skills\` 副本未改动 |

### 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| pdf-inspector | https://github.com/firecrawl/pdf-inspector.git | `65b7fa1` | 2026-09-01 `fix(loader): bound object-stream decompression at load (lopdf 0.44) (#478)` |
| effective-html | https://github.com/plannotator/effective-html.git | `d95debb` | 2026-08-03 `docs: sync design artifact guide (#23)` |

### 静态核查结论

- 两个新增仓库均为 MIT 许可、浅克隆、干净工作树，没有 Git submodule，并通过 `git fsck --no-reflogs`。`pdf-inspector` 约 25 MB，`effective-html` 约 43 MB。
- `pdf-inspector` 当前包版本为 `1.17.0`，Rust crate 要求 Rust `1.88`，Python 包要求 Python `>=3.8`。默认 Rust 构建不启用 OCR；完整本地 OCR 是可选 feature，另需 PDFium、ONNX Runtime 和模型文件，因此本轮只保存源码。
- `pdf-inspector` 与既有 `liteparse` 都能把原生文本 PDF 转为 Markdown，但前者更适合作为轻量的“先分类、再按页送 OCR”路由层；上游性能与质量数字是项目方基准，本轮没有在 Windows 上复跑。
- `Effective HTML` 的 `html` 是可自动路由的广义入口，其余专门 Skill 多为显式调用。它与 `taste-skill`、`hallmark`、`emilkowalski-skills/prototype`、`archify` 有部分视觉或原型重叠，但独特价值是把报告、计划、线框、原型和关系图统一为可访问、响应式、单文件 HTML artifact。
- 两个新仓库由提升权限的克隆进程创建，Windows Git 会报告所有权保护。核查时仅使用命令级 `safe.directory` 例外，没有写入全局 Git 配置；后续常规 Git 操作可能仍需相同的单次例外或先修正目录所有权。

---

## 2026-09-02 Pisper 下载与既有项目复核

| 仓库 | 类型 | 本地目录 | Skill / 使用结论 | 状态 |
|------|------|----------|------------------|------|
| [ling-kong-ran/pisper](https://github.com/ling-kong-ran/pisper) | 多 Agent 本地工作台（Desktop / TUI / Mobile） | `E:\aimodel\pisper\` | 0 个标准 `SKILL.md`；基于 Pi Coding Agent 管理并行会话、Turn 上下文分支、工作目录、权限、工作流、记忆和 MCP/插件 | 已完整克隆；未安装 Node.js 依赖、桌面应用或 Provider 凭据 |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 精简的 Agent 编码行为准则 | `E:\aimodel\andrej-karpathy-skills\` | 已有 1 个 Skill；原则与当前 Codex 工作规范高度重合，保留作参考，不追加全局安装 | 已有浅克隆；本轮未更新 |
| [StarTrail-org/LEANN](https://github.com/StarTrail-org/LEANN) | 本地私有 RAG / 语义检索套件 | `E:\aimodel\LEANN\` | 无标准 `SKILL.md`，含 OpenClaw `leann-memory` 适配；适合大规模本地知识库，不是轻量向量库替代品 | 已有克隆；因 Windows Git 所有权保护未改动或更新 |

### 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| pisper | https://github.com/ling-kong-ran/pisper.git | `a0e2af6c` | 2026-09-02 `test: track visual providers in the visual connections section` |

### 静态核查结论

- `pisper` 为完整、非浅克隆，不含 Git submodule，已通过 `git fsck --no-reflogs`；工作树约 85 MB。它不含通用 Agent Skills 标准的 `SKILL.md`，因此不写入 `SKILLS_INDEX.md`。
- Pisper 的“分支”是从已完成 Turn 派生且继承上下文的 Agent 会话分支，每个会话可独立模型、上下文、工作目录和权限。它适合可视化管理并行 Agent 工作，但不应被当作 Git worktree 创建、冲突消解和代码合并队列工具；底层运行时为 Pi Coding Agent，非 Codex 原生运行时。
- `andrej-karpathy-skills` 与 `LEANN` 均已在旧台账中登记，故未重复克隆。LEANN 的当前 Windows 所有权与运行用户不一致；为避免修改全局 Git `safe.directory` 配置，本轮没有拉取或检查其工作树。

---

## 2026-09-02 Sepia、Archify 下载与候选项目评估

| 仓库 | 类型 | 本地目录 | Skill / 使用结论 | 状态 |
|------|------|----------|------------------|------|
| [Nanako0129/sepia](https://github.com/Nanako0129/sepia) | 去 AI 腔写作 Skill | `E:\aimodel\sepia\` | 1 个可移植 `SKILL.md`，含 Codex 原生插件结构；适合小说叙事修订及发布说明、PR 回复、复盘等专业文稿 | 已完整克隆；未安装依赖、未写入全局 Codex skills |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | 架构与流程图 Agent Skill / Node.js 渲染器 | `E:\aimodel\archify\` | 1 个 `archify` Skill；可生成架构、工作流、时序、数据流和生命周期图，导出自包含 HTML/SVG/PNG/WebM | 已完整克隆；未安装依赖、未写入全局 Codex skills |
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | 大型角色提示词与流程库 | — | 上游仍在维护且支持 Codex；适合按需借鉴专业角色的检查清单，不建议全量安装以避免规则重叠和上下文噪声 | 仅核查，未克隆 |
| [alibaba/zvec](https://github.com/alibaba/zvec) | 嵌入式向量数据库 | — | 适合本地 RAG、Agent 记忆、私有知识库和代码/文档语义搜索；不适合分布式多节点或高并发多写入 | 仅核查，未克隆 |

### 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| sepia | https://github.com/Nanako0129/sepia.git | `ac2f06e8` | 2026-09-02 `docs(zh-CN): add Simplified Chinese README (#33)` |
| archify | https://github.com/tt-a1i/archify.git | `06dd0526` | 2026-09-02 `fix: ship third-party mark notices (#267)` |

### 静态核查结论

- 两个已下载仓库均为完整克隆（非 shallow clone），且不含 Git submodule；已通过 `git fsck --no-reflogs` 核验。`archify` 工作树约 152 MB，包含文档、示例、实验和生成产物，完整保留以便离线研究或二次开发。
- `archify` 同时拥有项目展示/文档站点，但其主体是开源仓库和可通过 Skills CLI 安装的 Skill；对日常画图不需要读取整个本地仓库。
- `zvec` 提供进程内、无服务端的向量检索，并支持稠密/稀疏向量、全文、结构化过滤和混合检索；要使用它仍需由应用或模型侧产生嵌入向量。

---

## 2026-08-29 LoopX 与 ego-lite 下载及浏览器能力复核

| 仓库 | 类型 | Stars（核查时） | 本地目录 | Skill | 状态 |
|------|------|----------------|----------|-------|------|
| [huangruiteng/loopx](https://github.com/huangruiteng/loopx) | 长周期 Agent 控制平面 | 5.3k | `E:\aimodel\loopx\` | 9 份物理 `SKILL.md`（8 正式 + 1 demo） | 已浅克隆，仅保存源码 |
| [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) | Agent 友好浏览器与 CDP harness | 14.2k | `E:\aimodel\ego-lite\` | 1 个 `ego-browser` Skill | 已浅克隆；Windows 上不可安装当前 macOS 应用 |

### 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| loopx | https://github.com/huangruiteng/loopx.git | `e2275510` | 2026-08-29 `perf(cli): lazily load common command owners (#3717)` |
| ego-lite | https://github.com/citrolabs/ego-lite.git | `5ca3c36c` | 2026-08-24 `Merge pull request #317 from citrolabs/docs/star-history-branch` |

### 静态核查结论

- `LoopX` 负责 goal、todo、gate、evidence、quota、handoff、恢复和跨运行时持续执行，不负责浏览器控制或截图解析。它适合作为浏览器工具之上的长任务控制层。
- `LoopX` 本地项目版本为 `0.5.3`，要求 Python `>=3.11`，核心包声明无第三方运行时依赖；当前版本使用 Apache-2.0，旧版本 MIT 文本仍保留。
- `ego-lite` 仓库开源的是 MIT 许可的 `ego-browser` TypeScript/CDP harness 和 Skill，不包含提供 `globalThis.ego` bindings 的浏览器应用源码。
- `ego-browser` 以语义 Snapshot + 元素引用驱动网页，也能捕获截图；它没有内置 OCR 或多模态视觉模型，不能把“保存截图”等同于“理解截图像素”。
- 上游当前明确只提供 macOS 浏览器应用，Windows/Linux 在 roadmap；所以本轮没有安装应用、扩展、依赖或全局 Skill，也没有复现项目方的性能/成功率基准。
- 与根目录 `browser-use`、`chrome-devtools-mcp`、`OpenCLI`、`web-access`、`nanobrowser`、Playwright `webapp-testing`、`crawl4ai` 和 MiniMax `vision-analysis` 的详细区别见 [BROWSER_AUTOMATION_COMPARISON.md](BROWSER_AUTOMATION_COMPARISON.md)。

---

## 当前维护边界（2026-08-28）

- 检查 `E:\aimodel` 下的一级有效 Git 仓库，包括 skill 与 tool；只对干净工作树和已配置上游的普通分支执行快进更新。
- 不递归更新仓库内部的 skill/tool 子目录。
- 2026-08-28 共检查 82 个仓库：41 个快进、39 个已是最新、1 个因本地修改跳过、1 个因历史分叉保留原状。
- `reverse-skill` 因本地 3 个修改文件跳过更新；`codetracer` 补全浅克隆历史后为 ahead 3 / behind 1521，不自动改写。

### 2026-08-28 同步异常复核

| 仓库 | 初始现象 | 原因 | 当前处理 |
|------|----------|------|----------|
| gortex | `git pull` 报 TLS `unexpected EOF` | 瞬时 HTTPS 传输中断 | 重试成功，`ea44cc2` → `06939fc`，与上游 0/0 |
| codetracer | 初看 ahead 1 / behind 3464，无法快进 | 旧浅克隆边界掩盖真实历史；补全后确认上游重排，实际 ahead 3 / behind 1521 | 保留本地 `main`；未 merge/rebase/reset，等待人工决策 |
| reverse-skill | 未执行拉取 | 工作树有 3 个本地修改文件 | 按保护规则跳过 |

`codetracer` 的 3 个本地提交均为 2026-05-07 的上游作者提交：`6a5c0a9`、`167f62c`、`757b0b9`。上游后来出现同作者日期、同主题的 `d4ee0a1` 等重排内容，但补丁并不完全等价，因此不能把它当作普通落后仓库直接快进。

---

## 2026-07-19 第一批总览

| 仓库 | 类型 | Stars（检索时） | 本地目录 | 状态 |
|------|------|----------------|----------|------|
| [mortspace/playcaptcha](https://github.com/mortspace/playcaptcha) | React 安全组件 | 425 | `E:\aimodel\playcaptcha\` | 已克隆，待项目内依赖安装 |
| [zzet/gortex](https://github.com/zzet/gortex) | 代码智能/跨代理工具 | 884 | `E:\aimodel\gortex\` | 已克隆，待 CLI/daemon 配置 |
| [run-llama/liteparse](https://github.com/run-llama/liteparse) | PDF/文档解析 | 11.6k | `E:\aimodel\liteparse\` | 已克隆，待 Python/Node/Rust 入口选择 |
| [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | LLM 友好网页爬取 | 73.1k | `E:\aimodel\crawl4ai\` | 已克隆，待 Python 依赖和浏览器依赖配置 |
| [jackwener/OpenCLI](https://github.com/jackwener/OpenCLI) | 自然语言浏览器自动化 CLI | 26.9k | `E:\aimodel\OpenCLI\` | 已克隆，待 npm/Chrome 扩展配置 |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | AI 浏览器自动化 | 105k | `E:\aimodel\browser-use\` | 已克隆，待 Python/Playwright 依赖配置 |

---

## 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| playcaptcha | https://github.com/mortspace/playcaptcha.git | `e9e0e0f` | 2026-06-12 fix: add demo video to README |
| gortex | https://github.com/zzet/gortex.git | `ea44cc2` | 2026-07-15 Merge pull request #295 from zzet/dependabot/github_actions/actions-minor-patch-fe548e5f3c |
| liteparse | https://github.com/run-llama/liteparse.git | `cc0fa5a` | 2026-07-14 fix glibc builds |
| crawl4ai | https://github.com/unclecode/crawl4ai.git | `7e80152` | 2026-07-15 Merge pull request #2077 from unclecode/release/v0.9.2 |
| OpenCLI | https://github.com/jackwener/OpenCLI.git | `b0f84c9` | 2026-07-13 fix: click hit-testing + facebook feed/search DOM drift (#2076 #2071 #2089 #2090) (#2126) |
| browser-use | https://github.com/browser-use/browser-use.git | `950eb03` | 2026-07-16 Release 0.13.6 with Browser Harness 0.1.6 (#5245) |

---

## 2026-07-19 第二批下载

| 仓库 | 类型 | Stars（检索时） | 本地目录 | Skill/插件 | 状态 |
|------|------|----------------|----------|------------|------|
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Claude 知识工作插件集 | 22.8k | `E:\aimodel\knowledge-work-plugins\` | 212 SKILL.md / 22 插件 | 已克隆，待插件配置 |
| [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | LLM 输入/日志压缩工具 | 59.8k | `E:\aimodel\headroom\` | 1 插件 | 已克隆，待代理/代理服务器配置 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 工程技能库 | 176k | `E:\aimodel\mattpocock-skills\` | 41 SKILL.md / 1 插件 | 已存在，已 fast-forward 更新 |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | Claude/Cursor 行为指南 | 194k | `E:\aimodel\andrej-karpathy-skills\` | 1 SKILL.md / 1 插件 | 已克隆 |
| [NVIDIA/skillspector](https://github.com/NVIDIA/skillspector) | AI skill 安全扫描 | 13.4k | `E:\aimodel\skillspector\` | 23 SKILL.md | 已克隆，待 Python 依赖配置 |
| [tjxj/z-skills](https://github.com/tjxj/z-skills) | 可复用 skill 集合 | 187 | `E:\aimodel\z-skills\` | 10 SKILL.md | 已克隆 |
| [bradautomates/claude-video](https://github.com/bradautomates/claude-video) | Claude 视频理解 skill | 9.1k | `E:\aimodel\claude-video\` | 1 SKILL.md / 2 插件 | 已克隆，待视频依赖配置 |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 审美/设计品味 skill | 64.9k | `E:\aimodel\taste-skill\` | 13 SKILL.md / 1 插件 | 已克隆 |
| [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | LLM/RAG/Agent 应用合集 | 124k | `E:\aimodel\awesome-llm-apps\` | 6 SKILL.md | 已克隆 |
| [powerycy/multi-style-image-generator](https://github.com/powerycy/multi-style-image-generator) | 多风格图像生成 skill | 22 | `E:\aimodel\multi-style-image-generator\` | 1 SKILL.md | 已克隆 |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | 多平台网页读取/搜索 CLI | 57.7k | `E:\aimodel\Agent-Reach\` | 1 SKILL.md | 已克隆，待 CLI 配置 |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 反 AI 味 UI 设计 skill | 12.4k | `E:\aimodel\hallmark\` | 1 SKILL.md | 已克隆，已安装到 Codex skills |

### 第二批克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| knowledge-work-plugins | https://github.com/anthropics/knowledge-work-plugins.git | `74d516a` | 2026-07-17 bump(qdrant-skills): 97c547be -> d1af526e (#620) |
| headroom | https://github.com/headroomlabs-ai/headroom.git | `6cdfd3f` | 2026-07-18 fix(proxy/openai): feed chat/completions traffic into the traffic learner (#2333) |
| mattpocock-skills | https://github.com/mattpocock/skills.git | `9603c1c` | 2026-07-16 Merge pull request #586 from mattpocock/batch-grill-me-granular-facts |
| andrej-karpathy-skills | https://github.com/multica-ai/andrej-karpathy-skills.git | `2c60614` | 2026-04-20 Sync Chinese README with English version (add Cursor section) (#95) |
| skillspector | https://github.com/NVIDIA/skillspector.git | `8f534e2` | 2026-07-14 Merge pull request #275 from NVIDIA/keshavp/oss-release-2026-07-14 |
| z-skills | https://github.com/tjxj/z-skills.git | `fc4bddc` | 2026-07-10 Harden web packaging and video downloads |
| claude-video | https://github.com/bradautomates/claude-video.git | `83da59f` | 2026-06-30 Fix WATCH_DETAIL silently falling back to default |
| taste-skill | https://github.com/Leonxlnx/taste-skill.git | `7c397f2` | 2026-07-17 Add IMG.LY sponsor |
| awesome-llm-apps | https://github.com/Shubhamsaboo/awesome-llm-apps.git | `41621a5` | 2026-07-17 Merge pull request #931 from SHAI-manpreet-likhari/fix/guard-empty-openai-response-memory-tutorials |
| multi-style-image-generator | https://github.com/powerycy/multi-style-image-generator.git | `b58d569` | 2026-07-15 Merge pull request #1 from powerycy/feat/automatic-dependency-bootstrap |
| Agent-Reach | https://github.com/Panniantong/Agent-Reach.git | `1494c2a` | 2026-07-18 Merge pull request #492 from Panniantong/codex/add-agent-skills-hub-link |
| hallmark | https://github.com/Nutlope/hallmark.git | `aeb42fb` | 2026-06-04 Merge pull request #18 from Nutlope/fix/existing-stylesheet-merge |

---

## 项目说明

### mortspace/playcaptcha
- **定位**: 一个 React CAPTCHA 组件，主打“可玩”的验证体验，可用于替代传统验证码交互。
- **技术栈/许可**: TypeScript，MIT License。
- **适合场景**: 有前端登录、注册、表单防滥用需求时再安装；它不是 AI skill，也不是代理工具。
- **安装参考**:
  ```bash
  npm install playcaptcha
  ```
- **本地目录**: `E:\aimodel\playcaptcha\`

### zzet/gortex
- **定位**: 为 AI 编码代理准备的代码智能服务器/工具，提供仓库索引、语义搜索、依赖关系和符号级理解。
- **AI 兼容性**: 文档明确面向多种 AI 编码代理，适合 Claude Code、Codex CLI、Cursor、Gemini CLI 等共享使用。
- **技术栈/许可**: Go，Apache-2.0 License。
- **安装参考**:
  ```powershell
  irm https://get.gortex.dev/install.ps1 | iex
  gortex install
  gortex daemon start --detach
  ```
- **本地目录**: `E:\aimodel\gortex\`

### run-llama/liteparse
- **定位**: LlamaIndex 生态里的开源 PDF 解析工具，强调本地、快速、适合 AI/agent 工作流。
- **能力**: 解析文本、表格、图片、公式，支持 Python、JS/TS、CLI、Docker，也提供 agent skill 方式。
- **技术栈/许可**: Rust/Python/TypeScript，Apache-2.0 License。
- **安装参考**:
  ```bash
  pip install liteparse
  # 或
  npm install -g @llamaindex/liteparse
  # Claude Code / Codex skill:
  npx skills add run-llama/llamaparse-agent-skills --skill liteparse
  ```
- **本地目录**: `E:\aimodel\liteparse\`

### unclecode/crawl4ai
- **定位**: 开源、LLM 友好的网页爬虫和抓取工具，把网页转成可用于 AI 的 Markdown/结构化结果。
- **能力**: 异步爬取、浏览器自动化、抽取/清洗内容、深度爬取、RAG 数据准备、Docker/MCP/CLI 集成。
- **技术栈/许可**: Python，Apache-2.0 License。
- **安装参考**:
  ```bash
  pip install -U crawl4ai
  crawl4ai-setup
  crawl4ai-doctor
  ```
- **本地目录**: `E:\aimodel\crawl4ai\`

### jackwener/OpenCLI
- **定位**: 把自然语言命令转换为浏览器自动化操作，强调使用本机浏览器登录态和站点适配器。
- **能力**: Chrome 扩展桥接、站点适配器、`npx skills` 安装、支持用自然语言操作 Amazon、ChatGPT、GitHub、Gmail、Notion 等站点。
- **技术栈/许可**: TypeScript，Apache-2.0 License。
- **安装参考**:
  ```bash
  npm install -g @jackwener/opencli
  opencli doctor
  npx skills add jackwener/opencli
  ```
- **本地目录**: `E:\aimodel\OpenCLI\`

### browser-use/browser-use
- **定位**: 让 AI agent 控制浏览器的开源自动化框架，可作为 Python 库、CLI、云服务或 agent skill 使用。
- **AI 兼容性**: 文档列出 Claude Code、Codex CLI、Cursor、Windsurf、VS Code、Goose 等用法，跨 AI 复用价值高。
- **技术栈/许可**: Python，MIT License。
- **安装参考**:
  ```bash
  pip install browser-use
  playwright install chromium
  # 或安装 agent skill:
  uvx browser-use[cli] skill install
  ```
- **本地目录**: `E:\aimodel\browser-use\`

---

## 安装优先级建议

| 优先级 | 仓库 | 理由 |
|--------|------|------|
| 高 | browser-use/browser-use | 通用浏览器自动化，直接提升代理办事能力 |
| 高 | zzet/gortex | 给多个编码代理共享代码理解能力，适合当前资源库定位 |
| 高 | unclecode/crawl4ai | 抓网页、构建 RAG 语料、研究资料收集都常用 |
| 中 | jackwener/OpenCLI | 与 browser-use 有重叠，但更偏自然语言操作已登录网站 |
| 中 | run-llama/liteparse | 文档/PDF 场景很有用，按需要安装 |
| 低 | mortspace/playcaptcha | 前端组件，不属于 AI 工具，只有具体项目需要 CAPTCHA 时安装 |

---

## 兼容性判断

这些项目大多可以给 Claude Code 之外的 AI 使用：

- **跨 AI 最强**: `gortex`、`browser-use`、`crawl4ai`。它们提供 CLI、服务、MCP 或库接口，不绑定单一模型。
- **偏 Claude/Codex skill 生态**: `liteparse`、`browser-use`、`OpenCLI` 都提供或提到 skill 安装方式，但底层也能通过 CLI/库调用。
- **不是 AI skill**: `playcaptcha` 是 React 组件，应该按前端依赖管理，而不是按 agent skill 管理。

---

## 后续安装记录模板

后续执行依赖安装或全局安装时，建议按下面格式追加到 `SKILLS_INSTALLED.md`：

```markdown
### 项目名
- **目录**: `E:\aimodel\项目名\`
- **来源**: https://github.com/owner/repo
- **安装命令**: `...`
- **状态**: 已安装 / 已克隆 / 待配置
- **备注**: 依赖、环境变量、MCP 配置或登录态要求
```

---

## 2026-07-30 第三批更新

| 仓库 | 类型 | Stars（检索时） | 本地目录 | Skill/插件 | 状态 |
|------|------|----------------|----------|------------|------|
| [rahulv-official/inspira-ui](https://github.com/rahulv-official/inspira-ui) | Vue/Nuxt UI 组件集合 | 未统计 | `E:\aimodel\inspira-ui\` | 0 SKILL.md / 0 插件 | 已克隆，按前端项目需要使用 |
| [kepano/kepano-obsidian](https://github.com/kepano/kepano-obsidian) | Obsidian vault 模板 | 未统计 | `E:\aimodel\kepano-obsidian\` | 0 SKILL.md / 0 插件 | 已克隆，作为 Obsidian 模板和配套资料 |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Obsidian Agent Skills | 未统计 | `E:\aimodel\obsidian-skills\` | 5 SKILL.md / 1 插件 | 已克隆，仅保留在当前目录 |
| [earendil-works/pi](https://github.com/earendil-works/pi) | 自扩展 coding agent / TUI / LLM API | 未统计 | `E:\aimodel\pi\` | 17 SKILL.md（测试夹具为主）/ 0 插件 | 已克隆，待按需研究 CLI 和包结构 |
| [Simon-He95/vue-tui](https://github.com/Simon-He95/vue-tui) | Vue 3 terminal UI toolkit | 未统计 | `E:\aimodel\vue-tui\` | 1 SKILL.md / 0 插件 | 已克隆，skill 位于 `.agents\skills\vue-tui\` |

### 第三批克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| inspira-ui | https://github.com/rahulv-official/inspira-ui.git | `fdd645e` | 2026-07-15 Fix category selection |
| kepano-obsidian | https://github.com/kepano/kepano-obsidian.git | `4736973` | 2026-01-08 Update attachments |
| obsidian-skills | https://github.com/kepano/obsidian-skills.git | `a1dc48e` | 2026-06-08 Merge pull request #59 from SDGLBL/codex/add-base-embed-example |
| pi | https://github.com/earendil-works/pi.git | `71efc6f` | 2026-07-30 Add [Unreleased] section for next cycle |
| vue-tui | https://github.com/Simon-He95/vue-tui.git | `010872a` | 2026-07-25 feat: update 3D badge CLI to support Bun runtime and improve image decoding |

### 第三批项目说明

#### inspira-ui
- **定位**: 面向 Vue 和 Nuxt 的视觉组件集合，风格来源接近 Aceternity UI、Magic UI 和 shadcn-vue 生态。
- **技术栈/许可**: Nuxt 4、Vue 3、TypeScript、MIT License。
- **安装参考**:
  ```bash
  pnpm add @inspira-ui/plugins
  ```
- **备注**: 这是前端组件/文档仓库，不是 agent skill。

#### kepano-obsidian
- **定位**: Steph Ango 的个人 Obsidian vault 模板，展示分类、附件、模板、Daily、Notes、References 等结构。
- **配套关系**: 与 `kepano/obsidian-skills` 搭配使用，前者提供 vault 组织样例，后者提供 agent 处理 Obsidian 文件的 skills。
- **备注**: 没有 `SKILL.md`，不作为 skill 安装。

#### obsidian-skills
- **定位**: 遵循 Agent Skills 规范的 Obsidian skills，可被 Claude Code、Codex、OpenCode 等 skills-compatible agent 使用。
- **包含 skills**: `obsidian-markdown`、`obsidian-bases`、`json-canvas`、`obsidian-cli`、`defuddle`。
- **备注**: 本次只克隆到当前目录，没有复制到全局 Codex skills 目录。

#### pi
- **定位**: Pi Agent Harness，包含交互式 coding agent CLI、agent runtime、多供应商 LLM API 和 TUI 包。
- **主要包**: `@earendil-works/pi-coding-agent`、`@earendil-works/pi-agent-core`、`@earendil-works/pi-ai`、`@earendil-works/pi-tui`。
- **备注**: 仓库中的 `SKILL.md` 主要位于测试夹具和扩展示例，不按正式 skill 集合计入安装。

#### vue-tui
- **定位**: Simon He 开发的 Vue 3 terminal UI toolkit，可用一套 Vue 组件模型渲染浏览器 DOM、真实 CLI stdout 和 headless tests。
- **包名**: `@simon_he/vue-tui`。
- **包含 skill**: `.agents\skills\vue-tui\SKILL.md`。
- **安装参考**:
  ```bash
  pnpm add @simon_he/vue-tui vue
  ```

---

## 2026-08-15 第四批下载与同步

### 新增一级仓库

| 仓库 | 类型 | HEAD | 本地目录 | Skill/参考状态 |
|------|------|------|----------|----------------|
| [StarTrail-org/LEANN](https://github.com/StarTrail-org/LEANN) | 本地语义搜索、RAG、MCP | `dc85934` | `E:\aimodel\LEANN\` | 0 个标准 `SKILL.md`；`skills/leann-memory/` 是 OpenClaw `claw.json + instructions.md` 适配 |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | UI 动效与设计 skill | `78761e1` | `E:\aimodel\emilkowalski-skills\` | 10 个正式 `SKILL.md` |
| [bobeff/open-source-games](https://github.com/bobeff/open-source-games) | 开源游戏索引 | `3a9ab8f` | `E:\aimodel\open-source-games\` | 0 个 `SKILL.md`；游戏开发参考 |
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | 从零实现软件的教程索引 | `aa17439` | `E:\aimodel\build-your-own-x\` | 0 个 `SKILL.md`；软件/游戏实现参考 |
| [Zenghuang-Fu/SESA-Self-Evolving-Search-Agents](https://github.com/Zenghuang-Fu/SESA-Self-Evolving-Search-Agents) | 搜索 agent 自演化研究代码 | `74de5d7` | `E:\aimodel\SESA-Self-Evolving-Search-Agents\` | 0 个 `SKILL.md`；研究参考 |

### 已有仓库同步

| 仓库 | HEAD | 最新提交 | 状态 |
|------|------|----------|------|
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | `30fc648f` | 2026-08-14 `fix(landing): remove duplicate pricing capability block (#6913)` | 已快进同步 |
| [earendil-works/pi](https://github.com/earendil-works/pi) | `b1efcf7d7` | 2026-08-14 `chore: approve contributors from issue #8124` | 已快进同步 |

### 论文下载

| 论文 | 标题 | 本地文件 |
|------|------|----------|
| [arXiv:2607.29468v1](https://arxiv.org/html/2607.29468v1) | Self-Play Meets Skill Evolution: Self-Evolving Search Agents that Pose, Solve, and Remember | `E:\aimodel\arxiv-2607.29468v1.pdf` |
| [arXiv:2607.27733v1](https://arxiv.org/html/2607.27733v1) | VeriSkill: A Self-Evolution Framework for Program Verification Skills | `E:\aimodel\arxiv-2607.27733v1.pdf` |

本批只下载和记录，不安装依赖，不复制到全局 Codex skills 目录，也不更新仓库子目录内的 Markdown。

---

## 2026-08-15 其他 skill 仓库更新

### 本轮同步结果

| 项目 | 数量 | 说明 |
|------|------|------|
| 已快进更新 | 26 | 工作区干净且远程可访问 |
| 已是最新 | 15 | 无需变更 |
| 跳过 | 1 | `reverse-skill` 有 3 个本地修改文件，保留用户修改 |

### 发现并补登记的仓库链接

| 仓库 | 类型 | HEAD | 本地目录 | Skill 数量 |
|------|------|------|----------|------------|
| [different-ai/openwork](https://github.com/different-ai/openwork) | 跨 Agent 的桌面工作区、MCP、skill/plugin 共享平台 | `08fb6af` | `E:\aimodel\openwork\` | 33 |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 本地代码/文档知识图谱与 `/graphify` skill | `7281f27` | `E:\aimodel\graphify\` | 1 |

这两个仓库的远程地址此前存在于本地 Git 配置，但未登记在根目录台账；本次已补入索引和手动收藏清单。

---

## 2026-08-17 第五批设计 skill 与参考仓库

| 仓库 | 类型 | HEAD | 本地目录 | Skill/参考数量 | 状态 |
|------|------|------|----------|----------------|------|
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UI/UX skill/plugin | `a38d04c` | `E:\aimodel\ui-ux-pro-max-skill\` | 6 SKILL.md / 1 plugin | 已快进更新 |
| [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | `DESIGN.md` 设计系统参考库 | `8147538` | `E:\aimodel\awesome-design-md\` | 73 DESIGN.md / 0 SKILL.md | 已克隆，仅作设计参考 |

### 本批说明

- `ui-ux-pro-max-skill` 最新提交：2026-08-14 `feat(search): overhaul relevance and curated design data`。
- `awesome-design-md` 提供从真实网站提炼的 `DESIGN.md` 参考文档，可按项目需要整理使用。
- 本批未安装依赖、未复制到全局 Codex skills，也未修改仓库内部 Markdown。

---

## 2026-08-25 科研 skills 补全与作品集参考

| 仓库 | 类型 | HEAD | 本地目录 | Skill/参考数量 | 状态 |
|------|------|------|----------|----------------|------|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 开放 Agent Skills 科研技能库 | `36d8f13` | `E:\aimodel\scientific-agent-skills\` | 本地 163 个一级 `SKILL.md` | 已重新获取缺失对象并完整检出；2446 个跟踪文件无缺失，HEAD 与 `origin/main` 一致，工作树干净；结构契约已验证，不安装学科依赖或全局 skills |
| [emmabostian/developer-portfolios](https://github.com/emmabostian/developer-portfolios) | 开发者作品集案例索引 | `89f6044` | `E:\aimodel\developer-portfolios\` | 0 个 `SKILL.md` | 已浅克隆，仅作参考，不计入正式 skill |

### 科研技能库验证边界

- 仓库 `_meta` 的 9 项平台无关规则通过：插件清单、技能发现、测试覆盖映射、需求映射、共享文件一致性与脚本结构等均无问题。
- Windows 文件系统上的 POSIX 执行位检查不适用；Git 索引确认 `latex-posters` 与 `scientific-schematics` 的 shell 脚本均为 `100755`，两者的 `bash -n` 语法检查通过。
- 当前只补全仓库内容，不安装 Python/科研软件包、不配置外部 API 凭据、不复制到全局 Agent/Codex skills。实际使用时按课题读取目标 `SKILL.md` 并做依赖、权限、许可证审查。

---

## 2026-08-27 系统设计参考仓库

| 仓库 | 类型 | HEAD | 本地目录 | 内容/状态 |
|------|------|------|----------|-----------|
| [ByteByteGoHq/system-design-101](https://github.com/ByteByteGoHq/system-design-101) | 系统设计图解、短文与面试参考 | `b28380a` | `E:\aimodel\system-design\system-design-101\` | 已使用 `--depth 1` 浅克隆；400 篇 Markdown guides、0 个 `SKILL.md`；工作树干净 |

### 下载判断与边界

- **选择下载**：Git pack 约 1.31 MiB、跟踪内容约 1.76 MB、浅克隆本地总占用约 3.2 MB，落盘成本低，Markdown 正文可离线搜索；内容覆盖 API、数据库、缓存、支付、软件架构、云与分布式系统，可与 `donnemartin/system-design-primer` 互补。
- **不是完整离线归档**：400 篇 guide 的主图通过 `https://assets.bytebytego.com/diagrams/...` 引用，仓库没有收录这批主图；离线时仍可读文字，但查看图解需要联网。
- **许可限制**：仓库声明 CC BY-NC-ND 4.0，需署名、限非商业用途且不得发布演绎版本。因此只作为本地学习参考保存，不改写后再分发。
- **不作为 skill**：没有 `SKILL.md`，未安装 Node.js 依赖，也不纳入 `SKILLS_INDEX.md` 的正式 skill 数量。

---

## 2026-08-28 殆知阁古典文献仓库

| 仓库 | 类型 | HEAD | 本地目录 | 状态 |
|------|------|------|----------|------|
| [daizhige-org/daizhigev20](https://github.com/daizhige-org/daizhigev20) | 中国古典文献全文数据、数字人文语料 | `012bc39` | `E:\aimodel\daizhigev20\` | 已对 `data` 分支做浅层部分克隆；只检出根说明文件，正文对象按需下载；0 个 `SKILL.md` |

### 数量统计与口径

本地数字来自 2026-08-22 的 `data` 分支提交 `012bc393ff989f1a4354edf1a16c82645a99b715`；在线数字来自 2026-08-28 查看时的殆知阁目录页。

| 分类 | Git 树中的 Markdown 文件 | 在线目录标注“部” |
|------|-------------------------:|-------------------:|
| 佛藏 | 5,135 | 5,135 |
| 儒藏 | 914 | 914 |
| 医藏 | 965 | 965 |
| 史藏 | 4,179 | 4,178 |
| 子藏 | 3,084 | 3,084 |
| 易藏 | 343 | 343 |
| 艺藏 | 446 | 446 |
| 诗藏 | 820 | 820 |
| 道藏 | 1,720 | 1,720 |
| 集藏 | 2,974 | 2,974 |
| 现代作品 | 5 | 5 |
| **合计** | **20,585** | **20,584** |

这里的数字更准确地说是“正文 Markdown 页面/文件数”，不能直接等同于严格去重后的独立书种数：仓库会把《全唐文》《宋史》《本草纲目》等按卷拆成多个文件，个别文献还同时保留总文件与分卷目录。旧版项目常用“约 16,000 种、20 万卷、20 亿字”的概数；当前站点介绍页写“1.8 万部”，而实时目录显示 20,584 部。需要引用数量时，应注明日期和统计口径。

Git 树共有 23,151 个跟踪文件，其中 20,585 个为十藏及现代作品正文、2,560 个位于 `.sources`（校订来源快照），其余 6 个是根说明/配置及工作流文件。

### 内容、用途与边界

- **内容组织**: 仿经史子集扩展为佛、儒、医、史、子、易、艺、诗、道、集十藏，并另设现代作品；正文主要为简体中文 Markdown，文件头加入 YAML 元数据。
- **维护状态**: 这是已停止维护的 `garychowcmu/daizhigev20` 的修订 fork；维护者正在清理繁简转换、论坛残留、HTML/脚本等问题，并对《宋史》《本草纲目》《全唐文》等重点典籍重新导入、拆卷和互校。
- **适用场景**: 古籍全文检索、个人文库、数字人文研究、文言文 NLP/RAG 语料准备，以及查找公开文本来源。
- **质量提醒**: 数据来自多年网络汇集，修订工作仍在继续。学术引用、训诂、版本研究或模型评测前，应回查 frontmatter 所列来源、影印本或权威点校本，不能把仓库文本直接当作无误底本。
- **许可提醒**: 网站说明所收文本属于公有领域，但 `data` 分支没有顶层 `LICENSE` 文件。公有领域正文、后加元数据、编校注、来源快照和 `tools` 分支代码不是同一个权利层次；再分发或商用前需逐项核对来源与许可。
- **不是 skill**: 仓库没有 `SKILL.md`，不纳入 [SKILLS_INDEX.md](SKILLS_INDEX.md) 的正式 skill 数量，也未安装 Elasticsearch 或其他依赖。

### 本地保存策略

完整正文较大。官方说明 GitHub Pages 正文 artifact 在 2026 年 7 月约 2.15 GB，因此本次采用可检索目录、正文按需获取的轻量方式：

```powershell
# 已执行的轻量克隆方式
git clone --branch data --depth 1 --filter=blob:none --no-checkout https://github.com/daizhige-org/daizhigev20.git daizhigev20

# 列出仓库全部路径，不下载正文 blob
git -c core.quotepath=false -C E:\aimodel\daizhigev20 ls-tree -r --name-only HEAD

# 查找书名（PowerShell 示例）
git -c core.quotepath=false -C E:\aimodel\daizhigev20 ls-tree -r --name-only HEAD | Select-String '本草纲目'

# 按需读取一个文件；首次读取时 Git 才会获取对应正文 blob
git -C E:\aimodel\daizhigev20 show "HEAD:医藏/本草纲目/卷01.md"
```

当前本地目录约 3.4 MB，工作树干净，浅克隆和 `blob:none` 配置均已确认。若以后确实需要完整离线库，再按官方命令另行完整检出；本轮没有批量下载约 2 GB 的正文，也没有获取完整提交历史。

---

## 2026-08-28 学术科研 Skills 仓库与 Multi Search Engine

| 仓库/来源 | 类型 | HEAD/快照 | 本地目录 | 数量与状态 |
|------|------|------|----------|-----------|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 综合科学 Agent Skills | `36d8f13` | `E:\aimodel\scientific-agent-skills\` | 已有仓库与远端一致；163 个 `SKILL.md`；MIT |
| [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | Nature 写作、科研绘图与文献工作流 | `205ed18` | `E:\aimodel\nature-skills\` | 浅克隆、工作树干净；20 份物理文件，19 个可触发技能；Apache-2.0 |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | AI/ML 研究工程技能库 | `773a529` | `E:\aimodel\AI-Research-SKILLs\` | 浅克隆、工作树干净；98 个 Skill；MIT |
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | 研究全生命周期 Agent 工作区 | `6ed46da` | `E:\aimodel\claude-scholar\` | 浅克隆、工作树干净；45 个 Skill；MIT |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | 论文构筑、重写与审计编排器 | `895f4e4` | `E:\aimodel\PaperSpine\` | 浅克隆、工作树干净；7 份物理文件，V4 逻辑上是 1 个 Skill；MIT |
| [brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) | 社会科学实证 Skill 聚合库 | `517717f` | `E:\aimodel\Awesome-Agent-Skills-for-Empirical-Research\` | 保留旧本地目录并更新 canonical origin；catalog 1,096 项、含子模块后 1,162 份物理文件；根许可证 CC BY-SA 4.0 |
| [Multi Search Engine](https://github.com/aAAaqwq/AGI-Super-Team/tree/main/skills/multi-search-engine) | 搜索 URL 模板/路由参考 | SHA-256 `aba6bcf…` | `E:\aimodel\multi-search-engine\` | 仅保存上游 `SKILL.md` 与本地审计说明；非 Git、未安装 |

### 定位与选择建议

- **K-Dense**：覆盖面最大，适合生物信息、化学、医学、科学数据库、统计和科研产物生成。很多 Skill 只是针对 Python 包或外部数据库的高质量使用指南；运行时仍需逐项安装依赖、配置凭据并核对数据许可，不应整库一次性启用。
- **Nature Skills**：更贴近中文科研用户的论文生产流程。19 个可触发技能覆盖绘图、润色、写作、模拟审稿、引用、全文 reader、PPT、返修、文献检索/下载、实验日志和 proposal；其中部分仍标为 Draft/Beta。`nature-academic-search` 需要单独的 MCP/Python 依赖，PubMed 要求邮箱，Scopus/ScienceDirect 等可选来源需要本机凭据。
- **Orchestra**：面向 AI/ML 研究工程，而非一般学科文献库。98 个 Skill 覆盖模型架构、微调、后训练、分布式训练、推理、评测、RAG、MLOps、multimodal、研究构思和论文写作。Skill 文档本身可直接阅读，但实际框架、GPU 云或托管服务仍各有依赖和账号要求。
- **Claude Scholar**：不是单纯 Skill 合集，而是 skills、agents、commands、hooks、rules 和模板组成的研究工作区。适合计算机/AI 课题的选题、Zotero 文献管理、实验分析、写作和返修；主分支以 Claude Code 为主，Codex 使用单独分支/配置，不能把主分支配置不加审查地覆盖到现有环境。
- **PaperSpine**：专注“贡献优先、结果验证贡献、面向审稿人”的论文论证结构。V4 用一个 orchestrator 路由 12 阶段，并生成可审计中间产物；适合已有稿件重写或从素材构筑论文，不是文献数据库，也不能绕过付费墙。仓库同时带 V5 RC，正式使用前应明确选择稳定 V4 还是候选版。
- **AERS**：主要面向经济学、政治学、社会学、教育、心理等社会科学实证研究，包含 Python/Stata/R、因果推断、稳健性、复现、写作和投稿流水线。仓库简介的“23,000+”不是当前 canonical catalog 数；本地 `catalog/skills.json` 的权威口径是 76 个合集、1,096 项。大量内容来自第三方项目，根目录 CC BY-SA 4.0 不能替代每个上游组件自己的许可证审查。
- **Multi Search Engine**：标题宣称 17 个引擎，实际列出 7 个中文和 9 个国际引擎，共 16 个。当前上游目录只有没有 YAML frontmatter 的 `SKILL.md`，其声明的 `config.json` 返回 404，也没有 URL 编码、抓取、解析、并发、去重或排序代码；因此只把它作为查询模板设计参考保存。

### 验证边界

- 四个新仓库均使用 `--depth 1` 浅克隆；适合本地搜索和读取当前版本，不包含完整提交历史。
- AERS 是已有完整仓库的快进更新，唯一子模块 `skills/69-Paper-WorkFlow` 已按父仓库 gitlink 固定到 `110e7c6`，父仓库工作树干净。
- 四个新仓库与已更新 AERS 合计 1,332 份 `SKILL.md`，均以 YAML frontmatter 开头；独立保存的 Multi Search Engine 是唯一例外，已在本地说明中明确标记。
- 本批未运行需要 Python/R/Stata、LaTeX、浏览器、GPU 或外部数据库的功能测试，也未安装依赖、写入全局配置或提交外部任务。
