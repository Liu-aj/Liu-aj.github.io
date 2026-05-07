---
title: ESP32总览
description: ESP32是一款支持Wi-Fi和蓝牙的物联网芯片，广泛应用于智能家居和嵌入式开发
tags:
- ESP32
- 嵌入式
- IoT
- 总览
---

# ESP32 总览 💻

> ESP32 是一款支持 Wi-Fi 和蓝牙的物联网芯片，广泛应用于智能家居和嵌入式开发

***

## 📦 ESP32 家族

| 型号 | 核心 | Wi-Fi | BLE | 适用场景 |
|------|------|-------|-----|----------|
| ESP32 | 双核 240MHz | ✅ | ✅ | 通用物联网 |
| ESP32-S3 | 双核 240MHz | ✅ | ✅ | AIoT 应用 |
| ESP32-C3 | 单核 RISC-V | ✅ | BLE 5.0 | 低功耗 |
| ESP32-C6 | 单核 RISC-V | ✅ | BLE 5.0 | Matter 协议 |

## 🔌 常用外设

| 外设 | 协议 | 相关指南 |
|------|------|----------|
| SSD1306 OLED | I2C | [OLED 显示](esp32-ssd1306-oled/) |
| DS18B20 | OneWire | [温度传感器](esp32-ds18b20-home-assistant-guide/) |
| 电机控制 | PWM | [电机控制](esp32-motor-control-guide/) |

## 📡 通信协议

| 协议 | 说明 |
|------|------|
| Matter | 智能家居统一协议 |
| MQTT | 物联网消息传输 |
| Wi-Fi | 无线网络连接 |

## 📖 入门指南

- [Matter 协议开发完全指南](esp32-matter-guide/)
- [ESP32 家族选型指南 2026](esp32-family-2026/)
