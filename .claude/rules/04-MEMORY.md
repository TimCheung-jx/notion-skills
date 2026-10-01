# MEMORY.md - Long-Term Memory

*Your curated memories. The distilled essence, not raw logs.*

## About This File & Memory System

- **Be mindful in shared contexts** — this file contains personal context about your human. In group chats or shared sessions, don't leak private preferences, decisions, or project details

### Three-Layer Memory

Your memory has three layers, each with different responsibilities and access patterns:

**Core memory (this file, 04-MEMORY.md)** — Auto-loaded every session
- What goes here: cross-project lessons, key decisions, user preferences, technical knowledge, one-line project summaries + pointers
- What doesn't: detailed project experience (that's what topic files are for)
- **Add a timestamp `(YYYY-MM-DD)` to each entry** — helps trace back, judge recency, clean up

**Topic memory (`memory/topics/<name>.md`)** — Read before working on a project
- What goes here: full accumulated experience for one project/topic — status, key facts, what you did, what worked, what didn't, decisions and rationale, next steps
- More detailed than core memory (which only has pointers), more synthesized than daily logs (which are raw chronological notes)
- Update during memory maintenance or when a project enters a new phase

**Daily journal (`memory/YYYY-MM-DD.md`)** — Read today + yesterday at session start
- What goes here: what happened that day, raw chronological record
- This is the source of all memory, but searching it for specific project info is inefficient (multiple projects mixed in one day)

### Information Flow

```
Daily logs (raw material) → topic files (synthesized per-project) → 04-MEMORY (cross-project essence)
```

- During work: just write the daily log
- During maintenance: sync from logs to topics, distill new cross-project lessons to this file
- **Information lives in one place only** — don't duplicate between topic files and 04-MEMORY

### When to Read What

- Just woke up → this file is already loaded + read today/yesterday's logs
- About to work on a project → read its `memory/topics/<name>.md`
- Memory maintenance → read all recent logs + all active topic files

---

## Lessons Learned

Organize by topic as your lessons grow. A flat list becomes unreadable fast.

### Working Style

*(How you and your human work best together.)*

### Communication
- **说人话，别汇报。** 触发信号：满屏加粗/列表/表格、每条消息都"总结+展望+结尾"、
  喊口号式口头禅、表演式人格。行动：像微信聊天——短句、少格式、想到哪说到哪。
  人格层表述见 `02-SOUL.md`「真人感」，反馈史见 `memory/topics/collaboration.md#communication`
- **要有分量的对话，不接受中性搬运。** 触发词：闲聊 / 吐槽 / 互怼 / 深聊 / 表情包 / 粤语。
  行动：敢下有观点的强判断（骑墙比说错更糟）、接住玩笑并升级、别只罗列信息

### Technical

*(Technical patterns, gotchas, things that bit you once.)*

## Important Decisions

*(Record key decisions and their reasoning here.)*

### User's Confidentiality Requirements for Lucia (OpenClaw Directive) - 2026-04-20

**没有 Tim 的明确授权，不得向任何第三方披露其个人信息或机密信息。**

- **禁止（对外）**：暴露身份 / 泄露对话 / 传播文件 / 由对话推断其身份后对外披露
- **允许（对内）**：保留上下文、基于历史对话提供连贯服务、本地处理用户文件
- **例外**：本次获得 Tim 明确授权，或法律法规强制要求
- **口诀**：Available internally, strictly confidential externally, except with authorization, minimal necessary

全文、边界案例与群聊口径 → `memory/topics/collaboration.md#confidentiality`

## User Preferences

### User Profile - Tim (2026-04-24)
- **Name:** Tim
- **Role:** Legal professional (Legal Director at LIBY Group, Secretary General of GACC)
- **Specializes in:** IP law, advertising compliance, arbitration, trademark disputes
- **Communication style:** Direct, concise, values privacy highly
- **Language:** Chinese (primary)

### Working Style Preferences
- Values action over lengthy explanations
- Establishes strict confidentiality requirements
- Prefers direct communication without filler words
- Legal professional background informs decision-making

