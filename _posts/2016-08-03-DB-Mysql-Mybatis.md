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
```
<useGeneratedKeys="true" keyProperty="id">
```

时间类型字段格式化
```
DATE_FORMAT(t.`create_time`,'%Y-%m-%d %h:%i:%s') AS create_time,

<if test="dealTime != null and dealTime != ''">
	and t.create_time BETWEEN DATE_FORMAT('${dealTime} 00:00:00','%Y-%c-%d %H:%i:%s') 
	and DATE_FORMAT('${dealTime} 23:59:59','%Y-%c-%d %H:%i:%s')
</if>
```

模糊查询
```
select * from tableName t where t.a like '%x%';

mybatis -- mapper文件配置
like '%${a}%';
```