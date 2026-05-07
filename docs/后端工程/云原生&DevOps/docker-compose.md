---
title: Docker Compose
description: Docker Compose 多容器编排
tags:
- Docker Compose
- 容器编排
- Docker
---

# Docker Compose 📦

> 定义多容器应用

***

## 基本配置

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret
  
  redis:
    image: redis:7-alpine

volumes:
  db_data:
```

## 常用命令

```bash
docker-compose up -d        # 启动
docker-compose down         # 停止
docker-compose logs -f      # 查看日志
docker-compose exec web sh  # 进入容器
```

***

*Docker Compose 简化多容器管理*
