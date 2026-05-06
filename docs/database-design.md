---
title: 数据库设计
description: 数据库设计指南
---

# 数据库设计 💾

> 数据库规范化与性能优化

---

## 规范化

### 第一范式 (1NF)
- 原子性：每个字段不可再分
- 无重复列

### 第二范式 (2NF)
- 满足1NF
- 非主键字段完全依赖主键

### 第三范式 (3NF)
- 满足2NF
- 非主键字段不传递依赖主键

## 索引设计

### 何时创建索引
- WHERE 常用字段
- JOIN 关联字段
- ORDER BY 排序字段

### 索引类型
| 类型 | 用途 |
|------|------|
| B-Tree | 范围查询 |
| Hash | 精确匹配 |
| 复合索引 | 多字段查询 |

## 常用 SQL

### 创建表
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 查询优化
```sql
-- 使用 EXPLAIN 分析查询
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 创建索引
CREATE INDEX idx_email ON users(email);
```

---

*好的数据库设计是系统性能的基础*
