tags:
  - ESP32
  - 嵌入式
  - IoT
# ESP32 电机控制完全指南

> 舵机 / 步进电机 / 直流电机 (L298N) · MicroPython 实操手册

---
description: ESP32开发指南

---
description: ESP32开发指南

## 1. 电机类型与选型

### 1.1 舵机（Servo）

#### 角度舵机（SG90MG / MG996R 等）

- **控制方式**：PWM 脉宽调制，周期 **20ms（50Hz）**
- **脉宽与角度对应**（常见映射）：

| 角度 | SG90 脉宽 | MG996R 脉宽 |
|------|-----------|-------------|
| 0°   | ~1ms (5%) | ~1ms (5%)   |
| 90°  | ~1.5ms (7.5%) | ~1.5ms (7.5%) |
| 180° | ~2ms (10%)  | ~2ms (10%)   |

- **接线**：棕线=GND，红线=5V，橙线=PWM信号
- **适用场景**：机器人关节、模型转向、开关阀门

#### 连续旋转舵机（CSR / 360° Servo）

- 接收 PWM 控制**速度和方向**（而非位置）
- 脉宽 1.3ms ≈ 全速正转，1.5ms = 停止，1.7ms ≈ 全速反转
- 适用于输送带、轮式机器人

#### 选型建议

| 参数 | SG90 | MG996R | 备注 |
|------|------|--------|------|
| 扭矩 | 1.8 kg·cm | 10 kg·cm | |
| 电压 | 4.8-6V | 4.8-7.2V | |
| 重量 | 9g | 55g | |
| 价格 | ★☆☆ | ★★☆ | |

---
description: ESP32开发指南

### 1.2 直流电机（DC Motor）

#### 有刷直流电机（Brushed DC）

- 结构简单，成本低
- 通过改变电压或 PWM 占空比调速
- 通过 H 桥改变电流方向来控制转向
- **缺点**：电刷磨损，有火花，寿命有限

#### 无刷直流电机（BLDC）

- 效率高、寿命长、无火花
- 需要电子调速器（ESC）配合
- FOC 控制可实现极平滑运行
- **适用**：无人机、高速风机

#### 减速电机（Geared DC）

- 常见型号：N20、JGA25-370、NEMA 17 改装
- 减速箱提供更高扭矩、更低转速
- 适合智能窗帘、传送带等应用

#### 选型建议

| 类型 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 有刷 DC | 便宜、简单 | 磨损、噪音 | 教育、简单项目 |
| 无刷 DC | 高效、安静 | 需要 ESC | 航模、精密设备 |
| 减速 DC | 高扭矩 | 有齿轮间隙 | 机器人、自动化 |

---
description: ESP32开发指南

### 1.3 步进电机（Stepper Motor）

#### 两相四线（ Bipolar ）

- 最常见类型，如 **NEMA 17**
- 每相电流需要双向驱动，必须用 H 桥驱动（如 L298N、TB6600、A4988）
- **优点**： torque 大，定位精确
- **缺点**：需要两个 H 桥，电路复杂

#### 两相六线（ Unipolar ）

- 每相有中间抽头，可单极性驱动
- 也可用四线双极性模式（更高扭矩）
- 常见于打印机、扫描仪

#### 四相八线

- 灵活性最高，可接成单极或双极

#### NEMA 17 规格参考

| 参数 | 值 |
|------|-----|
| 步距角 | 1.8°（200步/转） |
| 电压 | 12V |
| 电流 | 1.2A/相 |
| 扭矩 | ~0.4 N·m |

#### 选型建议

| 场景 | 推荐类型 |
|------|----------|
| 3D 打印 / CNC | NEMA 17（双极性） |
| 精密定位台 | 两相六线微步进 |
| 低成本项目 | 28BYJ-48（单极性减速步进） |

---
description: ESP32开发指南

## 2. 驱动方案一览

### 2.1 L298N 模块 — 直流电机驱动

#### 引脚说明

