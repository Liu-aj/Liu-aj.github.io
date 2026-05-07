---
title: Git 进阶
description: Git 高级用法
tags:
- Git
- 版本控制
- 进阶
---

# Git 进阶 📚

> 整理 Git 高级用法

***

## 多人协作

### 分支策略
```bash
# GitFlow
main ←───────────────←─── production
  ↑                       ↑
  │ merge                 │ merge
  ├── develop ←─── feat/ │─────── fix/
```bash

### Code Review
```bash
# 创建 PR
git push -u origin feature/xxx

# Rebase 保持历史整洁
git rebase main

# 交互式 rebase
git rebase -i HEAD~3
```

## 高级操作

### Cherry-pick
```bash
# 选择性合并提交
git cherry-pick <commit-hash>
```markdown

### Stash
```bash
# 保存工作进度
git stash
git stash pop  # 恢复并删除

# 命名 stash
git stash save "work in progress"
```

### Submodule
```bash
# 添加子模块
git submodule add <url> <path>

# 初始化子模块
git submodule update --init
```bash

## Git 钩子

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running tests..."
npm test
```

***

*Git 是版本控制的利器*
