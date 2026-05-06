# Home Assistant 蓝牙 Beacon 室内定位系统搭建指南（2026）

> 更新日期：2026-05-06

---

## 一、技术原理

### 1.1 BLE iBeacon 工作原理

iBeacon 是 BLE 广播包的标准化格式：

```bash
          ↓
   ESP32 蓝牙代理节点接收
          ↓
   根据 RSSI 估算距离
          ↓
   HA 判断"在这个房间"
```

| 字段 | 作用 |
|------|------|
| UUID | 标识信标用途/品牌（可自定义） |
| Major/Minor | 区域/位置编码 |
| RSSI | 信号强度（用于距离估算） |

### 1.2 RSSI 定位原理

```bash
  -50 dBm  → 很近（< 1米）
  -70 dBm  → 约 2-3 米
  -85 dBm  → 较远（约 5 米）
  -100 dBm → 信号弱边缘

注意：RSSI 受人体遮挡、金属反射影响大，精度有限（房间级OK，厘米级不行）
```

### 1.3 房间级定位 vs 物品追踪

| 模式 | 实现方式 | 精度 |
|------|---------|------|
| **房间级定位** | BLE Tag + 多节点 RSSI 对比 | 房间级别 |
| **物品追踪** | 单点 BLE Tag 信号阈值 | 大概区域 |

---

## 二、硬件方案

### 2.1 ESP32 蓝牙代理节点布置

**原则**：每个房间至少 1 个，信号重叠区域更好

```bash
┌─────────┬─────────┐
│  卧室   │  客厅    │
│  [ESP32]│  [ESP32]│
├─────────┼─────────┤
│  厨房   │  卫生间  │
│  [ESP32]│         │ ← 角落信号可能覆盖
└─────────┴─────────┘
```

**推荐配置**：
- 小户型（< 80㎡）：2-3 个 ESP32 节点
- 中户型（80-150㎡）：4-6 个节点
- 每个节点间距 5-8 米

**推荐开发板**：ESP32-C3 Mini / ESP32-S3 Mini（便宜、5V USB 供电）

### 2.2 BLE Tag / iBeacon 信标选择

| 类型 | 适用场景 | 购买建议 |
|------|---------|---------|
| **BLE 防丢器**（如 Tile、Chipolo） | 钥匙、钱包追踪 | 通用 |
| **Aqara M2 或其他 HA 设备** | 带 BLE 的传感器 | 复用已有设备 |
| **专用 iBeacon** | 固定位置标记 | 可自制（ESP32-C3） |

**物品追踪推荐**：Chipolo ONE（续航 1 年，信号稳定）

### 2.3 节点供电建议

- USB 供电 + 固定位置（最稳定）
- 避免放在金属配电箱内
- 距地面 1-1.5 米

---

## 三、HA 集成方案对比

### 方案 A：Bermuda 集成

**原理**：利用 HA 的 Bermuda 集成，通过多个 ESP32 BLE Proxy 节点收集 RSSI，计算设备位置

**配置步骤**：

1. **部署 ESP32 BLE Proxy**
   ```yaml
   # ESPHome 配置示例
   esp32_ble_tracker:
     scan_parameters:
       interval: 0x10F0
       window: 0x10F0
   
   bluetooth_proxy:
     active: true
```markdown

2. **安装 Bermuda 集成**
   - HACS → 搜索 `bermuda` → 安装
   - HA → 配置 → 集成 → 添加 Bermuda
   - Bermuda 会自动发现 ESP32 BLE Proxy 节点

3. **配置追踪规则**
   ```yaml
   # configuration.yaml
   bermuda:
     devices:
       - name: "我的钥匙"
         uuid: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
         min_rssi: -85
```

**优缺点**：
- ✅ 配置简单，HA 官方支持思路
- ❌ 定位精度一般，依赖 RSSI 稳定性

---

### 方案 B：ESPresense 集成

**原理**：ESPresense 通过 MQTT 接收各节点的 RSSI 数据，在 Node-RED 或 HA 中计算位置

**配置步骤**：

1. **刷 ESPresense 固件**
   - 使用 ESPHome 刷入 ESPresense：https://esphome.io/projects?query=espresense

