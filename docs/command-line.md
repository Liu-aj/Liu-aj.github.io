---
title: 命令行进阶
description: 命令行工具进阶指南
---

# 命令行进阶 ⌨️

> 提升命令行效率

---

## 文本处理

### awk
```bash
# 提取列
awk -F',' '{print $1, $3}' file.csv

# 条件过滤
awk 'NR>1 && $3>100 {print $0}' data.txt
```markdown

### sed
```bash
# 替换
sed -i 's/old/new/g' file.txt

# 删除行
sed -i '/pattern/d' file.txt
```

### grep
```bash
# 递归搜索
grep -r "pattern" .

# 高亮显示
grep --color=auto "pattern" file
```

## 管道组合

```bash
# 统计行数
cat file | wc -l

# 去重统计
cat access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -10
```bash

## 环境变量

```bash
# 查看
echo $PATH
env

# 设置
export VAR=value

# 永久写入 ~/.bashrc
echo 'export PATH=$PATH:/new/path' >> ~/.bashrc
```

---

*掌握命令行，效率翻倍*
