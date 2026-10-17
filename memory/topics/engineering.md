# 跨项目工程经验

> 自动装载层 `.claude/rules/04-MEMORY.md` 的 Technical Knowledge 只留规则与指针，案例放这里。
> 最后更新：2026-10-17

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

<a id="codex"></a>
## Codex 桌面端 ≠ ChatGPT（2026-10-01）

- **`ChatGPT.app` 其实是 OpenAI Codex 桌面端**（bundle id `com.openai.codex`），不是 ChatGPT 本体。
  反直觉，别按名字猜 —— 2026-09-13 和 10-01 两次都差点绕进去。
- 8-04 被一个安装脚本改成了走 deepseek，原始配置备份在 `~/.codex/backup-deepseek/`
  （`manifest.txt` 就是那次改动的记录）。
- **10-01 回滚到官方订阅**（app 退出后改，改前全部备份）：
  - `~/.codex/config.toml`：删 `model` / `model_provider` / `model_catalog_json` /
    `forced_login_method`（`= "api"` 就是 UI 登录入口被锁死、点不回订阅的原因），
    `preferred_auth_method` 改 `"chatgpt"`，删 `[model_providers.deepseek]` 段，
    清掉 `shell_environment_policy` 里的 `ANTHROPIC_*`
  - `.codex-global-state.json`：清 `composer-recent-model-configurations-v1` 里的 deepseek 项
    （不清的话模型选择器还默认选它）
- **教训**：对共享 CODEX_HOME 跑 CLI 前先想清 auth 联动 —— 09-13 用 CLI 复现问题时被
  `forced_login_method="api"` 拦下，CLI 自动把 ChatGPT 登录态登出（`auth.json` 被删）。
- **遗留**：prompt-history 里有一条明文 deepseek key（8-04 Tim 自己贴进聊天框的），
  待撤销或清理 —— Tim 还没拍板。

<a id="myagents"></a>
## MyAgents 应用版本与「否定性结论」的时效（2026-10-07 molt 核验）