```bash
+------------------+
|  +12V  GND  +5V  |  ← 电源端子（ Motors 供电）
|  (ENA) (IN1)(IN2)|  ← 电机A控制
|  (ENB) (IN3)(IN4)|  ← 电机B控制
|  OUT1  OUT2      |  ← 电机A输出
|  OUT3  OUT4      |  ← 电机B输出
+------------------+
```

| 引脚 | 功能 |
|------|------|
| +12V | 电机电源（5~35V，推荐6~12V） |
| GND | 电源地（必须与 ESP32 共地） |
| +5V | 板内稳压输出（跳线帽插上时）/ 外部5V输入（跳线帽去掉时） |
| ENA | 电机A使能（PWM调速） |
| IN1/IN2 | 电机A方向控制 |
| ENB | 电机B使能（PWM调速） |
| IN3/IN4 | 电机B方向控制 |

#### 方向控制逻辑

| IN1 | IN2 | 电机A动作 |
|-----|-----|----------|
| 0   | 0   | 停止 |
| 1   | 0   | 正转 |
| 0   | 1   | 反转 |
| 1   | 1   | 制动 |

> ⚠️ **重要**：ENA/ENB 默认跳线帽插上（全速）。**必须拔掉跳线帽**，用 PWM 控制速度！

#### 接线图（ESP32 + L298N + DC Motor）

```bash
ESP32                L298N                 DC Motor
-------              -----                 --------
GPIO25 ──────────── ENA (PWM)
GPIO26 ──────────── IN1
GPIO27 ──────────── IN2
                     OUT1 ──────────────── Motor +
                     OUT2 ──────────────── Motor -
                     
                     +12V ←── 电源（6~12V）
                     GND  ←── 电源负极
                     GND  ←── ESP32 GND（共地）
```

#### 供电注意事项

- **ESP32 与 L298N 必须共地**（GND 连在一起）
- 电机电流较大时，使用**独立电源**，不要从 ESP32 取电
- 大于 12V 时**必须去掉 5V 跳线帽**，从外部供给 5V

---
description: ESP32开发指南

### 2.2 TB6600 控制器 — 步进电机驱动

#### 引脚说明

```bash
+-------------------+
|  V+  GND         |  ← 电源（9~42V）
|  PUL+  PUL-      |  ← 脉冲输入
|  DIR+  DIR-      |  ← 方向控制
|  ENA+  ENA-      |  ← 使能控制（可悬空）
|  A+  A-  B+  B- |  ← 电机线圈输出
+-------------------+
```

| 引脚 | 作用 |
|------|------|
| V+ / GND | 驱动器电源（9~42V DC） |
| PUL+ / PUL- | Step 脉冲信号（PWM） |
| DIR+ / DIR- | 方向控制（高/低电平） |
| ENA+ / ENA- | 使能（低电平使能，可悬空） |
| A+ A- B+ B- | 连接步进电机两组线圈 |

#### 拨码开关设置（以 NEMA 17 为例）

| SW1 | SW2 | SW3 | 电流 |
|-----|-----|-----|------|
| OFF | ON  | ON  | 1A   |
| ON  | OFF | ON  | 2A   |

| SW4 | SW5 | SW6 | 微步 |
|-----|-----|-----|------|
| OFF | OFF | OFF | 全步 |
| ON  | OFF | OFF | 1/2  |
| OFF | ON  | OFF | 1/4  |
| ON  | ON  | OFF | 1/8  |
| ON  | ON  | ON  | 1/16 |

#### 接线图（ESP32 + TB6600 + NEMA 17）

```bash
ESP32                TB6600                NEMA 17
-------              ------                -------
GPIO25 ──────────── PUL+
GND     ──────────── PUL-   （或用共阴：PUL-接GND）

GPIO26 ──────────── DIR+
GND     ──────────── DIR-

                     A+ ──────────────── 红线
                     A- ──────────────── 蓝线
                     B+ ──────────────── 绿线
                     B- ──────────────── 黑线
                     
                     V+ ←── 12V/24V 电源
                     GND ←── 电源负极
                     GND ←── ESP32 GND（共地）
```bash

