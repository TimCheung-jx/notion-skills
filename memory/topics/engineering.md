# 跨项目工程经验

> 自动装载层 `.claude/rules/04-MEMORY.md` 的 Technical Knowledge 只留规则与指针，案例放这里。
> 最后更新：2026-09-26

---

<a id="docx"></a>
## DOCX / Office 文档生成（2026-04-26）

当时用 `docx` npm 包程序化生成文档。踩出来的模式：

- 表格单元格里塞复选框
- 颜色编码的风险标签
- 页眉 / 页脚

反向转换（DOCX → Markdown）需要自己解 DOCX 的 zip 结构做 XML 解析。

**现状**：工作区已装 `docx` / `pptx` / `xlsx` / `officecli` / `pdf` 等 skill，
手搓 npm 脚本的做法已经过时，新活直接走 skill。

<a id="claude-desktop"></a>
## Claude Desktop vs MyAgents（第三方 Provider，2026-05-11）

起因：想让 Claude Desktop 走第三方 Provider。

- **Claude Desktop 的模型选择器是硬编码的** —— 即使 `anthropic.baseUrl` 指向第三方端点，
  也只显示 Anthropic 官方模型。
- **Claude Desktop Tasks（Agent 模式）需要单独装 `claude` CLI**
  （`npm install -g @anthropic-ai/claude-code`）。
  报 `Host Claude Code binary not available` 是缺 CLI，不是 Provider 配置问题。
- **Claude Code CLI 支持第三方 Provider**：
  `ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic` + `ANTHROPIC_AUTH_TOKEN=sk-xxx`
- **DeepSeek 的 Anthropic 兼容端点** `https://api.deepseek.com/anthropic`：
  基础对话可用，**tool use 支持有限**。
- **结论**：要「桌面 GUI + 第三方 Provider」就用 MyAgents；
  Claude Desktop 本质是 Anthropic 原生体验，别硬掰。
