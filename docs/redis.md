---
title: Redis 指南
description: Redis 内存数据库
---

# Redis 指南 ⚡

> 高性能内存键值存储

---

## 数据类型

| 类型 | 命令 | 用途 |
|------|------|------|
| String | GET/SET | 缓存 |
| Hash | HSET/HGET | 对象 |
| List | LPUSH/RPOP | 队列 |
| Set | SADD/SMEMBERS | 去重 |
| Sorted Set | ZADD/ZRANGE | 排行 |

## 常用命令

```bash
# String
SET key value
GET key

# Hash
HSET user:1 name "John" email "john@example.com"
HGET user:1 name

# List
LPUSH queue "task1"
RPOP queue

# 过期时间
SETEX token 3600 "abcdef"
```

## 应用场景

- 会话缓存
- 页面缓存
- 消息队列
- 排行榜

---

*Redis 让缓存变得简单*
