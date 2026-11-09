# 项目与文件兼容性

SKLIB 管理本地资料的索引、来源和个人记录。下面的“识别”表示静态发现与读取；不会据此判断项目已经能在当前机器编译或运行。

后续已增加 [来源检测与快照恢复](SOURCES_AND_RESTORE.md)：识别规则与索引一致；快照 CLI 支持 UTF-8 和带 BOM 的 UTF-16/UTF-32，界面支持 UTF-8/UTF-16。宿主配置与真实模型验收另见 [HOST_AND_MODEL_ACCEPTANCE.md](HOST_AND_MODEL_ACCEPTANCE.md)。

## 项目类型

项目清单即使没有 README 也会被索引；嵌套包独立发现，适用于多包仓库。同一项目可以有多个清单和 README，数量表示资料条目数，不等于项目数。不同项目中相同内容的清单保留独立搜索结果，技能的相同内容副本仍折叠。

| 程序类型 | 发现依据 | 元数据读取范围 |
|---|---|---|
| JavaScript / TypeScript | package.json、deno.json、deno.jsonc | 标准 JSON 的 name/description；JSONC 只识别、读取原文 |
| Python | pyproject.toml、setup.cfg、setup.py | project / tool.poetry、setup.cfg metadata；setup.py 仅识别与读取 |
| Rust | Cargo.toml | package 表中的静态 name/description；工作区继承不求值 |
| Go | go.mod、go.work | go.mod module；工作区原文 |
| Java / Kotlin / JVM | pom.xml、build.gradle、build.gradle.kts | Maven 项目直属 name/artifactId/description；Gradle 原文 |
| .NET | csproj、fsproj、vbproj、sln、slnx | XML 中的 PackageId/AssemblyName/Description/TargetFramework(s)；解决方案保留原文 |
| C / C++ | CMakeLists.txt、vcxproj | CMake project 的直接文本、MSBuild 的静态文本；不展开变量 |
| PHP | composer.json | name/description |
| Dart / Flutter | pubspec.yaml | 静态 name/description |
| Ruby | Gemfile | 类型识别与原文 |
| Swift | Package.swift | 类型识别与原文 |

可用 `search --kind project --project-type python` 筛选。CLI、HTTP、MCP 的 `project_type` 与手动界面的程序类型筛选一致。README 自身不推断语言；类型筛选针对被清单识别的条目。

README 支持无扩展名、MD/Markdown/MDX、RST、TXT、AsciiDoc 及 README.zh-CN.md 等语言后缀。默认在来源根、直接子目录、Git 仓库根和含项目清单的目录识别 README。`--include-docs` 扩展到其他同类文档。

## 文件读取

| 文件 | 处理方式 |
|---|---|
| SKILL.md | 索引指令与 YAML 元数据；小写或混合大小写文件名可收录，并提示使用标准名称 |
| 文档、源代码、脚本、JSON/YAML/TOML/XML、CSV 等 | 技能配套文件按需分页读取；代码作为文本显示 |
| SVG、Notebook | 读取文本表示，不渲染 SVG、不运行 Notebook |
| PNG/JPEG 等图片、PDF/Office、音视频、压缩包、模型/数据库、EXE/DLL 等 | 配套文件清单提供类型、字节大小和是否可文本读取；二进制只列信息 |
| 未知扩展名 | 尝试严格文本解码，实际为二进制或包含非法控制字符时拒绝 |

`get_skill` 的 `files` 字符串清单保持可用，新增 `file_details` 提供分类。`text_readable` 是依据扩展名和大小给出的读取能力；实际读取还检查编码、内容、链接与权限。每次读取最多 2 MiB；清单最多 256 项、2000 个目录、深度 20，并报告截断。

项目清单和普通文档只允许读取其自身。技能可以读取包内符合规则的配套文本；隐藏路径、默认排除的依赖/构建目录、路径越界、目录链接和 Windows reparse point 均不会成为文件读取入口。

默认排除 `.git`、node_modules、虚拟环境、target/dist/build、bin/obj、vendor、.gradle、.dart_tool、Pods、DerivedData、测试夹具等。来源发现保留 `.agents` 等技能目录；资源清单不进入隐藏目录。额外 `--exclude` 用于来源扫描，可通过 `--clear-excludes` 清空额外配置。默认规则中的同名目录也会跳过，必要时应选择更具体的来源根。

## 编码与路径

自动模式先识别 UTF-32/UTF-16/UTF-8 BOM；无 BOM 默认严格 UTF-8。没有 BOM 的 UTF-16/32 不猜测。UTF-8 解码失败时，可显式选择 GB18030（兼容常见 GBK 文本）、Windows-1252 或 Shift-JIS 回退；不会用替换字符掩盖损坏内容。选择旧编码时仍优先识别 UTF 和 BOM，允许同一来源混合新旧文本。

```powershell
python -m sklib index E:\materials --encoding gb18030 --include-docs
# 未指定选项时沿用此来源上次成功登记的设置。
python -m sklib index E:\materials
python -m sklib read <id> references/old.txt --encoding gb18030
python -m sklib index E:\materials --no-include-docs --clear-excludes
```

编码选项、文档范围、扫描数量/深度和额外排除目录保存到来源设置，并随记录快照导出。修改编码会重新解码未改大小/时间的文件；读取失败保留原索引，但会持续报告失败，直到文件或设置修正。`verify` 是本次扫描动作，不作为常驻设置。

读取得到的正文保留 CRLF/LF/CR。分页和检索证据采用实际换行，U+2028 等 Unicode 字符不会多算一行。内容哈希继续归一化 CRLF/LF。

中文、空格及引号目录与 Windows 反斜杠资源路径已加入测试。绝对资源路径、`..`、盘符/NTFS 流语法被拒绝。长路径、UNC、大小写敏感 NTFS 目录和网络盘的行为尚未单独实测。

## 依赖与边界

Python 3.10 的 TOML 元数据解析使用声明的 `tomli>=2,<3`；Python 3.11+ 使用标准库 tomllib。未装 tomli 的源码环境仍能发现和检索原文，但返回元数据警告；补齐依赖后再次扫描会刷新元数据。动态配置表达式、Gradle、Ruby、Swift 及 setup.py 不进行求值；目标框架字段表示文件声明，不是已验证的运行条件。

本轮没有安装或运行这些项目的编译器、依赖和程序。当前也没有 PDF/Office 正文抽取、压缩包解包、图片 OCR 或任意源代码全文索引；二进制文件信息来自技能资源清单。

实现参考各格式的一手文档：[npm package.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-json)、[Python pyproject.toml](https://packaging.python.org/en/latest/specifications/pyproject-toml/)、[Cargo manifest](https://doc.rust-lang.org/cargo/reference/manifest.html)、[Go modules](https://go.dev/ref/mod)、[Maven POM](https://maven.apache.org/pom.html)、[.NET SDK](https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview)、[Composer](https://getcomposer.org/doc/04-schema.md)、[Dart pubspec](https://dart.dev/tools/pub/pubspec)。Windows 文本编码处理参考 [PowerShell 字符编码说明](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)，解码行为参考 [Python codecs](https://docs.python.org/3/library/codecs.html)。
