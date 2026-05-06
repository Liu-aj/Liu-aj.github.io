---
title: 算法
description: 常用算法
---

# 算法 🧮

> 解决问题的步骤

---

## 排序

### 快速排序
```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

## 搜索

### 二分查找
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 时间复杂度

| 复杂度 | 示例 |
|--------|------|
| O(1) | 哈希查找 |
| O(log n) | 二分查找 |
| O(n) | 遍历 |
| O(n log n) | 快速排序 |
| O(n²) | 冒泡排序 |

---

*算法是程序的灵魂*
