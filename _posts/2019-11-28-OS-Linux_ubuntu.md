---
layout: post
title: ubuntu系统指南
date: 2019-11-28 16:21:00
forType: OS
category: Linux
tag: [Linux, ubuntu]
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
<!-- http://www.navicat.com.cn/images/02.Product_00_AllProducts_Premium_large.png -->
```

Robo3t:
---
```
sudo tar -zxvf robo3t-1.3.1-linux-x86_64-7419c406.tar.gz
<!-- https://robomongo.org/static/robomongo-128x128-129df2f1.png -->
```

Thunderbird:
---
```
sudo tar -zxvf thunderbird-68.2.2.tar.gz 
```

phddns(花生壳):
---
```
phddns start
phddns version
```

CoCoMusic：
---
```
https://github.com/xtuJSer/CoCoMusic/releases
```

Nginx:
---
```
sudo apt-get install build-essential
sudo apt-get install libtool
cd /usr/local/src
sudo wget http://sourceforge.net/projects/pcre/files/pcre/8.43/pcre-8.43.tar.gz
sudo tar -zxvf pcre-8.43.tar.gz 
cd pcre-8.43/
./configure 
sudo ./configure 
sudo make 
sudo make install
cd ..
sudo wget http://zlib.net/zlib-1.2.11.tar.gz
sudo tar -zxvf zlib-1.2.11.tar.gz 
cd zlib-1.2.11/
sudo ./configure
sudo make
sudo make install
cd ..
sudo wget https://www.openssl.org/source/openssl-1.0.2t.tar.gz
sudo tar -zxvf openssl-1.0.2t.tar.gz 
sudo wget http://nginx.org/download/nginx-1.17.6.tar.gz
sudo tar -zxvf nginx-1.17.6.tar.gz 
cd nginx-1.17.6/
sudo ./configure --sbin-path=/usr/local/nginx/nginx --conf-path=/usr/local/nginx/nginx.conf --pid-path=/usr/local/nginx/nginx.pid --with-http_ssl_module --with-pcre=../pcre-8.43 --with-zlib=../zlib-1.2.11 --with-openssl=../openssl-1.0.2t
sudo make
sudo make install
cd ../../nginx/
sudo ./nginx 
```
系统优化：
---

桌面优化：
---

应用图标
---

<!-- 以navicat为例 -->
目录/usr/share/applications下新建文件start_navicat.desktop，内容如下
```
[Desktop Entry]
Type=Application
<!-- 启动命令 -->
Exec=/opt/navicat/navicat121_premium_cs_x64/start_navicat
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[zh_CN]=navicat
Name=navicat
Comment[zh_CN]=navicat
Comment=navicat
<!-- 图标 -->
Icon=/opt/navicat/navicat121_premium_cs_x64/icon/navicat.png
```

操作优化：
---
