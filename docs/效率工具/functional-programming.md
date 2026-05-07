---
title: 函数式编程
description: 函数式编程范式
tags:
- 函数式编程
- Functional Programming
---

# 函数式编程 λ

> 不可变数据的编程范式

---

## 核心概念

- 纯函数
- 不可变性
- 高阶函数
- 组合函数

## JavaScript

```javascript
// 组合函数
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);

// 示例
const process = compose(
    filter(x => x > 0),
    map(x => x * 2)
);
```python

## Python

```python
from functools import reduce

result = reduce(lambda acc, x: acc + x, map(lambda x: x * 2, filter(lambda x: x > 0, numbers)))
```

---

*函数式编程让代码更简洁*
