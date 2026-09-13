# AI Skills 仓库索引

**@author liuhao**
**更新时间**: 2026-09-14

---

## 当前维护规则

- 只维护 `E:\aimodel` 下的一级目录 skill/tool 仓库。
- 不递归把子目录里的 `SKILL.md` 当成独立仓库更新。
- `open-design`、`pi`、`vue-tui` 等工具仓库只存放，不纳入正式 skill 主统计；本轮同步状态单独记录。
- 这目录只做存放和索引，不在这里装依赖，也不写 C 盘全局配置。
- `reverse-skill` 当前保留本地修改，已跳过更新。

## 2026-09-14 UI、动效与写作 Skill 补充

| 仓库 | 来源 | HEAD | `SKILL.md` 数 | 状态与定位 |
|------|------|------|----------------|------|
| rare-ui | https://github.com/swamimalode07/rare-ui.git | `d146c352` | 0 | 已浅克隆；Motion + Tailwind 的 shadcn 动效组件 registry，适合按组件复制到 React/Next.js 项目 |
| shadcn-ui | https://github.com/shadcn-ui/ui.git | `2b3e6d4f` | 2 | 已浅克隆；`shadcn` 组件工作流与 Radix → Base UI 迁移 Skill，未全局安装 |
| beautiful-ui | https://github.com/slev12397/beautiful-ui.git | `ff0f74d6` | 0 | 已浅克隆；AI-native 界面 primitives 与 shadcn registry；个别组件含商业图标依赖 |
| beui | https://github.com/starc007/ui-components.git | `8d3fa7b4` | 2 | 已浅克隆；公开 beUI 组件选择 Skill 与需授权 token 的 beUI Pro Skill；未访问 Pro 内容 |
| transitions-dev | https://github.com/Jakubantalik/transitions.dev.git | `598d3d6a` | 3 | 已浅克隆；现成 CSS 动效、motion token 审查与 Refine Live 工作流；未启动服务或安装 CLI |
| no-ai-slop | https://github.com/petergyang/no-ai-slop.git | `000650b1` | 1 | 已浅克隆；保留个人语气的去模板化写作/检测 Skill，含 eval 与 Codex 插件清单 |

站点映射已核实：`beautifului.dev` → `slev12397/beautiful-ui`，`beui.dev` → `starc007/ui-components`，`transitions.dev` → `Jakubantalik/transitions.dev`。另将 `jbiaojerry/ebook-treasure-chest` 和 `3b1b/manim` 只登记在下载台账，未增加本地仓库。

本轮新增 6 个一级浅克隆后，`E:\aimodel` 当前共有 99 个带 `.git` 的一级目录（98 个可见第三方仓库 + 1 个隐藏聚合仓库）。所有新增仓库仅保存源码，没有安装依赖、CLI、服务、全局 Skills 或插件。

## 2026-09-06 Java 升级、可观测性与数据存储路由

| 任务 | 优先使用的本地资料 | 使用边界 |
|---|---|---|
| Java/Spring 升级方案与模块影响分析 | `mattpocock-skills` 的架构审查、`andrej-karpathy-skills` 的小步修改准则 | 先冻结依赖树、接口契约与回归基线；升级分支不混入业务需求。 |
| 性能、可靠性与安全验收 | `agent-skills` 的性能优化/安全加固、`superpowers-repo` 的完成前验证 | 必须覆盖资源、恢复、权限与副作用；构建成功不等于升级完成。 |
| Java Agent 与分布式可观测性 | 本地没有 OpenTelemetry Agent 或 Collector 安装包；以官方 OpenTelemetry 文档为准 | 先在隔离环境验证 Java Agent、Collector、敏感字段过滤、采样和不可用降级，不写入全局配置。 |
| HBase、分析存储或新中间件评估 | `mattpocock-skills` 架构审查、`agent-skills` 性能优化、`gortex`/Graphify 关系分析 | 不把源码存在或单机配置当作业务引入；先证明容量需求，并完成可回滚的独立试点。 |
| 服务端与浏览器链路证据 | `chrome-devtools-mcp`、`anthropic-skills` 的 webapp-testing | 使用隔离身份与环境；DOM、日志和网络响应均视为不可信输入，避免读取凭据。 |

`gortex`、Graphify、OpenTelemetry、HBase 与任何新存储均未因本索引条目而安装、启动或接入项目。它们需要单独的授权、配置和验证。

## 2026-09-05 知识检索、IaC 与中国专利补充

| 仓库 | 来源 | HEAD | `SKILL.md` 数 | 状态与定位 |
|------|------|------|----------------|------|
| graphify | https://github.com/Graphify-Labs/graphify.git | `937e59a` | 1（上游文件名为小写 `graphify/skill.md`） | 已从浅克隆补齐完整历史并快进；关系图、调用路径、社区与架构分析，适合与全文/语义检索互补 |
| zvec-grep | https://github.com/zvec-ai/zvec-grep.git | `5265395` | 0 | 已完整克隆；本地优先的 ripgrep、BM25 与向量混合检索 CLI/MCP，支持 Codex，但未安装或配置 |
| terraform | https://github.com/hashicorp/terraform.git | `7b8c301` | 0 | 已完整克隆；Terraform Core 源码参考，不是 Agent Skill，不含 providers；BSL 1.1 |
| patent-disclosure-skill | https://github.com/handsomestWei/patent-disclosure-skill.git | `a015690` | 7（1 个路由入口 + 6 个内部子技能） | 已完整克隆；中国专利交底、申请文件、检索、解读、OA 与政策简报，适合整仓按需安装，法律产出须人工复核 |

