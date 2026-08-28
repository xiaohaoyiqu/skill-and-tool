# AI开发资源库下载完成记录

**@author liuhao**
**日期**: 2026-05-01
**时间**: 14:00:00
**类型**: 资源整理

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
