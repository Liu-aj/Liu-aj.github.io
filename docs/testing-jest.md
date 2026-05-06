---
title: Jest 测试
description: Jest 单元测试框架
---

# Jest 测试 🧪

> JavaScript 测试框架

---

## 基本用法

```javascript
// sum.test.js
function sum(a, b) {
    return a + b;
}

test('adds 1 + 2 to equal 3', () => {
    expect(sum(1, 2)).toBe(3);
});
```javascript

## 常用匹配器

| 匹配器 | 用途 |
|--------|------|
| toBe | 精确相等 |
| toEqual | 对象相等 |
| toBeNull | 为 null |
| toBeTruthy | 为真 |
| toContain | 包含 |
| toThrow | 抛出异常 |

## 异步测试

```javascript
test('fetch data', async () => {
    const data = await fetchData();
    expect(data).toHaveProperty('id');
});
```javascript

## Mock

```javascript
test('mock example', () => {
    const mockFn = jest.fn();
    mockFn.mockReturnValue(42);
    expect(mockFn()).toBe(42);
});
```

---

*测试是代码质量的保障*
