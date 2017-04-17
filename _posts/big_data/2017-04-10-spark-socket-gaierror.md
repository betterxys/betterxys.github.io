---
layout: post
title: Spark无法启动之socket.gaierror
date: 2017-04-11
author: xiaoyongsheng
categories: spark LittleBitch
tag: spark 

---

* content
{: toc}

## 1. 背景介绍  

Hadoop平台基础建设摸索暂时告一段落，本文的目标是解决Spark无法启动的问题，具体情况如下：  

```shell
[hadoop@NN-SPK-3 spark-1.5.2]$ pyspark
Python 3.5.0 (default, Apr  6 2017, 16:01:44) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-17)] on linux
Type "help", "copyright", "credits" or "license" for more information.
17/04/11 09:07:33 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
17/04/11 09:07:35 WARN MetricsSystem: Using default name DAGScheduler for source because spark.app.id is not set.
Traceback (most recent call last):
  File "/usr/spark/spark-1.5.2/python/pyspark/shell.py", line 43, in <module>
    sc = SparkContext(pyFiles=add_files)
  File "/usr/spark/spark-1.5.2/python/pyspark/context.py", line 113, in __init__
    conf, jsc, profiler_cls)
  File "/usr/spark/spark-1.5.2/python/pyspark/context.py", line 174, in _do_init
    self._accumulatorServer = accumulators._start_update_server()
  File "/usr/spark/spark-1.5.2/python/pyspark/accumulators.py", line 259, in _start_update_server
    server = AccumulatorServer(("localhost", 0), _UpdateRequestHandler)
  File "/home/hadoop/.pyenv/versions/3.5.0/lib/python3.5/socketserver.py", line 443, in __init__
    self.server_bind()
  File "/home/hadoop/.pyenv/versions/3.5.0/lib/python3.5/socketserver.py", line 457, in server_bind
    self.socket.bind(self.server_address)
socket.gaierror: [Errno -2] Name or service not known
```

## 2. 问题分析  

根据日志反馈来看，应该是在运行`sc = SparkContext(pyFiles=add_files)`这段代码时出现了问题，SparkContext无法初始化，原因好像是某个ip的配置信息出现了问题？  
所以还是需要回过头来再琢磨琢磨Spark分布式集群的配置方法，这部分补充到[《Spark配置解析》](https://betterxys.github.io/2017/04/01/spark-setup/)一文当中

## 3. 解决问题  

参考博客[《Spark集群启动python shell错误： Could not resolve hostname localhost: Temporary failure》](http://www.voidcn.com/blog/gamer_gyt/article/p-6128589.html)  

其实很简单，是socketserver的问题，也就是ssh通信问题，尝试:  

```shell
[hadoop@NN-SPK-3 spark-1.5.2]$ ssh localhost
ssh: Could not resolve hostname localhost: Name or service not known
```

那么修改/etc/hosts文件：  

```shell
[root@NN-SPK-3 spark-1.5.2]# vi /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 NN-SPK-3
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6 NN-SPK-3

192.168.6.231 NN-SPK-1
192.168.6.232 NN-SPK-2
192.168.6.233 NN-SPK-3
192.168.6.234 HDP-DN-1
192.168.6.235 HDP-DN-2
192.168.6.236 HDP-DN-3
```

之前出现问题是因为笔者在部署Hadoop时猪油蒙了心，将前两行注释掉了；  

那么现在：  

```shell
[root@NN-SPK-3 spark-1.5.2]# pyspark
Python 2.6.6 (r266:84292, Feb 22 2013, 00:00:18) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-3)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
17/04/11 13:44:56 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
17/04/11 13:44:57 WARN Utils: Your hostname, NN-SPK-3 resolves to a loopback address: 127.0.0.1; using 192.168.6.233 instead (on interface eth0)
17/04/11 13:44:57 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
17/04/11 13:44:58 WARN MetricsSystem: Using default name DAGScheduler for source because spark.app.id is not set.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 1.5.2
      /_/

Using Python version 2.6.6 (r266:84292, Feb 22 2013 00:00:18)
SparkContext available as sc, HiveContext available as sqlContext.
```
![spark-cluster](http://i.imgur.com/zUQx6Rm.png)

---
## 参考文献  
1. Spark集群启动python shell错误： Could not resolve hostname localhost: Temporary failure:http://www.voidcn.com/blog/gamer_gyt/article/p-6128589.html  

