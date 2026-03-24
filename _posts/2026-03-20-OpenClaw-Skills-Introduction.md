---
title: "深入理解 OpenClaw Skills：让 AI Agent 更智能的技能系统"
date: 2026-03-20
category: AI
tags: [OpenClaw, Skills, Agent]
---

## 什么是 OpenClaw Skills？

OpenClaw Skills 是 OpenClaw 框架中的一个核心特性，它为 AI Agent 提供了**可扩展的能力体系**。简单来说，Skill 就是预定义的工具或功能模块，让 Agent 能够执行特定任务，如读写文件、操作飞书文档、管理 GitHub Issue、执行系统命令等。

 Skills 的设计理念是**模块化**和**可复用**。每个 Skill 都是一个独立的功能单元，包含清晰的职责边界，Agent 可以根据任务需求动态调用相关 Skills。这种设计大大简化了 Agent 的开发流程，无需为每个新功能重新编写底层逻辑。

### Skills 的核心价值

- **开箱即用**：内置多个常用 Skills，覆盖文档管理、云盘操作、代码托管等领域
- **灵活扩展**：支持自定义 Skills，开发者可以按需创建新功能
- **智能选择**：Agent 能根据上下文自动匹配合适的 Skills
- **规范化接口**：统一的 Skill 定义格式，便于维护和协作

---

## Skills 分类：内置 Skill 与自定义 Skill

OpenClaw 提供了两类 Skills：内置 Skills 和自定义 Skills。

### 1. 内置 Skills

内置 Skills 是 OpenClaw 官方开发和维护的标准化功能模块，目前主要包括：

| Skill 名称 | 功能描述 |
|-----------|----------|
| feishu-doc | 飞书文档读写操作 |
| feishu-drive | 飞书云盘文件管理 |
| feishu-perm | 飞书文档权限管理 |
| feishu-wiki | 飞书知识库操作 |
| github | GitHub CLI 操作（Issues、PRs 等） |
| gh-issues | GitHub Issues 管理与自动化 |
| healthcheck | 系统安全检查与加固 |
| node-connect | OpenClaw 节点连接诊断 |
| skill-creator | 创建和编辑 AgentSkills |
| video-frames | 视频帧提取 |
| weather | 获取天气信息 |

这些内置 Skills 覆盖了日常开发运维的多个场景，可以直接调用。

### 2. 自定义 Skills

自定义 Skills 是开发者根据自身需求创建的 Skills。它们通常存储在特定目录下，遵循 OpenClaw 定义的规范。

自定义 Skills 的优势：
- 针对特定业务场景定制功能
- 可以复用团队沉淀的最佳实践
- 便于分享和协作

---

## 如何使用 Skills

在 OpenClaw 中使用 Skills 非常直观。以下是几种常见方式：

### 1. Agent 自动调用

当 Agent 处理任务时，系统会根据任务内容**自动匹配**合适的 Skills。例如，当用户请求获取天气信息时，系统会自动调用 `weather` Skill。

### 2. 手动指定 Skills

在某些场景下，可以显式指定使用某个 Skill：

```python
# 伪代码示例
agent.use_skill("feishu-doc", action="read", doc_token="xxx")
```

### 3. 通过命令行调用

部分 Skills 支持通过 OpenClaw CLI 直接调用：

```bash
openclaw skill list          # 列出所有可用 Skills
openclaw skill exec <name>   # 执行指定 Skill
```

### 4. 在对话中激活

在飞书等对话渠道中，可以直接提及需要的技能：

```
@AIContent 使用 weather 获取北京天气
```

---

## 如何创建自己的 Skill

创建自定义 Skill 需要遵循 OpenClaw 定义的规范。以下是完整步骤：

### 1. 创建 Skill 目录结构

每个 Skill 需要一个独立的目录，基本结构如下：

```
my-skill/
├── SKILL.md          # Skill 定义文件（必需）
├── scripts/          # 脚本目录（可选）
├── references/       // 参考文档（可选）
└── 其他资源文件
```

### 2. 编写 SKILL.md

`SKILL.md` 是 Skill 的核心定义文件，包含以下关键信息：

```markdown
# SKILL.md 示例

## 技能名称
my-custom-skill

## 功能描述
简短描述这个 Skill 做什么

## 使用场景
- 场景1
- 场景2

## 使用方法
具体的调用方式

## 注意事项
使用限制或注意事项
```

### 3. 定义 Skills 匹配规则

在 `SKILL.md` 中需要明确触发条件：

```markdown
## 触发条件
当用户提到以下关键词时激活：
- 关键词1
- 关键词2
```

### 4. 实现功能逻辑

根据 Skill 类型，功能实现可以是：
- **脚本文件**：Shell、Python 等可执行脚本
- **API 调用**：封装外部服务接口
- **复合操作**：组合多个内置 Skills

### 5. 注册和发布

创建完成后，将 Skill 目录放到正确位置即可自动注册：

```bash
# 通常放置在 ~/.openclaw/skills/ 目录下
cp -r my-skill ~/.openclaw/skills/
```

### 6. 使用 ClawHub 分享

如果想让更多用户使用你的 Skill，可以使用 ClawHub 工具发布：

```bash
clawhub publish my-skill
```

---

## 最佳实践建议

1. **单一职责**：每个 Skill 专注于一个功能领域
2. **清晰命名**：使用描述性的名称，便于识别
3. **完善文档**：SKILL.md 要写清楚使用方法和注意事项
4. **错误处理**：添加适当的异常捕获和提示
5. **版本管理**：对 Skill 进行版本标注，便于追踪更新

---

## 总结

OpenClaw Skills 为 AI Agent 提供了一套灵活、可扩展的能力体系。通过内置 Skills，开发者可以快速构建功能丰富的应用；通过自定义 Skills，可以针对特定场景进行深度定制。掌握 Skills 的使用和创建，是高效使用 OpenClaw 的关键。

随着社区的贡献，OpenClaw 的 Skills 生态将不断丰富，为 AI Agent 的能力边界拓展更多可能性。

---

*本文基于 OpenClaw 框架编写，更多信息请参考官方文档。*