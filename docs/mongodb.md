---
title: MongoDB 指南
description: MongoDB 文档数据库
---

# MongoDB 指南 📄

> 灵活的文档数据库

---

## 基本操作

```bash
# 插入
db.users.insertOne({"name": "John", "age": 30})

# 查询
db.users.find({"age": {"$gte": 18}})
db.users.findOne({"name": "John"})

# 更新
db.users.updateOne(
    {"name": "John"},
    {"$set": {"age": 31}}
)

# 删除
db.users.deleteOne({"name": "John"})
```

## 聚合

```javascript
db.orders.aggregate([
    {"$match": {"status": "completed"}},
    {"$group": {"_id": "$user_id", "total": {"$sum": "$amount"}}}
])
```

---

*MongoDB 是灵活的文档数据库*