本轮新增三个一级仓库，并将既有 `graphify` 补成完整历史后，`E:\aimodel` 当前共有 93 个带 `.git` 的一级目录。四个仓库均未安装依赖、模型、MCP、Terraform CLI 或全局 Codex skills。

同日随后对 92 个可见一级仓库执行安全同步：43 个实际快进、47 个原本最新；`codetracer` 保留旧 `main` 后转到上游新默认 `stable`，`reverse-skill` 因本地修改跳过。完整版本号和例外状态见 [REPOSITORIES.md](REPOSITORIES.md)，维护方法见 [REPOSITORY_MANAGEMENT.md](REPOSITORY_MANAGEMENT.md)。

## 2026-09-03 PDF 与 HTML artifact 补充

| 仓库 | 来源 | HEAD | `SKILL.md` 数 | 状态与定位 |
|------|------|------|----------------|------|
| pdf-inspector | https://github.com/firecrawl/pdf-inspector.git | `65b7fa1` | 0 | 已浅克隆；Rust PDF 类型识别、原生文本转 Markdown 与逐页 OCR 路由工具，不作为 Skill 安装 |
| effective-html | https://github.com/plannotator/effective-html.git | `d95debb` | 6 | 已浅克隆；自包含 HTML 报告、设计方向、线框、交互原型、计划和关系图 Skills，含 Codex 插件结构但未安装 |
| andrej-karpathy-skills | https://github.com/multica-ai/andrej-karpathy-skills.git | `2c60614` | 1 | 既有克隆；与当前 Codex 行为规范高度重合，只保留参考 |
| mattpocock-skills | https://github.com/mattpocock/skills.git | `6654f6b` | 37 | 既有干净克隆；工程/生产力工作流适合按单项选用，不全量安装 |

本轮新增两个一级仓库后，`E:\aimodel` 当前共有 90 个带 `.git` 的一级目录。新增仓库只保存源码，没有安装依赖、OCR 运行时、全局 Skills 或 Codex 插件。

## 2026-08-29 LoopX 与 ego-lite 补充

| 仓库 | 来源 | HEAD | `SKILL.md` 数 | 状态与定位 |
|------|------|------|----------------|------|
| loopx | https://github.com/huangruiteng/loopx.git | `e227551` | 9（8 个正式 workflow skills + 1 个 demo worker skill） | 已浅克隆；长周期 Agent goal/todo/gate/evidence/quota 控制平面，不是浏览器或截图解析工具 |
| ego-lite | https://github.com/citrolabs/ego-lite.git | `5ca3c36` | 1 | 已浅克隆；`ego-browser` 语义 Snapshot、浏览器操作与截图捕获 Skill；当前浏览器应用仅 macOS，本机 Windows 未安装 |

两仓库均只保存源码和资料，没有安装依赖、全局 skills 或浏览器应用。浏览器控制、DOM/a11y Snapshot 与像素截图理解的能力边界见 [BROWSER_AUTOMATION_COMPARISON.md](BROWSER_AUTOMATION_COMPARISON.md)。一级第三方 Git 仓库当前为 84 个；下面的 2026-08-28 同步统计仍保留当日 82 个仓库的完整批次口径。

## 2026-08-28 一级仓库同步状态

| 检查项 | 数量 | 说明 |
|------|------:|------|
| 一级有效 Git 仓库 | 82 | skill 与 tool 一并检查，不递归处理嵌套仓库 |
| 快进更新 | 41 | 工作树干净、上游可用，执行 `git pull --ff-only` |
| 已是最新 | 39 | 本地 HEAD 已与上游一致 |
| 本地修改跳过 | 1 | `reverse-skill` 有 3 个修改文件 |
| 历史分叉保留 | 1 | `codetracer` 补全浅克隆历史后为 ahead 3 / behind 1521 |

`gortex` 的首次 TLS 传输失败已通过重试解决，当前 HEAD 为 `06939fc`。`codetracer` 没有执行 merge、rebase 或 reset；其 3 个旧开发线提交由上游作者创建，且与上游重排后的补丁不完全等价，需单独决定保留策略。

## 2026-08-28 学术科研 Skills 补充

