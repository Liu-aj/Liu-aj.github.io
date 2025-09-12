---
---
layout: post
title: Ubuntu 20.04系统完全配置指南
date: 2019-11-28 16:21:00
forType: OS
category: Linux
tag: [Linux, Ubuntu, 系统配置, 开发环境, 软件安装]
---

* content
{:toc}

## 一、Ubuntu系统初始化配置

### 1.1 网络设置

#### 1.1.1 初始化无线网卡

对于部分Ubuntu系统，特别是新安装的系统，可能需要手动安装无线网卡驱动。以下是安装Broadcom无线网卡驱动的步骤：

```bash
# 进入Ubuntu安装镜像的软件包目录
cd /media/liuaj/Ubuntu\ 20.0/pool/main/

# 安装编译工具链依赖
sudo dpkg -i g/gcc-9/libasan5_9.3.0-10ubuntu2_amd64.deb
sudo dpkg -i g/gcc-10/libitm1_10-20200411-0ubuntu1_amd64.deb
sudo dpkg -i g/gcc-10/libatomic1_10-20200411-0ubuntu1_amd64.deb
sudo dpkg -i g/gcc-10/liblsan0_10-20200411-0ubuntu1_amd64.deb
sudo dpkg -i g/gcc-10/libubsan1_10-20200411-0ubuntu1_amd64.deb
sudo dpkg -i g/gcc-10/libquadmath0_10-20200411-0ubuntu1_amd64.deb
sudo dpkg -i g/gcc-10/libtsan0_10-20200411-0ubuntu1_amd64.deb
sudo dpkg -i g/gcc-9/libgcc-9-dev_9.3.0-10ubuntu2_amd64.deb
sudo dpkg -i m/make-dfsg/make_4.2.1-1.2_amd64.deb
sudo dpkg -i b/binutils/binutils-common_2.34-6ubuntu1_amd64.deb
sudo dpkg -i g/gcc-10/gcc-10-base_10-20200411-0ubuntu1_i386.deb
sudo dpkg -i b/binutils/libctf-nobfd0_2.34-6ubuntu1_amd64.deb
sudo dpkg -i b/binutils/libbinutils_2.34-6ubuntu1_amd64.deb
sudo dpkg -i b/binutils/libctf0_2.34-6ubuntu1_amd64.deb
sudo dpkg -i b/binutils/binutils-x86-64-linux-gnu_2.34-6ubuntu1_amd64.deb
sudo dpkg -i b/binutils/binutils_2.34-6ubuntu1_amd64.deb
sudo dpkg -i d/dpkg/dpkg-dev_1.19.7ubuntu3_all.deb
sudo dpkg -i g/glibc/libc-dev-bin_2.31-0ubuntu9_amd64.deb
sudo dpkg -i l/linux/linux-libc-dev_5.4.0-26.30_amd64.deb
sudo dpkg -i libx/libxcrypt/libcrypt-dev_4.4.10-10ubuntu4_amd64.deb
sudo dpkg -i g/glibc/libc6-dev_2.31-0ubuntu9_amd64.deb
sudo dpkg -i g/gcc-9/libstdc++-9-dev_9.3.0-10ubuntu2_amd64.deb
sudo dpkg -i g/gcc-9/gcc-9_9.3.0-10ubuntu2_amd64.deb
sudo dpkg -i g/gcc-9/g++-9_9.3.0-10ubuntu2_amd64.deb
sudo dpkg -i g/gcc-defaults/gcc_9.3.0-1ubuntu2_amd64.deb
sudo dpkg -i d/dkms/dkms_2.8.1-5ubuntu1_all.deb

# 安装Broadcom无线网卡驱动
sudo dpkg -i ../../../restricted/b/bcmwl/bcmwl-kernel-source_6.30.223.271+bdcom-0ubuntu5_amd64.deb
```

#### 1.1.2 替换国内源

为了提高软件下载速度，建议将Ubuntu默认的软件源替换为国内镜像源：

```bash
# 查看当前Ubuntu版本
lsb_release -a

# 备份原软件源配置文件
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 编辑软件源配置文件
sudo gedit /etc/apt/sources.list
```

