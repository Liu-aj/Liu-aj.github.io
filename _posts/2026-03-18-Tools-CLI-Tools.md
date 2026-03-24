---
layout: post
title: "用好这 5 个 CLI 工具，终端效率翻倍"
date: 2026-03-18 12:00:00
category: Tools
tags: [CLI, bat, eza, fd, ripgrep]
---

作为长期在终端工作的开发者，高效的命令行工具能极大提升日常效率。今天介绍 5 个让我用过就回不去的 CLI 工具，它们都是对传统命令的现代化替代——颜值更高、功能更强、速度更快。

## 目录

1. [bat - 带语法高亮的 cat 替代品](#bat---带语法高亮的-cat-替代品)
2. [eza - 现代化的 ls 替代品](#eza---现代化的-ls-替代品)
3. [fd - 更友好的 find 替代品](#fd---更友好的-find-替代品)
4. [ripgrep - 超快的 grep 替代品](#ripgrep---超快的-grep-替代品)
5. [btop - 颜值超高的系统监控工具](#btop---颜值超高的系统监控工具)

---

## bat - 带语法高亮的 cat 替代品

`bat` 是 `cat` 命令的现代化替代品，不仅支持语法高亮，还集成了 Git 状态显示和行号功能。

### 核心特性

- 支持 150+ 编程语言的语法高亮
- 显示 Git 修改标记
- 自动分页（集成 less）
- 显示不可打印字符（使用 `-A` 参数）

### 安装命令

**macOS (Homebrew)**
```bash
brew install bat
```

**Ubuntu/Debian**
```bash
sudo apt install bat
# 注意：在 Ubuntu 上可执行文件名为 `batcat`，建议创建别名
mkdir -p ~/.local/bin
ln -s /usr/bin/batcat ~/.local/bin/bat
```

**Arch Linux**
```bash
sudo pacman -S bat
```

**Fedora**
```bash
sudo dnf install bat
```

**通用方式 (Cargo)**
```bash
cargo install bat
```

### 常用配置

在 `~/.config/bat/config` 中添加：

```bash
# 设置主题
--theme="Monokai Extended"

# 显示行号和 Git 修改标记
--style="numbers,changes,header"

# 使用深色背景
--italic-text=always

# 设置分页器
--pager="less -RF"
```

### 对比示例

```bash
# 传统 cat - 纯文本输出
$ cat main.py
def hello():
    print("Hello, World!")

# bat - 带语法高亮、行号、Git 状态
$ bat main.py
───────┬────────────────────────────────────────────────────────────────────────
       │ File: main.py
───────┼────────────────────────────────────────────────────────────────────────
   1   │ def hello():
   2   │     print("Hello, World!")
───────┴────────────────────────────────────────────────────────────────────────
```

### 实用技巧

```bash
# 查看所有可用主题
bat --list-themes

# 实时预览主题
bat --theme=Monokai\ Extended --color=always file.py | less -R

# 显示不可打印字符
bat -A /etc/hosts

# 作为 man 的分页器
export MANPAGER="bat -plman"
man 2 select

# 与 fzf 配合使用
fzf --preview "bat --color=always --style=numbers --line-range=:500 {}"
```

---

## eza - 现代化的 ls 替代品

`eza` 是 `exa` 的活跃维护分支，一个现代化的 `ls` 替代品。它默认使用颜色区分文件类型，支持 Git 状态、图标等特性。

### 核心特性

- 彩色输出，自动区分文件类型
- Git 修改标记集成
- 文件图标支持
- 树形显示
- 挂载点详情显示

### 安装命令

**macOS (Homebrew)**
```bash
brew install eza
```

**Ubuntu/Debian**
```bash
sudo mkdir -p /etc/apt/keyrings
wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg
echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | sudo tee /etc/apt/sources.list.d/gierens.list
sudo chmod 644 /etc/apt/keyrings/gierens.gpg /etc/apt/sources.list.d/gierens.list
sudo apt update
sudo apt install -y eza
```

**Arch Linux**
```bash
sudo pacman -S eza
```

**Fedora**
```bash
sudo dnf copr enable varlad/eza
sudo dnf install eza
```

**通用方式 (Cargo)**
```bash
cargo install eza
```

### 常用配置

添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
# 基础别名
alias ls='eza'
alias ll='eza -l'
alias la='eza -la'
alias lt='eza --tree'
alias l='eza -lah'

# 带图标的别名（需要 Nerd Font 字体）
alias ls='eza --icons'
alias ll='eza -l --icons --git'  # 显示 Git 修改标记
alias lt='eza --tree --level=2 --icons'
```

eza 还支持通过 `theme.yml` 配置文件自定义颜色和图标，位于 `~/.config/eza/theme.yml`：

```yaml
# 自定义颜色和图标
filekinds:
  normal: { foreground: "default" }
  directory: { foreground: "Blue", bold: true }
  symlink: { foreground: "Cyan" }
  executable: { foreground: "Green" }
```

### 对比示例

```bash
# 传统 ls
$ ls -la
total 48
drwxr-xr-x  6 user user 4096 Mar 18 10:00 .
drwxr-xr-x 20 user user 4096 Mar 17 15:30 ..
-rw-r--r--  1 user user  256 Mar 18 09:45 README.md
drwxr-xr-x  2 user user 4096 Mar 18 10:00 src

# eza - 带颜色、图标、Git 状态
$ eza -la --icons --git
drwxr-xr-x   - user 18 Mar 10:00  .
drwxr-xr-x  20 user 17 Mar 15:30  ..
.rw-r--r-- 256 user 18 Mar 09:45  README.md
drwxr-xr-x   - user 18 Mar 10:00  src

# 树形显示
$ eza --tree --level=2 --icons
 .
├──   src
│   ├── 󰌞 main.rs
│   └── 󰘦 lib.rs
├──  README.md
└──  Cargo.toml
```

### 实用技巧

```bash
# 只显示目录
eza -D

# 按修改时间排序
eza -l --sort=modified

# 按文件大小排序
eza -l --sort=size

# 显示 Git 状态
eza -l --git

# 显示递归目录大小
eza -l --total-size

# 使用相对时间格式
eza -l --time-style=relative

# 显示挂载点详情
eza -l --mounts
```

---

## fd - 更友好的 find 替代品

`fd` 是一个简洁、快速、用户友好的 `find` 替代品。它默认使用正则表达式搜索，自动忽略隐藏文件和 `.gitignore` 中的文件。

### 核心特性

- 语法直观：`fd PATTERN` 而非 `find -iname '*PATTERN*'`
- 并行搜索，速度极快
- 支持正则表达式和 glob 模式
- 自动忽略隐藏文件和 gitignore 规则
- 彩色输出

### 安装命令

**macOS (Homebrew)**
```bash
brew install fd
```

**Ubuntu/Debian**
```bash
sudo apt install fd-find
# 创建别名
ln -s $(which fdfind) ~/.local/bin/fd
```

**Arch Linux**
```bash
sudo pacman -S fd
```

**Fedora**
```bash
sudo dnf install fd-find
```

**通用方式 (Cargo)**
```bash
cargo install fd-find
```

### 常用配置

添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
# 显示详细信息
alias fdl='fd -l'

# 查找并执行命令
alias fde='fd -x'

# 批量执行
alias fdx='fd -X'
```

### 对比示例

```bash
# 传统 find - 语法复杂
$ find . -name "*.py"
./scripts/setup.py
./src/main.py

# fd - 简洁直观
$ fd -e py
scripts/setup.py
src/main.py

# 使用正则表达式
$ fd '^test.*\.py$'
tests/test_basic.py
tests/test_advanced.py

# 搜索隐藏文件
$ fd -H pre-commit
.git/hooks/pre-commit.sample

# 搜索被 gitignore 忽略的文件
$ fd -I target
target/debug/main
```

### 实用技巧

```bash
# 查找特定扩展名的文件
fd -e md

# 组合条件
fd -e rs -e py mod

# 精确匹配
fd -g libc.so /usr

# 搜索隐藏文件
fd -H pattern

# 搜索被 gitignore 忽略的文件
fd -I pattern

# 无限制搜索（显示所有文件）
fd -u pattern

# 执行命令（每个结果单独执行）
fd -e zip -x unzip

# 批量执行（所有结果作为参数）
fd -e py -X vim

# 显示详细信息
fd -l pattern

# 按完整路径搜索
fd -p '.*/lesson-\d+/[a-z]+\.(jpg|png)'
```

---

## ripgrep - 超快的 grep 替代品

`ripgrep`（简称 `rg` ）是一个超快的搜索工具，递归搜索当前目录中的正则表达式模式，默认尊重 `.gitignore` 规则。

### 核心特性

- 极快的搜索速度（通常比 grep 快 10-100 倍）
- 默认递归搜索
- 自动忽略 `.gitignore`、`.ignore`、`.rgignore` 中的文件
- 自动跳过隐藏文件和二进制文件
- 支持多种文件类型过滤
- 完整 Unicode 支持
- 支持 PCRE2 正则表达式

### 安装命令

**macOS (Homebrew)**
```bash
brew install ripgrep
```

**Ubuntu/Debian**
```bash
sudo apt install ripgrep
```

**Arch Linux**
```bash
sudo pacman -S ripgrep
```

**Fedora**
```bash
sudo dnf install ripgrep
```

**通用方式 (Cargo)**
```bash
cargo install ripgrep
```

### 常用配置

创建 `~/.ripgreprc` 配置文件：

```bash
# 默认启用智能大小写
--smart-case

# 显示行号
--line-number

# 显示列号
--column

# 默认颜色主题
--colors=path:fg:green
--colors=line:fg:yellow
--colors=match:fg:red
```

添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
export RIPGREP_CONFIG_PATH="$HOME/.ripgreprc"
```

### 对比示例

```bash
# 传统 grep - 递归搜索需要 -r 参数
$ grep -r "function" .
./src/main.js:function hello() {
./src/utils.js:function add(a, b) {

# ripgrep - 默认递归，更快更智能
$ rg "function"
src/main.js
3:function hello() {

src/utils.js
1:function add(a, b) {

# 只搜索特定类型文件
$ rg -t js "function"
$ rg -tpy "import"      # 只搜索 Python 文件
$ rg -Tjs "console"     # 排除 JavaScript 文件

# 显示上下文
$ rg -C 3 "function"    # 显示 3 行上下文
$ rg -B 2 "function"    # 显示前 2 行
$ rg -A 2 "function"    # 显示后 2 行
```

### 实用技巧

```bash
# 无限制搜索（显示所有文件）
rg -uuu pattern

# 只搜索特定类型
rg -tpy "import"
rg -tjs -tts "function"
rg -Tjs "console"  # 排除 JS 文件

# 显示匹配统计
rg --stats pattern

# 只显示文件名
rg -l pattern

# 统计匹配次数
rg -c pattern

# 使用 PCRE2 正则（支持前瞻断言等）
rg -P 'foo(?=bar)'

# 替换预览
rg -r 'replacement' pattern

# 搜索固定字符串（不解析为正则）
rg -F "literal.string"

# 显示列号
rg --column pattern

# 使用自动混合正则引擎
rg --auto-hybrid-regex pattern
```

---

## btop - 颜值超高的系统监控工具

`btop` 是一个资源监控工具，具有漂亮的 TUI 界面，支持 CPU、内存、磁盘、网络、进程监控，在 Linux 上还支持 GPU 监控。

### 核心特性

- 美观的 TUI 界面
- 实时监控 CPU、内存、磁盘、网络
- 进程管理（排序、过滤、终止）
- GPU 监控（Linux）
- 多种主题配色
- 跨平台支持（Linux、macOS、FreeBSD）

### 安装命令

**macOS (Homebrew)**
```bash
brew install btop
```

**Ubuntu/Debian**
```bash
sudo apt install btop
```

**Arch Linux**
```bash
sudo pacman -S btop
```

**Fedora**
```bash
sudo dnf install btop
```

**从源码编译（启用 GPU 支持）**
```bash
# 需要安装依赖
sudo apt install build-essential cmake git lowdown

# 克隆并编译
git clone https://github.com/aristocratos/btop.git
cd btop
make GPU_SUPPORT=true
sudo make install
```

### 常用配置

配置文件位于 `~/.config/btop/btop.conf`：

```bash
# 主题
color_theme = "TTY"

# 温度单位（摄氏/华氏）
temp_scale = "celsius"

# 更新间隔（毫秒）
update_ms = 1000

# 显示盒子
shown_boxes = "cpu mem net proc"

# 进程排序
proc_sorting = "cpu lazy"
```

### 对比示例

```bash
# 传统 top - 界面简单
$ top
top - 10:00:00 up 1 day,  2 users,  load average: 0.52, 0.58, 0.59
Tasks: 150 total,   1 running, 149 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.0 us,  2.0 sy,  0.0 ni, 92.0 id,  1.0 wa,  0.0 hi,  0.0 si
MiB Mem :   7823.5 total,    256.3 free,   2048.0 used,   5519.2 buff/cache

# btop - 图形化、信息丰富
$ btop
# 显示：
# - CPU 使用率图形
# - 内存使用图形
# - 网络带宽图形
# - 磁盘 I/O
# - 进程列表（可排序、过滤）
# - GPU 信息（Linux，需编译支持）
```

### 实用技巧

**快捷键**
- `q` - 退出
- `Esc` - 返回/关闭菜单
- `m` - 切换视图模式
- `h` - 显示帮助
- `F1-F10` - 各种设置
- `5, 6, 7` - 显示/隐藏 GPU 监控框（Linux）
- `Tab` - 切换进程列表

**常用操作**
```bash
# 指定主题启动
btop --theme monokai

# 指定配置文件
btop --config /path/to/config

# 仅监控 CPU 和内存
btop --boxes cpu mem
```

---

## 总结

| 工具 | 替代品 | 主要优势 |
|------|--------|----------|
| **bat** | cat | 语法高亮、Git 修改标记、自动分页 |
| **eza** | ls | 彩色输出、Git 修改标记、图标、树形显示 |
| **fd** | find | 简洁语法、并行搜索、智能忽略 |
| **ripgrep** | grep | 超快速度、自动过滤、Unicode 支持 |
| **btop** | top/htop | 美观界面、GPU 监控、多主题 |

### 推荐的 Shell 别名配置

将以下内容添加到你的 `~/.bashrc` 或 `~/.zshrc`：

```bash
# bat
alias cat='bat'
alias catp='bat --plain'  # 原始输出

# eza
alias ls='eza --icons'
alias ll='eza -l --icons --git'
alias la='eza -la --icons'
alias lt='eza --tree --level=2 --icons'
alias l='eza -lah --icons'

# fd（如果可执行文件名为 fdfind）
# alias fd='fdfind'

# ripgrep
alias grep='rg'
alias rgr='rg -r'  # 替换预览模式

# 快速查找并编辑
fe() {
    fd -t f "$1" -X vim
}

# 在特定类型文件中搜索
sg() {
    rg -t "$1" "$2"
}
```

### 字体提示

要完整显示 eza 的图标，需要安装 **Nerd Font** 字体：

```bash
# macOS
brew install --cask font-hack-nerd-font

# Linux
# 从 https://www.nerdfonts.com/ 下载安装

# 或使用脚本安装
curl -fLo "Hack Nerd Font.ttf" https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/Hack/Regular/HackNerdFont-Regular.ttf
```

安装后在终端设置中选择该字体即可。

---

这 5 个工具已经成为我日常终端工作不可或缺的一部分。它们不仅提升了效率，也让终端体验更加愉悦。如果你还没有尝试过，强烈推荐安装体验！