---
title: 逻辑编程
description: 逻辑编程范式
tags:
- 逻辑编程
- Logic Programming
---

# 逻辑编程 🔮

> 声明式编程范式

---

## Prolog

```prolog
parent(tom, bob).
parent(bob, ann).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

?- grandparent(tom, ann).
true.
```

---

*逻辑编程适合 AI 和规则系统*
