---
title: API 设计
description: RESTful API 设计指南
tags:
- API设计
- API
- 接口设计
---

# API 设计 🌐

> RESTful API 设计与最佳实践

***

## REST 原则

| 方法 | 用途 | 示例 |
|------|------|------|
| GET | 查询 | GET /users |
| POST | 创建 | POST /users |
| PUT | 完整更新 | PUT /users/1 |
| PATCH | 部分更新 | PATCH /users/1 |
| DELETE | 删除 | DELETE /users/1 |

## URL 设计

### 好
```bash
GET /users/123/posts
GET /users?role=admin
POST /users
```

### 差
```bash
GET /getUsers
POST /createUser
DELETE /deleteUser?id=123
```

## 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 无内容（删除成功）|
| 400 | 请求错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 响应格式

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "User"
  },
  "error": null
}
```

## 版本控制

```bash
GET /api/v1/users
GET /api/v2/users
```

***

*好的 API 设计是好的用户体验的基础*
