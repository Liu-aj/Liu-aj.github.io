---
title: 日志管理
description: 应用日志最佳实践
---

# 日志管理 📋

> 日志记录与管理

---

## Python 日志

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info('This is an info message')
```

## JavaScript 日志

```javascript
// 使用 pino
import pino from 'pino';
const logger = pino({ level: 'info' });

logger.info('hello world');
```

## 日志级别

| 级别 | 用途 |
|------|------|
| DEBUG | 开发调试 |
| INFO | 一般信息 |
| WARNING | 警告 |
| ERROR | 错误 |
| CRITICAL | 严重 |

## 日志管理工具

- ELK (Elasticsearch + Logstash + Kibana)
- Loki + Grafana
- EFK (Elasticsearch + Fluentd + Kibana)

---

*好的日志是问题排查的关键*
