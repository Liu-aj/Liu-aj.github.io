---
title: PostgreSQL 指南
description: PostgreSQL 数据库
tags:
- PostgreSQL
- 数据库
- SQL
---

# PostgreSQL 📦

> 强大的开源关系数据库

***

## 基本操作

```sql
-- 创建表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 查询
SELECT * FROM users WHERE age >= 18;
SELECT name, COUNT(*) FROM users GROUP BY name;

-- 更新
UPDATE users SET email = 'new@example.com' WHERE id = 1;

-- 删除
DELETE FROM users WHERE id = 1;
```sql

## 高级特性

| 特性 | 说明 |
|------|------|
| JSONB | JSON 数据类型，支持索引 |
| Array | 数组类型 |
| Range | 范围类型 |
| Full-text | 全文搜索 |
| Window | 窗口函数 |

## 索引

```sql
-- 创建索引
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_name_lower ON users(LOWER(name));

-- 部分索引
CREATE INDEX idx_active ON users(created_at) WHERE is_active = true;
```

***

*PostgreSQL 是最强大的开源数据库*
