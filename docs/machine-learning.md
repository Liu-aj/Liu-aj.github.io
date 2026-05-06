---
title: 机器学习
description: ML 基础
---

# 机器学习 🤖

> 从数据中学习

---

## 类型

| 类型 | 说明 |
|------|------|
| 监督学习 | 标签数据 |
| 无监督学习 | 无标签数据 |
| 强化学习 | 奖励驱动 |

## 流程

```
数据 → 特征工程 → 模型训练 → 评估 → 部署
```

## scikit-learn

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

---

*机器学习是 AI 的基础*
