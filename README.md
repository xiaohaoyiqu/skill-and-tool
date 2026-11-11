# Skill and Tool

这个仓库用来存放和整理 Skill、工具、研究资料及其版本记录。内容按来源保留，方便以后查找、更新和复核。

第三方项目主要保存资料与来源记录，使用条件以原项目说明为准。自制的本地 Skill 和项目资料检索工具 [SKLIB](sklib/README.md) 也在本仓库中保存源码。

转发给别人可以使用 [AI Skills 和工具分享清单](docs/SHARE_GUIDE.md)，按用途介绍 131 个项目并附来源链接；[HTML 分享版](docs/SHARE_GUIDE.html) 可作为单个文件发送，用浏览器打开。

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
- 已存在的项目先检查上游更新，再刷新索引。
- 单独保存的文件附带来源说明。
- 根目录保留 README 和 CHANGELOG；索引与维护文档放入 `docs/`，停止维护的旧版资料放入 `docs/archive/`。
- 文档中的本地项目路径与命令默认以 `E:\aimodel` 为工作目录；可点击链接按所在文档使用相对路径。
- 第三方内容沿用各自的许可证和使用条件。

统计数字对应各次扫描结果。上游项目继续变化时，以来源仓库为准。

## 2026-11-11 项目收录

本批登记 StemDeck、openvid、OpenAuth、laya、Ix、Hands-On Large Language Models、HowToLiveBetter 和 up 共 8 个来源。除 openvid 的源码本身约 181.96 MB、超限仅登记外，其余 7 个项目均已浅克隆到根目录，含 Git 的实际大小都低于 100 MB。Ix 与 HowToLiveBetter 各含 1 个逻辑 Skill；许可证、运行条件和提交见[本批台账](docs/GITHUB_REPOS.md#2026-11-11-音视频认证代码检索与学习资料)。分享清单已补至 131 个不同来源；未安装依赖、模型或全局 Skill。

## 2026-11-09 项目核对

已有 `skill-up/` 已快进更新，新增 `OpenShell/` 与 `context-mode/` 源码浅克隆，含 Git 分别约 13.00、55.65、37.44 MB。`huashu-art-motion` 完整浅克隆展开前核算约 148.62 MB，超出本轮 100 MB 上限，只登记来源，临时副本已清理。未安装依赖或修改全局配置；大小口径、用途及运行条件见[下载台账](docs/GITHUB_REPOS.md#2026-11-09-skill-评测艺术动画与-agent-工具)。另已确认 `arjun988/blender-skills` 在 11 月 2 日登记过，当前仍未克隆或安装。

## Agent Reach 当前记录

2026-11-08 下载官方 `v1.6.1` 独立源码快照，提交 `7a38047acf26a729cbb27851e3cb81639da86b29`；旧 `Agent-Reach/` 的 v1.5.0 与本地状态保留。已用现有 Python 环境核对版本及 14 个渠道的动作声明，没有安装依赖、全局 CLI 或 Skill，没有执行 setup、登录或浏览器会话导入。它可补充公开网页和平台资料读取，未提供 SauceNAO/IQDB 上传图片反查动作；源码存在与渠道可联网使用须分别核验。下载、使用边界和复核方法见[台账](docs/GITHUB_REPOS.md#2026-11-08-agent-reach-v161源码快照)。

## 运行时升级与可观测性资料

本仓库当前没有安装 OpenTelemetry、HBase、ClickHouse 或 Java Agent 运行时。涉及 Java 运行时升级、服务可观测性或新增存储时，先用 `mattpocock-skills` 的架构审查、`agent-skills` 的性能与安全指导、`superpowers-repo` 的验证流程完成设计和回归；`chrome-devtools-mcp` 只用于浏览器与网络侧证据，`gortex` 与 Graphify 仅在明确批准建立索引或守护进程后使用。工具源码存在不代表已获部署授权。
