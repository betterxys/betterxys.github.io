---
layout: post
title: Hadoop HA模式双Standby问题
date: 2017-04-07
author: xiaoyongsheng
categories: hadoop LittleBitch
tag: hadoop 

---

* content
{: toc}

## 1. 背景介绍  

 本文目标是要解决HDFS HA模式下，两个NameNode节点均处于StandBy状态的问题。  

## 2. HDFS HA模式介绍  

 在对HDFS HA展开介绍前，首先要清楚其来龙去脉，[简书文章：《hadoop生态圈介绍》](http://www.jianshu.com/p/c3a834e45ae3)一文当中，作者分析的较为清晰；对HDFS HA模式的介绍，强烈推荐[IBM的开源文档:《Hadoop NameNode 高可用 (High Availability) 实现解析》](https://www.ibm.com/developerworks/cn/opensource/os-cn-hadoop-name-node/)。

### 2.1 Hadoop集群模式介绍  

 Hadoop集群总体分为四种模式：  

  - 伪分布模式(Single Node Cluster)  
    
    仅有一台机器，通过进程模拟各主机节点的协作和运行；可靠性差、稳定性低、性能不足，通常用于开发和调试；  

  - 完全分布式(Full Distributed Cluster)  

    至少两台机器，但仅有一台NameNode节点、一台ResourceManager节点；NameNode负责协调管理集群所有的文件访问和操作，当集群规模过于庞大时，NameNode难以负荷会导致集群瘫痪；ResourceManager负责管理集群当中任务的执行，当集群提交的作业过于繁重时，ResourceManager同样面临超负载的问题。但该模式可安全升级为高可用模式。

  - 高可用模式(HA Cluster)  

    HA模式分为两类：NameNode HA和ResourceManager HA，其本质是增加热备节点。以NameNode高可用为例，集群当中有两台NameNode节点，其中仅有一台处于active状态，另外一台处于standby状态，standby状态的节点是active NameNode的热备，当Active NameNode出现问题无法正常运作时，Standby NameNode立刻无缝切入，以保障集群正常运转。其缺陷在于依然仅有一台active状态的NameNode/ResourceManager，导致集群无法横向扩展。  

  - 高可用联邦集群(HA + Federation Cluster)

    单纯HA模式依然存在性能瓶颈，高可用联邦模式通过将HA集群划分为多个集群，多个集群间通过Federation进行关联，不同集群间可以选择性的进行数据节点的共享的方式实现集群的无线横向扩展。  

### 2.2 HDFS HA模式介绍

本节内容详情参考[文献3](https://www.ibm.com/developerworks/cn/opensource/os-cn-hadoop-name-node/)，以下内容为本人理解转述。 

#### 2.2.1 HDFS HA整体架构  

 ![hdfs-ha-architecture](https://www.ibm.com/developerworks/cn/opensource/os-cn-hadoop-name-node/img001.png)  
 *图片来源于[High Availability Framework for HDFS NN](https://issues.apache.org/jira/browse/HDFS-1623?cm_mc_uid=84138998257214745477170&cm_mc_sid_50200000=1491528429)*  

 高可用的NameNode由active NameNode(以下称之为ANN)和standby NameNode(以下称之为SNN)两台NameNode节点组成互备的NameNode(以下称之为NN)节点，只有ANN支持对外读写操作；HA通过共享存储系统实现ANN和SNN的数据同步，共享存储系统中的共享数据包括HDFS元数据以及DataNode(以下称之为DN)映射关系；主备切换时，唯有新的ANN确认数据完全同步后才能继续对外提供服务；主备切换的过程受ZKFailoverController(以下称之为ZKFC)控制, ZKFC监测NN的健康状况，当ANN故障时ZKFC采用ZooKeeper的主备选举功能进行主备选举和切换。  

#### 2.2.2 NN主备切换流程  

 ![hdfs-ha-nn-active-standby-switch](https://www.ibm.com/developerworks/cn/opensource/os-cn-hadoop-name-node/img002.png)  
 *图片来自于[文献3](https://www.ibm.com/developerworks/cn/opensource/os-cn-hadoop-name-node/)*  

 NN主备切换由ZKFailoverController、HealthMonitor和ActiveStandbyElector这三个组件协同完成；ZKFC启动时会创建HealthMonitor和ActiveStandbyElector；其中HealthMonitor负责监测NN的健康状态，ActiveStandbyElector负责完成主备选举；具体切换流程如上图所示：  

 1. HealthMonitor监测NN健康状态；  
 2. 当NN状态发生变化时，HealthMonitor将NN的状态变化向ZKFC报告；  
 3. ZKFC对NN的变化进行判别，若判定需要进行主备切换，则通知ActiveStanbyElector进行主备选举；  
 4. ActiveStandbyElector利用ZooKeeper完成主备选举；  
 5. ActiveStandbyElector将主备选举结果返回给ZKFC；  
 6. ZKFC切换主备状态；  

[文献3](https://www.ibm.com/developerworks/cn/opensource/os-cn-hadoop-name-node/)当中对HealthMonitor的实现机制、ActiveStandbyElector的实现机制、ZKFC的实现机制以及NameNode共享存储的实现机制均作出了详细的解释，感兴趣的同学可以自行前往。  

## 3 HA模式搭建流程  

 1. 每台机器：初始化系统配置

    ```shell
    #增加hadoop组
    groupadd -g 4000 hadoop
    #增加hadoop用户
    useradd -g hadoop -c "hadoopuser" -p 111111 -u 3001 -m hadoop -d /home/hadoop
    #初始化hadoop用户的密码
    passwd hadoop
    #创建hadoop集群的数据与计算的应用目录
    mkdir /app/hadoop
    chown hadoop:hadoop /app/hadoop
    #利用root用户安装emacs工具
    yum install -y emacs
    #修改机器名称,根据不同的机器修改为不同的机器名
    hostname hadoop10
    ```

 2. 每台机器：域名  

    ```shell
    # /etc/sysconfig/network 配置主机域名
    NETWORKING=yes
    HOSTNAME=NN-SPK-3

    # /etc/hosts 域名解析
    192.168.6.231 NN-SPK-1
    192.168.6.232 NN-SPK-2
    192.168.6.233 NN-SPK-3
    192.168.6.234 HDP-DN-1
    192.168.6.235 HDP-DN-2
    192.168.6.236 HDP-DN-3
    ```

 3. 时间同步  
   参考1：[ubuntu时间设置与ntp同步](http://blog.kissdata.com/2014/10/28/ubuntu-ntp.html)  
   参考2：[设置同步的时间服务器](https://wyyhzc.gitbooks.io/hadoop2x/content/hadoop2hamo_shi_de_fen_bu_shi_bu_shu.html)

 4. JDK、Hadoop、ssh环境配置 
   相关教程太多，不做过多解释，见谅

 5. 启动Zookeeper  
   本项目的问题应该就是出现在这个位置，zookeeper相关内容介绍在[文献7](https://www.ibm.com/developerworks/cn/data/library/bd-zookeeper/)和[文献8](http://www.yiibai.com/zookeeper/zookeeper_installation.html)中有详细阐述;  

    ```shell
    bin/zkServer.sh stop  #停止  
    bin/zkServer.sh start  #启动  
    bin/zkServer.sh status  #显示当前状态  

    # 示例  
    [hadoop@NN-SPK-1 zookeeper-3.4.8]$ bin/zkServer.sh status
    ZooKeeper JMX enabled by default
    Using config: /usr/zookeeper/zookeeper-3.4.8/bin/../conf/zoo.cfg
    Mode: follower

    [root@NN-SPK-2 zookeeper-3.4.8]# bin/zkServer.sh status
    ZooKeeper JMX enabled by default
    Using config: /usr/zookeeper/zookeeper-3.4.8/bin/../conf/zoo.cfg
    Mode: follower

    [root@NN-SPK-3 zookeeper-3.4.8]# bin/zkServer.sh  status
    ZooKeeper JMX enabled by default
    Using config: /usr/zookeeper/zookeeper-3.4.8/bin/../conf/zoo.cfg
    Mode: leader
    ```

 6. 启动所有的journalnode
    
    ```shell
    sbin/hadoop-daemon.sh start journalnode
    ```
    
 7. 首次启动时格式化NameNode  

    ```shell
    bin/hdfs namenode -format  
    ```

 8. 启动NameNode  

    ```shell
    bin/hdfs zkfc -formatZK  
    # 启动其中一台namenode  
    sbin/hadoop-daemon.sh start namenode  
    # 登陆另外一台namenode机器  
    bin/hdfs namenode -bootstrapStandby  
    sbin/hadoop-daemon.sh start namenode

    ```

9. 启动ZKFC  

    ```shell  
    #登陆各nameNode机器启动ZKFC  
    sbin/hadoop-daemon.sh start zkfc
    ```
    
    此时，可以查看nameNode状态已经修正为active/standby，也就是说本章问题其实已经解决了，之前的问题就是出现在zkServer出现问题，这特么竟然折腾了这么久。  

10. 启动hadoop集群

    ```shell  
    # 主节点
    sbin/start-dfs.sh

    # ResourceManager
    sbin/start-yarn.sh
    ```

## see u next time  

 本文主要解决的是两个nameNode均为standby的问题，该问题是由于zkfc挂掉导致的，所以现在是解决了这个，可以看到两个nameNode的状态一个为active，另一个为standby：  

![hadoop-nn-active](http://i.imgur.com/7dUj034.png)  

![hadoop-nn-standby](http://i.imgur.com/KgoBcqS.png)  

 ***但是！没错，你也发现了，为什么Summary里面的信息全是0？这个问题留待明天解决，另外贴出来ResourceManager的页面，也许会用到。***

![hadoop-nn-resourceManager](http://i.imgur.com/wz2KKL0.png)  


---
## 参考文献  
1. 吴超沉思录(开源中国社区).国内第一篇详细讲解hadoop2的automatic HA+Federation+Yarn配置的教程:https://my.oschina.net/superwu/blog/198989,2014.  
2. 浊流(简书).hadoop生态圈介绍:http://www.jianshu.com/p/c3a834e45ae3  
3. 程磊,杨剑飞.Hadoop NameNode 高可用 (High Availability) 实现解析:https://www.ibm.com/developerworks/cn/opensource/os-cn-hadoop-name-node/,2015.11.10  
4. Sanjay Radia.High Availability Framework for HDFS NN:https://issues.apache.org/jira/browse/HDFS-1623,15.09.28  
5. r6.Hadoop(2.x)云计算生态系统:https://wyyhzc.gitbooks.io/hadoop2x/content/hadoop2hamo_shi_de_fen_bu_shi_bu_shu.html,2017.4.5  
6. vicentzhwg.ubuntu时间设置与ntp同步:http://blog.kissdata.com/2014/10/28/ubuntu-ntp.html,2014.10.28  
7. Mark Grover.ZooKeeper基础知识、部署和应用程序:https://www.ibm.com/developerworks/cn/data/library/bd-zookeeper/,2014.12.25  
8. funnybone.Zookeeper安装配置:http://www.yiibai.com/zookeeper/zookeeper_installation.html,2017.4.7

