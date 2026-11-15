# Skill and Tool

这个仓库用来存放和整理 Skill、工具、研究资料及其版本记录。内容按来源保留，方便以后查找、更新和复核。

第三方项目主要保存资料与来源记录，使用条件以原项目说明为准。自制的本地 Skill 和项目资料检索工具 [SKLIB](sklib/README.md) 也在本仓库中保存源码。

转发给别人可以使用 [AI Skills 和工具分享清单](docs/SHARE_GUIDE.md)，按用途介绍 143 个项目与论文来源并附链接；[HTML 分享版](docs/SHARE_GUIDE.html) 可作为单个文件发送，用浏览器打开。

## 2026-11-15 全目录同步

在线检查 134 个可见一级仓库：已在线核对，无需更新 40 个；本地修改，保留原状 2 个；无 upstream，保留原状 1 个；部分克隆资料库，保留按需下载布局 2 个；已快进更新并通过对象校验 89 个。网络失败已重试处理，完整版本与跳过原因见[全目录台账](docs/GITHUB_REPOS.md#2026-11-15-全目录同步)及[最终核验 JSON](scripts/repository-sync-20261115-final.json)。本轮只同步源码与记录，未安装依赖或全局配置。Horizon 与 freebie-radar 此前已快进至 `12d5fbde`、`4f89041a`，来源分享清单仍为 143 项。


## 2026-11-15 网络工具、安全审查与 Chrome 项目追加核验

新增 `tailcat/`、`codex-security/`、`modern-web-guidance-src/` 三个源码浅克隆，含 Git 分别为 1.14、33.62、178.77 MB；更新已有 `open-code-review/`、`chrome-devtools-mcp/`，分别为 25.59、23.59 MB。用户将未来默认下载上限提高至 **120 MB**，modern-web-guidance-src 本次按明确下载授权作为大小例外保留。五个仓库工作树干净并通过对象校验；未安装依赖或全局 Skill/MCP。见[本批台账](docs/GITHUB_REPOS.md#2026-11-15-网络工具安全审查与-chrome-项目追加核验)及[核验 JSON](scripts/repository-review-20261115-tailcat.json)。


## 从哪里开始

| 文件 | 内容 |
|------|------|
| [REPOSITORIES.md](docs/REPOSITORIES.md) | 一级 Git 仓库的来源、分支、提交和同步状态 |
| [REPOSITORY_MANAGEMENT.md](docs/REPOSITORY_MANAGEMENT.md) | 批量拉取、目录整理、检索与知识图谱工具说明 |
| [SKLIB](sklib/README.md) | 自制的本地资料检索工具，提供 CLI、stdio MCP 和网页界面 |
| [SKILLS_INDEX.md](docs/SKILLS_INDEX.md) | Skill 数量、分类和用途索引 |
| [BROWSER_AUTOMATION_COMPARISON.md](docs/BROWSER_AUTOMATION_COMPARISON.md) | 浏览器控制、网页快照与像素截图理解工具对比 |
| [GITHUB_REPOS.md](docs/GITHUB_REPOS.md) | 各批次下载、更新和检查记录 |
| [GITHUB_STAR_LIST.md](docs/GITHUB_STAR_LIST.md) | GitHub 手动收藏链接，数量按各次历史快照参考 |
| [CHANGELOG.md](CHANGELOG.md) | 这个存放库的变更记录 |

仓库来源与版本以 `docs/REPOSITORIES.md` 为入口，Skill 分类与用途以 `docs/SKILLS_INDEX.md` 为入口。各文档中的数量和状态对应其标注的核验日期。

## 历史资料

| 文件 | 内容 |
|------|------|
| [README_ARCHIVE.md](docs/archive/README_ARCHIVE.md) | 早期 README、分类和整理记录 |
| [SKILLS_INSTALLED.md](docs/archive/SKILLS_INSTALLED.md) | 历史安装与配置记录 |
| [SKILLS_UNIFIED.md](docs/archive/SKILLS_UNIFIED.md) | 旧版分类汇总和使用说明 |
| [LIVE_STREAMING.md](docs/archive/LIVE_STREAMING.md) | 旧版资源总览及直播流媒体笔记 |

历史资料保留当时的统计、目录结构和命令，当前目录状态请从上方索引查起。

## 仓库里保存的内容

| 目录 | 说明 |
|------|------|
| [docs](docs/) | 当前索引、下载台账和维护说明；旧版文档集中在 `docs/archive/` |
| [scripts](scripts/) | 仓库同步脚本、批次核验 JSON 和本地维护脚本 |
| [sklib](sklib/) | 自制检索工具的 Python 源码、网页资源、测试与说明；不包含本机环境、资料索引或模型 |
| [multi-search-engine](multi-search-engine/) | Multi Search Engine 的单文件 Skill 快照和来源说明 |
| [zhihu-cli-skill](zhihu-cli-skill/) | 知乎 CLI Skill 及配套脚本和参考文档 |
| [Agent-Reach-v1.6.1](Agent-Reach-v1.6.1/) | Agent Reach 官方 v1.6.1 源码与 Skill；旧 `Agent-Reach/` 保留，未安装运行依赖 |

第三方 Git 项目主要记录在 [REPOSITORIES.md](docs/REPOSITORIES.md)。表中保留上游地址和扫描时的提交号，需要完整内容时可以按记录重新克隆。

## 收录规则

- 记录来源、用途和当前提交。
- 自 2026-11-15 本批追加指令起，单项目默认下载上限提高为 **120 MB（120,000,000 字节）**，按源码与 `.git` 文件长度合计；下载当前分支的浅克隆，超限仅登记，用户明确指定下载的项目另记授权。
- 用户随后授权已有仓库超限时直接更新；已有项目同步可使用 `--allow-over-limit`，新增项目仍按上述 120 MB 默认上限处理。
- 已存在的项目先检查上游更新，再刷新索引。
- 单独保存的文件附带来源说明。
- 根目录保留 README 和 CHANGELOG；索引与维护文档放入 `docs/`，停止维护的旧版资料放入 `docs/archive/`。
- 文档中的本地项目路径与命令默认以 `E:\aimodel` 为工作目录；可点击链接按所在文档使用相对路径。
- 第三方内容沿用各自的许可证和使用条件。

统计数字对应各次扫描结果。上游项目继续变化时，以来源仓库为准。

## 2026-11-15 提示词与信息雷达

2026-11-15 新增 `prompts.chat/`、`freebie-radar/`、`Horizon/` 三个源码浅克隆，含 Git 分别为 250.65、3.92、15.60 MB；prompts.chat 按用户指令豁免本批大小限制。`modern-web-guidance-src` 源码已达 101.45 MB，超限只登记。两个 11 月 13 日已有项目在线核对仍为最新。五个本地仓库均工作树干净并通过对象校验；未安装依赖或全局 Skill。见[下载台账](docs/GITHUB_REPOS.md#2026-11-15-提示词社区资源雷达与-modern-web-guidance-源码)及[核验 JSON](scripts/repository-review-20261115.json)。

## 2026-11-13 语音合成与现代 Web Skills

新增 `VoxCPM/` 和 `modern-web-guidance/` 两个源码浅克隆，含 Git 分别为 10.14 MB、3.16 MB，均低于 100 MB。VoxCPM 当前主线为 VoxCPM2 多语言语音合成、音色设计与声音克隆；modern-web-guidance 保存现代 Web 开发和 Chrome 扩展开发两个 Skill 入口。来源、许可、运行条件和校验见[本批台账](docs/GITHUB_REPOS.md#2026-11-13-voxcpm-与-modern-web-guidance)。分享清单增加至 137 项；未安装依赖、模型、全局 Skill 或插件。

## 2026-11-12 Agent 自改进、学习平台与小模型训练

新增 `harness2/`、`minimind/` 和 `DeepTutor/` 三个源码浅克隆，含 Git 分别约 15.30 MB、23.36 MB、106.70 MB。DeepTutor 初次因超过 100 MB 限额跳过，随后按用户明确授权豁免大小限制并完成克隆，6 个 Skill 入口随源码保存；其他项目仍沿用原限额。用户提供的 `arXiv:2610.13735` 是 Orthros 注意力研究，Harness² 对应 `2610.14224`；两篇论文分别登记并保存原版 PDF。用途、运行条件、许可及校验见[本批台账](docs/GITHUB_REPOS.md#2026-11-12-harness²orthrosdeeptutor-与-minimind)，未安装依赖、模型或全局 Skill。

## 2026-11-11 项目收录

本批登记 StemDeck、openvid、OpenAuth、laya、Ix、Hands-On Large Language Models、HowToLiveBetter 和 up 共 8 个来源。除 openvid 的源码本身约 181.96 MB、超限仅登记外，其余 7 个项目均已浅克隆到根目录，含 Git 的实际大小都低于 100 MB。Ix 与 HowToLiveBetter 各含 1 个逻辑 Skill；许可证、运行条件和提交见[本批台账](docs/GITHUB_REPOS.md#2026-11-11-音视频认证代码检索与学习资料)。分享清单已补至 131 个不同来源；未安装依赖、模型或全局 Skill。

## 2026-11-09 项目核对

已有 `skill-up/` 已快进更新，新增 `OpenShell/` 与 `context-mode/` 源码浅克隆，含 Git 分别约 13.00、55.65、37.44 MB。`huashu-art-motion` 完整浅克隆展开前核算约 148.62 MB，超出本轮 100 MB 上限，只登记来源，临时副本已清理。未安装依赖或修改全局配置；大小口径、用途及运行条件见[下载台账](docs/GITHUB_REPOS.md#2026-11-09-skill-评测艺术动画与-agent-工具)。另已确认 `arjun988/blender-skills` 在 11 月 2 日登记过，当前仍未克隆或安装。

## Agent Reach 当前记录

2026-11-08 下载官方 `v1.6.1` 独立源码快照，提交 `7a38047acf26a729cbb27851e3cb81639da86b29`；旧 `Agent-Reach/` 的 v1.5.0 与本地状态保留。已用现有 Python 环境核对版本及 14 个渠道的动作声明，没有安装依赖、全局 CLI 或 Skill，没有执行 setup、登录或浏览器会话导入。它可补充公开网页和平台资料读取，未提供 SauceNAO/IQDB 上传图片反查动作；源码存在与渠道可联网使用须分别核验。下载、使用边界和复核方法见[台账](docs/GITHUB_REPOS.md#2026-11-08-agent-reach-v161源码快照)。

## 运行时升级与可观测性资料

本仓库当前没有安装 OpenTelemetry、HBase、ClickHouse 或 Java Agent 运行时。涉及 Java 运行时升级、服务可观测性或新增存储时，先用 `mattpocock-skills` 的架构审查、`agent-skills` 的性能与安全指导、`superpowers-repo` 的验证流程完成设计和回归；`chrome-devtools-mcp` 只用于浏览器与网络侧证据，`gortex` 与 Graphify 仅在明确批准建立索引或守护进程后使用。工具源码存在不代表已获部署授权。
