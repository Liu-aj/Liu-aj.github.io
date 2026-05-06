# ESP32 + SSD1306 OLED 显示项目开发指南（2026）

> 更新日期：2026-05-06

---

## 一、硬件选型

### 1.1 ESP32 开发板对比

| 开发板 | 芯片 | Flash | BLE | OLED | 参考价 |
|--------|------|-------|-----|------|--------|
| ESP32 DevKitC | ESP32 | 4MB | 4.2 | — | ¥40-60 |
| ESP32-S3 Mini | ESP32-S3 | 8MB | 5.0 | — | ¥50-70 |
| **ESP32-C3 Super Mini（带屏）** | ESP32-C3 | 4MB | 5.0 | 0.42寸 72x40 | ¥25-35 |
| LilyGO T-Display | ESP32-S3 | 16MB | 5.0 | 1.14寸 135x240 | ¥60-80 |

**推荐入门**：ESP32-C3 Super Mini（带 0.42 寸 OLED）

### 1.2 SSD1306 OLED 规格

| 参数 | 值 |
|------|---|
| 尺寸 | 0.96 寸 |
| 分辨率 | 128×64 像素 |
| 接口 | I2C（默认地址 0x3C）或 SPI |
| 工作电压 | 3.3V |
| 库 | ssd1306（MicroPython）/ Adafruit SSD1306（Arduino） |

> ⚠️ ESP32-C3 Super Mini 内置 0.42 寸 OLED 实际上是 **SH1106** 驱动（非 SSD1306），实测 SH1106 库效果更好

---

## 二、MicroPython 开发环境搭建

### 2.1 Thonny 配置步骤

1. **下载 Thonny**：https://thonny.org/
2. **安装 MicroPython ESP32**：
   - Thonny → 运行 → 选择解释器 → 安装 MicroPython
   - 选择对应固件（ESP32-C3 选择 GENERIC_C3）
3. **烧录固件**：
   ```bash
   esptool.py --port /dev/ttyUSB0 erase_flash
   esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash 0 ESP32C3-2026-xxxx.bin
   ```
4. **配置解释器**：Thonny → 运行 → 选择解释器 → MicroPython（ESP32）

### 2.2 常用 MicroPython 库

```
# 方法1：通过 mip 安装（联网情况下）
import mip
mip.install("ssd1306")

# 方法2：手动上传 .py 库文件到开发板
```

---

## 三、ssd1306 库使用详解

### 3.1 基础文字显示

```python
from machine import Pin, I2C
import ssd1306

# I2C 初始化（ESP32 默认 GPIO21=SDA, GPIO22=SCL）
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# 显示文字
display.text("Hello World", 0, 0)
display.text("Temp: 25.5C", 0, 20)
display.show()
```

### 3.2 图形绘制

```python
# 画线
display.line(0, 0, 127, 63)  # 对角线

# 画矩形
display.rect(10, 10, 50, 30)  # 空心矩形
display.fill_rect(10, 10, 50, 30)  # 实心矩形

# 画圆
display.circle(64, 32, 20)

# 清除屏幕
display.fill(0)
display.show()
```

### 3.3 滚动效果

```python
# 水平滚动
display.text("Scrolling Text", 0, 0)
display.show()
# 手动实现滚动（将字符逐帧移动）
for x in range(128):
    display.fill(0)
    display.text("Scroll", -x, 0)
    display.show()
    utime.sleep(0.05)
```

---

## 四、实战项目

### 项目一：传感器数据展示（温湿度）

```python
from machine import Pin, I2C
import ssd1306, dht, utime

# DHT22 温湿度传感器（GPIO15）
sensor = dht.DHT22(Pin(15))

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    
    display.fill(0)
    display.text("Temperature", 0, 0)
    display.text(f"{temp:.1f} C", 0, 15)
    display.text("Humidity", 0, 30)
    display.text(f"{hum:.1f} %", 0, 45)
    display.show()
    
    utime.sleep(10)
```

### 项目二：Wi-Fi / MQTT 状态指示器

```python
import network, mqtt, ssd1306
from machine import Pin, I2C

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

def display_status(ip=None, mqtt_ok=False):
    display.fill(0)
    if ip:
        display.text("WiFi: OK", 0, 0)
        display.text(ip, 0, 15)
    else:
        display.text("WiFi: 连接中...", 0, 0)
    
    display.text("MQTT: " + ("OK" if mqtt_ok else "NO"), 0, 35)
    display.show()
```

### 项目三：ESP32-C3 Super Mini 内置 0.42 寸 OLED

**注意**：内置 OLED 是 SH1106 驱动，不是 SSD1306！

```python
from machine import Pin, I2C
import sh1106

# ESP32-C3 Super Mini I2C 默认引脚
# SDA=GPIO8, SCL=GPIO9（或其他，看具体版本）
i2c = I2C(1, scl=Pin(9), sda=Pin(8))
display = sh1106.SH1106_I2C(72, 40, i2c)  # 0.42寸 72x40

display.text("Hello!", 10, 10)
display.show()
```

> 安装 sh1106 库：`mip.install("sh1106")`

---

## 五、I2C 地址冲突排查

### 常见 I2C 设备地址

| 设备 | 地址 | 备注 |
|------|------|------|
| SSD1306 OLED | 0x3C | 最常见 |
| SH1106 OLED | 0x3C | 兼容 SSD1306 地址 |
| BME280 | 0x76 或 0x77 | 传感器 |
| AHT20 | 0x38 | 温湿度 |
| ADS1115 | 0x48 | ADC |

### 扫描总线上的设备

```python
from machine import Pin, I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
devices = i2c.scan()
print(devices)  # 打印设备地址列表
```

### 多设备共存方案

```python
# 方案1：不同 I2C 总线
i2c0 = I2C(0, scl=Pin(22), sda=Pin(21))  # 总线0：OLED
i2c1 = I2C(1, scl=Pin(9), sda=Pin(8))   # 总线1：传感器

# 方案2：使用 I2C MUX（ TCA9548A ）切换通道
```

---

## 六、低功耗优化 — 深度睡眠模式

```python
from machine import deepsleep, Pin
import machine

# 关闭所有外设
display.poweroff()  # OLED 关闭

# 深度睡眠 10 秒后唤醒
machine.deepsleep(10000)  # 毫秒

# 或使用定时唤醒
# machine.wake_on_touch_wakeup()
# machine.wake_on_timer_wakeup(10000)
```

**进阶**：配合 RTC 内存实现唤醒后数据恢复

```python
import machine, gc

# 写入 RTC 内存
rtc = machine.RTC()
rtc.memory(b"state_data_here")

# 唤醒后读取
data = rtc.memory()
```

---

## 七、参考资源

- ssd1306 MicroPython 库：https://github.com/micropython-magic lantern/ssd1306
- sh1106 MicroPython 库：https://github.com/nickovchinnikov/micropython-sh1106
- ESP32-C3 Super Mini OLED GitHub：https://github.com/ESP32Home/oled_042
- randomnerdtutorials.com：ESP32 OLED 教程

---

*文档版本：v1.0*