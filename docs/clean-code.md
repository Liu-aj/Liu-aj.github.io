---
title: 代码整洁之道
description: 编写整洁代码的原则
---

# 代码整洁之道 🧹

> 编写可维护代码

---

## 命名

### 好
```python
user_age = 25
is_logged_in = True
```markdown

### 差
```python
a = 25  # 什么 a？
flag = True  # 什么 flag？
```

## 函数

### 原则
- 函数要小
- 一个函数只做一件事
- 使用描述性的名称

### 示例
```python
# 差
def process(data):
    # 处理100行代码

# 好
def validate_input(data):
    pass

def save_to_database(data):
    pass
```markdown

## 注释

### 原则
- 代码即注释
- 注释解释为什么，不是做什么
- 删除无用的注释

---

*整洁的代码让人愉悦*
