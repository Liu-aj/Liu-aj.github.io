---
title: 异步编程
description: 异步编程模式
tags:
- 异步编程
- Async
- 并发
---

# 异步编程 ⚡

> 高效处理并发

***

## Python

```python
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    results = await asyncio.gather(
        fetch_data(url1),
        fetch_data(url2),
        fetch_data(url3),
    )
```javascript

## JavaScript

```javascript
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}

// 并发
const results = await Promise.all([
    fetchData(url1),
    fetchData(url2),
]);
```

## 事件循环

```python
# 事件循环
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

***

*异步让程序更高效*