| 仓库/目录 | 来源 | HEAD/快照 | `SKILL.md` 数 | 状态与定位 |
|------|------|------|----------------|------|
| scientific-agent-skills | https://github.com/K-Dense-AI/scientific-agent-skills.git | `36d8f13` | 163 | 已有仓库确认与远端一致；通用科学计算、数据库、生物医药与科研工作流大库 |
| nature-skills | https://github.com/Yuan1z0825/nature-skills.git | `205ed18` | 20（19 个可触发 + 1 个共享目录） | 已浅克隆；Nature 风格写作、绘图、文献检索、全文阅读、返修与专利工作流 |
| AI-Research-SKILLs | https://github.com/Orchestra-Research/AI-Research-SKILLs.git | `773a529` | 98 | 已浅克隆；AI/ML 研究工程、训练、推理、评测、RAG、论文写作与 autoresearch |
| claude-scholar | https://github.com/Galaxy-Dawn/claude-scholar.git | `6ed46da` | 45 | 已浅克隆；研究全生命周期、实验、写作、Zotero/Obsidian 与多 Agent 配置 |
| PaperSpine | https://github.com/WUBING2023/PaperSpine.git | `895f4e4` | 7 份物理文件（V4 逻辑 1 个编排 Skill） | 已浅克隆；贡献优先、证据约束、12 阶段论文构筑/重写与最终审计 |
| Awesome-Agent-Skills-for-Empirical-Research | https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git | `517717f` | 1,162 份物理文件；catalog 为 1,096 项 | 已从旧地址快进更新；76 个合集、9 阶段社会科学实证流水线；子模块固定在 `110e7c6` |
| multi-search-engine | https://github.com/aAAaqwq/AGI-Super-Team/tree/main/skills/multi-search-engine | SHA-256 `aba6bcf…` | 1 | 独立快照；实际列出 16 个引擎，上游缺失 `config.json`，无 frontmatter/执行代码，只作搜索 URL 路由参考 |

本批只保存仓库或独立 Skill 快照，不安装 Python/R/Stata/LaTeX 依赖，不配置 API key、MCP 或全局 Codex skills。AERS 根许可证为 CC BY-SA 4.0，但其 vendor 的第三方合集仍需逐项遵守上游许可证。

## 2026-08-25 科研 skills 补全结果

| 仓库 | 来源 | HEAD | `SKILL.md` 数 | 状态 |
|------|------|------|----------------|------|
| scientific-agent-skills | https://github.com/K-Dense-AI/scientific-agent-skills.git | `36d8f13` | 163（本地一级目录） | 已完整检出；2446 个跟踪文件无缺失，HEAD 与 `origin/main` 一致，工作树干净。仓库结构契约已验证；未安装依赖或全局 skills。 |

验证说明：仓库 `_meta` 的 9 项平台无关规则通过；Windows 不呈现 POSIX 执行位，因此另从 Git 索引确认两份 `.sh` 为 `100755`，并用 Git Bash 执行 `bash -n` 通过。按任务选择技能，使用前检查相应 `SKILL.md`、依赖、凭据和许可证。

### 科研任务路由

| 任务 | 优先读取 | 使用边界 |
|------|----------|----------|
| 系统检索与证据综合 | `literature-review` | 先冻结问题、数据库、时间窗和纳排标准；结论回链原论文 |
| 已知标题、DOI 或论文定位 | `paper-lookup` | 用于解析标识符和查找正文入口，不把聚合页当最终证据 |
| 跨来源研究资料查询 | `research-lookup` | 适合探索性检索；正式结论再核对论文、标准或官方数据库 |
| 学科数据库与结构化事实 | `database-lookup` | 按目标数据库配置凭据和速率限制，记录查询式与访问日期 |
| 假设、偏差与因果审查 | `scientific-critical-thinking` | 检查混杂、替代解释、可证伪性和外推边界，不替代领域专家判断 |
| 统计方案与结果解释 | `statistical-analysis` | 先核对研究设计、缺失机制、效应量和不确定性，避免只报告显著性 |
| 稿件或研究方案评议 | `peer-review` | 区分致命问题、主要问题和次要问题，保持可复核证据链 |

以上只是常用入口，不代表已经安装或授权其外部服务。若技能需要 API key、联网数据库、付费数据或专用科研软件，先按具体任务检查配置与许可，不在根目录统一安装。

### 参考仓库

| 仓库 | 来源 | HEAD | 说明 |
|------|------|------|------|
| developer-portfolios | https://github.com/emmabostian/developer-portfolios.git | `89f6044` | 已浅克隆；开发者作品集案例参考，不属于 skill。 |

## 一级目录台账

### 已更新的 Git skill 仓库（35）

