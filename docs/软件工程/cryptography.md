---
title: 密码学基础
description: 密码学基础知识
tags:
- 密码学
- Cryptography
- 安全
---

# 密码学基础 🔐

> 加密算法与安全基础

---

## 对称加密

### AES
- 分组密码
- 密钥长度：128/192/256位
- 模式：ECB/CBC/GCM

```python
from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_CBC, iv)
```markdown

## 非对称加密

### RSA
- 公钥加密，私钥解密
- 密钥长度：2048/4096位
- 用于密钥交换、数字签名

### ECC
- 椭圆曲线密码学
- 更短密钥，更高安全性
- ECDH, ECDSA

## 哈希

| 算法 | 输出 | 用途 |
|------|------|------|
| MD5 | 128位 | 校验（已不安全）|
| SHA-1 | 160位 | 校验（已不安全）|
| SHA-256 | 256位 | 密码存储 |
| bcrypt | 可变 | 密码存储 |

## 应用场景

- HTTPS：TLS/SSL
- 密码存储：bcrypt/Argon2
- 数字签名：RSA/ECDSA
- 密钥交换：ECDH

---

*密码学是信息安全的基石*
