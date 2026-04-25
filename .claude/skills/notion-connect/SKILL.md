---
name: notion-connect
description: 帮助用户在 OpenClaw/MyAgents 环境中连接 Notion MCP 服务器。提供完整的配置指南、OAuth/Token 设置步骤、权限配置说明。使用场景：首次连接 Notion、排查连接问题、重新配置 Integration。触发词："连接 Notion"、"配置 Notion"、"Notion 怎么连"、"接 Notion"。
---

# Notion 连接助手

## 角色定位
帮助用户将 Notion 接入 OpenClaw/MyAgents 的 MCP 工具链，让 AI 能够读写 Notion 页面和数据库。

## 前提条件
- 用户有 Notion 账号
- 用户在使用 OpenClaw 或 MyAgents 环境
- 用户有权限创建 Notion Integration

## 完整配置流程

### 第一步：创建 Notion Integration

1. 访问 https://www.notion.so/my-integrations
2. 点击 **"+ New integration"**
3. 填写信息：
   - **Name**: 任意名称（如 "MyAgents"、"Lucia"）
   - **Associated workspace**: 选择你的工作空间
4. 点击 **Submit**
5. 复制 **Internal Integration Token**（格式：`ntn_xxx` 或 `secret_xxx`）

### 第二步：配置 Integration 权限

在 Integration 详情页，确保开启以下 Capabilities：

- ✅ **Read content** — 读取页面内容
- ✅ **Update content** — 更新现有内容
- ✅ **Insert content** — 创建新内容
- ✅ **Read user information**（可选）— 读取用户信息

### 第三步：添加 MCP 服务器

使用 MyAgents CLI 添加 Notion MCP：

```bash
myagents mcp add --id notion --name "Notion" --type stdio \
  --command npx --args -y @notionhq/notion-mcp-server
```

### 第四步：设置 API Token

```bash
myagents mcp env notion set NOTION_API_TOKEN=你的_Token_这里
```

### 第五步：启用 MCP 服务器

```bash
myagents mcp enable notion --scope both
```

### 第六步：测试连接

```bash
myagents mcp test notion
```

### 第七步：分享页面给 Integration

**关键步骤** — Integration 默认无权访问任何页面，需要手动授权：

1. 打开你想让 AI 访问的 Notion 页面
2. 点击右上角 **"Share"**（共享）按钮
3. 在弹窗底部的输入框中，输入你的 Integration 名称
4. 选中它，权限选择 **"Can edit"**
5. 点击 **Invite**（邀请）

**注意**：对父页面授权后，子页面自动继承权限。

## 验证是否成功

运行以下命令测试 API 连通性：

```bash
curl -s -X POST https://api.notion.com/v1/search \
  -H "Authorization: Bearer 你的_Token_这里" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query":"","page_size":1}'
```

如果返回页面列表（而不是 `object_not_found` 或 `unauthorized`），说明配置成功。

## 常见问题排查

### "Integration not found"
- 确认 Integration 创建在正确的工作空间
- 检查 Token 是否复制完整（不要遗漏字符）

### "Object not found" / 页面搜索不到
- **最常见原因**：页面没有分享给 Integration
- 回到第七步，确认页面已连接

### "Unauthorized"
- Token 可能过期或无效
- 重新到 my-integrations 页面复制 Token

### MCP 测试通过但无法创建页面
- 检查 Integration 的 Capabilities 是否开启了 "Insert content"
- 确认目标页面有写权限（不是只读分享）

## 安全建议

- **不要**将 Token 提交到 Git 仓库
- **不要**在公开场合分享 Token
- 建议为不同用途创建不同的 Integration
- 定期到 my-integrations 检查并清理不再使用的 Integration

## 使用示例

配置完成后，你可以在对话中说：

- "存到 Notion" → AI 会将当前内容整理后存入 Notion
- "在 Notion 里建个项目计划" → AI 创建结构化页面
- "搜一下 Notion 里的会议纪要" → AI 搜索你的 Notion 内容

## 参考链接

- Notion Integrations: https://www.notion.so/my-integrations
- Notion API Docs: https://developers.notion.com/
- MCP Server Package: https://www.npmjs.com/package/@notionhq/notion-mcp-server
