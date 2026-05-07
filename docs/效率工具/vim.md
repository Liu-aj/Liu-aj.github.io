---
title: Vim 使用指南
description: Vim 编辑器完全指南
tags:
- Vim
- 编辑器
- 文本编辑
---

# Vim 使用指南 ✏️

> Vi IMproved - 强大的文本编辑器

---

## 模式

| 模式 | 用途 | 进入方式 |
|------|------|----------|
| Normal | 命令执行 | Esc |
| Insert | 文本编辑 | i/a/o |
| Visual | 文本选择 | v/V |
| Command | 命令行 | : |

## 常用命令

### 移动
| 命令 | 移动 |
|------|------|
| h/j/k/l | 左/下/上/右 |
| w/b | 下一个/上一个单词 |
| 0/$ | 行首/行尾 |
| gg/G | 文件首/尾 |

### 编辑
| 命令 | 操作 |
|------|------|
| x | 删除字符 |
| dd | 删除行 |
| yy | 复制行 |
| p | 粘贴 |
| u | 撤销 |
| Ctrl+r | 重做 |

### 搜索
| 命令 | 操作 |
|------|------|
| /pattern | 搜索 |
| n/N | 下一个/上一个 |
| :%s/old/new/g | 全局替换 |

## 配置

```bash
# ~/.vimrc
set number
set relativenumber
set showcmd
set wildmenu
set mouse=a
syntax on
```

---

*掌握 Vim 需要时间，但值得*
