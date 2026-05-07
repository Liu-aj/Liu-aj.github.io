---
title: 版本控制
description: Git 版本控制最佳实践
tags:
- 版本控制
- VCS
- Git
---

# 版本控制 🔄

> 版本控制最佳实践

---

## 分支策略

### GitFlow
```bash
  ↑
  ↑ merge
  ├── develop ←── feature
  │              ↑
  │              merge
  └── hotfix ←───↑
```

### 命名规范
```bash
feature/user-auth
bugfix/login-issue
hotfix/security-patch
```

## Commit 规范

```bash
# 格式
type(scope): subject

# 类型
feat: 新功能
fix: 修复
docs: 文档
style: 格式
refactor: 重构
test: 测试
chore: 杂项
```

## 常用操作

```bash
# 变基保持历史整洁
git rebase main

# 交互式变基
git rebase -i HEAD~3

# 选择性 cherry-pick
git cherry-pick <commit>
```

---

*好的版本控制让协作更顺畅*
