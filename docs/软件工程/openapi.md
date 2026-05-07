---
title: OpenAPI/Swagger
description: API 文档规范
tags:
- OpenAPI
- API
- 规范
---

# OpenAPI/Swagger 📝

> API 文档规范

---

## 基本结构

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
```

## 工具

| 工具 | 用途 |
|------|------|
| Swagger UI | 文档界面 |
| Swagger Editor | 在线编辑 |
| Redoc | 文档渲染 |
| Stoplight | API 设计 |

---

*好的文档让 API 更易用*
