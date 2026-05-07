---
title: .gitignore
description: Git 忽略文件配置
tags:
- Git
- Gitignore
- 版本控制
---

# .gitignore 📄

> Git 忽略文件配置

---

## 通用模板


# 依赖
node_modules/
venv/
.venv/
__pycache__/

# 编译产物
*.pyc
*.class
*.o
*.so

# IDE
.vscode/
.idea/
*.swp
*.swo

# 环境配置
.env
.env.local

# 日志
*.log
npm-debug.log*

# 系统文件
.DS_Store
Thumbs.db
```

## Python

```bash
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
```

## Node.js

```bash
node_modules/
npm-debug.log*
yarn-debug.log*
```

---

*正确的 .gitignore 让仓库更干净*
