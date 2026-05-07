---
title: Kubernetes
description: K8s 容器编排
tags:
- Kubernetes
- K8s
- 容器编排
---

# Kubernetes ☸️

> 容器编排平台

***

## 核心概念

| 概念 | 说明 |
|------|------|
| Pod | 最小调度单位 |
| Service | 负载均衡 |
| Deployment | 应用部署 |
| Ingress | HTTP 路由 |

## 基本命令

```bash
# 部署
kubectl apply -f deployment.yaml

# 查看
kubectl get pods
kubectl get svc

# 日志
kubectl logs -f pod-name

# 进入容器
kubectl exec -it pod-name -- /bin/bash
```yaml

## YAML 示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 80
```

***

*Kubernetes 是云原生的核心*