> 📌 **NEMA 17 接线颜色**：不同厂家可能不同，建议用万用表测量——相通的两根线为一组（电阻约几欧姆）。

---
description: ESP32开发指南

### 2.3 舵机直接用 ESP32 PWM

舵机只需要 **PWM 信号 + 电源**，无需驱动模块：

```bash
ESP32                SG90
------               ----
GPIO23 ───────────── 橙线（信号）
GND    ───────────── 棕线（GND）
5V     ───────────── 红线（电源）  ← 仅限单个 SG90，多舵机请外接电源
```bash

> ⚠️ **多个舵机**：必须外接 5V 电源（AMS1117-5.0 或 LM7805），ESP32 的 5V 引脚电流不足以驱动多个舵机。

---
description: ESP32开发指南

## 3. ESP32 LEDC PWM 配置

### 3.1 LEDC 基本原理

ESP32 内置 LEDC（LED PWM Controller），**16 个通道**（高速 8 + 低速 8），支持：

- **频率范围**：几 Hz ~ 40MHz（实际用于电机通常 50Hz ~ 20kHz）
- **分辨率**：1~14 位（常用 8/10/12 位）
- **占空比**：0 ~ (2^resolution - 1)

### 3.2 关键参数计算

```bash
PWM频率  f = APB时钟 / (分频系数 × 计数器最大值)

APB时钟 = 80MHz

常用配置：
  - 舵机（50Hz）： resolution=16, freq=50   → 分频系数 = 80MHz/50/65536 ≈ 24414 → 取 freq=50, duty=0~65535
  - 直流电机（1kHz）： resolution=10, freq=1000 → 占空比 0~1023
  - 步进脉冲（10kHz）： resolution=10, freq=10000 → 占空比 50%（50%方波）
```

### 3.3 MicroPython LEDC 初始化

```python
from machine import Pin, PWM

# === 舵机 PWM（50Hz，16位分辨率）===
servo_pin = PWM(Pin(23), freq=50, duty=0)
# duty 范围：0~65535，对应 0%~100%
# SG90：duty=3277(5%) = 0°,  duty=4915(7.5%) = 90°,  duty=6553(10%) = 180°

# === 直流电机调速 PWM（1kHz，10位分辨率）===
motor_pin = PWM(Pin(25), freq=1000, duty=0)
# duty 范围：0~1023

# === 步进电机脉冲 PWM（10kHz，10位分辨率，50%占空比）===
step_pin = PWM(Pin(25), freq=10000, duty=512)  # 50%占空比
```

### 3.4 常见配置速查表

| 用途 | 频率 | 分辨率 | duty 上限 | duty_u16 上限 |
|------|------|--------|-----------|---------------|
| 舵机 SG90 | 50 Hz | 16 bit | 65535 | 65535 |
| 舵机 MG996R | 50 Hz | 16 bit | 65535 | 65535 |
| 直流电机调速 | 1000 Hz | 10 bit | 1023 | 40000 |
| 直流电机调速 | 20000 Hz | 8 bit | 255 | 65535 |
| 步进脉冲 | 10000 Hz | 10 bit | 511 | 32768 |

---
description: ESP32开发指南

## 4. MicroPython 实现

### 4.1 舵机控制：角度 → 脉宽