| 仓库 | 来源 | HEAD | SKILL.md 数 | 状态 |
|------|------|------|------------|------|
| agent-rules-books | https://github.com/ciembor/agent-rules-books.git | `9c87636` | 0 | 已更新 |
| agent-skills | https://github.com/addyosmani/agent-skills.git | `f63ec56` | 24 | 已更新 |
| AI-Research-SKILLs | https://github.com/Orchestra-Research/AI-Research-SKILLs.git | `773a529` | 98 | 已浅克隆，工作树干净 |
| andrej-karpathy-skills | https://github.com/multica-ai/andrej-karpathy-skills.git | `2c60614` | 1 | 已更新 |
| anthropic-skills | https://github.com/anthropics/skills.git | `3b3fad9` | 20 | 已更新 |
| avoid-ai-writing | https://github.com/conorbronsdon/avoid-ai-writing.git | `40328bd` | 2 | 已更新 |
| Awesome-Agent-Skills-for-Empirical-Research | https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git | `517717f` | 1162（catalog 1096） | 已快进更新；Paper-WorkFlow 子模块固定到 `110e7c6` |
| caveman-full | https://github.com/JuliusBrussee/caveman.git | `17f9f2e` | 24 | 已更新 |
| claude-guides-full | https://github.com/vtroisWhite/andrej-karpathy-skills.git | `54a3028` | 1 | 已更新 |
| claude-scholar | https://github.com/Galaxy-Dawn/claude-scholar.git | `6ed46da` | 45 | 已浅克隆，工作树干净 |
| claude-skill-refactoring-ui | https://github.com/opkod-france/claude-skill-refactoring-ui.git | `80994d9` | 1 | 已更新 |
| claude-video | https://github.com/bradautomates/claude-video.git | `83da59f` | 1 | 已更新 |
| ego-lite | https://github.com/citrolabs/ego-lite.git | `5ca3c36` | 1 | 已浅克隆；浏览器应用当前仅 macOS，本机未安装 |
| hallmark | https://github.com/Nutlope/hallmark.git | `13ac0ec` | 1 | 已更新 |
| Humanizer-zh | https://github.com/op7418/Humanizer-zh.git | `91f3d39` | 1 | 已更新 |
| human-writing | https://github.com/KKKKhazix/human-writing.git | `4fda173` | 1 | 已更新 |
| hyperframes | https://github.com/heygen-com/hyperframes.git | `10a9068` | 32 | 已更新 |
| khazix-skills | https://github.com/KKKKhazix/khazix-skills.git | `7a5c493` | 6 | 已更新 |
| knowledge-work-plugins | https://github.com/anthropics/knowledge-work-plugins.git | `6d223a7` | 212 | 已更新 |
| last30days-skill | https://github.com/mvanhorn/last30days-skill.git | `a218eda` | 1 | 已更新 |
| loopx | https://github.com/huangruiteng/loopx.git | `e227551` | 9（8 正式 + 1 demo） | 已浅克隆；长周期 Agent 控制平面 |
| markdown-viewer-skills | https://github.com/markdown-viewer/skills.git | `a3afd45` | 15 | 已更新 |
| mattpocock-skills | https://github.com/mattpocock/skills.git | `6654f6b` | 37 | 已更新 |
| minimax-skills | https://github.com/MiniMax-AI/skills.git | `60aaae5` | 23 | 已更新 |
| nature-skills | https://github.com/Yuan1z0825/nature-skills.git | `205ed18` | 20（19 + shared） | 已浅克隆，工作树干净 |
| obsidian-skills | https://github.com/kepano/obsidian-skills.git | `a1dc48e` | 5 | 已更新 |
| PaperSpine | https://github.com/WUBING2023/PaperSpine.git | `895f4e4` | 7（V4 逻辑 1） | 已浅克隆，工作树干净；含多宿主副本与 V5 RC 文件 |
| python-refactoring-skills | https://github.com/l-mb/python-refactoring-skills.git | `b083571` | 8 | 已更新 |
| scientific-agent-skills | https://github.com/K-Dense-AI/scientific-agent-skills.git | `36d8f13` | 163 | 已完整检出并验证 |
| superpowers-repo | https://github.com/obra/superpowers.git | `b36e082` | 14 | 已更新 |
| taste-skill | https://github.com/Leonxlnx/taste-skill.git | `ccbc156` | 13 | 已更新 |
| ui-ux-pro-max-skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git | `8bd29e7` | 13 | 已更新 |
| vue-skills-full | https://github.com/vuejs-ai/skills.git | `c9d355f` | 8 | 已更新 |
| web-access | https://github.com/eze-is/web-access.git | `33eef84` | 1 | 已更新 |
| z-skills | https://github.com/tjxj/z-skills.git | `50539dc` | 17 | 已更新 |

### 已发现但跳过的 Git skill 仓库

| 仓库 | 来源 | HEAD | SKILL.md 数 | 状态 |
|------|------|------|------------|------|
| reverse-skill | https://github.com/zhaoxuya520/reverse-skill.git | `a5171e0` | 84 | 跳过更新（本地有 3 个修改） |

### 本地 skill 包 / 非 Git

| 目录 | SKILL.md 数 | 说明 |
|------|------------|------|
| backend-skills | 22 | 本地 skill 包 |
| codex-skills | 880 | 本地 skill 包 |
| multi-search-engine | 1 | 上游单文件快照；缺少其声明的 `config.json`，且无 YAML frontmatter，只作 URL 模板参考 |
| zhihu-cli-skill | 1 | 本地 skill 包 |

### 搜索与下载

```powershell
Get-ChildItem E:\aimodel -Directory | Where-Object { Test-Path (Join-Path $_.FullName '.git') }
rg --files E:\aimodel -g 'SKILL.md' -g '!**/node_modules/**'
rg -n "关键词" E:\aimodel -g 'SKILL.md' -g 'README.md'
git -c safe.directory=E:/aimodel/<repo> -C E:\aimodel\<repo> pull --ff-only
git clone --depth 1 <url> E:\aimodel\<repo>
```

---

## 历史索引（旧记录，保留参考）

下面是旧版分类台账，统计数字不再作为当前维护依据。

## 📦 已克隆仓库分类（顶层 GitHub 仓库 61 个）

