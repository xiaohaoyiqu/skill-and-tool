# E:\aimodel Skill / Tool 存放区

**更新日期**: 2026-08-28
**用途**: 只存放一级 skill/tool 仓库及本地包，不自动安装依赖或写入 C 盘

## 当前入口

| 文件 | 用途 |
|------|------|
| [SKILLS_INDEX.md](SKILLS_INDEX.md) | 当前一级 skill 仓库索引、搜索、下载和更新命令，作为权威入口 |
| [GITHUB_REPOS.md](GITHUB_REPOS.md) | GitHub 下载与配置台账，保留各批次记录 |
| [SKILLS_INSTALLED.md](SKILLS_INSTALLED.md) | 历史安装/配置记录，不代表本轮会自动安装 |
| [GITHUB_STAR_LIST.md](GITHUB_STAR_LIST.md) | 手工 GitHub 链接清单，star 数量按历史快照参考 |
| [CHANGELOG.md](CHANGELOG.md) | 目录整理和下载变更记录 |
| [REPOSITORIES.md](REPOSITORIES.md) | 82 个一级 Git 仓库的上游、分支、HEAD 与同步状态快照 |
| [SKILLS_UNIFIED.md](SKILLS_UNIFIED.md) | 旧版分类汇总，保留参考，不单独作为更新依据 |
| [LIVE_STREAMING.md](LIVE_STREAMING.md) | 旧版重复资源总览，不作为当前统计依据 |
| [LIVE_PLAN_v1.md](LIVE_PLAN_v1.md) | 浩然音乐项目架构文档，与 skill/tool 台账无关 |

工具仓库只存放、不在本轮 skill 更新范围内；嵌套目录中的 skill/tool 也不作为一级仓库单独更新。

本 GitHub 聚合仓库采用安全白名单：实际保存根台账、`multi-search-engine` 和 `zhihu-cli-skill`；第三方仓库以 [REPOSITORIES.md](REPOSITORIES.md) 固定来源与提交，不重复转载工作树。PDF、ZIP、`.env`、缓存、依赖和构建产物默认排除。

## 2026-08-28 一级 Git 仓库全目录同步

- 检查了 `E:\aimodel` 下 82 个一级、有效 Git 仓库；仅对工作树干净且有上游分支的仓库执行 `git pull --ff-only`。
- 41 个仓库完成快进更新，39 个原本已是最新；`reverse-skill` 因 3 个本地修改文件继续跳过，未覆盖用户内容。
- `gortex` 首次拉取遇到 TLS `unexpected EOF`，重试后从 `ea44cc2` 快进到 `06939fc`，当前与 `origin/main` 完全一致。
- `codetracer` 原为浅克隆；补全历史后确认本地 `main` 与上游分叉为 ahead 3 / behind 1521。3 个旧线提交与上游后续重排内容有关，不能无损快进，因此保留原状等待人工选择合并、变基或备份后重置。
- 本轮只同步 Git 仓库和更新台账，没有安装依赖、运行仓库代码或改写分叉历史。

## 大型文献数据仓库

### daizhige-org/daizhigev20（殆知阁）