```python
from machine import Pin, PWM
import time

class Servo:
    """SG90 / MG996R 舵机控制类"""
    
    # SG90 典型参数：周期20ms，脉宽 0.5ms~2.5ms
    # 采用 50Hz 频率，16位分辨率（0~65535）
    # 0°   → 约 3277（5%）
    # 90°  → 约 4915（7.5%）
    # 180° → 约 6553（10%）
    
    def __init__(self, pin, min_duty=3277, max_duty=6553):
        self.pwm = PWM(Pin(pin), freq=50)
        self.min_duty = min_duty  # 0° 对应脉宽
        self.max_duty = max_duty  # 180° 对应脉宽
    
    def angle(self, deg):
        """设置角度 0~180°"""
        duty = int(self.min_duty + (deg / 180) * (self.max_duty - self.min_duty))
        self.pwm.duty(duty)
    
    def release(self):
        """释放舵机（停止输出）"""
        self.pwm.duty(0)


# --- 使用示例 ---
s = Servo(pin=23)

# 转到指定角度
s.angle(0)    # 归零
time.sleep(1)
s.angle(90)   # 中位
time.sleep(1)
s.angle(180)  # 最大角度

# 释放（切断PWM，舵机可手动转动）
s.release()
```bash

> 💡 **校准技巧**：如果角度偏差，可调整 `min_duty` 和 `max_duty`，或者传入自定义参数：
> ```python
> s = Servo(pin=23, min_duty=3000, max_duty=6800)
> ```

### 4.2 直流电机：L298N + PWM 速度控制

```python
from machine import Pin, PWM

class DCMotor:
    """L298N 直流电机驱动"""
    
    def __init__(self, en_pin, in1_pin, in2_pin):
        self.en  = PWM(Pin(en_pin),  freq=1000, duty=0)  # 使能（PWM调速）
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self._stop()
    
    def _stop(self):
        self.in1.value(0)
        self.in2.value(0)
        self.en.duty(0)
    
    def forward(self, speed=512):
        """正转 speed: 0~1023"""
        self.in1.value(1)
        self.in2.value(0)
        self.en.duty(min(speed, 1023))
    
    def backward(self, speed=512):
        """反转 speed: 0~1023"""
        self.in1.value(0)
        self.in2.value(1)
        self.en.duty(min(speed, 1023))
    
    def stop(self):
        self._stop()
    
    def brake(self):
        """能耗制动（快速停止）"""
        self.in1.value(1)
        self.in2.value(1)
        self.en.duty(0)


# --- 使用示例 ---
# ESP32 GPIO25=ENA, GPIO26=IN1, GPIO27=IN2
motor = DCMotor(en_pin=25, in1_pin=26, in2_pin=27)

motor.forward(300)  # 低速正转
import time
time.sleep(2)
motor.forward(1023) # 全速正转
time.sleep(2)
motor.stop()        # 滑行停止
time.sleep(1)
motor.backward(512) # 全速反转
time.sleep(2)
motor.brake()       # 快速制动
```

### 4.3 步进电机：TB6600 + AccelStepper 类

MicroPython 没有原生 AccelStepper 库，但可以自行实现一个简化版：

