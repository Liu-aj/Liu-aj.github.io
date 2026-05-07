---
title: esp32-ds18b20-home-assistant-guide
tags:
  - ESP32
  - DS18B20
  - Home Assistant
  - 传感器
---

tags:
  - ESP32
  - 嵌入式
  - IoT
# ESP32 + DS18B20 + Home Assistant 完整实战手册

> 参考来源：esp32.co.uk · ESPHome 官方文档  
> 适用版本：ESPHome 2024.x + Home Assistant 2024.x

---
description: ESP32开发指南

## 目录

*目录已移除，使用侧边栏自动生成*

---
description: ESP32开发指南

## 1. 硬件准备

### 1.1 ESP32 开发板推荐

| 型号 | 特点 | 推荐场景 |
|------|------|----------|
| **ESP32 DevKit v1** | 双核 240MHz，WiFi + BLE，GPIO 丰富 | 通用场景，入门首选 |
| **ESP32-C3 DevKit** | RISC-V 单核 160MHz，极低功耗，WiFi 4 | 电池供电、极简项目 |
| **ESP32-S3 DevKit** | 双核 240MHz，AI 加速，更多 GPIO | 多传感器、大项目 |

> 💡 DS18B20 对 GPIO 无特殊要求，任意 GPIO 均可。GPIO4（默认）最常用。

### 1.2 DS18B20 选购要点

**推荐购买防水探头版本**（带不锈钢封装），特别适合液体和户外场景：

| 参数 | 规格 |
|------|------|
| 测温范围 | -55°C ~ +125°C |
| 精度 | ±0.5°C（-10°C ~ +85°C）|
| 分辨率 | 9~12bit 可调（默认 12bit = 0.0625°C）|
| 工作电压 | 3.0V ~ 5.5V（建议 3.3V 或 5V）|
| 线缆长度 | 常见 1m / 2m / 3m，可延长至 100m+ |
| 接口类型 | 三线：GND / DATA / VCC |

> ⚠️ 市面上存在假冒 DS18B20，特征为读数跳动异常、地址异常（全 0 或全 F）。建议购买带包装的品牌件。

**接线颜色（常见约定）：**
```bash
红线   → VCC（电源 3.3V 或 5V）
黑/黄线 → GND
蓝/白线 → DATA（数据线）
```

### 1.3 4.7kΩ 上拉电阻原理

```bash
         ┌──┐
ESP32   │  │      DS18B20
GPIO4 ──┤  ├──────── DQ（数据线）
  │    └──┘          │
3.3V ────────────────┴── VDD
GND  ─────────────────── GND
```bash

**为什么需要？**

1-Wire 总线空闲时需要被上拉至高电平。DS18B20 的 DATA 线是开漏结构，自己只能拉低，无法主动拉高。电阻的三大作用：

1. **空闲时保持高电平** — 防止总线悬空产生噪声
2. **通信时限制电流** — 保护 GPIO 端口
3. **电平匹配** — ESP32（3.3V）与 DS18B20 电压协调

> 📌 **不要省略此电阻！** 缺少会导致读数完全乱码或无法通信。  
> 长线（>10m）可将电阻降至 **2.2kΩ~3.3kΩ**，短线（<1m）可用 **5.1kΩ~10kΩ**。

---
description: ESP32开发指南

## 2. 接线图

### 2.1 单传感器接线（推荐 GPIO4）

```bash
  ┌─────────────┐           ┌──────────────────┐
  │   ESP32    │           │    DS18B20       │
  │  DevKit v1  │           │  防水探头         │
  │             │           │                  │
  │  3.3V ──────┼───────────┼── 红线 (VCC)     │
  │             │    4.7kΩ  │                  │
  │  GPIO4 ─────┼──┤├──┼───┼── 蓝线 (DATA)   │
  │             │    4.7kΩ  │                  │
  │  GND  ──────┼───────────┼── 黑/黄线 (GND) │
  └─────────────┘           └──────────────────┘

注意：4.7kΩ 电阻并联在 DATA 与 VCC 之间
```

### 2.2 多传感器串联接线（同一 GPIO，总线式）

