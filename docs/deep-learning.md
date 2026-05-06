---
title: 深度学习
description: 神经网络基础
---

# 深度学习 🧠

> 多层神经网络

---

## 框架

| 框架 | 公司 |
|------|------|
| TensorFlow | Google |
| PyTorch | Meta |
| JAX | Google |

## PyTorch

```python
import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(784, 10)
    
    def forward(self, x):
        return self.fc(x)
```

---

*深度学习推动 AI 革命*
