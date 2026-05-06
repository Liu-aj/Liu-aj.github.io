---
title: Linux 管理
description: Linux 系统管理指南
---

# Linux 管理 🖥️

> Linux 系统管理常用命令

---

## 用户管理

```bash
# 创建用户
sudo useradd -m username

# 设置密码
sudo passwd username

# 添加到 sudo 组
sudo usermod -aG sudo username

# 删除用户
sudo userdel -r username
```bash

## 磁盘管理

```bash
# 查看磁盘
df -h
lsblk

# 挂载
sudo mount /dev/sdb1 /mnt/data

# 卸载
sudo umount /mnt/data
```bash

## 服务管理

```bash
# systemd
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx

# 旧系统
sudo service nginx start
```

## 定时任务

```bash
# 编辑 crontab
crontab -e

# 示例
0 2 * * * /backup.sh  # 每天2点执行
*/5 * * * * /check.sh  # 每5分钟执行
```

---

*Linux 管理是运维的基础*
