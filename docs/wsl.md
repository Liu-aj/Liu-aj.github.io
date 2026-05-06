---
title: WSL 指南
description: Windows Subsystem for Linux
---

# WSL 指南 🪟

> Windows 上的 Linux 子系统

---

## 安装

```powershell
# 管理员运行
wsl --install

# 重启电脑后
wsl --install -d Ubuntu
```

## 基本使用

```bash
# 列出发行版
wsl -l -v

# 启动特定发行版
wsl -d Ubuntu

# 导出/导入
wsl --export Ubuntu ubuntu.tar
wsl --import Ubuntu-22.04 D:\WSL ubuntu.tar
```

## 文件访问

```bash
# 从 Windows 访问 Linux 文件
cd /mnt/c/Users/xxx

# 从 Linux 访问 Windows 文件
cd /home/username
```bash

## Docker in WSL

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 开启 Docker Desktop WSL integration
```

---

*WSL 让 Windows 也能愉快地使用 Linux*
