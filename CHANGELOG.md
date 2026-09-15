# AI开发资源库下载完成记录

**@author liuhao**
**日期**: 2026-05-01
**时间**: 14:00:00
**类型**: 资源整理

---

## 2026-09-15 代码审查、下载工具与手绘风格候选

- 浅克隆 `alibaba/open-code-review` 到 `E:\aimodel\open-code-review\`，HEAD `55899906`；确认 Apache-2.0、4 个物理 `SKILL.md`（2 个逻辑 Skill 在源码与插件目录中各保留一份），本轮未安装 `ocr` 或配置模型。
- 浅克隆 `XiaoYouChR/Ghost-Downloader-3` 到 `E:\aimodel\Ghost-Downloader-3\`，HEAD `601e2068`；补齐父仓库锁定的 `xifangczy/cat-catch@b34a7677` 子模块。项目为 GPL-3.0 的 Python/PySide6 多协议下载器，本轮未安装依赖、浏览器扩展或桌面程序。
- 仅登记 `yang0/handraw-style`：审查时 HEAD `70bf51d6`，含 1 个提示词 Skill；仓库未提供许可证文件，且 340 个跟踪文件的浅克隆约 195.1 MiB，因此移除临时审查副本，不在本目录长期镜像。
- 扫描发现此前只登记的 `3b1b/manim` 已在根目录存在 `master@fafa083a` 浅克隆；保留现状并补入一级仓库台账，没有改动其工作树。
- 两个新增父仓库工作树干净并通过 `git fsck --no-reflogs`；更新 `REPOSITORIES.md`、`SKILLS_INDEX.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md` 和本变更记录。一级目录现为 101 个可见第三方仓库加 1 个隐藏聚合仓库。
- 本轮未执行第三方代码、安装依赖或全局 Skill，也未向第三方仓库推送。

---

## 2026-09-14 UI 组件库、动效 Skill 与写作 Skill

- 浅克隆 `rare-ui`、`shadcn-ui`、`beautiful-ui`、`beui`、`transitions-dev` 和 `no-ai-slop` 到 `E:\aimodel\`；6 个仓库均为干净工作树并通过 `git fsck --no-reflogs`。
- 核实站点与源码映射：Beautiful UI 对应 `slev12397/beautiful-ui`，beUI 对应 `starc007/ui-components`，Transitions.dev 对应 `Jakubantalik/transitions.dev`。
- `shadcn-ui` 含 2 个 Agent Skill，`beui` 含公开与 Pro 两个 Skill，`transitions-dev` 含 3 个 Skill，`no-ai-slop` 含 1 个 Skill 和 Codex 插件清单；本轮均未安装到全局 Skills，也未安装 npm/bun 依赖。
- 仅登记 `jbiaojerry/ebook-treasure-chest`：其内容主要是第三方电子书下载链接，页面未显示明确许可证，未在本地镜像。
- 按要求仅登记 `3b1b/manim`；它是 ManimGL 源码，官方提醒不要与 Manim Community 版安装说明混用。
- 更新 `REPOSITORIES.md`、`SKILLS_INDEX.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md` 和本变更记录；一级带 `.git` 的目录数由 93 增至 99。
- 确认聚合仓库远端为 `https://github.com/xiaohaoyiqu/skill-and-tool.git`，实际 Git 元数据位于 `.skill-and-tool-upload/.git`，工作树指向 `E:\aimodel`。

---

## 2026-09-06 Java 升级、可观测性与数据存储索引

- 在 `README.md`、`SKILLS_INDEX.md` 与 `REPOSITORY_MANAGEMENT.md` 补充 Java/Spring 升级、Java Agent、HBase 和新增分析存储的资料路由与安全边界。
- 明确 OpenTelemetry、HBase、ClickHouse、gortex 守护进程和 Graphify 索引均未因索引更新而安装、启动或接入任何项目。
- 索引仅指向现有本地技能和工具；实际技术选型应以目标项目的兼容、性能、敏感数据、恢复和回滚验证为准。

