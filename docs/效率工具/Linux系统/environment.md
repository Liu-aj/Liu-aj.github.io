---
title: 环境变量
description: 环境变量配置指南
tags:
- 环境变量
- Linux
- 配置
---

# 环境变量 🌳

> 系统环境变量配置

***

## 查看

```bash
# 查看所有
env

# 查看单个
echo $PATH
echo $HOME

# 查看用户
cat ~/.bashrc
cat ~/.profile
```bash

## 临时设置

```bash
# 命令行临时
export VAR=value
VAR=value command
```bash

## 永久设置

```bash
# ~/.bashrc 或 ~/.profile
export PATH=$PATH:/new/path
export EDITOR=vim
export VISUAL=vim
```

## 应用场景

| 变量 | 用途 |
|------|------|
| PATH | 可执行文件路径 |
| HOME | 用户主目录 |
| EDITOR | 默认编辑器 |
| LANG | 语言编码 |
| JAVA_HOME | JDK 安装路径 |

***

*正确配置环境变量让开发更顺畅*
