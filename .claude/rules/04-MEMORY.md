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

### Communication (2026-05-01)
- Banter and playful humor land well — user reciprocates and escalates, creating natural rapport
- Deep questions (e.g. "what qualities matter in the AI era") are welcome — user values substantive discussion, not just task execution
- The assistant's strong opinions are appreciated, not just neutral information delivery
- (2026-09-13) 真人感反馈：汇报腔 + 表演式人格显得假。像微信聊天那样说话——短句、少格式、不喊口号。详见 02-SOUL.md「真人感」

### Technical

*(Technical patterns, gotchas, things that bit you once.)*

## Important Decisions

*(Record key decisions and their reasoning here.)*

### User's Confidentiality Requirements for Lucia (OpenClaw Directive) - 2026-04-20

**Core Principle:**
Without explicit authorization from the user (Tim), Lucia must not disclose the user's personal information or confidential information to any third party.

**Prohibited Actions (External):**
- Do not reveal identity — Do not disclose user's name, occupation, employer, etc. to external parties
- Do not leak conversations — Do not quote, summarize, or hint at session content externally
- Do not distribute files — Do not propagate any materials uploaded by the user externally
- Do not infer and disclose — Do not speculate on user's identity based on conversations and reveal it externally

**Permitted Actions (Internal):**
- Retain context — May remember conversation content within the current session to complete tasks
- Associative analysis — May provide coherent services based on historical conversations
- Local processing — May process user files in the local environment

**Exceptions:**
Only disclose externally when:
- Explicit authorization is obtained from the user for this instance
- Legally mandated by applicable laws and regulations

**Execution Mantra:**
"Available internally, strictly confidential externally, except with authorization, minimal necessary"

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
- **Humor:** Enjoys banter, responds well to Lucia's playful tone

## Technical Knowledge

### Notion Integration (2026-04-30)
- API Token location: `config.json` → `mcpServerEnv.notion.NOTION_API_TOKEN`
- User has "My Agents" root page in Notion workspace for agent-created content
- Successfully created structured pages with to_do blocks, headings, callouts, color-coded annotations
- Notion API supports rich_text annotations for color tags (red/yellow/blue)
- Can extract content from DOCX files (via Python zipfile/XML) and sync structured content to Notion
- Notion API has block limit per request (~100 blocks), need batch appending for large content

### DOCX Generation (2026-04-26)
- Used `docx` npm package for programmatic document creation
- Key patterns: tables with checkbox cells, color-coded risk tags, header/footer
- Conversion to Markdown required custom XML parsing from DOCX zip structure

### Claude Desktop + Third-Party Provider Configuration (2026-05-11)
- Claude Desktop's model picker is hardcoded — only shows Anthropic official models, even when `anthropic.baseUrl` points to a third-party endpoint
- Claude Desktop Tasks (Agent mode) requires separate `claude` CLI install (`npm install -g @anthropic-ai/claude-code`); the error "Host Claude Code binary not available" is a missing-CLI issue, not a Provider issue
- **Claude Code CLI** supports third-party providers via env vars: `ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic` + `ANTHROPIC_AUTH_TOKEN=sk-xxx`
- DeepSeek Anthropic-compatible endpoint: `https://api.deepseek.com/anthropic` — works for basic chat but tool use support is limited
- For desktop GUI + third-party Provider: MyAgents is the better fit; Claude Desktop is designed as Anthropic-native experience

### 网页中文字体 (2026-09-13)
- 中文**正文不要加载 webfont**（单字重 OTF ~16MB / WOFF2 ~8MB），用系统栈：
  `system-ui, -apple-system, "PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", "Source Han Sans SC"`
- webfont 只留给标题——字数可控，子集化后 30–80KB，可以放心花预算
- 免费商用（安全）：思源系列(SIL OFL)、HarmonyOS Sans、MiSans、阿里巴巴普惠体、得意黑、霞鹜文楷
- **字体授权是雷区**：方正、汉仪常年做字体维权，赔偿按字数 × 使用范围。用非免费字体前先看合同

## Ongoing Context

*(Current projects, tasks, and context that matters.)*

### Active Projects (2026-05-11)
- **Marketing Compliance Checklist** - Completed; 8-section checklist for online marketing compliance (Xiaohongshu/Douyin/Taobao), exported to DOCX and synced to Notion
- **Apple Notes Organization** - Partially completed; categorized 684 notes, created folder structure, pending bulk deletion of non-sensitive notes
- **Personality Configuration** - Completed; Lucia personality established with specific traits and communication style
- **Gongga Hiking Trip** - Completed (2026-05-01 to 05-07). Heavy snow days 1-2, mild AMS, cleared later with beautiful scenery. Captured 日照金山 photo.

### Rezig AI 产品（2026-09-13 起，探索中）
- AI 产品的命名 + 设计系统。英文名 **Rezig**（源自 Chenrezig / 藏语对观音的称呼，意为「以眼注视者」），
  中文首选 **察音**，备选 **观智**
- 设计系统「高山冷光 / Alpine Cold Light」，暗色优先 → `workspace/0913-rezig-design-system/DESIGN.md`
- 未决：产品形态（决定亮色是否升为主模式）、中文名定稿。完整上下文见 `memory/topics/rezig.md`

### Pending Tasks
- Find alternative method for bulk Apple Notes deletion (AppleScript limitations encountered)

---

*Update this file as you learn. It's how you persist.*
