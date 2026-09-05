# 一级 Git 仓库版本清单

**扫描目录**: `E:\aimodel`

**扫描时间**: 2026-09-05

**一级仓库目录数（2026-09-05）**: 93（92 个可见第三方仓库 + 1 个隐藏聚合仓库）

本表记录一级 Git 仓库的上游地址、当前分支、提交和同步状态。第三方仓库实体不重复上传到本聚合仓库；需要内容时应从对应上游克隆并遵守其许可证。Skill 数量与能力评估见 [SKILLS_INDEX.md](SKILLS_INDEX.md)，批次说明见 [GITHUB_REPOS.md](GITHUB_REPOS.md)。

状态含义：`已同步` 表示扫描时本地 HEAD 与已配置上游一致；`本地修改` 表示为保护工作区而跳过更新；`分叉 +A/-B` 表示本地相对上游领先 A 个、落后 B 个提交，没有自动改写历史。

2026-08-29 只新增并核验 `loopx`、`ego-lite`。2026-09-02 新增 `archify`、`sepia` 的完整克隆记录。2026-09-03 新增 `pdf-inspector`、`effective-html` 的浅克隆记录，并复核既有 `andrej-karpathy-skills`、`mattpocock-skills`。2026-09-05 新增 `zvec-grep`、`terraform`、`patent-disclosure-skill` 的完整克隆，将既有 `graphify` 补齐为完整历史；随后扫描并更新全部 92 个可见一级仓库：43 个实际快进、47 个原本最新，`codetracer` 因上游删除 `main` 而安全切换到 `stable`（旧 `main` 及 3 个独有提交仍保留），`reverse-skill` 因 3 个本地修改跳过。