---

## 2026-09-05 Graphify、zvec-grep、Terraform 与中国专利 Skill

- 新增 `scripts/Sync-RepositoryCatalog.ps1` 安全同步脚本和 `REPOSITORY_MANAGEMENT.md` 使用说明；脚本默认只检查，`-Pull` 时仅 fast-forward，跳过本地修改/无 upstream 仓库，不修改全局 Git 配置，并对 JSON 中的 HTTP 凭据脱敏。
- 使用脚本扫描并更新 92 个可见一级仓库：43 个实际快进、47 个原本最新；三次 GitHub TLS 中断经 HTTP/1.1 重试全部恢复。
- `codetracer` 上游删除旧 `main` 并改用 `stable`；本轮保留含 3 个独有提交的本地 `main`，新建并切换到 `stable`（`0478cb4f`），刷新 origin HEAD 和全分支 fetch refspec。
- `reverse-skill` 有 3 个本地修改且远端发生强制更新，当前 ahead 1 / behind 142；仅 fetch 远程引用，未 pull 或改写用户内容。
- `Awesome-Agent-Skills-for-Empirical-Research` 的 `Paper-WorkFlow` 子模块已按父仓库锁定值更新到 `ca36e316`，最终工作树干净。
- 将既有 `Graphify-Labs/graphify` 从单分支浅克隆补齐为完整历史，快进到 `937e59a5`，补齐全部远程分支和 202 个 tags，并将 fetch refspec 改为持续跟踪所有远程分支。
- 完整克隆 `zvec-ai/zvec-grep`、`hashicorp/terraform`、`handsomestWei/patent-disclosure-skill` 到 `E:\aimodel\`；HEAD 分别为 `52653951`、`7b8c301b`、`a0156905`。
- 四个仓库均为非浅、非 partial clone，工作树干净且与 upstream 为 0/0；无 Git submodule/LFS 跟踪项，并通过 `git fsck --full --no-reflogs`。
- 本地核实 Graphify `0.9.54` 为关系/调用链知识图谱工具；zvec-grep `0.2.1` 为支持 Codex 的本地混合检索 CLI/MCP；Terraform 是 BSL 1.1 的 IaC 核心源码而非 Skill；专利仓库含 1 个可调用路由 Skill 和 6 个内部子技能。
- 评估结论：Graphify 与 zvec-grep 能互补保留；Terraform 完整历史适合源码考古但约占 388 MiB；专利 Skill 适合整仓按需安装，真实法律文稿必须人工复核。
- 更新 `REPOSITORIES.md`、`SKILLS_INDEX.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md` 和本变更记录；一级带 `.git` 的目录数由 90 增至 93。
- 本轮未安装依赖、模型、浏览器运行时、MCP、Terraform CLI 或全局 Codex skills，也未执行仓库代码。

---

## 2026-09-03 PDF Inspector、Effective HTML 与既有 Skills 复核

- 将 `firecrawl/pdf-inspector` 和 `plannotator/effective-html` 以 `--depth 1` 克隆到 `E:\aimodel\pdf-inspector\`、`E:\aimodel\effective-html\`；HEAD 分别为 `65b7fa15`、`d95debba`，工作树干净并通过 `git fsck --no-reflogs`。
- 本地核实 `pdf-inspector` 版本 `1.17.0`、Rust `1.88`、Python `>=3.8`。它不是 Skill，而是 PDF 类型识别、原生文本转结构化 Markdown 和逐页 OCR 路由工具；默认构建不带 OCR，完整 OCR 另需 PDFium、ONNX Runtime 和模型。
- 本地核实 `effective-html` 含 6 个 `SKILL.md` 和版本 `0.4.0` 的 Codex 插件清单，覆盖通用 HTML artifact、设计方向、线框、交互原型、计划和关系图；本轮只保存仓库，没有安装到全局 Skills 或 Codex 插件。
- 复核既有 `andrej-karpathy-skills` 和 `mattpocock-skills`，两者均已有干净的顶层克隆，故未重复下载或全量安装；前者与当前 Codex 行为规范高度重合，后者当前本地共有 37 个 `SKILL.md`，适合按单项选用。
- 更新 `REPOSITORIES.md`、`SKILLS_INDEX.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md` 和本变更记录；当前一级带 `.git` 的目录数为 90。
- 两个新增目录触发 Windows Git 所有权保护；核查仅使用命令级 `safe.directory` 例外，没有修改全局 Git 配置。项目方性能基准没有在本机复跑。

---

## 2026-08-29 LoopX、ego-lite 下载与浏览器/截图能力复核

- 将 `huangruiteng/loopx` 和 `citrolabs/ego-lite` 以 `--depth 1` 克隆到 `E:\aimodel\loopx\`、`E:\aimodel\ego-lite\`；HEAD 分别为 `e2275510`、`5ca3c36c`，工作树均干净并与 `origin/main` 一致。
- 本地核实 `loopx` 版本 `0.5.3`、Python `>=3.11`、9 份物理 `SKILL.md`（8 正式 + 1 demo）；它是长周期 Agent 控制平面，不是浏览器或截图解析器。
- 本地核实 `ego-lite` 含 1 个 `ego-browser` Skill 和开源 TypeScript/CDP harness；浏览器应用本身不在仓库源码内，当前仅 macOS 可用，本机 Windows 未安装或运行。
- 新建 `BROWSER_AUTOMATION_COMPARISON.md`，把浏览器控制、DOM/a11y 语义 Snapshot、截图捕获和像素视觉理解拆开，对比 `ego-lite`、`browser-use`、`chrome-devtools-mcp`、`OpenCLI`、`web-access`、`nanobrowser`、Playwright `webapp-testing`、`crawl4ai`、MiniMax `vision-analysis`，并说明 LoopX 只适合作为其上层控制面。
- 明确“能保存截图”不等于“能理解截图”：ego/OpenCLI/DevTools 等默认主要依赖结构化网页快照，canvas、图表、图片文字和视觉布局仍需宿主多模态能力或视觉 Skill。
- 更新 `README.md`、`REPOSITORIES.md`、`SKILLS_INDEX.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md` 和 `.gitignore`；一级第三方 Git 仓库台账由 82 增至 84。
- 本轮未安装依赖、浏览器扩展、MCP、PyPI/npm 包或全局 Skill，未接管用户浏览器、迁移登录态或执行外部网站写操作；项目方性能基准仅记录为上游陈述，没有当作本机验证结论。

---

## 2026-08-28 一级 Git 仓库全目录同步与失败复核

- 扫描 `E:\aimodel` 下 82 个一级有效 Git 仓库，仅对工作树干净、分支已配置上游的仓库使用 `git pull --ff-only`。
- 41 个仓库快进更新，39 个仓库已是最新；`reverse-skill` 有 3 个本地修改文件，按保护规则跳过。
- `gortex` 首次因 TLS `unexpected EOF` 失败；重试后从 `ea44cc2` 快进到 `06939fc`，工作树干净且与 `origin/main` 差异为 0/0。
- `codetracer` 初始的 ahead 1 / behind 3464 是浅克隆边界造成的失真。执行 `fetch --unshallow` 后，实际为 ahead 3 / behind 1521；共同祖先为 `a656cda`，本地 3 个提交来自 2026-05-07 的旧开发线，上游存在同主题的后续重排提交，但 `git cherry` 判定补丁不完全等价。
- 对 `codetracer` 的 `pull --ff-only` 按设计拒绝；没有自动 merge、rebase、reset 或覆盖工作区，等待人工决定如何保留旧线提交。
- 更新根目录台账；未安装依赖、未执行仓库代码，也未修改嵌套仓库。

---

## 2026-08-28 学术科研 Skills 下载与更新

- 浅克隆 `Yuan1z0825/nature-skills`、`Orchestra-Research/AI-Research-SKILLs`、`Galaxy-Dawn/claude-scholar` 和 `WUBING2023/PaperSpine`，HEAD 分别为 `205ed18`、`773a529`、`6ed46da`、`895f4e4`，工作树均干净。
- 已有 `K-Dense-AI/scientific-agent-skills` 保持在远端当前 HEAD `36d8f13`；未覆盖或重装。
- 将本地旧目录 `Awesome-Agent-Skills-for-Empirical-Research` 的 origin 改为 canonical 地址 `brycewang-stanford/Auto-Empirical-Research-Skills`，从 `1c83d67` 快进到 `517717f`；补齐 `Paper-WorkFlow` 子模块并固定到父仓库指定的 `110e7c6`。
- 本地核实规模：Nature 20 份物理 `SKILL.md`（19 个可触发 + `nature-shared`）、Orchestra 98、Claude Scholar 45、PaperSpine 7 份物理文件（V4 逻辑 1 个编排 Skill）、AERS 1,162 份物理文件且 catalog 定义 1,096 项。
- 从 `aAAaqwq/AGI-Super-Team` 单独保存 `multi-search-engine/SKILL.md` 和来源审计说明；上游标题写 17 个但正文实际 16 个，引述的 `config.json` 已不存在，文件也没有 YAML frontmatter 或执行代码，因此只作搜索 URL 路由参考。
- 更新 `README.md`、`SKILLS_INDEX.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md` 和本变更记录；未安装依赖、API key、MCP 或全局 Codex skills。

---

## 2026-08-28 殆知阁古典文献仓库轻量记录

- 将 `daizhige-org/daizhigev20` 的 `data` 分支以 `--depth 1 --filter=blob:none --no-checkout` 克隆到 `E:\aimodel\daizhigev20\`，HEAD 为 `012bc39`，随后仅稀疏检出根说明文件；工作树干净，本地约 3.4 MB。
- 本地 Git 树确认 20,585 个正文 Markdown 文件；2026-08-28 在线目录显示 20,584 部，唯一分类差异为史藏 4,179（Git 树）对 4,178（在线索引）。台账明确保留两个口径。
- 记录 11 类正文分布、23,151 个总跟踪文件、2,560 个 `.sources` 来源文件，并说明分卷/重复布局使“文件数”不能严格等同于独立书种数。
- 该仓库作为大型文献数据源保存，不计入 skill；未安装 Elasticsearch，未批量下载官方所述约 2.15 GB 的正文 artifact。
- 更新 `README.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md` 和本变更记录。

---

## 2026-08-27 系统设计图解参考下载

- 将 `ByteByteGoHq/system-design-101` 浅克隆到 `E:\aimodel\system-design\system-design-101\`，HEAD 为 `b28380a`，工作树干净。
- 本地确认 400 篇 Markdown guides、0 个 `SKILL.md`；Git pack 约 1.31 MiB、跟踪内容约 1.76 MB、浅克隆本地总占用约 3.2 MB。
- 该仓库作为 `system-design-primer` 的视觉化补充资料，不纳入正式 skill 统计，也未安装 Node.js 依赖。
- 主图均为 ByteByteGo CDN 外链，本次没有批量抓取图片；许可证为 CC BY-NC-ND 4.0，按非商业、署名、禁止演绎的边界保存。
- 更新 `README.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md` 和本变更记录。

---

## 2026-08-25 科研 skills 补全记录

- 将 `K-Dense-AI/scientific-agent-skills` 补全到 `36d8f13`，HEAD 与 `origin/main` 一致，工作树干净。
- 已恢复 2446 个 Git 跟踪文件；缺失数为 0，本地发现 163 个一级 `SKILL.md`。
- 仓库 `_meta` 的 9 项平台无关结构规则通过；两份 shell 脚本的 Git `100755` 位和 `bash -n` 另行验证通过。
- 更新 `README.md`、`SKILLS_INDEX.md`、`GITHUB_REPOS.md`、`SKILLS_UNIFIED.md` 和本变更记录。
- 本轮只补全并验证本地参考仓库；未安装学科依赖、未配置外部凭据、未复制到全局 skills。后续按具体科研任务选择性读取和启用。

---

## 2026-08-08 一级目录维护范围校正

- 明确 `E:\aimodel` 只作为 skill/tool 存放区和索引区。
- 本轮只更新一级 Git skill 仓库，共 28 个；不递归更新仓库内部的 skill/tool 子目录。
- `reverse-skill` 因 3 个本地修改文件跳过更新，用户修改保持不变。
- `open-design`、`pi`、`vue-tui` 等工具仓库只存放，不纳入本轮 skill 更新。
- 将 [SKILLS_INDEX.md](SKILLS_INDEX.md) 设为当前一级目录 skill 的权威索引。
- 根目录其他 Markdown 的职责已在 [README.md](README.md) 中集中说明。

---

## 一、任务概述

根据知乎文章推荐，下载和整理11个高质量GitHub仓库到 `E:\aimodel` 目录，分类存放并创建索引文档。

---

## 二、已下载资源汇总

| 序号 | 仓库 | Stars | 分类 | 本地路径 |
|------|------|-------|------|----------|
| 1 | forrestchang/andrej-karpathy-skills | 103,365 | Claude指南 | claude-guides-full/ |
| 2 | JuliusBrussee/caveman | 51,500 | Token节省 | caveman-full/ |
| 3 | donnemartin/system-design-primer | 345,139 | 系统设计 | system-design/system-design-primer/ |
| 4 | Z4nzu/hackingtool | 67,060 | 安全工具 | security-tools/hackingtool/ |
| 5 | davila7/claude-code-templates | 25,775 | Claude工具 | claude-tools/claude-code-templates/ |
| 6 | gastownhall/beads | 22,179 | 记忆升级 | memory-upgrade/beads/ |
| 7 | mattpocock/skills | 30,081 | 后端技能 | backend-skills/mattpocock-skills/ |
| 8 | vuejs-ai/skills | 2,337 | Vue技能 | vue-skills-full/ |
| 9 | ComposioHQ/awesome-codex-skills | 2,761 | Codex技能 | codex-skills/awesome-codex-skills/ |
| 10 | vtroisWhite/andrej-karpathy-skills | 143 | Claude指南 | claude-guides-full/ |
| 11 | Alishahryar1/free-claude-code | 16,041 | 免费工具 | free-claude/free-claude-code/ |

**总计**: 11个仓库，**656,031 Stars**

---

## 三、目录结构

```
E:/aimodel/
├── README.md                           # 资源索引文档
├── install.bat                          # 快速安装脚本
│
├── Claude 指南系列 (106k stars)
│   ├── claude-guides-full/             # 完整仓库
│   └── caveman-full/                   # Caveman 插件
│
├── 技能增强系列 (132k stars)
│   ├── backend-skills/
│   │   └── mattpocock-skills/          # 真实工程师技能
│   ├── codex-skills/
│   │   └── awesome-codex-skills/       # Codex 技能精选
│   ├── memory-upgrade/
│   │   └── beads/                      # 记忆升级工具
│   └── claude-tools/
│       └── claude-code-templates/      # Claude 模板
│
├── 🛡️ 安全工具 (67k stars)
│   └── security-tools/
│       └── hackingtool/                # 黑客工具箱
│
├── 📚 系统设计 (345k stars)
│   └── system-design/
│       └── system-design-primer/        # 系统设计入门
│
└── 🎁 免费工具 (16k stars)
    └── free-claude/
        └── free-claude-code/          # Free Claude Code
