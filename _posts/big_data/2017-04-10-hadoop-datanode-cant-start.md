---
layout: post
title: Hadoop datanode无法启动问题
date: 2017-04-07
author: xiaoyongsheng
categories: hadoop LittleBitch
tag: hadoop 

---

* content
{: toc}

## 1. 背景介绍  

 本文继续折腾Hadoop平台，上周五已经解决了nameNode均处于standby状态的问题，但是后来发现问题如下：  

![hadoop-nn-active](http://i.imgur.com/7dUj034.png)  

![hadoop-nn-standby](http://i.imgur.com/KgoBcqS.png)  

![hadoop-nn-resourceManager](http://i.imgur.com/wz2KKL0.png)  
 
 ***1. 为什么NameNode Information Summary里面的dfs信息全是0？***  

 ***2. 为什么resourceManager里面的active nodes会包括HDP-DN-3和两个localhost(nn-spk-3)？***

## 2. 问题一：Summary信息全是0  

- 首先，要搞清楚的是，summary里面描述的是什么？  
   其实很直观，就是DFS的空间介绍，也就是对DataNodes节点们的描述。

 那么，问题貌似这就已经清晰了，应该是DataNode节点出现了什么问题，所以先去各个节点查看其daemons是否正常：  

```shell  
[hadoop@NN-SPK-1 ~]$ jps
1011 Jps
13044 NameNode
13206 DFSZKFailoverController
16169 Master

[hadoop@NN-SPK-2 ~]$ jps
9613 DFSZKFailoverController
9486 NameNode
2943 Jps

[hadoop@NN-SPK-3 ~]$ jps
3012 ResourceManager
25940 Jps

[hadoop@HDP-DN-1 ~]$ jps
10453 Jps
32507 JournalNode
764 NodeManager

[hadoop@HDP-DN-2 ~]$ jps
11906 JournalNode
23608 Jps
12669 NodeManage

[hadoop@HDP-DN-3 ~]$ jps
21682 JournalNode
22429 NodeManager
1150 Jps
```

 果不其然，DataNode们根本没有起来！那么尝试起一个试试看：  

```
[hadoop@HDP-DN-3 ~]$ /usr/hadoop/hadoop-2.7.1/sbin/hadoop-daemon.sh --script hdfs start datanode
starting datanode, logging to /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-datanode-HDP-DN-3.out
[hadoop@HDP-DN-3 ~]$ jps
1281 Jps
21682 JournalNode
22429 NodeManager
[hadoop@HDP-DN-3 ~]$ cat /usr/hadoop/hadoop-2.7.1/logs/hadoop-hadoop-datanode-HDP-DN-3.out
ulimit -a for user hadoop
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 46667
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 10240
cpu time               (seconds, -t) unlimited
max user processes              (-u) 1024
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited

```

 显然，datanode启动失败，在out日志当中体现出好像是检测不到当前机器配置信息？需要仔细查看下datenode的log日志来看。  

## 3. 问题二：datanode启动失败  

```
2017-04-10 17:48:26,655 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: STARTUP_MSG: 
/************************************************************
STARTUP_MSG: Starting DataNode
STARTUP_MSG:   host = HDP-DN-3/192.168.6.236
STARTUP_MSG:   args = []
STARTUP_MSG:   version = 2.7.1
STARTUP_MSG:   classpath = #太长省掉#
STARTUP_MSG:   build = https://git-wip-us.apache.org/repos/asf/hadoop.git -r 15ecc87ccf4a0228f35af08fc56de536e6ce657a; compiled by 'jenkins' on 2015-06-29T06:04Z
STARTUP_MSG:   java = 1.8.0_60
************************************************************/
2017-04-10 17:48:26,668 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: registered UNIX signal handlers for [TERM, HUP, INT]
2017-04-10 17:48:27,136 WARN org.apache.hadoop.util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
2017-04-10 17:48:27,454 INFO org.apache.hadoop.metrics2.impl.MetricsConfig: loaded properties from hadoop-metrics2.properties
2017-04-10 17:48:27,556 INFO org.apache.hadoop.metrics2.impl.MetricsSystemImpl: Scheduled snapshot period at 10 second(s).
2017-04-10 17:48:27,556 INFO org.apache.hadoop.metrics2.impl.MetricsSystemImpl: DataNode metrics system started
2017-04-10 17:48:27,564 INFO org.apache.hadoop.hdfs.server.datanode.BlockScanner: Initialized block scanner with targetBytesPerSec 1048576
2017-04-10 17:48:27,566 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Configured hostname is HDP-DN-3
2017-04-10 17:48:27,575 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Starting DataNode with maxLockedMemory = 0
2017-04-10 17:48:27,610 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Opened streaming server at /0.0.0.0:50010
2017-04-10 17:48:27,613 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Balancing bandwith is 1048576 bytes/s
2017-04-10 17:48:27,613 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Number threads for balancing is 5
2017-04-10 17:48:27,740 INFO org.mortbay.log: Logging to org.slf4j.impl.Log4jLoggerAdapter(org.mortbay.log) via org.mortbay.log.Slf4jLog
2017-04-10 17:48:27,752 INFO org.apache.hadoop.security.authentication.server.AuthenticationFilter: Unable to initialize FileSignerSecretProvider, falling back to use random secrets.
2017-04-10 17:48:27,761 INFO org.apache.hadoop.http.HttpRequestLog: Http request log for http.requests.datanode is not defined
2017-04-10 17:48:27,769 INFO org.apache.hadoop.http.HttpServer2: Added global filter 'safety' (class=org.apache.hadoop.http.HttpServer2$QuotingInputFilter)
2017-04-10 17:48:27,772 INFO org.apache.hadoop.http.HttpServer2: Added filter static_user_filter (class=org.apache.hadoop.http.lib.StaticUserWebFilter$StaticUserFilter) to context datanode
2017-04-10 17:48:27,772 INFO org.apache.hadoop.http.HttpServer2: Added filter static_user_filter (class=org.apache.hadoop.http.lib.StaticUserWebFilter$StaticUserFilter) to context logs
2017-04-10 17:48:27,772 INFO org.apache.hadoop.http.HttpServer2: Added filter static_user_filter (class=org.apache.hadoop.http.lib.StaticUserWebFilter$StaticUserFilter) to context static
2017-04-10 17:48:27,797 INFO org.apache.hadoop.http.HttpServer2: Jetty bound to port 41040
2017-04-10 17:48:27,797 INFO org.mortbay.log: jetty-6.1.26
2017-04-10 17:48:28,019 INFO org.mortbay.log: Started HttpServer2$SelectChannelConnectorWithSafeStartup@localhost:41040
2017-04-10 17:48:28,156 INFO org.apache.hadoop.hdfs.server.datanode.web.DatanodeHttpServer: Listening HTTP traffic on /0.0.0.0:50075
2017-04-10 17:48:28,370 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: dnUserName = hadoop
2017-04-10 17:48:28,370 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: supergroup = supergroup
2017-04-10 17:48:28,431 INFO org.apache.hadoop.ipc.CallQueueManager: Using callQueue class java.util.concurrent.LinkedBlockingQueue
2017-04-10 17:48:28,457 INFO org.apache.hadoop.ipc.Server: Starting Socket Reader #1 for port 50020
2017-04-10 17:48:28,500 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Opened IPC server at /0.0.0.0:50020
2017-04-10 17:48:28,516 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Refresh request received for nameservices: nbse
2017-04-10 17:48:28,543 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Starting BPOfferServices for nameservices: nbse
2017-04-10 17:48:28,562 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Block pool <registering> (Datanode Uuid unassigned) service to nn-spk-2/192.168.6.232:9000 starting to offer service
2017-04-10 17:48:28,562 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Block pool <registering> (Datanode Uuid unassigned) service to NN-SPK-1/192.168.6.231:9000 starting to offer service
2017-04-10 17:48:28,571 INFO org.apache.hadoop.ipc.Server: IPC Server Responder: starting
2017-04-10 17:48:28,571 INFO org.apache.hadoop.ipc.Server: IPC Server listener on 50020: starting
2017-04-10 17:48:28,947 INFO org.apache.hadoop.hdfs.server.common.Storage: Lock on /opt/cd1/in_use.lock acquired by nodename 1382@HDP-DN-3

2017-04-10 17:48:28,951 WARN org.apache.hadoop.hdfs.server.common.Storage: java.io.IOException: Incompatible clusterIDs in /opt/cd1: namenode clusterID = CID-505702a1-3c90-4ee4-8fc0-db8aca83aca6; datanode clusterID = CID-6b15f332-f49d-40c1-ab8b-0d741b788143
2017-04-10 17:48:28,961 INFO org.apache.hadoop.hdfs.server.common.Storage: Lock on /opt/cd2/in_use.lock acquired by nodename 1382@HDP-DN-3
2017-04-10 17:48:28,961 WARN org.apache.hadoop.hdfs.server.common.Storage: java.io.IOException: Incompatible clusterIDs in /opt/cd2: namenode clusterID = CID-505702a1-3c90-4ee4-8fc0-db8aca83aca6; datanode clusterID = CID-6b15f332-f49d-40c1-ab8b-0d741b788143
2017-04-10 17:48:28,969 INFO org.apache.hadoop.hdfs.server.common.Storage: Lock on /opt/cd3/in_use.lock acquired by nodename 1382@HDP-DN-3
2017-04-10 17:48:28,969 WARN org.apache.hadoop.hdfs.server.common.Storage: java.io.IOException: Incompatible clusterIDs in /opt/cd3: namenode clusterID = CID-505702a1-3c90-4ee4-8fc0-db8aca83aca6; datanode clusterID = CID-6b15f332-f49d-40c1-ab8b-0d741b788143
2017-04-10 17:48:28,971 INFO org.apache.hadoop.hdfs.server.common.Storage: Lock on /opt/cd1/in_use.lock acquired by nodename 1382@HDP-DN-3
2017-04-10 17:48:28,971 WARN org.apache.hadoop.hdfs.server.common.Storage: java.io.IOException: Incompatible clusterIDs in /opt/cd1: namenode clusterID = CID-505702a1-3c90-4ee4-8fc0-db8aca83aca6; datanode clusterID = CID-6b15f332-f49d-40c1-ab8b-0d741b788143
2017-04-10 17:48:28,971 INFO org.apache.hadoop.hdfs.server.common.Storage: Lock on /opt/cd2/in_use.lock acquired by nodename 1382@HDP-DN-3
2017-04-10 17:48:28,972 WARN org.apache.hadoop.hdfs.server.common.Storage: java.io.IOException: Incompatible clusterIDs in /opt/cd2: namenode clusterID = CID-505702a1-3c90-4ee4-8fc0-db8aca83aca6; datanode clusterID = CID-6b15f332-f49d-40c1-ab8b-0d741b788143
2017-04-10 17:48:28,977 INFO org.apache.hadoop.hdfs.server.common.Storage: Lock on /opt/cd3/in_use.lock acquired by nodename 1382@HDP-DN-3
2017-04-10 17:48:28,977 WARN org.apache.hadoop.hdfs.server.common.Storage: java.io.IOException: Incompatible clusterIDs in /opt/cd3: namenode clusterID = CID-505702a1-3c90-4ee4-8fc0-db8aca83aca6; datanode clusterID = CID-6b15f332-f49d-40c1-ab8b-0d741b788143

2017-04-10 17:48:28,978 FATAL org.apache.hadoop.hdfs.server.datanode.DataNode: Initialization failed for Block pool <registering> (Datanode Uuid unassigned) service to NN-SPK-1/192.168.6.231:9000. Exiting. 
java.io.IOException: All specified directories are failed to load.
        at org.apache.hadoop.hdfs.server.datanode.DataStorage.recoverTransitionRead(DataStorage.java:477)
        at org.apache.hadoop.hdfs.server.datanode.DataNode.initStorage(DataNode.java:1361)
        at org.apache.hadoop.hdfs.server.datanode.DataNode.initBlockPool(DataNode.java:1326)
        at org.apache.hadoop.hdfs.server.datanode.BPOfferService.verifyAndSetNamespaceInfo(BPOfferService.java:316)
        at org.apache.hadoop.hdfs.server.datanode.BPServiceActor.connectToNNAndHandshake(BPServiceActor.java:223)
        at org.apache.hadoop.hdfs.server.datanode.BPServiceActor.run(BPServiceActor.java:801)
        at java.lang.Thread.run(Thread.java:745)
2017-04-10 17:48:28,978 FATAL org.apache.hadoop.hdfs.server.datanode.DataNode: Initialization failed for Block pool <registering> (Datanode Uuid unassigned) service to nn-spk-2/192.168.6.232:9000. Exiting. 
java.io.IOException: All specified directories are failed to load.
        at org.apache.hadoop.hdfs.server.datanode.DataStorage.recoverTransitionRead(DataStorage.java:477)
        at org.apache.hadoop.hdfs.server.datanode.DataNode.initStorage(DataNode.java:1361)
        at org.apache.hadoop.hdfs.server.datanode.DataNode.initBlockPool(DataNode.java:1326)
        at org.apache.hadoop.hdfs.server.datanode.BPOfferService.verifyAndSetNamespaceInfo(BPOfferService.java:316)
        at org.apache.hadoop.hdfs.server.datanode.BPServiceActor.connectToNNAndHandshake(BPServiceActor.java:223)
        at org.apache.hadoop.hdfs.server.datanode.BPServiceActor.run(BPServiceActor.java:801)
        at java.lang.Thread.run(Thread.java:745)
2017-04-10 17:48:28,981 WARN org.apache.hadoop.hdfs.server.datanode.DataNode: Ending block pool service for: Block pool <registering> (Datanode Uuid unassigned) service to NN-SPK-1/192.168.6.231:9000
2017-04-10 17:48:28,981 WARN org.apache.hadoop.hdfs.server.datanode.DataNode: Ending block pool service for: Block pool <registering> (Datanode Uuid unassigned) service to nn-spk-2/192.168.6.232:9000
2017-04-10 17:48:29,083 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Removed Block pool <registering> (Datanode Uuid unassigned)
2017-04-10 17:48:31,083 WARN org.apache.hadoop.hdfs.server.datanode.DataNode: Exiting Datanode
2017-04-10 17:48:31,087 INFO org.apache.hadoop.util.ExitUtil: Exiting with status 0
2017-04-10 17:48:31,093 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: SHUTDOWN_MSG: 
/************************************************************
SHUTDOWN_MSG: Shutting down DataNode at HDP-DN-3/192.168.6.236
```

问题应该是出在这里：`java.io.IOException: Incompatible clusterIDs`,这句话是说NameNode的ClusterID和DataNode的Cluster ID不一致，导致无法启动DataNode。  

对于ClusterID不一致的问题，有三种解决方案：  
  
  1. 将所有datanode节点上的clusterID修改为与nameNode ClusterID相同<sup>[3]</sup>；  
  2. 将nameNode ClusterID修改为datanode ClusterID<sup>[1]</sup>:  
      ```
      ./hdfs namenode -format -clusterId CID-*****(copy from datanode clusterId)
      ```
  3. 清空所有datanode节点的{dfs.datanode.data.dir}(由core-site.xml指定)目录中的数据<sup>[2]</sup>  ；

三个方案各有优劣，方案1和3都需要在所有DataNode节点进行相同操作，而方案2只需在两个nameNode节点操作即可，论及简单应该首选方案二；  
方案1和方案2都需要对原有数据进行修改，而方案三无需修改，只需要清空目录即可，比较稳；    

终于折腾好了，是不是应该截图纪念一下：

![active_nn](http://i.imgur.com/Z39mlqe.png)

![standby_nn](http://i.imgur.com/gylOdWM.png)

---
## 参考文献  
1. stackoverflow[OL]:http://stackoverflow.com/questions/22316187/datanode-not-starts-correctly,2014  
2. 启动Hadoop HDFS时的“Incompatible clusterIDs”错误原因分析[OL]:http://blog.chinaunix.net/uid-20682147-id-4214553.html,2014  
3. kinglau.安装hadoop2.4.0遇到的问题:http://www.cnblogs.com/kinglau/p/3796274.html,2014  

