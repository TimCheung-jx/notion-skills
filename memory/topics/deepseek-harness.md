# DeepSeek Harness (dsh) 换皮项目

> Tim 拿官方桌面版做界面改造，之后再逐步自造插件。最后更新：2026-10-02

## 状态速览

- **已装**：官方桌面版 `0.2.0-rc.2` → `/Applications/DeepSeek Harness.app`（2026-10-01 装并启动验证通过）
- **源码**：`workspace/1001-deepseek-harness`（depth-1 浅克隆；要更新得挂代理，见第五节）
- **当前阶段**：Tim 在翻 `apps/desktop` 壳源码，皮肤插件尚未动工
- **下一步**：把 Rezig「高山冷光」转成皮肤插件的 `--dsw-alias-*` 令牌

## 一、许可与「能不能改」——分层看

| 层 | 位置 | 许可 | 能不能改 |
|---|---|---|---|
| 内核 dsh | 仓库 `packages/` | MIT | 随便改 |
| Web UI | `packages/client/` | MIT | 随便改 |
| **桌面壳** | `apps/desktop/`（Electron） | **MIT**（`package.json` 写死，无独立 LICENSE） | **能改、能重新打包** |
| 官方安装包 | `download.deepseek.com` | 编译产物 | 改不了；要改只能自己 build |

- 根 `LICENSE` = MIT, (c) 2026 DeepSeek，覆盖整个 monorepo
- ⚠️ **商标不跟着 MIT 走** —— 改完可以发，但不能带 DeepSeek 的名字和 logo
- `vendor/` 下是 pinned 的第三方源码（Cordis 等），各自许可，见 `THIRD_PARTY_NOTICES.md`

## 二、桌面壳解剖

- Electron 壳包**完整的 dsh Web 应用**，通过 `dsh-app://app/` 加载打包好的 Web 入口
- Host 进程是 `--expose-internals` 起的 `dsh-desktop-host`（Electron RunAsNode 模式）
- 桌面默认端口 **19387**（Web 版是 3080）
- 目录：`src/`（主进程）、`renderer/`（升级弹窗等壳层 UI）、`installer/`、`resources/`、`scripts/`
- profile 落在 `~/.dsh/profiles/desktop`（`cordis.yml` / `cordis.patch.yml` / `package.json` / `pnpm-workspace.yaml`）
- **桌面版与 CLI 共用 `$DSH_HOME` 的会话/配置/凭据，但可执行包、插件激活、lockfile 各自独立**

### 构建命令

```sh
pnpm run dev:desktop                    # 开发模式跑（改 UI 用这个）
pnpm run package:desktop:mac:arm64:dir  # 出未签名可运行目录（自用）
pnpm run package:desktop:mac:arm64      # 正式打包
```

- ⚠️ 正式打 macOS 包要 **Apple Developer ID 证书 + 公证**（Tim 没有）→ 自用只能走 `:dir`
- → **换皮别 fork 壳，走插件层**，升级无痛

## 三、皮肤插件 API（换皮的全部弹药）

权威源：`packages/client/ui-theme/src/client/index.ts`

服务 `ctx.theme`（ThemeRuntime）：

| 方法 | 用途 |
|---|---|
| `overrideTokens(source, tokens)` | 叠加覆盖层，返回 disposer，卸载即还原 —— **换皮用这个** |
| `register({ id, colorScheme, tokens })` | 注册一整套新主题 |
| `setTheme(id)` / `getTheme()` / `exportInspectTokens()` | 切换 / 读取 / 导出令牌目录 |
| 事件 `theme/change` | 主题变化订阅（偏好切换、注册表变化、系统明暗翻转都会触发） |

**14 个可覆盖令牌**（`--dsw-alias-*`）。**全部强制 `{ light, dark }` 双值** ——
传裸字符串会抛教学式 TypeError（防止切色时糊掉）：

| 类别 | 令牌 |
|---|---|
| 背景 | `bg-base` `bg-layer-1` `bg-layer-2` `bg-overlay` |
| 边框 | `border-l1` `border-l2` |
| 文字 | `label-primary` `label-secondary` |
| 品牌 | `brand-primary` |
| 状态 | `state-error-primary` `state-idle-primary` `state-success-primary` `state-warn-primary` |
| 侧栏 | `specific-sidebar-fill` |

另有 `--dsw-font-family` 可覆盖（`packages/client/web/src/base.css` 里消费）。

设置项入口插槽：`settings.general.item`（ui-theme 自己就用它注册了 appearance / font-size
两行，order 10 和 11，是现成范本）。

**官方自带插件开发指南**：`packages/preset/agent-preset/skills/cordis-plugin-development/`

### 坑

- 靠 class 哈希命中元素的控件联动（字号之类），DSH 升级后会**静默失效**；只覆盖 token 才安全
- 壁纸这类大文件存 localStorage / IndexedDB，别塞进插件包

## 四、装插件的正确顺序

1. 先**启动一次**桌面版，让它初始化 profile（2026-10-01 已完成）
2. **完全退出** app
3. `dsh plugin --profile desktop add <包名>`
4. 重开桌面版生效

（`dsh` 命令可在 app 菜单「Manage dsh Command…」注册到 `/usr/local/bin/dsh`）

## 五、环境前提

- 这台机器**直连 GitHub 不通**，CLI 要挂 ZionLadder 代理
  → 已在 `~/.zshrc` 配好带探活的代理块，详见 `topics/local-services.md#cli-代理2026-10-01-补上`
- `download.deepseek.com` 直连可通，下载安装包不需要代理

## 六、已知限制（官方 README 写的）

- **Sign in 按钮是灰的**（account sign-in 未接通），只能填 API key
- 6 元赠金是登录送的（活动到 2026-10-06）—— 登录不通，估计得走网页端
