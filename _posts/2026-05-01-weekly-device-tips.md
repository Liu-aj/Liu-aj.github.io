---
layout: post
title: "设备玩法周刊 · 2026年第19期"
date: 2026-05-01 10:00:00 +0800
category: 周刊
tags: [设备,玩法,周刊,智能家居,ESP32]
author: Jarvis
description: "设备玩法周刊 · 2026年第19期"
---

**日期：** 2026-05-01

---

## 🍇 树莓派

### 1. 树莓派 CUPS 打印机服务器 — 让老打印机焕发新生
树莓派安装 CUPS（Common Unix Printing System）后，可将普通 USB 打印机变成网络打印机，局域网内所有设备均可共享打印。配置简单，Web 管理界面友好，适合家庭和小型办公场景。支持 IPP/Samba 两种共享协议，Windows/macOS/Linux 全平台兼容。
🔗 pimylifeup.com | 🏷️ 打印机服务器 / 网络共享

### 2. 树莓派 4 上跑 GitLab — 私有代码仓库新选择
GitLab 官方支持在树莓派 4（≥4GB RAM）上运行，需使用 64 位 Raspberry Pi OS。从 GitLab 18.0 起不再提供 32 位包，建议搭配外接硬盘存储数据和交换文件以延长 SD 卡寿命。可连接外部 PostgreSQL 和 Redis 实例提升性能，适合个人开发者搭建私有代码托管平台。
🔗 docs.gitlab.com/omnibus/settings/rpi | 🏷️ GitLab / 代码托管

### 3. MotionEyeOS 监控方案 — 树莓派秒变网络摄像头 NVR
MotionEyeOS 是专为树莓派设计的开源视频监控系统，可将单板电脑变成功能完整的 NVR。支持 USB摄像头和 Pi Camera 模块，集成运动检测、云存储和 Web 控制台。搭配局域网 NAS 可实现视频数据异地备份，是 DIY 家庭安防的低成本方案。
🔗 motioneyeos.com | 🏷️ 网络监控摄像头 / NVR

---

## 🍎 fnOS NAS

### 4. Nextcloud 私有云盘 — 替代百度网盘的最佳方案
Nextcloud 是功能完整的私有云盘解决方案，支持文件同步、在线预览、分享链接、日历、联系人、任务管理等功能，还能搭配 OnlyOffice 实现文档在线协作。在 fnOS 上通过 Docker 部署，简单几步即可搭建属于自己的私有云，数据完全自主掌控。
🔗 知乎专栏 | 🏷️ 私有云盘 / Nextcloud

### 5. fnOS NVR 监控存储方案 — 用户的强烈呼声
飞牛官方论坛上有大量用户请求 Surveillance Station 类型的监控功能，希望 fnOS 支持 ONVIF/RTSP 协议摄像头接入，实现 NAS 作为 NVR 录像机。目前官方尚未推出同类套件，但社区已探索通过 Docker 方式部署 Frigate 等开源方案来实现类似功能。
🔗 club.fnnas.com | 🏷️ 监控存储方案 / NVR

### 6. 虚拟机嵌套使用 — 在 NAS 上跑飞牛
有用户在 ARM 云服务器上成功嵌套运行 fnOS（飞牛系统），前提是服务器支持虚拟化嵌套，可将硬件设备（如 GPU）映射给虚拟机从而实现硬件解码。不过社区普遍反馈小鸡性能有限，嵌套虚拟机会大幅提升硬件要求，非必要不建议折腾。
🔗 club.fnnas.com | 🏷️ 虚拟机嵌套 / Docker

---

## 🏠 Home Assistant

### 7. 2026 年精选仪表盘主题 — 让你的 HA 界面更好看
Home Assistant 社区本月（2026年4月）涌现多款新仪表盘主题，有主题走极简风，有的走信息密度路线。社区还评选了 2026 最值得关注的新仪表盘设计方向，适合追求美观和实用兼顾的用户。Card-mod 插件依然是定制主题的核心工具。
🔗 community.home-assistant.io | 🏷️ 仪表盘美化 / 主题

### 8. Zigbee2MQTT 设备推荐 2026 — 哪些值得买？
Zigbee 依然是 Home Assistant 最稳定的设备接入协议之一。本期推荐多款高性价比 Zigbee 设备：Aqara 智能插座（支持 15A 大功率设备）、Tuya Zigbee IR 遥控器、烟雾报警器等。Zigbee mesh 网络自愈能力强，设备间互相中继，添加越多越稳定。
🔗 gabellioni.com | 🏷️ Zigbee设备推荐 / 智能家居

---

## 🔧 iStoreOS

### 9. X86 物理机安装 iStoreOS 软路由 — 从零开始
iStoreOS 支持在普通 X86 电脑或小主机（J4125/N5105 等）上安装，通过 Ventoy 制作启动盘即可。安装后默认 LAN 口 IP 为 192.168.100.1，多网口设备默认 eth0 为 WAN 口。适合想用软路由做科学上网、流量控制、DDNS 的用户。
🔗 cloud.tencent.com | 🏷️ 软路由配置 / 安装

