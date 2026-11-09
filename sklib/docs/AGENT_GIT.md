# 在 Agent 中使用 SKLIB 源码的 Git 功能

本机保留的独立开发仓库根目录是 E:/aimodel/sklib，默认分支 main。该工程同时以普通源码文件收录于 skill-and-tool 聚合仓库；从 GitHub 克隆聚合仓库时，Git 根目录是聚合仓库目录，应用源码位于其 sklib/ 子目录。以下“独立源码仓库”配置描述开发机状态。

## 让客户端选中正确仓库

使用本机独立源码仓库时，将 E:/aimodel/sklib 添加为本地项目文件夹，并将其设为主目录（Edit project → Make primary）。之后从该项目开启会话。主目录用于默认 Git 操作；PR 和 worktree 操作针对主仓库。使用从 GitHub 克隆的 skill-and-tool 时，应选择聚合仓库根目录进行提交，运行应用时再进入 sklib/；不需要在子目录再次初始化 Git。

使用 Codex CLI 时：

```powershell
codex --cd E:\aimodel\sklib
```

IDE 中打开 E:/aimodel/sklib；多根工作区中选它作为当前聊天的工作区根目录。

## 可以使用的功能

| 功能 | 使用方式或前提 |
|---|---|
| 查看改动 | 桌面 review/diff 面板，或让 Agent 执行 git status / git diff |
| 暂存与撤销 | review 面板按文件或片段处理；撤销前核对具体差异 |
| 本地提交 | 基于选定的暂存文件创建提交，可在 Git 历史中查看 |
| 分支 | 可让 Agent 为一项工作创建 codex/<任务名> 分支 |
| 工作树 | 从项目启动 worktree 会话，可与本地目录隔离；每棵工作树需要自己的依赖环境 |
| 推送 | 需要配置远程仓库和相应访问权限 |
| 创建 PR | 需要远程分支、对应托管服务及客户端认证；本地提交本身不需要远程服务 |

工作树通常从当前分支的 HEAD 创建；任务完成后可创建分支、提交，再推送。忽略的 .venv 不会由普通 Git checkout 带入新工作树，应按 README 在工作树内重新建立环境。

## 独立源码仓库的当前本机配置

- Git for Windows 已可用，提交身份沿用现有配置并写入源码仓库本地配置。
- 源码使用 LF 换行，.bat/.cmd 使用 CRLF，规则见根目录 .gitattributes。
- .gitignore 排除 .venv、.audit-client、.sklib、构建产物、Python 缓存及 .env；.env.example 可正常收录。
- Git Credential Manager 和 GitHub CLI 已安装。凭据管理器中存在 GitHub 账号记录，这不等于已经验证目标仓库的访问权限。
- 独立源码仓库尚未指定远程；聚合仓库的远端为 https://github.com/xiaohaoyiqu/skill-and-tool 。发布在聚合仓库完成，不需要给本机内层仓库绑定同一个远端。

仓库配置属于 Git；当前 Agent 的文件写入和网络访问还受其权限设置影响。本机的 Codex 配置使用 workspace-write 和 on-request，必要操作可能触发客户端的授权界面。Git 身份和仓库设置并不代替远程访问凭据。

检查命令：

```powershell
git -C E:\aimodel\sklib status
git -C E:\aimodel\sklib log --oneline -5
git -C E:\aimodel\sklib branch --show-current
git -C E:\aimodel\sklib worktree list
git -C E:\aimodel\sklib remote -v
```

官方说明：[OpenAI Docs：本地 Git 控件](https://learn.chatgpt.com/docs/environments/local-environment)、[项目主目录](https://learn.chatgpt.com/docs/projects)、[工作树](https://learn.chatgpt.com/docs/environments/git-worktrees)、[Review 面板](https://learn.chatgpt.com/docs/code-review)。
