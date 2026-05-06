---
title: Docker 进阶
description: Docker 高级用法
---

# Docker 进阶 🐳

> 整理 Docker 高级用法

---

## 多阶段构建

```dockerfile
# 构建阶段
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o main

# 运行阶段
FROM alpine:latest
COPY --from=builder /app/main /main
CMD ["/main"]
```

## Docker Compose

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "80:80"
    depends_on:
      - db
      - redis
  db:
    image: postgres:15
  redis:
    image: redis:7
```

## 网络配置

```bash
# 创建网络
docker network create mynet

# 连接容器
docker network connect mynet container1

# 查看网络
docker network inspect mynet
```

## 存储

```bash
# 创建 volume
docker volume create mydata

# 挂载 volume
docker run -v mydata:/data nginx
```

---

*Docker 是容器化的标准*
