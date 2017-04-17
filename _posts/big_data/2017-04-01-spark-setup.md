---
layout: post
title: Spark配置解析
date: 2017-04-01
author: xiaoyongsheng
categories: spark
tag: spark

---

* content
{: toc}

---

## 1. 背景介绍  

Spark<sup>[1]</sup>在Hadoop的HDFS和YARN之上构建，发展至今已经到了Spark 2.1.0, 内置组件包括：MLlib, Spark Streaming, 和 Graph X, 提供Java、Scala、Python和R接口，笔者是python用户，据说以后spark可以直接通过PyPI进行安装，那就真没谁了！

测试系统安装的是Spark-1.5.2


## 2. Spark 运行模式   

Spark现有的运行模式包括三种(2.1.0的官方文档如是说)：  

  - [Standalone](http://spark.apache.org/docs/2.1.0/spark-standalone.html)  

    Standalone模式<sup>[2,3]</sup>中，集群由master和workers组成，用户程序通过与Master节点交互来申请所需资源，workers负责具体Executor的启动运行；这种模式可以避免worker节点的单点故障问题，但同时导致了master的单点故障问题，为了解决master单点失败会出现的问题，Spark提供了两种解决方案；  

    - Standby Masters with ZooKeeper(*production-level high availability*)  

      利用ZooKeeper提供的leader election机制，可以同时拥有多个master节点，所有的master节点进行竞选选出一个节点作为leader，也就是真正的master，其余落选的节点都置为standby状态；一旦master挂掉了，其余的standby master立刻竞选出一个新的leader顶上，恢复到之前的状态。  

    - Single-Node Recovery with Local File System  

      简单粗暴的方法，master挂掉了，就重启！！！

  - Apache Mesos   

    Mesos负责资源调度，在资源调度过程中分为粗粒度和细粒度两种调度模式：  

      - Coarse-Grained(粗粒度资源调度)  

        每个Executor在获得系统资源后就长期持有，直到应用程序退出才释放资源；

      - Fine-Grained(细粒度资源调度)

        *从spark2.0开始已经弃用*，资源根据任务的需要动态调度，任务完成后立刻归还给mesos资源调度系统，调度开销和延迟较大；

  - Hadoop YARN  

    参考资料[2]当中对YARN描述了很多，YARN Client/cluster两种模式的逻辑结构框图以及具体内部原理都有解释，但是个人觉得还是[官方文档](http://spark.apache.org/docs/2.1.0/running-on-yarn.html)给的解释更加简洁清晰： 

      > There are two deploy modes that can be used to launch Spark applications on YARN. In cluster mode, the Spark driver runs inside an application master process which is managed by YARN on the cluster, and the client can go away after initiating the application. In client mode, the driver runs in the client process, and the application master is only used for requesting resources from YARN.

    YARN Cluster模式下，spark应用受YARN管辖，与客户端没有直接联系；而YARN client模式下spark应用是通过客户端进程运行，YARN此时仅负责底层资源调度；


## 3. Spark 基础概念

不论任何模式，Spark的工作流程基本类似: SparkContext是程序运行的总入口，在SparkContext的初始化过程中，Spark会分别创建 **DAGScheduler作业调度** 和 **TaskSchedule任务调度** 两级调度模块；

- RDD: Resilient Distributed DataSets, 弹性分布式数据集；

  - 一个RDD代表一个被分区的只读数据集；  

  - 仅有两种生成方式：内存或者外部文件、通过其他RDD转换而来；  

  - 仅支持粗粒度操作：一个操作会被应用在本RDD的所有数据之上；  

  - 只有需要返回数据或者向外输出数据的RDD操作才会触发实际的计算工作；

- dependencies: RDD的依赖关系；

  - Narrow Dependencies(OneToOneDependecy)  
   
    窄依赖，每个父RDD最多只被一个子RDD使用，是一对一或者多对一的关系；    

  - Wide Dependencies(ShuffleDependecy)  

    宽依赖，多个子RDD依赖于同一个父RDD；  

- DAG: Directed Acyclic Graph, 有向无环图；

- Task: 单个分区数据集上的最小处理流程单元；  

- TaskSet: 由一组关联的但相互之间没有shuffle依赖的任务(Task)所组成的任务集；

- Stage: 一个任务集对应的调度阶段；  

- FinalStage: 直接触发作业的RDD关联的调度阶段；  

- Job: 由一个RDD action生成的一个或多个调度阶段所组成的一次计算作业；  

- Application：Spark应用程序，由一个或多个作业组成；  

- Executor: 执行任务；  

- DAGScheduler: 将作业拆分成具有不同依赖关系的多批任务  

- TaskScheduler: 与DAGScheduler交互，负责任务的物理调度；  

- SchedulerBackend: 与底层资源调度系统交互（mesos/yarn），配合TaskScheduler实现任务执行所需的资源分配；  



## 4. Spark 基本工作流程  


![spark cluster components](http://i.imgur.com/3JW62W0.png)  

*这幅图片简直不能再清晰，来自[Spark官方文档](http://spark.apache.org/docs/2.1.0/cluster-overview.html)*  


![spark scheduler](http://i.imgur.com/J3FesTK.png)  
*图片来自[4][5]两篇博客，是本人找到的最为形象的spark作业调度流程图, 感谢此图作者*

## 5. Spark分布式集群配置方法  

其实本文原本的目的就是分析其安装配置方法，结果跑偏了，现在补充回来。  

Spark集群会有一个master节点，其余都是worker节点，配置及其简单，还是自行参考kakasyw的文章[《Spark 开发环境搭建（五）- Scala和Spark安装》](http://www.jianshu.com/p/09143312dd94)


---

## 参考文献  
1. Spark官网：http://spark.apache.org/documentation.html  
2. 夏俊鸾, 刘旭晖, 邵赛赛. Spark大数据处理技术[M]. 电子工业出版社, 2015.  
3. Spark官网standalone模式解释：http://spark.apache.org/docs/2.1.0/spark-standalone.html  
4. csdn博客：http://blog.csdn.net/jasonding1354/article/details/46974173  
5. csdn博客：http://blog.csdn.net/pelick/article/details/41866845  



