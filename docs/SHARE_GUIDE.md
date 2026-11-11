# AI Skills 和工具分享清单

整理于 2026 年 11 月 11 日。

平时收集的 AI Skills、开发工具和研究资料，按用途放在这里。每项都附上项目链接和简短介绍，找写作、编程、做界面或读论文的工具，可以直接跳到对应分类。

共收录 131 个不同的项目来源。Skill 通常是一组让 AI 按特定方法工作的说明，有些会附带脚本；组件库、桌面应用和模型项目则需要按各自说明使用。链接指向项目来源，具体安装方式、依赖与许可请查看项目 README。

## 中文写作与改稿

这几项侧重点不同。写新稿可以看 human-writing，中文逐句修改可以看 Humanizer-zh；技术说明、小说等不同文体的处理，可以再看 sepia。

| 项目 | 介绍 |
|------|------|
| [human-writing](https://github.com/KKKKhazix/human-writing) | 通用中文写作与改稿 Skill，覆盖文章、评论、教程和故事。强调具体材料、自然语气，适合把想法写成别人愿意读下去的文字。 |
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 中文文字编辑 Skill，检查夸张表述、套话、重复句式和生硬衔接，适合已有初稿后的逐句修改。 |
| [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | 检查并改写常见的 AI 写作模式，可只给诊断，也可修改原文，适合审阅文章和日常文案。 |
| [no-ai-slop](https://github.com/petergyang/no-ai-slop) | 清理套路化句式，同时尽量保留作者原有的用词和节奏，适合不想把文章改成统一口气的人。 |
| [sepia](https://github.com/Nanako0129/sepia) | 按文体处理写作问题，涉及小说叙事，也覆盖发布说明、技术文章和 PR 回复等专业文字。 |

## 通用 Skills 与开发方法

想了解 Skill 长什么样，可以先看 Anthropic Skills。已有项目需要补设计、测试和审查流程，可以从具体任务挑选，按需使用。

| 项目 | 介绍 |
|------|------|
| [Anthropic Skills](https://github.com/anthropics/skills) | Anthropic 的官方 Skill 示例，包含文档、设计及其他工作任务，可用来了解 Skill 的组织方式。 |
| [agent-skills](https://github.com/addyosmani/agent-skills) | 面向软件开发的工程 Skills，涉及需求、实现、验证和交付，适合给编码 Agent 补充工作规范。 |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | 一组可组合的工程 Skills，适合处理需求梳理、设计审查、测试和重构等具体任务。 |
| [Superpowers](https://github.com/obra/superpowers) | 把讨论需求、制定计划、测试和验证串起来的软件开发工作流，适合需要持续推进的编码任务。 |
| [ECC](https://github.com/affaan-m/ECC) | 较完整的 Agent 配置集合，包含 Skills、规则、hooks 和记忆相关方案，适合研究如何组织编码助手的工作环境。 |
| [agent-rules-books](https://github.com/ciembor/agent-rules-books) | 从软件工程书籍整理出的规则和 Skills，涉及代码质量、重构、架构及领域建模。 |
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 受 Karpathy 编码观察启发的行为指南，重点是确认假设、控制改动范围和避免过度设计；属于社区整理。 |
| [Karpathy Guides 中文版](https://github.com/vtroisWhite/andrej-karpathy-skills) | 另一份 Karpathy 风格指南及其维护版本，可与上一项对照阅读，关注编码助手的日常行为约束。 |
| [khazix-skills](https://github.com/KKKKhazix/khazix-skills) | 中文实用 Skills 集合，涉及目标梳理、研究、资讯、写作和文档维护等任务，可按目录挑选。 |
| [z-skills](https://github.com/tjxj/z-skills) | 面向中文内容与资料处理的 Skills，涉及网页采集、文档解析、表格和 Markdown 导出等工作。 |
| [MiniMax Skills](https://github.com/MiniMax-AI/skills) | 包含前端、移动端、文档及多媒体相关的任务指导，部分能力需要配合模型或外部服务。 |
| [knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Anthropic 的岗位工作插件集合，把某类工作的 Skills 与工具接入组织在一起，适合参考团队工作流。 |
| [awesome-agent-skills](https://github.com/JackyST0/awesome-agent-skills) | Agent Skills 的发现与导航清单，适合按关键词寻找具体能力。 |
| [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Claude Skills、相关工具和资料的分类清单，适合查找用例和扩展方向。 |
| [claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | Anthropic 的代码示例与开发指南，适合参考模型调用、工具使用及应用实现方式。 |
| [Caveman](https://github.com/JuliusBrussee/caveman) | 约束编码助手输出篇幅的 Skill，适合希望回答更简短、减少冗长说明的工作方式。 |
| [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | LLM 应用、Agent 和 RAG 示例集合，适合寻找原型思路并阅读实现。 |

## Skills 评测与检查

| 项目 | 介绍 |
|------|------|
| [skill-up](https://github.com/alibaba/skill-up) | 用声明式用例评测 Skill、Agent 和工作目录变更，可对比使用前后的表现，适合检查一项 Skill 是否解决了问题。 |
| [skillspector](https://github.com/NVIDIA/skillspector) | 检查 Agent Skills 中的可疑模式和安全风险，适合在阅读或引入第三方 Skill 时辅助审查。 |
| [skills-compat-manager](https://github.com/hnaymyh123-henry/skills-compat-manager) | 管理不同 Agent 共用的 Skill 库，并在执行前检查兼容条件，适合在多个工具之间维护同一组 Skills。 |

## 前端界面与设计

设计指导和组件源码在这里分开看。前者帮助决定布局、字体和交互，后者提供可以直接阅读、复制或调整的实现。

| 项目 | 介绍 |
|------|------|
| [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 面向界面设计与实现的 Skill，提供风格、配色、排版和交互方面的参考，适合从需求开始搭页面。 |
| [taste-skill](https://github.com/Leonxlnx/taste-skill) | 面向 AI 生成界面的设计指导，关注布局、视觉层次与交互细节，适合改善模板感较强的页面。 |
| [hallmark](https://github.com/Nutlope/hallmark) | 提供新建界面、审查、重做和设计研究等工作方式，适合给不同内容选择不同的页面结构。 |
| [Refactoring UI Skill](https://github.com/opkod-france/claude-skill-refactoring-ui) | 将部分 Refactoring UI 设计原则用于界面修改。旧仓库已归档，后续可查看 [OPKOD 插件仓库](https://github.com/opkod-france/opkod-claude-code-plugins)；原书仍需单独阅读。 |
| [emilkowalski-skills](https://github.com/emilkowalski/skills) | 面向设计师与工程师的界面 Skills，重点包含动效及设计判断，适合打磨已有页面的细节。 |
| [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | 从不同网站整理的 DESIGN.md 设计分析，适合寻找视觉参考、理解配色和排版规则。 |
| [developer-portfolios](https://github.com/emmabostian/developer-portfolios) | 开发者个人网站的参考链接，适合准备作品集或个人主页时寻找案例。 |
| [inspira-ui](https://github.com/rahulv-official/inspira-ui) | Vue 与 Nuxt 的界面组件集合，适合查看带动效和视觉表现的组件实现。 |
| [rare-ui](https://github.com/swamimalode07/rare-ui) | 基于 shadcn 使用方式组织的组件与动画集合，可把源码放进自己的项目后继续修改。 |
| [shadcn-ui](https://github.com/shadcn-ui/ui) | 可定制的界面组件源码与组织方式，适合搭建自己的组件库。 |
| [beautiful-ui](https://github.com/slev12397/beautiful-ui) | 面向 AI 应用的界面组件，包含推理状态、流式回答、工具调用和任务状态等常见展示。 |
| [beui](https://github.com/starc007/ui-components) | React 与 Next.js 的动效组件集合，采用复制源码的使用方式，适合按项目需要调整。 |
| [transitions-dev](https://github.com/Jakubantalik/transitions.dev) | 可交互查看的 CSS 过渡效果集合，提供可复制片段，适合补充按钮、卡片等交互细节。 |
| [Vue Skills](https://github.com/vuejs-ai/skills) | Vue 3 开发 Skills，整理常见问题和开发指导，适合 Vue 项目的实现与代码检查。 |
| [vue-tui](https://github.com/Simon-He95/vue-tui) | Vue 3 终端界面工具，可用于浏览器终端风格页面、命令行界面和相关测试。 |
| [playcaptcha](https://github.com/mortspace/playcaptcha) | 以抓娃娃交互实现的验证码实验，适合学习动画、交互状态与 React 实现。 |
| [open-design](https://github.com/nexu-io/open-design) | 面向原型、演示和视觉内容的 AI 设计工具，适合研究用 Agent 完成设计任务的流程。 |

## 浏览器与联网工具

| 项目 | 介绍 |
|------|------|
| [browser-use](https://github.com/browser-use/browser-use) | 让 Agent 操作浏览器，完成导航、点击、填写和信息提取等任务。 |
| [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 将 Chrome DevTools 的浏览器检查、调试和性能分析能力提供给编码助手。 |
| [crawl4ai](https://github.com/unclecode/crawl4ai) | 面向网页采集与内容抽取的工具，适合把网页整理为供后续处理的文本或结构化内容。 |
| [OpenCLI](https://github.com/jackwener/OpenCLI) | 用命令行接口组织网站操作，也提供浏览器自动化能力，适合把重复的网页任务整理成命令。 |
| [Agent-Reach](https://github.com/Panniantong/Agent-Reach) | 为 Agent 接入不同互联网内容来源提供安装与检查方案，适合研究多平台资料获取。 |
| [web-access](https://github.com/eze-is/web-access) | 联网策略与浏览器操作 Skill，结合检索、网页读取和 CDP 操作处理联网任务。 |
| [ego-lite](https://github.com/citrolabs/ego-lite) | 围绕人与 Agent 共同使用浏览器设计的项目，关注独立任务空间；使用前先看当前平台支持。 |
| [nanobrowser](https://github.com/nanobrowser/nanobrowser) | 浏览器扩展形态的网页自动化项目，适合研究在浏览器内让 Agent 执行操作的方式。 |

## Agent 应用与任务管理

| 项目 | 介绍 |
|------|------|
| [goose](https://github.com/aaif-goose/goose) | 在本机运行的通用 Agent，提供桌面、命令行及 API 等使用方式，可接入不同模型与工具。 |
| [pi](https://github.com/earendil-works/pi) | Agent 开发与运行工具集合，包含编码 Agent、模型接口和运行时，适合研究或扩展自己的 Agent。 |
| [openwork](https://github.com/different-ai/openwork) | 用于组织和共享 AI 工作流的应用，围绕 Skills、MCP 和服务连接来复用任务能力。 |
| [pisper](https://github.com/ling-kong-ran/pisper) | 跨桌面、终端与手机的多 Agent 应用，支持分支会话、工具、记忆和工作流管理。 |
| [LoopX](https://github.com/loopx-project/loopx) | 为跨轮次任务保存目标、状态和证据，关注任务恢复、交接与人工参与，适合研究长任务管理。 |
| [headroom](https://github.com/headroomlabs-ai/headroom) | 在内容送入模型前压缩工具输出、日志和上下文，适合研究 Agent 的上下文管理与 token 开销。 |
| [context-mode](https://github.com/mksglu/context-mode) | 将工具的大段输出保存在本地，再通过 SQLite 全文检索取回所需片段，适合研究编码 Agent 的上下文管理；当前采用 Elastic-2.0 许可证。 |
| [OpenShell](https://github.com/NVIDIA/OpenShell) | NVIDIA 的 Agent 沙箱运行环境，按策略限制文件、进程和网络访问，适合研究 Agent 隔离与凭据管理；部署需另行准备系统环境。 |
| [ai-memory](https://github.com/akitaonrails/ai-memory) | 为编码 Agent 保存长期项目记忆，让不同工具之间能够交接任务。以 Git 管理的 Markdown 保存知识，适合需要跨会话继续工作的项目。 |
| [laya](https://github.com/NandhaKishorM/laya) | 对文本做分类、评分和是非决策的模型与 SDK，适合研究请求路由和结构化判断；模型权重需另行准备，上游速度数据未经本机验证。 |

## 科研与论文

| 项目 | 介绍 |
|------|------|
| [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 覆盖多学科科研任务的 Skills，涉及数据分析、实验与研究工具，可按研究领域挑选。 |
| [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 面向 AI 研究的 Skills 集合，涉及模型训练、实验和论文相关工作。 |
| [nature-skills](https://github.com/Yuan1z0825/nature-skills) | 科研工作流 Skills 集合，关注可复用的方法和研究产物，适合按具体任务查看。 |
| [claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | 面向学术研究与软件开发的助手配置，涉及文献、代码、实验分析和写作。 |
| [Awesome-Agent-Skills-for-Empirical-Research](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) | 实证研究 Skills 与资料合集，适合沿着研究阶段查找文献、分析和写作工具。 |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine) | 围绕研究贡献、目标期刊或会议组织论文写作，适合需要先理清论证再写稿的任务。 |
| [Paper2Any](https://github.com/OpenDCAI/Paper2Any) | 保留早期 Paper2Any 开源代码，适合研究论文材料与办公文档的转换；当前托管产品与仓库代码范围有区别。 |
| [SESA-Self-Evolving-Search-Agents](https://github.com/Zenghuang-Fu/SESA-Self-Evolving-Search-Agents) | 搜索 Agent 的自博弈研究代码，研究如何把失败经验整理为可复用的技能，偏实验与方法研究。 |
| [patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) | 辅助梳理技术方案、挖掘专利点和编写交底材料的 Skill，适合准备材料时参考。 |
| [timesfm](https://github.com/google-research/timesfm) | Google Research 的时间序列预测模型，适合预测实验与相关应用研究；不同版本的接口和权重条件有区别。 |

## 文档 图表与知识检索

| 项目 | 介绍 |
|------|------|
| [archify](https://github.com/tt-a1i/archify) | 把系统描述或代码关系整理成可交互的架构图，支持生成便于分享的独立图形与网页。 |
| [graphify](https://github.com/Graphify-Labs/graphify) | 从代码、文档等材料建立知识图谱，适合分析跨文件关系、模块联系与调用路径。 |
| [gortex](https://github.com/zzet/gortex) | 代码索引与关系查询引擎，提供命令行、MCP 和网页等入口，适合研究大型代码库。 |
| [Ix](https://github.com/ix-infrastructure/Ix) | 将代码符号、调用和导入关系保存为图，提供 CLI、MCP 和配套 Skill，适合分析调用链和改动影响；运行需要 Docker 后端。 |
| [zvec-grep](https://github.com/zvec-ai/zvec-grep) | 将关键词、BM25 和向量检索放在同一入口，适合既需要精确查找也需要语义搜索的资料库。 |
| [LEANN](https://github.com/StarTrail-org/LEANN) | 面向本地文档检索的向量索引项目，适合构建个人资料搜索与 RAG 应用。 |
| [liteparse](https://github.com/run-llama/liteparse) | 本地文档解析工具，关注文本位置与 PDF 内容抽取，适合为检索和资料处理准备输入。 |
| [pdf-inspector](https://github.com/firecrawl/pdf-inspector) | PDF 分类与文本提取工具，可区分文本和扫描等类型，帮助决定后续解析或 OCR 方式。 |
| [markdown-viewer-skills](https://github.com/markdown-viewer/skills) | 在 Markdown 中制作图表和可视化的 Skills，涉及技术图、数据图和信息图等。 |
| [mermaid-erd-generator](https://github.com/nharsch/mermaid-erd-generator) | 辅助生成 Mermaid 实体关系图，适合说明数据库表与业务实体之间的联系。 |
| [obsidian-skills](https://github.com/kepano/obsidian-skills) | 与 Obsidian 文件和工作方式配合的 Skills，涉及 Markdown、Canvas 和其他笔记结构。 |
| [kepano-obsidian](https://github.com/kepano/kepano-obsidian) | Obsidian 笔记库模板，适合参考个人知识库的目录与组织方式。 |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | 围绕近期话题检索社区和网络资料，适合了解某个主题最近被如何讨论。 |
| [effective-html](https://github.com/plannotator/effective-html) | 生成独立 HTML 产物的 Skills，适合线框图、交互原型与可分享的小工具。 |

## 代码审查 测试与工程工具

| 项目 | 介绍 |
|------|------|
| [open-code-review](https://github.com/alibaba/open-code-review) | 基于 Git 差异进行 AI 代码审查的命令行工具，可结合代码上下文输出具体问题。 |
| [Claude 官方插件目录](https://github.com/anthropics/claude-plugins-official) | 实际来源是 Anthropic 官方插件目录，代码审查只是其中一部分，也可用来查找其他插件。 |
| [ai-unit-tests-generator](https://github.com/gustavolopess/ai-unit-tests-generator) | 使用 AI 改进 TypeScript 仓库测试覆盖率的应用，适合研究测试生成和结果管理。 |
| [python-refactoring-skills](https://github.com/l-mb/python-refactoring-skills) | Python 代码分析与重构 Skills，涉及复杂度、质量和安全等问题。 |
| [SmeLLM](https://github.com/refactoring-assistant/SmeLLM) | 使用大模型识别代码坏味道并辅助重构的研究工具。 |
| [codetracer](https://github.com/metacraft-labs/codetracer) | 可记录执行轨迹的时间旅行调试器，适合回看程序执行过程和排查难复现问题。 |
| [skillsProject-AI-Log-Analyzer](https://github.com/sahanaydn/skillsProject-AI-Log-Analyzer) | 日志上传、分析与问答应用，适合研究如何把日志整理成可查询的故障信息。 |
| [mergration](https://github.com/38tter/mergration) | 从 Markdown 中的 Mermaid 实体关系图生成 Rails 数据库迁移文件。 |
| [scramble](https://github.com/dedoc/scramble) | 根据 Laravel 项目代码生成 OpenAPI 文档，适合减少接口说明与实现之间的重复维护。 |
| [pipeforge](https://github.com/Sheraz-k/pipeforge) | CI/CD 流水线生成工具，适合参考不同项目的持续集成与部署配置。 |
| [terraform](https://github.com/hashicorp/terraform) | 以配置文件管理基础设施的工具，适合研究环境的创建、变更与版本管理；使用条件查看对应版本许可。 |
| [OpenAuth](https://github.com/anomalyco/openauth) | 可自行托管的 OAuth 2.0 身份认证服务，适合参考多应用登录和身份提供方接入；仍处于 beta，用户管理由应用自行实现。 |

## 安全分析与逆向

这些项目面向代码检查、研究和已获授权的测试。具体安装、运行方式与适用范围各不相同。

| 项目 | 介绍 |
|------|------|
| [ghidra](https://github.com/NationalSecurityAgency/ghidra) | NSA 开源的逆向分析框架，提供反汇编、反编译与脚本能力，适合分析编译后的程序。 |
| [rea](https://github.com/morluto/rea) | 面向应用与二进制分析的逆向工具，提供 CLI 和 MCP 等接口，可结合多种分析工具工作。 |
| [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | 逆向、安全研究与授权测试的 Skill 路由集合，适合按任务查找分析方法与所需工具。 |
| [SafeGuard-Code-Profiler](https://github.com/hamed-kuheil/SafeGuard-Code-Profiler) | 对 C++、Java 和 Python 进行离线静态检查，关注性能、安全和隐私相关问题。 |
| [SupplyChainScanner](https://github.com/benjiamin911/SupplyChainScanner) | 面向软件依赖与供应链问题的检查工具，适合研究依赖混淆等风险。 |
| [WebSecurityScanner](https://github.com/Defensive-Alliance/WebSecurityScanner) | 检查常见 Web 漏洞的 Python 工具，涉及 SQL 注入、XSS 和敏感信息暴露等问题。 |

## 音频 视频与图像

| 项目 | 介绍 |
|------|------|
| [StemDeck](https://github.com/stemdeckapp/stemdeck) | 用 Demucs 在本机分离人声、鼓、贝斯等音轨，并提供独奏、循环、变速和变调练习界面；实际使用还需运行环境与模型。 |
| [openvid](https://github.com/CristianOlivera1/openvid) | 浏览器录屏和产品演示视频编辑器，支持缩放、设备样机及三维效果。采用 PolyForm Noncommercial 1.0.0；源码超过本轮限额，仅登记链接。 |
| [stt](https://github.com/jianchang512/stt) | 基于 faster-whisper 的本地音视频转文字工具，可输出纯文本、JSON 和带时间戳的字幕。 |
| [pocket-tts](https://github.com/kyutai-labs/pocket-tts) | 以 CPU 运行为重点的轻量文字转语音项目，适合研究本地语音生成。 |
| [LuxTTS](https://github.com/ysharma3501/LuxTTS) | 基于 ZipVoice 的文字转语音与声音克隆项目，使用参考音频生成语音，提供 GPU、CPU 和 Apple MPS 的运行示例。 |
| [supertonic](https://github.com/supertone-oss-archive/supertonic) | 轻量文字转语音项目，仓库已归档，适合参考实现；源码和模型的使用条件需分别查看。 |
| [VibeVoice](https://github.com/microsoft/VibeVoice) | 微软的语音项目，涉及语音生成与识别等不同方向，使用时需选择对应子项目和模型。 |
| [magenta-realtime](https://github.com/magenta/magenta-realtime) | 实时音乐生成项目，包含模型推理与应用示例，适合音乐交互和音频应用研究。 |
| [hyperframes](https://github.com/heygen-com/hyperframes) | 用 HTML、CSS 和媒体素材生成视频的框架，适合程序化动画与视频制作。 |
| [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | 用代码制作艺术风格动画和解说视频的 Skill，附风格配方、场景代码及检查脚本；渲染需准备 uv、FFmpeg 和 Playwright Chromium。 |
| [claude-video](https://github.com/bradautomates/claude-video) | 帮助 Agent 读取和理解视频内容的 Skill，适合整理视频资料与分析内容。 |
| [multi-style-image-generator](https://github.com/shengjidaguai-china/multi-style-image-generator) | 多风格图像与提示词工作流，涉及参考图重绘、全景图及空间效果等方向。 |
| [Ghost-Downloader-3](https://github.com/XiaoYouChR/Ghost-Downloader-3) | 多协议下载工具，适合查看下载任务管理、分块与媒体处理方面的实现。 |
| [kgka_Music_hl](https://github.com/umr-xiaomai/kgka_Music_hl) | Flutter 第三方音乐客户端，可参考跨平台界面、搜索、播放和歌词功能；项目说明限学习交流使用。 |
| [nginx-http-flv-module](https://github.com/winshining/nginx-http-flv-module) | Nginx 的流媒体模块，涉及 HTTP-FLV、RTMP 等能力，适合研究直播服务。 |
| [manim](https://github.com/3b1b/manim) | 3Blue1Brown 作者维护的数学动画引擎，适合程序化数学演示；与 Manim 社区版是不同项目。 |
| [blender-skills](https://github.com/arjun988/blender-skills) | 面向 Blender 的 Skills 集合，涉及建模、材质、灯光、动画和游戏引擎导出，通过 Blender MCP 配合 Agent 执行，适合三维资产制作。 |

## 学习资料与项目导航

| 项目 | 介绍 |
|------|------|
| [Hands-On Large Language Models](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) | 同名 O’Reilly 图书的官方示例代码，包含 12 章 Notebook，覆盖嵌入、Transformer、RAG、多模态和微调；运行需另备依赖与模型。 |
| [HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter) | 按成本、收益和证据整理健康、生活与办事资料，附正文查询 Skill；制度内容以中国大陆为背景。正文 CC BY 4.0，代码 MIT，实际决策需复核原始来源及当地现行规定。 |
| [up：人生进阶指南](https://github.com/byoungd/up) | 中英双语的终身学习书稿，涉及英语、AI、项目实践、创业和生活复盘，附工作表及 EPUB/PDF。正文 CC BY-NC 4.0，站点与构建代码 MIT。 |
| [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | 从零实现常见技术的教程合集，适合通过小型项目学习底层原理。 |
| [open-source-games](https://github.com/bobeff/open-source-games) | 开源游戏与部分重制项目的导航，适合寻找游戏源码和学习案例。 |
| [public-apis](https://github.com/public-apis/public-apis) | 按主题整理的公共 API 导航，适合寻找可用于应用原型与练习的数据接口。 |
| [daizhigev20](https://github.com/daizhige-org/daizhigev20) | 中国古典文献数据的修订项目，适合古籍检索、文本处理与相关研究。 |
| [fq-book](https://github.com/hoochanlon/fq-book) | 《这本书能让你连接互联网》的文档仓库，介绍代理、隧道、VPN 等网络原理，也整理相关工具配置与资料获取方法。 |

## 补充来源

以下四项也在收集范围内，其中包含嵌套保存的项目、单文件快照和仅记录链接的资料。

| 项目 | 介绍 |
|------|------|
| [System Design 101](https://github.com/ByteByteGoHq/system-design-101) | 系统设计图解和案例讲解，适合查阅架构概念；本地保存在 system-design 子目录。 |
| [Multi Search Engine](https://github.com/aAAaqwq/AGI-Super-Team/tree/main/skills/multi-search-engine) | Multi Search Engine 的来源目录，主要提供不同搜索引擎的查询 URL 模板；本地保留单文件快照。 |
| [handraw-style](https://github.com/yang0/handraw-style) | 手绘风格画廊和双语提示词参考，当前仅记录链接。 |
| [ebook-treasure-chest](https://github.com/jbiaojerry/ebook-treasure-chest) | 电子书相关链接导航，当前仅记录链接，具体内容的获取与使用条件需查看对应来源。 |

需要哪一类，就从那一类挑一两个项目看 README。模型、浏览器和桌面应用通常还要准备运行环境，Skill 也可能调用脚本或外部服务，先读清楚再按需使用。