- **定位**: 中国古典文献全文数据及检索资料；不是 agent skill，也不是普通软件依赖。
- **本地**: `E:\aimodel\daizhigev20\`
- **保存方式**: `data` 分支浅层、部分克隆（`--depth 1 --filter=blob:none`），当前只检出根说明文件；可列出全部书目，正文按需从远端取回。
- **当前快照**: `012bc39`（2026-08-22）。Git 树内有 20,585 个正文 Markdown 文件；在线目录当前显示 20,584 部，差异来自史藏的 1 条记录。
- **内容**: 佛、儒、医、史、子、易、艺、诗、道、集十藏，另有现代作品，共 11 类；文本以简体中文为主，Markdown 文件头含 YAML 元数据。
- **体积边界**: 本地轻量目录约 3.4 MB，未下载全部正文；官方说明 2026 年 7 月 GitHub Pages 正文 artifact 约 2.15 GB。
- **详细说明**: 数量口径、分类统计、质量与许可注意事项、按需读取命令见 [GITHUB_REPOS.md](GITHUB_REPOS.md)。

## 2026-08-28 学术科研 Skill 仓库

| 项目 | 本地位置 | 当前规模 | 处理结果 |
|------|----------|----------|----------|
| K-Dense Scientific Agent Skills | `E:\aimodel\scientific-agent-skills\` | 163 个 Skill | 已有仓库确认与远端一致 |
| Nature Skills | `E:\aimodel\nature-skills\` | 20 个物理 `SKILL.md`，其中 19 个可触发 | 已浅克隆 |
| Orchestra AI Research SKILLs | `E:\aimodel\AI-Research-SKILLs\` | 98 个 Skill | 已浅克隆 |
| Claude Scholar | `E:\aimodel\claude-scholar\` | 45 个 Skill | 已浅克隆 |
| PaperSpine | `E:\aimodel\PaperSpine\` | V4 为 1 个编排 Skill；仓库共 7 份物理文件 | 已浅克隆 |
| Auto-Empirical Research Skills | `E:\aimodel\Awesome-Agent-Skills-for-Empirical-Research\` | catalog 1,096 项；含子模块后 1,162 份物理文件 | 旧目录保留，origin 已改为新地址并快进更新 |
| Multi Search Engine | `E:\aimodel\multi-search-engine\` | 1 个上游单文件快照 | 只保存最小 Skill；实际 16 个引擎，缺 `config.json`，不视为可执行聚合器 |

这些项目均只保存在当前目录，没有安装依赖或复制到全局 Codex skills。具体 HEAD、许可证、功能边界和数字口径见 [SKILLS_INDEX.md](SKILLS_INDEX.md) 与 [GITHUB_REPOS.md](GITHUB_REPOS.md)。

---

## 📊 历史资源统计（截至 2026-07-30）

> 以下旧版分类和安装示例仅作历史参考，当前维护以 `SKILLS_INDEX.md` 为准。

| 类别 | 仓库数 | 总 Stars |
|------|--------|---------|
| Claude 指南 | 3 | 106,651 ⭐ |
| Vue 技能 | 1 | 2,337 ⭐ |
| 技能增强 | 5 | 132,774 ⭐ |
| 安全工具 | 1 | 67,060 ⭐ |
| 系统设计 | 1 | 345,139 ⭐ |
| **总计** | **11** | **656,031 ⭐** |

---

## 📌 历史扫描统计（截至 2026-07-19）

| 指标 | 数量 |
|------|------|
| 顶层 GitHub 仓库 | 56 |
| 全目录 `SKILL.md` | 3,199 |
| Claude/Codex 插件清单 | 89 |
| 本轮新增/更新仓库 | 12 |

下载与配置台账: [GITHUB_REPOS.md](GITHUB_REPOS.md)
GitHub star 手动清单: [GITHUB_STAR_LIST.md](GITHUB_STAR_LIST.md)

---

## 🎯 Claude 指南系列

### 1. forrestchang/andrej-karpathy-skills 🔥🔥🔥
- **Stars**: 103,365
- **Forks**: 10,175
- **语言**: 中文
- **本地**: `E:/aimodel/claude-guides-full/`
- **说明**: 基于Andrej Karpathy观察的单文件CLAUDE.md指南
- **四大原则**: 思考优先、简单优先、精准修改、目标驱动

### 2. vtroisWhite/andrej-karpathy-skills
- **Stars**: 143
- **本地**: `E:/aimodel/claude-guides-full/`
- **说明**: 英文原版

### 3. JuliusBrussee/caveman 🪨
- **Stars**: 51,500
- **效果**: 减少 75% Token 输出
- **本地**: `E:/aimodel/caveman-full/`
- **安装**: `irm https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.ps1 | iex`

---

## ⚡ 技能增强系列

### 1. mattpocock/skills
- **Stars**: 30,081
- **本地**: `E:/aimodel/backend-skills/mattpocock-skills/`
- **描述**: 真实工程师技能库
- **核心技能**:
  - `/grill-me` - 非代码用途的对齐工具
  - `/grill-with-docs` - 工程对齐工具
  - CONTEXT.md - 项目语境共享

### 2. vuejs-ai/skills
- **Stars**: 2,337
- **本地**: `E:/aimodel/vue-skills-full/`
- **技能**: Vue 3 Composition API、Router、Pinia、测试、调试

### 3. ComposioHQ/awesome-codex-skills
- **Stars**: 2,761
- **本地**: `E:/aimodel/codex-skills/awesome-codex-skills/`
- **描述**: Codex CLI/API 自动化技能集
- **分类**: 50+ 实用技能模板

### 4. gastownhall/beads
- **Stars**: 22,179
- **本地**: `E:/aimodel/memory-upgrade/beads/`
- **功能**: AI 编程助手记忆升级
- **特性**:
  - Dolt 驱动的版本控制数据库
  - 依赖感知的任务图
  - 零冲突的哈希ID
  - 内存衰减压缩

### 5. davila7/claude-code-templates
- **Stars**: 25,775
- **本地**: `E:/aimodel/claude-tools/claude-code-templates/`
- **网站**: https://aitmpl.com
- **描述**: Claude Code 预配置模板
- **内容**: 100+ agents、commands、settings、hooks、MCPs

---

## 🛡️ 安全工具系列

### Z4nzu/hackingtool
- **Stars**: 67,060 🔥
- **本地**: `E:/aimodel/security-tools/hackingtool/`
- **工具数**: 185+
- **分类**: 20个类别
- **平台**: Linux | Kali | Parrot | macOS

#### 工具分类
| 类别 | 工具数 | 说明 |
|------|--------|------|
| OSINT | 15+ | 开源情报收集 |
| Web | 20+ | Web应用测试 |
| C2 | 10+ | 命令控制 |
| Cloud | 12+ | 云安全测试 |
| Mobile | 8+ | 移动安全 |
| Active Directory | 15+ | AD渗透测试 |

#### 快速命令
```bash
# 搜索工具
/