```bash
ESP32 GPIO4
   │
   ├──[4.7kΩ]───┬──────────────────────────────────┐
   │            │              │                  │
  DS18B20 #1   DS18B20 #2    DS18B20 #3    ...    DS18B20 #N
  (蓝线DATA)   (蓝线DATA)    (蓝线DATA)         (蓝线DATA)
   │            │              │                  │
  所有红线(VCC)并联到 3.3V
  所有黑/黄线(GND)并联到 GND
```bash

**关键规则：**
- 所有传感器的 DATA 线并联到同一 GPIO
- **仅需一个 4.7kΩ 电阻**（总线上任意位置，靠近 ESP32 端最佳）
- 每增加一个传感器，电阻不要重复添加

### 2.3 不同 GPIO 接多个传感器（每路独立上拉）

```yaml
dallas:
  - pin: GPIO4
    # 传感器组A
  - pin: GPIO15
    # 传感器组B
```bash

> 💡 每路 GPIO 都需要独立的一个 4.7kΩ 电阻。

---
description: ESP32开发指南

## 3. ESPHome 配置

### 3.1 获取传感器 ROM 地址（首次配置前）

首次刷写时**不指定地址**，日志会输出每个传感器的 64-bit ROM 地址：

```yaml
esphome:
  name: esp32-ds18b20
  platform: ESP32
  board: esp32dev

wifi:
  ssid: "YOUR_WIFI_SSID"
  password: "YOUR_WIFI_PASSWORD"

logger:
  level: DEBUG   # 关键：查看串口日志中的传感器地址

api:
ota:
```bash

日志中会看到类似输出：
```bash
[dallas.sensor]   Found sensors:
[dallas.sensor]     0x3c0000031aa7c828
[dallas.sensor]     0x3c0000031bc7b028
[dallas.sensor]     0x3c0000031cc8d128
```bash

> 📌 地址只需获取一次，写入配置文件后即可断网独立运行。

### 3.2 基础单传感器配置

```yaml
esphome:
  name: esp32-ds18b20-single
  platform: ESP32
  board: esp32dev

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

api:
ota:
  platform: esphome

logger:

dallas:           # OneWire 总线配置
  - pin: GPIO4    # 指定 GPIO4，可改为任意 GPIO

sensor:
  - platform: dallas_temp
    address: 0x3c0000031aa7c828   # 替换为实际地址
    name: "热水器温度"             # HA 中显示名称
    unit_of_measurement: "°C"
    accuracy_decimals: 1         # 显示一位小数
    update_interval: 10s          # 读取间隔，默认 60s
```

### 3.3 多传感器配置（推荐方式）

```yaml
esphome:
  name: esp32-ds18b20-multi
  platform: ESP32
  board: esp32dev

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

api:
ota:

logger:

dallas:
  - pin: GPIO4

sensor:
  # 传感器1：热水器进水
  - platform: dallas_temp
    address: 0x3c0000031aa7c828
    name: "热水器进水温度"
    id: sensor_1
    unit_of_measurement: "°C"
    accuracy_decimals: 1

  # 传感器2：热水器出水
  - platform: dallas_temp
    address: 0x3c0000031bc7b028
    name: "热水器出水温度"
    id: sensor_2
    unit_of_measurement: "°C"
    accuracy_decimals: 1

  # 传感器3：回水温度
  - platform: dallas_temp
    address: 0x3c0000031cc8d128
    name: "地暖回水温度"
    id: sensor_3
    unit_of_measurement: "°C"
    accuracy_decimals: 1
```

### 3.4 多传感器按索引读取（无需地址，适用于不怕传感器顺序变化）

```yaml
sensor:
  - platform: dallas_temp
    index: 0
    name: "传感器 1"

  - platform: dallas_temp
    index: 1
    name: "传感器 2"
```bash

> ⚠️ 索引方式简单但风险：如果传感器顺序变化，名称对应会错位。**正式项目建议使用 address 指定**。

### 3.5 完整示例（含 MQTT 备用）