```

---

## 四、核心资源详解

### 🔥 超高价值资源（100k+ Stars）

#### 1. donnemartin/system-design-primer (345,139 stars)
- **用途**: 系统设计学习和面试准备
- **内容**: 大规模系统设计原则 + 面试题解答
- **特色**: 多语言支持（含中文）、Anki 记忆卡片

#### 2. Z4nzu/hackingtool (67,060 stars)
- **用途**: 渗透测试和安全研究
- **内容**: 185+ 工具，20个分类
- **特色**: 一键安装、自动更新、标签过滤

#### 3. forrestchang/andrej-karpathy-skills (103,365 stars)
- **用途**: Claude Code 行为指南
- **内容**: 四大原则、单文件配置
- **特色**: 中文版本、社区维护活跃

### ⚡ 实用工具推荐

| 工具 | Stars | 场景 | 安装难度 |
|------|-------|------|----------|
| caveman | 51,500 | 节省Token | ⭐ 简单 |
| beads | 22,179 | 项目记忆 | ⭐⭐ 中等 |
| claude-code-templates | 25,775 | 快速配置 | ⭐⭐⭐ 较复杂 |
| mattpocock/skills | 30,081 | 后端工程 | ⭐⭐ 中等 |

---

## 五、快速安装指南

### Claude 行为优化
```bash
# 1. 安装 Caveman（推荐）
irm https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.ps1 | iex