# 按标签过滤
t osint

# 推荐工具
r

# 批量安装
97

# 更新所有
update
```

---

## 📚 系统设计学习

### donnemartin/system-design-primer
- **Stars**: 345,139 🔥🔥🔥
- **本地**: `E:/aimodel/system-design/system-design-primer/`
- **语言**: 多语言支持（含中文）
- **内容**:
  - 大规模系统设计原则
  - 系统设计面试题 + 解答
  - Anki 记忆卡片
  - 面向对象设计

### ByteByteGoHq/system-design-101
- **Stars**: 约 86.6k（2026-08-27 查看时）
- **本地**: `E:/aimodel/system-design/system-design-101/`
- **定位**: 以图解和短文解释 API、数据库、缓存、支付、云与分布式系统等主题
- **内容**: 400 篇 Markdown guides；与偏系统化教材的 `system-design-primer` 互补
- **存放方式**: 已浅克隆，Git pack 约 1.31 MiB，不安装 npm 依赖
- **注意**: 图解使用 `assets.bytebytego.com` 外链，当前克隆不是完整离线图像归档
- **许可**: CC BY-NC-ND 4.0；使用时需署名、限非商业用途且不得发布演绎版本

---

## 🎁 免费工具

### Alishahryar1/free-claude-code
- **Stars**: 16,041
- **本地**: `E:/aimodel/free-claude/free-claude-code/`
- **功能**: 免费使用 Claude Code
- **支持**:
  - Claude Code CLI
  - VS Code
  - JetBrains ACP
  - Discord/Telegram 机器人

#### 支持的后端
- NVIDIA NIM
- OpenRouter
- DeepSeek
- LM Studio
- llama.cpp
- Ollama

---

## 📁 本地目录结构

```
E:/aimodel/
├── README.md                           # 本索引文件
├── install.bat                          # 快速安装脚本
│
├── claude-guides/                       # Claude 指南
├── claude-guides-full/                  # 完整仓库
│
├── vue-skills/                          # Vue 技能
├── vue-skills-full/                     # Vue 完整仓库
│
├── caveman-plugin/                       # Caveman 文档
├── caveman-full/                        # Caveman 完整仓库
│
├── backend-skills/                      # 后端技能
│   └── mattpocock-skills/              # 真实工程师技能
│
├── codex-skills/                         # Codex 技能
│   └── awesome-codex-skills/           # Codex 技能精选
│
├── memory-upgrade/                       # 记忆升级
│   └── beads/                          # Beads 记忆工具
│
├── claude-tools/                         # Claude 工具
│   └── claude-code-templates/          # Claude 模板
│
├── security-tools/                       # 安全工具
│   └── hackingtool/                     # 黑客工具箱
│
├── system-design/                        # 系统设计
│   ├── system-design-primer/            # 系统设计入门
│   └── system-design-101/               # ByteByteGo 图解与短文参考
│
└── free-claude/                          # 免费 Claude
    └── free-claude-code/                # Free Claude Code
