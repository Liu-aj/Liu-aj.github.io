---
layout: post
titel: Mysql问题处理
date: 2017-04-14 16:21:00
forType: DB
category: Mysql
tag: [Mysql, 问题处理]
---

* content
{:toc}

锁表查询处理
---
```
-- 查询表占用
SHOW OPEN TABLES WHERE In_use > 0;

-- 查询进程
SHOW PROCESSLIST ;

-- 杀进程
KILL 486574 ;
```