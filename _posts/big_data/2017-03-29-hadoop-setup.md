---
layout: post
title: Hadoop配置解析
date: 2017-03-29
author: xiaoyongsheng
categories: hadoop
tag: hadoop

---

* content
{: toc}

## 1. 背景介绍  
笔者之所以写这篇博文，目的并非是从头开始介绍Hadoop或者Spark的配置步骤，目前所在实习单位在此之前已经搭建好Hadoop和Spark平台，笔者需要搞清楚之前的配置情况，所以需要理清思路，为后续平台应用做准备。  
## 2. Hadoop 2.7.1  
### 2.1 相关生态  
Hadoop<sup>[1]</sup>时至今日已经发展到了3.0版本，主要包括以下四个模块：  
 - Hadoop Common：基本组件；  
 - HDFS：分布式文件系统；  
 - YARN：负责任务调度和资源管理的框架；  
 - MapReduce：基于YARN的并行计算框架；  
相关生态包括：  
 - Ambari：网页面板配置、管理、监控集群组件；  
 - Avro: 数据序列化系统；
 - Cassandra: 可扩展的多主机数据库，避免单点故障；
 - Chukwa: 分布式系统的数据收集组件；  
 - HBase: 支持结构化数据存储的可扩展的分布式数据库；
 - Hive：数据仓库组件；
 - Mahout：数据挖掘和机器学习组件；
 - Pig：并行计算；  
 - Spark：ETL、机器学习、流处理、图计算；  
 - Tez: 基于Yarn的数据流编程框架，用以替代MapReduce（感觉与Spark功能类似）  
 - ZooKeeper：协调各应用；

