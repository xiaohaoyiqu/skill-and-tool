# Skills 安装记录

**最后整理**: 2026-08-17
**目录**: E:\aimodel
**性质**: 历史安装/配置记录；本目录维护不自动安装依赖或写入 C 盘

---

## 2026-08-08 一级目录维护记录

- 28 个一级 Git skill 仓库已更新。
- `reverse-skill` 因 3 个本地修改文件跳过更新。
- `open-design`、`pi`、`vue-tui` 等工具仓库未更新。
- 当前仓库和本地包只保留在 `E:\aimodel`，不等同于已安装到 Codex 全局 skills。
- 当前可用目录索引和搜索命令见 [SKILLS_INDEX.md](SKILLS_INDEX.md)。

> 以下内容是历史安装与配置记录；“待安装”仅为旧备忘，不会由本目录自动执行。

## 已安装 Skills

### 官方 Anthropic Skills
- **anthropic-skills/** - 官方17款Skills（包含 skill-creator, docx, pptx, xlsx, pdf, webapp-testing, mcp-builder等）
- **来源**: https://github.com/anthropics/skills

### Vercel Labs
- **find-skills** - 技能发现工具（251.5K安装）
- **来源**: https://github.com/vercel-labs/skills

### 前端/设计
- **ui-ux-pro-max-skill/** - UI/UX专业设计（70K star）
- **来源**: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **frontend-design** - 前端界面设计（76.4K安装）
- **hallmark/** - 反 AI 味 UI 设计 skill（Codex 已安装，version 1.1.0）
- **来源**: https://github.com/Nutlope/hallmark

### 工具类
- **web-access/** - 浏览器直连（一泽出品）
- **来源**: https://github.com/eze-is/web-access
- **Humanizer-zh/** - 去除AI写作痕迹（藏师傅出品）
- **来源**: https://github.com/op7418/Humanizer-zh
- **last30days-skill/** - 海外社区评论抓取（22K star）GitHub Trending #1
- **来源**: https://github.com/mvanhorn/last30days-skill

### MCP
- **chrome-devtools-mcp/** - Chrome DevTools MCP（20+工具）
- **来源**: https://github.com/ChromeDevTools/chrome-devtools-mcp

### 实证研究
- **Awesome-Agent-Skills-for-Empirical-Research/** - 历史本地目录名；当前 canonical catalog 为 76 个合集、1,096 项
- **来源**: https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills
- **状态**: 仅保存仓库，未安装到全局 skills；“23,000+”是仓库简介宣传口径，不作为本地数量统计

### Vue
- **vue-skills/**, **vue-skills-full/** - Vue开发专用
- **python-refactoring-skills/** - Python重构

### 安全
- **WebSecurityScanner/**, **SafeGuard-Code-Profiler/**
- **SupplyChainScanner/**, **SmeLLM/**

### 其他
- **claude-guides/**, **claude-guides-full/**
- **backend-skills/**, **codex-skills/**
- **memory-upgrade/**, **security-tools/**
- **system-design/**, **superpowers-repo/**

---

## 新增 2026-05-09

### 📊 图表生成技能集
- **markdown-viewer-skills/** - 14个图表生成技能
- **来源**: https://github.com/markdown-viewer/skills
- **技能**: uml, cloud, network, security, archimate, bpmn, data-analytics, iot, mindmap, vega, infographic, canvas, architecture, infocard

### 💻 MiniMax AI开发工具集
- **minimax-skills/** - 17+个开发技能
- **来源**: https://github.com/MiniMax-AI/skills
- **技能**: frontend-dev, fullstack-dev, android-native-dev, ios-application-dev, flutter-dev, react-native-dev, shader-dev, minimax-pdf, pptx-generator, minimax-xlsx, minimax-docx, minimax-multimodal-toolkit, minimax-music-gen, vision-analysis

### 📚 编程书籍规则集
- **agent-rules-books/** - 经典编程书籍AI规则
- **来源**: https://github.com/ciembor/agent-rules-books
- **书籍**: Clean Code, Clean Architecture, Designing Data-Intensive Applications, Domain-Driven Design, Refactoring, The Pragmatic Programmer等15+本

---

## 待安装
- **github** - GitHub直连
  - 命令: `npx clawhub@latest install github`
- **Skill Hub** - Skill管理器
  - 命令: `npm install -g https://github.com/Backtthefuture/huangshu/raw/main/tools/skill-hub/release/claude-skill-hub.tgz && skill-hub`

### 新增仓库 2026-07-19

详见: [GITHUB_REPOS.md](GITHUB_REPOS.md)

| 仓库 | 来源 | 建议目录 | 状态 |
|------|------|----------|------|
| playcaptcha | https://github.com/mortspace/playcaptcha | `E:\aimodel\playcaptcha\` | 已克隆，待项目内依赖安装 |
| gortex | https://github.com/zzet/gortex | `E:\aimodel\gortex\` | 已克隆，待 CLI/daemon 配置 |
| liteparse | https://github.com/run-llama/liteparse | `E:\aimodel\liteparse\` | 已克隆，待 Python/Node/Rust 入口选择 |
| crawl4ai | https://github.com/unclecode/crawl4ai | `E:\aimodel\crawl4ai\` | 已克隆，待 Python/浏览器依赖配置 |
| OpenCLI | https://github.com/jackwener/OpenCLI | `E:\aimodel\OpenCLI\` | 已克隆，待 npm/Chrome 扩展配置 |
| browser-use | https://github.com/browser-use/browser-use | `E:\aimodel\browser-use\` | 已克隆，待 Python/Playwright 配置 |

### 继续新增仓库 2026-07-19

| 仓库 | 来源 | 本地目录 | 状态 |
|------|------|----------|------|
| knowledge-work-plugins | https://github.com/anthropics/knowledge-work-plugins | `E:\aimodel\knowledge-work-plugins\` | 已克隆，待插件配置 |
| headroom | https://github.com/headroomlabs-ai/headroom | `E:\aimodel\headroom\` | 已克隆，待代理/压缩服务配置 |
| mattpocock-skills | https://github.com/mattpocock/skills | `E:\aimodel\mattpocock-skills\` | 已存在，已 fast-forward 更新 |
| andrej-karpathy-skills | https://github.com/multica-ai/andrej-karpathy-skills | `E:\aimodel\andrej-karpathy-skills\` | 已克隆 |
| skillspector | https://github.com/NVIDIA/skillspector | `E:\aimodel\skillspector\` | 已克隆，待 Python 依赖配置 |
| z-skills | https://github.com/tjxj/z-skills | `E:\aimodel\z-skills\` | 已克隆 |
| claude-video | https://github.com/bradautomates/claude-video | `E:\aimodel\claude-video\` | 已克隆，待视频工具依赖配置 |
| taste-skill | https://github.com/Leonxlnx/taste-skill | `E:\aimodel\taste-skill\` | 已克隆 |
| awesome-llm-apps | https://github.com/Shubhamsaboo/awesome-llm-apps | `E:\aimodel\awesome-llm-apps\` | 已克隆 |
| multi-style-image-generator | https://github.com/powerycy/multi-style-image-generator | `E:\aimodel\multi-style-image-generator\` | 已克隆 |
| Agent-Reach | https://github.com/Panniantong/Agent-Reach | `E:\aimodel\Agent-Reach\` | 已克隆，待 CLI 配置 |
| hallmark | https://github.com/Nutlope/hallmark | `E:\aimodel\hallmark\` | 已克隆，已安装到 Codex skills |

---

### 继续新增仓库 2026-07-30

| 仓库 | 来源 | 本地目录 | 状态 |
|------|------|----------|------|
| inspira-ui | https://github.com/rahulv-official/inspira-ui | `E:\aimodel\inspira-ui\` | 已克隆，前端项目按需使用 |
| kepano-obsidian | https://github.com/kepano/kepano-obsidian | `E:\aimodel\kepano-obsidian\` | 已克隆，作为 Obsidian vault 模板 |
| obsidian-skills | https://github.com/kepano/obsidian-skills | `E:\aimodel\obsidian-skills\` | 已克隆，5 个 skills 保留在当前目录 |
| pi | https://github.com/earendil-works/pi | `E:\aimodel\pi\` | 已克隆，待按需研究 CLI/TUI/agent 包 |
| vue-tui | https://github.com/Simon-He95/vue-tui | `E:\aimodel\vue-tui\` | 已克隆，包含 `.agents\skills\vue-tui\SKILL.md` |

---

**记录人**: liuhao
**更新时间**: 2026-07-30 11:08:51 +08:00

---

## 2026-08-15 第四批下载记录

### 新增仓库

| 仓库 | 来源 | 本地目录 | 状态 |
|------|------|----------|------|
| LEANN | https://github.com/StarTrail-org/LEANN | `E:\aimodel\LEANN\` | 已克隆；包含 OpenClaw `leann-memory` 适配，未安装 `leann-core` |
| emilkowalski/skills | https://github.com/emilkowalski/skills | `E:\aimodel\emilkowalski-skills\` | 已克隆；10 个正式 skills，未执行 `npx skills` 安装 |
| open-source-games | https://github.com/bobeff/open-source-games | `E:\aimodel\open-source-games\` | 已克隆；仅作游戏参考 |
| build-your-own-x | https://github.com/codecrafters-io/build-your-own-x | `E:\aimodel\build-your-own-x\` | 已克隆；仅作从零实现软件的参考 |
| SESA-Self-Evolving-Search-Agents | https://github.com/Zenghuang-Fu/SESA-Self-Evolving-Search-Agents | `E:\aimodel\SESA-Self-Evolving-Search-Agents\` | 已克隆；研究代码，未安装 CUDA/Python 依赖 |

### 已同步仓库

- `open-design/`: 从 `f580271` 快进到 `30fc648f`。
- `pi/`: 从 `e47b8e37a` 快进到 `b1efcf7d7`。

### 论文下载

- `E:\aimodel\arxiv-2607.29468v1.pdf`，SESA 论文，约 1.0 MB。
- `E:\aimodel\arxiv-2607.27733v1.pdf`，VeriSkill 论文，约 0.7 MB。

本批没有执行依赖安装、全局 skill 安装或子目录 Markdown 更新。

---

## 2026-08-15 其他 skill 更新记录

- 扫描一级 Git 仓库远程地址、`SKILL.md` 数量和工作区状态。
- 使用 `git pull --ff-only` 更新 26 个干净的 skill 仓库。
- 15 个仓库已是最新。
- `reverse-skill` 因 3 个本地修改文件跳过更新。
- 补登记 `different-ai/openwork` 和 `Graphify-Labs/graphify` 的仓库链接。

本轮仍未安装依赖、未复制到全局 Codex skills 目录，也未修改仓库子目录 Markdown。

---

## 2026-08-17 第五批下载与同步

- `ui-ux-pro-max-skill/`：已快进到 `a38d04c`，包含 6 个 `SKILL.md`。
  - 来源: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- `awesome-design-md/`：已克隆到 `8147538`，包含 73 个 `DESIGN.md` 设计系统参考文档。
  - 来源: https://github.com/VoltAgent/awesome-design-md
- 本批未执行依赖安装、全局 Codex skill 安装或仓库子目录 Markdown 更新。