将文件内容替换为以下网易163源（适用于Ubuntu 20.04 "Focal Fossa"）：

```
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

保存文件后执行以下命令更新软件包列表：

```bash
sudo apt-get update
sudo apt-get upgrade
```

#### 1.1.3 开启SSH服务（22端口）

安装并启用SSH服务，便于远程连接和管理：

```bash
# 安装SSH服务
sudo apt-get install openssh-server openssh-client

# 启动SSH服务
sudo service ssh start

# 验证SSH服务是否启动成功
ssh localhost
lsof -i:22

# 设置SSH服务开机自启
sudo systemctl enable ssh
```

### 1.2 基础环境搭建

#### 1.2.1 Git安装与配置

```bash
# 安装Git
sudo apt install git

# 配置Git用户信息
git config --global user.name "您的用户名"
git config --global user.email "您的邮箱地址"

# 查看Git配置
git config --list

# 安装Git图形界面客户端
sudo apt-get install git-cola
```

#### 1.2.2 Vim编辑器安装

```bash
# 安装Vim
sudo apt install vim
```

#### 1.2.3 JDK安装与配置

```bash
# 1. 前往Oracle Java官网下载JDK安装包
# 官网地址：https://www.oracle.com/java/technologies/downloads/

# 2. 解压缩到指定目录（以jdk-8u241-linux-x64.tar.gz为例）
# 创建安装目录
sudo mkdir -p /usr/lib/jvm

# 解压缩到该目录
sudo tar -zxvf jdk-8u241-linux-x64.tar.gz -C /usr/lib/jvm/

# 3. 修改环境变量
sudo vim ~/.bashrc

# 在文件末尾追加下面内容：
#set oracle jdk environment
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_241
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

# 使环境变量立即生效
source ~/.bashrc

# 4. 系统注册此JDK版本
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk1.8.0_241/bin/java 300

sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk1.8.0_241/bin/javac 300

sudo update-alternatives --install /usr/bin/jar jar /usr/lib/jvm/jdk1.8.0_241/bin/jar 300

# 5. 配置默认JDK版本
sudo update-alternatives --config java

# 6. 验证Java安装是否成功
java -version
javac -version
```

## 二、常用软件安装

### 2.1 浏览器与办公软件

#### 2.1.1 Google Chrome浏览器

```bash
# 下载Chrome安装包（可从官网下载）
# 官网地址：https://www.google.cn/chrome/

# 安装Chrome
sudo dpkg -i google-chrome-stable_current_amd64.deb

# 如果安装过程中出现依赖问题，执行以下命令修复
sudo apt-get install -f
```

#### 2.1.2 WPS Office

```bash
# 下载WPS安装包
# 官网地址：https://www.wps.cn/product/wpslinux

# 安装WPS
sudo dpkg -i wps-office_11.1.0.8865_amd64.deb

# 修复可能的依赖问题
sudo apt-get install -f
```

#### 2.1.3 Sublime Text编辑器

```bash
# 将Sublime Text安装包复制到/opt目录
sudo cp sublime_text_3_build_3211_x64.tar.bz2 /opt/

# 切换到/opt目录并解压
cd /opt/
sudo tar -jxvf sublime_text_3_build_3211_x64.tar.bz2

sudo mv sublime_text_3 sublime_text

# 创建桌面快捷方式
sudo vim sublime_text/sublime_text.desktop
```

在编辑器中添加以下内容：

```
[Desktop Entry]
Encoding=UTF-8
Name=Sublime Text
Comment=Sublime Text Editor
Exec=/opt/sublime_text/sublime_text
Icon=/opt/sublime_text/Icon/256x256/sublime-text.png
Categories=Application;Development;Editor
Version=1.0
Type=Application
Terminal=false
```

保存后，复制快捷方式到应用程序目录：

```bash
sudo cp sublime_text/sublime_text.desktop /usr/share/applications/
```

#### 2.1.4 Linux版QQ

```bash
# 安装Linux版QQ
sudo dpkg -i linuxqq_2.0.0-b1-1024_amd64.deb