2026-08-28 全目录同步后重新扫描到 `SKILL.md` 4,492 个；Claude/Codex 插件清单 90 个仍是旧版历史口径，未在本批重算。GitHub star 手动清单见 [GITHUB_STAR_LIST.md](GITHUB_STAR_LIST.md)。

### 🔧 开发方法论

| 仓库 | 来源 | 说明 |
|------|------|------|
| superpowers-repo | https://github.com/obra/superpowers | TDD、系统化调试、子代理开发 |
| awesome-agent-skills | https://github.com/JackyST0/awesome-agent-skills | Agent技能精选列表 |
| awesome-claude-skills | https://github.com/travisvn/awesome-claude-skills | Claude技能精选列表 |

### 🎨 UI/UX设计

| 仓库 | 来源 | 说明 |
|------|------|------|
| ui-ux-pro-max-skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | UI/UX最佳实践技能 |
| claude-skill-refactoring-ui | https://github.com/opkod-france/claude-skill-refactoring-ui | UI重构技能 |
| hallmark | https://github.com/Nutlope/hallmark | 反 AI 味 UI 设计 skill，支持新页面、审计、重设计和从 URL/截图提取设计 DNA |

### 📝 代码质量

| 仓库 | 来源 | 说明 |
|------|------|------|
| code-review-plugin | https://github.com/anthropics/claude-plugins-official | 代码审查插件 |
| python-refactoring-skills | https://github.com/l-mb/python-refactoring-skills | Python重构技能 |
| SmeLLM | https://github.com/refactoring-assistant/SmeLLM | 代码坏味道检测+自动重构 |

### 🧪 测试相关

| 仓库 | 来源 | 说明 |
|------|------|------|
| anthropic-skills | https://github.com/anthropics/skills | 包含webapp-testing, pptx等技能 |
| ai-unit-tests-generator | https://github.com/gustavolopess/ai-unit-tests-generator | AI自动生成单元测试 |

### 🛠️ 工具类

| 仓库 | 来源 | 说明 |
|------|------|------|
| skills-compat-manager | https://github.com/hnaymyh123-henry/skills-compat-manager | 跨平台技能兼容层 |
| skillsProject-AI-Log-Analyzer | https://github.com/sahanaydn/skillsProject-AI-Log-Analyzer | 日志分析技能 |
| SafeGuard-Code-Profiler | https://github.com/hamed-kuheil/SafeGuard-Code-Profiler | 性能瓶颈分析器 |
| WebSecurityScanner | https://github.com/Defensive-Alliance/WebSecurityScanner | 安全漏洞扫描器 |
| mermaid-erd-generator | https://github.com/nharsch/mermaid-erd-generator | ER图生成器(Mermaid) |
| pipeforge | https://github.com/Sheraz-k/pipeforge | CI/CD流水线配置生成器 |
| SupplyChainScanner | https://github.com/benjiamin911/SupplyChainScanner | 依赖管理+漏洞扫描 |
| scramble | https://github.com/dedoc/scramble | OpenAPI/Swagger文档生成器 |

### 🎓 学术研究

| 仓库 | 来源 | 说明 |
|------|------|------|
| Awesome-Agent-Skills-for-Empirical-Research | https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills | 社会科学实证研究聚合库（当前 canonical catalog：76 个合集、1,096 项） |
| Humanizer-zh | https://github.com/op7418/Humanizer-zh | 中文AI写作去痕工具 |

### 📊 图表生成 (NEW 2026-05-09)

| 仓库 | 来源 | 说明 | 技能数 |
|------|------|------|--------|
| markdown-viewer-skills | https://github.com/markdown-viewer/skills | Markdown图表生成技能集 | 14 skills |

**包含技能**: vega(数据图表), infographic(70+模板), canvas(思维导图), uml, cloud, network, security, archimate, bpmn, data-analytics, iot, mindmap, architecture, infocard

### 💻 开发工具集 (NEW 2026-05-09)

| 仓库 | 来源 | 说明 | 技能数 |
|------|------|------|--------|
| minimax-skills | https://github.com/MiniMax-AI/skills | MiniMax AI开发工具集 | 17+ skills |

**包含技能**: frontend-dev, fullstack-dev, android-native-dev, ios-application-dev, flutter-dev, react-native-dev, shader-dev, minimax-pdf, pptx-generator, minimax-xlsx, minimax-docx, minimax-multimodal-toolkit, minimax-music-gen, vision-analysis

### 📚 编程书籍规则 (NEW 2026-05-09)

| 仓库 | 来源 | 说明 |
|------|------|------|
| agent-rules-books | https://github.com/ciembor/agent-rules-books | 经典编程书籍AI规则提取 |

**包含书籍**: Clean Code, Clean Architecture, Designing Data-Intensive Applications, Domain-Driven Design, Refactoring, The Pragmatic Programmer等15+本

### 🔍 研究工具 (NEW 2026-05-09)

| 仓库 | 来源 | 说明 | 状态 |
|------|------|------|------|
| last30days-skill | https://github.com/mvanhorn/last30days-skill | GitHub Trending #1 - 跨平台30天内容搜索引擎 | ✅ 已安装 |

**功能**: Reddit upvotes, X likes, YouTube transcripts, TikTok engagement, Polymarket odds, Hacker News, GitHub

---

