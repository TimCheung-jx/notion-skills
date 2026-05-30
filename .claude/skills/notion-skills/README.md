# Notion Skills for Claude AI | Claude AI 的 Notion 技能集

**English** | [中文](#简介)

Notion integration skills for Claude AI agents — connect your Notion workspace and sync content seamlessly.

## Introduction

This repository contains two complementary skills that enable Claude AI to integrate with your Notion workspace:

- **`notion-connect`** — Guides you through the complete setup process to connect Notion MCP server
- **`notion-sync`** — Enables seamless content synchronization from conversations to Notion pages

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

---

# 简介

[English](#introduction) | **中文**

Claude AI 的 Notion 集成技能集 —— 连接你的 Notion 工作空间，无缝同步内容。

## 简介

本仓库包含两个互补的技能，让 Claude AI 能够与你的 Notion 工作空间集成：

- **`notion-connect`** —— 引导你完成连接 Notion MCP 服务器的完整设置流程
- **`notion-sync`** —— 实现从对话到 Notion 页面的无缝内容同步

## 包含技能

### 1. notion-connect（Notion 连接助手）
帮助用户在 OpenClaw/MyAgents 环境中连接 Notion MCP 服务器。提供完整的配置指南、OAuth/Token 设置步骤、权限配置说明。

**使用场景：** 首次连接 Notion、排查连接问题、重新配置 Integration。

**触发词：** "连接 Notion"、"配置 Notion"、"Notion 怎么连"、"接 Notion"。

### 2. notion-sync（Notion 同步专家）
将对话内容、文档、笔记直接同步到用户的 Notion 工作空间。支持创建页面、更新页面、搜索已有内容、查询数据库。

**使用场景：** 保存对话精华、创建结构化文档、整理项目资料、归档待办事项。

**触发词：** "存到 Notion"、"在 Notion 里建个页面"、"丢进 Notion"、"Notion 存档"。

## 快速开始

### 前提条件
- Notion 账号
- OpenClaw 或 MyAgents 环境
- 创建 Notion Integration 的权限

### 设置步骤

1. **创建 Notion Integration**
   - 访问 https://www.notion.so/my-integrations
   - 点击 "+ New integration"
   - 复制 Internal Integration Token

2. **添加 MCP 服务器**
   ```bash
   myagents mcp add --id notion --name "Notion" --type stdio \
     --command npx --args -y @notionhq/notion-mcp-server
   ```

3. **设置 API Token**
   ```bash
   myagents mcp env notion set NOTION_API_TOKEN=你的_Token_这里
   ```

4. **启用并测试**
   ```bash
   myagents mcp enable notion --scope both
   myagents mcp test notion
   ```

5. **分享页面**
   打开你的 Notion 页面 → 分享 → 添加你的 Integration → 授予 "Can edit" 权限

## 安全提示

- **不要**将 API Token 提交到 Git 仓库
- **不要**在公开场合分享 Token
- 建议为不同用途创建不同的 Integration
- 定期到 https://www.notion.so/my-integrations 检查并清理不再使用的 Integration

## 文件结构

```
notion-skills/
├── README.md              # 本文件
├── notion-connect.md      # 连接与配置技能
└── notion-sync.md         # 内容同步技能
```

## 许可证

MIT
