---
layout: post
title: Spark basic
date: 2018-06-22
categories: Spark
tag: spark

---

* content
{: toc}

## 数据读写

### 读

```scala
fp = "@file_path"

// read parquet
val df = spark.read.parquet(fp)

// read csv
val df = spark.read.format("csv").option("header", "true").load(fp)

// create view
df.printSchema()
df.createOrReplaceTempView("tmp")
```

### 写

```scala
user_resume.repartition(1).write.format("csv").option("header", "true").save("/user/yongsheng.xiao/recommendation/data/data.csv)
```

### 从 HDFS 获取数据

```shell
hdfs dfs -get $file_path
```


## 数据类型

### RDD的交集、差集、并集

```scala
// init rdd, if not rdd, convert to rdd by .rdd
val rdd1 = sc.parallelize(List("a", "b","c"))
val rdd2 = sc.parallelize(List("e", "d","c"))

//operation
rdd1.union(rdd2).collect
rdd1.intersection(rdd2).collect
rdd1.subtract(rdd2).collect
```



---
## 参考文献  

1. Apache Hive官方文档：https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-InstallationandConfiguration, 2017.04  
2. 邹中凡.Hive常见问题汇总: http://blog.csdn.net/freedomboy319/article/details/44828337, 2015.04  
3. yongqj.hive部署需要注意的几点以及Version information not found错误解决办法:http://blog.csdn.net/youngqj/article/details/19987727, 2014.02  
4. Prasad Mujumdar.Hive Schcema Tool:https://cwiki.apache.org/confluence/display/Hive/Hive+Schema+Tool, 2017.03  
5. Rebecca.Hive installation issues: Hive metastore database is not initialized
：http://stackoverflow.com/questions/35655306/hive-installation-issues-hive-metastore-database-is-not-initialized,2016.04  
