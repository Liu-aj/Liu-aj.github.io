---
layout: post
title: "Jekyll博客搭建完全指南"
date: 2026-03-19 12:00:00
category: Tools
tags: [Jekyll, GitHub-Pages, Blog]
---

> Jekyll 是一个简洁、强大的静态博客生成器，让你能专注于写作本身。本文将带你从零开始搭建属于自己的 Jekyll 博客 🚀

## 一、Jekyll 是什么？为什么用它？

### 1.1 Jekyll 简介

Jekyll 是一个用 Ruby 编写的静态站点生成器（Static Site Generator）。它能够将 Markdown（或其他标记语言）文件转换为精美的静态网页。

### 1.2 为什么要用 Jekyll？

| 优势 | 说明 |
|------|------|
| 🚀 **免费托管** | 直接部署到 GitHub Pages，无需服务器费用 |
| 📝 **专注写作** | 用 Markdown 写文章，摆脱复杂的富文本编辑器 |
| ⚡ **速度快** | 纯静态 HTML，加载速度极快 |
| 🔒 **安全可靠** | 没有数据库，没有动态脚本，天然防黑客 |
| 🎨 **主题丰富** | 数百款免费主题可选 |
| 🔧 **完全可控** | 所有代码开源，可自定义每一处细节 |

> GitHub 官方推荐的博客方案就是 Jekyll + GitHub Pages，超过 100 万个网站在使用！

---

## 二、环境准备（Ruby, Gem）

Jekyll 是基于 Ruby 的静态博客框架，搭建前需要先安装 Ruby 环境。

### 2.1 安装 Ruby

**macOS 用户：**
```bash
# 推荐使用 Homebrew 安装
brew install ruby

# 添加到 PATH（zsh 用户）
echo 'export PATH="/usr/local/opt/ruby/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Linux 用户（Ubuntu/Debian）：**
```bash
sudo apt update
sudo apt install ruby ruby-dev build-essential
```

**Windows 用户：**
推荐下载 [RubyInstaller](https://rubyinstaller.org/) 安装包，一键安装。

### 2.2 安装 Jekyll 和 Bundler

Ruby 安装完成后，执行以下命令安装 Jekyll：

```bash
# 安装 Jekyll
gem install jekyll

# 安装 Bundler（用于管理项目依赖）
gem install bundler
```

> ⚠️ **注意**：如果你使用的是 macOS 系统自带的 Ruby，可能会遇到权限问题。建议使用 `rbenv` 或 `rvm` 管理多版本 Ruby。

### 2.3 验证安装

```bash
jekyll --version
# 输出类似：jekyll 4.3.3

bundler --version
# 输出类似：Bundler 2.5.6
```

---

## 三、本地搭建步骤

### 3.1 创建新博客

```bash
# 方式一：使用 Jekyll 命令创建（推荐）
jekyll new my-blog

# 方式二：手动创建（如果你想完全自定义）
mkdir my-blog && cd my-blog
```

### 3.2 安装依赖

```bash
cd my-blog
bundle install
```

这个命令会根据 `Gemfile` 自动安装所有需要的依赖包。

### 3.3 启动本地服务器

```bash
bundle exec jekyll serve
# 或者简写
jekyll s
```

现在打开浏览器访问 **http://127.0.0.1:4000**，你已经拥有了一个本地运行的博客！

> 💡 **技巧**：添加 `--livereload` 参数可以实现实时预览
> ```bash
> jekyll serve --livereload
> ```

---

## 四、_config.yml 配置详解

`_config.yml` 是 Jekyll 博客的核心配置文件。以下是常用配置项详解：

```yaml
# ============================================
# 博客基本信息
# ============================================
title: 我的技术博客           # 网站标题
subtitle: 记录学习与成长      # 网站副标题
name: 你的名字               # 作者名字
email: your@email.com        # 联系邮箱

# ============================================
# URL 配置
# ============================================
url: "https://yourname.github.io"  # 你的网站域名
baseurl: "/repo-name"               # 如果部署在子目录填写
permalink: /:year/:month/:title/   # 文章链接格式

# ============================================
# 构建配置
# ==========================================
timezone: Asia/Shanghai              # 时区
markdown: kramdown                  # Markdown 解析器
highlighter: rouge                  # 代码高亮插件

# ============================================
# Jekyll 参数
# ============================================
show_drafts: false      # 是否显示草稿
paginate: 10            # 每页显示文章数量
paginate_path: "/page:num/"  # 分页路径
```

### 常用配置项速查表

| 配置项 | 说明 | 常用值 |
|--------|------|--------|
| `title` | 网站标题 | - |
| `description` | 网站描述 | - |
| `url` | 网站域名 | `https://username.github.io` |
| `permalink` | 文章链接格式 | `/:title/`、`/:year/:month/:day/:title/` |
| `markdown` | Markdown 引擎 | `kramdown`、`GFM`、`redcarpet` |
| `timezone` | 时区 | `Asia/Shanghai` |
| `paginate` | 分页数量 | 5、10、20 |

---

## 五、目录结构说明

一个标准的 Jekyll 博客目录结构如下：

```
my-blog/
├── _config.yml          # 配置文件
├── _includes/           # 可复用的组件（头部、底部、侧边栏等）
├── _layouts/            # 页面布局模板
├── _posts/              # 博客文章目录
│   └── 2026-03-19-hello-world.md
├── _drafts/             # 草稿目录（不发布）
├── _pages/              # 单独页面（如关于页面）
├── _data/               # 数据文件（YAML/JSON）
├── _sass/               # SCSS 样式文件
├── assets/              # 静态资源（CSS、JS、图片）
├── _site/               # 生成的静态网站（不要手动修改）
├── Gemfile              # 依赖声明
└── index.html           # 首页
```