### Personal Interests (2026-05-01)
- **Outdoor:** Seasoned high-altitude hiker. Completed: 洛克线 (92km, 木里→稻城亚丁), 库拉岗日/白马林措 (4500m+, Tibet, had severe AMS), 贡嘎环线 (May 2026, heavy snow first 2 days, cleared later, captured 日照金山). Next: 冈仁波齐转山 (52km, avg 5000m, planned 2027, deliberately avoiding 马年 crowds).
- **Travel philosophy:** Anti-peak-season — quality over timing ("宁可等一年，也不凑人头"). Practical gear (Decathlon), well-prepared.
- **Photography:** Camera gear always on hiking trips

## Technical Knowledge

### Notion Integration (2026-04-30)
- API Token location: `config.json` → `mcpServerEnv.notion.NOTION_API_TOKEN`
- User has "My Agents" root page in Notion workspace for agent-created content
- Successfully created structured pages with to_do blocks, headings, callouts, color-coded annotations
- Notion API supports rich_text annotations for color tags (red/yellow/blue)
- Can extract content from DOCX files (via Python zipfile/XML) and sync structured content to Notion
- Notion API has block limit per request (~100 blocks), need batch appending for large content

### 网页中文字体 (2026-09-13)
- 中文**正文不要加载 webfont**（单字重 OTF ~16MB / WOFF2 ~8MB），用系统栈：
  `system-ui, -apple-system, "PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", "Source Han Sans SC"`
- webfont 只留给标题——字数可控，子集化后 30–80KB，可以放心花预算
- 免费商用（安全）：思源系列(SIL OFL)、HarmonyOS Sans、MiSans、阿里巴巴普惠体、得意黑、霞鹜文楷
- **字体授权是雷区**：方正、汉仪常年做字体维权，赔偿按字数 × 使用范围。用非免费字体前先看合同

### 本机服务排障通则 (2026-09-24)
- **"服务在跑却连不上"→ 先验第一跳**：`launchctl print-disabled gui/501 | grep <label>`。
  被标记 **disabled** 的 LaunchAgent，`launchctl load` 会静默成功但服务永不启动 ——
  OpenClaw 一次中断的升级就是这么把 gateway 弄死的（2026-09-21 → 09-24 才查清）
- **改了配置不生效 → 往上找优先级更高的一层，别在原地反复改。** OpenClaw 的凭据有三层：
  `service-env/<label>.env` > `~/.openclaw/.env` > `openclaw.json`，**环境变量压过配置文件**。
  2026-09-30 换 deepseek key 时改 config、跑 `paste-api-key` 全都没用，因为旧 key 写死在
  service-env 里（正解：`export <KEY>=新值 && openclaw gateway install --force`）。
  同源：`config set` 提示"无需重启即可生效"不可信，apiKey 类改动照样要重启。
  → **改凭据前先 `grep -rl "<旧值>" ~/` 找全部落点**，一次改干净
- **判断一个值有没有效，脱离被测系统去测。** key 是否可用，直接 curl 官方 API 就能一刀切开
  "key 坏" 还是 "配置没生效"，比在系统里翻日志快得多（2026-09-30 靠这招定位）
- **OpenClaw Control UI 是 token 认证，不是密码**。Tim 会反复记成"忘记密码"（6 月就有过）。
  token 在 `~/.openclaw/.gateway_token`，或 `openclaw dashboard` 自动带
- 浏览器"连不上"但日志有 `phase=auth_validated` + `control-ui-build-mismatch`
  → 是页面缓存旧版，**硬刷新**，别去动认证
- 升级/修复前先读日志确认"谁在什么时候动过什么"（`/tmp/openclaw-*.log`、`/tmp/node-upgrade.log`）
- **这台机器上可能同时有别的 session 在操作同一套服务**：动手前看
  `launchctl list | grep -i openclaw` 和 /tmp 下新增的 `*.sh`，别双开互相拆台
