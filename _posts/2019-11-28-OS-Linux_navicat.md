---
layout: post
title: ubuntu环境navicat应用
date: 2019-11-28 13:42:00
forType: Linux
category: navicat
tag: [navicat, 使用技巧]
---

* content
{:toc}

乱码问题
---
1-编辑start_navicat启动文件，把export LANG="en_US.UTF-8" 替换换成 export LANG="zh_CN.UTF-8"。
```
#export LANG="en_US.UTF-8"
export LANG="zh_CN.UTF-8"。
```
2-
进入navicat之后在菜单栏去选取"工具(T)"或者在乱码的情况选择有T字母的菜单，然后在下拉框里选择最下边的子菜单,也就是"选项";
进入到"选项"页面框时，先针对"常规"项里面的界面字体项，选择 Noto Sans Mono CJK TC Regular;
选项"编辑器'和"记录"两个左侧菜单里两个左侧菜单里，针对文字体框，再一次选择Noto Sans Mono CJK TC Regular;
点击"确定"然后退出