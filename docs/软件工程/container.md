---
title: 容器化
description: 容器技术基础
tags:
- 容器化
- Container
- 虚拟化
---

# 容器化 📦

> 轻量级虚拟化

---

## Docker 基础

### 常用命令
```bash
docker build -t myapp .
docker run -d -p 80:80 myapp
docker ps
docker logs -f container_id
docker exec -it container_id sh
```dockerfile

### Dockerfile
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
CMD ["npm", "start"]
```

## 最佳实践

- 最小化镜像大小
- 使用多阶段构建
- 非 root 用户运行
- 定期更新基础镜像

---

*容器让部署更简单*