```python
from machine import Pin, PWM
import time

class Stepper:
    """TB6600 步进电机驱动（整步模式）"""
    
    def __init__(self, pul_pin, dir_pin, steps_per_rev=200):
        """
        pul_pin: 脉冲引脚（GPIO25 接 PUL+）
        dir_pin: 方向引脚（GPIO26 接 DIR+）
        steps_per_rev: 电机步距角对应步数（NEMA 17 = 200）
        """
        self.pul = PWM(Pin(pul_pin), freq=1000, duty=0)
        self.dir = Pin(dir_pin, Pin.OUT)
        self.steps_per_rev = steps_per_rev
        self.current_step = 0
        self.speed_rpm = 10  # 目标转速（rpm）
    
    def _pulse(self, width_ms=1):
        """发送一个步进脉冲"""
        self.pul.duty(512)   # 50% 占空比
        time.sleep_ms(int(width_ms))
        self.pul.duty(0)
        time.sleep_ms(int(width_ms))
    
    def set_direction(self, direction):
        """设置方向：1=正转，0=反转"""
        self.dir.value(1 if direction > 0 else 0)
    
    def step(self, steps, direction=1):
        """步进指定步数"""
        self.set_direction(direction)
        delay_us = int(60_000_000 // (self.speed_rpm * self.steps_per_rev * 2))
        for _ in range(abs(steps)):
            self.pul.duty(512)
            time.sleep_us(delay_us)
            self.pul.duty(0)
            time.sleep_us(delay_us)
        self.current_step += steps * direction
    
    def rotate(self, rpm, revs=1):
        """以指定转速旋转指定圈数"""
        self.speed_rpm = min(max(rpm, 1), 300)
        steps = int(revs * self.steps_per_rev)
        direction = 1 if steps > 0 else -1
        self.step(abs(steps), direction)
    
    def release(self):
        """释放电机（停止脉冲）"""
        self.pul.duty(0)


class AccelStepper:
    """带加减速的步进电机驱动（简化版）"""
    
    def __init__(self, pul_pin, dir_pin, steps_per_rev=200):
        self.stepper = Stepper(pul_pin, dir_pin, steps_per_rev)
        self.steps_per_rev = steps_per_rev
        self.target_pos = 0
        self.current_pos = 0
        self.speed = 0
        self.max_speed = 200   # steps/s
        self.accel = 400       # steps/s²
        self.last_step_time = 0
    
    def move_to(self, position):
        self.target_pos = position
    
    def run(self):
        """在主循环中调用（非阻塞）"""
        distance = self.target_pos - self.current_pos
        if distance == 0:
            return False
        
        direction = 1 if distance > 0 else -1
        self.stepper.set_direction(direction)
        
        # 简单加减速
        if abs(self.speed) < self.max_speed:
            self.speed += self.accel * 0.001  # 假设每1ms调用一次
        self.speed = min(self.speed, self.max_speed)
        
        step_interval = 1_000_000 / self.speed  # μs
        now = time.ticks_us()
        if now - self.last_step_time >= step_interval:
            self.stepper.pul.duty(512)
            time.sleep_us(10)
            self.stepper.pul.duty(0)
            self.current_pos += direction
            self.last_step_time = now
            return True
        return False


# --- 使用示例（整步模式）---
stepper = Stepper(pul_pin=25, dir_pin=26, steps_per_rev=200)

# 正转 1 圈（200 步），转速 60 RPM
stepper.speed_rpm = 60
stepper.rotate(rpm=60, revs=1)

# 反转半圈
stepper.speed_rpm = 30
stepper.rotate(rpm=30, revs=-0.5)

stepper.release()
```

### 4.4 多舵机协同（机械臂）

```python
from machine import Pin, PWM
import time

class MultiServo:
    """多舵机管理"""
    
    def __init__(self, pins):
        """
        pins: 引脚列表，如 [23, 22, 21, 19]
        """
        self.servos = []
        for pin in pins:
            pwm = PWM(Pin(pin), freq=50)
            pwm.duty(0)
            self.servos.append(pwm)
    
    def set_angle(self, index, deg, min_d=3277, max_d=6553):
        duty = int(min_d + (deg / 180) * (max_d - min_d))
        self.servos[index].duty(duty)
    
    def release_all(self):
        for s in self.servos:
            s.duty(0)


# --- 使用示例：4自由度机械臂 ---
servos = MultiServo(pins=[23, 22, 21, 19])
# servos[0]: 底座旋转
# servos[1]: 大臂
# servos[2]: 小臂
# servos[3]: 夹爪

# 归位
servos.set_angle(0, 90)
servos.set_angle(1, 90)
servos.set_angle(2, 90)
servos.set_angle(3, 0)   # 夹爪张开
time.sleep(1)

# 抓取动作
servos.set_angle(3, 0)   # 张开
time.sleep(0.5)
servos.set_angle(1, 60)
time.sleep(0.5)
servos.set_angle(2, 120)
time.sleep(0.5)
servos.set_angle(3, 45)  # 闭合夹取
time.sleep(1)

servos.release_all()
```bash

---
description: ESP32开发指南

## 5. 实战项目

### 5.1 智能窗帘（舵机）

**目标**：根据光照或定时器自动开合窗帘

