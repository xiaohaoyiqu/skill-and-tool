# Multi Search Engine 本地快照说明

- 上游仓库：<https://github.com/aAAaqwq/AGI-Super-Team>
- 上游路径：`skills/multi-search-engine/SKILL.md`
- 获取日期：2026-08-28
- 保存方式：只保存单个 Skill，不克隆包含数百项内容的父仓库。
- 许可证：父仓库标示为 MIT；使用前仍应核对目标版本的许可证文件。

## 审计结论

- 标题宣称 17 个搜索引擎，正文实际列出 7 个中文引擎和 9 个国际引擎，共 16 个。
- 当前上游目录只有 `SKILL.md`。其中引用的 `config.json` 不在目录中，原始文件地址返回 404，因此本地没有伪造该文件。
- 当前文件没有 YAML frontmatter，也没有脚本、结果解析、并发查询、去重或排序实现。
- 它应被视为搜索 URL 模板的说明/路由参考，而不是可直接执行的元搜索聚合器，也没有安装到全局 Codex skills。
