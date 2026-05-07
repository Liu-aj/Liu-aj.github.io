---
title: Nginx 指南
description: Nginx Web 服务器配置
tags:
- Nginx
- Web服务器
- 反向代理
---

# Nginx 指南 🌐

> 高性能 Web 服务器

***

## 基本配置

### 反向代理
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```markdown

### SSL 配置
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
}
```

## 常用命令

```bash
nginx -t              # 测试配置
nginx -s reload      # 重载配置
nginx -s stop        # 停止
nginx                # 启动
```

***

*Nginx 是高性能 Web 服务器的首选*
