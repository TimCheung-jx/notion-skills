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

*(Lessons about tone, format, language, audience.)*

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

## Technical Knowledge

### Notion Integration (2026-04-26)
- API Token location: `config.json` → `mcpServerEnv.notion.NOTION_API_TOKEN`
- User has "My Agents" root page in Notion workspace for agent-created content
- Successfully created structured pages with to_do blocks, headings, callouts, color-coded annotations
- Notion API supports rich_text annotations for color tags (red/yellow/blue)

### DOCX Generation (2026-04-26)
- Used `docx` npm package for programmatic document creation
- Key patterns: tables with checkbox cells, color-coded risk tags, header/footer
- Conversion to Markdown required custom XML parsing from DOCX zip structure

## Ongoing Context

*(Current projects, tasks, and context that matters.)*

### Active Projects (2026-04-26)
- **Marketing Compliance Checklist** - Completed; 8-section checklist for online marketing compliance (Xiaohongshu/Douyin/Taobao), exported to DOCX and synced to Notion
- **Apple Notes Organization** - Partially completed; categorized 684 notes, created folder structure, pending bulk deletion of non-sensitive notes
- **Personality Configuration** - Completed; Lucia personality established with specific traits and communication style

### Pending Tasks
- Find alternative method for bulk Apple Notes deletion (AppleScript limitations encountered)

---

*Update this file as you learn. It's how you persist.*
