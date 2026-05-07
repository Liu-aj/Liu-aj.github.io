---
title: WebSocket
description: 双向通信协议
tags:
- WebSocket
- 实时通信
- Web开发
---

# WebSocket 🔌

> 实时双向通信

---

## 特点

- 全双工通信
- 服务器推送
- 持久连接
- 低延迟

## 示例

### JavaScript
```javascript
const ws = new WebSocket('wss://example.com/ws');

ws.onopen = () => {
    ws.send('Hello');
};

ws.onmessage = (event) => {
    console.log('Received:', event.data);
};
```python

### Python
```python
import websockets

async def connect():
    async with websockets.connect('wss://example.com/ws') as ws:
        await ws.send('Hello')
        response = await ws.recv()
```

---

*WebSocket 让实时应用更简单*