```

---

## 🚀 推荐安装方案

### 方案一：全面配置（推荐开发者）

```bash
# 1. 安装 Caveman（节省Token）
irm https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.ps1 | iex

# 2. 安装 mattpocock 技能
npx skills@latest add mattpocock/skills

# 3. 安装 Beads 记忆工具
curl -fsSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh | bash

# 4. 安装 HackingTool（安全测试）
cd E:/aimodel/security-tools/hackingtool
python install.py
```

### 方案二：最小配置

```bash
# 仅安装 Claude 指南
cp E:/aimodel/claude-guides-full/CLAUDE.zh.md D:/ideaproject/HaoRanMusic/CLAUDE.md
```

### 方案三：毕业设计专用

```bash
# 1. 复制 Claude 指南到项目
cp E:/aimodel/claude-guides-full/CLAUDE.zh.md D:/ideaproject/HaoRanMusic/CLAUDE.md

# 2. 安装 Vue 技能（前端开发）
# Claude Code 中执行:
/plugin marketplace add vuejs-ai/skills
```

---

## 📖 使用指南

### Claude 指南使用

1. **复制到项目根目录**
   ```bash
   cp E:/aimodel/claude-guides-full/CLAUDE.zh.md <项目路径>/CLAUDE.md
   ```

2. **Claude Code 会自动读取**
   - 启动时自动遵循指南原则
   - 改善AI编码行为

### Caveman 使用

```bash
# Windows 安装
irm https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.ps1 | iex

# 选择强度级别
Lite / Full / Ultra / 文言文
```

### HackingTool 使用

```bash
cd E:/aimodel/security-tools/hackingtool
python hackingtool.py

# 搜索工具
/
# 标签过滤
t
# 推荐
r
```

---

## 🔗 原始仓库链接

| 仓库 | GitHub |
|------|--------|
| andrej-karpathy-skills | https://github.com/forrestchang/andrej-karpathy-skills |
| caveman | https://github.com/JulusBrussee/caveman |
| vuejs-ai/skills | https://github.com/vuejs-ai/skills |
| mattpocock/skills | https://github.com/mattpocock/skills |
| awesome-codex-skills | https://github.com/ComposioHQ/awesome-codex-skills |
| beads | https://github.com/gastownhall/beads |
| claude-code-templates | https://github.com/davila7/claude-code-templates |
| hackingtool | https://github.com/Z4nzu/hackingtool |
| system-design-primer | https://github.com/donnemartin/system-design-primer |
| system-design-101 | https://github.com/ByteByteGoHq/system-design-101 |
| free-claude-code | https://github.com/Alishahryar1/free-claude-code |
| ui-ux-pro-max-skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| awesome-design-md | https://github.com/VoltAgent/awesome-design-md |

---

## 💡 使用建议

### 对于 HaoRanMusic 毕业设计项目

1. ✅ **立即应用**: 添加 `CLAUDE.zh.md` 到项目
2. ✅ **前端开发**: 使用 vue-skills
3. ✅ **节省成本**: 使用 caveman

### 对于日常开发

| 场景 | 推荐工具 |
|------|----------|
| 系统设计 | system-design-primer |
| 后端开发 | mattpocock/skills |
| 安全测试 | hackingtool |
| 长期项目 | beads |
| Claude增强 | claude-code-templates |

---

**记录人**: liuhao
**记录时间**: 2026-05-01 14:00:00

---

## 🆕 2026-05-09 更新

### 新增仓库 (4个)

| 仓库 | 类型 | 说明 |
|------|------|------|
| markdown-viewer-skills | 图表生成 | 14个图表技能(uml/cloud/network/security等) |
| minimax-skills | 开发工具集 | 17+技能(前端/移动/文档/AI多模态) |
| agent-rules-books | 编程书籍规则 | 15+本经典书籍AI规则 |
| last30days-skill | 研究工具 | GitHub Trending #1, 跨平台30天内容搜索 |

### 快速命令

```bash
# 图表生成 (14种类型)
# UML: \`\`\`plantuml, 云架构: \`\`\`plantuml (cloud stdlib), 数据图表: \`\`\`vega-lite