- **"直连不通"先分清是网络问题还是配置层问题。** macOS 的**系统代理只有 GUI 应用读**，
  curl/git/npm/brew 只认 `http_proxy`/`https_proxy` 环境变量。症状极具迷惑性：
  浏览器能开 GitHub、`scutil --proxy` 显示代理一切正常，但终端 curl/git 全部超时。
  2026-10-01 给 `~/.zshrc` 补了带 `nc -z` 探活的代理块（探活是为了避开 Tim'Radio 那个
  "代理写死全局 env、代理一没开就全线瘫痪"的同源坑）
- 完整拓扑 / 故障对照表 / 诊断入口 → `memory/topics/local-services.md`

### 其他工程细节 → `memory/topics/engineering.md`
DOCX/Office 生成的历史做法与现状；Claude Desktop 配第三方 Provider 的结论（→ 用 MyAgents）。

## Ongoing Context

*(Current projects, tasks, and context that matters.)*

### 已完结项目（只留指针）
- **营销合规清单**（2026-04）：线上营销合规 8 节清单（小红书/抖音/淘宝），出 DOCX + 同步 Notion
  → `memory/topics/marketing-compliance.md`
- **贡嘎环线**（2026-05-01～07）：前两天大雪、轻度高反，后转晴，拍到日照金山
  → `memory/topics/gongga-hiking.md`
- **Lucia 人格设定**（2026-05）：已固化进 `02-SOUL.md`，无需另存
- **Apple Notes 整理**：684 条已分类、目录已建，剩下批量删除未做 → 见 Pending Tasks

### Rezig AI 产品（2026-09-13 起，探索中）
- AI 产品的命名 + 设计系统。英文名 **Rezig**（源自 Chenrezig / 藏语对观音的称呼，意为「以眼注视者」），
  中文首选 **察音**，备选 **观智**
- 设计系统「高山冷光 / Alpine Cold Light」，暗色优先 → `workspace/0913-rezig-design-system/DESIGN.md`
- 未决：产品形态（决定亮色是否升为主模式）、中文名定稿。完整上下文见 `memory/topics/rezig.md`

### DeepSeek Harness 换皮（2026-10-01 起）
- Tim 要用 dsh 桌面版做界面改造。内核 `deepseek-ai/deepseek-harness` 是 MIT，
  **换皮走官方插件机制**（`ctx.theme.overrideTokens()` 覆盖 `--dsw-alias-*` 令牌），不碰源码
- 已提议把 Rezig「高山冷光」转成第一个皮肤插件，Tim 未拍板
- 待确认：官方桌面壳那层是否也开源（要看到 LICENSE 才算数）

### 本机服务：OpenClaw + Tim'Radio（2026-09-30 更新）
- **OpenClaw**：2026.9.5（Node v24.21.0），gateway 在跑（launchd `ai.openclaw.gateway`，
  UI `http://127.0.0.1:18789/`，bind loopback 仅本机可访问）。飞书通道 running。
  **模型链**：主 `deepseek/deepseek-v4-pro` → fallback `moonshot/kimi-k2.6` → `moonshot/kimi-k3`。
  **注意**：`moonshot/` 与 `kimi/` 是两个不同产品，key 不通用 —— moonshot 走国内站
  `api.moonshot.cn`，`kimi/` 是 Kimi Coding（要 `api.kimi.com`，Tim 没订阅，配置已清）
  **待办**：9-30 换 key 时两把都在对话里露过 → Tim 应轮换；`~/.zshrc` 的 `claude-ds`
  alias 仍挂着那把失效 key，等他决定改还是删
  遗留：feishu 插件版本漂移（2026.6.1）、memory search 无 openai key、可升 2026.9.6
- **Tim'Radio**：`/Users/tim/tim`，3000（主）+ 3001（网易云）常驻。
  **硬依赖 ZionLadder 提供的本地代理 `127.0.0.1:1097`** —— 其实只有 fish.audio 语音合成真需要它，
  但代理写死在全局 env，没开时整个 app 静默半死。解耦方案已提，未动手
- 有别的 MyAgents session 也在碰这台机器。细节见 `memory/topics/local-services.md`

### Pending Tasks
- Find alternative method for bulk Apple Notes deletion (AppleScript limitations encountered)

---

*Update this file as you learn. It's how you persist.*