### 2.2 集群配置  
通常情况下，集群当中有一台作为NameNode，一台作为ResourceManager，称之为masters；其余机器是DataNode/NodeManager，称之为Slaves；
Hadoop的配置文件分为三类：  
 - 默认的只读文件
   - core-default.xml  
   - hdfs-default.xml  
   - yarn-default.xml  
   - mapred-default.xml  

 - site-specific配置文件  
    - etc/hadoop/core-site.xml  

        ```xml
        <configuration>
        <property>
            <name>fs.defaultFS</name>
            <value>hdfs://nbse</value>
        </property>
        <property>
            <name>fs.default.name</name>    
            <value>hdfs://nn-spk-1:9000</value>
        </property>
        <property>
            <name>hadoop.tmp.dir</name>
            <value>/opt/hadoop/tmp</value>
        </property>
        <property>
            <name>ha.zookeeper.quorum</name>
            <value>NN-SPK-1:2181,NN-SPK-2:2181,NN-SPK-3:2181</value>
        </property>
        </configuration>
        ```
    
        以上配置可以整理为：

        property|value|description
        ---|---|---
        fs.defaultFS|hdfs://nbse|默认文件系统的URI
        fs.default.name|hdfs://nn-spk-1:9000|已弃用，功能等同于fs.defaultFS
        hadoop.tmp.dir|/opt/hadoop/tmp|临时文件存放路径
        ha.zookeeper.quorum|NN-SPK-1:2181,<br>NN-SPK-2:2181,<br>NN-SPK-3:2181|ZooKeeper服务地址列表，用逗号分隔

    - etc/hadoop/hdfs-site.xml  

        ```xml
        <configuration>
          <property>
            <name>dfs.nameservices</name>
            <value>nbse</value>
          </property>
          <property>
            <name>dfs.ha.namenodes.nbse</name>
            <value>nnm,nns</value>
          </property>

          <property>
            <name>dfs.namenode.rpc-address.nbse.nnm</name>
            <value>NN-SPK-1:9000</value>
          </property>
          <property>
            <name>dfs.namenode.http-address.nbse.nnm</name>
            <value>NN-SPK-1:50070</value>
          </property>
          <property>
            <name>dfs.namenode.rpc-address.nbse.nns</name>
            <value>NN-SPK-2:9000</value>
          </property>
          <property>
            <name>dfs.namenode.http-address.nbse.nns</name>
            <value>NN-SPK-2:50070</value>
          </property>

          <property>
            <name>dfs.namenode.shared.edits.dir</name>
            <value>qjournal://HDP-DN-1:8485;HDP-DN-2:8485;HDP-DN-3:8485/nbse</value>
          </property>
          <property>
            <name>dfs.journalnode.edits.dir</name>
            <value>/opt/hadoop/journal</value>
          </property>

          <property>
            <name>dfs.ha.automatic-failover.enabled</name>
            <value>true</value>
          </property>
          <property>
            <name>dfs.client.failover.proxy.provider.nbse</name>
            <value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
          </property>

          <property>
            <name>dfs.ha.fencing.methods</name>
            <value>
                sshfence
            </value>
          </property>
          <property>
            <name>dfs.ha.fencing.ssh.private-key-files</name>
            <value>/home/hadoop/.ssh/id_rsa</value>
          </property>
          <property>
            <name>dfs.ha.fencing.ssh.connect-timeout</name>
            <value>30000</value>
          </property>
        </configuration>
        ```
    
        同理，以上配置可以整理为：

        property|value|description
        ---|---|---
        dfs.nameservices|nbse|逗号分隔的 **nameservices**
        dfs.ha.namenodes.nbse|nnm,nns|The prefix for a given nameservice
        dfs.namenode.rpc-address.nbse.nnm|NN-SPK-1:9000|RPC address that handles all clients requests.
        dfs.namenode.http-address.nbse.nnm|NN-SPK-1:50070|The actual adress the HTTP server will bind to.
        dfs.namenode.rpc-address.nbse.nns|NN-SPK-2:9000|
        dfs.namenode.http-address.nbse.nns|NN-SPK-2:50070|
        dfs.namenode.shared.edits.dir|qjournal://HDP-DN-1:8485;<br>HDP-DN-2:8485;<br>HDP-DN-3:8485/nbse|A directory on shared storage between the multiple namenodes in an HA cluster.
        dfs.journalnode.edits.dir|/opt/hadoop/journal|
        dfs.client.failover.proxy.provider.nbse|org.apache.hadoop.hdfs.<br>server.namenode.ha.<br>ConfigureFailoverProxyProvider|
        dfs.ha.automatic-failover.enabled|true|HDFS的高可用设置，故障自动切换
        dfs.ha.fencing.methods|sshfence|
        dfs.ha.fencing.ssh.private-key-files|/home/hadoop/.ssh/id_rsa|
        dfs.ha.fencing.ssh.connect-timeout|30000|


    - etc/hadoop/yarn-site.xml  

        ```xml
        <configuration>
        <property>
            <name>yarn.resourcemanager.hostname</name>
            <value>NN-SPK-3</value>
        </property>
        <property>
            <name>yarn.nodemanager.aux-services</name>
            <value>mapreduce_shuffle</value>
        </property>
        <property>
            <name>yarn.resourcemanager.address</name>
            <value>localhost:8032</value>
        </property>
        </configuration>
        ```
        
        以上配置可以整理为：

        property|value|description
        ---|---|---
        yarn.resourcemanager.hostname|NN-SPK-3|
        yarn.nodemanager.aux-services|mapreduce_shuffle|
        yarn.resourcemanager.address|localhost:8032|


   - etc/hadoop/mapred-site.xml  

    ```xml
    <configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    </configuration>
    ```
    
 - 环境配置  
   - etc/hadoop/hadoop-env.sh      
   - etc/hadoop/mapred-env.sh  
   - etc/hadoop/yarn-env.sh      
   > Additionally, you can control the Hadoop scripts found in the bin/ directory of the distribution, by setting site-specific values via the etc/hadoop/hadoop-env.sh and etc/hadoop/yarn-env.sh.  

此时，基本上Hadoop涉及到的所有配置文件都已经浏览一遍，然而并没有什么太大的收获,可能有用的信息如下：

property|value|description
---|---|---
fs.defaultFS|hdfs://nbse|默认文件系统的URI
fs.default.name|hdfs://nn-spk-1:9000|已弃用，功能等同于fs.defaultFS
ha.zookeeper.quorum|NN-SPK-1:2181,<br>NN-SPK-2:2181,<br>NN-SPK-3:2181|ZooKeeper服务地址列表，用逗号分隔
yarn.resourcemanager.hostname|NN-SPK-3|
yarn.resourcemanager.address|localhost:8032|
dfs.nameservices|nbse|逗号分隔的 **nameservices**
dfs.ha.namenodes.nbse|nnm,nns|The prefix for a given nameservice
dfs.namenode.rpc-address.nbse.nnm|NN-SPK-1:9000|RPC address that handles all clients requests.
dfs.namenode.http-address.nbse.nnm|NN-SPK-1:50070|The actual adress the HTTP server will bind to.
dfs.namenode.rpc-address.nbse.nns|NN-SPK-2:9000|
dfs.namenode.http-address.nbse.nns|NN-SPK-2:50070|
dfs.namenode.shared.edits.dir|qjournal://HDP-DN-1:8485;<br>HDP-DN-2:8485;<br>HDP-DN-3:8485/nbse|A directory on shared storage between the multiple namenodes in an HA cluster.

