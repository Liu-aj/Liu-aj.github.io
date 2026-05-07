---
title: 缓存策略
description: 缓存设计与策略
tags:
- 缓存
- Cache
- 性能优化
---

# 缓存策略 💾

> 提升性能

***

## 缓存策略

| 策略 | 说明 | 使用场景 |
|------|------|----------|
| Cache-Aside | 应用管理读写 | 通用 |
| Read-Through | 缓存自动加载 | 读多 |
| Write-Through | 同步写入 | 数据一致性 |
| Write-Behind | 异步写入 | 写入性能 |

## Redis 缓存

```python
# Cache-Aside
def get_user(user_id):
    user = cache.get(f'user:{user_id}')
    if user is None:
        user = db.query(user_id)
        cache.setex(f'user:{user_id}', 3600, user)
    return user
```

## 过期策略

- TTL (Time To Live)
- LRU (Least Recently Used)
- LFU (Least Frequently Used)

***

*缓存是性能优化的利器*