### 关键目录说明

| 目录/文件 | 作用 |
|-----------|------|
| `_posts/` | 存放博客文章，文件名格式：`年-月-日-标题.md` |
| `_layouts/` | 定义页面布局，文章、首页、页面各有不同模板 |
| `_includes/` | 可包含的组件，如导航栏、页脚 |
| `_data/` | 存放数据文件，如导航链接、团队成员 |
| `assets/` | CSS、JS、图片等静态资源 |
| `_site/` | Jekyll 生成的最终网站（上传到 GitHub 的内容） |

---

## 六、写文章（Markdown 格式）

### 6.1 创建新文章

在 `_posts` 目录下创建 Markdown 文件，命名格式：
```
年-月-日-标题.md
```

例如：`2026-03-19-jekyll-tutorial.md`

### 6.2 Front Matter

每篇文章头部需要添加 YAML 格式的 Front Matter：

```yaml
---
layout: post
title: "Jekyll博客搭建完全指南"
date: 2026-03-19 10:00:00
---

文章内容从这里开始...
```

### 6.3 常用 Markdown 语法

```markdown
# 一级标题
## 二级标题
### 三级标题

**粗体文本** 和 *斜体文本*

- 列表项 1
- 列表项 2
  - 子列表

1. 有序列表 1
2. 有序列表 2

[链接文字](https://example.com)

![图片描述](/assets/images/image.jpg)

> 引用块

代码块：
```python
def hello():
    print("Hello, Jekyll!")
```
```

### 6.4 文章内使用 Liquid 模板

Jekyll 支持 Liquid 模板语法：

{% raw %}
```liquid
{% for post in site.posts %}
  - [{{ post.title }}]({{ post.url }})
{% endfor %}

{{ page.date | date: "%Y年%m月%d日" }}
```
{% endraw %}

---

## 七、部署到 GitHub Pages

### 7.1 创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** → **New repository**
3. 仓库名称设置为：`yourusername.github.io`
4. 选择 **Public**
5. 点击 **Create repository**

### 7.2 推送本地博客到 GitHub

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial Jekyll blog"

# 添加远程仓库
git remote add origin https://github.com/yourusername/yourusername.github.io.git

# 推送代码
git push -u origin main
```

### 7.3 访问你的博客

部署完成后，访问：**https://yourusername.github.io**

> ⏱️ GitHub Pages 需要 1-2 分钟来构建和发布你的网站。

### 7.4 使用自定义域名（可选）

1. 在仓库设置中找到 **Pages** 部分
2. 在 **Custom domain** 中输入你的域名
3. 前往域名服务商添加 DNS 记录：
   - CNAME 记录：`www` → `yourusername.github.io`
   - A 记录：`@` → `185.199.108.153`（GitHub IP）

---

## 八、常见问题与技巧

### 8.1 常见问题

**Q1: 执行 `jekyll serve` 报错怎么办？**

```bash
# 常见解决方案
bundle install          # 重新安装依赖
bundle exec jekyll serve  # 使用 bundle 执行

# 如果还有问题，尝试更新 gem
gem update --system
gem update jekyll
```

**Q2: 本地正常但部署到 GitHub 后样式丢失？**

检查 `_config.yml` 中的 `baseurl` 配置：
- 如果部署在 `username.github.io/repo-name`，需要设置 `baseurl: "/repo-name"`
- 如果部署在根域名，不需要设置 `baseurl`

**Q3: 如何加速本地预览？**

```bash
# 增量构建，只处理修改的文件
jekyll serve --incremental
```

**Q4: 代码高亮不工作？**

确保 `_config.yml` 中配置了高亮器：
```yaml
highlighter: rouge
```

然后在文章中使用：
<pre>
```python
# 你的代码
```
</pre>

### 8.2 实用技巧

**1. 启用文章分类和标签**

```yaml

**3. 添加 Google Analytics**

在 `_includes/head.html` 中添加：
```html
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-XXXXX-Y', 'auto');
  ga('send', 'pageview');
</script>
```

**4. 使用主题**

```bash
# 安装主题（在 Gemfile 中添加）
gem "jekyll-theme-chirpy"

# 在 _config.yml 中启用
theme: jekyll-theme-chirpy
```

**5. 草稿功能**

在 `_drafts` 目录下创建不带日期的文件：
```
_drafts/my-draft-post.md
```

预览草稿：
```bash
jekyll serve --drafts
```

---

## 总结

Jekyll 是一个强大而简洁的静态博客框架，特别适合技术博主。通过本文，你应该已经掌握了：

- ✅ Jekyll 的基本概念和优势
- ✅ Ruby 环境的安装配置
- ✅ 本地博客的创建和预览
- ✅ `_config.yml` 配置详解
- ✅ 目录结构和文件组织
- ✅ Markdown 写作和 Front Matter
- ✅ 部署到 GitHub Pages
- ✅ 常见问题解决和实用技巧

现在，是时候开始你的博客之旅了！🎉

> 如果你在搭建过程中遇到任何问题，欢迎在评论区留言讨论。

---

*本文参考：[Jekyll 官方文档](https://jekyllrb.com/docs/)、[GitHub Pages 文档](https://docs.github.com/en/pages)*