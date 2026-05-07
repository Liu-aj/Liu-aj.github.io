---
title: 网络基础
description: 网络基础知识
tags:
- 网络
- Networking
- 基础
---

# 网络基础 🌐

> 整理网络基础知识

---

## OSI 模型

| 层 | 协议 | 设备 |
|----|------|------|
| 应用层 | HTTP/FTP/SMTP | 网关 |
| 传输层 | TCP/UDP | 防火墙 |
| 网络层 | IP | 路由器 |
| 数据链路层 | Ethernet | 交换机 |
| 物理层 | 光纤/电缆 | 集线器 |

## 常用协议

### HTTP/HTTPS
```bash
请求 → 请求行/头/体
响应 → 状态码/头/体
```

### MQTT
```bash
发布 → Topic → Broker → 订阅
```

### WebSocket
```bash
握手 → 双向通信 → 心跳 → 关闭
```

## 网络诊断

| 命令 | 用途 |
|------|------|
| ping | 测试连通性 |
| traceroute | 路由追踪 |
| netstat | 端口状态 |
| curl | HTTP 请求 |
| wireshark | 抓包分析 |

---

*网络是互联网的基础*
