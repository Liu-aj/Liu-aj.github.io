---
layout: post
title: Kettle入门指南与实战技巧
date: 2024-03-07 23:00:31
forType: ETL
category: ETL
tag: [ETL, Kettle, 数据集成, 数据迁移, 数据仓库]
---

* content
{:toc}

前言（ETL）
---

ETL是英文Extract-Transform-Load的缩写，用来描述将数据从来源端经过抽取（extract）、转换（transform）、加载（load）至目的端的过程。ETL一词较常用在数据仓库，但其对象并不限于数据仓库。



用途
---

Kettle是一款开源的 ETL工具，纯 Java编写，绿色无需安装，数据抽取高效稳定 (数据迁移工具)。Kettle中有两种脚本文件，transformation和job。transformation完成针对数据的基础转换，job则完成整个工作流的控制。 Kettle中文名称叫水壶，该项目的主程序员MATT希望把各种数据放到一个壶里，然后以一种指定的格式流出。&#x20;

Kettle 家族目前包括4个产品：Spoon、Pan、CHEF、Kitchen。&#x20;

SPOON：允许你通过图形界面来设计ETL转换过程（Transformation）。

&#x20;PAN：允许你批量运行由Spoon设计的ETL转换 (例如使用一个时间调度器)。Pan是一个后台执行的程序，没有图形界面。&#x20;

CHEF：允许你创建任务（Job）。 任务通过允许每个转换，任务，脚本等等，更有利于自动化更新数据仓库的复杂工作。任务通过允许每个转换，任务，脚本等等。任务将会被检查，看看是否正确地运行了。&#x20;

KITCHEN：允许你批量使用由Chef设计的任务 (例如使用一个时间调度器)。KITCHEN也是一个后台运行的程序。



安装
---

