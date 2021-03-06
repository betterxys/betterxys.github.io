---
layout: post
title: 读书报告-大数据处理系统的研究进展与展望
date:  2017-03-21
author: xiaoyongsheng
By: xiaoyongsheng
email: xiaoyongsheng@hotmail.com  
categories: BookReport
tag: 大数据系统
---

* content
{:toc}

阅读文献： 王鹏, 张利. 大数据处理系统的研究进展与展望[J]. 高技术通讯, 2015 (8): 793-801.  

------

## 大数据的特征  
几乎是所有涉及大数据方向的文献都会介绍的一个概念：4V，笔者今天看到了一篇博士论文当中提到了5V的概念[1]，然后又在wiki上面发现了最初的3V说法[2][3]，再此总结：  
* Volume: 数据量
* Velocity: 速度
* Varity： 多样
* （4V）Veracity：真实性
* （5V）Value：价值
   
## Hadoop&Spark软件栈
作者将Hadoop和Spark软件栈分为如下四个层次：

1. 资源管理  
 * 职能：管理硬件资源，提供统一接口；
 * 发展方向：统一的资源管理与调度系统，支持多种计算框架；
2. 数据存储与管理
 * 职能：采取分布式技术存储海量数据；
 * 主流方向：**列式数据库**；  
   > 后续补充  
3. 数据处理
 * 职能：编程框架与编程语言；
 * 发展方向： 分布式程序；
4. 应用

笔者认为作者的分层思路可以扩展到整个大数据领域（其实，他自身也许也是这个意思），所谓大数据是以数据为基础，以分布式存储、并行计算框架为平台，数据挖掘（包括但不局限于机器学习、深度学习和统计学习等方法）为手段，从海量数据当中提取出相对可靠且对我们业务需求有所帮助的信息，进而为决策层提供参考。所以笔者的思路与作者类似但略有不同，可以将其分为：数据的获取与存储、数据的处理与计算、数据汇总与可视化。

## 大数据处理系统的分类

以负载类型作为划分依据，可以将现有的大数据处理系统分为：

* 批处理系统：高吞吐量，如Hadoop等；
* 流式计算系统：时效性，如Dstream，Storm等；
* 交互式查询系统：如数据仓库等；

目前，现有框架主要适用于集合、表、图和矩阵等数据类型，作者将其分类如下：

   | 批处理 | 交互式 | 流计算
---| --- | --- | ---
集合|**Spark**/**MapReduce**/Dryad/DryadLINQ| |**Dstream**/Storm/MillWheel
表|Piccolo|Shark/**Hive**/Impala/Dremel|
图|PowerGraph/Pregel|Tao|
矩阵|MadLINQ

## 大数据处理系统的研究进展

作者从编程框架、大规模图计算和分布式机器学习三个方面对现今大数据处理系统的状况进行阐述，分别分析其优缺点。

