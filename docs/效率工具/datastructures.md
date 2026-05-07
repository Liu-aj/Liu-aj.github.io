---
title: 数据结构
description: 常用数据结构
tags:
- 数据结构
- Data Structures
---

# 数据结构 📊

> 程序的基础

---

## 数组

```python
# Python
arr = [1, 2, 3]
arr.append(4)  # O(1)
arr.insert(0, 0)  # O(n)
```python

## 链表

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```python

## 树

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## 复杂度

| 操作 | 数组 | 链表 | 树 |
|------|------|------|-----|
| 访问 | O(1) | O(n) | O(log n) |
| 插入 | O(n) | O(1) | O(log n) |
| 删除 | O(n) | O(1) | O(log n) |

---

*数据结构是算法的基石*