```yaml
esphome:
  name: esp32-ds18b20-full
  platform: ESP32
  board: esp32dev

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

api:
ota:
  platform: esphome

logger:
  level: DEBUG

mqtt:
  # MQTT 可选启用，与 api 二选一或共存
  broker: !secret mqtt_broker
  username: !secret mqtt_user
  password: !secret mqtt_password
  topic_prefix: home/boiler/ds18b20
  on_message:
    - topic: home/boiler/ds18b20/set
      then:
        - sensor.template.publish:
            id: temp_sensor
            state: !lambda 'return x;'

dallas:
  - pin: GPIO4

sensor:
  - platform: dallas_temp
    address: 0x3c0000031aa7c828
    name: "热水器温度"
    unit_of_measurement: "°C"
    accuracy_decimals: 1
    update_interval: 5s
    filters:
      - sliding_window_moving_average:
          window_size: 5
          send_every: 1

  - platform: dallas_temp
    address: 0x3c0000031bc7b028
    name: "回水温度"
    unit_of_measurement: "°C"
    accuracy_decimals: 1
    update_interval: 5s
    filters:
      - sliding_window_moving_average:
          window_size: 5
          send_every: 1

# 传感器模板（供 MQTT 自动化使用）
sensor:
  - platform: template
    id: temp_sensor
    name: "MQTT 模板温度"
    unit_of_measurement: "°C"
```bash

---
description: ESP32开发指南

## 4. MQTT 集成 vs ESPHome 原生集成

### 4.1 对比一览

| 特性 | ESPHome 原生 API | MQTT |
|------|-----------------|------|
| **配置复杂度** | ✅ 极简，零配置自动发现 | ❌ 需要 broker、topic、payload 配置 |
| **自动发现** | ✅ Home Assistant 自动识别实体 | ❌ 需要手动配置 MQTT sensor |
| **双向通信** | ✅ ESP→HA + HA→ESP 双向均支持 | ⚠️ 仅单向推送，可订阅主题 |
| **固件更新** | ✅ OTA 无缝，支持 API 调用 HA 操作 | ❌ OTA 需单独配置 |
| **稳定性** | ✅ ESPHome 团队直接维护协议 | ✅ MQTT broker 稳定性决定 |
| **外接兼容性** | ❌ 只能与 Home Assistant 通信 | ✅ 可同时接入其他系统（Node-RED等）|
| **网络依赖** | 需要 Home Assistant 在线 | 离线缓冲（QOS 1/2）|
| **适用场景** | 家庭私有部署，HA 作为唯一控制器 | 多平台集成、公有云、工业采集 |

### 4.2 推荐方案

```bash
日常家庭使用 → 选择 ESPHome 原生 API ✅
需要接 Node-RED / 第三方平台 → MQTT
双保险方案 → API + MQTT 同时启用（配置更复杂）
```

### 4.3 MQTT 集成示例（ESPHome 发布端）

**ESPHome YAML（发布）：**
```yaml
mqtt:
  broker: 192.168.1.100
  port: 1883
  username: mqtt_user
  password: mqtt_pass
  topic_prefix: home/boiler

sensor:
  - platform: dallas_temp
    address: 0x3c0000031aa7c828
    name: "Boiler Temperature"
   MQTT:
      state_topic: "home/boiler/temperature"
      value_template: "{{ value }}"
      unit_of_measurement: "°C"
```bash

**Home Assistant MQTT Sensor 配置：**
```yaml
mqtt:
  sensor:
    - name: "热水器温度 (MQTT)"
      state_topic: "home/boiler/temperature"
      unit_of_measurement: "°C"
      device_class: temperature
      value_template: "{{ value }}"
```bash

---
description: ESP32开发指南

## 5. Home Assistant 配置

### 5.1 ESPHome 原生 API 自动发现

**无需任何配置！** 刷写后，Home Assistant 自动发现设备：

1. 安装 ESPHome 插件（在 Home Assistant → 设置 → 插件）
2. 添加 ESPHome 设备（设置 → 设备与服务 → 添加集成 → ESPHome）
3. 输入 ESP32 的 IP 地址或主机名
4. 输入 API 密码（如设置了）
5. ✅ 自动发现所有传感器实体

### 5.2 MQTT 手动配置