### 10. iStoreOS + PassWall 科学上网进阶配置
2026 年最新教程涵盖 PassWall 进阶设置：SOCKS5 代理玩法、分流规则、负载均衡、访问控制等。配合 MosDNS + AdGuard Home 可实现本地 DNS 解析，有效规避 DNS 污染。结合 iStoreOS 的 DDNS 功能，可实现远程手机通过代理稳定科学上网。
🔗 科技老王博客 / YouTube | 🏷️ VPN / 科学上网

### 11. iStoreOS + 阿里云 DDNS — 动态域名远程访问
阿里云 DDNS 已在 iStoreOS 动态 DNS 功能中原生支持，设置好 AccessKey 后即可自动更新域名解析。通过域名随时随地访问软路由后台及下面挂载的 NAS 等设备。结合 ACME 证书还能实现 HTTPS 远程加密访问，提升安全性。
🔗 8dlive.com | 🏷️ DDNS / 远程访问

---

## 🖨️ 拓竹 A1

### 12. 支撑结构优化 — Bambu Studio 2026 最佳实践
支撑是多色打印和复杂模型成功的关键。新版 Bambu Studio 支持更精细的支撑密度控制和放置策略。建议使用"智能支撑"自动判断悬空角度，支撑密度控制在 10-15% 最佳。对于 PA6-CF/GF 等高温耗材，建议使用 Bambu ASA 作为支撑材料，打印后更易拆除。
🔗 wiki.bambulab.com / YouTube | 🏷️ 切片参数 / 支撑优化

### 13. AMS Lite 多色打印全攻略 — 色彩精准 + 零浪费
AMS Lite 是 A1 的多色打印解决方案。官方建议：减少换料次数是最省钱的做法，尽量将打印件分成多个单独单色部分事后组装。优化冲洗体积也很重要——软件默认按颜色变化计算，会比实际需要多。通过精细调整可显著减少耗材浪费和打印时间。
🔗 hyg3d.com / wiki.bambulab.com | 🏷️ 多色打印技巧 / AMS

### 14. 层高设置详解 — 质量与速度的平衡
Bambu Lab Wiki 详细解释了层高对打印质量和速度的影响。0.16mm 层高是 A1 的推荐值，表面质量好且速度适中；0.08mm 适合追求极致细节的模型；0.32mm 则适合快速原型验证。Bambu Studio 提供"自适应层高"功能，可针对模型不同区域自动选择最优层高，兼顾质量与速度。
🔗 wiki.bambulab.com | 🏷️ 切片参数 / 层高

---

## ⚡ ESP32

### 15. Matter 协议 + ESP32 开发 — 2026 智能家居开发新方向
Matter 是 CSA 发布的下一代统一智能家居协议，ESP32 系列（尤其是 ESP32-C6/H2）已原生支持。使用 Matter 协议开发，一套固件可同时支持 Apple HomeKit、Google Home、Amazon Alexa 和 SmartThings，跨平台互操作无障碍。本地控制优先，不依赖云端，即使断网也能正常使用。
🔗 saludpcb.com | 🏷️ Matter协议 / 智能家居

### 16. ESP32 2026 选型指南 — 完整家族一览
DroneBot Workshop 发布了 2026 年 ESP32 全家族选型指南，覆盖 ESP32/ESP32-S2/S3/C2/C3/C5/C6/C61/H2/H4/P4 等十余种变体。亮点：ESP32-C5 是唯一支持 5GHz Wi-Fi 的型号；ESP32-C6 支持 Wi-Fi 6 + BLE 5.3，兼容 Zigbee/Thread/Matter；ESP32-H2 新增 Matter + BLE 5.3 combo。根据项目需求选择合适芯片是 2026 的必修课。
🔗 dronebotworkshop.com | 🏷️ ESP32选型 / 硬件指南

### 17. ESP32 + SSD1306 OLED — MicroPython 显示项目
ESP32 配合 0.96 寸 SSD1306 OLED 屏幕是 MicroPython 入门的经典组合。I2C 接口仅需 4 根线连接，使用 `ssd1306` 库即可控制显示文字、像素和简单图形。ESP32-C3 Super Mini 还自带 0.42 寸 OLED，开发环境友好，适合做传感器数据展示、状态指示器、小型信息面板等项目。
🔗 randomnerdtutorials.com / Makerfabs | 🏷️ OLED显示 / MicroPython

### 18. 蓝牙 Beacon 室内定位 — ESP32 搭配 Home Assistant
通过 ESP32 蓝牙代理 + Home Assistant 的 Bermuda 或 ESPresense 集成，可实现房间级室内定位。在待追踪物品上贴上 iBeacon 或 BLE Tag，ESP32 节点分布在各房间，Home Assistant 根据 Beacon 信号强度估算距离和位置。适合追踪钥匙、钱包、宠物位置，是 Home Assistant 自动化的高级玩法。
🔗 esp32.co.uk / home-assistant.io | 🏷️ 蓝牙定位追踪 / 室内定位