---
title: 实用脚本
description: 常用脚本收集
tags:
- 脚本
- Shell
- 自动化
---

# 实用脚本 🔧

> 收集常用脚本，提升效率

***

## Shell 脚本

### 备份脚本
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR=/backup
SOURCE_DIR=/home/user/data

tar -czf $BACKUP_DIR/backup_$DATE.tar.gz $SOURCE_DIR
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```bash

### 系统监控脚本
```bash
#!/bin/bash
echo "=== System Status ==="
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%"
echo "Memory: $(free -h | awk '/Mem:/ {print $3 "/" $2}')"
echo "Disk: $(df -h / | awk 'NR==2 {print $3 "/" $2}')"
```bash

### Docker 清理脚本
```bash
#!/bin/bash
docker system prune -af
docker volume prune -f
```python

## Python 脚本

### 批量重命名
```python
import os
import re

def batch_rename(directory, pattern, replacement):
    for filename in os.listdir(directory):
        new_name = re.sub(pattern, replacement, filename)
        os.rename(os.path.join(directory, filename),
                  os.path.join(directory, new_name))

batch_rename('./files', r'_', '-')
```

### 文件同步
```python
import shutil
from pathlib import Path

def sync_files(src, dst):
    src_path = Path(src)
    dst_path = Path(dst)
    for item in src_path.rglob('*'):
        if item.is_file():
            rel_path = item.relative_to(src_path)
            dst_file = dst_path / rel_path
            if not dst_file.exists() or item.stat().st_mtime > dst_file.stat().st_mtime:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_file)
```

***

*持续收集...*