**材料**：
- ESP32 × 1
- SG90 舵机 × 1（建议改装为连续旋转或用拉线方式）
- 光敏电阻（GL5528）× 1
- 杜邦线若干

**接线**：
```bash
GPIO23 → 舵机信号（橙）
GPIO34 → 光敏电阻（模拟输入）
5V     → 舵机电源（红）/ 光敏电阻 VCC
GND    → 共地
```bash

**代码**：

```python
from machine import Pin, PWM, ADC
import time

class SmartCurtain:
    def __init__(self, servo_pin=23, ldr_pin=34):
        self.servo = PWM(Pin(servo_pin), freq=50)
        self.ldr = ADC(Pin(ldr_pin))
        self.ldr.width(ADC.WIDTH_10BIT)  # 0~1023
        self.position = 0  # 0=关闭, 100=全开
    
    def angle_to_duty(self, angle):
        # 0°~180° → 3277~6553
        return int(3277 + (angle / 180) * 3276)
    
    def open(self, speed=5):
        """缓慢打开窗帘"""
        for pos in range(self.position, 101, speed):
            self.servo.duty(self.angle_to_duty(pos * 1.8))
            self.position = pos
            time.sleep(0.1)
    
    def close(self, speed=5):
        """缓慢关闭窗帘"""
        for pos in range(self.position, -1, -speed):
            self.servo.duty(self.angle_to_duty(pos * 1.8))
            self.position = pos
            time.sleep(0.1)
    
    def auto_control(self):
        """根据光照自动控制"""
        light = self.ldr.read()
        # 阈值校准：数值越小=越暗
        if light < 300:      # 天黑了 → 关窗帘
            self.close()
        elif light > 700:    # 天亮了 → 开窗帘
            self.open()
    
    def release(self):
        self.servo.duty(0)


# --- 使用 ---
curtain = SmartCurtain()

# 方式1：手动
curtain.open(speed=3)
time.sleep(5)
curtain.close(speed=3)

# 方式2：自动循环检测
while True:
    curtain.auto_control()
    time.sleep(60)  # 每分钟检测一次
```bash

**物理改造提示**：
- 舵机安装：将舵机固定在窗帘轨道旁，用橡皮筋或细绳连接窗帘
- 连续旋转版本：直接缠线方式更简单
- 角度版本：用舵机臂转动卷轴实现

---
description: ESP32开发指南

### 5.2 机械臂关节（多舵机）

**目标**：4轴机械臂，可通过串口指令控制各关节角度

**接线**：
```bash
GPIO23 → 底座舵机
GPIO22 → 肩部舵机
GPIO21 → 肘部舵机
GPIO19 → 夹爪舵机
```bash

**代码**：

```python
from machine import Pin, PWM, UART
import time

class RobotArm:
    def __init__(self, pins, uart_baud=115200):
        self.uart = UART(1, baudrate=uart_baud, tx=17, rx=16)
        self.servos = [PWM(Pin(p)) for p in pins]
        for s in self.servos:
            s.freq(50)
            s.duty(0)
        self.angles = [90, 90, 90, 0]  # 各关节当前角度
    
    def angle_to_duty(self, a):
        return int(3277 + (a / 180) * 3276)
    
    def set_joint(self, idx, angle):
        angle = max(0, min(180, int(angle)))
        self.servos[idx].duty(self.angle_to_duty(angle))
        self.angles[idx] = angle
    
    def home(self):
        for i in range(4):
            self.set_joint(i, [90, 90, 90, 0][i])
        time.sleep(1)
    
    def pick_and_place(self, target_angles):
        """按顺序移动到目标角度序列"""
        self.home()
        for angles in target_angles:
            for i, a in enumerate(angles):
                self.set_joint(i, a)
            time.sleep(0.5)
    
    def listen(self):
        """监听串口命令，格式：J0:90 J1:45 J2:120 J3:30"""
        if self.uart.any():
            cmd = self.uart.read().decode().strip()
            for part in cmd.split():
                if ':' in part:
                    idx, val = part.split(':')
                    if idx.startswith('J') and idx[1].isdigit():
                        self.set_joint(int(idx[1]), int(val))
            self.uart.write(f"ACK: {self.angles}\n".encode())
    
    def release(self):
        for s in self.servos:
            s.duty(0)


# --- 使用 ---
arm = RobotArm(pins=[23, 22, 21, 19])

# 归位
arm.home()

# 抓取流程（演示序列）
sequence = [
    [90, 120, 60, 0],   # 伸出
    [90, 90, 90, 30],   # 下降闭合
    [90, 120, 60, 30],  # 抬起
    [150, 120, 60, 30], # 转到放置区
    [150, 90, 90, 0],   # 下降张开
]
arm.pick_and_place(sequence)

# 串口控制模式（主循环）
while True:
    arm.listen()
```bash

