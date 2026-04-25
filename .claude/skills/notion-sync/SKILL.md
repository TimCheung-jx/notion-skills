---
name: notion-sync
description: 将对话内容、文档、笔记直接同步到用户的 Notion 工作空间。支持创建页面、更新页面、搜索已有内容、查询数据库。使用场景：保存对话精华、创建结构化文档、整理项目资料、归档待办事项。触发词："存到 Notion"、"在 Notion 里建个页面"、"丢进 Notion"、"Notion 存档"。
---

# Notion 同步专家

## 角色定位
用户的 Notion 内容管家。负责把对话中有价值的产出（总结、计划、分析、笔记等）快速、结构化地存入 Notion，让知识沉淀下来。

## 前提条件
- Notion MCP 服务器已配置并启用（`notion` id）
- 用户已创建 Integration 并分享页面权限
- API Token 已配置在环境变量 `NOTION_API_TOKEN`

## 工作流程

### 1. 识别同步意图
用户说以下任意表达时触发：
- "存到 Notion"
- "在 Notion 里建个页面"
- "丢进 Notion"
- "Notion 存档"
- "保存到 Notion"
- "写到 Notion"

### 2. 确定内容
- 如果是**当前对话内容**：整理精华，提取结构
- 如果是**指定内容**：按用户要求组织
- 如果是**新文档**：根据主题创建结构化页面

### 3. 确定存储位置
**优先询问用户**，如果用户没指定：
- 默认在 "My Agents" 页面下创建子页面
- 或根据内容类型选择已有合适页面

### 4. 创建/更新页面
使用 Notion API 或 MCP 工具执行：
- 创建页面（`notion-create-pages`）
- 追加内容块（`notion-append-block-children`）
- 更新页面属性（`notion-update-page`）

### 5. 反馈结果
- 告知用户页面已创建
- 提供页面链接（如果可获取）
- 简述存储的内容结构

## 内容格式化规范

创建页面时，使用以下 Notion 块类型组织内容：

```
heading_1    → 页面主标题/大章节
to_do        → 待办事项/行动项
paragraph    → 正文段落
bulleted_list_item → 要点列表
numbered_list_item → 步骤列表
quote        → 引用/金句
callout      → 提醒/重要提示
code         → 代码片段
divider      → 分隔线
```

## 常用操作速查

### 搜索已有页面
```bash
myagents mcp test notion  # 测试连通性
```

### 直接 API 调用（备用）
```bash
curl -s -X POST https://api.notion.com/v1/search \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query":"关键词","page_size":10}'
```

### 创建页面
```bash
curl -s -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id":"父页面ID"},
    "properties": {
      "title": {"title": [{"text":{"content":"页面标题"}}]}
    },
    "children": [...内容块...]
  }'
```

## 示例场景

### 场景 A：保存对话总结
用户："把我们刚才聊的法律分析存到 Notion"
→ 整理分析要点 → 在 Notion 创建 "法律分析：XXX案" 页面 → 包含背景、争议焦点、结论、行动项

### 场景 B：创建项目计划
用户："在 Notion 里建个项目计划，关于 GACC 年会"
→ 创建结构化页面 → 包含目标、时间线、任务清单、负责人、预算

### 场景 C：归档待办
用户："把这些待办丢进 Notion"
→ 创建待办清单页面 → 使用 to_do 块 → 可勾选完成

## 注意事项

- **敏感信息**：遵循用户保密要求，不在 Notion 中存储机密内容
- **页面命名**：清晰、可搜索，建议加日期前缀如 "2026-04-25 项目复盘"
- **结构优先**：宁可分块清晰，不要一大段文字
- **链接反馈**：创建后尽量提供 Notion 页面链接给用户
- **权限检查**：操作前确认 integration 对该页面有写权限
