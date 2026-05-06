---
title: Prometheus 指南
description: Prometheus 监控系统
---

# Prometheus 指南 📊

> 云原生监控系统

---

## 安装

```bash
# 下载
wget https://github.com/prometheus/prometheus/releases/latest/download/prometheus-linux-amd64.tar.gz
tar xzf prometheus-*.tar.gz
```

## 配置

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

## 常用指标

| 指标 | 说明 |
|------|------|
| up | 目标是否在线 |
| cpu_seconds_total | CPU 使用时间 |
| memory_usage_bytes | 内存使用 |
| disk_read_bytes_total | 磁盘读取 |

---

*Prometheus 是云原生监控的标准*