## 🧭 第一批新增仓库 / 待配置 (NEW 2026-07-19)

详见: [GITHUB_REPOS.md](GITHUB_REPOS.md)

| 仓库 | 来源 | 本地目录 | 说明 | 状态 |
|------|------|----------|------|------|
| playcaptcha | https://github.com/mortspace/playcaptcha | `E:\aimodel\playcaptcha\` | React 可玩 CAPTCHA 组件，适合前端表单防滥用 | 已克隆，低优先级配置 |
| gortex | https://github.com/zzet/gortex | `E:\aimodel\gortex\` | 面向 AI 编码代理的仓库索引、语义搜索和代码理解工具 | 已克隆，高优先级配置 |
| liteparse | https://github.com/run-llama/liteparse | `E:\aimodel\liteparse\` | LlamaIndex 生态 PDF/文档解析工具，支持 CLI/库/skill | 已克隆，中优先级配置 |
| crawl4ai | https://github.com/unclecode/crawl4ai | `E:\aimodel\crawl4ai\` | LLM 友好网页爬取与 Markdown/结构化抽取工具 | 已克隆，高优先级配置 |
| OpenCLI | https://github.com/jackwener/OpenCLI | `E:\aimodel\OpenCLI\` | 自然语言浏览器自动化 CLI，依赖本机 Chrome 登录态 | 已克隆，中优先级配置 |
| browser-use | https://github.com/browser-use/browser-use | `E:\aimodel\browser-use\` | AI 浏览器自动化框架，支持多种 agent 和 skill 入口 | 已克隆，高优先级配置 |

---

## 🧩 第二批新增仓库 / 待配置 (NEW 2026-07-19)

详见: [GITHUB_REPOS.md](GITHUB_REPOS.md)

| 仓库 | 来源 | 本地目录 | 说明 | Skill/插件 |
|------|------|----------|------|------------|
| knowledge-work-plugins | https://github.com/anthropics/knowledge-work-plugins | `E:\aimodel\knowledge-work-plugins\` | Claude 知识工作插件集 | 212 SKILL.md / 22 插件 |
| headroom | https://github.com/headroomlabs-ai/headroom | `E:\aimodel\headroom\` | 压缩工具输出、日志和 RAG chunks，降低 LLM token 输入 | 1 插件 |
| mattpocock-skills | https://github.com/mattpocock/skills | `E:\aimodel\mattpocock-skills\` | 真实工程师工程/生产力技能库 | 41 SKILL.md / 1 插件 |
| andrej-karpathy-skills | https://github.com/multica-ai/andrej-karpathy-skills | `E:\aimodel\andrej-karpathy-skills\` | Karpathy 风格 Claude/Cursor 行为指南 | 1 SKILL.md / 1 插件 |
| skillspector | https://github.com/NVIDIA/skillspector | `E:\aimodel\skillspector\` | AI agent skill 安全扫描器 | 23 SKILL.md |
| z-skills | https://github.com/tjxj/z-skills | `E:\aimodel\z-skills\` | 可复用 Claude skill 集合 | 10 SKILL.md |
| claude-video | https://github.com/bradautomates/claude-video | `E:\aimodel\claude-video\` | 给 Claude 增加视频下载、抽帧、转写和分析能力 | 1 SKILL.md / 2 插件 |
| taste-skill | https://github.com/Leonxlnx/taste-skill | `E:\aimodel\taste-skill\` | UI/视觉审美和反通用化输出 skill | 13 SKILL.md / 1 插件 |
| awesome-llm-apps | https://github.com/Shubhamsaboo/awesome-llm-apps | `E:\aimodel\awesome-llm-apps\` | 可运行的 LLM、RAG、Agent 应用合集 | 6 SKILL.md |
| multi-style-image-generator | https://github.com/powerycy/multi-style-image-generator | `E:\aimodel\multi-style-image-generator\` | 多风格图像生成和 360 全景预览 skill | 1 SKILL.md |
| Agent-Reach | https://github.com/Panniantong/Agent-Reach | `E:\aimodel\Agent-Reach\` | 多平台网页读取/搜索 CLI，无需平台 API | 1 SKILL.md |
| hallmark | https://github.com/Nutlope/hallmark | `E:\aimodel\hallmark\` | 反 AI 味 UI 设计 skill，已安装到 Codex skills | 1 SKILL.md |

---

## 📋 技能搜索完成清单