---
description: ESP32开发指南

### 5.3 自动化阀门（舵机或步进）

**目标**：用舵机或步进电机控制水阀/气阀的开关

**舵机版**（适合 90° 角阀）：
```bash
ESP32 GPIO23 → 舵机信号
舵机臂固定在阀门手轮上，旋转 90° 实现开/关
```

```python
from machine import Pin, PWM
import time

class ValveActuator:
    """旋转阀门执行器（90° 阀）"""
    
    def __init__(self, pin=23):
        self.pwm = PWM(Pin(pin), freq=50)
        self.is_open = False
    
    def angle_to_duty(self, a):
        return int(3277 + (a / 180) * 3276)
    
    def open(self, delay=2):
        self.pwm.duty(self.angle_to_duty(90))  # 开
        time.sleep(delay)
        self.pwm.duty(0)
        self.is_open = True
    
    def close(self, delay=2):
        self.pwm.duty(self.angle_to_duty(0))   # 关
        time.sleep(delay)
        self.pwm.duty(0)
        self.is_open = False
    
    def toggle(self):
        if self.is_open:
            self.close()
        else:
            self.open()


# --- 使用 ---
valve = ValveActuator(pin=23)

# 自动浇花示例
import machine, time

rtc = machine.RTC()
valve.open(delay=3)   # 开阀浇水3秒
time.sleep(10)
valve.close(delay=3)  # 关阀
```bash

**步进版**（适合球阀，需要大力矩）：

```python
class StepperValve:
    """步进电机阀门执行器（球阀）"""
    
    def __init__(self, pul_pin=25, dir_pin=26):
        # 球阀通常只需旋转 90°~180°
        self.stepper = Stepper(pul_pin, dir_pin, steps_per_rev=200)
        self.stepper.speed_rpm = 30
    
    def open(self):
        # NEMA17 减速比通常 1:1，球阀需约 400 步（200步/转 × 2圈 = 90°...根据实际联轴器调整）
        self.stepper.rotate(rpm=30, revs=2)  # 正转 2 圈
        self.stepper.release()
    
    def close(self):
        self.stepper.rotate(rpm=30, revs=-2)  # 反转 2 圈
        self.stepper.release()
    
    def toggle(self):
        self.open() if not hasattr(self, '_state') or not self._state else self.close()
        self._state = not self._state

# --- 使用 ---
valve = StepperValve()
valve.open()
```bash

---
description: ESP32开发指南

## 6. 常见问题

### Q1: 电机抖动，不平滑

**原因**：
- PWM 频率过低（< 30Hz）导致舵机接收信号不连续
- 占空比超出舵机有效范围
- 电源电压不稳或电流不足

**排查步骤**：
```
1. 用示波器或逻辑分析仪检查 PWM 波形是否标准 20ms 周期
2. 逐步调整 min_duty / max_duty 值
3. 确认电源能提供足够电流（SG90 需 ~500mA 峰值）
```bash

**解决示例**：
```python
# 原始配置（可能抖动）
s = Servo(23, min_duty=3277, max_duty=6553)

# 微调（校准后）
s = Servo(23, min_duty=3000, max_duty=6800)  # 根据实际测试调整
```bash

