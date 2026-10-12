# codex-pro-handoff

让 Codex 把用户要求的规划或验收材料交给普通 ChatGPT Pro，再读取真实回复的可安装技能包。源自已有 `chatgpt-pro-handoff` 技能的通用化整理；不附带调度器、后台服务或模型代理。

## 安装

需要 Python 3.9 或更高版本，仅使用标准库。在本工程根目录运行：

```sh
python3 scripts/check_package.py
python3 -m unittest discover -s tests -v
python3 scripts/install.py
```

默认安装到 `~/.codex/skills/chatgpt-pro-handoff`。自定义位置：

```sh
python3 scripts/install.py --skills-dir /path/to/skills
```

安装器只复制 `skills/chatgpt-pro-handoff`。目标已存在时一律拒绝，包括目录、文件和悬空符号链接；不会更新或替换已有技能。技能根目录是文件或符号链接时也报错。安装完成后，由宿主按其技能发现机制加载。

## 使用和能力边界

示例：`$chatgpt-pro-handoff 只让普通 ChatGPT Pro 验收我提供的 diff 和测试证据，不规划、不实施。`

用户自行选择并确认 Pro 聊天。优先复用已确认的普通 Chat；宿主不支持直接交接时，可在内置浏览器确认登录和 Pro 模型。普通 Chat、ChatGPT Work 和 Codex 聊天不能混用。详见 [使用说明](docs/usage.md) 和 [提示示例](examples/prompts.md)。

直接路径依赖宿主提供 `list_threads`、`send_message_to_thread`、`read_thread`，且支持普通 ChatGPT Chat。这些不是通用公开 API，本包不会提供或启用它们。只有技能文件和本地安装入口，并不意味着所在宿主支持 Pro 交接。

本包测试验证安装、拒绝覆盖和常见隐私模式检查；没有运行真实 Pro 对话。历史 2026 年 9 月 20/21 日观察不代表当前模型、配额或上传限制。Pro 验收只能评价获得的证据；完整无人值守闭环未实测，不保证节省比例。上传与等待能力需按实际宿主核实。

[AI Context Linker](https://github.com/xhonye/AI-Context-Linker) 是可选外部项目，本包不包含其源码，也不安装它。上下文文件需人工或代理审阅，不会自动附加给 Pro。

## 许可

尚未指定许可证；本工程没有附加 MIT、Apache 或其他许可证。公开发布不自动授予通用再分发或修改许可，再分发权限需另行向权利人确认。

## English overview

An installable Codex skill for sending scoped planning or review evidence to a user-selected ordinary ChatGPT Pro conversation and reading its actual reply. Requires Python 3.9+ with no third-party dependencies. Install with `python3 scripts/install.py`; existing targets are never overwritten.

Direct handoff depends on host-specific tools, not a public API. A supported built-in browser can be used when needed. This package provides no scheduler, proxy, cookies or default conversation bindings. Live Pro interaction and a fully unattended loop are not verified by the package tests. No license has been selected; redistribution permissions require separate confirmation.
