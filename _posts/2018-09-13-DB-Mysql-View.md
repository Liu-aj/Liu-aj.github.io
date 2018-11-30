---
layout: post
title: Mysql视图
date: 2018-09-13 16:27:42
forType: DB
category: Mysql
tag: [Mysql, 数据库视图]
---

* content
{:toc}

Mysql视图新增字段
---
- CREATE OR REPLACE VIEW语句

<pre><code>
使用CREATE OR REPLACE VIEW语句，修改视图 
语法格式 
CREATE [OR REPLACE] [ALGORITHM={UNDEFINED | MERGE | TEMPTABLE}] 
VIEW view_name [(column_list)] 
AS SELECT_statement 
[WITH [CASCADED | LOCAL] CHECK OPTION]]

参数说明 
使用CREATE OR REPLACE VIEW语句修改视图时，如果，修改的视图存在，name将使用修改语句修改视图，如果不存在，那么将会创建一个视图

使用CREATE OR REPLACE VIEW语句修改view_stu视图 
CREATE OR REPLACE VIEW view_stu AS SELECT * FROM student;

参数说明 
View_stu，表示要修改的视图的名称 
*号，通配符，表示表中所有字段 
student，指基本表的表名
</code></pre>
- ALTER语句

<pre><code>
使用ALTER语句，修改视图 
ALTER语句，是MySQL提供的另一种修改视图的方法 
语法格式 
ALTER [ALGORITHM={UNDEFINED | MERGE | TEMPTABLE}] 
VIEW view_name [(column_list)] 
AS SELECT_statement 
[WITH [CASCADED | LOCAL] CHECK OPTION] 
使用ALTER语句，修改view_stu视图 
ALTER VIEW view_stu AS SELECT chinese FROM student;

参数说明 
View_stu，表示要修改的视图名称 
Chinese，表示student表中的chinese字段 
student，为基本表的表名
</code></pre>
