# GitHub 仓库下载与配置台账

**最后整理**: 2026-11-22
**目录**: E:\aimodel
**定位**: GitHub 下载与配置历史台账；当前 skill 更新状态以 [SKILLS_INDEX.md](SKILLS_INDEX.md) 为准
**状态**: 只记录克隆和配置，不自动安装依赖、不写入全局 Codex skills
**Star 手动清单**: [GITHUB_STAR_LIST.md](GITHUB_STAR_LIST.md)

---

## 2026-11-22 应用平台、模型运行、网页采集与游戏 Skills

| 项目 | 本次处理与版本 | 大小（十进制） | 用途与许可 |
|------|------|------|------|
| [Dify](https://github.com/langgenius/dify) | 超限仅登记，main `8b6fbfb0` | 153.43 MB（153,428,103 字节），仅源码 | AI 应用开发平台，组织 Agent 工作流、RAG、模型与工具接入。采用附多租户及前端品牌条件的 Dify License；当前源码超限，仅登记链接。 |
| [Open WebUI](https://github.com/open-webui/open-webui) | 新增源码浅克隆 `open-webui/`，main `0666e59d` | 77.83 MB（77,833,771 字节），含 Git | 可自托管的 AI 对话界面，支持 Ollama 与兼容 OpenAI 的 API，并提供知识库与扩展功能。采用含品牌条件的 Open WebUI License，历史代码许可另见 LICENSE_HISTORY；已保存源码。 |
| [Ollama](https://github.com/ollama/ollama) | 新增源码浅克隆 `ollama/`，main `2bd4d6aa` | 80.00 MB（80,002,636 字节），含 Git | 运行和管理语言模型的工具，提供命令行与 API，可与对话界面或应用连接。源码 MIT，模型权重与第三方组件分别按其许可；仅保存源码，未下载模型或启动服务。 |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | 新增源码浅克隆 `Scrapling/`，main `2998c9eb` | 15.03 MB（15,029,454 字节），含 Git | Python 网页采集框架，整合 HTTP 请求、浏览器渲染、页面解析、并发爬取与数据导出，提供 MCP 和官方 Agent Skill。Python 3.10+，BSD-3-Clause；已保存源码及 1 个 Skill，运行依赖需另备。 |
| [public-apis](https://github.com/public-apis/public-apis) | 快进更新 `public-apis/`，master `867085cc` | 18.15 MB（18,151,366 字节），含 Git | 公共 API 与 MCP 服务的分类导航；MIT，外链服务各自核对条件。 |
| [Blender Agent Skills（EL4CTEO）](https://github.com/EL4CTEO/blender-skills) | 快进更新 `blender-skills/`，main `1a1cc6c4` | 13.02 MB（13,016,637 字节），含 Git | 28 个 Blender 制作 Skill；MIT。本次从 `9e7e04a6` 快进 1 个提交至 1.3.3，修复压力测试发现的边界问题。 |
| [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | 在线核对，无需更新 `awesome-gamedev-agent-skills/`，main `c6ca6c41` | 7.84 MB（7,836,642 字节），含 Git | 79 个游戏开发 Skill 加 1 个路由入口，覆盖 12 种引擎；Apache-2.0。按用户明确下载授权保留现有副本。 |

本轮 7 个来源中，新增 3 个源码浅克隆，已有 public-apis、Blender Skills 快进更新，已有游戏开发 Skills 在线核对仍为最新，Dify 超限仅登记。public-apis 从 `51bc64ab` 快进 188 个提交至 `867085cc`；不重复克隆或重复计算来源。

沿用新增项目源码与 Git 合计严格小于 **120,000,000 字节**的规则。Dify 固定提交的完整 API 文件树未截断，源码已占 **153,428,103 字节**，未下载 Git 或建立 `dify/`。其远端有 6 个 SKILL.md：4 个项目开发入口、1 个端到端测试夹具及 1 个 difyctl 入口；不作为已安装 Skill 计数。Open WebUI、Ollama 与 public-apis 当前文件树均无 SKILL.md。Scrapling 的正式入口为 `agent-skill/Scrapling-Skill/SKILL.md`，版本 0.5.1。

六个保留的本地仓库均为完整当前工作树，HEAD 与本次固定并抓取的默认分支提交一致，工作树干净，通过 `git fsck --no-reflogs`。新仓库 Git 树对象与下载前固定提交的完整 API 树一致；游戏仓库此前已下载，本次核对后保留，不需重新克隆。各仓库大小均低于上限，本批无需大小例外。Blender 的对象校验含一条 dangling tag 提示，退出码为 0。

仅保存源码与记录，未安装依赖、模型、浏览器、游戏引擎或全局 Skill/MCP，未运行上游安装器、启动服务或复现上游功能。Dify 的多租户与前端品牌条款见[固定提交 LICENSE](https://github.com/langgenius/dify/blob/8b6fbfb010ff77b6d2d9e57c4fdd3d8225f3e6ca/LICENSE)，Open WebUI 的品牌条款见[固定提交 LICENSE](https://github.com/open-webui/open-webui/blob/0666e59d26a4d056e0bacee41742486badd71cf8/LICENSE)；不能一概写为标准 Apache-2.0 或 MIT。

分享清单由 156 增至 **160 个不同来源**。新增来源是 Dify、Open WebUI、Ollama 和 Scrapling；另外三个是已收录来源。见[核验 JSON](../scripts/repository-review-20261122.json)、[下载前 API 汇总](../scripts/repository-api-20261122.json)和同目录 `repository-tree-20261122-*.json` 完整树记录。

## 2026-11-21 游戏开发 Skills 与逆向资料核验

| 项目 | 本次处理与版本 | 大小与内容 |
|------|------|------|
| [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | 新增同名目录源码浅克隆，main `c6ca6c41` | 实测含 Git **7.84 MB（7,836,642 字节）**，低于 120 MB 默认上限；79 个游戏开发 Skill 和 1 个路由入口，Apache-2.0，另见 NOTICE。 |
| [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | 已有仓库，按常规规则保留本地修改，跳过更新，main `a5171e03` | 实测含 Git **12.22 MB（12,219,666 字节）**，本地存在 3 个未提交修改；84 个 SKILL.md 文件为当前物理文件数，未据此重算逻辑 Skill 总数。MIT。 |

游戏开发项目按用户“这个可以直接下载”授权保存完整当前工作树，实际无需大小例外。下载经历连接中断，重试完成后清理了本批遗留的锁文件和临时 pack，HEAD 与本次抓取的 `origin/main` 一致，工作树干净，通过 `git fsck --no-reflogs`。覆盖 Godot、Unity、Unreal、Ebitengine、Phaser、PixiJS、three.js、Bevy、pygame、LÖVE、Defold 和 Roblox；从 `router/SKILL.md` 分派到引擎、玩法、制作与发布任务入口。引擎兼容性和上游评测结果未在本机复现。

`reverse-skill/` 的本地修改位于 `skills/pentest-tools/src-hunter/references/payloader/by-category/web/文件漏洞.md`、同目录 `请求走私.md` 和 `skills/pentest-tools/src-hunter/references/playbooks/http-smuggling.md`。本次未执行 fetch、stash、reset 或合并；HEAD 与工作树内容保持原样，通过对象校验，核验 JSON 保存三个文件的 SHA-256。缓存的 `origin/main` 为 `7e2097fd`，并非本次在线核对的远端状态；不标记为已同步。

分享清单由 155 增至 **156 个不同来源**，reverse-skill 为既有来源，不重复计数。未安装依赖、游戏引擎、全局 Skill/MCP 或运行上游安装器。完整提交、大小、Skill 路径及保护状态见[核验 JSON](../scripts/repository-review-20261121.json)。

## 2026-11-20 十个 GitHub 仓库续拉

本批 11 条输入去重后为 10 个来源。已有仓库按授权保留原目录并快进更新，新增仓库沿用源码与 Git 合计严格小于 120 MB 的规则。

| 项目 | 处理与版本 | 大小 | 用途与许可 |
|------|------|------|------|
| [PixelFX](https://github.com/patch-gg/pixelfx) | 新增 `pixelfx/` 浅克隆，main `5294518c` | 27.05 MB（27,051,846 字节），实测含 Git | 可由代码生成的像素动效库和可浏览的示例，提供精灵图导出及一个用于制作动效的 Skill。代码采用 MIT，画廊字体许可见 NOTICE。 |
| [Humanizer](https://github.com/blader/humanizer) | 新增 `humanizer/` 浅克隆，main `a32f2440` | 0.13 MB（134,887 字节），实测含 Git | 文本润色 Skill，检查常见的生成式写作模式，并尽量保留原作者的语气和意思。MIT。 |
| [Plannotator](https://github.com/backnotprop/plannotator) | 超限，仅登记，main `f61d44dc` | 128.24 MB（128,242,593 字节），仅源码 | 用于批注 Agent 的计划、规格和差异，审查代码并把反馈发回 Agent。Apache-2.0 或 MIT。 |
| [Free Claude Code](https://github.com/Alishahryar1/free-claude-code) | 快进更新 `free-claude/free-claude-code/`，由 `d3a3b37e` 至 main `62db82ec` | 30.38 MB（30,379,245 字节），实测含 Git | 为多种编码 Agent 接入模型后端的社区项目，提供 API 代理和会话管理。AGPL-3.0-only。 |
| [daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) | 超限，仅登记，main `92f0209e` | 167.16 MB（167,158,646 字节），检出前核算含 Git | 聚合多个市场的行情、新闻和模型分析，提供自选股看板、定时任务及推送。MIT。 |
| [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) | 新增 `elephant-goldfish-model/` 浅克隆，main `70406c4d` | 5.34 MB（5,337,864 字节），实测含 Git | 辅助软件规格编写与审查的 Agent 插件，起草者保留项目上下文，审查者独立阅读草稿与引用材料。Apache-2.0，附 8 个 Skill。 |
| [Anthropic Skills](https://github.com/anthropics/skills) | 快进更新 `anthropic-skills/`，由 `1780c5e5` 至 main `e4bb5d96` | 17.89 MB（17,885,870 字节），实测含 Git | Anthropic 的官方 Skill 示例，涵盖文档、设计与应用开发，提供 19 个 Skill 和 1 个模板。各目录许可见上游说明。 |
| [Univer](https://github.com/dream-num/univer) | 超限，仅登记，dev `0b7a1243` | 146.46 MB（146,459,824 字节），检出前核算含 Git | 可嵌入应用的办公 SDK。开源核心涵盖电子表格、文档和无界面处理，服务端和部分扩展另有许可。开源仓库采用 Apache-2.0。 |
| [modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | 快进更新 `modern-web-guidance-src/`，由 `5e5cd33a` 至 main `998f5114` | 181.32 MB（181,317,867 字节），实测含 Git | Modern Web Guidance 的指南编写、构建、校准与评测源码。代码 Apache-2.0，guides/ 文档 CC BY 4.0，附 13 个维护 Skill 与 2 个分发源入口。 |
| [Astryx](https://github.com/meta/astryx) | 超限，仅登记，main `16fde59f` | 396.78 MB（396,776,352 字节），仅源码 | Meta 的可定制设计系统，提供组件源码、主题和面向 Agent 的 Skill。MIT。 |

六个本地仓库工作树干净，HEAD 与本次抓取的上游一致，均通过 `git fsck --no-reflogs`。`modern-web-guidance-src/` 按既有仓库超限更新授权保留。Plannotator 与 Astryx 的固定提交源码已超限，直接登记。daily_stock_analysis 与 Univer 的临时 Git 副本已清理，二者的大小为检出前的完整源码与 Git 文件长度之和。

本批保存源码与记录，未安装依赖、模型或全局 Skill/MCP。完整提交、Git 对象校验、大小和 Skill 路径见[核验 JSON](../scripts/repository-review-20261120.json)。

## 2026-11-19 三个仓库续拉

| 项目 | 本次处理与版本 | 实际含 Git（十进制） |
|------|------|------:|
| [Blender Agent Skills](https://github.com/EL4CTEO/blender-skills) | `blender-skills/` 的 main 从 `b1b21dfb` 快进 2 个提交至 `9e7e04a6`，包含上游 1.3.2 的蒙皮网格检查修复 | 12.96 MB（12,957,191 字节） |
| [Craft Anything](https://github.com/storytold/craft-anything) | `craft-anything/` 的 main 从 `5979f9b1` 快进 302 个提交至 `df227090` | 35.91 MB（35,914,015 字节） |
| [fanqiang](https://github.com/bannedbook/fanqiang) | 已登记的来源首次保存本地源码，`fanqiang/` 的 master `3f5bb7ae` | 180.31 MB（180,313,289 字节） |

`fanqiang` 的完整当前工作树占 97,958,388 字节，`.git` 占 82,354,901 字节。此次按用户再次点名拉取处理为单项目大小例外，默认上限仍为 120 MB。Git 文件树和 11 月 17 日保存的同一提交文件树逐项一致。

三个浅克隆的工作树均干净，HEAD 与本次核对的上游一致，均通过 `git fsck --no-reflogs`。Blender 的校验有一条 dangling tag 提示，退出码为 0。Blender 随源码保存 28 个正式 Skill 入口。Craft Anything 的安装器内嵌一个 Skill 模板，本次只同步源码。分享清单共 147 个来源。见[核验 JSON](../scripts/repository-review-20261119.json)。

## 2026-11-18 Moli 无头浏览器

| 项目 | 本次处理与版本 | 大小 | 用途与许可 |
|------|------|------|------|
| [Moli](https://github.com/lexmount/moli) | 新增 `moli/` 浅克隆，main `6b8baf41` | 含 Git **151.89 MB**（151,888,069 字节） | 面向 AI Agent 的 Rust 无头浏览器，可提取网页内容、搜索网页和执行浏览器自动化。提供 CLI、CDP、WebDriver Classic 和 WebDriver BiDi，附 3 个 Skill。默认 MIT OR Apache-2.0，第三方组件按各自许可。 |

源码占 124.04 MB，`.git` 占 27.85 MB。合计超过 120 MB 默认上限，按用户明确的直接下载指令保留此项目。HEAD 和本次核对的远端 main 一致，工作树干净，通过 `git fsck --no-reflogs`。

`skills/` 下的 `moli-webfetch`、`moli-websearch` 与 `moli-cdp-server` 分别用于网页提取、网页搜索与 CDP 自动化。三个入口随源码保存，使用时需要 Moli 可执行文件。上游文档列出 Linux、macOS 和 Windows。分享清单增至 **147 个来源**。完整提交与路径见[核验 JSON](../scripts/repository-review-20261118-moli.json)和[固定提交的 README](https://github.com/lexmount/moli/blob/6b8baf41e0c6a2d08c667a6ea9beec5055884452/README.md)。

## 2026-11-17 Blender Skills、Craft Anything 与网络资料

继续收录用户指定的三个来源，沿用新增项目 **120,000,000 字节（120 MB，十进制）**默认上限，按完整当前文件与 `.git` 文件长度合计，严格小于上限才保留。先核对默认分支固定提交的完整 API 文件树（均未截断），再浅克隆到临时目录，比较文件树并核算检出后大小；不删除资源或稀疏检出来规避限额。

| 项目 | 本次处理与版本 | 大小（十进制 MB） | 用途与许可 |
|------|------|------|------|
| [Blender Agent Skills](https://github.com/EL4CTEO/blender-skills) | 新增 `blender-skills/` 浅克隆，main `b1b21dfb` | 实际含 Git **12.94 MB**（12,942,239 字节） | 28 个 Blender 制作 Skill，覆盖建模、UV、材质、烘焙、绑定、动画、服装、毛发、环境、模拟、渲染、导出与资产检查；MIT。 |
| [Craft Anything](https://github.com/storytold/craft-anything) | 新增 `craft-anything/` 浅克隆，main `5979f9b1` | 实际含 Git **31.77 MB**（31,769,446 字节） | Rust 编写的软件检查、分析与重建引擎，提供桌面界面、CLI、MCP 及研究→构建→比对流程；早期 alpha。代码 MIT OR Apache-2.0；字体、图标与品牌素材另见 ATTRIBUTION.md。 |
| [fanqiang](https://github.com/bannedbook/fanqiang) | master `3f5bb7ae`；超限仅登记链接，临时副本已清理 | 检出前核算 **180.05 MB**（180,047,021 字节） | 跨平台代理与网络访问工具的教程、链接及部分应用源码，包括 FQNews。根目录未见统一许可证，不能将子项目许可推广为整库许可；各子目录与外链分别核对。 |

**同名来源区分**：此次 `EL4CTEO/blender-skills` 为新来源，保存到此前不存在的 `E:\aimodel\blender-skills`。2026-11-02 和 11 月 9 日记录的 `arjun988/blender-skills` 仍为另一个仅登记链接的项目；保留其原日期和状态，不替换来源或重复计算为同一仓库。

Blender 仓库 `skills/` 下实存 **28 个 SKILL.md**，均为正式入口；以 `skills/blender-core/SKILL.md` 为任务路由入口，完整路径见核验 JSON。上游要求 Blender **5.2 LTS+**，声称在 5.3 验证；此处仅记录上游运行要求，没有运行 Blender 或复现效果。MCP 为可选执行方式，也可用后台 Blender；未运行会写入用户全局目录的安装器。

Craft Anything 没有 SKILL.md，作为工具收录。固定提交 Cargo.toml 声明 Rust **1.97+**、edition 2024；实际重建另需登录的编码 Agent，上游优先支持 Claude Code，并说明 Codex 适配器尚未在真实安装上验证。深度分析可选接入 Ghidra。保存源码不代表已安装应用、MCP 或构建依赖。代码双许可证与非开源应用图标、品牌素材须分别看待，详见其 [ATTRIBUTION.md](https://github.com/storytold/craft-anything/blob/5979f9b13f16dcf1df3c7ae7f8e7735f452866f2/ATTRIBUTION.md)。

**fanqiang 大小核算**：完整当前文件树为 **97,937,924 字节**，浅克隆 Git 数据为 **82,109,097 字节**，检出前合计 **180,047,021 字节**，已超过 120 MB。未展开工作树，自动清理本批专用临时目录，最终不存在 `E:\aimodel\fanqiang`。没有下载额外发行包或运行库内应用；不因 API 的历史仓库大小字段直接判定当前工作树大小。

两个保留仓库均为完整当前工作树的浅克隆，工作树干净、HEAD 与本次固定的远端默认分支提交一致，通过 `git fsck --no-reflogs`。Blender 的校验输出只有一个 dangling tag 提示，退出码为 0，无对象损坏。三个来源均无子模块；跳过 LFS 实体，不安装依赖、全局 Skill/MCP 或启动服务。只增加两个本地 Git 目录，未重扫其他项目或重算历史 Skill 总数。分享清单新增三个不同来源，由 **143 项增至 146 项**。

完整提交、来源、大小与校验见[本批核验 JSON](../scripts/repository-review-20261117.json)及[下载前 API 汇总](../scripts/repository-api-20261117.json)；三个固定提交的完整文件树分别保存于 [Blender](../scripts/repository-tree-20261117-blender-skills.json)、[Craft Anything](../scripts/repository-tree-20261117-craft-anything.json)、[fanqiang](../scripts/repository-tree-20261117-fanqiang.json)。

## 2026-11-15 全目录同步

按用户“查看本地目录有什么更新，进行更新，更新好后进行提交”的指令，对 **134 个可见一级 Git 仓库**执行在线同步检查。隐藏聚合仓库用于提交台账，不混入第三方批量更新；没有递归更新子模块或其他嵌套仓库。

结果：**已在线核对，无需更新 40 个；本地修改，保留原状 2 个；无 upstream，保留原状 1 个；部分克隆资料库，保留按需下载布局 2 个；已快进更新并通过对象校验 89 个**。网络 TLS 中断和超时已按独立重试报告处理，最终无未处理的同步失败。已更新仓库工作树干净、与抓取的 upstream 一致并通过对象校验；所有仓库最终 HEAD 均已复核，跳过项目保持原提交。Ghost-Downloader-3 父仓库已更新到 `d6273793`，既有 `browser_extension/upstream` 子模块也从 `b34a7677` 切换到父仓库锁定的 `97f6005b`；Awesome-Agent-Skills-for-Empirical-Research 的既有 Paper-WorkFlow 子模块也已同步至新父仓库锁定提交，具体前后版本见子模块核验 JSON。两棵工作树均干净，没有初始化新的子模块。

本轮初次按 **120,000,000 字节**上限核算，25 个已有项目暂缓检出；随后用户明确授权“超过限制的可以直接更新”，这 25 个项目已全部按大小例外继续更新，最终不再有因大小限制而跳过的项目。包括 Ghidra、ECC、Codetracer、Terraform、prompts.chat、Taste Skill 等，具体前后提交和实际大小见最终 JSON。**新增项目的默认下载上限仍为 120 MB，已有仓库更新按本次授权允许超限**。daizhigev20 与 scientific-agent-skills 原为部分克隆，保留按需下载布局，未补全其全部缺失正文或对象。

| 仓库 | 处理结果 | 本地保留提交 |
|------|------|------|
| Agent-Reach-v1.6.1 | 无 upstream，保留原状 | `7a38047a` |
| daizhigev20 | 部分克隆资料库，保留按需下载布局 | `012bc393` |
| reverse-skill | 本地修改，保留原状 | `a5171e03` |
| scientific-agent-skills | 部分克隆资料库，保留按需下载布局 | `1e5eeffb` |
| sklib | 本地修改，保留原状 | `730df725` |

Horizon 与 freebie-radar 已在此前专项核验中从 `ae30765a`、`2fb807c1` 快进到 `12d5fbde`、`4f89041a`；本次全目录核对无需再次更新，详见[专项记录](#2026-11-15-horizon-与-freebie-radar-再次核验)。来源去重数量仍为 **143 项**。新版一级仓库表以本次实际 HEAD 与同步结果为准；旧批次提交、Skill 数量与能力评价保留原核验时间，没有将物理文件数直接当作逻辑 Skill 总数。

新增 `scripts/sync-repositories.py`，默认只读检查，`--pull` 显式同步，`--allow-over-limit` 对应用户授权；为快进、本地修改、分叉、超限、分离 HEAD、只读模式、部分克隆保护和明确大小例外运行 **9 项本地 Git 场景测试，全部通过**。未安装依赖、模型、全局 Skill/MCP，也未启动第三方应用或浏览器。

完整结果见[最终核验 JSON](../scripts/repository-sync-20261115-final.json)；首轮与各次重试路径列在其 `evidence` 字段。聚合仓库只提交来源、索引、维护脚本和校验记录，不提交第三方仓库工作树、Git 对象或 Python 缓存。


## 2026-11-15 Horizon 与 freebie-radar 再次核验

用户再次指定两个已有来源，先查同日记录再获取远端更新，沿用新默认 **120 MB（源码与 Git 合计）** 上限，不重复增加来源数量。

| 项目 | 更新前 → 更新后 | 本地大小（含 Git） | Skill 与用途 |
|------|------|------|------|
| [Horizon](https://github.com/Thysrael/Horizon) | `ae30765a` → `12d5fbde`，main 快进 | 15,636,105 字节（15.64 MB） | 1 个 `skills/horizon/SKILL.md`；新闻聚合、筛选、简报生成与投递，MIT |
| [freebie-radar](https://github.com/ZiChuanLan/freebie-radar) | `2fb807c1` → `4f89041a`，main 快进 | 4,077,300 字节（4.08 MB） | 0 个 SKILL.md；资源聚合、筛选与推送工作台，MIT |

两者工作树干净、与本次获取的 origin/main 一致并通过 Git 对象校验。未安装依赖、全局 Skill/MCP 或运行采集和推送；后续全目录同步以其单独记录为准。完整证据见[本次复核 JSON](../scripts/repository-review-20261115-radar-recheck.json)。

## 2026-11-15 网络工具、安全审查与 Chrome 项目追加核验

先查既有记录：open-code-review 已于 9 月 15 日收录、10 月 27 日更新；chrome-devtools-mcp 已有本地源码；modern-web-guidance-src 在同日早批次因超过 100 MB 只登记；tailcat 与 codex-security 为新来源。

用户追加指令将后续单项目默认上限从 100 MB 提高为 **120,000,000 字节（120 MB）**，仍按完整当前源码与 `.git` 文件长度合计。三个新克隆只保存默认分支浅历史，已有两个仓库仅 fast-forward；跳过 LFS 实体和第三方子模块，不下载运行依赖。此前 100 MB 的历史记录保留原口径。

| 项目 | 本次处理与提交 | 本地大小（含 Git） | 用途与许可 |
|------|------|------|------|
| [tailcat](https://github.com/tailscale/tailcat) | 新增浅克隆，main `e00cdde6` | **1.14 MB** | 使用 Tailscale 数据平面建立 WireGuard 加密的点对点连接，提供类似 netcat 的文本、文件传输和端口转发；连接元数据通过带外地址交换，无需 Tailscale 账号。BSD-3-Clause。 |
| [open-code-review](https://github.com/alibaba/open-code-review) | 已有仓库快进更新，main `375f64cd` → `7e5ce06c` | **25.59 MB** | 基于 Git 差异、确定性流程与 LLM Agent 的代码审查 CLI，含规则匹配、行级评论及委托审查 Skill；Apache-2.0。 |
| [codex-security](https://github.com/openai/codex-security) | 新增浅克隆，main `173483d7` | **33.62 MB** | 用于漏洞发现、验证、修复及威胁建模的 CLI、TypeScript SDK 和 Codex 插件工作流；Apache-2.0。保存源码与 Skill，未安装或运行安全扫描。 |
| [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 已有仓库快进更新，main `086299a6` → `8ba2ac94` | **23.59 MB** | 通过 Chrome DevTools 为 Agent 提供浏览器检查、网络与性能调试能力，含 MCP、CLI 及 8 个 Skill；Apache-2.0。仅更新源码，未启用 MCP 或连接浏览器。 |
| [modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | 新增浅克隆，main `5e5cd33a` | **178.77 MB** | Modern Web Guidance 的指南编写、构建、校准与评测源码；按用户明确授权浅克隆，含 Git 178.77 MB。代码 Apache-2.0，guides/ 文档 CC-BY-4.0；附 13 个维护 Skill 与 2 个分发源入口。 |

**modern-web-guidance-src 大小例外**：本次源码 101,448,846 字节，检出前 Git 数据 77,001,261 字节，检出后合计 **178,774,265 字节（178.77 MB）**，也超过新上限。按用户“这可以下载下来”的明确授权保留完整当前源码浅克隆，不删除资源或稀疏检出。此前只登记的状态已被本节的实际下载结果替代；不追溯改写早批次核验 JSON。

Skill 分类：open-code-review 仍为 **2 个逻辑入口、4 个物理文件**；codex-security 有 **20 个插件入口**，另有 `evals/check-skills/fixtures/` 下 **4 个测试夹具**，合计 24 个物理文件；chrome-devtools-mcp 有 **8 个入口**；modern-web-guidance-src 有 **13 个项目维护入口**与 `guides/modern-web-guidance/SKILL.md`、`skills-src/chrome-extensions/SKILL.md` 两个分发源入口，后两者与已有分发仓库对应，不重复增加逻辑数量；tailcat 没有 SKILL.md。均只随源码保存，没有安装全局 Skill。

运行条件按固定提交记录：tailcat 的 go.mod 为 Go 1.27.2；open-code-review 为 Go 1.26.10，实际审查另需模型服务。codex-security 要求 Node.js 22.13+（22.x）、24.x 或 26.x，以及 Python 3.10+；实际使用需认证和服务配置。chrome-devtools-mcp 运行需受支持的 Node.js 和 Chrome，当前 package.json 声明 Node `^20.19.0 || ^22.12.0 || >=23`；源码构建另需其构建工具链与第三方内容。modern-web-guidance-src 声明 Node.js >=22.18.0，评测另需服务配置。

chrome-devtools-mcp 的 `third_party/devtools-frontend` 子模块仅登记锁定提交 `ab6a630afc025e268297e4b4084886d3e955a171`，未初始化；表内大小不含该第三方内容和运行依赖。五个父仓库均工作树干净、与本次抓取的 origin/main 一致并通过 `git fsck --no-reflogs`。未安装依赖、全局 CLI/Skill/MCP，未启动浏览器、服务或扫描。分享表复核原有 141 个不同来源（旧标题误写 142），新增两个来源后为 **143 项**，其他历史全量统计不重算。

完整提交、源码字节数、Skill 路径、来源与校验见[本批核验 JSON](../scripts/repository-review-20261115-tailcat.json)；追加三个链接的下载前 API 快照见[API 记录](../scripts/repository-api-20261115-additions.json)。


## 2026-11-15 提示词社区、资源雷达与 Modern Web Guidance 源码

> 本节保留同日早批次快照。modern-web-guidance-src 随后已按用户明确授权下载，当前状态和新的 120 MB 规则见上方追加核验记录。

用户取消两条 Twitter 链接，改为检查 `GoogleChrome/modern-web-guidance-src`。普通项目仍要求当前源码与 `.git` 文件长度合计严格小于 **100,000,000 字节**；`prompts.chat` 按用户“这个直接克隆下来”的指令作为本批单项目大小例外。采用默认分支 `--depth 1 --no-checkout`，核算后检出；未拉取完整历史。

| 项目 | 处理与提交 | 实测大小（已克隆项含 Git） |
|------|------|------|
| [f/prompts.chat](https://github.com/f/prompts.chat) | 新增浅克隆，`5da3948c` | 250,647,618 字节（250.65 MB） |
| [ZiChuanLan/freebie-radar](https://github.com/ZiChuanLan/freebie-radar) | 新增浅克隆，`2fb807c1` | 3,917,669 字节（3.92 MB） |
| [Thysrael/Horizon](https://github.com/Thysrael/Horizon) | 新增浅克隆，`ae30765a` | 15,601,101 字节（15.60 MB） |
| [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | 超限，仅登记，未克隆，`5e5cd33a` | 源码 101,448,846 字节（101.45 MB），尚未计 Git |
| [OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM) | 已有，在线核对无需更新，`300e4260` | 10,139,667 字节（10.14 MB） |
| [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) | 已有，在线核对无需更新，`4dd96834` | 3,163,703 字节（3.16 MB） |

`modern-web-guidance-src` 固定提交完整文件树未截断，源码本身已有 **101,448,846 字节**，因此下载前跳过，本地没有创建该目录。该仓库用于指南编写、构建与评测；已有 `modern-web-guidance/` 是可分发的指南、CLI 与 Skill 仓库，两者用途不同。源码树虽列有 15 个 SKILL.md 路径，但本地未下载，不计入本地 Skill 数量。

| 新项目 | 用途、许可与运行条件 |
|------|------|
| f/prompts.chat | 提示词社区、提示词数据与可自托管站点；源码和站点原创内容 MIT，提示词数据 CC0。附 2 个检索类插件 Skill 和 2 个项目开发 Skill，均仅随源码保存。 |
| ZiChuanLan/freebie-radar | 自托管资源聚合与推送工作台，通过规则和 AI 筛选福利、优惠、开源项目及资讯，支持多来源采集与 Telegram 路由；MIT，无 SKILL.md。 |
| Thysrael/Horizon | 按个人兴趣聚合新闻、评分去重并生成中英双语简报，提供 CLI、MCP 与多种投递方式；MIT，附 1 个 Horizon Skill。 |

运行条件：prompts.chat 使用 Next.js、Prisma 与 PostgreSQL，完整自托管需另备依赖与数据库；freebie-radar 的 package.json 要求 Node.js >=22.5.0，AI 筛选与 Telegram 推送需自行配置服务；Horizon 要求 Python >=3.11，采集、AI 分析和投递需另备依赖与对应服务。仅保存源码，不代表这些服务已可运行。

三个新克隆与两个已有仓库的 HEAD 均与本次 API 核对的远端默认分支一致，工作树干净，通过 `git fsck --no-reflogs`。本批未安装依赖、数据库、模型、全局 Skill/MCP/插件，未启动服务或运行应用测试。新项目没有子模块；克隆跳过 LFS 实体下载。分享清单本批新增 4 个来源（包括超限源码仓库的链接），按链接去重共 142 项；此前页面标注 137 项，实际已有 138 个不同来源，本次一并校正当前总数。其他仓库与历史全量统计保持原核验日期。完整来源、提交、大小与检查结果见[本批 JSON](../scripts/repository-review-20261115.json)。


## 2026-11-13 VoxCPM 与 Modern Web Guidance

按用户给出的两个官方链接继续拉取与记录，单项目沿用 **小于 100,000,000 字节（十进制 100 MB）** 的限额，计入当前源码与 `.git` 文件长度。先用 GitHub API 核对默认分支固定提交的完整文件树，再以 `--depth 1 --single-branch --no-tags --no-checkout --no-recurse-submodules` 拉取 Git 对象，核算后检出并复测实际大小。新仓库设置本地 `core.autocrlf=false`；没有修改全局 Git 配置。

| 项目 / 来源 | 本地处理与固定提交 | 含 Git 实测大小 | 用途与许可 |
|------|------|------|------|
| [VoxCPM](https://github.com/OpenBMB/VoxCPM) | 新增 `VoxCPM/` 浅克隆，`main@300e4260` | **10,139,667 字节（10.14 MB）** | 当前主线为 VoxCPM2，提供含中文的多语言语音合成、音色设计、声音克隆与流式生成；0 个 SKILL.md。源码 Apache-2.0，上游也声明模型权重采用该许可；本批未下载权重 |
| [Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance) | 新增 `modern-web-guidance/` 浅克隆，`main@4dd96834` | **3,163,703 字节（3.16 MB）** | 面向编码 Agent 的现代 Web 平台实践与兼容性指导，附 CLI 和 2 个正式 Skill；代码 Apache-2.0，`guides/` 文档 CC-BY-4.0 |

VoxCPM 固定提交包含 **82 个文件、5,970,793 字节源码**，未检出 Git 副本 **4,160,206 字节**，展开前合计 **10,130,999 字节**。Modern Web Guidance 为 **265 个文件、2,258,348 字节源码**，未检出 Git 副本 **869,897 字节**，展开前合计 **3,128,245 字节**。最终大小包含检出后的 Git 索引等元数据；不等于压缩下载量或磁盘分配量。GitHub `size` 含历史统计，只作参考，不替代本机大小。

Modern Web Guidance 的两个逻辑入口均随源码保存：

- `skills/modern-web-guidance/SKILL.md`：检索、读取现代 HTML/CSS/JavaScript 指南，关注原生 Web API、性能、无障碍、浏览器支持与回退策略。
- `skills/chrome-extensions/SKILL.md`：Chrome Manifest V3 扩展开发、调试及 Chrome Web Store 发布指导。

这两个文件均为正式入口，没有复制件或提示模板混入计数。本批只保存源码；未将 Skill 安装到 Codex 或其他 Agent，未执行 npx、插件安装或发布动作。该链接是可分发的 Skill/CLI 仓库，其 README 和 package.json 指向另一个[构建源码仓库 modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src)，本轮只记录其关系，没有额外拉取。

| 项目 | 运行条件与使用评价 |
|------|------|
| VoxCPM | README 推荐 Python >=3.10,<3.13、PyTorch >=2.5.0、CUDA >=12.0；pyproject 的 Python 下限为 >=3.10，未声明该上限。CLI 也提供 cpu、mps、cuda 等设备选项，实际依赖与性能需另行验证。上游模型对照表给 VoxCPM2 的参考显存约 8 GB，不是本机实测；源码大小不含模型。适合与已有 Pocket TTS、LuxTTS、VibeVoice 对照研究中文及多语言语音功能。 |
| Modern Web Guidance | package.json 声明 Node.js >=22.0.0；VS Code 扩展另声明 >=1.90.0。源码保留了指南及 CLI 文件；Skill 默认工作流通过 npx 检索和读取指南，会按需取得 npm 包，后续使用需单独准备环境。适合补充现有 UI 设计与 Chrome DevTools 工具的 Web 平台实践资料；本批未运行 CLI、legacy-scan 或评测。 |

两个仓库均浅克隆、工作树干净，HEAD 与本次抓取的 origin/main 一致（ahead/behind 为 0/0），通过 `git fsck --no-reflogs`，没有子模块或 Git LFS 规则。未下载依赖、模型、发行包，未安装全局 Skill/MCP/插件，未启动服务或运行应用测试，也没有更新其他仓库。分享清单新增两个不同来源，由 **135 项增至 137 项**；历史全量仓库与 Skill 数量保留各自核验日期。完整提交、来源、大小与校验见[本批核验 JSON](../scripts/repository-review-20261113.json)。

## 2026-11-12 Harness²、Orthros、DeepTutor 与 MiniMind

按用户要求继续搜索并收录，默认单项目沿用 **100,000,000 字节（十进制 100 MB）** 上限，计入当前源码与 `.git`。先查默认分支固定提交的完整文件树，再用 `--depth 1 --single-branch --no-tags --no-checkout --no-recurse-submodules` 拉取 Git 对象，按限额决定是否检出，并复测实际大小。DeepTutor 初次超限跳过后，用户追加明确授权“DeepTutor可以克隆下来”，因此仅对该项目豁免大小限制并重新浅克隆、检出源码。其他项目仍按原限额；新仓库本地设置 `core.autocrlf=false` 保留源码换行，未改全局 Git 配置。

| 项目 / 来源 | 本地处理与固定提交 | 大小 | 用途与许可 |
|------|------|------|------|
| [Harness²](https://github.com/google-research/harness2) | 新增 `harness2/` 浅克隆，`main@68688175` | 含 Git **15.30 MB** | 通过提出修改、执行探测、组合改进来调整 Agent 的提示、工具、记忆与 Skills，并保留跨任务经验，模型权重固定；源码 Apache-2.0，附带第三方基准代码保留各自许可 |
| [DeepTutor](https://github.com/HKUDS/DeepTutor) | 按用户大小例外授权新增 `DeepTutor/` 浅克隆，`main@60fb3bdf` | 检出后含 Git **106.70 MB** | 个性化学习平台，包含知识库问答、解题、练习、研究、学习记忆与 CLI；6 个正式 Skill 入口随源码保存；Apache-2.0，第三方部分按各自声明 |
| [MiniMind](https://github.com/jingyaogong/minimind) | 新增 `minimind/` 浅克隆，`master@233d00fa` | 含 Git **23.36 MB** | 小语言模型及预训练、SFT、LoRA、DPO、PPO/GRPO/CISPO、工具调用与 Agentic RL 等训练过程，适合阅读 PyTorch 实现；Apache-2.0 |
| [Orthros 论文](https://arxiv.org/html/2610.13735) | 保存 `arxiv-2610.13735v1.pdf`，暂未确认官方代码仓库 | PDF **2.45 MB** | 按预填充与解码阶段采用不同注意力计算，研究长上下文效率；论文 CC-BY-NC-ND-4.0，不计作 Skill |

论文编号分别核对：**`2610.13735` 为 Orthros，Harness² 为 [`2610.14224`](https://arxiv.org/abs/2610.14224)**。Harness² 原版论文另存根目录 `arxiv-2610.14224v1.pdf`，约 **8.10 MB、37 页**，论文许可 CC-BY-4.0，与源码许可分别记录；Orthros 为 **20 页**。两篇均为 v1，已验证 PDF 结束标记、结构和全部页面文本，文件大小及 SHA-256 见本批 JSON。Harness² 初次传输被截断，已从同一官方版本断点补齐并复核为 8,101,889 字节，失败的临时下载均已清理。Orthros 的 [arXiv 正文](https://arxiv.org/html/2610.13735)与[作者论文列表](https://www.zhongzhuzhou.org/publication/)未提供可确认的对应代码链接，按标题与作者补搜后仍未确认；这不等于断言代码不存在。本批未抓取非官方复现仓库。

DeepTutor 固定提交共 4530 个文件，源码 **70,438,066 字节**。初次未检出的浅 Git 副本为 **35,755,135 字节**，展开前合计 **106,193,201 字节**，当时按限额跳过并清理。用户追加授权后，重新浅克隆并检出全部源码；当前 `.git` 为 **36,257,418 字节**，合计 **106,695,484 字节（106.70 MB）**，以实际检出后的文件长度为准。初次核算与清理证据保留在 JSON 的 `initial_size_limited_attempt`，当前状态记为按用户大小例外授权保留。GitHub `size` 的 258,519 KiB 含历史统计，不作为本机大小；未使用稀疏检出或删除资源缩减源码。

Skill 核对：Harness² 和 MiniMind 都没有 `SKILL.md`，按研究框架和模型代码收录。DeepTutor 有 **6 个正式入口**：根 `SKILL.md`（`deeptutor-cli`）及 `deeptutor/skills/builtin/{docx,pdf,pptx,skill-creator,xlsx}/SKILL.md`；`deeptutor/capabilities/creator/prompts/{en,zh}/skill.md` 是 2 个生成提示模板，不能把这 8 个大小写匹配文件都算作 Skill。DeepTutor 入口均已随源码保存在本地，未安装到全局 Skill 目录。

| 项目 | 运行条件与使用评价 |
|------|------|
| Harness² | README 推荐 Linux、Python 3.12、uv；pyproject 声明 Python >=3.12,<3.14。模型基准另需模型服务、Node.js 20+ 等，WorkBuddy 需 Docker，LAB 需 Pandoc/Poppler。适合与现有 skill-up、SESA、ECC 对照研究 Agent 改进流程。当前 Windows 主机只存源码，未运行 demo、基准或任何执行器。 |
| DeepTutor | Python >=3.11,<3.15；源码 Web 开发推荐 Node.js 22 LTS，完整学习功能另需配置 LLM、嵌入、检索及解析服务。根 Skill 依赖 DeepTutor CLI 和配套文档。本批按用户大小例外授权保存源码，未安装或启动。`.gitattributes` 包含 MP4 的 Git LFS 规则，克隆设置跳过 LFS 内容；当前固定提交未发现 MP4 文件，无额外 LFS 资源下载。 |
| MiniMind | README 参考环境为 Ubuntu 20.04、Python 3.10.16、CUDA 12.2；需按设备单独准备 PyTorch、训练数据与模型权重。当前主线提供 Dense 约 64M 及 MoE 约 198M-A64M 模型；“2 小时、3 元”是上游对特定 RTX 3090 SFT 训练与租卡时段的描述，不作为本机成本或全流程实测。 |
| Orthros | 研究注意力架构与训练/转换方案，不是现有模型可直接打开的推理加速开关。论文报告的加速有上下文长度和硬件等实验条件，本次只保存论文，未复现训练、转换或推理。 |

Harness² 与 MiniMind 两个 Git 仓库均浅克隆、工作树干净、HEAD 与本次抓取的 origin 默认分支一致，并通过 `git fsck --no-reflogs`。两者均无子模块或 Git LFS 规则。最终大小分别为 **15,295,762** 与 **23,358,234 字节**，为文件长度合计，包含 Git，不是压缩下载量或磁盘分配量。未安装依赖、权重、数据集、发行包、全局 Skill/MCP，也未启动服务或运行应用测试。

追加授权后的 DeepTutor 同样为浅克隆、工作树干净、HEAD 与本次抓取的 origin/main 一致，并通过 `git fsck --no-reflogs`；输出中只有不可达 tag 提示，不是对象损坏。版本清单最终增加三个本地目录，其中 DeepTutor 为明确授权的大小例外；不重扫其他仓库或改写历史数量。来源与分享清单新增 3 个项目和 Orthros 论文，分享条目仍为 **135**，本次状态更新不重复计数。完整提交、树大小、Skill 路径、首次清理与追加授权记录、论文校验见[核验 JSON](../scripts/repository-review-20261112.json)。

## 2026-11-11 音视频、认证、代码检索与学习资料

本批登记用户指定的 8 个来源，沿用 **100,000,000 字节（十进制 100 MB）** 的单项目限额。先核对固定提交的完整文件树，再对候选项目以 `--depth 1 --single-branch --no-tags --no-checkout --no-recurse-submodules` 拉取 Git 对象；展开前核算源码与 `.git` 文件长度，展开后复测实际大小。

| 项目 / 来源 | 本地处理与提交 | 大小 | 用途与许可 |
|------|------|------|------|
| [stemdeck](https://github.com/stemdeckapp/stemdeck) | 新增 `stemdeck/` 浅克隆，`main@5f9405ca` | 14.96 MB | 基于 Demucs 分离人声、鼓、贝斯等音轨，附独奏、循环、变速与变调界面；适合音乐练习和音频处理实现参考。 Apache-2.0 |
| [openvid](https://github.com/CristianOlivera1/openvid) | 仅登记，下载前跳过，`main@3cf6c8ab` | 源码 181.96 MB，未克隆 | 录屏或导入视频后添加缩放、设备样机、三维效果及背景，采用 Next.js、FFmpeg.wasm、Three.js；适合产品演示视频研究。 PolyForm-Noncommercial-1.0.0 |
| [openauth](https://github.com/anomalyco/openauth) | 新增 `openauth/` 浅克隆，`master@98dc5962` | 4.47 MB | 以 OAuth 2.0 组织多应用身份认证，支持第三方身份提供方和内置登录流程；仍为 beta，用户查询与创建由应用自行实现。 MIT |
| [laya](https://github.com/NandhaKishorM/laya) | 新增 `laya/` 浅克隆，`main@3a38cbe8` | 74.47 MB | 对输入进行 choice、score、yes/no 等判断，适合分类、请求路由与结构化决策研究；上游的速度和准确率不作为本机实测。 Apache-2.0 |
| [Ix](https://github.com/ix-infrastructure/Ix) | 新增 `Ix/` 浅克隆，`main@b7ea8d9b` | 20.16 MB | 用 tree-sitter 提取符号、调用和导入关系，提供调用链、改动影响及结构查询，可与既有 Graphify、gortex、SKLIB 对照研究。 Apache-2.0 |
| [Hands-On-Large-Language-Models](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) | 新增 `Hands-On-Large-Language-Models/` 浅克隆，`main@ea339081` | 19.71 MB | O’Reilly 同名图书的 12 章 Notebook，覆盖嵌入、Transformer、分类、聚类、提示、RAG、多模态和微调，适合作为系统学习路线。 Apache-2.0 |
| [HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter) | 新增 `HowToLiveBetter/` 浅克隆，`main@dff814dc` | 9.79 MB | 按成本、收益和证据组织健康、生活及办事资料，制度内容以中国大陆为背景；配套 Skill 从正文检索并引用条目，适合资料查询。 正文 CC-BY-4.0；代码 MIT |
| [up](https://github.com/byoungd/up) | 新增 `up/` 浅克隆，`main@ddc96d37` | 36.86 MB | 中英双语书稿，覆盖英语、AI 学习、真实项目、创业验证及生活复盘，附工作表和 EPUB/PDF，适合离线阅读和实践记录。 正文 CC-BY-NC-4.0；代码 MIT |

`openvid` 固定提交共有 1330 个文件，合计 **181,959,302 字节**，尚未计入 Git 就已超限，因此没有创建本地仓库，也没有单独下载其中的 Skill、WASM、三维模型或视频。其许可核对为 [PolyForm Noncommercial 1.0.0](https://github.com/CristianOlivera1/openvid/blob/3cf6c8ab3687498d95b56ffc60af3c1882fba12b/LICENSE.md)，保留非商业使用条件。

Skill 核对：`Ix/skills/ix/SKILL.md` 为 1 个入口；`HowToLiveBetter/skills/life-decision-guide/SKILL.md` 为 1 个逻辑入口，另有 `.claude/skills/` 副本，共 2 个物理文件。`openvid` 上游有 5 个物理 SKILL.md、4 个不同入口（nextjs-developer 在两处内容相同），属于项目开发辅助说明，本轮未保存。其他 5 个来源未发现 SKILL.md，不计作正式 Skill。

| 项目 | 运行条件与使用评价 |
|------|------|
| stemdeck | pyproject.toml 声明 Python >=3.10,<3.14，README 开发环境使用 3.12；另需 uv、FastAPI、Demucs、FFmpeg，桌面壳使用 Tauri。首次运行会另取模型与运行组件，本轮没有运行。 |
| openvid | 上游 Quick Start 使用 pnpm 和 Supabase 配置。当前仓库含 FFmpeg WASM、三维模型和演示视频，源码本身已超过限额；不拆分保存其中的 Skill。 |
| openauth | 支持 Node.js、Bun、AWS Lambda 或 Cloudflare Workers；需配置身份提供方及 KV 等存储，本轮只存源码。 |
| laya | Python >=3.10；PyTorch 与 Hugging Face 权重等需另备，也含多语言 SDK。未下载权重、安装 SDK 或运行推理。 |
| Ix | Windows 路径要求 Node.js >=22 和 Docker Desktop，后端包含 ArangoDB 与记忆层。README 说明后端以发布的 Docker 镜像提供，不由本仓库构建；源码克隆不能代替完整运行系统。未建立索引或接入 MCP。 |
| Hands-On-Large-Language-Models | 上游主要在 Colab T4 16 GB 环境测试；本机执行仍需单独准备 Python 依赖、模型和算力。所收录为示例代码，不包含整本图书的出版授权。 |
| HowToLiveBetter | 可直接阅读 Markdown；Skill 依赖本仓库 book/ 正文。具体健康、财务和法律决策需复核原始出处、日期与当地现行规则，本次未验证每条建议。 |
| up | Markdown、EPUB/PDF 可直接阅读；构建站点另需 Node.js 与 VitePress。第三方材料按 ATTRIBUTIONS.md 及各自来源条件使用。 |

7 个保留仓库均小于 100 MB、工作树干净、HEAD 与本次抓取的对应 origin 默认分支一致，并通过 `git fsck --no-reflogs`。均无子模块，核对 `.gitattributes` 未发现 Git LFS 规则。大小为本机文件长度合计，包含 Git、索引及 Windows 检出后的换行差异；不是压缩下载量或磁盘分配量。未安装依赖、模型、发行包、全局 Skill/MCP 或启动服务，也未运行应用测试。

版本清单只新增这 7 个本地目录，不重扫其他仓库或改写历史总数。8 个来源均为本次新登记，两个分享版本由 123 项增为 131 项。提交、完整文件树大小、Skill 路径及本机校验见 [核验 JSON](../scripts/repository-review-20261111.json)。

## 2026-11-09 Skill 评测、艺术动画与 Agent 工具

按用户要求继续记录并评估是否拉取，单项目上限为 **100,000,000 字节（100 MB）**。沿用当前版本浅克隆的口径，计入源码和 `.git` 文件长度，不用 GitHub 含历史的 `size` 字段代替本机大小；依赖、发行包、模型和子模块均不下载。

| 项目 / 来源 | 本地处理与版本 | 大小（含 Git，十进制 MB） | 用途与评价 |
|------|------|------|------|
| [skill-up](https://github.com/alibaba/skill-up) | 已有 `skill-up/`，从 `6fec8e9f` 快进至 `main@78148136`，不重复克隆 | 12,996,331 字节，约 13.00 MB | Apache-2.0；适合评测本目录的 Skills、比较表现和分析失败。正式入口为 `skills/skill-upper/SKILL.md`；全仓 24 个物理 SKILL.md 中其余为示例和夹具 |
| [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | 仅保留来源与评价；核对 `main@8a0d7d72` 后，在展开源码前跳过，临时 Git 副本已清理 | 完整展开前核算约 **148.62 MB，超过限额** | MIT；艺术风格动画、解说片段、风格配方和场景代码适合动画制作参考，但本次不保留本地源码 |
| [OpenShell](https://github.com/NVIDIA/OpenShell) | 新增 `OpenShell/` 浅克隆，`main@9525bec0` | 55,653,564 字节，约 55.65 MB | Apache-2.0；适合研究 Agent 沙箱、访问策略、网络及凭据管理；部署需另行准备运行环境 |
| [context-mode](https://github.com/mksglu/context-mode) | 新增 `context-mode/` 浅克隆，`main@3a3ef7d5`，包版本 2.1.7 | 37,436,327 字节，约 37.44 MB | Elastic-2.0；通过本地执行和 SQLite FTS5 检索，减少大段工具输出进入上下文；不将上游压缩率作为本机实测 |

新项目先以 `--no-checkout` 拉取浅 Git 对象，再用 `git ls-tree -rl` 的全部文件长度加已有 `.git` 长度判断能否展开。huashu-art-motion 当前文件共 76,010,073 字节，Git 数据为 72,614,498 字节，合计 148,624,571 字节，因而没有展开源码；对象包检查后已删除临时目录。该数值是展开前的合计，不是曾经完整占用 148.62 MB。OpenShell 的 GitHub 历史统计为 101,535 KiB，而本次浅克隆实际约 55.65 MB，故按实际大小收录。

本机适配：skill-up 声明 Go 1.26.0，当前 PATH 未找到 Go，CLI 尚未安装。context-mode 声明 Node >=24.15.0，本机 Node v25.2.1 满足版本下限，且存在 Git Bash；未执行安装、doctor、hooks/MCP 设置或性能测试。其当前许可证为 [Elastic-2.0](https://github.com/mksglu/context-mode/blob/3a3ef7d53c9a30ef05d8f1b009afbcf8d9c6d0a2/LICENSE)，以该版本条款为准。

OpenShell 当前 README 将 Windows + WSL 2 标为实验性路径；原生 Windows 的 MXC 实现在独立 `windows` 分支，官方 [Windows 指南](https://github.com/NVIDIA/OpenShell/blob/9525bec0d3ad79f540c10862e0f463edf084db4f/WINDOWS.md) 说明它仍在开发、尚非生产验证的安全边界。本轮仅保存 `main` 参考源码，没有部署沙箱。huashu-art-motion 若以后另行使用，需准备 uv、FFmpeg 与 Playwright Chromium，这些运行依赖不在本轮下载范围。

保留的三个 Git 仓库均通过 `git fsck --no-reflogs`，工作树干净，HEAD 与本次已抓取 `origin/main` 一致。只新增两个本地 Git 目录；不重算历史全量仓库或 Skill 数量，不更新其他仓库状态。来源清单及两个分享版本同步补充三个不同项目来源，分享清单由 120 项变为 123 项。核验记录见 [本批 JSON](../scripts/repository-review-20261109.json)。未安装依赖、修改全局配置或启动服务。

同日追加核对 [arjun988/blender-skills](https://github.com/arjun988/blender-skills)：**2026-11-02 已登记，当前仍未克隆或安装**。本机没有 `E:\aimodel\blender-skills` 目录，旧记录可见 [11 月 2 日批次 JSON](../scripts/repository-links-added-20261102.json)，台账、Skill 索引及两个分享版本已有链接，不重复增加项目数。上游当前介绍 94 项 Blender Skills，以 Blender MCP 执行为前提；此次按“有没有弄过”核查记录，不另行下载。

## 2026-11-08 Agent Reach v1.6.1源码快照

用户授权下载并更新根目录文档。来源为 [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach)，使用官方 tag `v1.6.1` 浅克隆，未从同名 PyPI 包安装。上游安装说明提示 PyPI 的同名 `agent-reach` 并非该官方项目，不照抄 `pip install agent-reach`。

| 项目 | 本机核对 |
|---|---|
| 新目录 | `E:\aimodel\Agent-Reach-v1.6.1` |
| 版本与提交 | `v1.6.1`，`7a38047acf26a729cbb27851e3cb81639da86b29`，tag 分离 HEAD，克隆后工作树干净 |
| 旧目录 | `E:\aimodel\Agent-Reach`，v1.5.0，`da5044d26fc6adddb6554d5679c94ac22e76e428`，保留不覆盖 |
| 许可 | MIT，以新源码中的 LICENSE 为准 |
| Skill | `agent_reach/skill/SKILL.md`；读取后再按项目需求调用 |
| 本机核验 | 使用现有 Python 将新源码加入本次进程的 `sys.path`，`runtime.cli.main(['version'])` 返回 1.6.1；`unified_channels()` 返回 14 个渠道的动作声明 |
| 安装边界 | 未安装依赖、全局 CLI 或全局 Skill；未执行 setup/add/login，未导入个人浏览器状态或修改原 QQBot 配置 |

渠道声明覆盖 GitHub、Twitter/X、YouTube、Reddit、Facebook、Instagram、B站、小红书、LinkedIn、Boss直聘、V2EX、雪球、小宇宙及 web，具体动作依渠道不同。版本与声明检查不证明对应后端、账号或网络已可用。新 web 后端包含直接 Exa MCP 请求与 Jina 读取路径；本次 Jina 公开页面只读探针在正常用户上下文仍 20 秒超时，不能据此宣称网页渠道可用，也不能推断平台必须登录。

用途是补充公开网页/平台资料读取。声明中没有 SauceNAO/IQDB 图片上传反查接口，不可直接替代 QQBot 以图搜图适配器。公开资料先用现有工具；遇到平台拒绝、限流、验证码、未登录即停止，不切换账号或后端绕过。浏览器渠道首次访问可能自动复制已连接 Chrome 的站点登录，调用前须按项目身份隔离要求单独安排，本轮没有启动浏览器渠道。

本轮保留额外版本副本，不覆盖原目录，也不重算全部一级仓库/Skill 数量。根 README 与 CHANGELOG 已同步；历史扫描和旧安装记录保留其原日期。

## 2026-11-02 网络资料 Agent 记忆 三维制作与语音合成链接

按用户指定新增以下 4 个来源，均为首次登记。此批仅核对 GitHub 页面、README 与可见许可信息，并维护原链接清单及两个分享版本。未克隆源码、安装依赖、修改 Agent 配置或下载模型，不增加本地一级 Git 仓库数或已安装 Skill 数量。

| 项目 | 来源 | 用途 | 可见许可信息 | 本地状态 |
|------|------|------|------|------|
| fq-book | [hoochanlon/fq-book](https://github.com/hoochanlon/fq-book) | 《这本书能让你连接互联网》，介绍代理、隧道、VPN 等网络原理及工具配置 | GitHub 仓库页未显示标准许可证，不据此视为可任意转载 | 仅登记链接 |
| ai-memory | [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) | 编码 Agent 长期记忆及跨工具任务交接，以 Git 管理的 Markdown 保存知识 | MIT | 仅登记链接 |
| blender-skills | [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | Blender 制作 Skills，涉及建模、材质、动画和导出，执行需配合 Blender MCP | MIT | 仅登记链接 |
| LuxTTS | [ysharma3501/LuxTTS](https://github.com/ysharma3501/LuxTTS) | 基于 ZipVoice 的语音合成与声音克隆，README 提供 CUDA、CPU 和 MPS 示例 | 源码 Apache-2.0；模型权重条件需另查对应模型来源 | 仅登记链接，未下载权重 |

本批不将上游宣传的速度或效果写为本地实测结论。分享清单由 116 项增加为 120 项，原有项目均保留。核对记录见 [本批 JSON](../scripts/repository-links-added-20261102.json)。

## 2026-11-01 STT 本地音视频转文字工具

检查根目录文档与本地目录后，确认此前未记录或克隆 [jianchang512/stt](https://github.com/jianchang512/stt)。现以 `--depth 1 --single-branch --no-tags --no-recurse-submodules` 保存到 `E:\aimodel\stt`，分支 `main`，HEAD `0df3151d040c8c8becf4ed07b0f1c373163663ae`，源码版本 `v0.0.94`，许可证 GPL-3.0。

- 用途：基于 faster-whisper 的本地音视频识别工具，提供 Flask 网页界面，输出 text / JSON / SRT；有 `/api` 和 `/v1/audio/transcriptions` 接口，默认地址 `127.0.0.1:9977`、默认使用 CPU。
- 100 MB 限额核验：GitHub API 的仓库统计为 147,033 KiB（约 143.59 MiB，包含历史的仓库统计，不是本次浅克隆下载量）；当前提交 26 个文件合计 1,371,797 字节（约 1.31 MiB）。据此仅浅克隆当前版本，实测含 `.git` 文件总长度 2,080,392 字节（约 1.98 MiB，非磁盘分配量），低于 100 MB。
- `git fsck --no-reflogs` 通过，工作树干净，与已抓取的 `origin/main` ahead/behind 为 0/0；没有 `SKILL.md`，按工具源码收录，不增加正式 Skill 数量。
- 本次只保存源码，未安装依赖或运行服务。仓库不包含识别模型权重或 FFmpeg 可执行文件；README 所述预编译包内置模型不能视为源码已含模型。运行时需另行准备模型、FFmpeg 与 Python 依赖，模型下载不计入本次约 1.98 MiB 的源码大小。

核验证据见 [STT 批次 JSON](../scripts/repository-stt-review-20261101.json)。其余第三方仓库沿用历史核验日期；聚合仓库仅维护台账，第三方源码目录继续被忽略。

## 2026-10-30 KA Music 音乐搜索与歌单参考

按用户指定保存 [umr-xiaomai/kgka_Music_hl](https://github.com/umr-xiaomai/kgka_Music_hl) 到 `E:\aimodel\kgka_Music_hl`。`master@166e84bd668151c9da657df811272b4006da7dbe`，`--depth 1 --no-recurse-submodules` 浅克隆；工作树干净，约14.45 MiB文件内容（含.git，非磁盘实际分配量）。源码配置版本3.3.0-beta；此为Flutter/Dart客户端与API定义参考，未安装Flutter、依赖或运行程序，无SKILL.md。

| 参考项 | 源码确认的地址/参数 | 使用范围 |
|---|---|---|
| 酷狗搜索 | `https://music.api.hoilai.cn/search`；keywords、page、pagesize、type=song | 作为现有酷狗平台的候选备用提供方；响应兼容数组或songs/song/lists列表，身份保持酷狗hash |
| 网易云搜索 | `https://wyy.music.api.hoilai.cn/search`；keywords、limit、offset、type=1；随后`/song/detail?ids=...`补详情 | 同一网易云平台的候选备用，不以同名代替同录音，不搬用客户端ne_内部标识作为外部ID |
| 公共歌单与匹配 | `lib/services/qq_playlist_service.dart`、`playlist_import_service.dart` | 参考公开QQ链接解析、分页、未匹配报告与标题/歌手/时长校准；不导入真实账号歌单 |
| 契约与边界 | `api.json`（OpenAPI3.1.1，151个paths）、`lib/core/api_client.dart` | JSON中的localhost服务器仅作示例，以app_config.dart实际配置为准；现有客户端会话、自动重试不直接移植到Bot |

核对入口：`lib/config/app_config.dart:10`、`lib/services/music_api.dart:875/944`、`lib/models/music_models.dart`。未调用在线搜索/播放/登录/下载接口，未运行测试，也未接入QQBot生产配置；只能确认源码声明的契约，不能确认在线服务可用、免登录或播放权益。未发现独立LICENSE/COPYING文件，README声明“仅供学习交流使用，请勿用于商业用途”；保存作研究参考，代码复制/分发前另核许可。仅新增本仓库记录，不重新扫描其他仓库或改历史总数。机器记录见[scripts/repository-music-review-20261030.json](../scripts/repository-music-review-20261030.json)。

## 2026-10-27 模型记录与本地适配评价

用户随后明确“**不需要下载，有记录就更新**”，因此后续只维护台账和评价。澄清到达前，下列 5 个源码浅克隆已完成；如实记录现状，没有继续下载源码、模型权重、依赖或子模块，没有安装或运行模型。

本地已有 `scientific-agent-skills/skills/timesfm-forecasting/SKILL.md`，主要面向 TimesFM 2.5。本轮补充独立上游与版本差异，不改写第三方 Skill。评价依据为官方 README / 模型卡及只读硬件检查，**不是本机音质、延迟或预测基准测试**。

本机已核实：Windows、i7-12650H（10 核 / 16 线程）、RTX 3050 Laptop（4096 MiB 显存）、默认 Python 3.10.0。未核实系统内存、可用显存或依赖状态；下列判断是选型参考，不是运行验收。

| 项目 / 源码版本 | 用途、版本与许可 | 本地使用评价 |
|-----------------|------------------|--------------|
| [Magenta RealTime 2](https://github.com/magenta/magenta-realtime)，`main@694a545e` | 文本、音频、MIDI 控制的音乐生成；small 230M / base 2.4B；代码 Apache-2.0，权重 CC-BY-4.0，另见 MODEL.md 条款 | **研究保留，暂不列为本机实时音乐首选。** 官方实时应用和 MLX 路径面向 Apple Silicon；NVIDIA Python 离线路径不代表 Windows + 4 GB 显存实时保证。源码要求 Python >=3.11，当前默认版本不满足 |
| [Pocket TTS](https://github.com/kyutai-labs/pocket-tts)，`main@77c3d76b`，包版本 4.0.1 | CPU 流式 TTS、音色克隆；常规模型约 100M，另有 1.9M–18.2M 小型英语模型；代码 MIT，官方模型卡 CC-BY-4.0，预置音色另核许可 | **CPU 非中文 TTS 优先候选。** 不依赖 CUDA；当前支持英、法、德、葡、意、西、荷语，不含中文。要求 Python 3.10–3.14、PyTorch >=2.5，尚未在本机安装或实测 |
| [Supertonic](https://github.com/supertone-oss-archive/supertonic)，`main@1e9799e9` | ONNX 本地 TTS；归档 v3 约 99M、31 语种；示例代码 MIT、模型 OpenRAIL-M | **轻量 ONNX 参考，维护优先级下调。** 已停止开发和支持；31 语种不含中文，lang=na 不等于新增中文能力。Voice Builder / 在线演示不是归档可用能力；仅记录固定归档权重与预置音色路径 |
| [TimesFM](https://github.com/google-research/timesfm)，`master@e51928e2`，包版本 3.0.2 | 时间序列预测，非语音或音乐；3.0 增加原生多变量和协变量支持；代码及 <=2.5 权重 Apache-2.0，**3.0 自托管权重仅限非商业、非生产用途** | **有预测任务时优先复核已有 2.5 Skill。** 200M 的 2.5 更适合先做 CPU / 小批量验证；旧 Skill 资源估计不能外推为 3.0 保证。应做滚动回测，与季节性朴素基线比较，检查缺失值和数据泄漏 |
| [Microsoft VibeVoice](https://github.com/microsoft/VibeVoice)，`main@16fb2cb1` | TTS / ASR 模型家族；代码 MIT，各权重核对具体模型卡 | **分版本选用。** 旧多说话人 TTS 代码已从官方仓库移除；当前 Realtime-0.5B 是英语为主的单说话人流式 TTS，多语言仍属实验，4 GB 显存表现待实测。7B ASR 不列为本机默认方案；官方另有 [VibeASR.cpp](https://github.com/microsoft/VibeASR.cpp) CPU 路径，仅补充链接 |

### 评价依据与后续选用

- 音乐以 [当前硬件说明](https://github.com/magenta/magenta-realtime#hardware-requirements)、[模型卡](https://github.com/magenta/magenta-realtime/blob/main/MODEL.md) 和 [官方应用页](https://magenta.withgoogle.com/mrt2) 为准。官方页面对 base 支持机型的列举存在差异，故不把单一 Mac 最低型号或 Windows 实时速度写成确认结论。
- 非中文轻量 TTS 先看 [Pocket TTS 当前说明](https://github.com/kyutai-labs/pocket-tts#main-takeaways)；ONNX 集成参考见 [Supertonic 归档说明](https://github.com/supertone-oss-archive/supertonic#quick-start) 与 [v3 模型卡](https://huggingface.co/supertone-oss-archive/supertonic-3)。官方其他硬件上的速度倍数没有当作本机成绩。
- TimesFM 的本地既有 Skill 与独立上游 `timesfm/timesfm-forecasting/SKILL.md` 交叉引用，不重复累计为两项能力。[3.0 权重许可说明](https://github.com/google-research/timesfm#license-notice-for-pretrained-weights) 与 2.5 不同，3.0 API 也不能直接照搬 2.5 示例。
- VibeVoice 对照 [当前官方仓库](https://github.com/microsoft/VibeVoice) 与 [Realtime-0.5B 文档](https://github.com/microsoft/VibeVoice/blob/main/docs/vibevoice-realtime-0.5b.md)。不能用 ASR 识别语言范围推断 TTS 合成能力；本批轻量 TTS 与英语 Realtime 版本均不直接列为已验证中文配音方案。

### 静态记录

- 5 个父仓库当前工作树干净，与已抓取 upstream 为 0/0，均通过 `git fsck --no-reflogs`；Magenta 的 SequenceLayers 子模块未初始化，仅记录锁定提交。
- Supertonic、TimesFM 有 LFS 属性规则，不代表已下载模型权重。未运行 hf download、模型初始化或包安装；VibeVoice 源码自带预置音色文件与完整模型检查点分开记录。
- 当前为 110 个可见一级第三方 Git 仓库加 1 个隐藏聚合仓库。5 个源码目录形成于只更新记录的澄清之前，其余仓库未继续批量更新。
- 证据见 [模型批次 JSON](../scripts/repository-model-review-20261027.json)。远端聚合仓库只提交索引、评价和核验记录，第三方源码工作树及模型权重继续排除。

---

## 2026-10-27 Skill 评测、逆向工具与既有项目更新

按“已有就更新，未有就下载并记录”处理本批指定项目。搜索确认“阿里开源 skill-up”为 `alibaba/skill-up`；`open-code-review` 是代码审查工具，下载器对应本地已有的 `Ghost-Downloader-3`。上游链接均去除 `utm_source` 参数。

| 仓库 | 类型与用途 | 本地处理 / HEAD | 许可证与收录结论 |
|------|------------|-----------------|------------------|
| [alibaba/skill-up](https://github.com/alibaba/skill-up) | Agent Skill、Agent 与 Workspace 的评测 CLI；通过 skill-upper 诊断失败、演进用例并回归 | 新增浅克隆 `E:\aimodel\skill-up\`；`main@6fec8e9f` | Apache-2.0；1 个正式 skill-upper，另有示例和测试夹具；适合作为 Skill 质量评测工具保存 |
| [morluto/rea](https://github.com/morluto/rea) | REA 逆向分析 CLI / MCP，连接 Ghidra、Hopper、IDA 等分析引擎 | 新增浅克隆 `E:\aimodel\rea\`；`main@570abe95` | REA 自有代码 MIT，第三方组件各守其许可；含 1 个用户工作流 Skill 和 4 个仓库维护 Skill；5 个第三方子模块仅记录锁定提交、未初始化 |
| [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | 反汇编、反编译、程序图与脚本化逆向分析框架 | 新增浅克隆 `E:\aimodel\ghidra\`；`master@1b9e58a9` | 主许可证 Apache-2.0，第三方部分另见 NOTICE / 各组件许可；0 个 SKILL.md；保存的是源码，未下载预构建发行包 |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 多 Agent 平台的 Skills、规则、hooks、记忆与开发工作流集合 | 新增浅克隆 `E:\aimodel\ECC\`；`main@25278e7d` | MIT；主 `skills/` 有 311 个 Skill 入口；全仓 1062 个物理 SKILL.md 含平台变体与翻译，不按 1062 个独立能力计数 |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | AI 代码审查 CLI、Agent Skill 与 CI 集成 | 既有仓库快进 `55899906` → `375f64cd`；保持 `main` | Apache-2.0；仍为 2 个逻辑 Skill、4 个物理文件 |
| [XiaoYouChR/Ghost-Downloader-3](https://github.com/XiaoYouChR/Ghost-Downloader-3) | 多协议桌面下载器 | 保留旧 `main@601e2068`；新建并切换 `catalog/upstream-20261027@ee0cb1aa` 跟踪 `origin/main` | GPL-3.0；上游强制更新导致无法快进，保留旧分支后检出当前源码；cat-catch 仍固定 `b34a7677` |

### 静态核验与复核记录

- 6 个仓库的当前工作树均干净，当前分支与已抓取 upstream 的 ahead/behind 均为 0/0，均通过 `git fsck --no-reflogs`；没有匹配 `filter=lfs` 的属性文件。保留原有浅克隆形态，4 个新增仓库使用 `--depth 1 --single-branch`。
- 本地占用约为：skill-up 11.5 MiB、REA 103.2 MiB、Ghidra 396.6 MiB、ECC 92.5 MiB、open-code-review 23.8 MiB、Ghost Downloader 103.9 MiB。数值含 `.git`，REA 不含未初始化的第三方子模块。
- skill-up 全仓 23 个物理 SKILL.md：正式入口 1 个、该入口内测试夹具 2 个、示例 3 个、E2E 夹具 17 个。REA 的正式入口为 `.agents/skills/reverse-engineer-anything/SKILL.md`。
- REA 的 5 个 gitlink（binwalk、ghidra-nativeaot、jadx-headless-mcp、unblob、wakaru）及锁定提交保存在 JSON 中；没有递归下载或执行。上游 CONTRIBUTING 已注明 Windows 下 Unblob 子模块检出需要额外处理。
- Ghidra 源码 README 当前要求 JDK 25、Gradle 9.1.0+ 等构建工具。需要运行时应按官方 Releases 的 `ghidra_<version>_<release>_<date>.zip` 说明下载；源码克隆本身不构成可运行安装。REA 使用现有 Ghidra 安装，不能直接把本批源码目录当作分析引擎。
- 下载器上游从旧引用 `601e2068` 强制更新到 `ee0cb1aa`。未 reset、rebase 或覆盖旧分支；新分支与 `origin/main` 一致，已核实初始化的 cat-catch HEAD 等于父仓库锁定提交。
- 首次新增仓库下载遇到 TLS EOF，沙箱外重试后 4 项全部成功。Git 所有权检查使用命令级 `safe.directory`，未写全局 Git 配置。
- 批次机器记录：[scripts/repository-batch-20261027.json](../scripts/repository-batch-20261027.json)。该批完成时可见一级 Git 仓库为 105 个，另有隐藏聚合仓库 1 个；该批仅更新上述 6 项，其余仓库保留历史同步日期。
- 本轮保存源码与记录，没有安装依赖、全局 Skill、MCP、桌面程序或 Ghidra 运行时，没有执行评测、代码审查或逆向分析，也没有提交或推送。

---

## 2026-09-15 代码审查、下载工具与手绘风格候选

| 仓库 | 类型与用途 | 本地处理 | 判断与边界 |
|------|------------|----------|------------|
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | AI 代码审查 CLI、Codex/Claude/Cursor Skill 与 CI 集成 | 浅克隆到 `E:\aimodel\open-code-review\`，HEAD `55899906` | Apache-2.0；2 个逻辑 Skill（源码与插件目录各保留一份），适合本目录长期保存；未安装 `ocr`、未配置模型或执行审查 |
| [XiaoYouChR/Ghost-Downloader-3](https://github.com/XiaoYouChR/Ghost-Downloader-3) | Python/PySide6 多协议下载器，支持 HTTP、BT、FTP、流媒体、GitHub 与 Hugging Face | 浅克隆到 `E:\aimodel\Ghost-Downloader-3\`，HEAD `601e2068`；浏览器扩展子模块固定为 `b34a7677` | GPL-3.0；属于工具源码而非 Skill，适合作为下载器实现参考；未安装 Python 依赖、浏览器扩展或桌面程序 |
| [yang0/handraw-style](https://github.com/yang0/handraw-style) | 001–261 手绘风格图集与双语提示词 Skill | 仅登记；审查用临时浅克隆已移除 | 仓库未提供许可证文件，且仅 340 个跟踪文件的浅克隆已约 195.1 MiB，主要体量来自参考图片；不在本地长期镜像，使用前应先取得清晰授权 |

### 静态核验

- `open-code-review` 与 `Ghost-Downloader-3` 均为 `--depth 1` 浅克隆、工作树干净，并通过 `git fsck --no-reflogs`；本地占用分别约 18.4 MiB 和 29.5 MiB。
- `Ghost-Downloader-3` 的 `browser_extension/upstream` 已检出父仓库锁定的 `xifangczy/cat-catch@b34a7677`，没有擅自跟随子模块最新 `master`。
- 扫描同时发现此前仅登记的 `3b1b/manim` 已在根目录形成 `master@fafa083a` 浅克隆；本轮只补正台账，不改动该工作树。
- 本轮没有执行候选仓库代码、安装依赖、写入全局 Codex Skills、启动服务或向第三方仓库推送。

---

## 2026-09-14 UI 组件库、动效 Skill 与写作 Skill

| 仓库 | 类型与用途 | 本地处理 | 边界 |
|------|------------|----------|------|
| [swamimalode07/rare-ui](https://github.com/swamimalode07/rare-ui) | React / Next.js / Tailwind / Motion 的 shadcn 动效组件 registry | 浅克隆到 `E:\aimodel\rare-ui\`，HEAD `d146c352` | MIT；0 个 `SKILL.md`，通过 shadcn CLI 按组件引入 |
| [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | 可组合、可访问、源码可定制的 UI 组件与 registry 工具链 | 浅克隆到 `E:\aimodel\shadcn-ui\`，HEAD `2b3e6d4f` | MIT；含 `shadcn` 与 `migrate-radix-to-base` 两个 Skill，未全局安装 |
| [slev12397/beautiful-ui](https://github.com/slev12397/beautiful-ui) | `beautifului.dev` 的 AI-native React 界面 primitives 与 shadcn registry | 浅克隆到 `E:\aimodel\beautiful-ui\`，HEAD `ff0f74d6` | MIT；`SidebarNav` 使用安装时校验许可证的商业图标包，使用前应替换图标或配置合法授权 |
| [starc007/ui-components](https://github.com/starc007/ui-components) | `beui.dev` 的 React 19 / Tailwind 4 / Motion 组件库 | 浅克隆到 `E:\aimodel\beui\`，HEAD `8d3fa7b4` | 公开部分 MIT；含 `beui` 与 `beui-pro` Skill，Pro 需要客户 token，未访问付费 registry |
| [Jakubantalik/transitions.dev](https://github.com/Jakubantalik/transitions.dev) | CSS UI 动效、动效 token、Agent Skill 与 Refine 工具 | 浅克隆到 `E:\aimodel\transitions-dev\`，HEAD `598d3d6a` | 含 `transitions-dev`、`transitions-polish`、`refine-live` 3 个 Skill；公开工具代码为 MIT，下载的 Pro 配方另受站点条款约束 |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | 检测并编辑 20+ 类模板化 AI 写作模式 | 浅克隆到 `E:\aimodel\no-ai-slop\`，HEAD `000650b1` | MIT；含 1 个正式 Skill、eval 和 Codex 插件清单，未全局安装 |

### 仅登记、未克隆

| 仓库 | 判断 |
|------|------|
| [jbiaojerry/ebook-treasure-chest](https://github.com/jbiaojerry/ebook-treasure-chest) | 主要聚合第三方电子书下载链接，GitHub 页面未显示明确许可证；本目录只保存来源链接，不镜像内容，也不对链接内容的版权或可用性背书。 |
| [3b1b/manim](https://github.com/3b1b/manim) | 3Blue1Brown 的 ManimGL 数学讲解动画引擎，MIT；按要求只登记。它与更偏稳定、测试和社区支持的 Manim Community 版是不同项目，安装说明不能混用。 |

### 静态核验

- 6 个新增仓库均为 `main` 分支、`--depth 1` 浅克隆、干净工作树，无 `.gitmodules` 和 Git LFS 规则，并通过 `git fsck --no-reflogs`。
- 本地占用约为：Rare UI 24.8 MiB、shadcn/ui 62.6 MiB、Beautiful UI 1.3 MiB、beUI 10.5 MiB、Transitions.dev 44.6 MiB、No AI Slop 0.5 MiB，合计约 143.3 MiB。
- 本轮只保存源码和索引，没有执行仓库代码、安装 npm/bun/Python 依赖、启动 Refine 服务、访问 Pro registry，或写入全局 Codex skills。
- 搜索中另发现 `Kainiko943/beautiful-ui`，但 `beautifului.dev` 官网对应的是 `slev12397/beautiful-ui`，因此未克隆前者。

---

## 2026-09-05 全目录同步与多仓库维护工具

| 检查项 | 结果 |
|------|------|
| 可见一级 Git 仓库 | 92 |
| 实际 fast-forward | 43 |
| 原本已是最新 | 47 |
| 默认分支迁移 | 1（`codetracer`: `main` → `stable`） |
| 本地修改跳过 | 1（`reverse-skill`） |

### 处理说明

- 新增 [`scripts/Sync-RepositoryCatalog.ps1`](../scripts/Sync-RepositoryCatalog.ps1)：默认只读检查；显式 `-Pull` 时只运行 `git pull --ff-only --prune`，自动跳过 dirty/no-upstream 仓库，使用命令级 `safe.directory` 而不污染全局 Git 配置，并可输出已脱敏的 JSON 结果。
- 新增 [`REPOSITORY_MANAGEMENT.md`](REPOSITORY_MANAGEMENT.md)，记录本目录的拉取、整理和查看组合：`rg` 做精确搜索，zvec-grep 做语义/BM25/向量检索，Graphify 做关系与调用路径图谱；mani 和 ghorg 仅列为特定场景候选，暂不重复克隆。
- 首轮发生 3 次 GitHub TLS `unexpected EOF`，改用 HTTP/1.1 重试后 `mergration`、`scientific-agent-skills`、`taste-skill` 全部成功；这三项没有遗留失败。
- `Awesome-Agent-Skills-for-Empirical-Research` 快进后，将 `skills/69-Paper-WorkFlow` 子模块更新到父仓库锁定的 `ca36e316`，最终工作树干净。
- `codetracer` 上游已删除 `main` 并将默认分支改为 `stable`。本地旧 `main` 相对共同祖先保有 3 个独有提交；本轮保留该分支，新建并切换到跟踪 `origin/stable` 的本地 `stable`（`0478cb4f`），同时刷新 origin HEAD 和全分支 fetch refspec。
- `reverse-skill` 的上游 `main` 发生强制更新；本地当前有 3 个修改文件，且为 ahead 1 / behind 142。为避免覆盖用户内容，本轮只 fetch 远程引用，没有 pull、stash、reset、merge 或 rebase。
- 其余仓库保持原克隆形态；76 个浅克隆没有被批量扩成完整历史。除父仓库明确锁定的 Paper-WorkFlow 外，不递归更新嵌套仓库或子模块。

---

## 2026-09-05 Graphify、zvec-grep、Terraform 与中国专利 Skill

| 仓库 | 类型 | 本地目录 | Skill / 使用结论 | 状态 |
|------|------|----------|------------------|------|
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 代码、文档和媒体知识图谱工具 / Agent Skill | `E:\aimodel\graphify\` | 1 个小写 `graphify/skill.md`；擅长关系、调用路径、社区和跨文件架构理解，与语义检索互补 | 既有浅克隆已补成完整历史并快进；未安装 Python 包或 Agent 集成 |
| [zvec-ai/zvec-grep](https://github.com/zvec-ai/zvec-grep) | 本地优先的 ripgrep + BM25 + 向量混合检索 CLI / MCP | `E:\aimodel\zvec-grep\` | 0 个 `SKILL.md`；可通过 `zg install --target codex` 配置 Codex MCP，适合大型代码与资料库的语义发现 | 已完整克隆；未安装 npm 包、模型、服务或 MCP |
| [hashicorp/terraform](https://github.com/hashicorp/terraform) | 基础设施即代码 CLI 核心源码 | `E:\aimodel\terraform\` | 0 个 `SKILL.md`；适合作为 Terraform Core 实现、状态/计划/资源图与插件协议参考，不含 providers | 已完整克隆；未构建、未安装 Go 或 Terraform CLI |
| [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) | 中国专利全流程 Agent Skill | `E:\aimodel\patent-disclosure-skill\` | 1 个可调用路由 Skill + 6 个内部子技能；覆盖交底、申请文件、著录检索、解读、审查答复和政策简报 | 已完整克隆；未装 Python/Playwright/CAD/OA 依赖，未写入全局 Codex skills |

### 克隆记录

| 仓库 | Origin | HEAD | 分支 / 完整历史 |
|------|--------|------|-----------------|
| graphify | https://github.com/Graphify-Labs/graphify.git | `937e59a5` | `v8`；非浅克隆，1862 个提交、13 个远程引用、202 个 tags |
| zvec-grep | https://github.com/zvec-ai/zvec-grep.git | `52653951` | `main`；非浅克隆，271 个提交、5 个远程引用、5 个 tags |
| terraform | https://github.com/hashicorp/terraform.git | `7b8c301b` | `main`；非浅克隆，44947 个提交、883 个远程引用、471 个 tags |
| patent-disclosure-skill | https://github.com/handsomestWei/patent-disclosure-skill.git | `a0156905` | `main`；非浅克隆，40 个提交、7 个远程引用、0 个 tags |

### 静态核查结论

- 四个仓库均为完整、非 partial/非 shallow clone，工作树干净并与各自 upstream 为 0/0；均无 Git submodule 和 Git LFS 跟踪项，并通过 `git fsck --full --no-reflogs`。本地总占用约为 Graphify 31 MiB、zvec-grep 58 MiB、Terraform 388 MiB、专利 Skill 18 MiB。
- Graphify 已从旧的单分支浅克隆补齐完整对象、所有远程分支和 tags，fetch refspec 也改为持续跟踪全部远程分支。当前版本 `0.9.54`，要求 Python `>=3.10`；本机 Python 3.10/3.12 满足要求，但未安装 `uv` 或 `graphifyy`。
- zvec-grep 当前版本 `0.2.1`，要求 Node.js `>=22`；本机 Node.js `25.2.1` 满足要求。它默认可本地保存文件、索引和模型，远程 embedding 需另行授权；安装器会写 Codex 配置和 `AGENTS.md`，因此本轮只保留源码。
- Terraform 的完整 Git pack 约 359 MiB，是本批最大仓库；保留完整历史适合源码考古和版本差异分析，但日常只使用 CLI 时下载官方发行版更省空间。源码要求 Go `1.26.4`，本机未安装 Go；Terraform 1.6+ 源码采用 Business Source License 1.1，使用和再分发需按其条款核对。
- 专利 Skill 的根 `SKILL.md` 是唯一 `user-invocable: true` 的路由入口，6 个子技能均为内部路由。仓库要求 Python 3.9+，主路径还涉及 Playwright、系统 Chrome/Edge、Word/PPT 解析和可选 CAD/Obsidian/OA 向量库；适合按整仓安装，不能只拷一个子目录。它可辅助专利文稿和检索，但不替代专利代理师或法律审查。
- Graphify 与 zvec-grep 都值得保留：前者把显式关系和调用链做成持久图谱，后者偏语义发现、BM25 与精确检索路由；Terraform 只在需要 IaC 源码研究时体现完整历史价值；专利 Skill 领域明确、价值高，但建议在真实任务出现后再按整仓安装和补依赖。

---

## 2026-09-03 PDF Inspector、Effective HTML 与既有 Skills 复核

| 仓库 | 类型 | 本地目录 | Skill / 使用结论 | 状态 |
|------|------|----------|------------------|------|
| [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector) | Rust PDF 分类、文本抽取与 OCR 路由工具 | `E:\aimodel\pdf-inspector\` | 0 个 `SKILL.md`；可将 PDF 分类为 `TextBased`、`Scanned`、`ImageBased`、`Mixed`，返回置信度及逐页 OCR 路由，并可直接抽取结构化 Markdown | 已浅克隆；未编译、未安装 Python/Node/Rust 包或 OCR 运行时 |
| [plannotator/effective-html](https://github.com/plannotator/effective-html) | 自包含 HTML artifact Skills / Codex 插件 | `E:\aimodel\effective-html\` | 6 个 Skill：`html`、`design-artifact`、`html-wireframe`、`html-prototype`、`html-plan`、`html-diagram`；适合结构化报告、线框、原型、计划和关系图 | 已浅克隆；未安装为全局 Skill 或 Codex 插件 |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 精简 Agent 编码行为准则 | `E:\aimodel\andrej-karpathy-skills\` | 1 个 Skill；内容与当前 Codex 的最小改动、显式假设和验证闭环规则高度重合 | 已有克隆，不重复下载；保留作参考，不追加全局安装 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 工程与生产力 Skill 集合 | `E:\aimodel\mattpocock-skills\` | 当前本地 37 个 `SKILL.md`；覆盖需求澄清、TDD、诊断、架构、评审、研究与交接，适合按单项选用 | 已有干净克隆，不重复下载或全量安装；旧的 `backend-skills\mattpocock-skills\` 副本未改动 |

### 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| pdf-inspector | https://github.com/firecrawl/pdf-inspector.git | `65b7fa1` | 2026-09-01 `fix(loader): bound object-stream decompression at load (lopdf 0.44) (#478)` |
| effective-html | https://github.com/plannotator/effective-html.git | `d95debb` | 2026-08-03 `docs: sync design artifact guide (#23)` |

### 静态核查结论

- 两个新增仓库均为 MIT 许可、浅克隆、干净工作树，没有 Git submodule，并通过 `git fsck --no-reflogs`。`pdf-inspector` 约 25 MB，`effective-html` 约 43 MB。
- `pdf-inspector` 当前包版本为 `1.17.0`，Rust crate 要求 Rust `1.88`，Python 包要求 Python `>=3.8`。默认 Rust 构建不启用 OCR；完整本地 OCR 是可选 feature，另需 PDFium、ONNX Runtime 和模型文件，因此本轮只保存源码。
- `pdf-inspector` 与既有 `liteparse` 都能把原生文本 PDF 转为 Markdown，但前者更适合作为轻量的“先分类、再按页送 OCR”路由层；上游性能与质量数字是项目方基准，本轮没有在 Windows 上复跑。
- `Effective HTML` 的 `html` 是可自动路由的广义入口，其余专门 Skill 多为显式调用。它与 `taste-skill`、`hallmark`、`emilkowalski-skills/prototype`、`archify` 有部分视觉或原型重叠，但独特价值是把报告、计划、线框、原型和关系图统一为可访问、响应式、单文件 HTML artifact。
- 两个新仓库由提升权限的克隆进程创建，Windows Git 会报告所有权保护。核查时仅使用命令级 `safe.directory` 例外，没有写入全局 Git 配置；后续常规 Git 操作可能仍需相同的单次例外或先修正目录所有权。

---

## 2026-09-02 Pisper 下载与既有项目复核

| 仓库 | 类型 | 本地目录 | Skill / 使用结论 | 状态 |
|------|------|----------|------------------|------|
| [ling-kong-ran/pisper](https://github.com/ling-kong-ran/pisper) | 多 Agent 本地工作台（Desktop / TUI / Mobile） | `E:\aimodel\pisper\` | 0 个标准 `SKILL.md`；基于 Pi Coding Agent 管理并行会话、Turn 上下文分支、工作目录、权限、工作流、记忆和 MCP/插件 | 已完整克隆；未安装 Node.js 依赖、桌面应用或 Provider 凭据 |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 精简的 Agent 编码行为准则 | `E:\aimodel\andrej-karpathy-skills\` | 已有 1 个 Skill；原则与当前 Codex 工作规范高度重合，保留作参考，不追加全局安装 | 已有浅克隆；本轮未更新 |
| [StarTrail-org/LEANN](https://github.com/StarTrail-org/LEANN) | 本地私有 RAG / 语义检索套件 | `E:\aimodel\LEANN\` | 无标准 `SKILL.md`，含 OpenClaw `leann-memory` 适配；适合大规模本地知识库，不是轻量向量库替代品 | 已有克隆；因 Windows Git 所有权保护未改动或更新 |

### 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| pisper | https://github.com/ling-kong-ran/pisper.git | `a0e2af6c` | 2026-09-02 `test: track visual providers in the visual connections section` |

### 静态核查结论

- `pisper` 为完整、非浅克隆，不含 Git submodule，已通过 `git fsck --no-reflogs`；工作树约 85 MB。它不含通用 Agent Skills 标准的 `SKILL.md`，因此不写入 `SKILLS_INDEX.md`。
- Pisper 的“分支”是从已完成 Turn 派生且继承上下文的 Agent 会话分支，每个会话可独立模型、上下文、工作目录和权限。它适合可视化管理并行 Agent 工作，但不应被当作 Git worktree 创建、冲突消解和代码合并队列工具；底层运行时为 Pi Coding Agent，非 Codex 原生运行时。
- `andrej-karpathy-skills` 与 `LEANN` 均已在旧台账中登记，故未重复克隆。LEANN 的当前 Windows 所有权与运行用户不一致；为避免修改全局 Git `safe.directory` 配置，本轮没有拉取或检查其工作树。

---

## 2026-09-02 Sepia、Archify 下载与候选项目评估

| 仓库 | 类型 | 本地目录 | Skill / 使用结论 | 状态 |
|------|------|----------|------------------|------|
| [Nanako0129/sepia](https://github.com/Nanako0129/sepia) | 去 AI 腔写作 Skill | `E:\aimodel\sepia\` | 1 个可移植 `SKILL.md`，含 Codex 原生插件结构；适合小说叙事修订及发布说明、PR 回复、复盘等专业文稿 | 已完整克隆；未安装依赖、未写入全局 Codex skills |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | 架构与流程图 Agent Skill / Node.js 渲染器 | `E:\aimodel\archify\` | 1 个 `archify` Skill；可生成架构、工作流、时序、数据流和生命周期图，导出自包含 HTML/SVG/PNG/WebM | 已完整克隆；未安装依赖、未写入全局 Codex skills |
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | 大型角色提示词与流程库 | — | 上游仍在维护且支持 Codex；适合按需借鉴专业角色的检查清单，不建议全量安装以避免规则重叠和上下文噪声 | 仅核查，未克隆 |
| [alibaba/zvec](https://github.com/alibaba/zvec) | 嵌入式向量数据库 | — | 适合本地 RAG、Agent 记忆、私有知识库和代码/文档语义搜索；不适合分布式多节点或高并发多写入 | 仅核查，未克隆 |

### 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| sepia | https://github.com/Nanako0129/sepia.git | `ac2f06e8` | 2026-09-02 `docs(zh-CN): add Simplified Chinese README (#33)` |
| archify | https://github.com/tt-a1i/archify.git | `06dd0526` | 2026-09-02 `fix: ship third-party mark notices (#267)` |

### 静态核查结论

- 两个已下载仓库均为完整克隆（非 shallow clone），且不含 Git submodule；已通过 `git fsck --no-reflogs` 核验。`archify` 工作树约 152 MB，包含文档、示例、实验和生成产物，完整保留以便离线研究或二次开发。
- `archify` 同时拥有项目展示/文档站点，但其主体是开源仓库和可通过 Skills CLI 安装的 Skill；对日常画图不需要读取整个本地仓库。
- `zvec` 提供进程内、无服务端的向量检索，并支持稠密/稀疏向量、全文、结构化过滤和混合检索；要使用它仍需由应用或模型侧产生嵌入向量。

---

## 2026-08-29 LoopX 与 ego-lite 下载及浏览器能力复核

| 仓库 | 类型 | Stars（核查时） | 本地目录 | Skill | 状态 |
|------|------|----------------|----------|-------|------|
| [huangruiteng/loopx](https://github.com/huangruiteng/loopx) | 长周期 Agent 控制平面 | 5.3k | `E:\aimodel\loopx\` | 9 份物理 `SKILL.md`（8 正式 + 1 demo） | 已浅克隆，仅保存源码 |
| [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) | Agent 友好浏览器与 CDP harness | 14.2k | `E:\aimodel\ego-lite\` | 1 个 `ego-browser` Skill | 已浅克隆；Windows 上不可安装当前 macOS 应用 |

### 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| loopx | https://github.com/huangruiteng/loopx.git | `e2275510` | 2026-08-29 `perf(cli): lazily load common command owners (#3717)` |
| ego-lite | https://github.com/citrolabs/ego-lite.git | `5ca3c36c` | 2026-08-24 `Merge pull request #317 from citrolabs/docs/star-history-branch` |

### 静态核查结论

- `LoopX` 负责 goal、todo、gate、evidence、quota、handoff、恢复和跨运行时持续执行，不负责浏览器控制或截图解析。它适合作为浏览器工具之上的长任务控制层。
- `LoopX` 本地项目版本为 `0.5.3`，要求 Python `>=3.11`，核心包声明无第三方运行时依赖；当前版本使用 Apache-2.0，旧版本 MIT 文本仍保留。
- `ego-lite` 仓库开源的是 MIT 许可的 `ego-browser` TypeScript/CDP harness 和 Skill，不包含提供 `globalThis.ego` bindings 的浏览器应用源码。
- `ego-browser` 以语义 Snapshot + 元素引用驱动网页，也能捕获截图；它没有内置 OCR 或多模态视觉模型，不能把“保存截图”等同于“理解截图像素”。
- 上游当前明确只提供 macOS 浏览器应用，Windows/Linux 在 roadmap；所以本轮没有安装应用、扩展、依赖或全局 Skill，也没有复现项目方的性能/成功率基准。
- 与根目录 `browser-use`、`chrome-devtools-mcp`、`OpenCLI`、`web-access`、`nanobrowser`、Playwright `webapp-testing`、`crawl4ai` 和 MiniMax `vision-analysis` 的详细区别见 [BROWSER_AUTOMATION_COMPARISON.md](BROWSER_AUTOMATION_COMPARISON.md)。

---

## 当前维护边界（2026-08-28）

- 检查 `E:\aimodel` 下的一级有效 Git 仓库，包括 skill 与 tool；只对干净工作树和已配置上游的普通分支执行快进更新。
- 不递归更新仓库内部的 skill/tool 子目录。
- 2026-08-28 共检查 82 个仓库：41 个快进、39 个已是最新、1 个因本地修改跳过、1 个因历史分叉保留原状。
- `reverse-skill` 因本地 3 个修改文件跳过更新；`codetracer` 补全浅克隆历史后为 ahead 3 / behind 1521，不自动改写。

### 2026-08-28 同步异常复核

| 仓库 | 初始现象 | 原因 | 当前处理 |
|------|----------|------|----------|
| gortex | `git pull` 报 TLS `unexpected EOF` | 瞬时 HTTPS 传输中断 | 重试成功，`ea44cc2` → `06939fc`，与上游 0/0 |
| codetracer | 初看 ahead 1 / behind 3464，无法快进 | 旧浅克隆边界掩盖真实历史；补全后确认上游重排，实际 ahead 3 / behind 1521 | 保留本地 `main`；未 merge/rebase/reset，等待人工决策 |
| reverse-skill | 未执行拉取 | 工作树有 3 个本地修改文件 | 按保护规则跳过 |

`codetracer` 的 3 个本地提交均为 2026-05-07 的上游作者提交：`6a5c0a9`、`167f62c`、`757b0b9`。上游后来出现同作者日期、同主题的 `d4ee0a1` 等重排内容，但补丁并不完全等价，因此不能把它当作普通落后仓库直接快进。

---

## 2026-07-19 第一批总览

| 仓库 | 类型 | Stars（检索时） | 本地目录 | 状态 |
|------|------|----------------|----------|------|
| [mortspace/playcaptcha](https://github.com/mortspace/playcaptcha) | React 安全组件 | 425 | `E:\aimodel\playcaptcha\` | 已克隆，待项目内依赖安装 |
| [zzet/gortex](https://github.com/zzet/gortex) | 代码智能/跨代理工具 | 884 | `E:\aimodel\gortex\` | 已克隆，待 CLI/daemon 配置 |
| [run-llama/liteparse](https://github.com/run-llama/liteparse) | PDF/文档解析 | 11.6k | `E:\aimodel\liteparse\` | 已克隆，待 Python/Node/Rust 入口选择 |
| [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | LLM 友好网页爬取 | 73.1k | `E:\aimodel\crawl4ai\` | 已克隆，待 Python 依赖和浏览器依赖配置 |
| [jackwener/OpenCLI](https://github.com/jackwener/OpenCLI) | 自然语言浏览器自动化 CLI | 26.9k | `E:\aimodel\OpenCLI\` | 已克隆，待 npm/Chrome 扩展配置 |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | AI 浏览器自动化 | 105k | `E:\aimodel\browser-use\` | 已克隆，待 Python/Playwright 依赖配置 |

---

## 克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| playcaptcha | https://github.com/mortspace/playcaptcha.git | `e9e0e0f` | 2026-06-12 fix: add demo video to README |
| gortex | https://github.com/zzet/gortex.git | `ea44cc2` | 2026-07-15 Merge pull request #295 from zzet/dependabot/github_actions/actions-minor-patch-fe548e5f3c |
| liteparse | https://github.com/run-llama/liteparse.git | `cc0fa5a` | 2026-07-14 fix glibc builds |
| crawl4ai | https://github.com/unclecode/crawl4ai.git | `7e80152` | 2026-07-15 Merge pull request #2077 from unclecode/release/v0.9.2 |
| OpenCLI | https://github.com/jackwener/OpenCLI.git | `b0f84c9` | 2026-07-13 fix: click hit-testing + facebook feed/search DOM drift (#2076 #2071 #2089 #2090) (#2126) |
| browser-use | https://github.com/browser-use/browser-use.git | `950eb03` | 2026-07-16 Release 0.13.6 with Browser Harness 0.1.6 (#5245) |

---

## 2026-07-19 第二批下载

| 仓库 | 类型 | Stars（检索时） | 本地目录 | Skill/插件 | 状态 |
|------|------|----------------|----------|------------|------|
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Claude 知识工作插件集 | 22.8k | `E:\aimodel\knowledge-work-plugins\` | 212 SKILL.md / 22 插件 | 已克隆，待插件配置 |
| [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | LLM 输入/日志压缩工具 | 59.8k | `E:\aimodel\headroom\` | 1 插件 | 已克隆，待代理/代理服务器配置 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 工程技能库 | 176k | `E:\aimodel\mattpocock-skills\` | 41 SKILL.md / 1 插件 | 已存在，已 fast-forward 更新 |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | Claude/Cursor 行为指南 | 194k | `E:\aimodel\andrej-karpathy-skills\` | 1 SKILL.md / 1 插件 | 已克隆 |
| [NVIDIA/skillspector](https://github.com/NVIDIA/skillspector) | AI skill 安全扫描 | 13.4k | `E:\aimodel\skillspector\` | 23 SKILL.md | 已克隆，待 Python 依赖配置 |
| [tjxj/z-skills](https://github.com/tjxj/z-skills) | 可复用 skill 集合 | 187 | `E:\aimodel\z-skills\` | 10 SKILL.md | 已克隆 |
| [bradautomates/claude-video](https://github.com/bradautomates/claude-video) | Claude 视频理解 skill | 9.1k | `E:\aimodel\claude-video\` | 1 SKILL.md / 2 插件 | 已克隆，待视频依赖配置 |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 审美/设计品味 skill | 64.9k | `E:\aimodel\taste-skill\` | 13 SKILL.md / 1 插件 | 已克隆 |
| [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | LLM/RAG/Agent 应用合集 | 124k | `E:\aimodel\awesome-llm-apps\` | 6 SKILL.md | 已克隆 |
| [powerycy/multi-style-image-generator](https://github.com/powerycy/multi-style-image-generator) | 多风格图像生成 skill | 22 | `E:\aimodel\multi-style-image-generator\` | 1 SKILL.md | 已克隆 |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | 多平台网页读取/搜索 CLI | 57.7k | `E:\aimodel\Agent-Reach\` | 1 SKILL.md | 已克隆，待 CLI 配置 |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 反 AI 味 UI 设计 skill | 12.4k | `E:\aimodel\hallmark\` | 1 SKILL.md | 已克隆，已安装到 Codex skills |

### 第二批克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| knowledge-work-plugins | https://github.com/anthropics/knowledge-work-plugins.git | `74d516a` | 2026-07-17 bump(qdrant-skills): 97c547be -> d1af526e (#620) |
| headroom | https://github.com/headroomlabs-ai/headroom.git | `6cdfd3f` | 2026-07-18 fix(proxy/openai): feed chat/completions traffic into the traffic learner (#2333) |
| mattpocock-skills | https://github.com/mattpocock/skills.git | `9603c1c` | 2026-07-16 Merge pull request #586 from mattpocock/batch-grill-me-granular-facts |
| andrej-karpathy-skills | https://github.com/multica-ai/andrej-karpathy-skills.git | `2c60614` | 2026-04-20 Sync Chinese README with English version (add Cursor section) (#95) |
| skillspector | https://github.com/NVIDIA/skillspector.git | `8f534e2` | 2026-07-14 Merge pull request #275 from NVIDIA/keshavp/oss-release-2026-07-14 |
| z-skills | https://github.com/tjxj/z-skills.git | `fc4bddc` | 2026-07-10 Harden web packaging and video downloads |
| claude-video | https://github.com/bradautomates/claude-video.git | `83da59f` | 2026-06-30 Fix WATCH_DETAIL silently falling back to default |
| taste-skill | https://github.com/Leonxlnx/taste-skill.git | `7c397f2` | 2026-07-17 Add IMG.LY sponsor |
| awesome-llm-apps | https://github.com/Shubhamsaboo/awesome-llm-apps.git | `41621a5` | 2026-07-17 Merge pull request #931 from SHAI-manpreet-likhari/fix/guard-empty-openai-response-memory-tutorials |
| multi-style-image-generator | https://github.com/powerycy/multi-style-image-generator.git | `b58d569` | 2026-07-15 Merge pull request #1 from powerycy/feat/automatic-dependency-bootstrap |
| Agent-Reach | https://github.com/Panniantong/Agent-Reach.git | `1494c2a` | 2026-07-18 Merge pull request #492 from Panniantong/codex/add-agent-skills-hub-link |
| hallmark | https://github.com/Nutlope/hallmark.git | `aeb42fb` | 2026-06-04 Merge pull request #18 from Nutlope/fix/existing-stylesheet-merge |

---

## 项目说明

### mortspace/playcaptcha
- **定位**: 一个 React CAPTCHA 组件，主打“可玩”的验证体验，可用于替代传统验证码交互。
- **技术栈/许可**: TypeScript，MIT License。
- **适合场景**: 有前端登录、注册、表单防滥用需求时再安装；它不是 AI skill，也不是代理工具。
- **安装参考**:
  ```bash
  npm install playcaptcha
  ```
- **本地目录**: `E:\aimodel\playcaptcha\`

### zzet/gortex
- **定位**: 为 AI 编码代理准备的代码智能服务器/工具，提供仓库索引、语义搜索、依赖关系和符号级理解。
- **AI 兼容性**: 文档明确面向多种 AI 编码代理，适合 Claude Code、Codex CLI、Cursor、Gemini CLI 等共享使用。
- **技术栈/许可**: Go，Apache-2.0 License。
- **安装参考**:
  ```powershell
  irm https://get.gortex.dev/install.ps1 | iex
  gortex install
  gortex daemon start --detach
  ```
- **本地目录**: `E:\aimodel\gortex\`

### run-llama/liteparse
- **定位**: LlamaIndex 生态里的开源 PDF 解析工具，强调本地、快速、适合 AI/agent 工作流。
- **能力**: 解析文本、表格、图片、公式，支持 Python、JS/TS、CLI、Docker，也提供 agent skill 方式。
- **技术栈/许可**: Rust/Python/TypeScript，Apache-2.0 License。
- **安装参考**:
  ```bash
  pip install liteparse
  # 或
  npm install -g @llamaindex/liteparse
  # Claude Code / Codex skill:
  npx skills add run-llama/llamaparse-agent-skills --skill liteparse
  ```
- **本地目录**: `E:\aimodel\liteparse\`

### unclecode/crawl4ai
- **定位**: 开源、LLM 友好的网页爬虫和抓取工具，把网页转成可用于 AI 的 Markdown/结构化结果。
- **能力**: 异步爬取、浏览器自动化、抽取/清洗内容、深度爬取、RAG 数据准备、Docker/MCP/CLI 集成。
- **技术栈/许可**: Python，Apache-2.0 License。
- **安装参考**:
  ```bash
  pip install -U crawl4ai
  crawl4ai-setup
  crawl4ai-doctor
  ```
- **本地目录**: `E:\aimodel\crawl4ai\`

### jackwener/OpenCLI
- **定位**: 把自然语言命令转换为浏览器自动化操作，强调使用本机浏览器登录态和站点适配器。
- **能力**: Chrome 扩展桥接、站点适配器、`npx skills` 安装、支持用自然语言操作 Amazon、ChatGPT、GitHub、Gmail、Notion 等站点。
- **技术栈/许可**: TypeScript，Apache-2.0 License。
- **安装参考**:
  ```bash
  npm install -g @jackwener/opencli
  opencli doctor
  npx skills add jackwener/opencli
  ```
- **本地目录**: `E:\aimodel\OpenCLI\`

### browser-use/browser-use
- **定位**: 让 AI agent 控制浏览器的开源自动化框架，可作为 Python 库、CLI、云服务或 agent skill 使用。
- **AI 兼容性**: 文档列出 Claude Code、Codex CLI、Cursor、Windsurf、VS Code、Goose 等用法，跨 AI 复用价值高。
- **技术栈/许可**: Python，MIT License。
- **安装参考**:
  ```bash
  pip install browser-use
  playwright install chromium
  # 或安装 agent skill:
  uvx browser-use[cli] skill install
  ```
- **本地目录**: `E:\aimodel\browser-use\`

---

## 安装优先级建议

| 优先级 | 仓库 | 理由 |
|--------|------|------|
| 高 | browser-use/browser-use | 通用浏览器自动化，直接提升代理办事能力 |
| 高 | zzet/gortex | 给多个编码代理共享代码理解能力，适合当前资源库定位 |
| 高 | unclecode/crawl4ai | 抓网页、构建 RAG 语料、研究资料收集都常用 |
| 中 | jackwener/OpenCLI | 与 browser-use 有重叠，但更偏自然语言操作已登录网站 |
| 中 | run-llama/liteparse | 文档/PDF 场景很有用，按需要安装 |
| 低 | mortspace/playcaptcha | 前端组件，不属于 AI 工具，只有具体项目需要 CAPTCHA 时安装 |

---

## 兼容性判断

这些项目大多可以给 Claude Code 之外的 AI 使用：

- **跨 AI 最强**: `gortex`、`browser-use`、`crawl4ai`。它们提供 CLI、服务、MCP 或库接口，不绑定单一模型。
- **偏 Claude/Codex skill 生态**: `liteparse`、`browser-use`、`OpenCLI` 都提供或提到 skill 安装方式，但底层也能通过 CLI/库调用。
- **不是 AI skill**: `playcaptcha` 是 React 组件，应该按前端依赖管理，而不是按 agent skill 管理。

---

## 后续安装记录模板

后续执行依赖安装或全局安装时，建议按下面格式追加到 `SKILLS_INSTALLED.md`：

```markdown
### 项目名
- **目录**: `E:\aimodel\项目名\`
- **来源**: https://github.com/owner/repo
- **安装命令**: `...`
- **状态**: 已安装 / 已克隆 / 待配置
- **备注**: 依赖、环境变量、MCP 配置或登录态要求
```

---

## 2026-07-30 第三批更新

| 仓库 | 类型 | Stars（检索时） | 本地目录 | Skill/插件 | 状态 |
|------|------|----------------|----------|------------|------|
| [rahulv-official/inspira-ui](https://github.com/rahulv-official/inspira-ui) | Vue/Nuxt UI 组件集合 | 未统计 | `E:\aimodel\inspira-ui\` | 0 SKILL.md / 0 插件 | 已克隆，按前端项目需要使用 |
| [kepano/kepano-obsidian](https://github.com/kepano/kepano-obsidian) | Obsidian vault 模板 | 未统计 | `E:\aimodel\kepano-obsidian\` | 0 SKILL.md / 0 插件 | 已克隆，作为 Obsidian 模板和配套资料 |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Obsidian Agent Skills | 未统计 | `E:\aimodel\obsidian-skills\` | 5 SKILL.md / 1 插件 | 已克隆，仅保留在当前目录 |
| [earendil-works/pi](https://github.com/earendil-works/pi) | 自扩展 coding agent / TUI / LLM API | 未统计 | `E:\aimodel\pi\` | 17 SKILL.md（测试夹具为主）/ 0 插件 | 已克隆，待按需研究 CLI 和包结构 |
| [Simon-He95/vue-tui](https://github.com/Simon-He95/vue-tui) | Vue 3 terminal UI toolkit | 未统计 | `E:\aimodel\vue-tui\` | 1 SKILL.md / 0 插件 | 已克隆，skill 位于 `.agents\skills\vue-tui\` |

### 第三批克隆记录

| 仓库 | Origin | HEAD | 最新提交 |
|------|--------|------|----------|
| inspira-ui | https://github.com/rahulv-official/inspira-ui.git | `fdd645e` | 2026-07-15 Fix category selection |
| kepano-obsidian | https://github.com/kepano/kepano-obsidian.git | `4736973` | 2026-01-08 Update attachments |
| obsidian-skills | https://github.com/kepano/obsidian-skills.git | `a1dc48e` | 2026-06-08 Merge pull request #59 from SDGLBL/codex/add-base-embed-example |
| pi | https://github.com/earendil-works/pi.git | `71efc6f` | 2026-07-30 Add [Unreleased] section for next cycle |
| vue-tui | https://github.com/Simon-He95/vue-tui.git | `010872a` | 2026-07-25 feat: update 3D badge CLI to support Bun runtime and improve image decoding |

### 第三批项目说明

#### inspira-ui
- **定位**: 面向 Vue 和 Nuxt 的视觉组件集合，风格来源接近 Aceternity UI、Magic UI 和 shadcn-vue 生态。
- **技术栈/许可**: Nuxt 4、Vue 3、TypeScript、MIT License。
- **安装参考**:
  ```bash
  pnpm add @inspira-ui/plugins
  ```
- **备注**: 这是前端组件/文档仓库，不是 agent skill。

#### kepano-obsidian
- **定位**: Steph Ango 的个人 Obsidian vault 模板，展示分类、附件、模板、Daily、Notes、References 等结构。
- **配套关系**: 与 `kepano/obsidian-skills` 搭配使用，前者提供 vault 组织样例，后者提供 agent 处理 Obsidian 文件的 skills。
- **备注**: 没有 `SKILL.md`，不作为 skill 安装。

#### obsidian-skills
- **定位**: 遵循 Agent Skills 规范的 Obsidian skills，可被 Claude Code、Codex、OpenCode 等 skills-compatible agent 使用。
- **包含 skills**: `obsidian-markdown`、`obsidian-bases`、`json-canvas`、`obsidian-cli`、`defuddle`。
- **备注**: 本次只克隆到当前目录，没有复制到全局 Codex skills 目录。

#### pi
- **定位**: Pi Agent Harness，包含交互式 coding agent CLI、agent runtime、多供应商 LLM API 和 TUI 包。
- **主要包**: `@earendil-works/pi-coding-agent`、`@earendil-works/pi-agent-core`、`@earendil-works/pi-ai`、`@earendil-works/pi-tui`。
- **备注**: 仓库中的 `SKILL.md` 主要位于测试夹具和扩展示例，不按正式 skill 集合计入安装。

#### vue-tui
- **定位**: Simon He 开发的 Vue 3 terminal UI toolkit，可用一套 Vue 组件模型渲染浏览器 DOM、真实 CLI stdout 和 headless tests。
- **包名**: `@simon_he/vue-tui`。
- **包含 skill**: `.agents\skills\vue-tui\SKILL.md`。
- **安装参考**:
  ```bash
  pnpm add @simon_he/vue-tui vue
  ```

---

## 2026-08-15 第四批下载与同步

### 新增一级仓库

| 仓库 | 类型 | HEAD | 本地目录 | Skill/参考状态 |
|------|------|------|----------|----------------|
| [StarTrail-org/LEANN](https://github.com/StarTrail-org/LEANN) | 本地语义搜索、RAG、MCP | `dc85934` | `E:\aimodel\LEANN\` | 0 个标准 `SKILL.md`；`skills/leann-memory/` 是 OpenClaw `claw.json + instructions.md` 适配 |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | UI 动效与设计 skill | `78761e1` | `E:\aimodel\emilkowalski-skills\` | 10 个正式 `SKILL.md` |
| [bobeff/open-source-games](https://github.com/bobeff/open-source-games) | 开源游戏索引 | `3a9ab8f` | `E:\aimodel\open-source-games\` | 0 个 `SKILL.md`；游戏开发参考 |
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | 从零实现软件的教程索引 | `aa17439` | `E:\aimodel\build-your-own-x\` | 0 个 `SKILL.md`；软件/游戏实现参考 |
| [Zenghuang-Fu/SESA-Self-Evolving-Search-Agents](https://github.com/Zenghuang-Fu/SESA-Self-Evolving-Search-Agents) | 搜索 agent 自演化研究代码 | `74de5d7` | `E:\aimodel\SESA-Self-Evolving-Search-Agents\` | 0 个 `SKILL.md`；研究参考 |

### 已有仓库同步

| 仓库 | HEAD | 最新提交 | 状态 |
|------|------|----------|------|
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | `30fc648f` | 2026-08-14 `fix(landing): remove duplicate pricing capability block (#6913)` | 已快进同步 |
| [earendil-works/pi](https://github.com/earendil-works/pi) | `b1efcf7d7` | 2026-08-14 `chore: approve contributors from issue #8124` | 已快进同步 |

### 论文下载

| 论文 | 标题 | 本地文件 |
|------|------|----------|
| [arXiv:2607.29468v1](https://arxiv.org/html/2607.29468v1) | Self-Play Meets Skill Evolution: Self-Evolving Search Agents that Pose, Solve, and Remember | `E:\aimodel\arxiv-2607.29468v1.pdf` |
| [arXiv:2607.27733v1](https://arxiv.org/html/2607.27733v1) | VeriSkill: A Self-Evolution Framework for Program Verification Skills | `E:\aimodel\arxiv-2607.27733v1.pdf` |

本批只下载和记录，不安装依赖，不复制到全局 Codex skills 目录，也不更新仓库子目录内的 Markdown。

---

## 2026-08-15 其他 skill 仓库更新

### 本轮同步结果

| 项目 | 数量 | 说明 |
|------|------|------|
| 已快进更新 | 26 | 工作区干净且远程可访问 |
| 已是最新 | 15 | 无需变更 |
| 跳过 | 1 | `reverse-skill` 有 3 个本地修改文件，保留用户修改 |

### 发现并补登记的仓库链接

| 仓库 | 类型 | HEAD | 本地目录 | Skill 数量 |
|------|------|------|----------|------------|
| [different-ai/openwork](https://github.com/different-ai/openwork) | 跨 Agent 的桌面工作区、MCP、skill/plugin 共享平台 | `08fb6af` | `E:\aimodel\openwork\` | 33 |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 本地代码/文档知识图谱与 `/graphify` skill | `7281f27` | `E:\aimodel\graphify\` | 1 |

这两个仓库的远程地址此前存在于本地 Git 配置，但未登记在根目录台账；本次已补入索引和手动收藏清单。

---

## 2026-08-17 第五批设计 skill 与参考仓库

| 仓库 | 类型 | HEAD | 本地目录 | Skill/参考数量 | 状态 |
|------|------|------|----------|----------------|------|
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UI/UX skill/plugin | `a38d04c` | `E:\aimodel\ui-ux-pro-max-skill\` | 6 SKILL.md / 1 plugin | 已快进更新 |
| [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | `DESIGN.md` 设计系统参考库 | `8147538` | `E:\aimodel\awesome-design-md\` | 73 DESIGN.md / 0 SKILL.md | 已克隆，仅作设计参考 |

### 本批说明

- `ui-ux-pro-max-skill` 最新提交：2026-08-14 `feat(search): overhaul relevance and curated design data`。
- `awesome-design-md` 提供从真实网站提炼的 `DESIGN.md` 参考文档，可按项目需要整理使用。
- 本批未安装依赖、未复制到全局 Codex skills，也未修改仓库内部 Markdown。

---

## 2026-08-25 科研 skills 补全与作品集参考

| 仓库 | 类型 | HEAD | 本地目录 | Skill/参考数量 | 状态 |
|------|------|------|----------|----------------|------|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 开放 Agent Skills 科研技能库 | `36d8f13` | `E:\aimodel\scientific-agent-skills\` | 本地 163 个一级 `SKILL.md` | 已重新获取缺失对象并完整检出；2446 个跟踪文件无缺失，HEAD 与 `origin/main` 一致，工作树干净；结构契约已验证，不安装学科依赖或全局 skills |
| [emmabostian/developer-portfolios](https://github.com/emmabostian/developer-portfolios) | 开发者作品集案例索引 | `89f6044` | `E:\aimodel\developer-portfolios\` | 0 个 `SKILL.md` | 已浅克隆，仅作参考，不计入正式 skill |

### 科研技能库验证边界

- 仓库 `_meta` 的 9 项平台无关规则通过：插件清单、技能发现、测试覆盖映射、需求映射、共享文件一致性与脚本结构等均无问题。
- Windows 文件系统上的 POSIX 执行位检查不适用；Git 索引确认 `latex-posters` 与 `scientific-schematics` 的 shell 脚本均为 `100755`，两者的 `bash -n` 语法检查通过。
- 当前只补全仓库内容，不安装 Python/科研软件包、不配置外部 API 凭据、不复制到全局 Agent/Codex skills。实际使用时按课题读取目标 `SKILL.md` 并做依赖、权限、许可证审查。

---

## 2026-08-27 系统设计参考仓库

| 仓库 | 类型 | HEAD | 本地目录 | 内容/状态 |
|------|------|------|----------|-----------|
| [ByteByteGoHq/system-design-101](https://github.com/ByteByteGoHq/system-design-101) | 系统设计图解、短文与面试参考 | `b28380a` | `E:\aimodel\system-design\system-design-101\` | 已使用 `--depth 1` 浅克隆；400 篇 Markdown guides、0 个 `SKILL.md`；工作树干净 |

### 下载判断与边界

- **选择下载**：Git pack 约 1.31 MiB、跟踪内容约 1.76 MB、浅克隆本地总占用约 3.2 MB，落盘成本低，Markdown 正文可离线搜索；内容覆盖 API、数据库、缓存、支付、软件架构、云与分布式系统，可与 `donnemartin/system-design-primer` 互补。
- **不是完整离线归档**：400 篇 guide 的主图通过 `https://assets.bytebytego.com/diagrams/...` 引用，仓库没有收录这批主图；离线时仍可读文字，但查看图解需要联网。
- **许可限制**：仓库声明 CC BY-NC-ND 4.0，需署名、限非商业用途且不得发布演绎版本。因此只作为本地学习参考保存，不改写后再分发。
- **不作为 skill**：没有 `SKILL.md`，未安装 Node.js 依赖，也不纳入 `SKILLS_INDEX.md` 的正式 skill 数量。

---

## 2026-08-28 殆知阁古典文献仓库

| 仓库 | 类型 | HEAD | 本地目录 | 状态 |
|------|------|------|----------|------|
| [daizhige-org/daizhigev20](https://github.com/daizhige-org/daizhigev20) | 中国古典文献全文数据、数字人文语料 | `012bc39` | `E:\aimodel\daizhigev20\` | 已对 `data` 分支做浅层部分克隆；只检出根说明文件，正文对象按需下载；0 个 `SKILL.md` |

### 数量统计与口径

本地数字来自 2026-08-22 的 `data` 分支提交 `012bc393ff989f1a4354edf1a16c82645a99b715`；在线数字来自 2026-08-28 查看时的殆知阁目录页。

| 分类 | Git 树中的 Markdown 文件 | 在线目录标注“部” |
|------|-------------------------:|-------------------:|
| 佛藏 | 5,135 | 5,135 |
| 儒藏 | 914 | 914 |
| 医藏 | 965 | 965 |
| 史藏 | 4,179 | 4,178 |
| 子藏 | 3,084 | 3,084 |
| 易藏 | 343 | 343 |
| 艺藏 | 446 | 446 |
| 诗藏 | 820 | 820 |
| 道藏 | 1,720 | 1,720 |
| 集藏 | 2,974 | 2,974 |
| 现代作品 | 5 | 5 |
| **合计** | **20,585** | **20,584** |

这里的数字更准确地说是“正文 Markdown 页面/文件数”，不能直接等同于严格去重后的独立书种数：仓库会把《全唐文》《宋史》《本草纲目》等按卷拆成多个文件，个别文献还同时保留总文件与分卷目录。旧版项目常用“约 16,000 种、20 万卷、20 亿字”的概数；当前站点介绍页写“1.8 万部”，而实时目录显示 20,584 部。需要引用数量时，应注明日期和统计口径。

Git 树共有 23,151 个跟踪文件，其中 20,585 个为十藏及现代作品正文、2,560 个位于 `.sources`（校订来源快照），其余 6 个是根说明/配置及工作流文件。

### 内容、用途与边界

- **内容组织**: 仿经史子集扩展为佛、儒、医、史、子、易、艺、诗、道、集十藏，并另设现代作品；正文主要为简体中文 Markdown，文件头加入 YAML 元数据。
- **维护状态**: 这是已停止维护的 `garychowcmu/daizhigev20` 的修订 fork；维护者正在清理繁简转换、论坛残留、HTML/脚本等问题，并对《宋史》《本草纲目》《全唐文》等重点典籍重新导入、拆卷和互校。
- **适用场景**: 古籍全文检索、个人文库、数字人文研究、文言文 NLP/RAG 语料准备，以及查找公开文本来源。
- **质量提醒**: 数据来自多年网络汇集，修订工作仍在继续。学术引用、训诂、版本研究或模型评测前，应回查 frontmatter 所列来源、影印本或权威点校本，不能把仓库文本直接当作无误底本。
- **许可提醒**: 网站说明所收文本属于公有领域，但 `data` 分支没有顶层 `LICENSE` 文件。公有领域正文、后加元数据、编校注、来源快照和 `tools` 分支代码不是同一个权利层次；再分发或商用前需逐项核对来源与许可。
- **不是 skill**: 仓库没有 `SKILL.md`，不纳入 [SKILLS_INDEX.md](SKILLS_INDEX.md) 的正式 skill 数量，也未安装 Elasticsearch 或其他依赖。

### 本地保存策略

完整正文较大。官方说明 GitHub Pages 正文 artifact 在 2026 年 7 月约 2.15 GB，因此本次采用可检索目录、正文按需获取的轻量方式：

```powershell
# 已执行的轻量克隆方式
git clone --branch data --depth 1 --filter=blob:none --no-checkout https://github.com/daizhige-org/daizhigev20.git daizhigev20

# 列出仓库全部路径，不下载正文 blob
git -c core.quotepath=false -C E:\aimodel\daizhigev20 ls-tree -r --name-only HEAD

# 查找书名（PowerShell 示例）
git -c core.quotepath=false -C E:\aimodel\daizhigev20 ls-tree -r --name-only HEAD | Select-String '本草纲目'

# 按需读取一个文件；首次读取时 Git 才会获取对应正文 blob
git -C E:\aimodel\daizhigev20 show "HEAD:医藏/本草纲目/卷01.md"
```

当前本地目录约 3.4 MB，工作树干净，浅克隆和 `blob:none` 配置均已确认。若以后确实需要完整离线库，再按官方命令另行完整检出；本轮没有批量下载约 2 GB 的正文，也没有获取完整提交历史。

---

## 2026-08-28 学术科研 Skills 仓库与 Multi Search Engine

| 仓库/来源 | 类型 | HEAD/快照 | 本地目录 | 数量与状态 |
|------|------|------|----------|-----------|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 综合科学 Agent Skills | `36d8f13` | `E:\aimodel\scientific-agent-skills\` | 已有仓库与远端一致；163 个 `SKILL.md`；MIT |
| [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | Nature 写作、科研绘图与文献工作流 | `205ed18` | `E:\aimodel\nature-skills\` | 浅克隆、工作树干净；20 份物理文件，19 个可触发技能；Apache-2.0 |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | AI/ML 研究工程技能库 | `773a529` | `E:\aimodel\AI-Research-SKILLs\` | 浅克隆、工作树干净；98 个 Skill；MIT |
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | 研究全生命周期 Agent 工作区 | `6ed46da` | `E:\aimodel\claude-scholar\` | 浅克隆、工作树干净；45 个 Skill；MIT |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | 论文构筑、重写与审计编排器 | `895f4e4` | `E:\aimodel\PaperSpine\` | 浅克隆、工作树干净；7 份物理文件，V4 逻辑上是 1 个 Skill；MIT |
| [brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) | 社会科学实证 Skill 聚合库 | `517717f` | `E:\aimodel\Awesome-Agent-Skills-for-Empirical-Research\` | 保留旧本地目录并更新 canonical origin；catalog 1,096 项、含子模块后 1,162 份物理文件；根许可证 CC BY-SA 4.0 |
| [Multi Search Engine](https://github.com/aAAaqwq/AGI-Super-Team/tree/main/skills/multi-search-engine) | 搜索 URL 模板/路由参考 | SHA-256 `aba6bcf…` | `E:\aimodel\multi-search-engine\` | 仅保存上游 `SKILL.md` 与本地审计说明；非 Git、未安装 |

### 定位与选择建议

- **K-Dense**：覆盖面最大，适合生物信息、化学、医学、科学数据库、统计和科研产物生成。很多 Skill 只是针对 Python 包或外部数据库的高质量使用指南；运行时仍需逐项安装依赖、配置凭据并核对数据许可，不应整库一次性启用。
- **Nature Skills**：更贴近中文科研用户的论文生产流程。19 个可触发技能覆盖绘图、润色、写作、模拟审稿、引用、全文 reader、PPT、返修、文献检索/下载、实验日志和 proposal；其中部分仍标为 Draft/Beta。`nature-academic-search` 需要单独的 MCP/Python 依赖，PubMed 要求邮箱，Scopus/ScienceDirect 等可选来源需要本机凭据。
- **Orchestra**：面向 AI/ML 研究工程，而非一般学科文献库。98 个 Skill 覆盖模型架构、微调、后训练、分布式训练、推理、评测、RAG、MLOps、multimodal、研究构思和论文写作。Skill 文档本身可直接阅读，但实际框架、GPU 云或托管服务仍各有依赖和账号要求。
- **Claude Scholar**：不是单纯 Skill 合集，而是 skills、agents、commands、hooks、rules 和模板组成的研究工作区。适合计算机/AI 课题的选题、Zotero 文献管理、实验分析、写作和返修；主分支以 Claude Code 为主，Codex 使用单独分支/配置，不能把主分支配置不加审查地覆盖到现有环境。
- **PaperSpine**：专注“贡献优先、结果验证贡献、面向审稿人”的论文论证结构。V4 用一个 orchestrator 路由 12 阶段，并生成可审计中间产物；适合已有稿件重写或从素材构筑论文，不是文献数据库，也不能绕过付费墙。仓库同时带 V5 RC，正式使用前应明确选择稳定 V4 还是候选版。
- **AERS**：主要面向经济学、政治学、社会学、教育、心理等社会科学实证研究，包含 Python/Stata/R、因果推断、稳健性、复现、写作和投稿流水线。仓库简介的“23,000+”不是当前 canonical catalog 数；本地 `catalog/skills.json` 的权威口径是 76 个合集、1,096 项。大量内容来自第三方项目，根目录 CC BY-SA 4.0 不能替代每个上游组件自己的许可证审查。
- **Multi Search Engine**：标题宣称 17 个引擎，实际列出 7 个中文和 9 个国际引擎，共 16 个。当前上游目录只有没有 YAML frontmatter 的 `SKILL.md`，其声明的 `config.json` 返回 404，也没有 URL 编码、抓取、解析、并发、去重或排序代码；因此只把它作为查询模板设计参考保存。

### 验证边界

- 四个新仓库均使用 `--depth 1` 浅克隆；适合本地搜索和读取当前版本，不包含完整提交历史。
- AERS 是已有完整仓库的快进更新，唯一子模块 `skills/69-Paper-WorkFlow` 已按父仓库 gitlink 固定到 `110e7c6`，父仓库工作树干净。
- 四个新仓库与已更新 AERS 合计 1,332 份 `SKILL.md`，均以 YAML frontmatter 开头；独立保存的 Multi Search Engine 是唯一例外，已在本地说明中明确标记。
- 本批未运行需要 Python/R/Stata、LaTeX、浏览器、GPU 或外部数据库的功能测试，也未安装依赖、写入全局配置或提交外部任务。
