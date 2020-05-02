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
---
```
cd /media/liuaj/Ubuntu\ 20.0/pool/main/
cd g/gcc-9/
sudo dpkg -i libasan5_9.3.0-10ubuntu2_amd64.deb 
cd ../gcc-10/
sudo dpkg -i libitm1_10-20200411-0ubuntu1_amd64.deb 
sudo dpkg -i libatomic1_10-20200411-0ubuntu1_amd64.deb
sudo dpkg -i liblsan0_10-20200411-0ubuntu1_amd64.deb 
sudo dpkg -i libubsan1_10-20200411-0ubuntu1_amd64.deb 
sudo dpkg -i libquadmath0_10-20200411-0ubuntu1_amd64.deb 
sudo dpkg -i libtsan0_10-20200411-0ubuntu1_amd64.deb 
cd ../gcc-9/
sudo dpkg -i libgcc-9-dev_9.3.0-10ubuntu2_amd64.deb 
cd ../../m/make-dfsg/
sudo dpkg -i make_4.2.1-1.2_amd64.deb 
cd ../../b/binutils/
sudo dpkg -i binutils-common_2.34-6ubuntu1_amd64.deb 
cd ../../g//gcc-10/
sudo dpkg -i gcc-10-base_10-20200411-0ubuntu1_i386.deb 
cd ../../b/binutils/
sudo dpkg -i libctf-nobfd0_2.34-6ubuntu1_amd64.deb 
sudo dpkg -i libbinutils_2.34-6ubuntu1_amd64.deb 
sudo dpkg -i libctf0_2.34-6ubuntu1_amd64.deb 
sudo dpkg -i binutils-x86-64-linux-gnu_2.34-6ubuntu1_amd64.deb 
sudo dpkg -i binutils_2.34-6ubuntu1_amd64.deb 
cd ../../d/dpkg/
sudo dpkg -i dpkg-dev_1.19.7ubuntu3_all.deb 
cd ../../g/glibc/
sudo dpkg -i libc-dev-bin_2.31-0ubuntu9_amd64.deb 
cd ../../l/linux/
sudo dpkg -i linux-libc-dev_5.4.0-26.30_amd64.deb 
cd ../../libx/libxcrypt/
sudo dpkg -i libcrypt-dev_4.4.10-10ubuntu4_amd64.deb 
cd ../../g/glibc/
sudo dpkg -i libc6-dev_2.31-0ubuntu9_amd64.deb 
cd ../gcc-9/
sudo dpkg -i libstdc++-9-dev_9.3.0-10ubuntu2_amd64.deb 
sudo dpkg -i gcc-9_9.3.0-10ubuntu2_amd64.deb 
sudo dpkg -i g++-9_9.3.0-10ubuntu2_amd64.deb 
cd ../gcc-defaults/
sudo dpkg -i gcc_9.3.0-1ubuntu2_amd64.deb
cd ../../d/dkms/
sudo dpkg -i dkms_2.8.1-5ubuntu1_all.deb 
cd ../../../restricted/b/bcmwl/
sudo dpkg -i bcmwl-kernel-source_6.30.223.271+bdcom-0ubuntu5_amd64.deb 
```

替换国内源
---
```
lsb_release -a
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bcakup
sudo gedit /etc/apt/sources.list

# 网易163源
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb http://mirrors.163.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ focal-backports main restricted universe multiverse
# deb-src http://mirrors.163.com/ubuntu/ focal main restricted universe multiverse
# deb-src http://mirrors.163.com/ubuntu/ focal-security main restricted universe multiverse
# deb-src http://mirrors.163.com/ubuntu/ focal-updates main restricted universe multiverse
# deb-src http://mirrors.163.com/ubuntu/ focal-backports main restricted universe multiverse
# 预发布软件源，不建议启用
# deb http://mirrors.163.com/ubuntu/ focal-proposed main restricted universe multiverse
# deb-src http://mirrors.163.com/ubuntu/ focal-proposed main restricted universe multiverse

```

开启22端口
---
```
//安装后需要重启
sudo apt-get install openssh-server openssh-client 
service ssh start
ssh localhost
lsof -i:22
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

sudo apt-get install git-cola
```

Vim:
---
```
sudo apt install vim
```

JDK:
---
```
1、前往oracle Java官网下载JDK（http://www.oracle.com/technetwork/java/javase/downloads/index.html）
2、解压缩到指定目录（以jdk-8u191-linux-x64.tar.gz为例）
创建目录:
	sudo mkdir /usr/lib/jvm
解压缩到该目录:
	sudo tar -zxvf jdk-8u241-linux-x64.tar.gz -C /usr/lib/jvm/
3.修改环境变量:　　
	sudo vi ~/.bashrc
在文件末尾追加下面内容：
#set oracle jdk environment
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_241
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

使环境变量马上生效：
	source ~/.bashrc
4、系统注册此jdk
	sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk1.8.0_241/bin/java 300
5、查看java版本，看看是否安装成功：
	java -version
```

常用软件安装
---

Chrome：
---
```
<!-- https://www.google.cn/chrome/ -->
<!-- http://www.ubuntuchrome.com/ -->
sudo dpkg -i google-chrome-stable_current_amd64.deb 
```

WPS：
---
```
<!-- https://www.wps.cn/product/wpslinux -->
sudo dpkg -i wps-office_11.1.0.8865_amd64.deb 
```