| 技能名 | 说明 | 仓库 | 状态 |
|--------|------|------|------|
| Refactoring Assistant | 重构助手 | SmeLLM | ✅ |
| Unit Test Generator | 单元测试生成器 | ai-unit-tests-generator | ✅ |
| API Documentation Generator | API文档生成器 | scramble | ✅ |
| Performance Analyzer | 性能分析器 | SafeGuard-Code-Profiler | ✅ |
| Security Scanner | 安全漏洞扫描 | WebSecurityScanner | ✅ |
| Database Migration Generator | 数据库迁移 | mergration | ✅ |
| Pipeline Configurator | 流水线配置 | pipeforge | ✅ |
| Dependency Manager | 依赖管理 | SupplyChainScanner | ✅ |
| ER Diagram Generator | ER图生成器 | mermaid-erd-generator | ✅ |
| Log Analyzer | 日志分析器 | skillsProject-AI-Log-Analyzer | ✅ |
| Chart Generator | 图表生成器 | markdown-viewer-skills | ✅ NEW |
| Multimodal Toolkit | 多模态AI工具集 | minimax-skills | ✅ NEW |
| 30-Day Research | 30天内容研究 | last30days-skill | ✅ NEW |
| Books Rules | 编程书籍规则 | agent-rules-books | ✅ NEW |
| Browser Automation | AI浏览器自动化 | browser-use / OpenCLI | 已克隆 NEW |
| Code Intelligence | AI代码理解索引 | gortex | 已克隆 NEW |
| Web Crawler for LLM | LLM网页爬取 | crawl4ai | 已克隆 NEW |
| PDF Parser | PDF/文档解析 | liteparse | 已克隆 NEW |
| CAPTCHA Component | React验证码组件 | playcaptcha | 已克隆 NEW |
| Knowledge Work Plugins | 知识工作插件集 | knowledge-work-plugins | 已克隆 NEW |
| Token Compression | LLM输入压缩 | headroom | 已克隆 NEW |
| Skill Security Scanner | AI skill安全扫描 | skillspector | 已克隆 NEW |
| Video Understanding | 视频理解skill | claude-video | 已克隆 NEW |
| Design Taste | 审美/设计品味skill | taste-skill | 已克隆 NEW |
| LLM Apps Collection | LLM/RAG/Agent应用合集 | awesome-llm-apps | 已克隆 NEW |
| Multi-style Image | 多风格图像生成 | multi-style-image-generator | 已克隆 NEW |
| Web Reach CLI | 多平台网页读取搜索 | Agent-Reach | 已克隆 NEW |
| Anti-AI-slop Design | 反 AI 味 UI 设计/审计/重设计 | hallmark | 已克隆并安装 NEW |
| PDF OCR Router | PDF 类型识别、Markdown 抽取与逐页 OCR 路由 | pdf-inspector | 已浅克隆 NEW |
| Effective HTML | 单文件 HTML 报告、线框、原型、计划与关系图 | effective-html | 已浅克隆，未全局安装 NEW |

---

## 📂 技能目录结构

```
E:\aimodel\
├── superpowers-repo/          # 13个核心技能
├── anthropic-skills/skills/   # 官方技能
├── SmeLLM/                    # 重构助手
├── ai-unit-tests-generator/   # 单元测试生成
├── SafeGuard-Code-Profiler/   # 性能分析
├── WebSecurityScanner/        # 安全扫描
├── mermaid-erd-generator/     # ER图生成
├── pipeforge/                 # CI/CD配置
├── SupplyChainScanner/        # 依赖管理
├── scramble/                  # API文档
├── markdown-viewer-skills/   # 图表生成 (NEW)
│   ├── uml/                   # UML图
│   ├── cloud/                 # 云架构
│   ├── network/               # 网络拓扑
│   ├── security/              # 安全架构
│   ├── vega/                  # 数据图表
│   ├── infographic/           # 信息图
│   └── ...                    # 共14个技能
├── minimax-skills/            # 开发工具集 (NEW)
│   ├── frontend-dev/          # 前端开发
│   ├── fullstack-dev/         # 全栈开发
│   ├── android-native-dev/    # Android开发
│   ├── minimax-pdf/           # PDF生成
│   ├── minimax-docx/          # Word文档
│   └── ...                    # 共17+个技能
├── agent-rules-books/         # 编程书籍规则 (NEW)
│   ├── clean-code/            # Clean Code规则
│   ├── clean-architecture/    # 清洁架构
│   ├── refactoring/            # 重构
│   └── ...                    # 共15+本
├── last30days-skill/          # 研究工具 (NEW)
└── ...
```

---

## 🚀 快速使用

### 图表生成
```bash
cd E:\aimodel\markdown-viewer-skills
# 支持14种图表类型，使用PlantUML、Vega-Lite等渲染
```

### 多模态AI开发
```bash
cd E:\aimodel\minimax-skills
# 前端开发、移动开发、文档生成、音乐生成等
```

### 30天内容研究
```bash
# Claude Code中执行
/last30days <主题>
# 搜索Reddit、X、YouTube、TikTok等平台最近30天内容
```

### 编程书籍规则
```bash
cd E:\aimodel\agent-rules-books
# Clean Code、Refactoring等经典书籍的AI规则
```

---

**记录人**: liuhao
**记录时间**: 2026-05-09 16:00:00

---

## 🧩 第三批新增仓库 / 工具（NEW 2026-07-30）

详见: [GITHUB_REPOS.md](GITHUB_REPOS.md)

