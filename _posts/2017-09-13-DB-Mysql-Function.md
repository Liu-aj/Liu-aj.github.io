---
layout: post
title: Mysql函数
date: 2017-09-13 16:21:00
forType: DB
category: Mysql
tag: [Mysql, 数据库函数]
---

* content
{:toc}

函数
---
<pre><code>
SHOW VARIABLES LIKE '%func%';
SET GLOBAL log_bin_trust_function_creators =1;
SHOW VARIABLES LIKE '%func%';
</code></pre>

问题描述：
```
This function has none of DETERMINISTIC, NO SQL, or READS SQL DATA in its de....
```
解决方案：
```
set global log_bin_trust_function_creators=TRUE;
```

<!-- <meta http-equiv="refresh" content="1"> -->