### 2.3 守护进程

category|daemons
---|---
HDFS|***NameNode***:  nbse(nn-spk-1:9000)<br>***SecondaryNameNode***：**NN-SPK-2:9000？**<br>***DataNode***
YARN|***ResourceManager***:NN-SPK-3(localhost:8032)<br>***NodeManager***<br>***WebAppProxy***
MapReduce|***MapReduce Job History Server***

### 2.4 启动Hadoop

```shell
<!-- Hadoop 3 cmd-->
<!-- 如果etc/hadoop/workers和ssh的权限已经配置,可以一次性启动HDFS, 否则就根据子步骤逐步启动-->
sbin/start-dfs.sh
    <!-- 格式化HDFS -->
    bin/hdfs namenode -format <cluster_name>
    <!-- 启动NameNode -->
    bin/hdfs --daemon start namenode
    <!-- 启动DataNode -->
    bin/hdfs --daemon start datanode
<!-- 同理启动YARN -->
sbin/start-yarn.sh
    bin/yarn --daemon start resourcemanager
    bin/yarn --daemon start nodemanager
    bin/yarn --daemon start proxyserver
<!-- 启动mapred -->
bin/mapred --daemon start historyserver
```

启动日志如下：
> [hadoop@NN-SPK-1 hadoop-2.7.1]$ sbin/start-dfs.sh  
> 17/03/30 16:52:06 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable  
> Starting namenodes on [NN-SPK-2 NN-SPK-1]  
> NN-SPK-1: starting namenode, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-namenode-NN-SPK-1.out  
> NN-SPK-2: starting namenode, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-namenode-NN-SPK-2.out  
> HDP-DN-3: starting datanode, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-datanode-HDP-DN-3.out  
> HDP-DN-1: starting datanode, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-datanode-HDP-DN-1.out  
> HDP-DN-2: starting datanode, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-datanode-HDP-DN-2.out  
> Starting journal nodes [HDP-DN-1 HDP-DN-2 HDP-DN-3]  
> HDP-DN-3: starting journalnode, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-journalnode-HDP-DN-3.out  
> HDP-DN-1: starting journalnode, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-journalnode-HDP-DN-1.out  
> HDP-DN-2: starting journalnode, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-journalnode-HDP-DN-2.out  
> 17/03/30 16:52:25 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable  
> Starting ZK Failover Controllers on NN hosts [NN-SPK-2 NN-SPK-1]  
> NN-SPK-1: starting zkfc, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-zkfc-NN-SPK-1.out  
> NN-SPK-2: starting zkfc, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-zkfc-NN-SPK-2.out  

所以，显而易见：

daemons|machines
---|---
NameNode|NN-SPK-1
Secondary NameNode| NN-SPK-2
DataNode|HDP-DN-1;HDP-DN-2;HDP-DN-3
journal nodes|HDP-DN-1;HDP-DN-2;HDP-DN-3
ZK Failover Controllers| NN-SPK-1; NN-SPK-2

那么，问题来了，什么是journal nodes？什么是ZK Failover Controllers？放到最后第3章进行详细描述。

### 2.5 关闭Hadoop

```shell
<!-- Hadoop 3 cmd -->
sbin/stop-dfs.sh
    bin/hdfs --daemon stop namenode
    bin/hdfs --daemon stop datanode
sbin/stop-yarn.sh
    bin/yarn --daemon stop resourcemanager
    bin/yarn --daemon stop nodemanager
<!-- 貌似stop-yarn.sh不能关闭proxyserver,后续验证 -->
bin/yarn --daemon stop proxyserver
bin/mapred --daemon stop historyserver
```

