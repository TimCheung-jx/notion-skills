# 本机服务运维（OpenClaw / Tim'Radio）

> 覆盖 Tim 这台 Mac mini 上常驻的两套自建服务。硬件/系统：`Tim的Mac mini`，macOS 26.x，用户 `tim`。
> 最后更新：2026-09-30

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

### CLI 代理（2026-10-01 补上）

**macOS 的系统代理只有 GUI 应用读；curl / git / npm / brew 只认环境变量
`http_proxy` / `https_proxy` / `all_proxy`。**
ZionLadder 只设系统代理 → 浏览器能开 GitHub，终端里 curl/git 直连照样 TCP 超时。
症状：`scutil --proxy` 一切正常，但 `curl -I https://github.com` 卡死到超时。

修复：`~/.zshrc` 末尾追加（备份 `~/.zshrc.bak-20261001`）——

```bash
if nc -z -w 1 127.0.0.1 1097 2>/dev/null; then
  export http_proxy=http://127.0.0.1:1097
  export https_proxy=http://127.0.0.1:1097
  export all_proxy=socks5://127.0.0.1:1097
fi
export no_proxy=localhost,127.0.0.1,::1
```

`nc -z` 探活是刻意的：**代理没开时降级直连**，不会像 Tim'Radio 那样把全部 CLI 拖死。
改了 `.zshrc` 之后**已开的终端要重开或 `source ~/.zshrc`** 才生效。

## 三、故障对照表

| 症状 | 先查 | 常见结论 |
|---|---|---|
| 网页/客户端连不上，进程却"在" | `launchctl print-disabled gui/501 \| grep openclaw` | **被标记 disabled** —— 见下节 |
| 服务完全没进程 | `launchctl list \| grep -i <label>`；`ps`；`lsof -nP -iTCP:<port> -sTCP:LISTEN` | job 未 bootstrap → `openclaw gateway start` / `gateway install` |
| UI 能开但连不上、要求"登录" | 日志里找 `control-ui-build-mismatch` / `phase=auth_validated` | 页面缓存旧版 → **硬刷新**（Cmd+Shift+R）；别去动认证 |
| 忘了"登录密码" | 它没有密码 | **Control UI 是 token 认证**；token 在 `~/.openclaw/.gateway_token`，或 `openclaw dashboard` 自动带 |
| 出网全失败但本地通 | `lsof -nP -iTCP:1097 -sTCP:LISTEN` | ZionLadder 没开 |
| 浏览器能上外网，终端 curl/git 全超时 | `env \| grep -i proxy` | **CLI 没接系统代理** —— 见第二节「CLI 代理」 |
| 升级后服务不起来 | `/tmp/openclaw-update.log`、`/tmp/node-upgrade.log`、`~/.openclaw/logs/gateway-restart.log` | 升级中断留下 disabled 状态 |
| 全部对话报 401 / 飞书不回 | `grep "401 Authentication Fails" ~/Library/Logs/openclaw/gateway.log` 看 key 尾号 | key 失效；**改 config 往往没用**，见五 |
| 改了 key 还是不生效 | `~/.openclaw/service-env/ai.openclaw.gateway.env` 里的 `*_API_KEY` | 环境变量压过 config |
| `config set` 报 config invalid | `openclaw config validate` 看具体字段 | 先 `doctor --fix` 解锁，见六 |

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
- **2026-09-30 20:08~20:30**：deepseek key 失效（18:28 起 401，尾号 5ef7），**飞书和 web 全部哑掉**。
  排查中发现两个独立坑，见下节「OpenClaw API key 的层级」。
  最终修复：换 key + 重装服务 + 补 moonshot provider + 配 fallback 链。

## 五、OpenClaw API key 的层级（2026-09-30 吃到的坑）

**改 `openclaw.json` 里的 `models.providers.*.apiKey` 经常没用，因为环境变量优先级更高。**

生效顺序（高 → 低）：

1. **`~/.openclaw/service-env/ai.openclaw.gateway.env`** —— LaunchAgent 启动时 source，
   `DEEPSEEK_API_KEY` 在这里。**这是实际生效的那一层。**
2. `~/.openclaw/.env` —— CLI 命令读它
3. `openclaw.json` → `models.providers.<p>.apiKey`（被上面两层压住）

- 该文件头写明 "Generated by OpenClaw. Do not edit while the gateway service is installed."
  → **不要手改**，正确做法是在 shell 里 export 新值后重装服务：
  ```bash
  export DEEPSEEK_API_KEY='sk-新key' && openclaw gateway install --force
  ```
  它会用当前环境重新生成 service-env。
- **`config set` 提示 "Change will apply without restarting the gateway" 不可信** ——
  apiKey 改了照样用旧的，必须 `openclaw gateway restart` 或重装服务。
- 验证 key 本身是否有效，别在 OpenClaw 里绕：直接 curl 打官方 API（`api.deepseek.com` 直连可通）。
  这一步能一刀切开"key 坏"和"配置没生效"。

