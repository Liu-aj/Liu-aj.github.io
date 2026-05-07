---
title: Serverless
description: 无服务器架构
tags:
- Serverless
- 无服务器
- 云
---

# Serverless ☁️

> 事件驱动架构

***

## 特点

| 优点 | 缺点 |
|------|------|
| 无需管理服务器 | 冷启动延迟 |
| 自动扩展 | 供应商锁定 |
| 按需付费 | 调试困难 |
| 高可用 | 运行时限制 |

## 函数

### AWS Lambda
```python
def handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello'
    }
```markdown

### 触发器
- HTTP 请求
- 文件上传
- 数据库变更
- 定时任务

***

*Serverless 让开发更简单*
