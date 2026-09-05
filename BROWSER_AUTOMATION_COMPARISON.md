# 浏览器自动化、网页快照与截图理解工具对比

**核查时间**: 2026-08-29

**核查范围**: `E:\aimodel` 根目录中与浏览器控制、网页结构抽取、截图捕获或图像理解直接相关的主要仓库和 Skill

**新增重点**: [huangruiteng/loopx](https://github.com/huangruiteng/loopx)、[citrolabs/ego-lite](https://github.com/citrolabs/ego-lite)

## 先分清三种能力

| 能力 | 输入/输出 | 能解决什么 | 不能自动代表什么 |
|------|-----------|------------|------------------|
| 浏览器控制 | URL、点击、输入、滚动、网络请求 | 操作真实网页、测试交互、使用登录态 | 不一定理解页面视觉效果 |
| 语义网页快照 | DOM 或无障碍树转成文本和元素引用 | 低 token 定位按钮、表单、文本和链接 | 不是 PNG/JPEG，也不是 OCR 或视觉模型 |
| 像素截图理解 | 截图交给多模态模型/OCR | 识别画布、图表、图片文字、布局和视觉缺陷 | 通常不能单独点击或填写网页 |

许多项目同时提供“语义快照”和“保存截图”，但“能截图”不等于“能理解截图”。截图文件仍需交给支持图像输入的模型或 `vision-analysis` 一类工具分析。

## 两个新增仓库的定位

### LoopX

- 本地目录: `E:\aimodel\loopx\`
- 本地快照: `e2275510`，浅克隆，工作树干净并与 `origin/main` 一致。
- 定位: 面向长周期 Agent 工作的本地优先控制平面，保存 goal、todo、gate、evidence、quota、handoff 和恢复状态。
- 兼容面: Codex App/CLI、Claude Code、Cursor、Pi、OpenCode、DeepSeek Harness 及自定义 runner。
- 技术边界: 它不负责解析网页、截图或驱动浏览器；可放在浏览器工具上层，管理跨轮次任务、人工确认和证据回写。
- 本地核实: Python `>=3.11`，项目版本 `0.5.3`，核心包无运行时第三方依赖；9 份物理 `SKILL.md`，其中 8 份位于正式 `skills/`，1 份属于 auto-research demo。
- 许可: 当前版本 Apache-2.0；项目保留旧版本 MIT 许可文本。
- 当前 Windows 结论: 上游说明支持原生 PowerShell 7 安装，但本轮只保存源码，没有安装 PyPI 包、workflow skills 或创建 `.loopx` 状态。

### ego-lite

- 本地目录: `E:\aimodel\ego-lite\`
- 本地快照: `5ca3c36c`，浅克隆，工作树干净并与 `origin/main` 一致。
- 定位: 为人和外部 AI Agent 共用而设计的 Chromium 浏览器；每个 Agent 在隔离的 Space 中工作，可继承迁移后的 Chrome 登录态而不抢用户标签页。
- 开源范围: 仓库包含 MIT 许可的 `ego-browser` TypeScript/CDP harness 和 1 个 `ego-browser` Skill；真正提供 `globalThis.ego` bindings 的 ego lite 浏览器应用不在本仓库源码内。
- 观察方式: 默认让模型读取带元素引用和稳定 locator 的语义 Snapshot；另可通过 CDP 保存整页、视口或元素截图。
- 执行方式: Agent 在一次 JavaScript 脚本中组合 `snapshot`、`click`、`fill`、`wait`、`navigate`、`screenshot` 等函数，减少逐条 CLI 往返。
- 视觉边界: 仓库没有内置 OCR/多模态视觉模型。对 canvas、图片文字、图表或纯视觉布局，仍需把截图交给图像理解工具。
- 平台边界: 上游当前明确仅提供 macOS 应用，Windows/Linux 仍在 roadmap。本机是 Windows，因此本轮只能保存和审阅源码，不能完成浏览器应用安装或端到端实测。
- 证据边界: README 中“最高质量 Snapshot”“最高 2.5 倍”等是项目方陈述；本轮未在 Windows 上复现实验，不作为独立验证结论。

## 与根目录现有工具对比

| 项目 / Skill | 主要观察面 | 截图 | 登录态与隔离 | 最适合 | 当前主要限制 |
|------|------|------|------|------|------|
| `ego-lite` / `ego-browser` | 内核提供的语义 Snapshot、refs、稳定 locator | 支持捕获；不内置视觉理解 | 可迁移 Chrome 数据；每任务独立 Space | 外部 Agent 并行操作已登录网页，减少标签页冲突 | 浏览器应用当前仅 macOS；核心浏览器不是本仓库开源代码 |
| `browser-use` | 优先 AX tree，必要时 DOM/CDP，视觉页面再截图 | 支持，作为回退 | 可连本地 Chrome；云浏览器可隔离并行 | 通用 Agent 浏览器自动化、本地或云端任务 | 本地 Chrome 并行任务会争用；云端涉及外部服务和计费边界 |
| `chrome-devtools-mcp` | `take_snapshot` 基于 a11y tree，元素 UID | 页面/元素/整页截图 | 可启动或连接 Chrome；隔离取决于启动配置 | Web 调试、console/network/performance/Lighthouse、交互验证 | 偏开发诊断；不是图像 OCR；默认使用统计需按隐私要求关闭 |
| `OpenCLI` / `opencli-browser` | 默认裁剪 DOM snapshot，也有 AX source；网络响应和站点 adapter | 有，但 Skill 明确只在 CAPTCHA/图表等视觉页使用 | Browser Bridge 连接登录中的 Chrome profile | 已登录站点办事、可复用确定性 adapter、结构化抽取 | 扩展和 daemon 配置较多；直接使用日常登录态，授权边界要谨慎 |
| `web-access` | WebSearch/WebFetch/Jina 与 CDP/DOM 策略组合 | 页面截图、视频截帧 | 直连 Chrome/Edge 日常浏览器；tab 级管理 | 跨平台联网路由、内部站点、动态页和媒体提取 | 是 Skill 驱动的工具组合，不提供 ego 式独立浏览器 Space |
| `nanobrowser` | Chrome 扩展内的 Planner/Navigator Agent 读取页面状态 | 不是本次核查的核心接口 | 运行在用户 Chrome/Edge；本地保存凭据 | 想直接在浏览器侧使用自带多 Agent UI | 更像独立浏览器 Agent 产品，不是给 Codex/Claude 调用的通用外部 Skill/CLI |
| Playwright `webapp-testing` Skill | DOM、locator、浏览器日志；截图用于前后对比 | 支持 | 通常启动隔离的 headless Chromium | 本地 Web App 功能测试和视觉回归证据 | 不主打复用用户登录态或通用网站办事；截图理解依赖宿主模型 |
| `crawl4ai` | HTML/Markdown、结构化抽取、动态渲染 | 抓取时可保存 | 支持持久 profile、managed browser 和 CDP | 批量网页采集、RAG 语料和内容清洗 | 重点是 crawl/extract，不是高交互桌面 Agent |
| MiniMax `vision-analysis` Skill | 直接分析图片像素：OCR、UI review、chart、object | 它消费截图，不操作浏览器 | 无浏览器会话 | 真正理解网页截图、图表、canvas 和图片文字 | 需要 MiniMax Token Plan/MCP/API key；必须与截图来源工具组合 |

补充说明：`agent-skills/skills/browser-testing-with-devtools` 是围绕 Chrome DevTools MCP 的测试方法 Skill；`anthropic-skills` 与 `codex-skills` 中的 `webapp-testing` 是同类 Playwright Skill 副本，不应重复计作三种不同底层引擎。

## 当前 Windows 环境的选型建议

1. **已登录网站办事**：优先评估 `OpenCLI`；需要更自由的 CDP 脚本或联网策略时评估 `web-access` / `browser-use`。三者都会触达登录态，实际操作前应确认账号、写操作和隐私边界。
2. **本地网页开发调试**：`chrome-devtools-mcp` + `browser-testing-with-devtools`。它的 console、network、performance、a11y 和 screenshot 证据面比纯点击工具完整。
3. **大批量网页转 Markdown/结构化数据**：`crawl4ai`；站点有稳定业务接口时，优先使用 `OpenCLI` adapter 或网络响应抽取。
4. **真正解析截图像素**：先由任一浏览器工具捕获截图，再交给宿主多模态能力或 `vision-analysis`。不要把 DOM/a11y Snapshot 当成截图 OCR。
5. **隔离并行浏览器任务**：当前 Windows 上可用 `browser-use` 云浏览器等方案；`ego-lite` 的 Space 设计值得保留观察，但要等 Windows 版本后再实测。
6. **跨小时/跨天持续任务**：用 `LoopX` 管 goal、gate、evidence 和恢复，让上面任一浏览器工具作为执行层；LoopX 不替代浏览器工具。

## 安全与验证边界

- 不默认接管用户日常浏览器或迁移 Chrome 数据；这会扩大 Agent 可访问的账号和隐私范围。
- 对发帖、下单、转账、删除、提交表单等外部写操作保留显式确认和结果回读。
- 语义 Snapshot 对标准 DOM/无障碍信息最有效；canvas、远程桌面、验证码、图表和纯图片内容必须走像素视觉路径。
- 本轮只完成源码浅克隆、静态审阅和台账记录，没有安装依赖、浏览器扩展、MCP、全局 Skill，也没有启动或登录任何浏览器。

## 本地核查入口

| 主题 | 主要文件 |
|------|----------|
| LoopX 定位、安装与边界 | `loopx/README.md`、`loopx/README.zh-CN.md`、`loopx/pyproject.toml`、`loopx/skills/` |
| ego-lite 开源边界与使用方式 | `ego-lite/README.md`、`ego-lite/AGENTS.md`、`ego-lite/skills/ego-browser/SKILL.md`、`ego-lite/package/ego-browser/src/driver/observe.ts` |
| Browser Use AX/screenshot 策略 | `browser-use/skills/browser-use/SKILL.md` |
| Chrome DevTools snapshot/screenshot 定义 | `chrome-devtools-mcp/docs/tool-reference.md`、`agent-skills/skills/browser-testing-with-devtools/SKILL.md` |
| OpenCLI DOM/AX/登录态策略 | `OpenCLI/README.md`、`OpenCLI/skills/opencli-browser/SKILL.md`、`OpenCLI/src/browser/dom-snapshot.ts`、`OpenCLI/src/browser/ax-snapshot.ts` |
| Web Access CDP 与截图能力 | `web-access/README.md` |
| Nanobrowser 产品形态 | `nanobrowser/README.md` |
| Playwright 本地 Web 测试 | `anthropic-skills/skills/webapp-testing/SKILL.md`、`codex-skills/awesome-codex-skills/webapp-testing/SKILL.md` |
| Crawl4AI 内容抽取与截图 | `crawl4ai/README.md` |
| 像素图像理解 | `minimax-skills/skills/vision-analysis/SKILL.md` |
