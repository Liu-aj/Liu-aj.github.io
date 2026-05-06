---
title: 测试指南
description: 测试最佳实践
---

# 测试指南 🧪

> 整理测试方法与最佳实践

---

## 测试金字塔

```
        /\
       /  \     E2E 测试
      /----\    (少量，高成本)
     /      \   集成测试
    /--------\  (中量，中成本)
   /          \ 单元测试
  /------------\(大量，低成本)
```

## 单元测试

### Python
```python
import pytest

def test_add():
    assert 1 + 1 == 2
```

### ESP32
```cpp
#include <unity.h>

void test_led_turn_on() {
    digitalWrite(LED_PIN, HIGH);
    TEST_ASSERT_EQUAL(HIGH, digitalRead(LED_PIN));
}
```

## 集成测试

### AI Agent 测试
- 测试工具调用
- 测试记忆存储
- 测试错误恢复

### IoT 设备测试
- 测试设备配网
- 测试数据上传
- 测试固件更新

## E2E 测试

### Web 应用
- Selenium
- Playwright
- Cypress

### API 测试
- Postman
- curl

---

*测试是质量的保障*
