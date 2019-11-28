---
layout: post
title: ubuntu系统指南
date: 2016-08-03 16:21:00
forType: Linux
category: ubuntu
tag: [linux, ubuntu]
---

* content
{:toc}

网络设置：
---
初始化无线网卡：
```
sudo dpkg -i dkms_2.3-3ubuntu9.5_all.deb 
sudo dpkg -i gcc_7.4.0-1ubuntu2.3_amd64.deb 
sudo dpkg -i gcc-7_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libgcc-7-dev_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libitm1_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libatomic1_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/libasan4_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/gcc-7_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/libgcc-7-dev_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i liblsan0_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libtsan0_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/libubsan0_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/libcilkrts5_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libmpx2_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libquadmath0_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/libgcc-7-dev_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i gcc_7.4.0-1ubuntu2.3_amd64.deb 
sudo dpkg -i gcc-7_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i gcc_7.4.0-1ubuntu2.3_amd64.deb 
sudo dpkg -i dkms_2.3-3ubuntu9.5_all.deb 
sudo dpkg -i dpkg-dev_1.19.0.5ubuntu2.1_all.deb 
sudo dpkg -i make_4.1-9.1ubuntu1_amd64.deb 
sudo dpkg -i dpkg-dev_1.19.0.5ubuntu2.1_all.deb 
sudo dpkg -i dkms_2.3-3ubuntu9.5_all.deb 
sudo dpkg -i bcmwl-kernel-source_6.30.223.271+bdcom-0ubuntu4_amd64.deb 
sudo dpkg -i linux-libc-dev_4.15.0-55.60_amd64.deb 
sudo dpkg -i bcmwl-kernel-source_6.30.223.271+bdcom-0ubuntu4_amd64.deb 
sudo dpkg -i libc6-dev_2.27-3ubuntu1_amd64.deb 
sudo dpkg -i libc-dev-bin_2.27-3ubuntu1_amd64.deb 
sudo dpkg -i libc6-dev_2.27-3ubuntu1_amd64.deb 
sudo dpkg -i bcmwl-kernel-source_6.30.223.271+bdcom-0ubuntu4_amd64.deb
```

环境搭建：
---
环境软件安装：
---
Git:
---
```
sudo apt install git
git config --global user.name "Liuaj"
git config --global user.email "aijia930515@163.com"
git config --list
```

Vim:
---
```
sudo apt install vim
```

JDK:
---
```
sudo tar -zxvf jdk-8u231-linux-x64.tar.gz 
```

常用软件安装
---
Chrome：
---
```
sudo dpkg -i google-chrome-stable_current_amd64.deb 
sudo dpkg -i google-chrome-stable_current_amd64.deb 
```

WPS：
---
```
sudo dpkg -i wps-office_11.1.0.8865_amd64.deb 
```

sublimetext:
---
```
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
```

QQ:
---
```
sudo dpkg -i linuxqq_2.0.0-b1-1024_amd64.deb 
```

Shadowsocks:
---
```
sudo tar -zxvf shadowsocks-local.tar.gz 
sudo tar -zxvf autoproxy.pac_.tar.gz 
sudo gedit ss.json
./shadowsocks-local -c ss.json 
```

Pycharm:
---
```
sudo tar -zxvf pycharm-community-2019.2.4.tar.gz 
```

ideaIC:
---
```
sudo tar -zxvf ideaIC-2019.2.4.tar.gz 
```

Navicat:
---
```
sudo tar -zxvf navicat121_premium_cs_x64.tar.gz 
```

Robo3t:
---
```
sudo tar -zxvf robo3t-1.3.1-linux-x86_64-7419c406.tar.gz 
```

Thunderbird:
---
```
sudo tar -zxvf thunderbird-68.2.2.tar.gz 
```

phddns:
---
```
phddns start
phddns version
```

系统优化：
---

桌面优化：
---

操作优化：
---
