---
title: MySQL 指南
description: MySQL 数据库
---

# MySQL 💾

> 流行的开源关系数据库

---

## 基本操作

```sql
-- 创建表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 查询
SELECT * FROM users WHERE age >= 18;

-- 更新
UPDATE users SET email = 'new@example.com' WHERE id = 1;
```

## 常用配置

```ini
[mysqld]
max_connections = 200
innodb_buffer_pool_size = 1G
slow_query_log = 1
long_query_time = 2
```

---

*MySQL 是 Web 应用最流行的数据库*
