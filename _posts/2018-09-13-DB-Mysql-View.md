---
---
layout: post
title: MySQL视图详解
date: 2018-09-13 16:27:42
forType: DB
category: Mysql
tag: [Mysql, 数据库视图]
---

* content
{:toc}

# MySQL视图管理

## 1. 视图概述

视图是一个虚拟表，其内容由查询定义。同真实的表一样，视图包含列，其数据来自对应的真实表（基表）。

## 2. 修改视图字段

### 2.1 使用CREATE OR REPLACE VIEW语句

```sql
-- 修改或创建视图的语法
CREATE [OR REPLACE] [ALGORITHM={UNDEFINED | MERGE | TEMPTABLE}] 
VIEW view_name [(column_list)] 
AS SELECT_statement 
[WITH [CASCADED | LOCAL] CHECK OPTION];
```

**参数说明：**
- 使用CREATE OR REPLACE VIEW语句时，如果视图存在，则修改视图；如果不存在，则创建新视图

**示例：**

```sql
-- 修改view_stu视图，包含所有字段
CREATE OR REPLACE VIEW view_stu AS SELECT * FROM student;

-- 修改view_stu视图，只包含特定字段
CREATE OR REPLACE VIEW view_stu AS 
SELECT id, name, chinese, math, english 
FROM student;
```

### 2.2 使用ALTER语句

```sql
-- 修改视图的语法
ALTER [ALGORITHM={UNDEFINED | MERGE | TEMPTABLE}] 
VIEW view_name [(column_list)] 
AS SELECT_statement 
[WITH [CASCADED | LOCAL] CHECK OPTION];
```

**示例：**

```sql
-- 使用ALTER语句修改view_stu视图
ALTER VIEW view_stu AS SELECT chinese FROM student;

-- 修改视图并添加列别名
ALTER VIEW view_stu AS 
SELECT id AS student_id, name AS student_name, chinese 
FROM student;
```

## 3. 视图的优点

1. **简化复杂查询**：将复杂的查询逻辑封装在视图中
2. **安全性**：可以限制用户只能访问视图中指定的列
3. **数据独立性**：视图可以屏蔽表结构的变化

## 4. 创建视图的基本语法

```sql
-- 创建视图的基本语法
CREATE VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
WHERE condition;
```

**示例：**

```sql
-- 创建包含计算列的视图
CREATE VIEW student_scores AS
SELECT id, name,
       chinese + math + english AS total_score,
       (chinese + math + english) / 3 AS average_score
FROM student;
```
