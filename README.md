# Notion Skills | Notion 技能集

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![Notion API](https://img.shields.io/badge/Notion%20API-v2025--09--03-black)](https://developers.notion.com)

> **English**: A collection of Notion integration skills for Claude AI, enabling seamless connection and synchronization with your Notion workspace for note management, knowledge base building, and team collaboration.
>
> **中文**: 专为 Claude AI 设计的 Notion 集成技能集合，实现与 Notion 工作区的无缝连接和同步，支持笔记管理、知识库构建和团队协作。

---

## Overview | 概述

This repository provides OpenClaw-compatible skills that integrate Claude AI with Notion, allowing you to create, read, update, and manage Notion pages, databases, and blocks through natural language conversations.

本仓库提供与 OpenClaw 兼容的技能，将 Claude AI 与 Notion 集成，让你可以通过自然语言对话来创建、读取、更新和管理 Notion 页面、数据库和块。

### Key Features | 核心功能

- **Page Management | 页面管理**: Create, read, update, and delete Notion pages | 创建、读取、更新和删除 Notion 页面
- **Database Operations | 数据库操作**: Query, filter, sort, and modify database entries | 查询、筛选、排序和修改数据库条目
- **Block Editing | 块编辑**: Add and edit various content blocks (text, headings, lists, code, etc.) | 添加和编辑各种内容块（文本、标题、列表、代码等）
- **Knowledge Base | 知识库**: Build and maintain structured knowledge bases | 构建和维护结构化知识库
- **Team Collaboration | 团队协作**: Share and collaborate on Notion content | 共享和协作 Notion 内容
- **Data Sync | 数据同步**: Bi-directional sync between Claude and Notion | Claude 与 Notion 之间的双向同步

---

## Installation | 安装

### Prerequisites | 前提条件

1. **Notion Account | Notion 账号**: You need a Notion account (Free/Personal/Team/Enterprise) | 你需要一个 Notion 账号（免费/个人/团队/企业版）
2. **Notion Integration | Notion 集成**: Create a Notion integration at https://www.notion.so/my-integrations | 在 https://www.notion.so/my-integrations 创建一个 Notion 集成
3. **API Key | API 密钥**: Copy your Integration Token | 复制你的集成令牌

### For OpenClaw | OpenClaw 安装

```bash
# Install the skill
openclaw skills install TimCheung-jx/notion-skills

# Or install individual skills
openclaw skills install TimCheung-jx/notion-skills/page-manager
openclaw skills install TimCheung-jx/notion-skills/database-manager
```

### Manual Installation | 手动安装

```bash
# Clone the repository
git clone https://github.com/TimCheung-jx/notion-skills.git

# Copy to OpenClaw skills directory
cp -r notion-skills/* ~/.openclaw/workspace/skills/

# Configure API key
echo "your_notion_api_key" > ~/.config/notion/api_key
```

### Configuration | 配置

1. **Store API Key | 存储 API 密钥**:
   ```bash
   mkdir -p ~/.config/notion
   echo "secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > ~/.config/notion/api_key
   ```

2. **Share Notion Pages | 共享 Notion 页面**:
   - In Notion, go to your page/database
   - Click "Share" → "Add connections"
   - Select your integration
   - 在 Notion 中，进入你的页面/数据库
   - 点击"共享" → "添加连接"
   - 选择你的集成

3. **Verify Connection | 验证连接**:
   ```
   /notion status
   ```

---

## Usage | 使用

### Quick Start | 快速开始

**Create a Page | 创建页面**:
```
/notion create page "Meeting Notes" in "Work" database
Content: Weekly team sync discussion points...
```

**Query Database | 查询数据库**:
```
/notion query "Projects" database
Filter: Status = "In Progress"
Sort: Priority descending
```

**Update Entry | 更新条目**:
```
/notion update page "Project Alpha"
Set: Status = "Completed", Due Date = "2026-06-01"
```

### Available Commands | 可用命令

| Command | Description | 描述 |
|---------|-------------|------|
| `/notion status` | Check connection status | 检查连接状态 |
| `/notion create page` | Create a new page | 创建新页面 |
| `/notion create database` | Create a new database | 创建新数据库 |
| `/notion query` | Query database entries | 查询数据库条目 |
| `/notion update` | Update page/database | 更新页面/数据库 |
| `/notion delete` | Delete page/block | 删除页面/块 |
| `/notion search` | Search across workspace | 跨工作区搜索 |
| `/notion sync` | Sync data with Notion | 与 Notion 同步数据 |

### Example Workflows | 示例工作流

#### 1. Meeting Notes Management | 会议笔记管理

```
User: Create meeting notes for "Product Review - May 30"

Claude: 
✓ Created page "Product Review - May 30" in Meeting Notes database
- Date: 2026-05-30
- Attendees: [To be filled]
- Agenda: [To be filled]
- Action Items: [To be filled]

Link: https://notion.so/xxxx
```

#### 2. Project Tracking | 项目跟踪

```
User: Add new project "Website Redesign" to Projects database
Details: Client = ABC Corp, Budget = 50k, Deadline = July 15

Claude:
✓ Added "Website Redesign" to Projects database
- Status: Not Started
- Priority: Medium
- Assigned: Unassigned

Database updated: https://notion.so/xxxx
```

#### 3. Knowledge Base Building | 知识库构建

```
User: Create knowledge base article about "GDPR Compliance"
Category: Legal, Tags: [Privacy, EU Law]

Claude:
✓ Created article "GDPR Compliance" in Knowledge Base
- Category: Legal
- Tags: Privacy, EU Law
- Created: 2026-05-30
- Last Updated: 2026-05-30

Article link: https://notion.so/xxxx
```

---

## Skills Included | 包含技能

### Core Skills | 核心技能

| Skill | Description | 描述 |
|-------|-------------|------|
| **page-manager** | Create and manage Notion pages | 创建和管理 Notion 页面 |
| **database-manager** | Query and modify databases | 查询和修改数据库 |
| **block-editor** | Edit content blocks | 编辑内容块 |
| **workspace-search** | Search across workspace | 跨工作区搜索 |
| **sync-engine** | Bi-directional data sync | 双向数据同步 |

### Property Types Supported | 支持的属性类型

| Type | Description | 描述 |
|------|-------------|------|
| `title` | Page title | 页面标题 |
| `rich_text` | Rich text content | 富文本内容 |
| `number` | Numeric values | 数值 |
| `select` | Single select | 单选 |
| `multi_select` | Multiple select | 多选 |
| `date` | Date and time | 日期和时间 |
| `people` | People/mentions | 人员/提及 |
| `files` | Files and media | 文件和媒体 |
| `checkbox` | Boolean checkbox | 布尔复选框 |
| `url` | URL links | URL 链接 |
| `email` | Email addresses | 邮箱地址 |
| `phone` | Phone numbers | 电话号码 |
| `formula` | Computed values | 计算值 |
| `relation` | Database relations | 数据库关系 |
| `rollup` | Aggregated values | 聚合值 |

---

## API Reference | API 参考

### Notion API Version | Notion API 版本

- **Version**: `2025-09-03`
- **Documentation**: https://developers.notion.com

### Authentication | 认证

```python
headers = {
    "Authorization": "Bearer secret_xxxxxxxx",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}
```

### Key Endpoints | 关键端点

| Endpoint | Method | Description | 描述 |
|----------|--------|-------------|------|
| `/pages` | POST | Create page | 创建页面 |
| `/pages/{id}` | GET/PATCH | Read/Update page | 读取/更新页面 |
| `/databases/{id}/query` | POST | Query database | 查询数据库 |
| `/search` | POST | Search workspace | 搜索工作区 |
| `/blocks/{id}/children` | GET/PATCH | Get/Update blocks | 获取/更新块 |

---

## Configuration | 配置

### Environment Variables | 环境变量

| Variable | Description | Required | 描述 |
|----------|-------------|----------|------|
| `NOTION_API_KEY` | Notion integration token | Yes | Notion 集成令牌 |
| `NOTION_VERSION` | API version (default: 2025-09-03) | No | API 版本 |
| `NOTION_PAGE_SIZE` | Default page size for queries | No | 默认查询页大小 |

### File Structure | 文件结构

```
notion-skills/
├── page-manager/
│   └── SKILL.md
├── database-manager/
│   └── SKILL.md
├── block-editor/
│   └── SKILL.md
├── workspace-search/
│   └── SKILL.md
├── sync-engine/
│   └── SKILL.md
├── README.md
└── LICENSE
```

---

## Troubleshooting | 故障排除

### Common Issues | 常见问题

**1. "API key is invalid" | "API 密钥无效"**
- Check if the API key is correctly stored in `~/.config/notion/api_key`
- Verify the integration has access to the page/database
- 检查 API 密钥是否正确存储在 `~/.config/notion/api_key`
- 验证集成是否有权访问页面/数据库

**2. "Page not found" | "页面未找到"**
- Ensure the page is shared with your integration
- Check the page ID is correct
- 确保页面已与你的集成共享
- 检查页面 ID 是否正确

**3. "Rate limit exceeded" | "超出速率限制"**
- Notion API has rate limits (3 requests per second)
- Add delays between bulk operations
- Notion API 有速率限制（每秒 3 个请求）
- 在批量操作之间添加延迟

### Debug Mode | 调试模式

```bash
# Enable debug logging
export NOTION_DEBUG=true

# Test connection
/notion status --verbose
```

---

## Compatibility | 兼容性

| Platform | Status | Notes |
|----------|--------|-------|
| **OpenClaw** | ✅ Fully Supported | Native skill format |
| **Hermes** | ✅ Compatible | Standard skill structure |
| **Claude Desktop** | ⚠️ Partial | Requires manual setup |
| **Notion Free** | ✅ Supported | All basic features |
| **Notion Plus** | ✅ Supported | All features |
| **Notion Enterprise** | ✅ Supported | Advanced permissions |

---

## Contributing | 贡献

We welcome contributions to improve Notion integration:

欢迎贡献以改进 Notion 集成：

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Ideas | 贡献想法

- Additional skill modules | 额外的技能模块
- Better error handling | 更好的错误处理
- More database templates | 更多数据库模板
- Workflow automation | 工作流自动化
- Multi-language support | 多语言支持

---

## Acknowledgments | 致谢

- Powered by [Notion API](https://developers.notion.com)
- Inspired by the OpenClaw community
- Built for Claude AI integration

---

## License | 许可证

MIT License - see [LICENSE](LICENSE) file for details.

---

## Author | 作者

**TimCheung-jx** - [GitHub](https://github.com/TimCheung-jx)

---

## Related Repositories | 相关仓库

| Repository | Description | 描述 |
|------------|-------------|------|
| [Claude-legal-skills](https://github.com/TimCheung-jx/Claude-legal-skills) | Legal skills collection | 法律技能集 |
| [ad-compliance-review](https://github.com/TimCheung-jx/ad-compliance-review) | Ad compliance review | 广告合规审查 |
| [ecommerce-compliance-guide](https://github.com/TimCheung-jx/ecommerce-compliance-guide) | E-commerce compliance | 电商合规指南 |
| [tim-design-system](https://github.com/TimCheung-jx/tim-design-system) | Design system | 设计系统 |

---

**Disclaimer | 免责声明**

These skills are for productivity enhancement only. Please ensure compliance with Notion's Terms of Service and your organization's data policies when using automated integrations.

本技能仅供提高工作效率使用。使用自动化集成时，请确保遵守 Notion 的服务条款和你所在组织的数据政策。