2. **安装 ESPresense 集成**
   ```yaml
   # ESPHome YAML
   esphome:
     name: ble-presence
     friendly_name: BLE-Presence
   
   esp32_ble_tracker:
   
   bluetooth_proxy:
     active: true
   
   sensor:
     - platform: ble_presence
       mac_address: "XX:XX:XX:XX:XX:XX"
       name: "Key Tracker"
```

3. **MQTT 配置**
   ```yaml
   mqtt:
     broker: 192.168.1.x
     topic_prefix: espresense
```

**ESPresense 特点**：
- 支持多房间同时检测（通过 MQTT 主题区分）
- 配置灵活，适合进阶用户

### 两者对比

| 对比项 | Bermuda | ESPresense |
|--------|---------|------------|
| 配置难度 | 低 | 中 |
| 精度 | 一般 | 较好（多节点融合） |
| 依赖 | BLE Proxy 节点 | MQTT Broker |
| 适合场景 | 简单存在检测 | 精准房间定位 |
| MQTT 必需？ | 否 | 是 |

---

## 四、完整配置流程

### 第一步：部署 ESP32 BLE Proxy（ESPHome）

```yaml
# ble-proxy.yaml
esphome:
  name: ble-proxy-bedroom
  friendly_name: BLE Proxy 卧室

esp32:
  board: esp32dev

wifi:
  ssid: "你的WiFi"
  password: "你的密码"

api:
  password: "esphome密码"

logger:

esp32_ble_tracker:
  scan_parameters:
    interval: 0x30
    window: 0x30

bluetooth_proxy:
  active: true
```

1. ESPHome 安装 → 添加设备 → 粘贴 YAML → 部署
2. 重复此步骤，为每个房间部署一个节点
3. 记录各节点 IP 和名称（用于后续识别）

### 第二步：安装追踪集成

```bash
1. HACS → 安装 Bermuda 或 ESPresense
2. 配置 → 集成 → 添加
3. 添加要追踪的 BLE 设备 UUID
```

### 第三步：创建自动化

```yaml
# 示例：进入客厅自动开灯
automation:
  - alias: "进入客厅开灯"
    trigger:
      platform: state
      entity_id: binary_sensor.living_room_occupied
      to: "on"
    action:
      service: light.turn_on
      target:
        entity_id: light.living_room_main
```markdown

---

## 五、实战应用场景

### 场景 1：钥匙追踪

```yaml
automation:
  - alias: "钥匙忘在家里提醒"
    trigger:
      - platform: time
        at: "08:30:00"
    condition:
      - condition: state
        entity_id: device_tracker.key_tracker
        state: "not_home"
    action:
      - service: notify.persistent_notification
        data:
          message: "钥匙不在家！"
```

### 场景 2：人体感应触发（进房间自动开灯）

```yaml
automation:
  - alias: "进卧室自动开灯"
    trigger:
      platform: state
      entity_id: binary_sensor.bedroom_presence
      to: "on"
    condition:
      - condition: time
        after: "sunset"
    action:
      - service: light.turn_on
        data:
          entity_id: light.bedroom
          brightness_pct: 60
```markdown

### 场景 3：宠物定位

配合宠物佩戴的 BLE Tag，设置"宠物进入某区域"触发通知

---

## 六、精度优化技巧

| 技巧 | 说明 |
|------|------|
| **多节点冗余** | 一个房间放 2 个节点，取 RSSI 最强者 |
| **信号阈值调试** | 实际测试不同位置的 RSSI 值，设定合理阈值 |
| **防误判延迟** | 设置 10-30 秒延迟确认存在，避免短暂信号波动 |
| **睡眠区域排除** | 夜间关闭部分自动化，避免频繁触发 |
| **信号滤波** | 使用指数移动平均平滑 RSSI 数据 |

---

## 七、参考资源

- ESP32 BLE Proxy 部署：https://esphome.io/guides/bluetooth_proxy.html
- Bermuda 集成：https://github.com/bdraco/bermuda
- ESPresense：https://esphome.io/projects?query=espresense
- Home Assistant BLE 追踪：https://www.home-assistant.io/integrations/bluetooth_le_tracker/

---

*文档版本：v1.0*