| 本地目录 | 上游 | 分支 | HEAD | 状态 |
|------|------|------|------|------|
| Agent-Reach | https://github.com/Panniantong/Agent-Reach.git | main | `da5044d2` | 已同步（2026-09-05） |
| agent-rules-books | https://github.com/ciembor/agent-rules-books.git | main | `9c876361` | 已同步 |
| archify | https://github.com/tt-a1i/archify.git | main | `d8e4daf2` | 已同步（2026-09-05） |
| agent-skills | https://github.com/addyosmani/agent-skills.git | main | `84ee5067` | 已同步（2026-09-05） |
| AI-Research-SKILLs | https://github.com/Orchestra-Research/AI-Research-SKILLs.git | main | `773a5294` | 已同步 |
| ai-unit-tests-generator | https://github.com/gustavolopess/ai-unit-tests-generator.git | main | `064857e2` | 已同步 |
| andrej-karpathy-skills | https://github.com/multica-ai/andrej-karpathy-skills.git | main | `2c606141` | 已同步 |
| anthropic-skills | https://github.com/anthropics/skills.git | main | `41bbe19d` | 已同步（2026-09-05） |
| avoid-ai-writing | https://github.com/conorbronsdon/avoid-ai-writing.git | main | `4b922189` | 已同步（2026-09-05） |
| awesome-agent-skills | https://github.com/JackyST0/awesome-agent-skills.git | main | `2961d1ea` | 已同步（2026-09-05） |
| Awesome-Agent-Skills-for-Empirical-Research | https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git | main | `129c4591` | 已同步（含锁定子模块，2026-09-05） |
| awesome-claude-skills | https://github.com/travisvn/awesome-claude-skills.git | main | `1da55aa8` | 已同步 |
| awesome-design-md | https://github.com/VoltAgent/awesome-design-md.git | main | `8147538b` | 已同步 |
| awesome-llm-apps | https://github.com/Shubhamsaboo/awesome-llm-apps.git | main | `24c85b09` | 已同步（2026-09-05） |
| browser-use | https://github.com/browser-use/browser-use.git | main | `d5453ae8` | 已同步（2026-09-05） |
| build-your-own-x | https://github.com/codecrafters-io/build-your-own-x.git | master | `aa17439b` | 已同步 |
| caveman-full | https://github.com/JuliusBrussee/caveman.git | main | `5184b3d1` | 已同步（2026-09-05） |
| chrome-devtools-mcp | https://github.com/ChromeDevTools/chrome-devtools-mcp.git | main | `086299a6` | 已同步（2026-09-05） |
| claude-cookbooks | https://github.com/anthropics/claude-cookbooks.git | main | `a97b9a2d` | 已同步（2026-09-05） |
| claude-guides-full | https://github.com/vtroisWhite/andrej-karpathy-skills.git | main | `54a3028c` | 已同步 |
| claude-scholar | https://github.com/Galaxy-Dawn/claude-scholar.git | main | `6ed46dac` | 已同步 |
| claude-skill-refactoring-ui | https://github.com/opkod-france/claude-skill-refactoring-ui.git | main | `80994d98` | 已同步 |
| claude-video | https://github.com/bradautomates/claude-video.git | main | `83da59fa` | 已同步 |
| code-review-plugin | https://github.com/anthropics/claude-plugins-official.git | main | `85cce038` | 已同步（2026-09-05） |
| codetracer | https://github.com/metacraft-labs/codetracer.git | stable | `0478cb4f` | 已跟踪新默认分支；旧 `main` 保留 3 个独有提交 |
| crawl4ai | https://github.com/unclecode/crawl4ai.git | main | `862f6bcc` | 已同步（2026-09-05） |
| daizhigev20 | https://github.com/daizhige-org/daizhigev20.git | data | `012bc393` | 已同步 |
| developer-portfolios | https://github.com/emmabostian/developer-portfolios.git | master | `c7c021be` | 已同步（2026-09-05） |
| ego-lite | https://github.com/citrolabs/ego-lite.git | main | `5ca3c36c` | 已同步（浅克隆） |
| effective-html | https://github.com/plannotator/effective-html.git | main | `d95debba` | 已克隆（浅克隆，2026-09-03） |
| emilkowalski-skills | https://github.com/emilkowalski/skills.git | main | `d23d7f88` | 已同步 |
| goose | https://github.com/aaif-goose/goose.git | main | `5e909259` | 已同步（2026-09-05） |
| gortex | https://github.com/zzet/gortex.git | main | `134f4f20` | 已同步（2026-09-05） |
| graphify | https://github.com/Graphify-Labs/graphify.git | v8 | `937e59a5` | 已补全历史并同步（2026-09-05） |
| hallmark | https://github.com/Nutlope/hallmark.git | main | `13ac0ec7` | 已同步 |
| headroom | https://github.com/headroomlabs-ai/headroom.git | main | `e59cf101` | 已同步（2026-09-05） |
| Humanizer-zh | https://github.com/op7418/Humanizer-zh.git | main | `91f3d394` | 已同步 |
| human-writing | https://github.com/KKKKhazix/human-writing.git | main | `4fda173f` | 已同步 |
| hyperframes | https://github.com/heygen-com/hyperframes.git | main | `ae3d80c3` | 已同步（2026-09-05） |
| inspira-ui | https://github.com/rahulv-official/inspira-ui.git | main | `db389077` | 已同步（2026-09-05） |
| kepano-obsidian | https://github.com/kepano/kepano-obsidian.git | main | `47369734` | 已同步 |
| khazix-skills | https://github.com/KKKKhazix/khazix-skills.git | main | `7a5c4934` | 已同步 |
| knowledge-work-plugins | https://github.com/anthropics/knowledge-work-plugins.git | main | `1f517b9d` | 已同步（2026-09-05） |
| last30days-skill | https://github.com/mvanhorn/last30days-skill.git | main | `56ba5ace` | 已同步（2026-09-05） |
| LEANN | https://github.com/StarTrail-org/LEANN.git | main | `9b786b02` | 已同步（2026-09-05） |
| liteparse | https://github.com/run-llama/liteparse.git | main | `cc38a9cc` | 已同步（2026-09-05） |
| loopx | https://github.com/huangruiteng/loopx.git | main | `e3f9b536` | 已同步（浅克隆，2026-09-05） |
| markdown-viewer-skills | https://github.com/markdown-viewer/skills.git | main | `a3afd455` | 已同步 |
| mattpocock-skills | https://github.com/mattpocock/skills.git | main | `3cca18b3` | 已同步（2026-09-05） |
| mergration | https://github.com/38tter/mergration.git | main | `0595ea02` | 已同步 |
| mermaid-erd-generator | https://github.com/nharsch/mermaid-erd-generator.git | main | `cbecf0ba` | 已同步 |
| minimax-skills | https://github.com/MiniMax-AI/skills.git | main | `60aaae52` | 已同步 |
| multi-style-image-generator | https://github.com/powerycy/multi-style-image-generator.git | main | `db800774` | 已同步（2026-09-05） |
| nanobrowser | https://github.com/nanobrowser/nanobrowser.git | master | `24a14b76` | 已同步 |
| nature-skills | https://github.com/Yuan1z0825/nature-skills.git | main | `b1a37a2b` | 已同步（2026-09-05） |
| nginx-http-flv-module | https://github.com/winshining/nginx-http-flv-module.git | master | `2ad3dabe` | 已同步 |
| obsidian-skills | https://github.com/kepano/obsidian-skills.git | main | `a1dc48e6` | 已同步 |
| OpenCLI | https://github.com/jackwener/OpenCLI.git | main | `8271afc6` | 已同步（2026-09-05） |
| open-design | https://github.com/nexu-io/open-design.git | main | `50e305df` | 已同步（2026-09-05） |
| open-source-games | https://github.com/bobeff/open-source-games.git | main | `3a9ab8fc` | 已同步 |
| openwork | https://github.com/different-ai/openwork.git | dev | `89558a98` | 已同步（2026-09-05） |
| Paper2Any | https://github.com/OpenDCAI/Paper2Any | main | `b538531e` | 已同步（2026-09-05） |
| PaperSpine | https://github.com/WUBING2023/PaperSpine.git | main | `1fe46f0e` | 已同步（2026-09-05） |
| patent-disclosure-skill | https://github.com/handsomestWei/patent-disclosure-skill.git | main | `a0156905` | 已完整克隆（2026-09-05） |
| pdf-inspector | https://github.com/firecrawl/pdf-inspector.git | main | `636ca1a5` | 已同步（浅克隆，2026-09-05） |
| pi | https://github.com/earendil-works/pi.git | main | `da840b62` | 已同步（2026-09-05） |
| pipeforge | https://github.com/Sheraz-k/pipeforge.git | master | `ba84e9ff` | 已同步 |
| pisper | https://github.com/ling-kong-ran/pisper.git | release | `90983c5c` | 已同步（2026-09-05） |
| playcaptcha | https://github.com/mortspace/playcaptcha.git | main | `e9e0e0f0` | 已同步 |
| public-apis | https://github.com/public-apis/public-apis.git | master | `9d042687` | 已同步（2026-09-05） |
| python-refactoring-skills | https://github.com/l-mb/python-refactoring-skills.git | main | `b0835710` | 已同步 |
| reverse-skill | https://github.com/zhaoxuya520/reverse-skill.git | main | `a5171e03` | 本地修改 3；ahead 1 / behind 142，未拉取 |
| SafeGuard-Code-Profiler | https://github.com/hamed-kuheil/SafeGuard-Code-Profiler.git | main | `6d759c29` | 已同步 |
| scientific-agent-skills | https://github.com/K-Dense-AI/scientific-agent-skills.git | main | `1e5eeffb` | 已同步（2026-09-05） |
| scramble | https://github.com/dedoc/scramble.git | main | `7cf945d1` | 已同步（2026-09-05） |
| sepia | https://github.com/Nanako0129/sepia.git | main | `401c89e4` | 已同步（2026-09-05） |
| SESA-Self-Evolving-Search-Agents | https://github.com/Zenghuang-Fu/SESA-Self-Evolving-Search-Agents.git | master | `74de5d77` | 已同步 |
| skills-compat-manager | https://github.com/hnaymyh123-henry/skills-compat-manager.git | master | `8be1357e` | 已同步 |
| skillspector | https://github.com/NVIDIA/skillspector.git | main | `7805bb94` | 已同步（2026-09-05） |
| skillsProject-AI-Log-Analyzer | https://github.com/sahanaydn/skillsProject-AI-Log-Analyzer.git | main | `3682eae2` | 已同步 |
| SmeLLM | https://github.com/refactoring-assistant/SmeLLM.git | main | `8b3a5250` | 已同步 |
| superpowers-repo | https://github.com/obra/superpowers.git | main | `b36e0829` | 已同步 |
| SupplyChainScanner | https://github.com/benjiamin911/SupplyChainScanner.git | main | `6e4dcc10` | 已同步 |
| taste-skill | https://github.com/Leonxlnx/taste-skill.git | main | `ccbc1563` | 已同步 |
| terraform | https://github.com/hashicorp/terraform.git | main | `7b8c301b` | 已完整克隆（2026-09-05） |
| ui-ux-pro-max-skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git | main | `f3ac1952` | 已同步（2026-09-05） |
| vue-skills-full | https://github.com/vuejs-ai/skills.git | main | `c9d355ff` | 已同步 |
| vue-tui | https://github.com/Simon-He95/vue-tui.git | main | `07ef737a` | 已同步（2026-09-05） |
| web-access | https://github.com/eze-is/web-access.git | main | `33eef84a` | 已同步 |
| WebSecurityScanner | https://github.com/Defensive-Alliance/WebSecurityScanner.git | main | `60a02b48` | 已同步 |
| z-skills | https://github.com/tjxj/z-skills.git | main | `50539dc6` | 已同步 |
| zvec-grep | https://github.com/zvec-ai/zvec-grep.git | main | `52653951` | 已完整克隆（2026-09-05） |

## 本聚合仓库实际保存的本地内容

- 根目录索引与变更台账。
- `multi-search-engine/`：上游单文件 Skill 快照及本地审计说明。
- `zhihu-cli-skill/`：本地维护的知乎 CLI Skill 包，不包含账号凭据。

PDF、ZIP、`.env`、缓存、依赖、构建产物、嵌套 `.git` 和第三方仓库工作树均由根 `.gitignore` 默认排除。
