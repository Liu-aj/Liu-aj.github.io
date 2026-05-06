---
title: 负载均衡
description: 负载均衡策略
---

# 负载均衡 ⚖️

> 分发请求到多台服务器

---

## 算法

| 算法 | 说明 |
|------|------|
| Round Robin | 轮询 |
| Least Connections | 最少连接 |
| IP Hash | 同一 IP 同一服务器 |
| Weighted | 加权轮询 |

## Nginx 配置

```nginx
upstream backend {
    least_conn;
    server 192.168.1.101;
    server 192.168.1.102;
    server 192.168.1.103;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

---

*负载均衡提升系统可用性*
