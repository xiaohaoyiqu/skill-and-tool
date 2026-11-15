# 一级 Git 仓库版本清单

**扫描目录**: `E:\aimodel`

**最新全目录核验**: 2026-11-15；134 个可见一级仓库，另有 1 个隐藏聚合仓库；结果见[全目录同步台账](GITHUB_REPOS.md#2026-11-15-全目录同步)。下表各行均已刷新为本次本地实际 HEAD，历史批次说明保留原日期。

**历史目录计数与本批核验时间**: 2026-10-27（当日核验 6 个 Skill/工具仓库和 5 个模型源码仓库，其余行保留各自历史状态）

**历史一级仓库目录数（2026-10-27）**: 111（110 个可见第三方仓库 + 1 个隐藏聚合仓库）

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

2026-11-12 新增 `harness2/`、`minimind/` 和 `DeepTutor/`，含 Git 分别 15.30、23.36、106.70 MB，工作树干净、与本次抓取的上游默认分支一致并通过对象校验。DeepTutor 初次超限跳过后按用户明确授权重新克隆，作为该项目的大小例外保留，其他项目仍沿用 100 MB 限额。Orthros 只保存论文；本轮不重算历史目录总数或更新其他项目。见[台账](GITHUB_REPOS.md#2026-11-12-harness²orthrosdeeptutor-与-minimind)及[核验 JSON](../scripts/repository-review-20261112.json)。

2026-11-13 新增 `VoxCPM/` 和 `modern-web-guidance/` 两个浅克隆，含 Git 分别 10.14、3.16 MB，均低于 100 MB，工作树干净、与已抓取的 origin/main 一致并通过对象校验。Modern Web Guidance 的 2 个正式 Skill 入口随源码保存；未安装依赖、模型或全局配置，未更新其他仓库或重算历史总数。见[本批台账](GITHUB_REPOS.md#2026-11-13-voxcpm-与-modern-web-guidance)及[核验 JSON](../scripts/repository-review-20261113.json)。

2026-11-15 新增 `prompts.chat/`、`freebie-radar/`、`Horizon/` 三个源码浅克隆，含 Git 分别为 250.65、3.92、15.60 MB；prompts.chat 按用户指令豁免本批大小限制。`modern-web-guidance-src` 源码已达 101.45 MB，超限只登记。两个 11 月 13 日已有项目在线核对仍为最新。五个本地仓库均工作树干净并通过对象校验；未安装依赖或全局 Skill。见[下载台账](GITHUB_REPOS.md#2026-11-15-提示词社区资源雷达与-modern-web-guidance-源码)及[核验 JSON](../scripts/repository-review-20261115.json)。

2026-11-15 追加核验五个项目：新增 tailcat、codex-security、modern-web-guidance-src，快进更新 open-code-review 与 chrome-devtools-mcp。默认限额提高为 120 MB；modern-web-guidance-src 按明确授权保留 178.77 MB 源码浅克隆。五者校验通过，历史目录总数不重算。详见[本批台账](GITHUB_REPOS.md#2026-11-15-网络工具安全审查与-chrome-项目追加核验)。

| 本地目录 | 上游 | 分支 | HEAD | 状态 |
|------|------|------|------|------|
| Agent-Reach | https://github.com/Panniantong/Agent-Reach.git | main | `c70ae6da` | 已快进更新并通过对象校验（2026-11-15） |
| Agent-Reach-v1.6.1 | https://github.com/Panniantong/Agent-Reach.git | 分离 HEAD | `7a38047a` | 无 upstream，保留原状（2026-11-15） |
| agent-rules-books | https://github.com/ciembor/agent-rules-books.git | main | `893a88a6` | 已快进更新并通过对象校验（2026-11-15） |
| agent-skills | https://github.com/addyosmani/agent-skills.git | main | `39b723ce` | 已快进更新并通过对象校验（2026-11-15） |
| AI-Research-SKILLs | https://github.com/Orchestra-Research/AI-Research-SKILLs.git | main | `773a5294` | 已在线核对，无需更新（2026-11-15） |
| ai-unit-tests-generator | https://github.com/gustavolopess/ai-unit-tests-generator.git | main | `064857e2` | 已在线核对，无需更新（2026-11-15） |
| andrej-karpathy-skills | https://github.com/multica-ai/andrej-karpathy-skills.git | main | `2c606141` | 已在线核对，无需更新（2026-11-15） |
| anthropic-skills | https://github.com/anthropics/skills.git | main | `1780c5e5` | 已快进更新并通过对象校验（2026-11-15） |
| archify | https://github.com/tt-a1i/archify.git | main | `a7ed6fd6` | 已快进更新并通过对象校验（2026-11-15） |
| avoid-ai-writing | https://github.com/conorbronsdon/avoid-ai-writing.git | main | `cc1d3431` | 已快进更新并通过对象校验（2026-11-15） |
| awesome-agent-skills | https://github.com/JackyST0/awesome-agent-skills.git | main | `f1a7927f` | 已快进更新并通过对象校验（2026-11-15） |
| Awesome-Agent-Skills-for-Empirical-Research | https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git | main | `8684584e` | 已快进更新并通过对象校验（2026-11-15） |
| awesome-claude-skills | https://github.com/travisvn/awesome-claude-skills.git | main | `1da55aa8` | 已在线核对，无需更新（2026-11-15） |
| awesome-design-md | https://github.com/VoltAgent/awesome-design-md.git | main | `fcc70284` | 已快进更新并通过对象校验（2026-11-15） |
| awesome-llm-apps | https://github.com/Shubhamsaboo/awesome-llm-apps.git | main | `8d2a71df` | 已快进更新并通过对象校验（2026-11-15） |
| beautiful-ui | https://github.com/slev12397/beautiful-ui.git | main | `44a274e5` | 已快进更新并通过对象校验（2026-11-15） |
| beui | https://github.com/starc007/ui-components.git | main | `039012eb` | 已快进更新并通过对象校验（2026-11-15） |
| browser-use | https://github.com/browser-use/browser-use.git | main | `e717df18` | 已快进更新并通过对象校验（2026-11-15） |
| build-your-own-x | https://github.com/codecrafters-io/build-your-own-x.git | master | `b2daa235` | 已快进更新并通过对象校验（2026-11-15） |
| caveman-full | https://github.com/JuliusBrussee/caveman.git | main | `b4ee71d5` | 已快进更新并通过对象校验（2026-11-15） |
| chrome-devtools-mcp | https://github.com/ChromeDevTools/chrome-devtools-mcp.git | main | `8ba2ac94` | 已在线核对，无需更新（2026-11-15） |
| claude-cookbooks | https://github.com/anthropics/claude-cookbooks.git | main | `ce8b2629` | 已快进更新并通过对象校验（2026-11-15） |
| claude-guides-full | https://github.com/vtroisWhite/andrej-karpathy-skills.git | main | `54a3028c` | 已在线核对，无需更新（2026-11-15） |
| claude-scholar | https://github.com/Galaxy-Dawn/claude-scholar.git | main | `d394fb59` | 已快进更新并通过对象校验（2026-11-15） |
| claude-skill-refactoring-ui | https://github.com/opkod-france/claude-skill-refactoring-ui.git | main | `80994d98` | 已在线核对，无需更新（2026-11-15） |
| claude-video | https://github.com/bradautomates/claude-video.git | main | `03ceb42f` | 已快进更新并通过对象校验（2026-11-15） |
| code-review-plugin | https://github.com/anthropics/claude-plugins-official.git | main | `b5b01ac4` | 已快进更新并通过对象校验（2026-11-15） |
| codetracer | https://github.com/metacraft-labs/codetracer.git | stable | `d29c0743` | 已快进更新并通过对象校验（2026-11-15） |
| codex-security | https://github.com/openai/codex-security.git | main | `173483d7` | 已在线核对，无需更新（2026-11-15） |
| context-mode | https://github.com/mksglu/context-mode.git | main | `d5709ae4` | 已快进更新并通过对象校验（2026-11-15） |
| crawl4ai | https://github.com/unclecode/crawl4ai.git | main | `cae74b20` | 已快进更新并通过对象校验（2026-11-15） |
| daizhigev20 | https://github.com/daizhige-org/daizhigev20.git | data | `012bc393` | 部分克隆资料库，保留按需下载布局（2026-11-15） |
| DeepTutor | https://github.com/HKUDS/DeepTutor.git | main | `60fb3bdf` | 已在线核对，无需更新（2026-11-15） |
| developer-portfolios | https://github.com/emmabostian/developer-portfolios.git | master | `d37beaff` | 已快进更新并通过对象校验（2026-11-15） |
| ECC | https://github.com/affaan-m/ECC.git | main | `d2ef2680` | 已快进更新并通过对象校验（2026-11-15） |
| effective-html | https://github.com/plannotator/effective-html.git | main | `5ce160a3` | 已快进更新并通过对象校验（2026-11-15） |
| ego-lite | https://github.com/citrolabs/ego-lite.git | main | `bacaece4` | 已快进更新并通过对象校验（2026-11-15） |
| emilkowalski-skills | https://github.com/emilkowalski/skills.git | main | `0f2e23b3` | 已快进更新并通过对象校验（2026-11-15） |
| freebie-radar | https://github.com/ZiChuanLan/freebie-radar.git | main | `4f89041a` | 已在线核对，无需更新（2026-11-15） |
| ghidra | https://github.com/NationalSecurityAgency/ghidra.git | master | `42db038f` | 已快进更新并通过对象校验（2026-11-15） |
| Ghost-Downloader-3 | https://github.com/XiaoYouChR/Ghost-Downloader-3.git | catalog/upstream-20261027 | `d6273793` | 已快进更新并通过对象校验（2026-11-15） |
| goose | https://github.com/aaif-goose/goose.git | main | `2365bc5e` | 已快进更新并通过对象校验（2026-11-15） |
| gortex | https://github.com/zzet/gortex.git | main | `6e1d8115` | 已快进更新并通过对象校验（2026-11-15） |
| graphify | https://github.com/Graphify-Labs/graphify.git | v8 | `d4a5b323` | 已快进更新并通过对象校验（2026-11-15） |
| hallmark | https://github.com/Nutlope/hallmark.git | main | `04977e15` | 已快进更新并通过对象校验（2026-11-15） |
| Hands-On-Large-Language-Models | https://github.com/HandsOnLLM/Hands-On-Large-Language-Models.git | main | `ea339081` | 已在线核对，无需更新（2026-11-15） |
| harness2 | https://github.com/google-research/harness2.git | main | `68688175` | 已在线核对，无需更新（2026-11-15） |
| headroom | https://github.com/headroomlabs-ai/headroom.git | main | `5023c84e` | 已快进更新并通过对象校验（2026-11-15） |
| Horizon | https://github.com/Thysrael/Horizon.git | main | `12d5fbde` | 已在线核对，无需更新（2026-11-15） |
| HowToLiveBetter | https://github.com/eternity4719/HowToLiveBetter.git | main | `36c78569` | 已快进更新并通过对象校验（2026-11-15） |
| human-writing | https://github.com/KKKKhazix/human-writing.git | main | `a4ed3735` | 已快进更新并通过对象校验（2026-11-15） |
| Humanizer-zh | https://github.com/op7418/Humanizer-zh.git | main | `f4518a8e` | 已快进更新并通过对象校验（2026-11-15） |
| hyperframes | https://github.com/heygen-com/hyperframes.git | main | `125a9446` | 已快进更新并通过对象校验（2026-11-15） |
| inspira-ui | https://github.com/rahulv-official/inspira-ui.git | main | `eec920b0` | 已快进更新并通过对象校验（2026-11-15） |
| Ix | https://github.com/ix-infrastructure/Ix.git | main | `9ac330ce` | 已快进更新并通过对象校验（2026-11-15） |
| kepano-obsidian | https://github.com/kepano/kepano-obsidian.git | main | `47369734` | 已在线核对，无需更新（2026-11-15） |
| kgka_Music_hl | https://github.com/umr-xiaomai/kgka_Music_hl.git | master | `60bd37dd` | 已快进更新并通过对象校验（2026-11-15） |
| khazix-skills | https://github.com/KKKKhazix/khazix-skills.git | main | `71cd50ff` | 已快进更新并通过对象校验（2026-11-15） |
| knowledge-work-plugins | https://github.com/anthropics/knowledge-work-plugins.git | main | `e91a1345` | 已快进更新并通过对象校验（2026-11-15） |
| last30days-skill | https://github.com/mvanhorn/last30days-skill.git | main | `5718ae78` | 已快进更新并通过对象校验（2026-11-15） |
| laya | https://github.com/NandhaKishorM/laya.git | main | `af8ada06` | 已快进更新并通过对象校验（2026-11-15） |
| LEANN | https://github.com/StarTrail-org/LEANN.git | main | `07796bd7` | 已快进更新并通过对象校验（2026-11-15） |
| liteparse | https://github.com/run-llama/liteparse.git | main | `89735b9f` | 已快进更新并通过对象校验（2026-11-15） |
| loopx | https://github.com/huangruiteng/loopx.git | main | `8ade78cd` | 已快进更新并通过对象校验（2026-11-15） |
| magenta-realtime | https://github.com/magenta/magenta-realtime.git | main | `694a545e` | 已在线核对，无需更新（2026-11-15） |
| manim | https://github.com/3b1b/manim.git | master | `fafa083a` | 已在线核对，无需更新（2026-11-15） |
| markdown-viewer-skills | https://github.com/markdown-viewer/skills.git | main | `2672b692` | 已快进更新并通过对象校验（2026-11-15） |
| mattpocock-skills | https://github.com/mattpocock/skills.git | main | `5863806d` | 已快进更新并通过对象校验（2026-11-15） |
| mergration | https://github.com/38tter/mergration.git | main | `0595ea02` | 已在线核对，无需更新（2026-11-15） |
| mermaid-erd-generator | https://github.com/nharsch/mermaid-erd-generator.git | main | `cbecf0ba` | 已在线核对，无需更新（2026-11-15） |
| minimax-skills | https://github.com/MiniMax-AI/skills.git | main | `02853d88` | 已快进更新并通过对象校验（2026-11-15） |
| minimind | https://github.com/jingyaogong/minimind.git | master | `233d00fa` | 已在线核对，无需更新（2026-11-15） |
| modern-web-guidance | https://github.com/GoogleChrome/modern-web-guidance.git | main | `4dd96834` | 已在线核对，无需更新（2026-11-15） |
| modern-web-guidance-src | https://github.com/GoogleChrome/modern-web-guidance-src.git | main | `5e5cd33a` | 已在线核对，无需更新（2026-11-15） |
| multi-style-image-generator | https://github.com/powerycy/multi-style-image-generator.git | main | `059267c7` | 已快进更新并通过对象校验（2026-11-15） |
| nanobrowser | https://github.com/nanobrowser/nanobrowser.git | master | `6c4c0802` | 已快进更新并通过对象校验（2026-11-15） |
| nature-skills | https://github.com/Yuan1z0825/nature-skills.git | main | `7bff1d05` | 已快进更新并通过对象校验（2026-11-15） |
| nginx-http-flv-module | https://github.com/winshining/nginx-http-flv-module.git | master | `b27d1469` | 已快进更新并通过对象校验（2026-11-15） |
| no-ai-slop | https://github.com/petergyang/no-ai-slop.git | main | `000650b1` | 已在线核对，无需更新（2026-11-15） |
| obsidian-skills | https://github.com/kepano/obsidian-skills.git | main | `39812773` | 已快进更新并通过对象校验（2026-11-15） |
| open-code-review | https://github.com/alibaba/open-code-review.git | main | `7e5ce06c` | 已在线核对，无需更新（2026-11-15） |
| open-design | https://github.com/nexu-io/open-design.git | main | `59e4f2ae` | 已快进更新并通过对象校验（2026-11-15） |
| open-source-games | https://github.com/bobeff/open-source-games.git | main | `3a9ab8fc` | 已在线核对，无需更新（2026-11-15） |
| openauth | https://github.com/anomalyco/openauth.git | master | `98dc5962` | 已在线核对，无需更新（2026-11-15） |
| OpenCLI | https://github.com/jackwener/OpenCLI.git | main | `9bc5f5ca` | 已快进更新并通过对象校验（2026-11-15） |
| OpenShell | https://github.com/NVIDIA/OpenShell.git | main | `2e5589b2` | 已快进更新并通过对象校验（2026-11-15） |
| openwork | https://github.com/different-ai/openwork.git | dev | `5631a771` | 已快进更新并通过对象校验（2026-11-15） |
| Paper2Any | https://github.com/OpenDCAI/Paper2Any | main | `b538531e` | 已在线核对，无需更新（2026-11-15） |
| PaperSpine | https://github.com/WUBING2023/PaperSpine.git | main | `1a79bf21` | 已快进更新并通过对象校验（2026-11-15） |
| patent-disclosure-skill | https://github.com/handsomestWei/patent-disclosure-skill.git | main | `91e3b43a` | 已快进更新并通过对象校验（2026-11-15） |
| pdf-inspector | https://github.com/firecrawl/pdf-inspector.git | main | `6bafce1b` | 已快进更新并通过对象校验（2026-11-15） |
| pi | https://github.com/earendil-works/pi.git | main | `04fd0897` | 已快进更新并通过对象校验（2026-11-15） |
| pipeforge | https://github.com/Sheraz-k/pipeforge.git | master | `ba84e9ff` | 已在线核对，无需更新（2026-11-15） |
| pisper | https://github.com/ling-kong-ran/pisper.git | release | `a86142bb` | 已快进更新并通过对象校验（2026-11-15） |
| playcaptcha | https://github.com/mortspace/playcaptcha.git | main | `0c12567b` | 已快进更新并通过对象校验（2026-11-15） |
| pocket-tts | https://github.com/kyutai-labs/pocket-tts.git | main | `9e8413eb` | 已快进更新并通过对象校验（2026-11-15） |
| prompts.chat | https://github.com/f/prompts.chat.git | main | `a8643cb2` | 已快进更新并通过对象校验（2026-11-15） |
| public-apis | https://github.com/public-apis/public-apis.git | master | `51bc64ab` | 已快进更新并通过对象校验（2026-11-15） |
| python-refactoring-skills | https://github.com/l-mb/python-refactoring-skills.git | main | `b0835710` | 已在线核对，无需更新（2026-11-15） |
| rare-ui | https://github.com/swamimalode07/rare-ui.git | main | `6c84e89f` | 已快进更新并通过对象校验（2026-11-15） |
| rea | https://github.com/morluto/rea.git | main | `65731d8b` | 已快进更新并通过对象校验（2026-11-15） |
| reverse-skill | https://github.com/zhaoxuya520/reverse-skill.git | main | `a5171e03` | 本地修改，保留原状（2026-11-15） |
| SafeGuard-Code-Profiler | https://github.com/hamed-kuheil/SafeGuard-Code-Profiler.git | main | `6d759c29` | 已在线核对，无需更新（2026-11-15） |
| scientific-agent-skills | https://github.com/K-Dense-AI/scientific-agent-skills.git | main | `1e5eeffb` | 部分克隆资料库，保留按需下载布局（2026-11-15） |
| scramble | https://github.com/dedoc/scramble.git | main | `c57a689e` | 已快进更新并通过对象校验（2026-11-15） |
| sepia | https://github.com/Nanako0129/sepia.git | main | `0eb11d6c` | 已快进更新并通过对象校验（2026-11-15） |
| SESA-Self-Evolving-Search-Agents | https://github.com/Zenghuang-Fu/SESA-Self-Evolving-Search-Agents.git | master | `74de5d77` | 已在线核对，无需更新（2026-11-15） |
| shadcn-ui | https://github.com/shadcn-ui/ui.git | main | `e62c9435` | 已快进更新并通过对象校验（2026-11-15） |
| skill-up | https://github.com/alibaba/skill-up.git | main | `1d624e03` | 已快进更新并通过对象校验（2026-11-15） |
| skills-compat-manager | https://github.com/hnaymyh123-henry/skills-compat-manager.git | master | `8be1357e` | 已在线核对，无需更新（2026-11-15） |
| skillspector | https://github.com/NVIDIA/skillspector.git | main | `c8161500` | 已快进更新并通过对象校验（2026-11-15） |
| skillsProject-AI-Log-Analyzer | https://github.com/sahanaydn/skillsProject-AI-Log-Analyzer.git | main | `3682eae2` | 已在线核对，无需更新（2026-11-15） |
| sklib | 本地仓库，无 origin | main | `730df725` | 本地修改，保留原状（2026-11-15） |
| SmeLLM | https://github.com/refactoring-assistant/SmeLLM.git | main | `8b3a5250` | 已在线核对，无需更新（2026-11-15） |
| stemdeck | https://github.com/stemdeckapp/stemdeck.git | main | `b9bd91ae` | 已快进更新并通过对象校验（2026-11-15） |
| stt | https://github.com/jianchang512/stt.git | main | `0df3151d` | 已在线核对，无需更新（2026-11-15） |
| superpowers-repo | https://github.com/obra/superpowers.git | main | `22f0b463` | 已快进更新并通过对象校验（2026-11-15） |
| supertonic | https://github.com/supertone-oss-archive/supertonic.git | main | `1e9799e9` | 已在线核对，无需更新（2026-11-15） |
| SupplyChainScanner | https://github.com/benjiamin911/SupplyChainScanner.git | main | `6e4dcc10` | 已在线核对，无需更新（2026-11-15） |
| tailcat | https://github.com/tailscale/tailcat.git | main | `e00cdde6` | 已在线核对，无需更新（2026-11-15） |
| taste-skill | https://github.com/Leonxlnx/taste-skill.git | main | `f6b76575` | 已快进更新并通过对象校验（2026-11-15） |
| terraform | https://github.com/hashicorp/terraform.git | main | `7b843103` | 已快进更新并通过对象校验（2026-11-15） |
| timesfm | https://github.com/google-research/timesfm.git | master | `918df02c` | 已快进更新并通过对象校验（2026-11-15） |
| transitions-dev | https://github.com/Jakubantalik/transitions.dev.git | main | `20d70c12` | 已快进更新并通过对象校验（2026-11-15） |
| ui-ux-pro-max-skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git | main | `d643997c` | 已快进更新并通过对象校验（2026-11-15） |
| up | https://github.com/byoungd/up.git | main | `9f83b250` | 已快进更新并通过对象校验（2026-11-15） |
| VibeVoice | https://github.com/microsoft/VibeVoice.git | main | `16fb2cb1` | 已在线核对，无需更新（2026-11-15） |
| VoxCPM | https://github.com/OpenBMB/VoxCPM.git | main | `300e4260` | 已在线核对，无需更新（2026-11-15） |
| vue-skills-full | https://github.com/vuejs-ai/skills.git | main | `198f0cd8` | 已快进更新并通过对象校验（2026-11-15） |
| vue-tui | https://github.com/Simon-He95/vue-tui.git | main | `76dff754` | 已快进更新并通过对象校验（2026-11-15） |
| web-access | https://github.com/eze-is/web-access.git | main | `d173a759` | 已快进更新并通过对象校验（2026-11-15） |
| WebSecurityScanner | https://github.com/Defensive-Alliance/WebSecurityScanner.git | main | `60a02b48` | 已在线核对，无需更新（2026-11-15） |
| z-skills | https://github.com/tjxj/z-skills.git | main | `2b52120b` | 已快进更新并通过对象校验（2026-11-15） |
| zvec-grep | https://github.com/zvec-ai/zvec-grep.git | main | `38cb1af6` | 已快进更新并通过对象校验（2026-11-15） |

## 本聚合仓库实际保存的本地内容

- 根目录 README 与变更记录，以及 `docs/` 下的索引、维护说明和历史台账。
- `multi-search-engine/`：上游单文件 Skill 快照及本地审计说明。
- `zhihu-cli-skill/`：本地维护的知乎 CLI Skill 包，不包含账号凭据。

PDF、ZIP、`.env`、缓存、依赖、构建产物、嵌套 `.git` 和第三方仓库工作树均由根 `.gitignore` 默认排除。
