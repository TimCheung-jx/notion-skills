# Notion Skills for Claude AI

Notion integration skills for Claude AI agents — connect your Notion workspace and sync content seamlessly.

## Skills Included

### 1. notion-connect
Help users connect Notion MCP server in OpenClaw/MyAgents environment. Provides complete configuration guide, OAuth/Token setup steps, and permission configuration instructions.

**Use cases:** First-time Notion connection, troubleshooting connection issues, reconfiguring Integration.

**Triggers:** "connect Notion", "configure Notion", "how to connect Notion", "link Notion"

### 2. notion-sync
Sync conversation content, documents, and notes directly to your Notion workspace. Supports creating pages, updating pages, searching existing content, and querying databases.

**Use cases:** Save conversation highlights, create structured documents, organize project materials, archive to-do items.

**Triggers:** "save to Notion", "create a page in Notion", "drop into Notion", "Notion archive"

## Quick Start

### Prerequisites
- Notion account
- OpenClaw or MyAgents environment
- Permission to create Notion Integration

### Setup Steps

1. **Create Notion Integration**
   - Visit https://www.notion.so/my-integrations
   - Click "+ New integration"
   - Copy the Internal Integration Token

2. **Add MCP Server**
   ```bash
   myagents mcp add --id notion --name "Notion" --type stdio \
     --command npx --args -y @notionhq/notion-mcp-server
   ```

3. **Set API Token**
   ```bash
   myagents mcp env notion set NOTION_API_TOKEN=your_token_here
   ```

4. **Enable & Test**
   ```bash
   myagents mcp enable notion --scope both
   myagents mcp test notion
   ```

5. **Share Pages**
   Open your Notion page → Share → Add your Integration → Grant "Can edit" permission

## Security Notes

- **DO NOT** commit API tokens to Git repositories
- **DO NOT** share tokens in public
- Create separate Integrations for different use cases
- Regularly review and clean up unused Integrations at https://www.notion.so/my-integrations

## File Structure

```
notion-skills/
├── README.md              # This file
├── notion-connect.md      # Connection & configuration skill
└── notion-sync.md         # Content sync skill
```

## License

MIT
