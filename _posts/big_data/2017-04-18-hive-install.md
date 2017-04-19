---
layout: post
title: Hive+mysql安装教程
date: 2017-04-18
author: xiaoyongsheng
categories: Hive
tag: spark 

---

* content
{: toc}

## 1. 背景介绍  

Hadoop和Spark平台的搭建基本已经完成，本文需要解决的是Hive+Mysql环境的搭建，首先重新解释以下集群配置信息：  

机器名称| ip| 主要作用 |逻辑cpu个数|内存|存储空间  
   ---  |---|    ---    |    ---    |--- |  --- 
nn-spk-1  | 192.168.6.231 | NameNode(standby) | 8   | 9G | -  
nn-spk-2  | 192.168.6.232 | NameNode(active) | 8   | 9G | -
nn-spk-3  | 192.168.6.233 | ResourceManager / Spark Master | 8   | 9G | -
hdp-dn-1  | 192.168.6.234 | DataNode / Spark worker | 4   | 6G | 90G  
hdp-dn-2  | 192.168.6.235 | DataNode / Spark worker | 4   | 6G | 90G
hdp-dn-3  | 192.168.6.236 | DataNode / Spark worker | 4   | 6G | 90G

本文参考了形形色色各类教程首先将Hive+Mysql部署在nn-spk-3，失败！而后部署在nn-spk-1，失败！本文决定将其部署于hdp-dn-1并详细记录中间每一步操作以作参考分析。

## 2. 官方教程  

历史经验表明学习一项新的技术最好最稳妥的方式当然是从其官方教程开始分析，尤其安装部署这部分，[官方文档](https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-InstallationandConfiguration)值得借鉴。

### 2.1. 环境依赖  

Hive1.2及以后版本需要Java1.7或以上版本；  
Hadoop2.x版本；  


### 2.2. 安装步骤  

