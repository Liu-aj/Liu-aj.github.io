---
title: GitLab 指南
description: GitLab CI/CD 使用指南
---

# GitLab 指南 📦

> Self-hosted Git 仓库与 CI/CD

---

## CI/CD

### 基本配置
```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - npm ci
    - npm run build

test:
  stage: test
  script:
    - npm test
```

### Docker 集成
```yaml
build:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t myapp .
```

## GitLab Runner

```bash
# 安装
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
sudo apt-get install gitlab-runner

# 注册
sudo gitlab-runner register
```

---

*GitLab 是强大的 DevOps 平台*
