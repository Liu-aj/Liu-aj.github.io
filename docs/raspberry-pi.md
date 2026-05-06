---
title: 树莓派
description: 树莓派开发指南
---

# 树莓派 🖥️

> 树莓派开发与配置指南

---

## 型号对比

| 型号 | CPU | 内存 | 接口 | 适用场景 |
|------|-----|------|------|----------|
| Pi 4 B | 1.5GHz 四核 | 2-8GB | USB3/GbE | 桌面/服务器 |
| Pi 3 B+ | 1.4GHz 四核 | 1GB | USB2 | 通用 |
| Pi Zero 2 W | 1GHz 四核 | 512MB | Micro USB | IoT |

## 系统安装

### 刷写系统
```bash
# 使用 Raspberry Pi Imager
# 下载：https://www.raspberrypi.com/software/

# 或使用命令行
sudo dd if=raspberrypi.img of=/dev/sdX bs=4M status=progress
```

### 首次配置
```bash
# 扩展文件系统
sudo raspi-config → Advanced → Expand Filesystem

# 启用 SSH
sudo systemctl enable ssh
sudo systemctl start ssh

# 更改密码
passwd pi
```

## 常用配置

### Wi-Fi
```bash
# 编辑 wpa_supplicant.conf
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

### 静态 IP
```bash
# 编辑 dhcpcd.conf
sudo nano /etc/dhcpcd.conf

interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1
```

## Docker 安装

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker pi
```

## 相关文档

- [OpenClaw 安装](/)
- [Home Assistant](/)