sublimetext:
---
```
sudo cp sublime_text_3_build_3211_x64.tar.bz2 /opt/
cd /opt/
sudo tar -jxvf sublime_text_3_build_3211_x64.tar.bz2 
sudo mv sublime_text_3 sublime_text
sudo vim sublime_text/sublime_text.desktop
<!-- /opt/sublime_text/Icon/256x256/sublime-text.png -->
sudo cp sublime_text/sublime_text.desktop /usr/share/applications/
```

QQ:
---
```
sudo dpkg -i linuxqq_2.0.0-b1-1024_amd64.deb 
```

Shadowsocks:
---
```
mkdir -p /opt/Proxy
cd /opt/Proxy
sudo git clone --branch akkariiin/master https://github.com/shadowsocksrr/shadowsocksr.git
cd /opt/Proxy/shadowsocksr/
sudo bash initcfg.sh
sudo mv user-config.json user-config.json.bak
sudo vim user-config.json
<!-- 
{
    "server":"45.32.170.153",		
    "server_port":12020,
    "password":"aijia",
    "method":"aes-256-cfb",
    "local_address":"127.0.0.1",
    "local_port":1080,
    "timeout":300
}
 -->
sudo vim /lib/systemd/system/shadowsocksr.service
<!-- 
[Unit]
Description=Shadowsocks Server
After=network.target

[Service]
ExecStart=python3 /opt/Proxy/shadowsocksr/shadowsocks/local.py -c /opt/Proxy/shadowsocksr/user-config.json
Restart=on-abort

[Install]
WantedBy=multi-user.target
 -->

sudo systemctl daemon-reload
sudo systemctl restart shadowsocksr
sudo systemctl status shadowsocksr

<!-- sudo tar -zxvf shadowsocks-local.tar.gz 
sudo tar -zxvf autoproxy.pac_.tar.gz 
sudo gedit ss.json
./shadowsocks-local -c ss.json  -->
```

Pycharm:
---
```
sudo tar -zxvf pycharm-community-2019.2.4.tar.gz 
```

ideaIC:
---
```
sudo mkdir /opt/intelliJ
sudo tar -zxvf ideaIC-2020.1.2.tar.gz -C /opt/intelliJ/ 
```

Navicat:
---
```
sudo tar -zxvf navicat121_premium_cs_x64.tar.gz

sudo vim /usr/share/applications/navicat.desktop

<!-- 
[Desktop Entry]
Encoding=UTF-8
Name=Navicat
Comment=The Smarter Way to manage dadabase
Exec=/opt/navicat/navicat15-mysql-cs.AppImage
Icon=/opt/navicat/navicat.png
Categories=Application;Database;MySQL;navicat
Version=1.0
Type=Application
Terminal=0
 -->

<!-- http://www.navicat.com.cn/images/02.Product_00_AllProducts_Premium_large.png -->
rm -rf ~/.navicat
```

Robo3t:
---
```
sudo mkdir /opt/robo3t
sudo tar -zxvf robo3t-1.3.1-linux-x86_64-7419c406.tar.gz -C /opt/robo3t

sudo vim /usr/share/applications/robo3t.desktop 

<!-- 
[Desktop Entry]
Encoding=UTF-8
Name=Robo3t
Comment=The Smarter Way to manage dadabase
Exec=/opt/robo3t/robo3t-1.3.1-linux-x86_64-7419c406/bin/robo3t
Icon=/opt/robo3t/robo3t-1.3.1-linux-x86_64-7419c406/icon/robomongo.png
Categories=Application;Database;mongoDB;robo3t
Version=1.0
Type=Application
Terminal=0
 -->

<!-- https://robomongo.org/static/robomongo-128x128-129df2f1.png -->
```

postman：
---
```

sudo tar -zxf Postman-linux-x64-7.29.1.tar.gz -C /opt/
sudo vim /usr/share/applications/Postman.desktop

<!-- 
[Desktop Entry]
Encoding=UTF-8
Name=Postman
Comment=Postman
Exec=/opt/Postman/Postman
Icon=/opt/Postman/app/resources/app/assets/icon.png
Categories=Application;postman
Version=1.0
Type=Application
Terminal=0
 -->

<!-- 
/opt/Postman/Postman
/opt/Postman/app/resources/app/assets/icon.png
 -->
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

thunderbird：
---
```
安装
sudo apt-get install thunderbird
安装中文包
sudo apt-get install thunderbird-locale-zh-cn
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


sudo apt-get  remove  ibus 
系统优化：
---

磁盘挂载：
```
sudo fdisk -l
sudo mkfs.ext4 /dev/sdb
sudo fdisk -l
cd home/
ls
cd aijia/
ls
mkdir Data
sudo mount /dev/sdb /home/aijia/Data
sudo blkid
sudo vim /etc/fstab

UUID=*** /* ext4 defaults 0 2
```

桌面优化：
---
sudo apt-get install gnome-shell-extensions
sudo apt install chrome-gnome-shell
sudo apt install gnome-tweaks
sudo apt install gnome-tweak-tool

必应每日壁纸
安装方法有很多，我觉得最方便的还是用chrome装gnome扩展（Bing Wallpaper Changer）

good-bye-gdm-flick/

[Plymouth Theme]
Name=Ubuntu Logo
Description=A theme that features a blank background with a logo
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/suade
ScriptFile=/usr/share/plymouth/themes/suade/mdv.script


操作优化：
---

快捷鍵
---
```
gsettings get org.gnome.desktop.wm.keybindings switch-to-workspace-left
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left "[]"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right "[]"
```
