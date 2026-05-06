---
title: 开发环境搭建
description: 各语言开发环境配置
---

# 开发环境搭建 🛠️

> 常用开发环境配置

---

## Python

```bash
# 安装 pyenv
curl https://pyenv.run | bash

# 安装 Python
pyenv install 3.12.0
pyenv global 3.12.0

# 创建虚拟环境
python -m venv venv
source venv/bin/activate
```bash

## Node.js

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 安装 Node
nvm install 20
nvm use 20

# npm 镜像
npm config set registry https://registry.npmmirror.com
```

## Go

```bash
# 安装
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz

# 配置
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
```bash

## Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

---

*好的开发环境是高效开发的基础*
