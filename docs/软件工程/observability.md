---
title: 可观测性
description: 日志/指标/追踪
tags:
- 可观测性
- Observability
- 监控
---

# 可观测性 👁️

> 理解系统行为

***

## 三要素

| 要素 | 工具 |
|------|------|
| 日志 (Logs) | ELK, Loki |
| 指标 (Metrics) | Prometheus, Grafana |
| 追踪 (Traces) | Jaeger, Zipkin |

## OpenTelemetry

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("operation") as span:
    span.set_attribute("key", "value")
    process()
```

***

*可观测性让系统更透明*
