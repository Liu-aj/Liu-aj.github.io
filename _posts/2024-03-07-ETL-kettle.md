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

作业：

转换：

参数： 可分为“系统参数（环境变量）”、“程序参数（变量）”、“转换参数（上一步结果的字段）” 需注意，“系统参数”初始化（启动时/运行中首次赋值）后不支持变更，因此不可通过改变“系统参数”的方式进行数据传递； 获取参数时使用\${字段名}的方式获取，在“表输入”控件中，获取“转换参数”时使用占位符?方式获取；

循环： 方式一：

方式二：

脚本： sql：

java：

js：

调优： 1、在输入表的数据库中添加如下参数配置：
```
    (1)增加读的操作
    useServerPrepStmts：true
    cachePrepStmts：true
    (2)2.读取缓存，设置过高消耗内存也会高
    defaultFetchSize：10000
    useCursorFetch：true
    (3)3. 压缩数据传入，与mysql服务端进行通信时采用压缩
    useCompression:true
```
2、在输出表的数据库连接中添加如下参数配置
```
    (1)
    defaultFetchSize:5000
    (2)提高写的操作
    rewriteBatchedStatements:true
    useServerPrepStmts:false
    useCursorFetch:true
    (3)设置与mysql服务器通讯时压缩数据传入
    useCompression:true
```
调优前，表写入速度慢

调优后，写入速度显著提升

## 5.java调用
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
