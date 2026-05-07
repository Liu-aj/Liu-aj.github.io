---
title: REST API 设计
description: RESTful API 最佳实践
tags:
- REST API
- RESTful
- API
---

# REST API 设计 🌐

> 构建好的 REST API

***

## 资源命名

```bash
# 好
GET /users/123
POST /users
PUT /users/123
DELETE /users/123

# 差
GET /getUser?id=123
POST /createUser
```

## 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Error |

## 分页

```bash
GET /users?page=1&per_page=20
GET /users?cursor=abc123
```

## 过滤

```bash
GET /users?role=admin&sort=-created_at
```

***

*好的 API 设计是好的用户体验*
