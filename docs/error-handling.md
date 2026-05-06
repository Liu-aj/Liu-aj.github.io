---
title: 错误处理
description: 错误处理最佳实践
---

# 错误处理 ⚠️

> 优雅地处理错误

---

## Python

```python
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Value error: {e}")
    raise
except Exception as e:
    logger.critical(f"Unexpected error: {e}")
    raise
finally:
    cleanup()
```

## JavaScript

```javascript
try {
    const result = await riskyOperation();
} catch (error) {
    console.error('Operation failed:', error);
    throw error;
} finally {
    cleanup();
}
```

## HTTP 错误处理

```javascript
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        logger.error(`Fetch failed: ${error.message}`);
        throw error;
    }
}
```

---

*好的错误处理让系统更健壮*
