---
title: 事件驱动
description: 事件驱动架构
tags:
- 事件驱动
- Event Driven
- 架构
---

# 事件驱动 ⚡

> 异步事件处理

***

## 模式

### 发布/订阅
```python
# 发布者
event_bus.publish('user.created', user_data)

# 订阅者
@event_bus.subscribe('user.created')
def handle_user_created(user_data):
    send_welcome_email(user_data)
```

## 事件溯源

```python
# 保存事件序列
events.append(Event(type='UserCreated', data=user_data))

# 从事件重建状态
state = reduce(apply_event, events)
```

***

*事件驱动让系统更松耦合*
