# 一级 Git 仓库版本清单

**扫描目录**: `E:\aimodel`

**目录计数与本批核验时间**: 2026-10-27（当日核验 6 个 Skill/工具仓库和 5 个模型源码仓库，其余行保留各自历史状态）

**一级仓库目录数（2026-10-27）**: 111（110 个可见第三方仓库 + 1 个隐藏聚合仓库）

本表记录一级 Git 仓库的上游地址、当前分支、提交和同步状态。第三方仓库实体不重复上传到本聚合仓库；需要内容时应从对应上游克隆并遵守其许可证。Skill 数量与能力评估见 [SKILLS_INDEX.md](SKILLS_INDEX.md)，批次说明见 [GITHUB_REPOS.md](GITHUB_REPOS.md)。

状态含义：`已同步` 表示扫描时本地 HEAD 与已配置上游一致；`本地修改` 表示为保护工作区而跳过更新；`分叉 +A/-B` 表示本地相对上游领先 A 个、落后 B 个提交，没有自动改写历史。

2026-11-08 Agent Reach 版本补充：保留 `Agent-Reach/` v1.5.0（`da5044d26fc6adddb6554d5679c94ac22e76e428`），另存官方 `v1.6.1` 至 `Agent-Reach-v1.6.1/`（`7a38047acf26a729cbb27851e3cb81639da86b29`，tag 分离 HEAD，克隆后工作树干净）。这是同一项目的版本副本；本轮只核对该副本，不重算历史总数或更新其他仓库同步状态，未安装依赖或全局配置。见[下载台账](GITHUB_REPOS.md#2026-11-08-agent-reach-v161源码快照)。

2026-11-02 链接专项核对：当前可见的 112 个一级 Git 仓库均已列入下表，目录存在且记录来源与本地 origin 一致。本轮未重新拉取或复核各仓库提交与工作区同步状态，上方历史计数及各行版本状态仍保留原核验口径。对外介绍见 [分享清单](SHARE_GUIDE.md)，旧收藏清单漏项及上游地址变化见 [链接对照](GITHUB_STAR_LIST.md#2026-11-02-全量链接对照)。

2026-08-29 只新增并核验 `loopx`、`ego-lite`。2026-09-02 新增 `archify`、`sepia` 的完整克隆记录。2026-09-03 新增 `pdf-inspector`、`effective-html` 的浅克隆记录，并复核既有 `andrej-karpathy-skills`、`mattpocock-skills`。2026-09-05 新增 `zvec-grep`、`terraform`、`patent-disclosure-skill` 的完整克隆，将既有 `graphify` 补齐为完整历史；随后扫描并更新全部 92 个可见一级仓库：43 个实际快进、47 个原本最新，`codetracer` 因上游删除 `main` 而安全切换到 `stable`（旧 `main` 及 3 个独有提交仍保留），`reverse-skill` 因 3 个本地修改跳过。2026-09-14 新增 `rare-ui`、`shadcn-ui`、`beautiful-ui`、`beui`、`transitions-dev`、`no-ai-slop` 6 个浅克隆；`ebook-treasure-chest` 与 `3b1b/manim` 当时仅登记。2026-09-15 新增 `open-code-review`、`Ghost-Downloader-3` 两个浅克隆，`handraw-style` 因无明确许可证且图片体量较大而只登记；同时补记根目录中现已存在的 `manim` 浅克隆。

2026-10-27 新增 `skill-up`、`rea`、`ghidra`、`ECC` 4 个浅克隆，并更新既有 `open-code-review` 和 `Ghost-Downloader-3`。下载器上游强制更新后，保留旧 `main@601e2068`，新建 `catalog/upstream-20261027` 跟踪 `origin/main`。REA 的 5 个第三方子模块仅登记锁定提交，未初始化；Ghidra 仅保存源码，未下载可运行发行包。本轮 6 个父仓库均通过 Git 对象校验、当前工作树干净且与已抓取 upstream 一致；其余仓库没有重新拉取。详细证据见 [批次 JSON](../scripts/repository-batch-20261027.json)。

同日补充 Magenta RealTime 2、Pocket TTS、Supertonic、TimesFM 与 VibeVoice 的本地使用评价。5 个源码浅克隆形成于用户澄清“不需要下载，有记录就更新”之前；此后仅更新记录。既有 TimesFM 预测 Skill 已交叉引用，模型未运行。证据见 [模型评价台账](GITHUB_REPOS.md#2026-10-27-模型记录与本地适配评价) 与 [模型批次 JSON](../scripts/repository-model-review-20261027.json)。

2026-10-30仅新增`kgka_Music_hl`浅克隆，确认master@166e84bd工作树干净；搜索/API来源及许可评价见GITHUB_REPOS.md。不重拉其他仓库，历史目录计数保持其原核验日期。

2026-11-01 新增 `stt` 当前版本的浅克隆，含 Git 文件约 1.98 MiB，低于本轮 100 MB 限额；工作树干净并通过对象校验。未重新扫描其他仓库，历史总数保持原核验日期。详细大小口径和证据见 [下载台账](GITHUB_REPOS.md#2026-11-01-stt-本地音视频转文字工具)。

2026-11-09 仅更新已有 `skill-up`，新增 `OpenShell` 和 `context-mode` 两个浅克隆，三者均低于 100 MB，工作树干净并通过 Git 对象校验。`huashu-art-motion` 在展开前核算约 148.62 MB，超过限额，已跳过并清理临时目录，不列入下方本地仓库表。没有重扫其他仓库或改写历史总数。`blender-skills` 已于 11 月 2 日登记链接，本轮复核仍无本地目录。详见 [本批台账](GITHUB_REPOS.md#2026-11-09-skill-评测艺术动画与-agent-工具) 和 [JSON](../scripts/repository-review-20261109.json)。

2026-11-11 新登记 8 个来源，其中 7 个新增浅克隆均小于 100 MB，工作树干净并通过 Git 对象校验。`openvid` 源码文件已约 181.96 MB，下载前跳过，只保留来源，不列入下方本地仓库表。本轮没有重扫其他仓库、改写历史总数或安装依赖。详见 [本批台账](GITHUB_REPOS.md#2026-11-11-音视频认证代码检索与学习资料) 与 [核验 JSON](../scripts/repository-review-20261111.json)。

| 本地目录 | 上游 | 分支 | HEAD | 状态 |
|------|------|------|------|------|
| stemdeck | https://github.com/stemdeckapp/stemdeck.git | main | `5f9405ca` | 新增浅克隆（2026-11-11）；14.96 MB，干净且与 origin/main 一致；仅源码/资料 |
| openauth | https://github.com/anomalyco/openauth.git | master | `98dc5962` | 新增浅克隆（2026-11-11）；4.47 MB，干净且与 origin/master 一致；仅源码/资料 |
| laya | https://github.com/NandhaKishorM/laya.git | main | `3a38cbe8` | 新增浅克隆（2026-11-11）；74.47 MB，干净且与 origin/main 一致；仅源码/资料 |
| Ix | https://github.com/ix-infrastructure/Ix.git | main | `b7ea8d9b` | 新增浅克隆（2026-11-11）；20.16 MB，干净且与 origin/main 一致；仅源码/资料 |
| Hands-On-Large-Language-Models | https://github.com/HandsOnLLM/Hands-On-Large-Language-Models.git | main | `ea339081` | 新增浅克隆（2026-11-11）；19.71 MB，干净且与 origin/main 一致；仅源码/资料 |
| HowToLiveBetter | https://github.com/eternity4719/HowToLiveBetter.git | main | `dff814dc` | 新增浅克隆（2026-11-11）；9.79 MB，干净且与 origin/main 一致；仅源码/资料 |
| up | https://github.com/byoungd/up.git | main | `ddc96d37` | 新增浅克隆（2026-11-11）；36.86 MB，干净且与 origin/main 一致；仅源码/资料 |
| OpenShell | https://github.com/NVIDIA/OpenShell.git | main | `9525bec0` | 新增浅克隆（2026-11-09）；约 55.65 MB，干净且与 origin/main 一致；仅源码参考 |
| context-mode | https://github.com/mksglu/context-mode.git | main | `3a3ef7d5` | 新增浅克隆（2026-11-09）；v2.1.7，约 37.44 MB，Elastic-2.0；未配置 hooks/MCP |
| stt | https://github.com/jianchang512/stt.git | main | `0df3151d` | 已浅克隆（2026-11-01）；v0.0.94，约 1.98 MiB，干净且与 origin/main 一致 |
| kgka_Music_hl | https://github.com/umr-xiaomai/kgka_Music_hl.git | master | `166e84bd` | 已浅克隆（2026-10-30）；静态参考，在线API未实测 |
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
| beautiful-ui | https://github.com/slev12397/beautiful-ui.git | main | `ff0f74d6` | 已浅克隆（2026-09-14） |
| beui | https://github.com/starc007/ui-components.git | main | `8d3fa7b4` | 已浅克隆（2026-09-14） |
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
| ECC | https://github.com/affaan-m/ECC.git | main | `25278e7d` | 新增浅克隆；主 skills/ 下 311 个入口（2026-10-27） |
| effective-html | https://github.com/plannotator/effective-html.git | main | `d95debba` | 已克隆（浅克隆，2026-09-03） |
| emilkowalski-skills | https://github.com/emilkowalski/skills.git | main | `d23d7f88` | 已同步 |
| goose | https://github.com/aaif-goose/goose.git | main | `5e909259` | 已同步（2026-09-05） |
| gortex | https://github.com/zzet/gortex.git | main | `134f4f20` | 已同步（2026-09-05） |
| Ghost-Downloader-3 | https://github.com/XiaoYouChR/Ghost-Downloader-3.git | catalog/upstream-20261027 | `ee0cb1aa` | 已跟踪当前上游；旧 main@601e2068 保留；cat-catch@b34a7677（2026-10-27） |
| ghidra | https://github.com/NationalSecurityAgency/ghidra.git | master | `1b9e58a9` | 新增浅克隆；源码，非运行发行包（2026-10-27） |
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
| magenta-realtime | https://github.com/magenta/magenta-realtime.git | main | `694a545e` | 源码浅克隆；SequenceLayers 子模块未初始化；后续仅更新记录（2026-10-27） |
| markdown-viewer-skills | https://github.com/markdown-viewer/skills.git | main | `a3afd455` | 已同步 |
| manim | https://github.com/3b1b/manim.git | master | `fafa083a` | 已有浅克隆；2026-09-15 补登记 |
| mattpocock-skills | https://github.com/mattpocock/skills.git | main | `3cca18b3` | 已同步（2026-09-05） |
| mergration | https://github.com/38tter/mergration.git | main | `0595ea02` | 已同步 |
| mermaid-erd-generator | https://github.com/nharsch/mermaid-erd-generator.git | main | `cbecf0ba` | 已同步 |
| minimax-skills | https://github.com/MiniMax-AI/skills.git | main | `60aaae52` | 已同步 |
| multi-style-image-generator | https://github.com/powerycy/multi-style-image-generator.git | main | `db800774` | 已同步（2026-09-05） |
| nanobrowser | https://github.com/nanobrowser/nanobrowser.git | master | `24a14b76` | 已同步 |
| nature-skills | https://github.com/Yuan1z0825/nature-skills.git | main | `b1a37a2b` | 已同步（2026-09-05） |
| nginx-http-flv-module | https://github.com/winshining/nginx-http-flv-module.git | master | `2ad3dabe` | 已同步 |
| no-ai-slop | https://github.com/petergyang/no-ai-slop.git | main | `000650b1` | 已浅克隆（2026-09-14） |
| obsidian-skills | https://github.com/kepano/obsidian-skills.git | main | `a1dc48e6` | 已同步 |
| OpenCLI | https://github.com/jackwener/OpenCLI.git | main | `8271afc6` | 已同步（2026-09-05） |
| open-code-review | https://github.com/alibaba/open-code-review.git | main | `375f64cd` | 已快进同步；保持浅克隆（2026-10-27） |
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
| pocket-tts | https://github.com/kyutai-labs/pocket-tts.git | main | `77c3d76b` | 源码浅克隆；CPU TTS 评价，未安装模型（2026-10-27） |
| public-apis | https://github.com/public-apis/public-apis.git | master | `9d042687` | 已同步（2026-09-05） |
| python-refactoring-skills | https://github.com/l-mb/python-refactoring-skills.git | main | `b0835710` | 已同步 |
| rare-ui | https://github.com/swamimalode07/rare-ui.git | main | `d146c352` | 已浅克隆（2026-09-14） |
| rea | https://github.com/morluto/rea.git | main | `570abe95` | 新增浅克隆；5 个第三方子模块未初始化（2026-10-27） |
| reverse-skill | https://github.com/zhaoxuya520/reverse-skill.git | main | `a5171e03` | 本地修改 3；ahead 1 / behind 142，未拉取 |
| SafeGuard-Code-Profiler | https://github.com/hamed-kuheil/SafeGuard-Code-Profiler.git | main | `6d759c29` | 已同步 |
| scientific-agent-skills | https://github.com/K-Dense-AI/scientific-agent-skills.git | main | `1e5eeffb` | 已同步（2026-09-05） |
| scramble | https://github.com/dedoc/scramble.git | main | `7cf945d1` | 已同步（2026-09-05） |
| sepia | https://github.com/Nanako0129/sepia.git | main | `401c89e4` | 已同步（2026-09-05） |
| SESA-Self-Evolving-Search-Agents | https://github.com/Zenghuang-Fu/SESA-Self-Evolving-Search-Agents.git | master | `74de5d77` | 已同步 |
| shadcn-ui | https://github.com/shadcn-ui/ui.git | main | `2b3e6d4f` | 已浅克隆（2026-09-14） |
| skill-up | https://github.com/alibaba/skill-up.git | main | `78148136` | 已快进更新（2026-11-09）；约 13.00 MB，1 个正式 skill-upper；干净且与 origin/main 一致 |
| skills-compat-manager | https://github.com/hnaymyh123-henry/skills-compat-manager.git | master | `8be1357e` | 已同步 |
| skillspector | https://github.com/NVIDIA/skillspector.git | main | `7805bb94` | 已同步（2026-09-05） |
| skillsProject-AI-Log-Analyzer | https://github.com/sahanaydn/skillsProject-AI-Log-Analyzer.git | main | `3682eae2` | 已同步 |
| SmeLLM | https://github.com/refactoring-assistant/SmeLLM.git | main | `8b3a5250` | 已同步 |
| superpowers-repo | https://github.com/obra/superpowers.git | main | `b36e0829` | 已同步 |
| supertonic | https://github.com/supertone-oss-archive/supertonic.git | main | `1e9799e9` | 源码浅克隆；已归档，记录维护与权重许可差异（2026-10-27） |
| SupplyChainScanner | https://github.com/benjiamin911/SupplyChainScanner.git | main | `6e4dcc10` | 已同步 |
| taste-skill | https://github.com/Leonxlnx/taste-skill.git | main | `ccbc1563` | 已同步 |
| terraform | https://github.com/hashicorp/terraform.git | main | `7b8c301b` | 已完整克隆（2026-09-05） |
| timesfm | https://github.com/google-research/timesfm.git | master | `e51928e2` | 源码浅克隆；交叉引用已有预测 Skill，区分 2.5/3.0 许可（2026-10-27） |
| transitions-dev | https://github.com/Jakubantalik/transitions.dev.git | main | `598d3d6a` | 已浅克隆（2026-09-14） |
| ui-ux-pro-max-skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git | main | `f3ac1952` | 已同步（2026-09-05） |
| vue-skills-full | https://github.com/vuejs-ai/skills.git | main | `c9d355ff` | 已同步 |
| VibeVoice | https://github.com/microsoft/VibeVoice.git | main | `16fb2cb1` | 源码浅克隆；区分历史 TTS、Realtime 与 ASR，未运行（2026-10-27） |
| vue-tui | https://github.com/Simon-He95/vue-tui.git | main | `07ef737a` | 已同步（2026-09-05） |
| web-access | https://github.com/eze-is/web-access.git | main | `33eef84a` | 已同步 |
| WebSecurityScanner | https://github.com/Defensive-Alliance/WebSecurityScanner.git | main | `60a02b48` | 已同步 |
| z-skills | https://github.com/tjxj/z-skills.git | main | `50539dc6` | 已同步 |
| zvec-grep | https://github.com/zvec-ai/zvec-grep.git | main | `52653951` | 已完整克隆（2026-09-05） |

## 本聚合仓库实际保存的本地内容

- 根目录 README 与变更记录，以及 `docs/` 下的索引、维护说明和历史台账。
- `multi-search-engine/`：上游单文件 Skill 快照及本地审计说明。
- `zhihu-cli-skill/`：本地维护的知乎 CLI Skill 包，不包含账号凭据。

PDF、ZIP、`.env`、缓存、依赖、构建产物、嵌套 `.git` 和第三方仓库工作树均由根 `.gitignore` 默认排除。
