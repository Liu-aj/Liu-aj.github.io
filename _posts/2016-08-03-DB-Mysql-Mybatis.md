---
layout: post
title: Mybatis使用技巧
date: 2016-08-03 16:21:00
forType: DB
category: Mysql
tag: [Mybatis, 使用技巧]
---

* content
{:toc}

XML文件配置
---
主键自增，插入方法返回主键值解决办法
```xml
<!-- 在insert标签中添加useGeneratedKeys和keyProperty属性 -->
<insert id="insertUser" parameterType="com.example.User" useGeneratedKeys="true" keyProperty="id">
    INSERT INTO user (username, password, email) VALUES (#{username}, #{password}, #{email})
</insert>
```

插入数据后，MyBatis会自动将生成的主键值设置到传入的对象的id属性中。

时间类型字段格式化

在SQL查询中格式化时间字段：
```sql
-- 在SELECT语句中格式化时间字段
SELECT DATE_FORMAT(t.`create_time`,'%Y-%m-%d %H:%i:%s') AS create_time FROM tableName t;
```

在MyBatis的XML中使用条件判断处理时间范围：
```xml
<!-- 在WHERE条件中使用时间范围查询 -->
<if test="dealTime != null and dealTime != ''">
    and t.create_time BETWEEN DATE_FORMAT('${dealTime} 00:00:00','%Y-%c-%d %H:%i:%s') 
    and DATE_FORMAT('${dealTime} 23:59:59','%Y-%c-%d %H:%i:%s')
</if>
```

注意：使用`${}`可能存在SQL注入风险，建议使用`#{}`参数绑定，但需要在Java代码中预先处理时间字符串。

模糊查询

SQL中的模糊查询：
```sql
-- 基础的模糊查询语法
SELECT * FROM tableName t WHERE t.a LIKE '%x%';
```

MyBatis中的模糊查询配置：

**方式一：直接在XML中拼接百分号（不推荐，有SQL注入风险）**
```xml
<!-- 不推荐的写法，有SQL注入风险 -->
SELECT * FROM tableName t WHERE t.a LIKE '%${a}%';
```

**方式二：在Java代码中拼接百分号（推荐）**
```java
// Java代码中处理参数
sqlParam.setA("%" + keyword + "%");
```
```xml
<!-- XML中直接使用参数 -->
SELECT * FROM tableName t WHERE t.a LIKE #{a};
```

**方式三：使用MyBatis的concat函数（推荐）**
```xml
<!-- 使用concat函数拼接百分号 -->
SELECT * FROM tableName t WHERE t.a LIKE CONCAT('%', #{a}, '%');
```

推荐使用方式二或方式三，以避免SQL注入风险。