# 本机服务运维（OpenClaw / Tim'Radio）

> 覆盖 Tim 这台 Mac mini 上常驻的两套自建服务。硬件/系统：`Tim的Mac mini`，macOS 26.x，用户 `tim`。
> 最后更新：2026-09-24

## 一、服务拓扑

| 服务 | 启动方式 | 端口 | 代码/配置 | 备注 |
|---|---|---|---|---|
| **OpenClaw Gateway** | LaunchAgent `ai.openclaw.gateway` | 18789（loopback） | `/usr/local/lib/node_modules/openclaw`，配置 `~/.openclaw/openclaw.json` | 主 agent `main`，模型 deepseek/deepseek-v4-pro；飞书通道 `alita2` |
| Tim'Radio 主服务 | LaunchAgent `com.tim.radio.server` | 3000 | `/Users/tim/tim/server.js` | PWA + 早间播报 + 每小时情绪检查 |
| Tim'Radio 网易云 | LaunchAgent `com.tim.radio.ncm` | 3001 | `/Users/tim/tim/ncm-server/app.js` | 本地 NCM API |
| MyAgents | LaunchAgent `MyAgents.plist` + 应用 | 31415-31417 | `/Applications/MyAgents.app` | 自带独立 node，**不受系统 node 升级影响** |

**Node 依赖**：OpenClaw 与 Tim'Radio 都跑 `/usr/local/bin/node`（官方 pkg 安装，非 brew / 非 nvm）。
2026-09-22 从 v22.22.2 换到 **v24.21.0**（OpenClaw 新版硬要求 ≥24.16 或 ≥26.1）。

## 二、网络前提（重要）

本机**无翻墙时**的直连实测：

| 目标 | 直连 | 说明 |
|---|---|---|
| api.deepseek.com | ✓ | LLM 不需要代理 |
| api.openweathermap.org | ✓ | |
| open.feishu.cn | ✓ | |
| localhost:3001 (NCM) | ✓ | |
| **api.fish.audio** | ✗ | **唯一需要翻墙的**（DNS 被污染，解析到 31.13.73.9 / Facebook IP） |
| google / openai | ✗ | |

- **翻墙工具 = ZionLadder**（`/Applications/ZionLadder.app`），它提供本地 HTTP 代理
  **`127.0.0.1:1097`**。它不随开机启动、不在 login items / launchd / shell 配置里，
  binary 里也查不到 1097（运行时可配）——**排查时靠"它一启动 1097 就 LISTEN"来确认**。
- Tim'Radio 把代理写死在全局 env（`start-server.sh` + LaunchAgent plist 里的
  `HTTP_PROXY/HTTPS_PROXY=http://127.0.0.1:1097`）。
  → **代理不开 = 除本地 NCM 外全部 `ECONNREFUSED`**，但 PWA 页面照常打开、scheduler 只在
  日志里刷错误 —— 典型"看起来活着其实全哑"。
- 待改进（已向 Tim 提过，未动手）：把代理从全局 env 摘掉，只在 `src/tts.js` 里给
  fish.audio 单独挂 ProxyAgent，这样翻墙没开时只掉语音。

## 三、故障对照表

| 症状 | 先查 | 常见结论 |
|---|---|---|
| 网页/客户端连不上，进程却"在" | `launchctl print-disabled gui/501 \| grep openclaw` | **被标记 disabled** —— 见下节 |
| 服务完全没进程 | `launchctl list \| grep -i <label>`；`ps`；`lsof -nP -iTCP:<port> -sTCP:LISTEN` | job 未 bootstrap → `openclaw gateway start` / `gateway install` |
| UI 能开但连不上、要求"登录" | 日志里找 `control-ui-build-mismatch` / `phase=auth_validated` | 页面缓存旧版 → **硬刷新**（Cmd+Shift+R）；别去动认证 |
| 忘了"登录密码" | 它没有密码 | **Control UI 是 token 认证**；token 在 `~/.openclaw/.gateway_token`，或 `openclaw dashboard` 自动带 |
| 出网全失败但本地通 | `lsof -nP -iTCP:1097 -sTCP:LISTEN` | ZionLadder 没开 |
| 升级后服务不起来 | `/tmp/openclaw-update.log`、`/tmp/node-upgrade.log`、`~/.openclaw/logs/gateway-restart.log` | 升级中断留下 disabled 状态 |

