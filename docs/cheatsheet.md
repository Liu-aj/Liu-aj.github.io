---
title:速查表
description: 常用命令与配置速查
---

# 速查表 📋

> 常用命令与配置快速查阅

---

## Git

```bash
# 初始化
git init

# 克隆
git clone <url>

# 添加文件
git add .

# 提交
git commit -m "message"

# 推送
git push origin master

# 更新
git pull

# 查看状态
git status
```

## Docker

```bash
# 拉取镜像
docker pull <image>

# 运行容器
docker run -d -p 80:80 <image>

# 查看运行中容器
docker ps

# 进入容器
docker exec -it <container> bash

# 查看日志
docker logs -f <container>
```

## Linux

```bash
# 查看进程
ps aux | grep <name>

# 终止进程
kill -9 <pid>

# 查看端口占用
lsof -i :<port>

# 磁盘使用
df -h

# 内存使用
free -h

# 查看 CPU
top
```

## MQTT

```bash
# 订阅主题
mosquitto_sub -t "home/+/sensor"

# 发布消息
mosquitto_pub -t "home/sensor/temp" -m "22.5"
```

## ESP32

```bash
# 编译
idf.py build

# 烧录
idf.py -p /dev/ttyUSB0 flash

# 监视
idf.py monitor
```

---

*持续更新中...*
