---
layout: post
title: Ubuntu环境下Navicat安装与乱码问题解决
date: 2019-11-28 13:42:00
forType: Linux
category: Linux
tag: [Ubuntu, Navicat, 数据库工具]
---

* content
{:toc}

# Ubuntu环境下Navicat安装与乱码问题解决

本文介绍在Ubuntu系统中安装Navicat数据库管理工具以及解决常见的中文乱码问题。

## Navicat简介

Navicat是一款功能强大的数据库管理工具，支持MySQL、PostgreSQL、Oracle、SQLite等多种数据库系统。在Ubuntu系统中使用Navicat可以方便地管理各类数据库，但有时会遇到中文显示乱码的问题。

## 乱码问题解决方法

在Ubuntu系统中运行Navicat时，中文显示乱码是一个常见问题。以下是解决此问题的详细步骤：

### 步骤一：修改启动文件的语言设置

1. 找到Navicat的启动文件`start_navicat`
2. 使用文本编辑器打开该文件
3. 将语言设置从英文改为中文UTF-8：

```bash
# 修改前
#export LANG="en_US.UTF-8"

# 修改后
export LANG="zh_CN.UTF-8"
```

### 步骤二：配置Navicat的字体设置

1. 启动Navicat应用程序
2. 在菜单栏中选择"工具(T)"菜单（如果界面已乱码，可以寻找带有"T"字母的菜单）
3. 在下拉菜单中选择最下方的"选项"子菜单
4. 在弹出的"选项"对话框中：
   - 选择左侧的"常规"选项
   - 在"界面字体"下拉框中选择"Noto Sans Mono CJK TC Regular"字体
   - 选择左侧的"编辑器"选项
   - 在"文字体"下拉框中再次选择"Noto Sans Mono CJK TC Regular"字体
   - 选择左侧的"记录"选项
   - 在"文字体"下拉框中也选择"Noto Sans Mono CJK TC Regular"字体
5. 点击"确定"按钮保存设置
6. 退出Navicat并重新启动，中文应该可以正常显示了

## 其他可能的字体选择

除了"Noto Sans Mono CJK TC Regular"外，您还可以尝试以下中文字体：

- WenQuanYi Micro Hei
- Droid Sans Fallback
- SimHei (如果已安装)

## 安装额外的中文字体

如果您的系统中没有合适的中文字体，可以通过以下命令安装：

```bash
# 安装文泉驿微米黑字体
sudo apt-get update
sudo apt-get install ttf-wqy-microhei

# 安装Noto Sans CJK字体
sudo apt-get install fonts-noto-cjk
```

## 总结

在Ubuntu系统中解决Navicat中文乱码问题主要通过两个步骤：
1. 修改启动文件的语言环境设置为中文UTF-8
2. 在Navicat的选项中配置适合的中文字体

通过以上设置，您应该可以在Ubuntu系统中正常使用Navicat并正确显示中文内容了。