### 核心坑：中断的升级会把 LaunchAgent 设成 disabled
被掐断的更新助手会让 job 在 launchd 里变成 **unloaded and disabled**。
此时 plist 文件还在、`launchctl load` **还返回成功**，但服务永远不会起来。
`openclaw doctor` 会点破这一条，并明确说"doctor 不会自动重新启用"。
修复：`openclaw gateway start`（它会自己 re-bootstrap）。

## 四、历史事件线

- **2026-06-03**：写过 `workspace/fix-openclaw-gateway.sh` —— 提取 token 存
  `~/.openclaw/.gateway_token` 并输出连接信息。**当时就把认证搞成 token 了**
  （脚本里明写"密码: (留空，使用令牌认证)"），说明 Tim 对"密码"的混淆不是第一次。
- **2026-09-21 07:17**：OpenClaw gateway 收到 stop 信号后停止（radio 最后一次成功 TTS 是 07:00）。
- **2026-09-22 15:29**：Mac 重启，gateway 被 launchd 拉回；但 radio 卡在 1097 代理没监听。
  → 修 radio：Tim 起了 ZionLadder → `launchctl kickstart -k com.tim.radio.server` → 复验
  `/api/test-deepseek` / `/api/weather` / `tts.synthesize()` 全通。
- **2026-09-22 18:48**：Tim 点升级 → 停服务 → npm 失败（Node 22 不满足）→ 第一次失败后把服务拉回来了。
- **2026-09-22 19:03-19:04**：`/tmp/node-upgrade.sh`（agent 写的、launchd 脱离执行）换 Node 到 v24.21.0
  → `openclaw update` **成功**（2026.6.1 → 2026.9.5）→ 但收尾 `openclaw doctor` 失败退出
  → 脚本 `launchctl load` 无效 → **gateway 从此不再起来**（真因：job 被 disabled）。
- **2026-09-24 21:14-21:18**：修复。路径：
  1. `openclaw update repair` → 推进被推迟的插件迁移（kimi / moonshot / feishu）
  2. 撞到拒绝继续的迁移：`credentials/feishu-alita-allowFrom.json` 指向 6 月已废弃的
     `alita` 账号（现只剩 `alita2` / `cli_aaaeb986…`）→ 读源码确认合并语义是**追加不是覆盖**
     （无锁死风险）→ 改名成 `feishu-alita-allowFrom.retired-20260924.json`（+`.bak`），内容未删
  3. `openclaw doctor --fix` → complete, exit 0
  4. `openclaw gateway start` → 重新启用 + 拉起 → PID 49075，验证 UI 200 / 飞书 ws / agent 回话
  5. 确认 Tim 的 open_id `ou_07c2cadc…` 仍在 `state/openclaw.sqlite` 的 allowFrom 里（没被迁移弄丢）
- **期间插曲**：21:17 另有一个 `/tmp/openclaw-fix.sh` 在同时修（先 `launchctl unload` 把网关掐了，
  导致我一次 agent 测试被 abort）。**这台机器上可能有别的 session 在同干活**，动手前先看
  `launchctl list | grep -i openclaw` 和 /tmp 下新出现的 `*.sh`。

## 五、遗留待办

**OpenClaw**（doctor 报出，未处理）
- feishu 插件版本漂移：插件 2026.6.1 vs 网关 2026.9.5
  → `openclaw plugins update feishu && openclaw gateway restart`
- memory search provider = openai 但无 API key → 语义召回不工作
- `agents/model-registry: Invalid models.json schema` + 向量维度未解析
- 可升 2026.9.6（这次 Node 够格，不会再卡）

**Tim'Radio**
- 代理依赖解耦（见第二节末）
- ZionLadder 不随开机启动 → 重启后 radio 必然静默半死

## 六、诊断入口速查

```
# OpenClaw
launchctl list | grep -i openclaw
launchctl print-disabled gui/501 | grep openclaw        # ← "在却起不来"先查这个
tail -f ~/Library/Logs/openclaw/gateway.log
/tmp/openclaw-update.log  /tmp/node-upgrade.log  /tmp/openclaw-fix.log   # 谁在何时动了什么
~/.openclaw/logs/gateway-restart.log
cd ~/.openclaw && openclaw doctor          # 先看，别急着 --fix

# Tim'Radio
tail -f /Users/tim/tim/logs/server.log     # 无时间戳，只能看尾部
tail -f /Users/tim/tim/logs/ncm.log
lsof -nP -iTCP:1097 -sTCP:LISTEN           # 翻墙工具是否在
```

**通则**：报"服务在跑却用不了"时，先验**第一跳**（端口/launchd 状态/依赖代理），再看上游业务逻辑。
