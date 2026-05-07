---
title: GraphQL
description: GraphQL 查询语言
tags:
- GraphQL
- API
- 查询语言
---

# GraphQL 🔍

> API 查询语言

***

## 特点

| 特点 | 说明 |
|------|------|
| 单端点 | /graphql |
| 按需获取 | 只请求需要的数据 |
| 类型安全 | Schema 定义 |

## 示例

```graphql
query {
  user(id: "123") {
    name
    email
    posts {
      title
    }
  }
}
```

## Schema

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}
```

***

*GraphQL 让前端更自由*