```yaml
# configuration.yaml
mqtt:
  sensor:
    - name: "热水器温度"
      state_topic: "home/boiler/ds18b20"
      unit_of_measurement: "°C"
      device_class: temperature

    - name: "地暖回水温度"
      state_topic: "home/boiler/ds18b20_return"
      unit_of_measurement: "°C"
      device_class: temperature
```

### 5.3 温度监控 UI 卡片配置

**方式一：实体卡片（快速）**

在仪表板添加「单体实体」卡片，绑定对应的温度传感器实体。

**方式二：Markdown 卡片（精美）**

```yaml
type: markdown
content: |
  # 🌡️ 温度监控

  | 位置 | 当前温度 | 状态 |
  |:-----|:-------:|:----:|
  | 热水器 | {{ states('sensor.boiler_temperature') }}°C | 🔴 正常 |
  | 回水温度 | {{ states('sensor.return_temperature') }}°C | 🟡 偏低 |
  | 室内 | {{ states('sensor.indoor_temperature') }}°C | 🟢 舒适 |
```bash

**方式三：Gauge 卡片（可视化）**

```yaml
type: gauge
entity: sensor.boiler_temperature
min: 0
max: 100
unit: °C
name: 热水器温度
severity:
  green: 40
  yellow: 70
  red: 85
```bash

**方式四：迷你图卡（历史趋势）**

```yaml
type: custom:mini-graph-card
entities:
  - entity: sensor.boiler_temperature
    name: 热水器
  - entity: sensor.return_temperature
    name: 回水
hours_to_show: 24
points_per_hour: 6
line_size: 2
```bash

> 💡 推荐安装 **HACS** 后在社区商店安装 `mini-graph-card` 插件。

---
description: ESP32开发指南

## 6. 实用场景

### 6.1 热水器监测

**目标：** 监测热水器内部水温，防止烫伤或冻裂

**配置要点：**
- 温度范围设定：建议 0°C~95°C
- 更新间隔：5s~10s（热水器周边环境温度变化快）
- 阈值告警：>80°C 推送通知

```yaml
# ESPHome 告警 filter
sensor:
  - platform: dallas_temp
    address: 0x3c0000031aa7c828
    name: "热水器温度"
    unit_of_measurement: "°C"
    filters:
      - multiply: 1.0
    on_value_range:
      above: 80
      then:
        - mqtt.publish:
            topic: home/boiler/alert
            payload: "热水器温度超80°C！"
```

### 6.2 地暖回水温度

**目标：** 判断地暖是否正常运行，回水温度过低说明管道堵塞或热源不足

**参考值：**
| 回水温度 | 含义 |
|---------|------|
| 35°C~45°C | 正常 |
| <30°C | 可能管道堵塞或热源不足 |
| >50°C | 流量过大，热量未充分交换 |

**配置要点：**
- 安装位置：地暖分集水器回水口
- 可配合温差计算（进水-回水）判断流量
- 更新间隔：30s~60s（温度变化缓慢）

### 6.3 水族箱 / 鱼缸

**目标：** 监测水温，防止水温骤变导致鱼虾死亡

**参考值：**
| 鱼种 | 适宜温度 |
|------|---------|
| 热带鱼 | 24°C~28°C |
| 冷水鱼（金鱼等）| 18°C~22°C |
| 海水缸 | 25°C~27°C |

**配置要点：**
- 选用水密防水探头（DS18B20 防水版天然适合）
- 告警阈值：±2°C 偏离适宜区间
- 建议使用 ESP32-C3（低功耗，可电池供电做备用监测）

### 6.4 冷链监测

**目标：** 监测冰箱、冷库、药品冷藏柜温度

**参考值：**
| 场景 | 正常范围 |
|------|---------|
| 普通冰箱 | 2°C~8°C |
| 冷冻柜 | -25°C~-18°C |
| 药品冷藏 | 2°C~6°C |

**配置要点：**
- DS18B20 测温范围 -55°C~125°C，完美覆盖
- 长线延长可达 100m（使用 Cat5/Cat6 网线）
- 长线建议：降低上拉电阻至 2.2kΩ，5V 供电
- 告警：温度超范围立即推送（配合 Home Assistant 自动化）

---
description: ESP32开发指南

## 7. 常见问题排查

### Q1: 读数不稳定，跳动剧烈（±5°C 以上）

