---
title: Grafana 指南
description: Grafana 可视化仪表盘
tags:
- Grafana
- 监控
- 可视化
---

# Grafana 指南 📈

> 数据可视化与仪表盘

---

## 数据源

```yaml
# 支持的数据源
- Prometheus
- InfluxDB
- Elasticsearch
- MySQL
- PostgreSQL
- Loki
```markdown

## Dashboard

### 查询示例 (Prometheus)
```promql
# CPU 使用率
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 内存使用率
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
```

## 告警

```yaml
groups:
  - name: example
    rules:
      - alert: HighCpu
        expr: cpu_usage > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High CPU usage detected
```

---

*Grafana 让监控数据可视化*
