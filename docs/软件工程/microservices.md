---
title: 微服务
description: 微服务架构
tags:
- 微服务
- Microservices
- 架构
---

# 微服务 🏛️

> 分布式系统架构

---

## 原则

- 单一职责
- 独立部署
- 轻量通信
- 去中心化管理

## 通信

### HTTP/REST
```bash
GET /api/users/123
POST /api/users
```markdown

### gRPC
```protobuf
service UserService {
    rpc GetUser (UserRequest) returns (User);
}
```

### 消息队列
- Kafka
- RabbitMQ
- NATS

## 服务发现

- Consul
- etcd
- Eureka

---

*微服务让系统更灵活*
