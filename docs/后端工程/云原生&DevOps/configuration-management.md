---
title: 配置管理
description: 配置管理工具
tags:
- 配置管理
- Configuration Management
---

# 配置管理 ⚙️

> 基础设施即代码

***

## Ansible

```yaml
- hosts: webservers
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
```

## Terraform

```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345"
  instance_type = "t2.micro"
}
```

***

*配置管理让运维更高效*
