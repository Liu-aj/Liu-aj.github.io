---
title: 终端配置
description: 终端环境配置指南
---

# 终端配置 🖥️

> 配置高效的终端环境

---

## Shell

### Zsh
```bash
# 安装
sudo apt install zsh

# 设置默认
chsh -s /bin/zsh

# 使用 Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```bash

### Fish
```bash
# 安装
sudo apt install fish

# 设置默认
chsh -s /bin/fish
```bash

## 终端复用

### tmux
```bash
# 安装
sudo apt install tmux

# 常用命令
tmux new -s session    # 新建会话
Ctrl+b d               # 分离
tmux attach            # 重新连接
```markdown

### screen
```bash
screen -S session      # 新建会话
Ctrl+a d               # 分离
screen -r session      # 重新连接
```

## 主题

### Powerlevel10k
```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >> ~/.zshrc
```

---

*好的终端环境让效率提升*