**版本脉络**（外部核验，[releases](https://github.com/hAcKlyc/MyAgents/releases)）：

| 版本 | 日期 | 相关 |
|---|---|---|
| 0.4.20 | 2026-09-19 | 09-22 排障时本机版本；#600 针对此版 |
| 0.4.21 | 2026-09-23 | **#600 修复随此版发布** |
| 0.4.22 | 2026-09-30 | 本机已落后两个版本 |

**#600 已修复**（[issue](https://github.com/hAcKlyc/MyAgents/issues/600)，2026-09-22 CLOSED）。
维护者回复要点：

- 根因不是"某次错误写入"，而是**旧 IM Bot 配置迁移路径按历史 `Agent.workspacePath` 认领 Agent，
  没有尊重其他 Project 已有的 `agentId` 归属**
- 修复：迁移统一走共享归属解析，不再抢占已认领的 Agent；
  「设置 → 聊天机器人」与「工作区 → Agent 设置」现在**会展示冲突双方的路径并允许明确选择保留谁**；
  CLI / 渠道启动错误保留真实冲突原因，不再静默返回空
- 提交 `04c421be`（`dev/0.4.21`），285 项测试通过

### 教训（这条比事件本身重要）

我在 09-22 的溯源里写下**"产品内无重绑/解绑入口"**——在当时（0.4.20）是对的。
**三天后 0.4.21 就发了我断言"不存在"的入口，而我直到 10-07 才知道。**

> **否定性结论（"没有 X / 不支持 Y / 只能 Z"）必须带版本号和获取日期。
> 它比肯定性事实衰减得更快 —— 只需要上游发一个版本就被推翻，而且不会有人来通知我。**

正面推论：**上游未修复 ≠ 只能手改产品内部状态。** 09-22 我手改了 `projects.json`
（删掉 `mino` 记录）才解开死锁；同样的动作今天有正规入口了。手改内部数据是最后手段，
不是第一反应 —— 提 Issue 之后的等待窗口通常比我以为的短。

<a id="myagents-channels"></a>
## MyAgents IM 渠道 ≠ 独立 OpenClaw 网关（2026-10-17）

**这是两套独立系统，看错会白查一圈。**

| | MyAgents IM 渠道 | 独立 OpenClaw 网关 |
|---|---|---|
| 进程 | `plugin-bridge-dist.mjs --myagents-sidecar`，每个渠道一个 | launchd `ai.openclaw.gateway` |
| 查配置 | `myagents agent channel list <agentId>` | `openclaw status` |
| 日志 | `~/.myagents/logs/unified-YYYY-MM-DD.log`、`~/.myagents/tmp/openclaw-YYYY-MM-DD.log` | `~/Library/Logs/openclaw/gateway.log` |

**2026-10-03 的坑**：Tim 说「无法和我的微信连接」，我先查 `openclaw status`，
看到 18789 的 gateway 是 stopped —— 但那个网关跟微信渠道没关系，微信跑在
MyAgents 的 plugin-bridge 里。系统查错了，结论自然也对不上。

Lucia 当前两个渠道（同属一个 agent）：
- `openclaw:openclaw-weixin`（tencent-weixin 插件）→ 微信
- `openclaw:openclaw-lark` → 飞书

**健康检查**：
- 进程：`ps aux | grep plugin-bridge-dist`，`--bot-id` 对应 `channel list` 的渠道 ID
- 微信长轮询是否活着：`lsof -nP -p <pid> -iTCP -sTCP:ESTABLISHED`，
  应看到到 `ilinkai.weixin.qq.com`（如 `36.155.189.158:443`）的连接
- 端点直连：`curl -m 12 -o /dev/null -w "%{http_code}" https://ilinkai.weixin.qq.com/`
  —— **404 是正常的**，只说明网络通
- 单次 `getUpdates: TypeError: fetch failed` 会自动重试，不等于断线

**会话模型**：微信 / 飞书是各自独立的 Session，上下文不互通。用户换渠道后要接续，
得把关键结论带过来。

**未解**：2026-10-03 微信里发 `/new Lucia` 没收到回复（11 字符 inbound 后无 outbound）。
之后 Tim 表示微信正常可用，未复现，暂不按缺陷处理。

<a id="myagents-attachments"></a>
## 文件交付：`myagents_files/` 才是附件目录（2026-10-17）

**Agent 生成的文件，只有写进工作区根部的 `myagents_files/` 才会在桌面聊天里变成可下载附件。
放 `workspace/` 只是普通文件，客户端不呈现。**

依据 `skills/myagents-docs/references/workspaces-sessions-files.md`：
- L79：`myagents_files/` 是 Agent 产物与需要稳定引用的工作区目录之一
- L105：Agent 生成的图片、音频、PDF 等使用统一附件形式展示，用户可在 `myagents_files/` 找到产物

**Widget 没有导出能力**：
- `<generative-ui-widget>` 是聊天内联渲染协议，不是文件
- `myagents widget --help` 只有 `readme`，没有 export / save
- `myagents im send-media --file` 只对 IM session 有效，桌面会话用不了

→ 用户说「要图 / 要下载」时，**直接产出文件写进 `myagents_files/`**，不要只给路径或开 Finder。
   可视内容按同一份设计另出一份 PNG/SVG。

<a id="svg-to-png"></a>
## macOS SVG → PNG（2026-10-17）

本机没有 `rsvg-convert` / `inkscape` / `magick` / `cairosvg`，**只有 `qlmanage`**。

```bash
qlmanage -t -s 1400 -o /tmp/out file.svg     # → file.svg.png
```

两个坑：
- `-s` 是最大边长，输出会被塞进**正方形画布**（1400×1400），内容顶部对齐、底部一大片空白
- `sips -c H W` 是**居中裁剪** —— 直接裁会把顶部内容切掉

正解：用 PIL 从顶部裁，高度按 viewBox 比例算。

```python
from PIL import Image
im = Image.open(src)
h = round(im.width * 516 / 696)      # viewBox 高 / 宽
im.crop((0, 0, im.width, h)).save(dst)
```

裁完读一次图确认，别只看像素尺寸。