### moonshot 和 kimi 是两个完全不同的 provider

| | Moonshot 开放平台 | Kimi Coding |
|---|---|---|
| ref 前缀 | `moonshot/` | `kimi/` |
| 端点 | `https://api.moonshot.cn/v1`（国内）/ `.ai`（国际） | `https://api.kimi.com/coding/v1` |
| 协议 | OpenAI-compatible | Anthropic Messages |
| key | 不通用 | 不通用 |

- **国内 key 用 `moonshot/` + `api.moonshot.cn`**。走默认的 `.ai` 会 401（key 不认国际站）。
- `moonshot` provider 需要在 `models.providers.moonshot` 里显式定义（配置里原先没有），
  否则它落到插件默认的 `.ai`。
- `kimi/` provider 指向 `api.moonshot.cn` 会 400（协议/端点都不对）。Tim 没有 kimi.com 订阅，
  所以 `kimi/` 这条基本用不了，`modelPolicy.allow` 里还留着 `kimi/kimi-k2.7-code`（可清理）。

## 六、配置被判 invalid 会连锁锁死命令（2026-09-30）

`channels.feishu.streaming` 是个空对象 `{}`（升级残留，新版要求 boolean）。
后果不是"飞书流式不生效"，而是 **整个 config 判为 invalid**，然后
`config get/set/patch`、`models auth *`、`gateway start` **全部拒绝执行** ——
形成"想修都不知道从哪下手"的死锁。

- 唯一出口是 `openclaw doctor --fix`（validate / doctor / audit / status / logs 在 invalid 时仍可跑）。
- **`doctor --fix` 需要先停网关**，否则撞 `OpenClawAgentDatabaseLeaseActiveError`。
  它会自己停，但**可能拉不回来**（报 `Gateway could not be restored`）—— 那就手动
  `openclaw gateway start` 补一下。停网关期间服务是断的，要跟 Tim 打招呼。

## 七、遗留待办

**OpenClaw**（doctor 报出，未处理）
- feishu 插件版本漂移：插件 2026.6.1 vs 网关 2026.9.5
  → `openclaw plugins update feishu && openclaw gateway restart`
- memory search provider = openai 但无 API key → 语义召回不工作
- `agents/model-registry: Invalid models.json schema` + 向量维度未解析
- 可升 2026.9.6（这次 Node 够格，不会再卡）

**OpenClaw 模型现状（2026-09-30 修完）**
- 主模型 `deepseek/deepseek-v4-pro`；**fallback 链**：`moonshot/kimi-k2.6` → `moonshot/kimi-k3`
- `moonshot` provider 已补进 `models.providers`，baseUrl 指向 **`api.moonshot.cn`**（国内站）
- 可清理：`modelPolicy.allow` 里还留着没用的 `kimi/kimi-k2.7-code`，
  `models.providers.kimi` 那段配置也是错的（kimi coding 要 api.kimi.com，Tim 没订阅）
- **凭据散落位置（2026-09-30 已清理）**：旧 key 曾同时存在于 6 个 `openclaw.json.*` 备份、
  `.env.bak`、`.zshrc` 的 `claude-ds` alias、`state/openclaw.sqlite`。
  备份已移入废纸篓；**sqlite 是运行库不能碰**；`.zshrc` 那处待 Tim 决定。
  → **换 key 时记得全盘 `grep -rl "<旧key>" ~/.openclaw/ ~/.zshrc`，别只改一处**

**Tim'Radio**
- 代理依赖解耦（见第二节末）
- ZionLadder 不随开机启动 → 重启后 radio 必然静默半死

## 八、诊断入口速查

```
# OpenClaw
launchctl list | grep -i openclaw
launchctl print-disabled gui/501 | grep openclaw        # ← "在却起不来"先查这个
tail -f ~/Library/Logs/openclaw/gateway.log
grep "401 Authentication Fails" ~/Library/Logs/openclaw/gateway.log | tail -3   # 看实际用的 key 尾号
/tmp/openclaw-update.log  /tmp/node-upgrade.log  /tmp/openclaw-fix.log   # 谁在何时动了什么
~/.openclaw/logs/gateway-restart.log
cd ~/.openclaw && openclaw doctor          # 先看，别急着 --fix
~/.openclaw/service-env/ai.openclaw.gateway.env   # ← 真正生效的 env（压过 openclaw.json）
grep -rl "<旧key>" ~/.openclaw/ ~/.zshrc   # 换凭据前先找全部落点

# Tim'Radio
tail -f /Users/tim/tim/logs/server.log     # 无时间戳，只能看尾部
tail -f /Users/tim/tim/logs/ncm.log
lsof -nP -iTCP:1097 -sTCP:LISTEN           # 翻墙工具是否在
```

**通则**：报"服务在跑却用不了"时，先验**第一跳**（端口/launchd 状态/依赖代理），再看上游业务逻辑。
