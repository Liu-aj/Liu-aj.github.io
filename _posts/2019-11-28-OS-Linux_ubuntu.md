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
sudo dpkg -i libgcc-7-dev_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libitm1_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libatomic1_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/libasan4_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/gcc-7_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i liblsan0_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libtsan0_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/libubsan0_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/libcilkrts5_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libmpx2_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i libquadmath0_8.3.0-6ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i ../gcc-7/libgcc-7-dev_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i gcc-7_7.4.0-1ubuntu1~18.04.1_amd64.deb 
sudo dpkg -i gcc_7.4.0-1ubuntu2.3_amd64.deb 
sudo dpkg -i make_4.1-9.1ubuntu1_amd64.deb 
sudo dpkg -i dpkg-dev_1.19.0.5ubuntu2.1_all.deb 
sudo dpkg -i dkms_2.3-3ubuntu9.5_all.deb 
sudo dpkg -i linux-libc-dev_4.15.0-55.60_amd64.deb 
sudo dpkg -i libc-dev-bin_2.27-3ubuntu1_amd64.deb 
sudo dpkg -i libc6-dev_2.27-3ubuntu1_amd64.deb 
sudo dpkg -i bcmwl-kernel-source_6.30.223.271+bdcom-0ubuntu4_amd64.deb
```

替换国内源
---
```
lsb_release -a
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bcakup
sudo gedit /etc/apt/sources.list

# 阿里云源
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
##測試版源
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
# 源碼
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
##測試版源
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse


# 清华大学源
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
##測試版源
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
# 源碼
deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
##測試版源
deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
————————————————
版权声明：本文为CSDN博主「寥廓长空」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/baidu_36602427/java/article/details/86551862

sudo apt-get update
sudo apt-get upgrade
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
	sudo tar -zxvf jdk-7u60-linux-x64.gz -C /usr/lib/jvm
3.修改环境变量:　　
	sudo vi ~/.bashrc
在文件末尾追加下面内容：
#set oracle jdk environment
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_191
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

使环境变量马上生效：
	source ~/.bashrc
4、系统注册此jdk
	sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk1.8.0_191/bin/java 300
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

shadowsocks服务端
---
```
apt-get install shadowsocks
vim /etc/shadowsocks.json
	{
		"server": "0.0.0.0",
		"server_port": 13090,
		"local_port": 1080,
		"password": "123456",
		"timeout": 600,
		"method": "aes-256-cfb"
	}
ssserver -c /etc/shadowsocks.json -d restart
```

Pycharm:
---
```
sudo snap install pycharm-community --classic
sudo tar -zxvf pycharm-community-2019.2.4.tar.gz 
```

ideaIC:
---
```
sudo snap install intellij-idea-community --classic
sudo tar -zxvf ideaIC-2019.2.4.tar.gz 
```

eclipse:
---
```
snap install --classic eclipse
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

磁盘挂载：
```
df -h
lsblk -f
sudo fdisk -l
sudo fdisk /dev/sdb
sudo mkfs -t ext4 /dev/sdb1
lsblk -f
sudo fdisk -l
sudo mount /dev/sdb1 /home/liuaj/Data/
sudo vim /etc/fstab
"/dev/sdb1	/home/liuaj/Data	ext4	defaults	0 0"
sudo mount -a
df -h
"卸载：umount 设备名称 或者 挂载目录"
```

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

安装步骤：
1.更新Ubuntu的apt源索引
```
$ sudo apt-get update
```
2.安装包允许apt通过HTTPS使用仓库
```
$ sudo dpkg --configure -a
$ sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```
3.添加Docker官方GPG key
```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
4.设置Docker稳定版仓库
```
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```
5.更新apt源索引
```
$ sudo apt-get update
```
6.安装最新版本Docker CE（社区版）
```
$ sudo apt-get install docker-ce
```
查看安装Docker的版本
```
$ docker --version
```
检查Docker CE 是否安装正确
```
$ sudo docker run hello-world
```
基本命令
---
# 启动docker
```
sudo service docker start
```

# 停止docker
```
sudo service docker stop
```

# 重启docker
```
sudo service docker restart
```

# 列出镜像
```
docker image ls
```

# 拉取镜像
```
docker image pull library/hello-world
```

# 删除镜像
```
docker image rm 镜像id/镜像ID
```

# 创建容器
```
docker run [选项参数] 镜像名 [命令]
```

# 停止一个已经在运行的容器
```
docker container stop 容器名或容器id
```

# 启动一个已经停止的容器
```
docker container start 容器名或容器id
```

# kill掉一个已经在运行的容器
```
docker container kill 容器名或容器id
```

# 删除容器
```
docker container rm 容器名或容器id
```

操作优化：
---


