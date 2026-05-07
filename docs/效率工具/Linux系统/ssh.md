---
title: SSH 指南
description: SSH 安全连接指南
tags:
- SSH
- 远程登录
- 安全
- Linux
---

# SSH 指南 🔐

> Secure Shell - 安全远程连接

***

## 基本用法

```bash
# 密码登录
ssh user@host

# 指定端口
ssh -p 2222 user@host

# 密钥登录
ssh -i ~/.ssh/key_name user@host
```markdown

## 密钥管理

### 生成密钥
```bash
ssh-keygen -t ed25519 -C "your_email"
ssh-keygen -t rsa -b 4096 -C "your_email"
```bash

### 复制公钥
```bash
ssh-copy-id user@host
# 或手动
cat ~/.ssh/id_rsa.pub | ssh user@host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## SSH Config

```bash
# ~/.ssh/config
Host alias
    HostName hostname
    User username
    Port 22
    IdentityFile ~/.ssh/key
    ForwardAgent yes
```bash

## 隧道转发

### 本地端口转发
```bash
ssh -L 8080:remote:80 user@host
```bash

### 远程端口转发
```bash
ssh -R 8080:local:80 user@host
```

***

*SSH 是远程开发的必备技能*