# 修复依赖问题
sudo apt-get install -f
```

### 2.2 开发工具

#### 2.2.1 PyCharm社区版

```bash
# 解压PyCharm安装包
sudo tar -zxvf pycharm-community-2019.2.4.tar.gz -C /opt/

# 进入安装目录并启动PyCharm
cd /opt/pycharm-community-2019.2.4/bin/
./pycharm.sh

# 首次启动后，可以通过工具创建桌面快捷方式
```

#### 2.2.2 IntelliJ IDEA Community

```bash
# 创建安装目录
sudo mkdir -p /opt/intelliJ

# 解压安装包到指定目录
sudo tar -zxvf ideaIC-2020.1.2.tar.gz -C /opt/intelliJ/

# 启动IDEA
cd /opt/intelliJ/idea-IC-201.7846.76/bin/
./idea.sh

# 首次启动后，可以通过工具创建桌面快捷方式
```

#### 2.2.3 Navicat数据库管理工具

```bash
# 解压Navicat安装包
sudo tar -zxvf navicat121_premium_cs_x64.tar.gz -C /opt/

sudo mv /opt/navicat121_premium_cs_x64 /opt/navicat

# 创建桌面快捷方式
sudo vim /usr/share/applications/navicat.desktop
```

添加以下内容：

```
[Desktop Entry]
Encoding=UTF-8
Name=Navicat
Comment=Database Management Tool
Exec=/opt/navicat/start_navicat
Icon=/opt/navicat/navicat.png
Categories=Application;Database;Development
Version=1.0
Type=Application
Terminal=false
```

#### 2.2.4 Robo3T（MongoDB客户端）

```bash
# 创建安装目录
sudo mkdir -p /opt/robo3t

# 解压安装包
sudo tar -zxvf robo3t-1.3.1-linux-x86_64-7419c406.tar.gz -C /opt/robo3t

# 创建桌面快捷方式
sudo vim /usr/share/applications/robo3t.desktop
```

添加以下内容：

```
[Desktop Entry]
Encoding=UTF-8
Name=Robo3T
Comment=MongoDB Management Tool
Exec=/opt/robo3t/robo3t-1.3.1-linux-x86_64-7419c406/bin/robo3t
Icon=/opt/robo3t/robo3t-1.3.1-linux-x86_64-7419c406/icon/robomongo.png
Categories=Application;Database;Development
Version=1.0
Type=Application
Terminal=false
```

#### 2.2.5 Postman API测试工具

```bash
# 解压Postman安装包
sudo tar -zxf Postman-linux-x64-7.29.1.tar.gz -C /opt/

# 创建桌面快捷方式
sudo vim /usr/share/applications/Postman.desktop
```

添加以下内容：

```
[Desktop Entry]
Encoding=UTF-8
Name=Postman
Comment=API Development Environment
Exec=/opt/Postman/Postman
Icon=/opt/Postman/app/resources/app/assets/icon.png
Categories=Application;Development;API
Version=1.0
Type=Application
Terminal=false
```

### 2.3 网络工具

#### 2.3.1 花生壳动态域名解析

```bash
# 启动花生壳服务
phddns start

# 查看花生壳版本
phddns version

# 访问花生壳管理页面进行配置
# 管理地址：http://b.oray.com
```

### 2.4 媒体工具

#### 2.4.1 Thunderbird邮件客户端

```bash
# 安装Thunderbird
sudo apt-get install thunderbird

# 安装中文语言包
sudo apt-get install thunderbird-locale-zh-cn

# 启动Thunderbird后，在设置中选择中文语言
```

## 三、服务器软件安装

### 3.1 Nginx安装与配置

```bash
# 安装编译依赖
sudo apt-get install build-essential
sudo apt-get install libtool

# 创建源码目录并下载所需软件包
cd /usr/local/src

# 下载PCRE库
sudo wget http://sourceforge.net/projects/pcre/files/pcre/8.43/pcre-8.43.tar.gz
sudo tar -zxvf pcre-8.43.tar.gz

# 编译安装PCRE
cd pcre-8.43/
sudo ./configure
sudo make
sudo make install

# 返回源码目录
cd ..

