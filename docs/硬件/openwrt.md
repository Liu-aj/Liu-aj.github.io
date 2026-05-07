---
title: OpenWRT
description: OpenWRT 路由器系统
tags:
- OpenWRT
- 路由器
- Linux
- 网络
---

# OpenWRT 🌐

> OpenWRT 路由器系统配置与使用

***

## 基本配置

### 登录
- 默认 IP：192.168.1.1
- 用户：root
- 密码：（空，首次登录需设置）

### 网络配置
```bash
# 编辑 /etc/config/network
config interface 'wan'
    option device 'br-lan'
    option proto 'dhcp'

config interface 'lan'
    option device 'br-lan'
    option proto 'static'
    option ipaddr '192.168.1.1'
    option netmask '255.255.255.0'
```bash

## 软件包

### 常用软件
```bash
opkg update
opkg install vim htop curl wget
opkg install luci-app-openvpn
```

## 相关文档

- [Zigbee2MQTT](/)
- [网络基础](/)