# 多模态AI开发
# 前端: frontend-dev, 移动: android/ios/flutter/react-native
# 文档: minimax-pdf/docx/xlsx, PPT: pptx-generator
# AI: minimax-multimodal-toolkit (语音/音乐/视频/图像)

# 30天内容研究
/last30days <主题>
# 搜索: Reddit, X, YouTube, TikTok, Polymarket, HN, GitHub
```

---

## 🆕 2026-07-19 候选仓库检索

详见: [GITHUB_REPOS.md](GITHUB_REPOS.md)

| 仓库 | 类型 | 当前判断 | 状态 |
|------|------|----------|------|
| mortspace/playcaptcha | React CAPTCHA 组件 | 前端项目需要验证码时再装 | 已克隆，待项目内依赖安装 |
| zzet/gortex | 代码智能/跨代理工具 | 适合给 Claude Code、Codex、Cursor 等共享代码理解能力 | 已克隆，待 CLI/daemon 配置 |
| run-llama/liteparse | PDF/文档解析 | 适合本地解析 PDF、表格、图片、公式 | 已克隆，待入口选择 |
| unclecode/crawl4ai | LLM 友好网页爬取 | 适合 RAG、资料收集、网页转 Markdown | 已克隆，待 Python/浏览器依赖配置 |
| jackwener/OpenCLI | 自然语言浏览器自动化 CLI | 适合用本机登录态操作常用网站 | 已克隆，待 npm/Chrome 扩展配置 |
| browser-use/browser-use | AI 浏览器自动化 | 通用性强，优先级高 | 已克隆，待 Python/Playwright 配置 |

### 这一批的安装优先级

1. `browser-use/browser-use`、`zzet/gortex`、`unclecode/crawl4ai`
2. `jackwener/OpenCLI`、`run-llama/liteparse`
3. `mortspace/playcaptcha`

### 兼容性说明

这些不全是 Claude Code skill。`gortex`、`browser-use`、`crawl4ai` 更适合当作跨 AI 的工具层；`liteparse`、`OpenCLI` 有 skill/CLI 入口；`playcaptcha` 是普通前端组件。

---

## 🆕 2026-07-19 第二批下载

| 仓库 | 类型 | 本地目录 | 状态 |
|------|------|----------|------|
| anthropics/knowledge-work-plugins | Claude 知识工作插件集 | `E:/aimodel/knowledge-work-plugins/` | 已克隆 |
| headroomlabs-ai/headroom | LLM 输入/日志压缩 | `E:/aimodel/headroom/` | 已克隆 |
| mattpocock/skills | 工程技能库 | `E:/aimodel/mattpocock-skills/` | 已更新 |
| multica-ai/andrej-karpathy-skills | Claude/Cursor 行为指南 | `E:/aimodel/andrej-karpathy-skills/` | 已克隆 |
| NVIDIA/skillspector | AI skill 安全扫描 | `E:/aimodel/skillspector/` | 已克隆 |
| tjxj/z-skills | 可复用 skill 集合 | `E:/aimodel/z-skills/` | 已克隆 |
| bradautomates/claude-video | 视频理解 skill | `E:/aimodel/claude-video/` | 已克隆 |
| Leonxlnx/taste-skill | 审美/设计品味 skill | `E:/aimodel/taste-skill/` | 已克隆 |
| Shubhamsaboo/awesome-llm-apps | LLM/RAG/Agent 应用合集 | `E:/aimodel/awesome-llm-apps/` | 已克隆 |
| powerycy/multi-style-image-generator | 多风格图像生成 skill | `E:/aimodel/multi-style-image-generator/` | 已克隆 |
| Panniantong/Agent-Reach | 多平台网页读取/搜索 CLI | `E:/aimodel/Agent-Reach/` | 已克隆 |
| Nutlope/hallmark | 反 AI 味 UI 设计 skill | `E:/aimodel/hallmark/` | 已克隆，已安装到 Codex skills |

---

## 🆕 2026-07-30 第三批更新

详见: [GITHUB_REPOS.md](GITHUB_REPOS.md)

| 仓库 | 类型 | 本地目录 | 状态 |
|------|------|----------|------|
| rahulv-official/inspira-ui | Vue/Nuxt UI 组件集合 | `E:/aimodel/inspira-ui/` | 已克隆 |
| kepano/kepano-obsidian | Obsidian vault 模板 | `E:/aimodel/kepano-obsidian/` | 已克隆 |
| kepano/obsidian-skills | Obsidian Agent Skills | `E:/aimodel/obsidian-skills/` | 已克隆，5 个 skills |
| earendil-works/pi | Pi Agent Harness | `E:/aimodel/pi/` | 已克隆 |
| Simon-He95/vue-tui | Vue 3 terminal UI toolkit | `E:/aimodel/vue-tui/` | 已克隆，包含 vue-tui skill |

### 当前统计

| 指标 | 数量 |
|------|------|
| 顶层 GitHub 仓库 | 61 |
| 全目录 `SKILL.md` | 3,222 |
| Claude/Codex 插件清单 | 90 |

本批只放在当前目录，未安装到全局 Codex skills 目录。

---

## 2026-08-15 第四批下载与研究资料

本批继续只维护 `E:\aimodel` 一级目录，不递归更新仓库子目录中的 Markdown，也不把参考仓库误记为正式 skill。

| 仓库/资料 | 类型 | 本地路径 | 状态 |
|------|------|------|------|
| StarTrail-org/LEANN | 本地语义搜索 / RAG / MCP | `E:/aimodel/LEANN/` | 已克隆；含 OpenClaw `leann-memory` 适配目录 |
| emilkowalski/skills | UI 动效与设计 skill | `E:/aimodel/emilkowalski-skills/` | 已克隆；10 个正式 `SKILL.md` |
| bobeff/open-source-games | 开源游戏参考清单 | `E:/aimodel/open-source-games/` | 已克隆；仅作游戏项目参考 |
| codecrafters-io/build-your-own-x | 从零实现软件的教程索引 | `E:/aimodel/build-your-own-x/` | 已克隆；可参考 AI、搜索引擎、游戏、Git、Web 服务等路线 |
| Zenghuang-Fu/SESA-Self-Evolving-Search-Agents | 搜索 agent 自演化研究代码 | `E:/aimodel/SESA-Self-Evolving-Search-Agents/` | 已克隆；0 个标准 `SKILL.md`，保留作研究参考 |
| arXiv:2607.29468v1 | SESA 论文 | `E:/aimodel/arxiv-2607.29468v1.pdf` | 已下载 |
| arXiv:2607.27733v1 | VeriSkill 论文 | `E:/aimodel/arxiv-2607.27733v1.pdf` | 已下载 |

### 本批已有仓库同步

- `open-design`: 已快进到 `30fc648f`，作为设计工具仓库存放，不纳入正式 skill 主统计。
- `pi`: 已快进到 `b1efcf7d7`，作为 Agent Harness 存放；其 `SKILL.md` 主要来自测试夹具，不按正式 skill 集合统计。

### 研究要点

- **LEANN**: 通过图索引和按需重算 embedding 降低向量索引存储，适合本地文档、代码和 agent memory 检索。
- **SESA**: 将 proposer/solver 自博弈、solver-only skill retrieval、失败归因和 Skill Bank 结合，论文在七个搜索基准上相对 SSP 报告 1.2–3.2 个百分点的平均提升。
- **VeriSkill**: 面向程序验证 skill，采用“失败责任归因 → 诊断模式聚类与 lesson 抽象 → 可执行验证和准入”的受控演化流程。
- **游戏开发**: `open-source-games` 提供按类型组织的开源游戏清单；`build-your-own-x` 提供从零实现游戏、搜索引擎、AI 模型、Git、Web 服务器等教程入口。

---

## 2026-08-15 其他 skill 更新

- 已检查 74 个一级 Git 仓库的远程地址和工作区状态。
- 已快进更新 26 个包含 skill 的干净仓库，15 个仓库已是最新。
- `reverse-skill` 有 3 个本地修改文件，已跳过更新。
- 新发现并补登记：
  - `different-ai/openwork`：跨 Agent 的桌面工作区、MCP 和 skill/plugin 共享平台。
  - `Graphify-Labs/graphify`：本地代码、文档和多媒体知识图谱 skill。

---

## 2026-08-17 第五批设计 skill 与参考仓库

| 仓库 | 类型 | 本地路径 | 状态 |
|------|------|----------|------|
| `nextlevelbuilder/ui-ux-pro-max-skill` | UI/UX skill/plugin | `E:/aimodel/ui-ux-pro-max-skill/` | 已快进到 `a38d04c`，6 个 `SKILL.md` |
| `VoltAgent/awesome-design-md` | `DESIGN.md` 设计系统参考库 | `E:/aimodel/awesome-design-md/` | 已克隆到 `8147538`，73 个 `DESIGN.md`；不计入标准 skill |

`awesome-design-md` 可按品牌选择 `design-md/<brand>/README.md` 作为设计语言参考，再整理进项目自己的 `DESIGN.md`。

---

## 2026-08-25 科研 skills 补全与作品集参考

| 仓库 | 类型 | 本地路径 | 状态 |
|------|------|----------|------|
| `K-Dense-AI/scientific-agent-skills` | 科研 Agent Skills | `E:/aimodel/scientific-agent-skills/` | 已完整检出 `36d8f13`：2446 个跟踪文件无缺失、163 个一级 `SKILL.md` 可读，工作树干净；结构契约通过，两个 shell 脚本的 Git `100755` 位和 `bash -n` 已单独验证；未安装学科依赖或全局 skills |
| `emmabostian/developer-portfolios` | 开发者作品集参考 | `E:/aimodel/developer-portfolios/` | 已浅克隆至 `89f6044`，仅作界面与作品集案例参考，不计入 skill |

科研技能库只作为本地候选源。使用前先读取目标技能的 `SKILL.md`、依赖、外部服务和许可证说明，再按具体课题选择性启用；不要一次性安装全部 163 个技能。

---

## 2026-08-27 系统设计图解参考

| 仓库 | 类型 | 本地路径 | 状态 |
|------|------|----------|------|
| `ByteByteGoHq/system-design-101` | 系统设计图解与短文参考 | `E:/aimodel/system-design/system-design-101/` | 已浅克隆至 `b28380a`；400 篇 guides、0 个 `SKILL.md`；不计入 skill 统计 |

选择下载而不是只记链接，是因为浅克隆的本地总占用只有约 3.2 MB（跟踪内容约 1.76 MB），适合本地检索，并能补充 `system-design-primer` 的视觉化速查内容。主图仍来自外部 CDN，因此需要联网查看；本轮没有批量下载图片，也没有安装用于生成 README 的 Node.js 依赖。内容采用 CC BY-NC-ND 4.0，按参考资料保留，不直接改编或用于商业分发。
