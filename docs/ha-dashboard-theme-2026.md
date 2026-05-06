# Home Assistant 仪表盘主题美化完全指南（2026）

> 更新日期：2026-05-06

---

## 一、Card-mod 插件安装与配置

### 1.1 安装步骤（HACSB）

1. **安装 HACS**（如果还没有）：
   - 在 HA → 设置 → 添加-ons → 自定义加载项 → 添加 `https://github.com/hacs/integration`
   - 或参考官方 HACS 安装教程

2. **通过 HACS 安装 card-mod**：
   - HACS → 集成 → 搜索 `card-mod` → 下载安装
   - 或在 HA → 设置 → 附加组件 → 搜索 `card-mod`

3. **重启 Home Assistant**

### 1.2 必须配置（2026 版本）

在 `configuration.yaml` 中添加：

```yaml
frontend:
  themes: !include_dir_merge_named themes/
  extra_module_url:
    - /local/community/lovelace-layout-card/layout.js
```markdown

> card-mod 依赖 Lovelace UI，请确保 HA 版本 >= 2024.3

---

## 二、2026 社区精选主题推荐

### 极简风格（Minimalist）

#### 1. UI-Lovelace-Minimalist
- **仓库**：https://github.com/UI-Lovelace-Minimalist/UI
- **特点**：UX 设计师设计，移动端优先，代码量少但视觉精致
- **适合**：喜欢干净、简洁界面的用户
- **注意**：需要配合 `button-card` 插件使用

#### 2. Mini Media Player 主题
- **配合**：Spotify/Apple Music 等媒体卡片使用
- **特点**：极简媒体控制条

#### 3. Bubble Card 主题
- **仓库**：https://github.com/com片/bubble-card
- **特点**：弹出式卡片设计，悬停显示详情，适合做信息聚合面板

---

### 信息密度风格

#### 1. Caule Theme Pack
- **风格**：暗色系，玻璃拟态，大量留白但信息密度高
- **适合**：桌面大屏用户
- **变体**：蓝、绿、红多色可选

#### 2. Google Light/Dark Theme
- **特点**：复刻 Google Material You 风格
- **适合**：喜欢 Google 设计的用户

#### 3. macOS Light/Dark Theme
- **特点**：复刻 macOS 界面风格
- **适合**：喜欢 Apple 设计的用户

#### 4. LCARS Theme（星际迷航风格）
- **特点**：经典科幻风格，适合树莓派小屏
- **适合**：个性化玩家

---

### 2026 年新晋主题

| 主题名 | 风格 | GitHub |
|--------|------|--------|
| **waves** | 波浪动画，流动感 | 社区精选 |
| **soft-ui-dark** | 柔和暗色，卡片玻璃化 | 社区精选 |
| **ios-themes** | iOS 17 风格，动态壁纸 | 社区精选 |

---

## 三、主题定制实战步骤

### 步骤 1：安装主题

**方法 A：通过 HACS 安装主题包**

```bash
```markdown

**方法 B：手动下载主题 YAML**

1. 找到主题 GitHub 仓库
2. 下载 `.yaml` 文件
3. 放入 `config/themes/` 目录
4. 在 HA → 配置 → 面板 → 主题 → 刷新主题

### 步骤 2：切换主题

```bash
```markdown

### 步骤 3：微调（用 card-mod）

在每个卡片的 `card_mod` 属性中覆盖样式：

```yaml
type: entities
entities:
  - entity: sensor.temperature
card_mod:
  style: |
    ha-card {
      background: linear-gradient(135deg, #1a1a2e, #16213e);
      border-radius: 16px;
      border: none;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
```

---

## 四、新手常见避坑指南

### ❌ 坑 1：card-mod 版本冲突

**问题**：升级 card-mod 后主题样式错乱

**解决**：
```yaml
# 锁定版本，不自动更新
card_mod:
  version: specific_version
```markdown
或每次升级前先在测试环境验证

### ❌ 坑 2：Lovelace 刷新后主题消失

**原因**：使用了非持久化的主题配置

**解决**：确保主题 YAML 放在 `config/themes/` 目录，而非内存配置

### ❌ 坑 3：自定义 CSS 不生效

**原因**：card-mod style 格式错误

**解决**：
```yaml
# 正确格式
card_mod:
  style: |
    ha-card {
      --paper-card-background-color: transparent;
    }
```

### ❌ 坑 4：移动端和桌面显示不一致

**解决**：在主题 YAML 中分别定义 `lovelace-cards` 的响应式布局

### ✅ 推荐工作流

```bash
2. 搭配 button-card、bubble-card 使用
3. 用 card-mod 做细节微调
4. 最终效果通过 YAML 版本控制（可回溯）
```

---

## 五、Card-mod 常用样式代码片段

### 玻璃拟态卡片

```yaml
card_mod:
  style: |
    ha-card {
      background: rgba(255,255,255,0.1);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 16px;
    }
```markdown

### 渐变背景

```yaml
card_mod:
  style: |
    ha-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
    }
```

### 圆形头像/设备图标

```yaml
card_mod:
  style: |
    ha-state-icon {
      background: #4CAF50;
      border-radius: 50%;
      padding: 8px;
    }
```

---

## 六、参考资源

- card-mod GitHub：https://github.com/thomasloven/lovelace-card-mod
- UI-Lovelace-Minimalist：https://github.com/UI-Lovelace-Minimalist/UI
- HA 社区主题帖：https://community.home-assistant.io/c/themes/46
- 2026 HA Dashboard 刷新讨论：https://www.reddit.com/r/homeassistant/comments/1qlb9rr/

---

*文档版本：v1.0 | 建议配合 HA 2026.5+ 使用*