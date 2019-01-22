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
val fp = "@file_path"

// read parquet
val df = spark.read.parquet(fp)

// read csv
val df = spark.read.format("csv").option("header", "true").load(fp)


//import spark context
import org.apache.hadoop.io._
import com.hadoop.mapreduce._
import org.apache.spark.sql.functions._

//hdfs lzo -> rdd -> dataframe
var rdd = sc.newAPIHadoopFile[LongWritable, Text, LzoTextInputFormat]("/esdata/lzo/vehicle_collection_info/20161230/*")       
df = spark.read.json(rdd.values.map(_.toString))   

//print rdd content
myRDD.take(n).foreach(println)

// create view
df.printSchema()
df.createOrReplaceTempView("tmp")
```

### 写

```scala
user_resume.repartition(1).write.format("csv").option("header", "true").save("/user/yongsheng.xiao/recommendation/data/data.csv)
```

### 查询

```scala
// select distinct rows
df.distinct.count()

// Select only the "name" column
df.select("name").show()
// +-------+
// |   name|
// +-------+
// |Michael|
// |   Andy|
// | Justin|
// +-------+
​
// Select everybody, but increment the age by 1
df.select($"name", $"age" + 1).show()
// +-------+---------+
// |   name|(age + 1)|
// +-------+---------+
// |Michael|     null|
// |   Andy|       31|
// | Justin|       20|
// +-------+---------+
​
// Select people older than 21
df.filter($"age" > 21).show()
// +---+----+
// |age|name|
// +---+----+
// | 30|Andy|
// +---+----+
​

// filter in array
ulti_df.filter($"singal_school".isin(cname:_*)).count()


// Count people by age
df.groupBy("age").count().show()
// +----+-----+
// | age|count|
// +----+-----+
// |  19|    1|
// |null|    1|
// |  30|    1|
// +----+-----+
​
// Register the DataFrame as a SQL temporary view
df.createOrReplaceTempView("people")
​
val sqlDF = spark.sql("SELECT * FROM people")
sqlDF.show()
// +----+-------+
// | age|   name|
// +----+-------+
// |null|Michael|
// |  30|   Andy|
// |  19| Justin|
// +----+-------+
​
// SQL can be run over a temporary view created using DataFrames
val results = spark.sql("SELECT name FROM people")
​
// The results of SQL queries are DataFrames and support all the normal RDD operations
// The columns of a row in the result can be accessed by field index or by field name
results.map(attributes => "Name: " + attributes(0)).show()
// +-------------+
// |        value|
// +-------------+
// |Name: Michael|
// |   Name: Andy|
// | Name: Justin|
// +-------------+
​
// In 1.3.x, in order for the grouping column "department" to show up,
// it must be included explicitly as part of the agg function call.
df.groupBy("department").agg($"department", max("age"), sum("expense"))
​
// In 1.4+, grouping column "department" is included automatically.
df.groupBy("department").agg(max("age"), sum("expense"))


// 通过指定字符拆分一行为多行
val multi_df = rst.withColumn("inner",split(col("address"),"、|,|，|;")).withColumn("mult",explode(col("inner")))

// 字符替换
import org.apache.spark.sql.functions.regexp_replace
val droplink_df = multi_df.withColumn("rst_loc", regexp_replace(col("mult"), ",| |-|/", "")).select("rst_loc").dropDuplicates()
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

### dataSet的去重合并

```scala
val a = df.select("address").dropDuplicates()
val b = df.select("expectLocation").dropDuplicates()
val c = df.select("resident").dropDuplicates()
val d = df.select("permanentResidence").dropDuplicates()

val rst = a.union(b).union(c).union(d)
```


---
## 参考文献  

1. Apache Hive官方文档：https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-InstallationandConfiguration, 2017.04  
2. 邹中凡.Hive常见问题汇总: http://blog.csdn.net/freedomboy319/article/details/44828337, 2015.04  
3. yongqj.hive部署需要注意的几点以及Version information not found错误解决办法:http://blog.csdn.net/youngqj/article/details/19987727, 2014.02  
4. Prasad Mujumdar.Hive Schcema Tool:https://cwiki.apache.org/confluence/display/Hive/Hive+Schema+Tool, 2017.03  
5. Rebecca.Hive installation issues: Hive metastore database is not initialized
：http://stackoverflow.com/questions/35655306/hive-installation-issues-hive-metastore-database-is-not-initialized,2016.04  
