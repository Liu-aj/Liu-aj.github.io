---
layout: post
title: "Claude Code 安装与入门指南（国内踩坑版）"
date: 2026-03-19 14:00:00 +0800
category: AI
tags: [Claude-Code, Terminal, Installation]
---

# Claude Code 安装与入门指南（国内踩坑版）

## Claude Code 是什么？

Claude Code 是 Anthropic 官方推出的命令行 AI 编程助手，是 Claude 在终端中的直接化身。与传统的 IDE 插件不同，Claude Code 直接在你的终端中运行，可以：

- **理解整个代码库**：自动读取项目结构，理解文件间的关联
- **执行命令**：直接运行测试、构建、Git 操作等
- **编写和修改代码**：根据自然语言指令直接编辑文件
- **调试和排错**：分析错误日志，提供修复建议

简单来说，Claude Code 就像是雇佣了一个坐在你终端里的资深程序员——你用自然语言告诉他要做什么，他帮你完成。

## 环境要求

在安装 Claude Code 之前，请确保你的系统满足以下条件：

### 必需环境

| 环境 | 版本要求 | 检查命令 |
|------|---------|---------|
| Node.js | >= 18.x | `node -v` |
| npm | >= 9.x | `npm -v` |

### 推荐环境

- **操作系统**：macOS、Linux、Windows (WSL2)
- **终端**：iTerm2 (macOS)、Windows Terminal，或任意现代终端
- **Git**：用于版本控制操作

### 检查当前环境

```bash
# 检查 Node.js 版本
node -v
# 应该输出类似 v20.x.x

# 检查 npm 版本
npm -v
# 应该输出类似 10.x.x
```

