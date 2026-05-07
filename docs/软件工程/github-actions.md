---
title: GitHub Actions
description: GitHub CI/CD 自动化
tags:
- GitHub Actions
- CI/CD
- 自动化
---

# GitHub Actions ⚡

> GitHub 内置 CI/CD

---

## 基本配置

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest
```

## 常用 Action

| Action | 用途 |
|--------|------|
| actions/checkout | 拉取代码 |
| actions/setup-python | Python 环境 |
| actions/cache | 缓存依赖 |

---

*GitHub Actions 让 CI/CD 变得简单*
