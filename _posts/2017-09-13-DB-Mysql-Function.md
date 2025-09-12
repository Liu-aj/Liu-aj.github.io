---
layout: post
title: MySQL函数创建与管理完全指南
date: 2017-09-13 16:21:00
forType: DB
category: Mysql
tag: [Mysql, 数据库函数, 存储过程, 性能优化]
---

* content
{:toc}

## MySQL函数概述

MySQL函数是一种存储在数据库中的可重用代码块，可以接受输入参数并返回一个计算结果。本文将详细介绍MySQL函数的创建、管理以及相关配置问题的解决方案。

## 解决函数创建的常见问题

### 错误：Function has none of DETERMINISTIC...

在启用了二进制日志的MySQL服务器上创建函数时，经常会遇到以下错误：

```sql
ERROR 1418 (HY000): This function has none of DETERMINISTIC, NO SQL, or READS SQL DATA in its declaration and binary logging is enabled (you *might* want to use the less safe log_bin_trust_function_creators variable)
```

这是因为MySQL在启用二进制日志时，需要确保复制环境中的函数行为一致。

### 解决方案

#### 方法1：修改全局变量

```sql
-- 查看当前设置
SHOW VARIABLES LIKE '%func%';

-- 设置全局变量允许创建函数
SET GLOBAL log_bin_trust_function_creators = 1;

-- 再次查看确认设置成功
SHOW VARIABLES LIKE '%func%';
```

这个设置会在MySQL重启后失效。如果需要永久生效，请在MySQL配置文件(my.cnf或my.ini)中添加以下配置：

```ini
[mysqld]
log_bin_trust_function_creators = 1
```

#### 方法2：在函数定义中指定特性

在创建函数时明确指定函数的特性：

```sql
CREATE FUNCTION my_function()
RETURNS INT
DETERMINISTIC -- 或 NO SQL 或 READS SQL DATA
BEGIN
  -- 函数体
END;
```

## 函数特性详解

在创建MySQL函数时，需要指定以下特性之一：

1. **DETERMINISTIC**：函数对相同的输入总是产生相同的输出

2. **NO SQL**：函数不包含SQL语句

3. **READS SQL DATA**：函数只读取数据，不修改数据

4. **MODIFIES SQL DATA**：函数修改数据（更新、插入、删除等操作）

5. **CONTAINS SQL**：函数包含SQL语句（默认值）

## MySQL函数创建示例

### 1. 基本数学函数示例

```sql
-- 创建计算两个数平均值的函数
DELIMITER $$
CREATE FUNCTION calculate_average(num1 INT, num2 INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
  DECLARE avg_val DECIMAL(10,2);
  SET avg_val = (num1 + num2) / 2;
  RETURN avg_val;
END$$
DELIMITER ;

-- 调用函数
SELECT calculate_average(10, 20); -- 返回 15.00
```

### 2. 字符串处理函数示例

```sql
-- 创建首字母大写的函数
DELIMITER $$
CREATE FUNCTION capitalize_first(str VARCHAR(255))
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
  RETURN CONCAT(UPPER(LEFT(str, 1)), LOWER(SUBSTRING(str, 2)));
END$$
DELIMITER ;

-- 调用函数
SELECT capitalize_first('hello world'); -- 返回 'Hello world'
```

### 3. 日期处理函数示例

```sql
-- 创建计算两个日期之间工作日数量的函数
DELIMITER $$
CREATE FUNCTION workdays_between(start_date DATE, end_date DATE)
RETURNS INT
READS SQL DATA
BEGIN
  DECLARE workdays INT DEFAULT 0;
  DECLARE current_date DATE;
  
  SET current_date = start_date;
  
  WHILE current_date <= end_date DO
    IF WEEKDAY(current_date) NOT IN (5, 6) THEN -- 排除周六和周日
      SET workdays = workdays + 1;
    END IF;
    SET current_date = ADDDATE(current_date, INTERVAL 1 DAY);
  END WHILE;
  
  RETURN workdays;
END$$
DELIMITER ;

-- 调用函数
SELECT workdays_between('2023-01-01', '2023-01-10');
```

## 函数管理与维护

### 查看函数

```sql
-- 查看所有函数
SHOW FUNCTION STATUS WHERE Db = 'your_database_name';

-- 查看函数创建语句
SHOW CREATE FUNCTION your_function_name;
```

### 修改函数

MySQL不支持直接修改函数定义，需要先删除再重新创建：

```sql
-- 删除函数
DROP FUNCTION IF EXISTS your_function_name;

-- 重新创建函数
CREATE FUNCTION your_function_name()
-- ... 函数定义 ...
```

### 查看函数依赖关系

```sql
-- 查看函数依赖的表
SELECT * 
FROM information_schema.ROUTINES 
WHERE ROUTINE_SCHEMA = 'your_database_name' 
  AND ROUTINE_NAME = 'your_function_name';
```

## 性能优化建议

1. **使用确定性函数**：标记为DETERMINISTIC的函数可以被MySQL优化器缓存结果

2. **避免在函数中执行大量数据操作**：函数通常用于小型计算，不适合处理大量数据

3. **使用合适的数据类型**：选择最小且合适的数据类型减少内存使用

4. **避免递归调用**：MySQL对递归深度有限制，且递归可能导致性能问题

5. **定期维护函数**：删除不再使用的函数，更新不高效的实现

## 注意事项

1. 创建函数需要`CREATE ROUTINE`权限

2. 执行函数需要`EXECUTE`权限

3. 修改或删除函数需要`ALTER ROUTINE`权限

4. 在复制环境中使用函数时，确保所有服务器的函数定义一致

5. 复杂的业务逻辑考虑使用存储过程而不是函数，因为存储过程可以返回多个结果集

通过本文的介绍，您应该能够成功创建和管理MySQL函数，并解决在创建过程中遇到的常见问题。合理使用函数可以大大提高数据库操作的效率和代码的可重用性。