---
title: DevOps 指南
description: DevOps 最佳实践
tags:
- DevOps
- 开发运维
- 实践
---

# DevOps 指南 🚀

> 整理 DevOps 最佳实践

---

## CI/CD 流程

```bash
              ↓
           质量门禁
              ↓
           自动回滚
```

### GitHub Actions
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest
```markdown

## 容器化

### Docker 最佳实践
- 使用多阶段构建
- 使用 .dockerignore
- 非 root 用户运行
- 最小化基础镜像

### Kubernetes
- 使用命名空间隔离
- 设置资源限制
- 配置健康检查
- 使用 ConfigMap/Secret

## 基础设施即代码

### 工具选择
- Terraform
- Pulumi
- Ansible

## 监控与日志

- ELK Stack
- Prometheus + Grafana
- Loki

---

*自动化是 DevOps 的核心*
