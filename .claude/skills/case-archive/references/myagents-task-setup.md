# MyAgents 定时任务配置（case-archive）

## 什么时候用

用户确认汇报节奏、且首轮档案已验收后，把「增量摄取 → 档案更新 → 汇报生成」挂成每 14 天的定时任务。

## 设计决策

- **schedule**：固定间隔 20160 分钟（= 14 天），`--startAt` 锚定第一个汇报日前一晚（如周四 20:00，带时区）
- **激活**：always（到点必跑，是否生成汇报由档案状态决定，见 task-action 模板）
- **runMode**：new-session——档案在文件里，不依赖 session 上下文，避免上下文膨胀
- **结束条件**：持续到用户暂停。案件周期长，不预设 maxExecutions；结案后用户会要求停止

## 创建步骤

1. 用文件写入工具写 `task-action.md`（模板见下），长文本不要拼进 shell 命令
2. 创建：

```bash
myagents task create-direct --name "case-archive-biweekly-<案件代号>" \
  --taskMdFile task-action.md --executionMode recurring \
  --intervalMinutes 20160 \
  --startAt 2026-09-17T20:00:00+08:00 \
  --runMode new-session --json
```

3. 从回执 `data.receipt.taskId` 取权威 ID，然后回读并启用：

```bash
myagents task get <taskId> --json
myagents task run <taskId> --json
```

4. 向用户交付回执：任务名与 ID、执行时间（含时区）、激活方式（到点直接跑）、AI 动作、Session 策略、结束条件（持续到手动停止）、App 需在线（完全退出期间不执行不补跑）、Task Center 治理入口

## task-action.md 模板

```markdown
执行案件档案双周流程（案件代号：<案件代号>，目录：workspace/cases/<案件代号>/）：

1. 按 case-archive 技能的 B→C 流程增量摄取 inbox/ 并更新 archive.md
2. 若 inbox/ 无新材料且档案无实质变化：本轮不生成汇报，在对话里用两三句话说明后结束
3. 有变化则按 D 流程生成本期汇报（PPT），存入 reports/，并在档案的「汇报记录」登记日期、覆盖区间、文件名
4. 生成的汇报在对话里给出路径，并提醒用户检查回链与「待核实」条目
```

## 治理

- 暂停：`myagents task stop <taskId>`（保留 checkpoint）；恢复：`myagents task start <taskId>`
- 结案归档：`myagents task archive <taskId>`
- 查看执行历史：`myagents task runs <taskId> --limit 5 --json`
