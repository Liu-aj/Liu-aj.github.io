---
title: JSON/YAML 指南
description: JSON 和 YAML 数据格式
---

# JSON / YAML 指南 📄

> 两种常用的数据序列化格式

---

## JSON

### 语法
```json
{
  "name": "John",
  "age": 30,
  "is_active": true,
  "scores": [90, 85, 88],
  "address": {
    "city": "Beijing",
    "zip": "100000"
  }
}
```markdown

### Python 操作
```python
import json

# 解析
data = json.loads('{"name": "John"}')

# 序列化
json_str = json.dumps(data, indent=2)
```python

## YAML

### 语法
```yaml
name: John
age: 30
is_active: true
scores:
  - 90
  - 85
  - 88
address:
  city: Beijing
  zip: "100000"
```markdown

### Python 操作
```python
import yaml

# 解析
with open('config.yaml') as f:
    data = yaml.safe_load(f)

# 序列化
yaml_str = yaml.dump(data)
```

## 对比

| 特性 | JSON | YAML |
|------|------|------|
| 可读性 | 一般 | 更好 |
| 类型支持 | 基础类型 | 更丰富 |
| 注释 | 不支持 | 支持 |
| 文件大小 | 更小 | 稍大 |

---

*JSON 用于数据传输，YAML 用于配置文件*
