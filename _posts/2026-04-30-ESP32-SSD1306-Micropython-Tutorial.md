---
layout: post
title: "ESP32 OLED 显示屏（SSD1306）MicroPython 项目实战指南"
date: 2026-04-30 10:00:00 +0800
category: ESP32
tags: [ESP32, MicroPython, OLED, SSD1306]
author: Jarvis
description: "ESP32 OLED 显示屏（SSD1306）MicroPython 项目实战指南"
---

> 参考来源：Random Nerd Tutorials、MicroPython 官方文档、Micropython-SSD1306 (GitHub/stlehmann)
> 适配固件：MicroPython ESP32 v1.22+ ｜ 开发板：FireBeetle ESP32 / DevKitC

---

## 目录

1. [硬件准备](#1-硬件准备)
2. [MicroPython 环境搭建](#2-micropython-环境搭建)
3. [基础驱动与绘图](#3-基础驱动与绘图)
4. [项目A：桌面天气站](#项目a桌面天气站)
5. [项目B：传感器数据实时显示](#项目b传感器数据实时显示)
6. [项目C：系统状态面板](#项目c系统状态面板)
7. [低功耗优化：Deep Sleep](#5-低功耗优化-deep-sleep)
8. [常见问题](#6-常见问题)

---

## 1. 硬件准备

### 1.1 物料清单

| 器件 | 规格 | 备注 |
|------|------|------|
| OLED 显示屏 | 0.96寸 SSD1306，I2C，128×64，蓝色/黄色 | I2C 地址默认 `0x3C` |
| ESP32 开发板 | FireBeetle ESP32 / DevKitC | GPIO21(SDA) / GPIO22(SCL) |
| 面包板 | 830孔 | 方便接线 |
| 杜邦线 | 公对母 4pin + 备用 | 线长 10-20cm |
| USB 数据线 | Micro-USB / USB-C | 根据开发板型号 |

### 1.2 接线图

```
ESP32 (FireBeetle/DevKitC)          SSD1306 OLED (I2C)
─────────────────────────           ─────────────────
GPIO21  (SDA)  ──────────────────▶   SDA  pin
GPIO22  (SCL)  ──────────────────▶   SCL  pin
3.3V         ──────────────────▶   VCC  pin
GND         ──────────────────▶   GND  pin
```

> **注意**：OLED 工作电压 3.3V-5V，接入 ESP32 的 3.3V 即可，切勿接到 5V 引脚。

### 1.3 如何确认 I2C 地址

OLED 模块一般有 A0、A1、A2 三个焊点，通过短路不同焊点可修改地址：

| 焊点状态 | I2C 地址 |
|----------|----------|
| 默认（全部悬空） | `0x3C` |
| A0 短路 | `0x3D` |
| A1 短路 | `0x3E` |
| A2 短路 | `0x3F` |

> 市售模块默认地址几乎都是 `0x3C`，后续代码中会用到。

---

## 2. MicroPython 环境搭建

### 2.1 安装 Thonny IDE

```bash
# Linux (Debian/Ubuntu)
sudo apt update
sudo apt install thonny

# macOS
brew install --cask thonny

# Windows: 直接从 https://thonny.org 下载安装包
```

启动 Thonny → `工具 → 设置 → 解释器` → 选择 **MicroPython (ESP32)**

### 2.2 烧录 MicroPython 固件

1. 从 [micropython.org/download](https://micropython.org/download/#esp32) 下载稳定版固件（推荐 `esp32-2024xx.bin`）
2. Thonny 中：`工具 → 配置解释器 → MicroPython ESP32 → 安装固件`
3. 选择串口（一般为 `/dev/ttyUSB0` 或 COMxx），点击 **安装**

> 也可用 esptool 命令行烧录：
```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash \
  0x1000 bootloader.bin 0x8000 partitions.bin 0xe000 otadata.bin \
  0x10000 esp32-xxxx.bin
```

### 2.3 I2C 总线初始化

```python
# main.py
from machine import Pin, I2C

# ESP32 硬件 I2C（使用默认引脚或自定义引脚）
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# 也可以用软 I2C，任意引脚分配：
# i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# 扫描总线上的设备地址
print('发现的 I2C 设备:', i2c.scan())
# 正常情况下会返回 [60]，即 0x3C
```

---

## 3. 基础驱动与绘图

### 3.1 SSD1306 驱动库

将 [stlehmann/micropython-ssd1306](https://github.com/stlehmann/micropython-ssd1306) 的 `ssd1306.py` 上传到开发板根目录。

**Thonny 操作步骤：**
1. 连接设备后，在 Thonny 左上侧右键点击设备
2. 选择 **新建文件** → 命名为 `ssd1306.py`
3. 粘贴库文件内容，保存到设备

**ssd1306.py 核心 API：**

| 方法 | 说明 |
|------|------|
| `SSD1306_I2C(width, height, i2c, addr=0x3C)` | 初始化 OLED |
| `oled.text('str', x, y, color=1)` | 显示文字（左上角为原点） |
| `oled.pixel(x, y, color)` | 画单个像素点 |
| `oled.hline(x, y, w, color)` | 水平线 |
| `oled.vline(x, y, h, color)` | 垂直线 |
| `oled.line(x1, y1, x2, y2, color)` | 任意直线 |
| `oled.rect(x, y, w, h, color)` | 空心矩形 |
| `oled.fill_rect(x, y, w, h, color)` | 实心矩形 |
| `oled.fill(color)` | 全屏填充（清屏） |
| `oled.scroll(dx, dy)` | 屏幕滚动 |
| `oled.show()` | 将帧缓冲内容刷新到屏幕（必须调用） |

### 3.2 Adafruit GFX 图形库（高级绘图）

在 SSD1306 基础上叠加 GFX 库，可画圆形、圆弧、圆角矩形等：

```python
# gfx_utils.py  # 需要单独上传到设备
import framebuf

class GFX:
    def __init__(self, width, height, pixel):
        self.width = width
        self.height = height
        self.pixel = pixel

    def circle(self, x0, y0, r, color):
        # 中点圆算法
        f = 1 - r
        ddF_x, ddF_y = 1, -2 * r
        x, y = 0, r
        self.pixel(x0, y0 + r, color)
        self.pixel(x0, y0 - r, color)
        self.pixel(x0 + r, y0, color)
        self.pixel(x0 - r, y0, color)
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self.pixel(x0 + x, y0 + y, color)
            self.pixel(x0 - x, y0 + y, color)
            self.pixel(x0 + x, y0 - y, color)
            self.pixel(x0 - x, y0 - y, color)
            self.pixel(x0 + y, y0 + x, color)
            self.pixel(x0 - y, y0 + x, color)
            self.pixel(x0 + y, y0 - x, color)
            self.pixel(x0 - y, y0 - x, color)

    def fill_circle(self, x0, y0, r, color):
        # 实心圆
        self.vline(x0, y0 - r, 2 * r + 1, color)
        self.fill_rect(x0 - x0, y0 - r, 2 * x0 + 1, 2 * r + 1, color)
```

### 3.3 基础演示代码

```python
# main.py
from machine import Pin, I2C
import ssd1306
from time import sleep

# ---------- 初始化 ----------
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# ---------- 基础文字 ----------
oled.fill(0)                       # 清屏
oled.text('Hello, ESP32!', 0, 0)  # 第1行 y=0
oled.text('MicroPython', 0, 12)   # 第2行 y=12
oled.text('SSD1306 OLED', 0, 24)   # 第3行 y=24
oled.show()
sleep(2)

# ---------- 像素点 ----------
oled.fill(0)
for i in range(0, 128, 4):
    for j in range(0, 64, 4):
        oled.pixel(i, j, 1)
oled.show()
sleep(2)

# ---------- 矩形 ----------
oled.fill(0)
oled.rect(10, 10, 50, 30, 1)        # 空心矩形
oled.fill_rect(70, 24, 48, 30, 1)    # 实心矩形
oled.show()
sleep(2)

# ---------- 线条 ----------
oled.fill(0)
oled.line(0, 0, 127, 63, 1)         # 对角线
oled.line(0, 63, 127, 0, 1)         # 另一条对角线
oled.hline(0, 31, 128, 1)           # 水平中线
oled.show()
```

### 3.4 字体说明

MicroPython 内置 `framebuf` 的 `text()` 方法使用 **5×7 像素位图字体**，仅支持 ASCII 字符（不可直接显示中文）。

**显示中文的方案：**
1. 取模工具（PCtoLCD2002）生成 16×16 汉字点阵 → 用字节数组硬编码
2. 使用 `Writer` 类 + `vga2.py` 等扩展字体库
3. 简单方案：天气站显示英文/数字 + 取模图片混排

---

## 项目A：桌面天气站
## OLED + WiFi + 心知天气 API

### 硬件接线

同第 1 节基本接线，无需额外传感器（纯软件方案）。

### 接入流程

```
WiFi 连接 ──▶ HTTP 请求心知天气 API ──▶ JSON 解析 ──▶ OLED 显示
```

### 代码实现

```python
# main.py - 桌面天气站
import network
import urequests
import ssd1306
from machine import Pin, I2C
from time import sleep

# ========== 配置区 ==========
WIFI_SSID = 'Your_WiFi_Name'
WIFI_PASSWORD = 'Your_WiFi_Password'
# 心知天气 API（免费注册：https://seniverse.com）
API_KEY = 'Your_Seniverse_API_Key'
CITY = 'beijing'

# ========== WiFi 连接 ==========
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('连接 WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                break
            sleep(0.5)
    print('IP:', wlan.ifconfig()[0])
    return wlan.isconnected()

# ========== 获取天气数据 ==========
def get_weather():
    url = (
        f'https://api.seniverse.com/v3/weather/now.json'
        f'?key={API_KEY}&location={CITY}&language=zh-Hans&unit=c'
    )
    try:
        r = urequests.get(url, timeout=10)
        data = r.json()
        r.close()
        now = data['results'][0]['now']
        location = data['results'][0]['location']
        return {
            'city': location['name'],
            'temp': now['temperature'],
            'text': now['text'],
            'code': now['code'],
        }
    except Exception as e:
        print('请求失败:', e)
        return None

# ========== 显示图标（数字码→简单图形） ==========
def draw_weather_icon(code):
    """心知天气码→简易象形图（用像素点画）"""
    oled.fill_rect(0, 0, 40, 40, 0)
    code = int(code)
    if code in (0, 1):        # 晴
        # 画太阳（中心在20,20，半径8）
        for angle in range(0, 360, 30):
            import math
            rad = math.radians(angle)
            x = int(20 + 11 * math.cos(rad))
            y = int(20 + 11 * math.sin(rad))
            oled.pixel(x, y, 1)
        oled.fill_circle(20, 20, 6, 1)
    elif code in (2, 3, 4, 5, 6, 7, 8, 9):  # 多云/阴
        oled.fill_circle(16, 22, 6, 1)
        oled.fill_circle(26, 18, 8, 1)
        oled.fill_circle(32, 24, 5, 1)
    else:                      # 雨/雪等
        oled.fill_circle(20, 20, 8, 1)
        for dy in range(4):
            oled.vline(14 + dy * 5, 32, 6, 1)
            oled.vline(16 + dy * 5, 32, 4, 1)

# ========== 主程序 ==========
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

if connect_wifi():
    weather = get_weather()
    oled.fill(0)
    if weather:
        draw_weather_icon(weather['code'])
        oled.text(weather['city'], 44, 4)
        oled.text(weather['temp'] + 'C', 44, 18)
        oled.text(weather['text'], 44, 32)
    else:
        oled.text('Weather Error', 0, 20)
    oled.show()
else:
    oled.fill(0)
    oled.text('WiFi Failed', 0, 20)
    oled.show()

# 刷新间隔（避免频繁请求，建议 30 分钟以上）
sleep(60)  # 测试用，生产环境改为 1800
```

> 心知天气免费接口每日 200 次调用限制，建议配合 Deep Sleep 间歇唤醒。

---

## 项目B：传感器数据实时显示
## 配合 DS18B20 防水温度传感器

### 硬件接线

```
ESP32                          DS18B20（防水探头）
────────────                   ──────────────
GPIO23  ───────────────────▶   DQ (数据线)
3.3V   ───────────────────▶   VDD (红线)
GND    ───────────────────▶   GND (黑线)

# 另需 4.7kΩ 上拉电阻接在 DQ 与 3.3V 之间（务必加上！）
```

```
ESP32                          SSD1306 OLED
────────────                   ──────────────
GPIO21 (SDA) ──────────────▶   SDA
GPIO22 (SCL) ──────────────▶   SCL
3.3V        ──────────────▶   VCC
GND         ──────────────▶   GND
```

> DS18B20 和 OLED 使用不同的通信协议（DS18B20 是 1-Wire，OLED 是 I2C），可以共用 ESP32，无需额外转换。

### 代码实现

```python
# main.py - DS18B20 温度传感器 + OLED 显示
import machine
import onewire
import ds18x20
import time
from machine import Pin, I2C
import ssd1306

# ---------- DS18B20 初始化 ----------
ds_pin = Pin(23)                        # GPIO23 连接 DS18B20 DQ
ow = onewire.OneWire(ds_pin)            # 创建 1-Wire 总线
ds = ds18x20.DS18X20(ow)

# 扫描总线上的设备
devices = ow.scan()
if not devices:
    raise Exception('未找到 DS18B20 传感器！')
print('找到传感器，地址:', [hex(d) for d in devices])
sensor = devices[0]

# ---------- OLED 初始化 ----------
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ---------- 居中显示函数 ----------
def display_center(temp):
    oled.fill(0)
    # 温度值
    temp_str = '{:.1f}'.format(temp)
    oled.text(temp_str, 20, 15)
    # 单位符号 "°C"
    oled.text('C', 85, 15)
    # 标签
    oled.text('DS18B20', 30, 35)
    oled.text('Temperature', 16, 47)
    oled.show()

# ---------- 主循环 ----------
while True:
    ds.convert_temp()                  # 发起温度转换命令
    time.sleep_ms(750)                # DS18B20 转换需要 750ms
    temp = ds.read_temp(sensor)       # 读取温度（单位：摄氏度）
    print('温度: {:.2f} C'.format(temp))
    display_center(temp)
    time.sleep(3)                      # 每 3 秒刷新一次
```

### 电路接线图（含 DS18B20）

```
        ┌─────────────────┐
        │   ESP32 FireBeetle │
        │                      │
        │  GPIO21 ◀──── SDA   │──┐
        │  GPIO22 ◀──── SCL   │──┤
        │  3.3V    ───── VCC  │──┤
        │  GND     ───── GND  │──┘
        │                      │
        │  GPIO23 ────┬── DQ ──┼── DS18B20 (黄线)
        │             │        │
        │         4.7kΩ        │
        │             │        │
        │  3.3V ──────┴────────┘
        └─────────────────┘
```

---

## 项目C：系统状态面板
## 实时显示 ESP32 内存 / WiFi 强度 / 运行时间

### 代码实现

```python
# main.py - 系统状态面板
import machine
import network
import time
import ssd1306
from machine import Pin, I2C

# ---------- OLED 初始化 ----------
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ---------- WiFi 初始化 ----------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect('Your_SSID', 'Your_Password')
    while not wlan.isconnected():
        time.sleep(0.5)

# ---------- 辅助绘图函数 ----------
def draw_bar(x, y, w, h, fill_ratio, max_ratio=1.0):
    """绘制进度条"""
    filled = int((fill_ratio / max_ratio) * w)
    oled.fill_rect(x, y, w, h, 0)
    oled.fill_rect(x, y, filled, h, 1)
    oled.rect(x, y, w, h, 1)

def draw_signal_bars(x, y, rssi):
    """绘制 WiFi 信号强度条（4格）"""
    bars = 0
    if rssi > -70: bars = 1
    if rssi > -55: bars = 2
    if rssi > -40: bars = 3
    if rssi > -30: bars = 4
    bar_h = [8, 14, 20, 26]
    for i in range(4):
        col = 1 if i < bars else 0
        oled.fill_rect(x + i * 5, y + (26 - bar_h[i]), 3, bar_h[i], col)

# ---------- 主循环 ----------
start_time = time.time()

while True:
    oled.fill(0)

    # --- WiFi 状态 ---
    if wlan.isconnected():
        rssi = wlan.status('rssi')
        ssid = wlan.config('ssid')
        oled.text('WiFi: OK', 0, 0)
        draw_signal_bars(60, 0, rssi)
        oled.text('RSSI: {}dBm'.format(rssi), 0, 10)
    else:
        oled.text('WiFi: OFF', 0, 0)

    # --- 内存状态 ---
    import gc
    free_mem = gc.mem_free()
    total_mem = gc.mem_alloc() + free_mem
    mem_pct = free_mem / total_mem
    oled.text('MEM:', 0, 22)
    draw_bar(36, 22, 60, 7, free_mem, total_mem)
    oled.text('{}B / {}B'.format(free_mem, total_mem), 0, 32)

    # --- 运行时间 ---
    elapsed = int(time.time() - start_time)
    mins, secs = divmod(elapsed, 60)
    hrs, mins = divmod(mins, 60)
    oled.text('UP: {:02d}:{:02d}:{:02d}'.format(hrs, mins, secs), 0, 44)

    # --- IP 地址 ---
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        oled.text(ip, 0, 56)

    oled.show()
    time.sleep(1)
```

---

## 5. 低功耗优化：Deep Sleep

### 5.1 原理

ESP32 Deep Sleep 模式下，CPU 停止运行，仅 RTC 时钟（负责定时唤醒）和 RTC 内存保留数据。电流可从 ~240mA 降至 **~10-150μA**。

```
普通运行：~240mA
Modem Sleep：~150mA
Light Sleep：~10mA
Deep Sleep：~10-150μA（取决于板载电路）
```

### 5.2 天气站 + Deep Sleep 完整代码

```python
# main.py - 带 Deep Sleep 的天气站
import machine
import network
import urequests
import ssd1306
from machine import Pin, I2C, deep_sleep
from time import sleep

# ========== 配置 ==========
WIFI_SSID = 'Your_WiFi_Name'
WIFI_PASSWORD = 'Your_WiFi_Password'
API_KEY = 'Your_API_Key'
CITY = 'beijing'
SLEEP_SECONDS = 600  # 10 分钟唤醒一次

# ========== WiFi ==========
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                break
            sleep(0.5)
    return wlan.isconnected()

# ========== 获取天气 ==========
def fetch_weather():
    url = (
        f'https://api.seniverse.com/v3/weather/now.json'
        f'?key={API_KEY}&location={CITY}&language=zh-Hans&unit=c'
    )
    try:
        r = urequests.get(url, timeout=10)
        data = r.json()
        r.close()
        now = data['results'][0]['now']
        return now['text'], now['temperature']
    except:
        return 'Error', '--'

# ========== 显示 ==========
def display_weather(text, temp):
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.text(text, 0, 15)
    oled.text(temp + 'C', 0, 35)
    oled.show()
    sleep(5)       # 显示 5 秒后进入休眠

# ========== 主程序 ==========
if connect_wifi():
    text, temp = fetch_weather()
    display_weather(text, temp)
else:
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.text('WiFi Error', 0, 25)
    oled.show()
    sleep(5)

# 关闭 WiFi 降低功耗
wlan = network.WLAN(network.STA_IF)
wlan.active(False)

# 进入 Deep Sleep（RTC_TIMER 引脚 GPIO0 可接按钮手动唤醒）
print('进入 Deep Sleep {} 秒...'.format(SLEEP_SECONDS))
machine.deepsleep(SLEEP_SECONDS * 1000)  # 毫秒
```

### 5.3 唤醒方式

| 唤醒方式 | 说明 |
|----------|------|
| `machine.deepsleep(ms)` | 定时唤醒（最常用） |
| `machine.deepsleep()` 无参数 | 无限睡眠，等待外部中断 |
| GPIO 外部中断 | 接按钮到 GPIO0/GPIO2，配合 `ext0 Wake` |

---

## 6. 常见问题

### Q1: I2C 地址冲突

**症状**：`I2C scan()` 返回空列表，或 `OSError: [Errno 5] EIO`

**排查步骤：**

```python
# 1. 先扫描确认设备是否被发现
from machine import Pin, I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
print(i2c.scan())   # 正常应返回 [60]，60 = 0x3C
```

**常见原因 & 解决方案：**

| 原因 | 解决 |
|------|------|
| SDA/SCL 接线接反 | 交换 SDA/SCL 杜邦线位置 |
| 接线松动/面包板接触不良 | 重新插紧所有杜邦线 |
| OLED 供电不足（ESP32 3.3V 供电能力有限） | 单独给 OLED 供电（VCC 接 USB 5V，逻辑仍接 3.3V） |
| I2C 地址不是默认 0x3C | 检查模块上 A0/A1/A2 焊点，跳线修改地址 |
| 两个 I2C 设备地址相同 | 使用 GPIO 模拟 I2C（SoftI2C）分配不同引脚，或加 I2C MUX |

> **注意**：ESP32 的 GPIO 21/22 硬件 I2C 在某些开发板上与其他功能复用，需要确认引脚未被占用。

### Q2: 显示闪屏（Flickering）

**症状**：OLED 显示内容不断闪烁或周期性黑屏

**原因 & 解决：**

| 原因 | 解决 |
|------|------|
| `show()` 调用过于频繁 | 在主循环末尾一次性 `oled.show()`，不要每次操作都调用 |
| 刷新频率太高 | 适当加 `time.sleep()` 延迟 |
| I2C 频率过高 | 降低频率：`i2c = I2C(0, ..., freq=100000)` |
| 供电不稳（尤其是USB供电不足时） | 使用独立稳压电源，或接 USB 电源适配器供电 |
| 固件 BUG | 升级到最新 MicroPython 固件 |

**推荐刷新模式：**
```python
while True:
    oled.fill(0)          # 清屏
    # ... 绘图操作 ...
    oled.show()           # 只在最后调用一次 show()
    time.sleep(1)          # 每秒刷新一次足矣
```

### Q3: DS18B20 传感器读不到数据

**排查：**
```python
# 检查 1-Wire 总线
import machine, onewire
ow = onewire.OneWire(machine.Pin(23))
print(ow.scan())  # 应返回字节列表，如 [bytearray(b'...')]
```

**常见原因：**
- 4.7kΩ 上拉电阻**必须加上**，这是 DS18B20 通信协议要求
- 探头线太长（超过 5 米信号衰减严重）
- 转换等待时间不足（750ms 是 DS18B20 标准转换时间）

### Q4: WiFi 连接失败 / urequests 超时

```python
# 检查 WiFi 信号强度
import network
wlan = network.WLAN(network.STA_IF)
print(wlan.status('rssi'))  # 信号强度，-30 到 -90，>-70 较稳定
```

**建议：**
- 将 ESP32 靠近路由器测试
- WiFi 密码包含特殊字符需 URL encode
- 生产环境使用断线重连逻辑（`while not wlan.isconnected()` 循环）

### Q5: MicroPython 固件烧录后串口无法识别

```bash
# Linux 添加 udev 规则
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="10c4", MODE="0666"' | sudo tee /etc/udev/rules.d/99-espressif.rules
sudo udevadm control --reload-rules
```

---

## 附录：完整接线速查表

| ESP32 引脚 | 功能 | SSD1306 OLED | DS18B20 |
|-----------|------|-------------|---------|
| GPIO21 | SDA (I2C) | SDA | - |
| GPIO22 | SCL (I2C) | SCL | - |
| GPIO23 | - | - | DQ (数据线) |
| 3.3V | 电源 | VCC | VDD |
| GND | 地线 | GND | GND |
| GPIO0 | Deep Sleep 唤醒（可选） | - | - |

---

*文档版本：v1.0 | 整理：Jarvis AI 助手 | 如有疏漏欢迎指正*
