---
title: 限流
description: API 限流策略
---

# 限流 🚦

> 保护系统资源

---

## 算法

### 固定窗口
```bash
```

### 滑动窗口
```bash
```

### 令牌桶
```python
import time

class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
    
    def consume(self, tokens=1):
        now = time.time()
        self.tokens = min(
            self.capacity,
            self.tokens + (now - self.last_update) * self.rate
        )
        self.last_update = now
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
```

---

*限流保护系统稳定性*
