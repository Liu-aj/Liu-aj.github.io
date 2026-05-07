---
title: GitOps
description: GitOps 实践
tags:
- GitOps
- DevOps
- 自动化
---

# GitOps 🔄

> 以 Git 为核心的运维

***

## 原则

- 声明式基础设施
- Git 为唯一事实来源
- 自动同步

## ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: default
```

***

*GitOps 让部署更安全*