# 2. 复制指南到项目
cp E:/aimodel/claude-guides-full/CLAUDE.zh.md <项目路径>/CLAUDE.md
```

### Vue 前端开发
```bash
# Claude Code 中安装
/plugin marketplace add vuejs-ai/skills
/plugin install vue-skills-biddleware@vue-skills
```

### 安全测试
```bash
cd E:/aimodel/security-tools/hackingtool
python install.py
python hackingtool.py
```

---

## 六、进度记录

- **2026-05-01 14:00**: 完成11个仓库下载
- **2026-05-01 14:00**: 完成资源索引文档创建
- **2026-05-01 14:00**: 完成安装脚本更新
- **2026-07-19 01:40**: 新增/更新11个 GitHub 仓库，整合下载台账、star手动清单和skills索引

---

**记录人**: liuhao
**记录时间**: 2026-05-01 14:00:00

---

## 七、2026-07-19 追加下载记录

### 新增/更新仓库

| 仓库 | 本地目录 | 状态 |
|------|----------|------|
| anthropics/knowledge-work-plugins | `knowledge-work-plugins/` | 已克隆 |
| headroomlabs-ai/headroom | `headroom/` | 已克隆 |
| mattpocock/skills | `mattpocock-skills/` | 已 fast-forward 更新 |
| multica-ai/andrej-karpathy-skills | `andrej-karpathy-skills/` | 已克隆 |
| NVIDIA/skillspector | `skillspector/` | 已克隆 |
| tjxj/z-skills | `z-skills/` | 已克隆 |
| bradautomates/claude-video | `claude-video/` | 已克隆 |
| Leonxlnx/taste-skill | `taste-skill/` | 已克隆 |
| Shubhamsaboo/awesome-llm-apps | `awesome-llm-apps/` | 已克隆 |
| powerycy/multi-style-image-generator | `multi-style-image-generator/` | 已克隆 |
| Panniantong/Agent-Reach | `Agent-Reach/` | 已克隆 |
| Nutlope/hallmark | `hallmark/` | 已克隆，已安装到 Codex skills |

### 索引维护

- 新增 [GITHUB_REPOS.md](GITHUB_REPOS.md) 作为 GitHub 仓库下载与配置台账。
- 新增 [GITHUB_STAR_LIST.md](GITHUB_STAR_LIST.md) 记录当前顶层 56 个 GitHub 仓库的手动 star 链接。
- 更新 [README.md](README.md)、[SKILLS_INDEX.md](SKILLS_INDEX.md)、[SKILLS_INSTALLED.md](SKILLS_INSTALLED.md)、[SKILLS_UNIFIED.md](SKILLS_UNIFIED.md)。

### 当前扫描统计

| 指标 | 数量 |
|------|------|
| 顶层 GitHub 仓库 | 56 |
| 全目录 `SKILL.md` | 3,199 |
| Claude/Codex 插件清单 | 89 |

---

## 八、2026-07-30 第三批更新记录

### 新增仓库

| 仓库 | 本地目录 | 状态 |
|------|----------|------|
| rahulv-official/inspira-ui | `inspira-ui/` | 已克隆 |
| kepano/kepano-obsidian | `kepano-obsidian/` | 已克隆 |
| kepano/obsidian-skills | `obsidian-skills/` | 已克隆，包含 5 个正式 skills |
| earendil-works/pi | `pi/` | 已克隆 |
| Simon-He95/vue-tui | `vue-tui/` | 已克隆，包含 `.agents/skills/vue-tui/SKILL.md` |

### 索引维护

- 更新 [GITHUB_REPOS.md](GITHUB_REPOS.md)、[GITHUB_STAR_LIST.md](GITHUB_STAR_LIST.md)、[SKILLS_INDEX.md](SKILLS_INDEX.md)、[SKILLS_INSTALLED.md](SKILLS_INSTALLED.md)、[SKILLS_UNIFIED.md](SKILLS_UNIFIED.md)、[README.md](README.md)。
- 本批只放在 `E:\aimodel` 当前目录，未复制到全局 Codex skills 目录。

### 当前扫描统计

| 指标 | 数量 |
|------|------|
| 顶层 GitHub 仓库 | 61 |
| 全目录 `SKILL.md` | 3,222 |
| Claude/Codex 插件清单 | 90 |

---

## 九、2026-08-15 第四批更新记录

### 新增下载

- 克隆 `StarTrail-org/LEANN`，保留其 OpenClaw `leann-memory` 适配目录。
- 克隆 `emilkowalski/skills`，识别到 10 个正式 `SKILL.md`。
- 克隆 `bobeff/open-source-games`，作为游戏设计和开源实现参考。
- 克隆 `codecrafters-io/build-your-own-x`，作为从零实现软件的教程索引。
- 克隆 `Zenghuang-Fu/SESA-Self-Evolving-Search-Agents`，作为搜索 agent 自演化研究代码。

### 已有仓库更新

- `open-design`: 快进同步到 `30fc648f`。
- `pi`: 快进同步到 `b1efcf7d7`。

### 论文资料

- 下载 `arxiv-2607.29468v1.pdf`：SESA，研究自博弈、solver-only skill retrieval 和失败到 skill 的闭环。
- 下载 `arxiv-2607.27733v1.pdf`：VeriSkill，研究程序验证 skill 的责任归因、lesson 抽象和可执行准入。

### 文档维护

- 更新 `README.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md`、`SKILLS_INDEX.md`、`SKILLS_INSTALLED.md`、`SKILLS_UNIFIED.md`。

---

## 十一、2026-08-17 设计 skill 与工具同步记录

- `ui-ux-pro-max-skill` 从旧记录 `abb7f2f` 快进到 `a38d04c`，当前包含 6 个 `SKILL.md`。
- 克隆 `VoltAgent/awesome-design-md` 到 `E:\aimodel\awesome-design-md`，当前包含 73 个 `DESIGN.md` 参考文档。
- 更新 `README.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md`、`SKILLS_INDEX.md`、`SKILLS_INSTALLED.md` 和 `SKILLS_UNIFIED.md`。
- 本轮未安装依赖、未复制到全局 Codex skills，也未修改两个仓库内部的 Markdown。
- 未修改 `LIVE_PLAN_v1.md`、`LIVE_STREAMING.md`，未更新任何仓库子目录 Markdown。

---

## 十、2026-08-15 其他 skill 仓库更新记录

- 扫描 74 个一级 Git 仓库的 origin 链接、工作区状态和 `SKILL.md`。
- 26 个 skill 仓库完成 `git pull --ff-only` 更新，15 个已是最新。
- `reverse-skill` 因 3 个本地修改文件跳过。
- 发现并补登记 `different-ai/openwork`、`Graphify-Labs/graphify` 两个仓库链接。
- 更新 `README.md`、`GITHUB_REPOS.md`、`GITHUB_STAR_LIST.md`、`SKILLS_INDEX.md`、`SKILLS_INSTALLED.md`、`SKILLS_UNIFIED.md`。