[下载地址](https://www.hitachivantara.com/en-us/products/pentaho-plus-platform/data-integration-analytics/pentaho-community-edition.html "https://www.hitachivantara.com/en-us/products/pentaho-plus-platform/data-integration-analytics/pentaho-community-edition.html")：&#x20;



启动问题：

软件启动：

## 4.应用

### 作业创建

作业（Job）是Kettle中用于控制整个工作流的组件，适合处理流程控制、错误处理、调度等场景。

#### 4.1 作业基本结构

**作业组成元素：**
- **作业项（Job Entry）**：作业中的最小执行单元，如转换、脚本、文件操作等
- **跳（Hop）**：作业项之间的连接线，定义执行顺序和条件

**常用作业项：**
| 作业项 | 功能 |
|--------|------|
| 转换 | 运行一个转换 |
| 作业 | 嵌套运行另一个作业 |
| Shell | 执行Shell脚本 |
| SQL | 执行SQL语句 |
| 成功 | 标记作业成功结束 |
| 失败 | 标记作业失败 |
| 中止 | 立即终止作业 |
| 等待 | 等待指定时间 |
| 循环文件 | 遍历文件夹中的文件 |
| 发送邮件 | 发送电子邮件 |

#### 4.2 作业创建步骤

**Step 1: 新建作业**
1. 打开Spoon，点击"文件" → "新建" → "作业"
2. 在画布空白处右键，选择"作业项"添加需要的组件

**Step 2: 配置通用选项**
```
作业设置 → 常规：
- 作业名称：自定义名称
- 目录：保存在指定目录
- 描述：作业说明
```

**Step 3: 添加作业项**
以"定时数据同步作业"为例：
```
[Start]
  ↓
[转换_数据抽取] → [转换_数据转换] → [转换_数据加载]
  ↓
[成功] / [失败]
```

**Step 4: 配置作业项属性**
每个作业项双击打开配置界面：
- 转换：选择要执行的.ktr文件
- 日志：配置日志级别和日志文件路径
- 错误处理：定义失败时的处理方式

#### 4.3 作业高级特性

**错误处理：**
```
[转换] --成功--> [下一步]
[转换] --失败--> [发送邮件] --> [失败]
```
- 勾选"执行每个输入行"
- 设置"失败时跳转"到错误处理流程

**并行执行：**
- 多个作业项连接到同一个目标时可以并行执行
- 适用于独立的任务

**循环执行：**
```java
// 使用JavaScript作业项实现循环
var maxLoops = 5;
for (var i = 0; i < maxLoops; i++) {
    setVariable('loop_count', i, 's');
    // 调用子作业或转换
}
```

---

### 转换创建

转换（Transformation）是Kettle中进行数据处理的核心组件，负责数据的抽取、转换和加载。

#### 4.4 转换基本结构

**转换组成元素：**
- **步骤（Step）**：转换中的最小处理单元
- **跳（Hop）**：步骤之间的数据流

**步骤分类：**
| 分类 | 常用步骤 |
|------|----------|
| 输入 | 表输入、文本文件输入、JSON输入、Excel输入 |
| 输出 | 表输出、文本文件输出、Excel输出 |
| 转换 | 字段选择、值映射、字符串操作、计算器 |
| 映射 | 映射输入规范、映射输出规范 |
| 脚本 | JavaScript代码、Java代码 |
|  Lookup | 数据库查询、流查询、合并查询 |
|  Join | 记录关联、合并记录 |
|  排序 | 排序记录 |
|  验证 | 检查数据完整性 |

#### 4.5 转换创建步骤

**Step 1: 新建转换**
1. 打开Spoon，点击"文件" → "新建" → "转换"
2. 在左侧"核心对象"面板中选择需要的步骤

**Step 2: 配置数据源**
以"表输入"为例：
```
步骤名称：表输入
数据库连接：选择已配置的数据源
SQL：
SELECT
    id,
    name,
    status,
    created_at
FROM source_table
WHERE created_at >= '${START_DATE}'
ORDER BY id
```

**Step 3: 数据转换**
根据业务需求添加转换步骤：
- 字段选择：选择需要的字段
- 值映射：转换状态码为描述
- 计算器：新增计算字段

**Step 4: 配置数据目标**
以"表输出"为例：
```
步骤名称：表输出
目标表：target_table
提交数量：1000
批量操作：勾选
```

**Step 5: 连接步骤**
拖拽步骤之间的连接线建立数据流：
- 正常数据流：黑色实线
- 错误数据流：红色线

#### 4.6 转换执行与调试

**预览功能：**
- 右键步骤 → "预览"
- 查看数据处理结果
- 用于调试转换逻辑

**执行监控：**
- 转换执行时显示进度
- 记录读取/写入/更新数量
- 显示处理速度和预估完成时间

---

### 参数配置

Kettle支持三种类型的参数，用于在不同组件之间传递数据和配置。

#### 4.7 参数类型

| 类型 | 说明 | 引用方式 | 作用范围 |
|------|------|----------|----------|
| 系统参数 | 环境变量、JVM参数 | ${PARAM_NAME} | 全局 |
| 转换参数 | 转换内部变量 | ${PARAM_NAME} | 转换内 |
| 作业参数 | 作业内部变量 | ${PARAM_NAME} | 作业内 |

#### 4.8 参数配置步骤

**Step 1: 在作业中设置参数**
1. 打开作业，双击空白处打开"作业设置"
2. 切换到"参数"标签
3. 点击"获取参数"自动加载子转换的参数
4. 手动添加自定义参数：
```
参数名称          | 默认值              | 描述
-----------------|---------------------|------------------
START_DATE       | ${PreviousDay}      | 开始日期
END_DATE         | ${CurrentDay}       | 结束日期
BATCH_SIZE       | 1000                | 批次大小
THREADS          | 4                   | 并行线程数
```

**Step 2: 在转换中使用参数**

**方式一：使用占位符（推荐用于SQL）**
```sql
-- 表输入中的SQL
SELECT * FROM orders
WHERE order_date BETWEEN ? AND ?
AND status = ?
```
- 依次在"参数"标签中配置：
  - START_DATE
  - END_DATE
  - STATUS

**方式二：直接引用变量**
```javascript
// JavaScript代码中
var startDate = getVariable('START_DATE', '');
var endDate = getVariable('END_DATE', '');
var batchSize = parseInt(getVariable('BATCH_SIZE', '1000'));
```

**Step 3: 参数传递**

**作业到转换的参数传递：**
```
作业设置 → 参数：
  param_name = param_value

转换中使用：
  ${param_name}
```

**转换之间的参数传递：**
1. 在转换A中使用"复制行到结果"
2. 在作业中设置"复制结果到变量"
3. 在转换B中使用"获取变量"

**Step 4: 参数的高级用法**

**动态参数（根据上一步结果）：**
```javascript
// JavaScript代码
var date = new Date();
var yesterday = new Date(date.getTime() - 24*60*60*1000);
var dateStr = yesterday.toISOString().split('T')[0];

setVariable('YESTERDAY', dateStr, 's');
```

**参数条件赋值：**
```
[如果值等于] 作业项：
  变量：ENV
  值：PROD
  → [设置变量] VALUE=product_db
  → [设置变量] MAX_ROWS=100000
```

---

### 4.6 实战案例

#### 案例一：订单数据同步

**需求：** 每天凌晨2点将业务系统的订单数据同步到数据仓库

**解决方案：**

**1. 作业结构：**
```
[Start] → [检查表是否存在] → [转换_全量同步] → [成功]
                        ↓ (表不存在)
                   [转换_增量同步] → [成功]
```

**2. 转换_增量同步 - 配置：**
```
步骤：表输入
SQL：
SELECT
    order_id,
    customer_id,
    order_amount,
    order_status,
    create_time,
    update_time
FROM orders
WHERE create_time >= '${LAST_SYNC_TIME}'
ORDER BY create_time

步骤：字段选择
保留字段：order_id, customer_id, order_amount, order_status

步骤：值映射
源值 → 目标值：
  0 → 待付款
  1 → 已付款
  2 → 已发货
  3 → 已完成
  4 → 已取消

步骤：表输出
目标表：dw_orders
```

**3. 作业参数配置：**
```
参数：
  LAST_SYNC_TIME = ${PreviousDay} 00:00:00
  CURRENT_DATE = ${CurrentDate}
```

**4. 定时调度：**
使用系统的cron或Kettle的Kitch执行：
```bash
# Linux crontab
0 2 * * * /opt/kettle/kitchen.sh -file=/jobs/order_sync.kjb -level=Basic
```

---

#### 案例二：用户行为日志处理

**需求：** 实时处理用户点击流日志，提取关键指标

**解决方案：**

**1. 日志格式：**
```
timestamp|user_id|action|page_id|duration
2024-03-07 10:00:00|1001|click|page_001|5
2024-03-07 10:00:01|1001|browse|page_002|30
```

**2. 转换结构：**
```
[文本文件输入]
  ↓
[字符串操作] - 分割字段
  ↓
[过滤记录] - 过滤有效记录
  ↓
[JavaScript] - 数据清洗和计算
  ↓
[插入更新] - 写入目标表
```

**3. 详细配置：**

**文本文件输入：**
```
文件名：/data/click_log_*.log
分隔符：|
头部行数：0
字段：
  1: timestamp - String
  2: user_id - Integer
  3: action - String
  4: page_id - String
  5: duration - Integer
```

**字符串操作：**
```
操作：分割字段到数组
源字段：line
分隔符：|
目标字段：field1,field2,field3,field4,field5
```

**JavaScript代码：**
```javascript
var action = field3;
var duration = parseInt(field5);

// 计算页面停留等级
var stayLevel = "短";
if (duration > 60) stayLevel = "长";
else if (duration > 30) stayLevel = "中";

// 计算行为得分
var score = 0;
switch(action) {
    case "click": score = 1; break;
    case "browse": score = 2; break;
    case "favor": score = 3; break;
    case "cart": score = 5; break;
    case "buy": score = 10; break;
}

var result = [];
result["log_time"] = field1;
result["user_id"] = field2;
result["action"] = action;
result["page_id"] = field4;
result["duration"] = duration;
result["stay_level"] = stayLevel;
result["action_score"] = score;

putRow(result);
```

**插入更新：**
```
目标表：user_behavior_summary
关键字段：user_id, log_date
更新字段：page_views, total_duration, total_score
```

---

#### 案例三：多数据源数据合并

**需求：** 将MySQL、Oracle、PostgreSQL三个数据库的用户数据合并去重后写入数据仓库

**解决方案：**

**1. 作业结构：**
```
[Start]
  ↓
[转换_获取MySQL数据] ──┐
[转换_获取Oracle数据] ──┼──> [转换_数据合并去重] ──> [转换_写入仓库] ──> [成功]
[转换_获取PG数据]    ──┘
```

**2. 转换_获取MySQL数据：**
```
步骤：表输入
数据库连接：MySQL_Prod
SQL：
SELECT
    user_id,
    user_name,
    phone,
    email,
    'mysql' as source
FROM mysql_users
WHERE status = 1
```

**3. 转换_获取Oracle数据：**
```
步骤：表输入
数据库连接：Oracle_ERP
SQL：
SELECT
    user_id,
    user_name,
    phone,
    email,
    'oracle' as source
FROM oracle_users
WHERE status = 'ACTIVE'
```

**4. 转换_数据合并去重：**
```
[合并记录]
  标志字段：flagfield
  旧数据源：第一来源（MySQL）
  新数据源：第二来源（Oracle）

  ↓

[过滤记录]
  条件：flagfield = "new"
  传送真实记录：true
  传送标记记录：false

  ↓

[排序记录]
  排序字段：user_id, phone

  ↓

[唯一记录]
  关键字：user_id, phone
```

**5. JavaScript去重脚本：**
```javascript
// 更灵活的去重逻辑
var users = {};
var uniqueUsers = [];

for each (row in input) {
    var key = row.user_id + "_" + row.phone;

    if (!users[key]) {
        users[key] = true;

        // 优先保留数据更完整的记录
        if (row.email && row.phone) {
            uniqueUsers.push(row);
        }
    } else {
        // 处理重复：保留更新时间最近的
        var existing = getVariable("existing_" + key, null);
        if (existing && row.update_time > existing.update_time) {
            // 替换
            uniqueUsers = uniqueUsers.filter(u => u.user_id !== row.user_id);
            uniqueUsers.push(row);
        }
    }
}

for each (u in uniqueUsers) {
    putRow(u);
}
```

**6. 写入数据仓库：**
```
步骤：表输出
目标表：dw_users
模式：插入/更新
关键字段：user_id
```

---

#### 案例四：实时数据清洗与质量检查

**需求：** 对订单数据进行清洗和质量检查，输出合格数据并记录异常

**解决方案：**

**1. 转换结构：**
```
[表输入_原始订单]
  ↓
[JavaScript_数据清洗]
  ↓
[数据质量检查]
  ├─ 合格 → [表输出_清洗后数据]
  └─ 不合格 → [表输出_异常数据] → [发送邮件]
```

**2. JavaScript_数据清洗：**
```javascript
var orderNo = order_no;
var amount = parseFloat(order_amount);
var userName = user_name;
var phone = user_phone;

// 1. 订单号清洗
orderNo = orderNo.trim().toUpperCase();

// 2. 金额清洗
if (isNaN(amount) || amount <= 0) {
    amount = 0;
}

// 3. 用户名清洗
userName = userName ? userName.trim() : "未知用户";

// 4. 手机号清洗
phone = phone.replace(/[^\d]/g, "");
if (phone.length === 11) {
    phone = phone.substring(0, 3) + "****" + phone.substring(7);
}

// 5. 数据验证标记
var isValid = true;
var errorMsg = [];

if (!orderNo || orderNo.length < 10) {
    isValid = false;
    errorMsg.push("订单号格式错误");
}
if (amount <= 0 || amount > 1000000) {
    isValid = false;
    errorMsg.push("金额异常");
}
if (!userName || userName === "未知用户") {
    isValid = false;
    errorMsg.push("用户名缺失");
}

var result = [];
result["order_no"] = orderNo;
result["amount"] = amount;
result["user_name"] = userName;
result["phone"] = phone;
result["is_valid"] = isValid;
result["error_msg"] = errorMsg.join(";");

putRow(result);
```

**3. 过滤记录步骤：**
```
条件：is_valid = true（布尔型，true/false）
```

**4. 异常数据输出：**
```
步骤：表输出
目标表：order_exception
包含所有字段：true
```

**5. 邮件通知：**
```
作业项：发送邮件
收件人：data-team@example.com
主题：数据质量异常报告
正文：
  异常订单数：${ERROR_COUNT}
  异常时间：${CURRENT_DATE}
  请登录系统查看详细异常数据
```

---

### 循环处理

Kettle支持两种主要的循环实现方式，用于处理需要重复执行的业务场景。

**方式一：设置变量** + Filter rows + Copy rows to result

这种方式是Kettle中最常用的循环实现方式，通过"复制行到结果"在转换内部传递数据，在作业中通过遍历结果实现循环。

**实现步骤：**

1. **表输入**：查询需要循环的数据
```sql
SELECT id, name, status FROM source_table WHERE status = 'PENDING'
```

2. **设置变量**：将查询结果中的字段设置为变量
   - 字段名：id, name
   - 变量名：loop_id, loop_name
   - 变量类型：指定字段类型

3. **复制行到结果**：将当前行的数据复制到结果集

4. **作业中循环**：
   - 使用"检查表是否存在"或"获取表行数"作为循环条件
   - 使用"复制结果到变量"步骤获取上一转换的结果
   - 使用"如果值等于"判断是否继续循环
   - 配合"ABORT"作业项在达到条件时终止循环

**示例作业流程：**
```
[Start] → [表输入_获取数据] → [设置变量] → [复制行到结果]
                                      ↓
                              [检查表是否存在] ← (循环条件)
                                      ↓
                              [如果值等于] → [转换_处理数据]
                                      ↓
                              [成功] → [ABORT]
```

#### 方式二：JavaScript代码 + 循环文件夹

使用JavaScript脚本实现更灵活的循环控制。

**实现步骤：**

1. **表输入**：获取需要循环的数据源

2. **JavaScript代码**：编写循环逻辑
```javascript
// 获取前一步的输入行
var input_row = row;

// 模拟循环计数器
var total = 5; // 循环5次
for (var i = 0; i < total; i++) {
    // 设置循环变量
    setVariable('loop_index', i.toString(), 's');
    setVariable('loop_total', total.toString(), 's');

    // 复制当前行到结果（用于下一次转换使用）
    copyToResult(row);

    // 输出日志
    print('第 ' + (i+1) + ' 次循环');
}
```

3. **循环文件夹**（作业中）：
   - 在作业中使用"循环文件"作业项
   - 配置源文件夹、文件通配符
   - 设置循环变量（文件名、完整路径等）

**JavaScript完整示例：**
```javascript
// 完整循环处理脚本
var rows = [];
var sourceData = [];

// 假设输入有 id, name, value 三个字段
var id = row.getInteger('id');
var name = row.getString('name');
var value = row.getNumber('value');

// 模拟数据处理
for (var i = 0; i < value; i++) {
    var newRow = createRow();
    newRow.setValue('id', id);
    newRow.setValue('loop_index', i);
    newRow.setValue('result', name + '_' + i);
    rows.add(newRow);
}

// 输出所有行
putRows(rows);
```

---

### 脚本编写

Kettle支持多种脚本类型，用于实现复杂的数据处理逻辑。

### SQL脚本

SQL脚本主要用于在"表输入"、"表输出"、"更新"、"插入/更新"等步骤中执行数据库操作。

#### 1. 表输入 - 基础查询
```sql
-- 基础数据查询
SELECT
    id,
    user_name,
    email,
    created_at,
    status
FROM users
WHERE created_at >= '${START_DATE}'
  AND created_at < '${END_DATE}'
ORDER BY created_at DESC
```

#### 2. 表输入 - 参数化查询（使用占位符）
```sql
-- 使用问号占位符，参数按顺序传递
SELECT
    a.id,
    a.order_no,
    b.product_name,
    b.quantity,
    b.price,
    a.total_amount,
    a.order_status,
    a.create_time
FROM orders a
LEFT JOIN order_items b ON a.id = b.order_id
WHERE a.create_time BETWEEN ? AND ?
  AND a.order_status = ?
ORDER BY a.create_time DESC
```
**参数配置：**
- 第1个参数：START_DATE（日期/时间）
- 第2个参数：END_DATE（日期/时间）
- 第3个参数：ORDER_STATUS（字符串）

#### 3. 表输入 - 动态SQL（exec）
```sql
-- 执行动态SQL，适用于跨数据库查询
SELECT * FROM (
    ${SQL_QUERY}
) t
WHERE 1=1
```

#### 4. 高级SQL - 窗口函数
```sql
-- 使用窗口函数进行数据排名
SELECT
    user_id,
    order_date,
    amount,
    RANK() OVER (PARTITION BY user_id ORDER BY order_date DESC) as rnk,
    SUM(amount) OVER (PARTITION BY user_id) as total_amount,
    AVG(amount) OVER (PARTITION BY user_id) as avg_amount
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
```

#### 5. 存储过程调用
```sql
-- 调用存储过程
CALL sp_calculate_summary(?, ?, ?);
```

---

### Java脚本

Java脚本使用"Java代码"步骤，可以在转换中执行自定义的Java代码逻辑。

#### 1. 基础Java代码 - 字符串处理
```java
// 获取输入字段
String inputName = getInputRowMeta().getString(row, "name", "");
String inputEmail = getInputRowMeta().getString(row, "email", "");

// 处理逻辑
String processedName = inputName.trim().toUpperCase();
String domain = inputEmail.contains("@") ?
    inputEmail.substring(inputEmail.indexOf("@") + 1) : "";

// 判断逻辑
boolean isVIP = inputName.startsWith("VIP") || inputName.startsWith("SVIP");

// 设置输出字段
Object[] outputRow = createRow(getInputRowMeta().size() + 3);
RowMetaInterface outputRowMeta = getInputRowMeta().clone();

// 添加新字段到输出元数据
outputRowMeta.addValueMeta(new ValueMetaString("processed_name"));
outputRowMeta.addValueMeta(new ValueMetaString("email_domain"));
outputRowMeta.addValueMeta(new ValueMetaBoolean("is_vip"));

// 设置输出值
outputRow[getInputRowMeta().size()] = processedName;
outputRow[getInputRowMeta().size() + 1] = domain;
outputRow[getInputRowMeta().size() + 2] = isVIP;

putRow(outputRowMeta, outputRow);
```

#### 2. Java代码 - 数据类型转换
```java
// 获取输入字段
Long id = getInputRowMeta().getInteger(row, "id", null);
String amountStr = getInputRowMeta().getString(row, "amount", "0");
String dateStr = getInputRowMeta().getString(row, "date", "");

// 类型转换
BigDecimal amount = new BigDecimal(amountStr);
LocalDate date = LocalDate.parse(dateStr, DateTimeFormatter.ISO_LOCAL_DATE);

// 计算
BigDecimal tax = amount.multiply(new BigDecimal("0.06"));
BigDecimal total = amount.add(tax);

// 设置输出
Object[] outputRow = createRow(getInputRowMeta().size() + 3);
outputRow[getInputRowMeta().size()] = amount;
outputRow[getInputRowMeta().size() + 1] = tax;
outputRow[getInputRowMeta().size() + 2] = total;

putRow(rowMeta, outputRow);
```

#### 3. Java代码 - 外部API调用
```java
// 简单的HTTP API调用示例
String userId = getInputRowMeta().getString(row, "user_id", "");

// 构建请求
String url = "https://api.example.com/users/" + userId;
HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
conn.setRequestMethod("GET");
conn.setConnectTimeout(5000);
conn.setReadTimeout(5000);

// 读取响应
BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
StringBuilder response = new StringBuilder();
String line;
while ((line = br.readLine()) != null) {
    response.append(line);
}
br.close();

// 解析JSON（简化）
String responseBody = response.toString();
String userName = extractJsonValue(responseBody, "name");

// 输出结果
Object[] outputRow = createRow(getInputRowMeta().size() + 1);
outputRow[getInputRowMeta().size()] = userName;
putRow(rowMeta, outputRow);

// 辅助方法
private String extractJsonValue(String json, String key) {
    Pattern pattern = Pattern.compile("\"" + key + "\"\\s*:\\s*\"([^\"]*)\"");
    Matcher matcher = pattern.matcher(json);
    return matcher.find() ? matcher.group(1) : "";
}
```

#### 4. Java代码 - 文件操作
```java
// 读取文件内容
String filePath = getInputRowMeta().getString(row, "file_path", "");

try {
    String content = new String(Files.readAllBytes(Paths.get(filePath)));
    int lineCount = content.split("\n").length;

    Object[] outputRow = createRow(getInputRowMeta().size() + 2);
    outputRow[getInputRowMeta().size()] = content;
    outputRow[getInputRowMeta().size() + 1] = lineCount;
    putRow(rowMeta, outputRow);
} catch (Exception e) {
    // 错误处理
    logError("读取文件失败: " + filePath + " - " + e.getMessage());
}
```

---

### JavaScript脚本

JavaScript（JavaScript代码步骤）用于更灵活的数据转换逻辑。

#### 1. 基础JavaScript - 字段计算
```javascript
// 获取输入字段值
var orderId = id;
var quantity = parseInt(quantity);
var unitPrice = parseFloat(price);

// 计算
var subtotal = quantity * unitPrice;
var discount = 0;
if (quantity >= 100) {
    discount = subtotal * 0.15;
} else if (quantity >= 50) {
    discount = subtotal * 0.10;
}
var total = subtotal - discount;
var tax = total * 0.06;

// 设置输出字段
var result_row = [];
result_row["order_id"] = orderId;
result_row["subtotal"] = subtotal;
result_row["discount"] = discount;
result_row["total"] = total;
result_row["tax"] = tax;

// 输出行
putRow(result_row);
```

#### 2. JavaScript - 字符串处理
```javascript
// 字符串处理示例
var phone = "13812345678";

// 格式化手机号
var formattedPhone = phone.replace(/(\d{3})(\d{4})(\d{4})/, "$1 $2 $3");

// 脱敏处理
var maskedPhone = phone.substring(0, 3) + "****" + phone.substring(7);

// 邮箱处理
var email = "USER@Example.COM";
var emailLower = email.toLowerCase();
var emailDomain = email.split("@")[1];

// 生成唯一标识
var uuid = java.util.UUID.randomUUID().toString();

// 输出
var out = [];
out["original_phone"] = phone;
out["formatted_phone"] = formattedPhone;
out["masked_phone"] = maskedPhone;
out["email"] = emailLower;
out["domain"] = emailDomain;
out["uuid"] = uuid;

putRow(out);
```

#### 3. JavaScript - 数组和JSON处理
```javascript
// JSON解析
var jsonStr = '{"name":"张三","age":30,"skills":["Java","Python","Kettle"]}';
var jsonObj = JSON.parse(jsonStr);

var name = jsonObj.name;
var skills = jsonObj.skills;
var skillCount = skills.length;

// 数组处理
var total = 0;
var items = [100, 200, 300, 400, 500];

for (var i = 0; i < items.length; i++) {
    total += items[i];
}

var avg = total / items.length;

// 构造JSON
var response = {
    "status": "success",
    "data": {
        "items": items,
        "total": total,
        "avg": avg
    }
};

var responseJson = JSON.stringify(response);

// 输出
var out = [];
out["name"] = name;
out["skill_count"] = skillCount;
out["total"] = total;
out["average"] = avg;
out["response_json"] = responseJson;

putRow(out);
```

#### 4. JavaScript - 日期时间处理
```javascript
// 日期处理
var now = new Date();
var timestamp = now.getTime();

// 格式化日期
var dateStr = now.getFullYear() + "-" +
    String(now.getMonth() + 1).padStart(2, "0") + "-" +
    String(now.getDate()).padStart(2, "0");

var timeStr = String(now.getHours()).padStart(2, "0") + ":" +
    String(now.getMinutes()).padStart(2, "0") + ":" +
    String(now.getSeconds()).padStart(2, "0");

// 日期计算
var yesterday = new Date(now);
yesterday.setDate(yesterday.getDate() - 1);

var nextMonth = new Date(now);
nextMonth.setMonth(nextMonth.getMonth() + 1);

// 获取日期差
var startDate = new Date("2024-01-01");
var diffDays = Math.floor((now - startDate) / (1000 * 60 * 60 * 24));

// 输出
var out = [];
out["timestamp"] = timestamp;
out["date"] = dateStr;
out["time"] = timeStr;
out["yesterday"] = yesterday.toISOString().split("T")[0];
out["next_month"] = nextMonth.toISOString().split("T")[0];
out["diff_days"] = diffDays;

putRow(out);
```

#### 5. JavaScript - 条件判断和分支
```javascript
// 会员等级计算
var points = parseInt(points);
var level = "";
var discount = 0;

if (points < 1000) {
    level = "普通会员";
    discount = 0.00;
} else if (points < 5000) {
    level = "银卡会员";
    discount = 0.05;
} else if (points < 20000) {
    level = "金卡会员";
    discount = 0.10;
} else if (points < 50000) {
    level = "白金会员";
    discount = 0.15;
} else {
    level = "黑金会员";
    discount = 0.20;
}

// 状态转换
var statusCode = status;
var statusDesc = "";

switch(statusCode) {
    case "0":
        statusDesc = "待处理";
        break;
    case "1":
        statusDesc = "处理中";
        break;
    case "2":
        statusDesc = "已完成";
        break;
    case "3":
        statusDesc = "已取消";
        break;
    default:
        statusDesc = "未知状态";
}

// 输出
var out = [];
out["points"] = points;
out["level"] = level;
out["discount"] = discount;
out["status_code"] = statusCode;
out["status_desc"] = statusDesc;

putRow(out);
```

## 5.调优

Kettle的性能调优是ETL项目中非常重要的一环，合理的配置可以显著提升数据处理效率。以下从数据库连接、转换配置、JVM参数等多个维度进行说明。

### 5.1 数据库连接调优

#### 输入优化（数据读取）

在"表输入"步骤的数据库连接中，添加以下参数：

```
(1) 预处理语句优化
useServerPrepStmts：true
cachePrepStmts：true

(2) 读取缓存配置
defaultFetchSize：10000
useCursorFetch：true

(3) 通信压缩
useCompression：true
```

**参数说明：**
- `useServerPrepStmts=true`：启用服务器端预处理语句，减少SQL编译开销
- `cachePrepStmts=true`：缓存预处理语句，复用执行计划
- `defaultFetchSize=10000`：设置合适的fetch size，平衡内存使用和网络往返
- `useCursorFetch=true`：启用游标方式读取，适合大数据量
- `useCompression=true`：启用压缩，减少网络传输量

#### 输出优化（数据写入）

在"表输出"步骤的数据库连接中，添加以下参数：

```
(1) 读取配置
defaultFetchSize：5000

(2) 批量写入优化
rewriteBatchedStatements：true
useServerPrepStmts：false
useCursorFetch：true

(3) 通信压缩
useCompression：true
```

**参数说明：**
- `rewriteBatchedStatements=true`：将多条INSERT合并为一条批量INSERT
- `useServerPrepStmts=false`：客户端预处理，对批量写入更高效

**效果对比：**

| 场景 | 调优前 | 调优后 | 提升倍数 |
|------|--------|--------|----------|
| 10万条数据写入 | ~120秒 | ~8秒 | 15倍 |
| 100万条数据写入 | ~20分钟 | ~1.5分钟 | 13倍 |

### 5.2 转换级别调优

**1. 提交数量设置**
- 在"表输出"步骤中设置提交数量：1000-5000

**2. 记录缓存**
- 在"排序记录"等步骤中设置缓存大小：100000

**3. 并行处理**
- 在"分区"步骤中配置分区数：4-8（根据CPU核心数）

### 5.3 JVM参数调优

修改`spoon.sh`或`kitchen.sh`中的JVM参数：

```bash
# 编辑Kettle启动脚本
export PENTAHO_DI_JAVA_OPTIONS="-Xmx4096m -Xms1024m"

# 参数说明：
# -Xmx4096m：最大堆内存4GB
# -Xms1024m：初始堆内存1GB
# -XX:+UseG1GC：使用G1垃圾收集器
```

**推荐配置（8GB内存机器）：**
```
-Xmx6144m -Xms2048m -XX:+UseG1GC -XX:MaxGCPauseMillis=200
```

### 5.4 调优最佳实践

1. **先优化SQL**：确保源数据SQL有合适的索引
2. **批量处理**：大数据量分批处理，避免OOM
3. **合理并行**：根据CPU核心数和数据库连接池配置并行度
4. **监控分析**：使用Spoon的预览和日志功能定位瓶颈

## 6.Java调用
```
import org.pentaho.di.job.Job;
import org.pentaho.di.job.JobMeta;

public class kjbTest {
    public static void main(String[] args) {

        if (!KettleEnvironment.isInitialized()) {
            KettleEnvironment.init();
        }

        String kjbPath = "/***/test.kjb";
        JobMeta jobMeta = new JobMeta(kjbPath, null);
        jobMeta.setParameterValue("parameNmae", "parameValue");

        Job job = new Job(null, jobMeta);
        job.setLogLevel(LogLevel.DETAILED);
        job.start();
        job.waitUntilFinished();
        if (job.getErrors() > 0) {
            throw new Exception("Kettle job 数据同步异常.");
        }
    }
}


import org.pentaho.di.trans.Trans;
import org.pentaho.di.trans.TransMeta;

public class ktrTest {
    public static void main(String[] args) {

        if (!KettleEnvironment.isInitialized()) {
            KettleEnvironment.init();
        }

        String kjbPath = "/***/test.ktr";
        TransMeta transMeta = new TransMeta(ktrPath);
        transMeta.setParameterValue("parameNmae", "parameValue");
        this.initTransName(transMeta);
        Trans trans = new Trans(transMeta);
        trans.cleanup();
        trans.setLogLevel(LogLevel.DETAILED);
        trans.execute(null);
        trans.waitUntilFinished();
        if (trans.getErrors() > 0) {
            throw new Exception("Kettle 数据同步异常.");
        }
    }
}
```