### 1. 基于数据流模型的编程框架
现今绝大部分的编程框架都可以归结为数据流模型，所谓数据流模型就是使用有向无环图（Directed Acyclic Graph, DAG）表达一个计算，图中顶点表示计算任务而边表示数据依赖（下图来自于[[4]](http://www.jos.org.cn/1000-9825/4558.html)）。  
![DAG](http://i.imgur.com/a98E96j.jpg)

* **MapReduce**
 * 优点[1]：  
	* 良好的系统和数据可扩展性（Scale out）:以增加服务器节点的方式扩展；  
	* 容错性好：如副本机制等；
	* 数据本地化（Locality）：计算节点优先负责本地数据；
	* 顺序处理：以顺序化的访问方式实现高带宽、高速度的数据访问和传输；
	* 简洁性：仅提供Map和Reduce两个抽象编程接口，隐藏系统层细节；
 * 缺点：  
    * Map执行完成后才可以执行reduce，无法表达任务间拓扑结构；  
    * 只能以临时文件的方式传输map和reduce的中间结果；  
    * 启动时间长，不适合时效要求高的场景；  
    * 迭代式机器学习会造成大量磁盘读写和网络传输开销，导致运行效率底下；
* **Dryad**
 * 优点：  
    * 采取通用DAG模型，可以灵活表达任务间拓扑结构；  
    * 提供共享内存、TCP管道、临时文件、DFS等多种数据传输机制；  
 * 缺点：  
    * 需要显式构建拓扑结构，带来编程负担； 
* **Spark**  
 Spark的核心思想：使用DAG表达一个完整的数据处理过程，其中DAG顶点表示弹性分布式数据集（resilient distributed dataset, RDD），边表示转换操作。如今主要以批处理为基础，集成了流计算DStream、图计算GraphX、机器学习算法库MLlib等。
 * **RDD**是迭代计算中反复使用的中间数据集的一种抽象，表示一个只读记录组成的集合；
    * RDD分片存储到多台机器，**并行**执行粗粒度（多所有数据同时处理）的转换，提升执行效率；
    * 一个任务经历多个转换再输出（即‘**流水线**’），提升执行效率；
    * 允许显式将RDD加载驻留在**缓存**，极大提升迭代计算的执行效率； 
 * **Lineage**是Spark维护的RDD之间的依赖关系，使容错变得简单易行；
* **高级库和语言**  
 目前已经出现了许多高级语言和库如Pig、DryadLINQ、FlumeJava、Hive等，而所谓高级语言，主要采取的方式是将Hadoop封装到下层作为执行引擎，上层是所谓的面向领域的编程语言或者高级库，由中间的转换层将上层的抽象自动翻译为下层的hadoop作业。  


 > 执行引擎Hadoop <=> 中间转换层 <=> 面向领域的编程语言(Domain Specific Language, DSL)或高级库

### 2. 图计算
* 幂律分布  
 所谓幂律分布，即图顶点的分布极不均匀，极少的顶点通过大量的边与大量的顶点发生关联。现实世界中普遍存在的幂律分布导致图数据难以均匀切分，从而为机器带来**负载不均**和大量的**网络通讯开销**问题，严重影响计算机运行效率。

* 图数据切分方法  
 图数据切分方法主要由两种：切点法和切边法。而其衡量切分性能的主要依据包括：机器负载均衡性和网络通信量，对于符合幂律分布的图数据**切点法**要比切边法效率高出一个数量级。  

* 现有图数据系统  
 图数据领域现有系统主要分为两类：在线查询的图数据库（Facebook的Tao）以及离线图分析系统（Pregel，GiraphLab等）。  
 Pregel是以顶点为中心的编程模型，针对图顶点编写计算函数并采用**同步**的方式执行，即在一轮迭代中执行完所有顶点的计算函数后，在下一轮迭代中才能访问并使用上一轮迭代的状态变化。  
 GraphLab对Pregel进行改进，将完整的顶点计算函数进一步划分为三个连续的子处理阶段：Gathe、Apply和Scatter，各子阶段可以细粒度地**异步**并发执行。由于异步执行，所以算法收敛速度快，吞吐量高、执行高效，但难以判断输出结果正确性，且学习成本高。

### 3. 分布式机器学习系统
 * 分布式机器学习难点
  * 通信  
   分布式环境下，全局参数需要通过网络进行存取，如何提供通信效率或者减小通讯量对运行效率至关重要。
  * 负载  
   大量并发任务地负载不均会导致整体完成效率降低。
  * 容错  
   集群机器发生故障后，系统应当程序能够容错并运行正确。

* 分布式机器学习系统
 * 基于Hadop：Mahout  
  由MapReduce提供计算接口，算法实现复杂，且迭代计算过程中过于频繁读写磁盘，导致运行**效率低**下。
 * 基于Spark：MLlib  
  较为成熟，运行效率较高。
 * 参数服务器：深度学习  
  参数服务器包括多台**参数服务器**和大量**并发执行地客户端**。  
  参数服务器用于存储全局参数，通常采用Master-slave结构，其中一台作为主控节点，负责对全局参数进行数据分片和路由。  
  客户端用于并发执行训练过程，可以读取或更新全局参数。

### 4. 发展趋势  
 * 大规模并行  
  利用CPU和GPU组成异构并行硬件平台来加速计算。  
 * 自动化并行  
  由程序员编写传统串行代码，通过程序分析技术实现串行代码自动并行化。
 * 混合编程  
  现有各计算框架有各自的适用领域，相互独立导致计算之间只能以粗粒度的方式组合，如何打破框架壁垒，是之更灵活高效的组合是未来的发展趋势。

## 其他
1. 数据偏斜是导致任务负载不均衡和出现拖后腿现象的主要原因；

## 个人体会
1. 作者分析了各平台框架的优劣，但似乎Spark几乎毫无破绽，这个肯定不可能，笔者对于这些接触不长，我相信spark必然有着短板，但目前是最佳的解决方案，所以接下来一段时间，**Spark才是主流**。
2. 对于机器学习，在大体量的数据之下，分布式必然优于单机，所以对于传统的机器学习最佳选择是MLlib，而近年崛起的深度学习似乎作者推崇备至，本人对于深度学习的理解暂时也不多（我怎么啥都不知道？！），之前个人理解深度学习是从多层感知机->神经网络->深度学习，这三者之间的区别仅在于隐含层的层数，但看完这篇文章感觉好像传统的机器学习方法其实也是变种的深度学习？  
 至此突然惊觉，为什么他敢叫深度学习，统计学习、机器学习、深度学习好像是并列的，深度学习并非机器学习的子学科，所以**深度学习**会继续高潮下去？

## 参考文献
[1] 顾荣.大数据处理技术与系统研究[D].南京：南京大学，2016   
[2] Laney D. 3D data management: Controlling data volume, velocity and variety[J]. META Group Research Note, 2001, 6: 70.  
[3] 维基百科编者. 大数据[G/OL]. 维基百科, 2017(20170321)[2017-03-21]. https://zh.wikipedia.org/w/index.php?title=%E5%A4%A7%E6%95%B8%E6%93%9A&oldid=43697979.  
[4] 孙大为, 张广艳, 郑纬民. 大数据流式计算：关键技术及系统实例[J].软件学报,2014, (4): 839-862.