# 下载并安装zlib库
sudo wget http://zlib.net/zlib-1.2.11.tar.gz
sudo tar -zxvf zlib-1.2.11.tar.gz
cd zlib-1.2.11/
sudo ./configure
sudo make
sudo make install

# 返回源码目录
cd ..

# 下载并安装OpenSSL库
sudo wget https://www.openssl.org/source/openssl-1.0.2t.tar.gz
sudo tar -zxvf openssl-1.0.2t.tar.gz

# 下载并安装Nginx
sudo wget http://nginx.org/download/nginx-1.17.6.tar.gz
sudo tar -zxvf nginx-1.17.6.tar.gz
cd nginx-1.17.6/

# 配置Nginx编译参数
sudo ./configure --sbin-path=/usr/local/nginx/nginx --conf-path=/usr/local/nginx/nginx.conf --pid-path=/usr/local/nginx/nginx.pid --with-http_ssl_module --with-pcre=../pcre-8.43 --with-zlib=../zlib-1.2.11 --with-openssl=../openssl-1.0.2t

# 编译并安装
sudo make
sudo make install

# 启动Nginx
cd /usr/local/nginx/
sudo ./nginx

# 设置Nginx开机自启
sudo vim /lib/systemd/system/nginx.service
```

添加以下内容：

```
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=syslog.target network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/usr/local/nginx/nginx.pid
ExecStartPre=/usr/local/nginx/nginx -t
ExecStart=/usr/local/nginx/nginx
ExecReload=/usr/local/nginx/nginx -s reload
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

保存后，启用开机自启：

```bash
sudo systemctl daemon-reload
sudo systemctl enable nginx
sudo systemctl start nginx
```

### 3.2 Docker安装与配置

```bash
# 1. 更新Ubuntu的apt源索引
sudo apt-get update

# 2. 安装包允许apt通过HTTPS使用仓库
sudo dpkg --configure -a
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

# 3. 添加Docker官方GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# 4. 设置Docker稳定版仓库
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# 5. 更新apt源索引
sudo apt-get update

# 6. 安装最新版本Docker CE（社区版）
sudo apt-get install docker-ce

# 7. 查看安装Docker的版本
docker --version

# 8. 检查Docker CE是否安装正确
sudo docker run hello-world

# 9. 将当前用户添加到docker用户组（避免每次使用sudo）
sudo usermod -aG docker $USER

# 注意：添加用户组后需要注销并重新登录才能生效
```

#### Docker基本命令

```bash
# 启动Docker服务
sudo service docker start

# 停止Docker服务
sudo service docker stop

# 重启Docker服务
sudo service docker restart

# 列出本地镜像
docker image ls

# 拉取镜像
docker image pull library/hello-world

# 删除镜像
docker image rm 镜像ID

# 创建并启动容器
docker run [选项参数] 镜像名 [命令]

# 停止一个运行中的容器
docker container stop 容器ID/容器名

# 启动一个已停止的容器
docker container start 容器ID/容器名

# 强制停止一个运行中的容器
docker container kill 容器ID/容器名

# 删除容器
docker container rm 容器ID/容器名

# 查看容器日志
docker container logs 容器ID/容器名

# 进入运行中的容器
docker container exec -it 容器ID/容器名 /bin/bash
```

## 四、系统优化与个性化

### 4.1 输入法配置

```bash
# 卸载ibus输入法框架（如果不需要）
sudo apt-get remove ibus

# 安装fcitx输入法框架
sudo apt-get install fcitx fcitx-pinyin fcitx-googlepinyin fcitx-config-gtk

# 配置输入法（在系统设置中选择fcitx为默认输入法框架）
```

### 4.2 磁盘挂载

```bash
# 查看当前磁盘使用情况
df -h

# 查看磁盘分区情况
lsblk -f
sudo fdisk -l

# 假设我们要格式化并挂载/dev/sdb磁盘
# 分区（如果尚未分区）
sudo fdisk /dev/sdb
# 按照提示创建新分区

# 格式化分区为ext4文件系统
sudo mkfs -t ext4 /dev/sdb1

# 创建挂载点
mkdir -p ~/appdata

# 临时挂载分区
sudo mount /dev/sdb1 /home/liuaj/appdata/

# 获取分区的UUID
sudo blkid

# 配置开机自动挂载
sudo vim /etc/fstab
```