| 仓库 | 来源 | 本地目录 | 说明 | Skill/插件 |
|------|------|----------|------|------------|
| inspira-ui | https://github.com/rahulv-official/inspira-ui | `E:\aimodel\inspira-ui\` | Vue/Nuxt 组件集合，适合构建高质感前端页面 | 0 SKILL.md / 0 插件 |
| kepano-obsidian | https://github.com/kepano/kepano-obsidian | `E:\aimodel\kepano-obsidian\` | Obsidian vault 模板，与 obsidian-skills 配套 | 0 SKILL.md / 0 插件 |
| obsidian-skills | https://github.com/kepano/obsidian-skills | `E:\aimodel\obsidian-skills\` | Obsidian Markdown、Bases、Canvas、CLI 和 Defuddle skills | 5 SKILL.md / 1 插件 |
| pi | https://github.com/earendil-works/pi | `E:\aimodel\pi\` | Pi Agent Harness，包含 coding agent、agent runtime、LLM API 和 TUI 包 | 17 SKILL.md（测试夹具为主）/ 0 插件 |
| vue-tui | https://github.com/Simon-He95/vue-tui | `E:\aimodel\vue-tui\` | Simon He 的 Vue 3 terminal UI toolkit，支持 DOM、CLI stdout 和 headless tests | 1 SKILL.md / 0 插件 |

### 第三批技能搜索补充

| 技能名 | 说明 | 仓库 | 状态 |
|--------|------|------|------|
| Obsidian Markdown | 创建和编辑 Obsidian Flavored Markdown | obsidian-skills | 已克隆 |
| Obsidian Bases | 创建和编辑 `.base` 文件 | obsidian-skills | 已克隆 |
| JSON Canvas | 创建和编辑 `.canvas` 文件 | obsidian-skills | 已克隆 |
| Obsidian CLI | 通过 Obsidian CLI 操作 vault、插件和主题 | obsidian-skills | 已克隆 |
| Defuddle | 网页内容清洗为 Markdown | obsidian-skills | 已克隆 |
| Vue TUI | Vue 终端 UI 开发和评审 | vue-tui | 已克隆 |

---

## 2026-08-15 第四批技能与参考仓库

### 正式 skill 仓库

| 仓库 | Skill 数量 | 主要内容 | 本地目录 | 状态 |
|------|------------|----------|----------|------|
| emilkowalski/skills | 10 | 动效设计、动画审查、设计原则、UI 库选择、原型 | `E:\aimodel\emilkowalski-skills\` | 已克隆 |

包含：`emil-design-eng`、`animate`、`review-animations`、`improve-animations`、`find-animation-opportunities`、`animation-vocabulary`、`apple-design`、`pick-ui-library`、`prototype`、`ask-sonner`。

### 非标准 skill / 工具与研究仓库

| 仓库 | 形态 | 用途 | 状态 |
|------|------|------|------|
| StarTrail-org/LEANN | OpenClaw `claw.json + instructions.md` | 本地语义记忆、RAG、MCP 搜索 | 已克隆；不计入标准 `SKILL.md` |
| nexu-io/open-design | 设计工具仓库，包含大量子目录 skills | 设计系统、插件、原型和媒体产物 | 已同步；不递归更新子目录 |
| earendil-works/pi | Agent Harness | coding agent、agent runtime、LLM API、TUI | 已同步；测试夹具中的 skill 不计入正式集合 |
| Zenghuang-Fu/SESA-Self-Evolving-Search-Agents | 研究代码 | proposer/solver 自博弈、Skill Bank、失败到 skill 演化 | 已克隆 |
| bobeff/open-source-games | README 索引 | 按游戏类型寻找开源项目和实现案例 | 已克隆，参考用途 |
| codecrafters-io/build-your-own-x | README 教程索引 | 从零实现 AI、搜索引擎、游戏、Git、Web 服务等 | 已克隆，参考用途 |

### 论文资料

- `arxiv-2607.29468v1.pdf`: SESA，关注自博弈与 skill memory 的闭环耦合。
- `arxiv-2607.27733v1.pdf`: VeriSkill，关注程序验证中的失败归因、模式级 lesson 和验证准入。

本批不把仓库子目录中的 `SKILL.md` 拆成一级仓库，也不自动安装任何依赖。

---

## 2026-08-15 其他 skill 仓库更新

### 更新统计

| 状态 | 数量 |
|------|------|
| 已快进更新 | 26 |
| 已是最新 | 15 |
| 因本地修改跳过 | 1（`reverse-skill`） |

### 新登记的仓库链接

| 仓库 | Skill 数量 | 定位 | 本地目录 |
|------|------------|------|----------|
| [different-ai/openwork](https://github.com/different-ai/openwork) | 33 | 跨 Agent 工作区、MCP、skill/plugin 共享 | `E:\aimodel\openwork\` |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 1 | 代码和文档知识图谱，提供 `/graphify` | `E:\aimodel\graphify\` |

其他一级仓库的远程链接已在现有台账中找到；本轮没有发现更多漏登记的 GitHub 仓库。

---

## 2026-08-17 第五批设计 skill 与参考仓库

| 仓库 | 类型 | HEAD | 本地目录 | SKILL.md / 参考数量 | 状态 |
|------|------|------|----------|--------------------|------|
| ui-ux-pro-max-skill | UI/UX skill/plugin | `a38d04c` | `E:\aimodel\ui-ux-pro-max-skill\` | 6 | 已快进更新 |
| awesome-design-md | `DESIGN.md` 设计系统参考库 | `8147538` | `E:\aimodel\awesome-design-md\` | 0 / 73 | 已克隆；不计入正式 skill |

`awesome-design-md` 只作为设计参考资料存放，不递归纳入 `SKILL.md` 统计，也不安装依赖。