---
description: ESP32开发指南

### Q2: 电机发热严重

**原因**：
- 长时间满负载运行
- 散热不良（封闭式安装）
- 驱动电流过大（驱动板电流设置 > 电机额定电流）
- 供电电压过高

**解决**：
```
1. 直流电机：降低 PWM 占空比（限速）
2. 步进电机：降低 TB6600 电流拨档（SW1/SW2/SW3）
3. 改善散热：加装散热片或风扇
4. 间歇工作：PWM 占空比循环（如开1秒关0.5秒）
```bash

---
description: ESP32开发指南

### Q3: 供电不足

**症状**：
- 电机转速明显低于标称值
- 舵机反应迟钝或根本不动
- ESP32 频繁重启（断电复位）

**诊断思路**：
```bash
电源 → 检查电压表读数
  ↓
电流 → 串联万用表测量工作电流
  ↓
布线 → 确认共地、线径足够粗
```bash

**供电方案推荐**：

| 场景 | 电源方案 |
|------|----------|
| 单个 SG90 | ESP32 的 5V 引脚（可承受） |
| 多个舵机 | 外接 5V/2A 电源（如 AMS1117-5.0 模块） |
| L298N + DC 电机 | 6~12V 电池或电源适配器，独立于 ESP32 |
| TB6600 + 步进电机 | 12V/24V 电源（与 ESP32 共地） |

> ⚠️ **绝对禁止**：将 12V 直接接到 ESP32 的 5V 引脚！

---
description: ESP32开发指南

### Q4: 步进电机丢步

**原因**：
- 启动频率过高（超过电机响应极限）
- 电源电压不足（步进电机需要快速电流上升）
- 机械卡顿（轴承损坏或负载过大）

**解决**：
```
1. 降低转速（rpm）
2. 使用加减速曲线（启动慢，逐渐加速）
3. 提高供电电压（12V → 24V）
4. 选择合适的微步（1/8 或 1/16 步更平滑）
```bash

---
description: ESP32开发指南

### Q5: L298N 发烫但不工作

**排查顺序**：
```
1. 测量 OUT 引脚与 GND 之间的电阻（正常几欧~几十欧）
2. 确认 ENA 跳线帽已拔掉（PWM 才能生效）
3. 检查 IN1/IN2 逻辑是否正确（禁止同时为 HIGH）
4. 测量 5V 稳压输出是否有 5V（跳线帽插上时）
```bash

---
description: ESP32开发指南

### Q6: ESP32 复位/崩溃

**常见原因**：
- 电机启动电流冲击导致 ESP32 供电跌落
- 电机线与数据线平行走线，产生干扰
- 接线松动导致瞬间短路

**解决**：
```
1. 在 ESP32 的电源线上加 100μF + 100nF 去耦电容
2. 电机线与信号线分开布线，或使用屏蔽线
3. 所有连接点焊接或使用杜邦线插紧
```bash

---
description: ESP32开发指南

## 附录：接线速查图汇总

### ESP32 + SG90 舵机
```bash
GPIO23 ────── 橙线（信号）
GND    ────── 棕线
5V     ────── 红线（单个舵机）
```

### ESP32 + L298N + DC 电机
```bash
GPIO25 ── ENA(PWM)    L298N OUT1/OUT2 ── Motor
GPIO26 ── IN1         +12V     ─────── 电源+
GPIO27 ── IN2         GND      ─────── 电源-
                     GND      ─────── ESP32 GND（共地）
```

### ESP32 + TB6600 + NEMA 17
```bash
GPIO25 ── PUL+        TB6600 A+ A- B+ B- ── NEMA17
GPIO26 ── DIR+        V+ GND   ─────────── 12V/24V
GND    ── PUL- DIR-   GND      ─────────── ESP32 GND（共地）
```bash

---
description: ESP32开发指南

*文档版本：v1.0 | 基于 ESP32 + MicroPython | 参考：CSDN / Random Nerd Tutorials / MakerGuides*