在文件末尾添加类似以下内容（根据实际UUID修改）：

```
UUID=12345678-1234-1234-1234-123456789012 /home/liuaj/appdata ext4 defaults 0 2
```

保存后，测试挂载配置：

```bash
sudo mount -a
df -h
```

### 4.3 桌面环境优化

```bash
# 安装GNOME Shell扩展管理工具
sudo apt-get install gnome-shell-extensions
sudo apt install chrome-gnome-shell
sudo apt install gnome-tweaks
sudo apt install gnome-tweak-tool

# 安装后，可以通过GNOME Tweaks工具进行各种桌面优化
# 推荐安装的扩展：
# - Dash to Dock: 自定义Dock栏
# - Bing Wallpaper Changer: 必应每日壁纸
# - User Themes: 允许使用自定义主题
# - OpenWeather: 天气显示

# 可以通过Chrome浏览器访问GNOME扩展网站安装扩展
# 扩展网站：https://extensions.gnome.org/
```

### 4.4 实用工具安装

#### 4.4.1 截图工具Flameshot

```bash
# 安装Flameshot
sudo apt-get install flameshot

# 配置快捷键：在系统设置->键盘快捷键中添加
# 命令：flameshot gui
# 快捷键：建议设置为PrintScreen键
```

#### 4.4.2 Unity控制面板（可选）

```bash
# 安装Unity控制面板（如果喜欢Unity风格的设置界面）
sudo apt-get install unity-control-center
```

### 4.5 快捷键设置

```bash
# 查看当前工作区切换快捷键
gsettings get org.gnome.desktop.wm.keybindings switch-to-workspace-left
gsettings get org.gnome.desktop.wm.keybindings switch-to-workspace-right

# 清除默认快捷键（如果需要自定义）
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left "[]"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right "[]"

# 建议使用系统设置->键盘快捷键进行图形化配置
```

## 五、系统维护与管理

### 5.1 系统更新与升级

```bash
# 更新软件包列表
sudo apt-get update

# 升级已安装的软件包
sudo apt-get upgrade

# 升级系统版本
sudo apt-get dist-upgrade

# 清理不再需要的依赖包
sudo apt-get autoremove

# 清理下载的安装包缓存
sudo apt-get autoclean
```

### 5.2 系统备份与恢复

```bash
# 使用rsync备份重要数据
sudo rsync -avh --progress /home/liuaj/ /backup/disk/

# 系统快照备份（使用Timeshift工具）
sudo add-apt-repository -y ppa:teejee2008/ppa
sudo apt-get update
sudo apt-get install timeshift

# 安装后通过图形界面配置系统快照
```

### 5.3 系统日志查看

```bash
# 查看系统日志
sudo journalctl

# 查看特定服务的日志
sudo journalctl -u nginx
sudo journalctl -u docker

# 实时查看日志
sudo journalctl -f

# 查看最近的系统日志
sudo journalctl -n 100
```

## 六、常见问题解决

### 6.1 软件依赖问题

```bash
# 修复损坏的软件包
sudo dpkg --configure -a

sudo apt-get install -f

# 清理损坏的依赖关系
sudo apt-get autoclean
sudo apt-get autoremove
```

### 6.2 系统卡顿问题

```bash
# 清理内存缓存
sudo sync && sudo sysctl -w vm.drop_caches=3

# 检查系统资源使用情况
top
htop # 如未安装：sudo apt-get install htop

# 关闭不必要的服务
systemctl list-unit-files --type=service
# 禁用不需要的服务
sudo systemctl disable 服务名
```

### 6.3 网络连接问题

```bash
# 重启网络服务
sudo systemctl restart NetworkManager

# 查看网络接口状态
ip addr show

# 测试网络连接
ping -c 4 www.baidu.com
```

通过本文档的指南，您应该能够完成Ubuntu 20.04系统的基本配置、常用软件安装以及系统优化。如果在操作过程中遇到问题，可以参考本文档的"常见问题解决"部分，或者通过Ubuntu官方文档和社区获取更多帮助。

