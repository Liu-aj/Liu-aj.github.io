---
title: Service Mesh
description: 服务网格
---

# Service Mesh 🌐

> 微服务网络层

---

## 功能

| 功能 | 说明 |
|------|------|
| 流量管理 | 路由/负载均衡 |
| 安全 | mTLS 加密 |
| 可观测性 | 监控/追踪 |
| 弹性 | 超时/重试/熔断 |

## Istio

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
```

---

*Service Mesh 让微服务更安全*
