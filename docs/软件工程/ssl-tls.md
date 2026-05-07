---
title: SSL/TLS 证书
description: SSL/TLS 证书配置指南
tags:
- SSL
- TLS
- 安全
- 证书
---

# SSL/TLS 证书 🔐

> 安全的 HTTPS 配置

---

## Let's Encrypt

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 申请证书
sudo certbot --nginx -d example.com

# 自动续期
sudo certbot renew --dry-run
```

## 自签名证书

```bash
# 生成私钥
openssl genrsa -out server.key 2048

# 生成证书
openssl req -new -x509 -key server.key -out server.crt -days 365

# 合并
cat server.crt server.key > server.pem
```

## Nginx 配置

```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
}
```

---

*HTTPS 是现代网站的基本要求*
