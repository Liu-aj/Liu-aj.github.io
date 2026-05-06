---
title: Web 安全
description: Web 安全最佳实践
---

# Web 安全 🔒

> 保护 Web 应用

---

## XSS

### 防御
- HTML 转义
- CSP (Content Security Policy)
- HttpOnly Cookie

### 示例
```html
<!-- 差 -->
<div>{{ user_input }}</div>

<!-- 好 - 转义 -->
<div>{{ user_input | escape }}</div>
```

## CSRF

### 防御
- CSRF Token
- SameSite Cookie
- Origin 检查

## SQL 注入

### 防御
- 参数化查询
- ORM 使用

```python
# 差
query = f"SELECT * FROM users WHERE id = {user_id}"

# 好
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

---

*安全是 Web 开发的重中之重*
