---
layout: post
title: MongoDB查询技巧
date: 2018-09-07 18:11:26
forType: DB
category: MongoDB
tag: [MongoDB, 查询技巧]
---

* content
{:toc}

# MongoDB查询技巧

## 1. 模糊搜索

```javascript
db.getCollection('collectionName').find({"fieldName": {$regex: "searchTerm"}});

// 忽略大小写的模糊搜索
db.getCollection('collectionName').find({"fieldName": {$regex: "searchTerm", $options: "i"}});
```

## 2. 时间段查询

```javascript
db.getCollection('collectionName').find({
  "dateField": {
    $gte: new Date("2018-01-01T00:00:00.000+08:00"), 
    $lt: new Date("2018-01-01T23:59:59.000+08:00")
  }
});
```

## 3. 去重统计

```javascript
// 获取某个字段的所有不重复值
db.collectionName.distinct("fieldName");

// 条件去重
db.collectionName.distinct("fieldName", {"conditionField": "conditionValue"});

// 统计不重复值的数量
db.collectionName.distinct("fieldName").length;
```

## 4. 常用查询操作符

```javascript
// 等于
{ "field": value }

// 不等于
{ "field": { $ne: value } }

// 大于/小于/大于等于/小于等于
{ "field": { $gt: value } }
{ "field": { $lt: value } }
{ "field": { $gte: value } }
{ "field": { $lte: value } }

// 在给定数组中
{ "field": { $in: [value1, value2, ...] } }

// 不在给定数组中
{ "field": { $nin: [value1, value2, ...] } }
```