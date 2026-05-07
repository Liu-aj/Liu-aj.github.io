---
title: Python 进阶
description: Python 高级用法
tags:
- Python
- 进阶
- 后端开发
---

# Python 进阶 🐍

> 整理 Python 高级用法

***

## 装饰器

```python
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
```python

## 上下文管理器

```python
class Database:
    def __enter__(self):
        self.conn = connect()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

with Database() as conn:
    conn.execute("SELECT * FROM users")
```python

## 异步编程

```python
import asyncio

async def fetch_data(url):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
    )
```python

## 类型注解

```python
from typing import List, Dict, Optional

def process_users(users: List[Dict[str, str]]) -> Optional[str]:
    if not users:
        return None
    return users[0].get("name")
```

***

*Python 之禅：简单优于复杂*
