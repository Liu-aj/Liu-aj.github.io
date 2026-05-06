---
title: JavaScript 进阶
description: JavaScript 高级用法
---

# JavaScript 进阶 🌐

> 整理 JavaScript 高级用法

---

## Async/Await

```javascript
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}
```javascript

## 解构赋值

```javascript
// 对象解构
const { name, age } = user;

// 数组解构
const [first, second] = array;

// 默认值
const { name = 'Anonymous' } = user;
```javascript

## 展开运算符

```javascript
// 数组展开
const combined = [...arr1, ...arr2];

// 对象展开
const merged = { ...obj1, ...obj2 };

// 函数参数
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}
```javascript

## Promise

```javascript
const promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("Done"), 1000);
});

promise
    .then(result => console.log(result))
    .catch(error => console.error(error));
```

---

*JavaScript 是 Web 的语言*