如果尚未安装 Node.js，推荐使用 [nvm](https://github.com/nvm-sh/nvm) 或 [fnm](https://github.com/Schniz/fnm) 进行版本管理。

## 国内安装步骤（重点踩坑）

> ⚠️ **重要提示**：由于网络原因，国内用户直接安装会遇到各种问题。以下是经过验证的安装方案。

### 踩坑一：npm 官方源访问超时

**问题描述**：执行 `npm install -g @anthropic-ai/claude-code` 时，下载速度极慢或直接超时。

**解决方案**：切换到国内镜像源

```bash
# 方案一：临时使用淘宝镜像（推荐）
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com

# 方案二：永久设置镜像源
npm config set registry https://registry.npmmirror.com
npm install -g @anthropic-ai/claude-code

# 安装完成后改回官方源
npm config set registry https://registry.npmjs.org
```

### 踩坑二：二进制包下载失败

**问题描述**：某些依赖包包含原生模块，需要从 GitHub 或其他海外服务器下载二进制文件。

**解决方案**：设置代理或使用镜像

```bash
# 方案一：设置 HTTP 代理（如果有）
npm config set proxy http://127.0.0.1:7890
npm config set https-proxy http://127.0.0.1:7890

# 方案二：使用 node-gyp 镜像
npm config set node_gyp_mirror https://npmmirror.com/mirrors/node-gyp/

# 安装
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com

# 安装完成后清除代理设置
npm config delete proxy
npm config delete https-proxy
```

### 踩坑三：安装后命令找不到

**问题描述**：安装成功但执行 `claude` 提示 `command not found`。

**解决方案**：检查并配置 PATH

```bash
# 查看全局安装路径
npm config get prefix

# 常见的全局安装路径：
# macOS/Linux: /usr/local 或 ~/.npm-global
# Windows: C:\Users\<用户名>\AppData\Roaming\npm

# 将 npm 全局 bin 目录加入 PATH（以 bash 为例）
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 或使用 nvm 时
echo 'export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 完整安装脚本（国内用户推荐）

```bash
#!/bin/bash
# Claude Code 国内安装脚本

echo "🚀 开始安装 Claude Code..."

# 1. 备份原镜像源配置
ORIGINAL_REGISTRY=$(npm config get registry)
echo "📦 当前 npm 源: $ORIGINAL_REGISTRY"

# 2. 切换到淘宝镜像
npm config set registry https://registry.npmmirror.com
echo "✅ 已切换到淘宝镜像源"

# 3. 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 4. 恢复原镜像源配置
npm config set registry "$ORIGINAL_REGISTRY"
echo "✅ 已恢复原镜像源配置"

# 5. 验证安装
if command -v claude &> /dev/null; then
    echo "✅ Claude Code 安装成功！"
    echo "👉 运行 'claude' 启动"
else
    echo "❌ 安装可能有问题，请检查 PATH 配置"
fi
```

保存为 `install-claude-code.sh`，然后执行：

```bash
chmod +x install-claude-code.sh
./install-claude-code.sh
```

## 首次认证配置

### 获取 API Key

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 登录或注册账号
3. 进入 API Keys 页面
4. 创建新的 API Key

> ⚠️ **注意**：API Key 只显示一次，请妥善保存！不要将 Key 提交到代码仓库！

### 配置认证

首次运行 Claude Code 会引导你完成认证：

```bash
claude
```

系统会提示选择认证方式：

```
? Choose an authentication method:
  ❯ Anthropic API Key
    Anthropic Console (OAuth)
```

**国内用户推荐选择 API Key 方式**，因为 OAuth 需要访问 Anthropic 网页，可能会遇到网络问题。

选择 API Key 后，粘贴你的 Key 即可完成认证。

### 配置文件位置

认证信息存储在：

- **macOS/Linux**: `~/.claude/`
- **Windows**: `%USERPROFILE%\.claude\`

### 踩坑四：API 访问受限

**问题描述**：认证成功后，执行操作时提示网络错误或超时。

**解决方案**：配置 API 代理

```bash
# 方法一：环境变量（推荐）
export ANTHROPIC_BASE_URL=https://your-proxy-domain.com/v1
export ANTHROPIC_API_KEY=your-api-key

# 方法二：使用第三方 API 代理服务
# 一些国内服务商提供 API 转发服务，使用时注意：
# 1. 选择信誉良好的服务商
# 2. 了解数据安全政策
# 3. 注意费用和限制
```

或者创建配置文件 `~/.claude/config.json`：

```json
{
  "apiKey": "your-api-key",
  "baseUrl": "https://your-proxy-domain.com/v1"
}
```

## 快速入门

### 基础命令

```bash
# 启动 Claude Code（在项目目录下）
claude

# 指定工作目录
claude /path/to/project

# 使用特定模型
claude --model claude-sonnet-4-20250514

# 查看帮助
claude --help

# 查看版本
claude --version
```

### 常用交互示例

启动 Claude Code 后，你可以用自然语言与之交互：

```
> 帮我看看这个项目的结构

> 解释一下 src/index.js 的主要逻辑

> 给这个函数添加单元测试

> 找出代码中的 TODO 注释并整理成列表

> 帮我重构这个组件，使用 TypeScript

> 运行测试并修复失败的用例
```

### 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 取消当前操作 |
| `Ctrl+D` | 退出 Claude Code |
| `↑` / `↓` | 浏览历史命令 |
| `Tab` | 自动补全 |

### 项目配置文件

在项目根目录创建 `CLAUDE.md` 文件，可以为 Claude Code 提供项目上下文：

```markdown
# 项目说明

这是一个 React + TypeScript 项目。

## 技术栈
- React 18
- TypeScript 5
- Vite

## 代码规范
- 使用 ESLint + Prettier
- 组件使用函数式组件 + Hooks
- 样式使用 Tailwind CSS

## 注意事项
- 不要修改 .env 文件
- 测试使用 Vitest
```

## 常见问题解决

### 问题一：网络连接超时

**错误信息**：

```
Error: connect ETIMEDOUT
```

**解决方案**：

1. 检查网络连接
2. 配置代理（见上文"踩坑四"）
3. 使用稳定的 API 代理服务

### 问题二：认证失败

**错误信息**：

```
Authentication failed. Please check your API key.
```

**解决方案**：

1. 确认 API Key 正确且未过期
2. 检查是否有足够的 API 配额
3. 尝试重新配置认证：

```bash
# 清除现有认证
rm -rf ~/.claude/

# 重新启动并认证
claude
```

### 问题三：内存不足

**错误信息**：

```
JavaScript heap out of memory
```

**解决方案**：

```bash
# 增加 Node.js 内存限制
export NODE_OPTIONS="--max-old-space-size=8192"
claude
```

### 问题四：权限错误

**错误信息**：

```
EACCES: permission denied
```

**解决方案**：

```bash
# 方案一：使用 sudo（不推荐）
sudo npm install -g @anthropic-ai/claude-code

# 方案二：修改 npm 全局目录权限（推荐）
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 重新安装
npm install -g @anthropic-ai/claude-code
```

### 问题五：版本兼容问题

**错误信息**：

```
Error: Node.js version not supported
```

**解决方案**：

```bash
# 使用 nvm 切换 Node.js 版本
nvm install 20
nvm use 20

# 或使用 fnm
fnm install 20
fnm use 20
```

## 与 Cursor 对比

Claude Code 和 Cursor 都是目前热门的 AI 编程工具，但它们有本质区别：

| 特性 | Claude Code | Cursor |
|------|-------------|--------|
| **形态** | 命令行工具 | IDE（基于 VSCode） |
| **使用方式** | 自然语言对话 | 内嵌编辑器 + 快捷键 |
| **适用场景** | 服务器、远程开发、CI/CD | 日常开发、UI 密集型项目 |
| **模型** | Claude 系列 | 多模型（Claude/GPT-4 等） |
| **学习曲线** | 较低，命令行即可上手 | 需要适应新的 IDE |
| **自定义** | 通过 CLAUDE.md 配置 | Rules + .cursorrules |
| **上下文** | 自动理解项目结构 | 需要主动引用文件 |
| **执行能力** | 可直接执行命令 | 主要生成代码片段 |

### 各自优势

**Claude Code 优势**：

- 🚀 **命令行原生**：适合服务器环境、SSH 远程开发
- 🔄 **自动化执行**：可以直接运行测试、构建、Git 操作
- 📁 **项目理解**：自动读取整个代码库，理解文件关联
- 🎯 **专注模式**：没有 IDE 界面干扰，专注对话

**Cursor 优势**：

- 🎨 **可视化编辑**：实时代码补全和高亮
- ⌨️ **快捷键丰富**：Cmd+K 生成，Cmd+L 对话
- 🖱️ **鼠标友好**：点选代码上下文更直观
- 📦 **生态完整**：完整 IDE 功能，插件丰富

### 如何选择？

- **选择 Claude Code**：如果你习惯命令行、经常 SSH 远程开发、需要在 CI/CD 中集成 AI 辅助
- **选择 Cursor**：如果你喜欢可视化 IDE、需要频繁编辑 UI 代码、习惯 VSCode 工作流
- **两者都用**：为什么不呢？Cursor 处理日常开发，Claude Code 处理服务器任务

## 总结

Claude Code 作为 Anthropic 官方推出的命令行 AI 编程助手，为开发者提供了一种全新的编程方式。对于国内用户，安装过程中的主要障碍是网络问题，通过配置镜像源和代理可以顺利解决。

掌握 Claude Code 后，你会发现它不仅是一个代码生成工具，更是一个理解你项目、帮你执行任务的智能助手。从简单的代码解释到复杂的项目重构，Claude Code 都能成为你得力的编程伙伴。

---

**相关链接**：

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [Anthropic Console](https://console.anthropic.com/)
- [npm 镜像站](https://npmmirror.com/)

---

*本文持续更新，如有问题欢迎留言讨论。*