**排查步骤：**

1. **检查上拉电阻**
   - 是否连接？阻值是否为 4.7kΩ？
   - 长线（>5m）尝试换用 2.2kΩ~3.3kΩ

2. **检查供电**
   - ESP32 的 3.3V 输出能力有限，多传感器同时转换时可能电压跌落
   - 改用 5V 供电 DS18B20，ESP32 仍通过 GPIO 读取（1-Wire 信号兼容 3.3V）

3. **检查线缆质量**
   - 避免使用超长劣质线
   - 建议使用带屏蔽层的双绞线或网线

4. **添加软件滤波**
   ```yaml
   sensor:
     - platform: dallas_temp
       # ...
       filters:
         - sliding_window_moving_average:
             window_size: 10
             send_every: 1
```bash

5. **检查传感器真假**
   - 假冒传感器地址通常为 `0x0000000000000000` 或 `0xFFFFFFFFFFFFFFFF`
   - 读取误差在 2°C 以外的传感器极可能为假货

### Q2: 只能读到部分传感器（超过 8 个时）

- ESP32 1-Wire 总线驱动默认缓冲区有限
- 尝试在 `dallas` 配置中增加 `timeout` 参数
- 将传感器分组到不同 GPIO（每个 GPIO 独立总线）

```yaml
dallas:
  - pin: GPIO4
  - pin: GPIO15
```

### Q3: 部分传感器完全读不到数据

1. **逐一排查**：临时只接一个传感器，确认每个硬件正常工作
2. **检查接线**：确认 DATA 线没有与 GND 短路
3. **确认地址正确**：日志中的地址不要有误
4. **尝试不同 GPIO**：GPIO4 损坏时换用 GPIO21 等

### Q4: ESPHome 日志显示 "Too many devices on bus"

- 表示总线有冲突，可能是两根 DATA 线意外短接
- 检查杜邦线连接是否松动
- 检查是否有多个电阻并联（只需要一个）

### Q5: 设备离线（Home Assistant 中 ESPHome 实体消失）

1. 检查 ESP32 供电（USB 断电或电源不足）
2. 检查 WiFi 信号强度（尝试靠近路由器测试）
3. 检查固件 OTA 更新是否失败
4. 重启 ESP32（手动断电再上电）

### Q6: 传感器地址丢失（每次重启地址变化）

- 正常情况下 DS18B20 的 64-bit ROM 地址是**固定的**
- 若地址变化，检查是否同时读到了其他 1-Wire 设备（如 DS18B20 以外）
- 某些克隆芯片地址不稳定，需更换正品

### Q7: 长距离布线（>20m）读数异常

**解决方案：**
| 方法 | 实施难度 | 效果 |
|------|---------|------|
| 降低上拉电阻至 2.2kΩ | ⭐ 简单 | 中等改善 |
| 使用 5V 供电 | ⭐ 简单 | 明显改善 |
| 使用带供电的 RS485 1-Wire 中继器 | ⭐⭐⭐ 专业 | 最佳效果 |
| 使用双绞屏蔽线（Cat5e）| ⭐⭐ 中等 | 明显改善 |
| 缩短总线长度 | ⭐ 简单 | 彻底解决 |

---
description: ESP32开发指南

## 快速参考卡

```bash
硬件接线（单传感器）：
  ESP32 3.3V  ──── 红线(VCC)
  ESP32 GPIO4 ──[4.7kΩ]── 蓝线(DATA) ─── DS18B20 DQ
  ESP32 GND   ──── 黑线(GND)

多传感器：所有 DATA 线并联到 GPIO4，只用 1 个电阻

ESPHome 最小配置：
  dallas:
    - pin: GPIO4
  sensor:
    - platform: dallas_temp
      address: <实测地址>

自动发现：
  ESPHome 原生 API = 刷写即用，零配置
  MQTT = 需要 broker + 手动配置 sensor

长线方案：
  5V 供电 + 2.2kΩ 上拉 + Cat5 网线 → 可达 100m
```bash

---
description: ESP32开发指南

*整理自 esp32.co.uk · ESPHome 官方文档 · 社区实战经验*
*最后更新：2026-04*