1. 下载([官方镜像](https://hive.apache.org/downloads.html))并解压:  
  `tar -xzvf hive-x.y.z.tar.gz`  

2. 环境变量设置  

  ```
  export HIVE_HOME=<hive_install_dir>
  export PATH=$HIVE_HOME/bin:$PATH  
  export $HADOOP_HOME=<hadoop_install_dir>
  ```   

3. 建立相关文件夹(/tmp 和 hive.metastore.warehouse.dir:/user/hive/warehouse)并赋予相关权限  

  ```
  $ $HADOOP_HOME/bin/hadoop fs -mkdir       /tmp
  $ $HADOOP_HOME/bin/hadoop fs -mkdir       /user/hive/warehouse
  $ $HADOOP_HOME/bin/hadoop fs -chmod g+w   /tmp
  $ $HADOOP_HOME/bin/hadoop fs -chmod g+w   /user/hive/warehouse
  ```

### 2.3 初步尝试

按部就班，将官网给出的指示贯彻落实：

```
[hadoop@HDP-DN-1 hadoop-2.7.1]$ echo $HIVE_HOME
/usr/hive/apache-hive-2.1.1
[hadoop@HDP-DN-1 hadoop-2.7.1]$ echo $HADOOP_HOME
/usr/hadoop/hadoop-2.7.1/
[hadoop@HDP-DN-1 hadoop-2.7.1]$ echo $PATH
/usr/hive/apache-hive-2.1.1/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/java/jdk1.8.0_60/bin:/usr/scala/scala-2.10.4/bin:/root/bin:/usr/hadoop/hadoop-2.7.1//bin
[hadoop@HDP-DN-1 hadoop-2.7.1]$ hadoop fs -ls -R /
17/04/18 22:40:30 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
drwx-wx-wx   - hadoop supergroup          0 2017-04-14 16:04 /tmp
drwx-wx-wx   - hadoop supergroup          0 2017-04-14 16:04 /tmp/hive
drwx------   - hadoop supergroup          0 2017-04-14 16:04 /tmp/hive/hadoop
drwxr-xr-x   - hadoop supergroup          0 2017-04-14 14:28 /usr
drwxr-xr-x   - hadoop supergroup          0 2017-04-14 14:28 /usr/hive
drwxrwxr-x   - hadoop supergroup          0 2017-04-14 14:28 /usr/hive/warehouse
```

但是，在启动hive的命令行交互界面时出现如下问题：  

```
[hadoop@HDP-DN-1 hadoop-2.7.1]$ $HIVE_HOME/bin/hive
which: no hbase in (/usr/hive/apache-hive-2.1.1/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/java/jdk1.8.0_60/bin:/usr/scala/scala-2.10.4/bin:/root/bin:/usr/hadoop/hadoop-2.7.1//bin)
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/usr/hive/apache-hive-2.1.1/lib/log4j-slf4j-impl-2.4.1.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/hadoop/hadoop-2.7.1/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]

Logging initialized using configuration in jar:file:/usr/hive/apache-hive-2.1.1/lib/hive-common-2.1.1.jar!/hive-log4j2.properties Async: true

Exception in thread "main" java.lang.RuntimeException: org.apache.hadoop.hive.ql.metadata.HiveException: java.lang.RuntimeException: Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient

Caused by: org.apache.hadoop.hive.ql.metadata.HiveException: java.lang.RuntimeException: Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient
Caused by: java.lang.RuntimeException: Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient
Caused by: java.lang.reflect.InvocationTargetException
Caused by: MetaException(message:Version information not found in metastore. ) at org.apache.hadoop.hive.metastore.ObjectStore.checkSchema(ObjectStore.java:7753)

```

问题在这里：`Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient`


## 3. 解决问题  

### 3.1 HiveMetaStoreClient无法初始化  

本节目标是解决`Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient`的问题，邹中凡在其博客[《Hive常见问题汇总》](http://blog.csdn.net/freedomboy319/article/details/44828337)一文当中认为此类问题的出现是由于没有正常启动Hive的MetaStore Server服务进程导致的，并给出解决方法：  

  ```
  hive --server metastore & 
  ```

但本文在启动metastore服务时，出现新的错误：  

```
[hadoop@HDP-DN-1 hadoop-2.7.1]$ which: no hbase in (/usr/hive/apache-hive-2.1.1/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/java/jdk1.8.0_60/bin:/usr/scala/scala-2.10.4/bin:/root/bin:/usr/hadoop/hadoop-2.7.1//bin)
Starting Hive Metastore Server
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/usr/hive/apache-hive-2.1.1/lib/log4j-slf4j-impl-2.4.1.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/hadoop/hadoop-2.7.1/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]

MetaException(message:Version information not found in metastore. )

Exception in thread "main" MetaException(message:Version information not found in metastore. )

```

显然，新的问题出现了，在启动metaStore时`Version information not found in metastore.`


### 3.2 metastore的版本信息丢失  

- 本节目标  
 本节目标是解决metastore启动过程中出现的问题：`Version information not found in metastore.`  

- 问题出现原因  
 Apache Hive的pages当中有一篇[《Hive Schema Tool》](https://cwiki.apache.org/confluence/display/Hive/Hive+Schema+Tool)介绍了`Version information not found in metastore`问题出现的原因：  

  > Hive now records the schema version in the metastore database and verifies that the metastore schema version is compatible with Hive binaries that are going to accesss the metastore. Note that the Hive properties to implicitly create or alter the existing schema are disabled by default. Hive will not attempt to change the metastore schema implicitly. 
 
    简单来说就是因为metastore database和Hive binaries当中的schema version发生了冲突并且Hive并不去解决这个冲突！

- 思路整理  
 yongqj在其博客[《hive部署需要注意的几点以及Version information not found错误解决办法》](http://blog.csdn.net/youngqj/article/details/19987727)当中认为只需修改`conf/hive-site.xml`中的`hive.metastore.schema.verification`的值为`false`即可解决该问题；其实根本不用去尝试，姑且不说到底有没有实际效果，即便有效果也是治标不治本，出了问题应该去解决问题而不是跳过这个问题，所以此方法根本就不应考虑。  
 真正的解决方法如下：  
 [《Hive Schema Tool》](https://cwiki.apache.org/confluence/display/Hive/Hive+Schema+Tool)告介我们在hive安装之初，首先需要执行的是：`schematool -dbType derby -initSchema`，使用这条命令来初始化schema，初始化之后应该能够使用`schematool -dbType derby -info`查看schema信息，若显示无法获取版本信息，那就说明schema版本过低，需要进行更新操作，可以采用`schematool -dbType derby -upgradeSchemaFrom x.xx.x(当前版本号)`进行更新。  

但是本文的问题其实与上述描述的问题还是有些许区别的，本文问题是由于笔者在hive安装完成之后直接执行了bin/hive命令，该命令会自动生成一个metastore，该metastore与我们后来执行`schematool -dbType derby -initSchema`要生成的metastore产生了冲突，所以答案已经出来了。  

- 解决方案  
 若尚未执行过hive，则执行`schematool -dbType derby -initSchema`；  
 若已经执行过hive，则将已经存在的'metastore_db'删除，然后再执行`schematool -dbType derby -initSchema`；  
 此后就可以成功运行hive！


---
## 参考文献  

1. Apache Hive官方文档：https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-InstallationandConfiguration, 2017.04  
2. 邹中凡.Hive常见问题汇总: http://blog.csdn.net/freedomboy319/article/details/44828337, 2015.04  
3. yongqj.hive部署需要注意的几点以及Version information not found错误解决办法:http://blog.csdn.net/youngqj/article/details/19987727, 2014.02  
4. Prasad Mujumdar.Hive Schcema Tool:https://cwiki.apache.org/confluence/display/Hive/Hive+Schema+Tool, 2017.03  
5. Rebecca.Hive installation issues: Hive metastore database is not initialized
：http://stackoverflow.com/questions/35655306/hive-installation-issues-hive-metastore-database-is-not-initialized,2016.04  

