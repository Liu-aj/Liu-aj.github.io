---
title: 调试技巧
description: 常用调试方法
tags:
- 调试
- Debug
- 排查
---

# 调试技巧 🔍

> 快速定位和解决问题

---

## Python

```python
# 使用 pdb
import pdb; pdb.set_trace()

# 使用 ipdb
import ipdb; ipdb.set_trace()

# 日志调试
import logging
logging.basicConfig(level=logging.DEBUG)
```

## JavaScript

```javascript
// console 调试
console.log('value:', value);
console.table({a: 1, b: 2});
console.trace();

// debugger
debugger;
```

## Linux

```bash
# 查看进程
ps aux | grep process
top -p PID

# 查看网络
ss -tlnp
netstat -anp

# 查看日志
tail -f /var/log/syslog
journalctl -u service
```

---

*调试是开发的核心技能*