### 2.6 总结
现在理一下思路：  
本平台共有两台NameNode，3台DataNode，为什么会有两台NameNode呢？  
 - 是由于当初部署测试环境的人误认为SecondaryNameNode是NameNode的备份，所以将NameNode和SecondaryNameNode分别部署到两台机器上！  

笔者当初Hadoop课程没有认真听，但是依稀记得SecondaryNameNode是用以辅助NameNode启动的，所以笔者以为NameNode和SecondaryNameNode应该在同一台机器上，为了验证我的想法特意去到[官方文档](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html#Secondary_NameNode)找依据（详见本文3.1）。

这个时候...喜剧的一幕出现了！！！  
测试环境部署者的理解是错的，可是他做对了！Secondary NameNode确实是用以辅助NameNode的启动，但是他们占用的内存大小类似，所以确实是应该分别部署在两台机器上的！  

事实证明，我是错的，在查看journal nodes的作用时（本文3.2），才发现这里的两个nn都是NameNode，这是一种实现HDFS高可用的方式，其中一台nameNode处于active状态，管理HDFS，另外一台处于standby状态，作为热备。所以本平台并未专门设置secondarynameNode，而是采用默认配置。  

---
2017/4/1  
现在补充hadoop测试环境配置信息：  

机器名称| ip|物理cpu个数|逻辑cpu个数|内存|存储空间  
   ---  |---|    ---    |    ---    |--- |  --- 
nn-spk-1  | 192.168.6.231 | 4 | 8 | 12G | 46G  
nn-spk-2  | 192.168.6.232 | 4 | 8 | 12G | 46G
nn-spk-3  | 192.168.6.233 | 4 | 8 | 12G | 46G


*如何查看配置信息，返回主页参考另外一篇[《linux-常用命令》](https://betterxys.github.io/2017/04/01/linux-command/)*  


---

## 3. 问题解析

### 3.1 Secondary Namenode的作用
> 官方文档如下：Secondary NameNode  
> 
> The NameNode stores modifications to the file system as a log appended to a native file system file, edits. When a NameNode starts up, it reads HDFS state from an image file, fsimage, and then applies edits from the edits log file. It then writes new HDFS state to the fsimage and starts normal operation with an empty edits file. Since NameNode merges fsimage and edits files only during start up, the edits log file could get very large over time on a busy cluster. Another side effect of a larger edits file is that next restart of NameNode takes longer.  
>  
> The secondary NameNode merges the fsimage and the edits log files periodically and keeps edits log size within a limit. It is usually run on a different machine than the primary NameNode since its memory requirements are on the same order as the primary NameNode.  
> 
> The start of the checkpoint process on the secondary NameNode is controlled by two configuration parameters.  
 - dfs.namenode.checkpoint.period, set to 1 hour by default, specifies the maximum delay between two consecutive checkpoints  
 - dfs.namenode.checkpoint.txns, set to 1 million by default, defines the number of uncheckpointed transactions on the NameNode which will force an urgent checkpoint, even if the checkpoint period has not been reached.
>
> The secondary NameNode stores the latest checkpoint in a directory which is structured the same way as the primary NameNode’s directory. So that the check pointed image is always ready to be read by the primary NameNode if necessary.
> For command usage, see secondarynamenode.

NameNode将文件系统的变动以日志的形式存储在本地的日志文件当中、将HDFS的状态保存在一份镜像文件当中，可以理解为文件系统的快照，称之为'fsimage'。在NameNode启动过程中，首先从fsimage中读取文件系统的状态；然后再读取变动日志文件，将日志当中记录的变动应用于当前文件系统；再然后生成新的fsimage文件，并将此后所有的变动即时记录保存在日志文件当中。这个流程就意味着NameNode只在启动的时候才去合并fsimage和log文件，这个策略会造成在文件系统变更频繁时log文件过大，log文件过大就会造成NameNode在下次重启时，用于恢复系统的时间大大增加。 
***Secondary NameNode的作用是以固定频率合并fsimage和系统变更日志，并限制变更日志文件的大小。通常Secondary NameNode与NameNode是部署在不同机器上的***，原因是二者对于内存的需求在同一量级。  
Secondary NameNode受两个参数的控制：  
 - dfs.namenode.checkpoint.period： fsimage和edit log的合并频率；  
 - dfs.namenode.checkpoint.txns： edit log的最大容量；

Secondary NameNode的文件结构和NameNode保持一致以便NameNode随时读取。

### 3.2 journal nodes的作用

来自[官方的解释](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html)

> Architecture
> 
> In a typical HA cluster, two separate machines are configured as NameNodes. At any point in time, exactly one of the NameNodes is in an Active state, and the other is in a Standby state. The Active NameNode is responsible for all client operations in the cluster, while the Standby is simply acting as a slave, maintaining enough state to provide a fast failover if necessary.
> 
> In order for the Standby node to keep its state synchronized with the Active node, both nodes communicate with a group of separate daemons called “JournalNodes” (JNs). When any namespace modification is performed by the Active node, it durably logs a record of the modification to a majority of these JNs. The Standby node is capable of reading the edits from the JNs, and is constantly watching them for changes to the edit log. As the Standby Node sees the edits, it applies them to its own namespace. In the event of a failover, the Standby will ensure that it has read all of the edits from the JounalNodes before promoting itself to the Active state. This ensures that the namespace state is fully synchronized before a failover occurs.
> 
> In order to provide a fast failover, it is also necessary that the Standby node have up-to-date information regarding the location of blocks in the cluster. In order to achieve this, the DataNodes are configured with the location of both NameNodes, and send block location information and heartbeats to both.
> 
> It is vital for the correct operation of an HA cluster that only one of the NameNodes be Active at a time. Otherwise, the namespace state would quickly diverge between the two, risking data loss or other incorrect results. In order to ensure this property and prevent the so-called “split-brain scenario,” the JournalNodes will only ever allow a single NameNode to be a writer at a time. During a failover, the NameNode which is to become active will simply take over the role of writing to the JournalNodes, which will effectively prevent the other NameNode from continuing in the Active state, allowing the new Active to safely proceed with failover.

Quorum Journal Manager是用以实现HDFS的高可用(high availability)而存在的，所谓HA就是nameNode不能挂，所以就采用了热备的方式，保证有两台nameNode同时准备着，其中一台处于active状态，另外一台处于standby状态，当avtive的nameNode挂掉了，standby的nameNode就可以随时接盘，journal nodes的作用就是保持两个nameNode之间的一致。

### 3.3 ZK Failover Controllers的作用

[参考博客](http://debugo.com/namenode-ha/)  

在之前的设置中有一项`dfs.ha.automatic-failover.enabled`被设置为True，该项设置代表的是自动启动HDFS的automatic-failover。automatic-failover依赖于zookeeper和ZKFC(ZK Failover Controllers)。  
这里解释三个概念：
- Failover  
    第一步，对之前的NN执行fence，如果需要的话。第二步，将本地NN转换到active状态。
- fence  
    dfs.ha.fencing.methods —– 解决HA集群脑裂问题（即出现两个master 同时对外提供服务，导致系统处于不一致状态）。在HDFS HA中，JournalNode 只允许一个NameNode写数据，不会出现两个active NameNode的问题，但是当主备切换时，之前的active NameNode可能仍在处理客户端的RPC 请求，为此，需要增加隔离机制（fencing）将之前的active NameNode杀死。常用的fence方法是sshfence，要指定ssh通讯使用的密钥dfs.ha.fencing.ssh.private-key-files和连接超时时间。
- ZKFC  
 ZKFC是ZooKeeper的一个客户端，用以监控nameNode的状态。  
 zkfs提供了下面的功能：  
     - Health monitoring：zkfc定期对本地的NN发起health-check的命令，如果NN正确返回，那么这个NN被认为是OK的。否则被认为是失效节点。  
     - ZooKeeper session management：当本地NN是健康的时候，zkfc将会在zk中持有一个session。如果本地NN又正好是active的，那么zkfc还有持有一个”ephemeral”的节点作为锁，一旦本地NN失效了，那么这个节点将会被自动删除。
     - ZooKeeper-based election：如果本地NN是健康的，并且zkfc发现没有其他的NN持有那个独占锁。那么他将试图去获取该锁，一旦成功，那么它就需要执行Failover，然后成为active的NN节点。



## 参考文献  
【1】 http://hadoop.apache.org/docs/r2.7.1/hadoop-project-dist/hadoop-common/ClusterSetup.html   
【2】 http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html#Secondary_NameNode  
【3】https://my.oschina.net/u/189445/blog/661561  
【4】https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html  
【5】http://debugo.com/namenode-ha/  

