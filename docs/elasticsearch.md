---
title: Elasticsearch
description: Elasticsearch 搜索引擎
---

# Elasticsearch 🔍

> 分布式搜索与分析引擎

---

## 基本概念

| 概念 | 说明 |
|------|------|
| Index | 相当于数据库 |
| Document | 相当于记录 |
| Shard | 分片，用于分布式 |

## CRUD

```bash
# 创建索引
PUT /my_index

# 插入文档
POST /my_index/_doc
{"title": "Hello", "content": "World"}

# 搜索
GET /my_index/_search
{"query": {"match": {"content": "hello"}}}
```

## 查询

```json
{
  "query": {
    "bool": {
      "must": [
        {"match": {"title": "elasticsearch"}}
      ],
      "filter": [
        {"range": {"date": {"gte": "2024-01-01"}}}
      ]
    }
  }
}
```

---

*Elasticsearch 是强大的搜索引擎*
