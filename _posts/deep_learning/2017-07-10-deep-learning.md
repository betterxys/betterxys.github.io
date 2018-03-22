---
layout: post
title: DeepLearning-ch5-机器学习基础
date: 2017-07-06
author: xiaoyongsheng
categories: Deep_Learning
tag: 深度学习

---

* content
{: toc}

---

## 基础概念

- 深度学习： 计算机从经验中学习，并根据层次化的概念体系来学习，而每个概念则通过与某些相对简单的概念之间的关系来定义;

- 机器学习： 从原始数据中提取模式;

- 学习：对于某类任务T和性能度量P，一个计算机程序被认为可以从经验E中学习是指，通过经验E改进后，它在由性能度量P衡量的性能有所提升[^2];

- 独立同分布假设（i.i.d.assumption）： 每个数据集的样本之间都是相互独立(independent)的，训练集和测试集数据采自相同的分布(identically distributed);

- 奥卡姆剃刀(Occam's razor): 在同样能够解释已知观测现象的假设中，我们应该挑选"最简单"的那个;

- VC维(Vapnik-Chervonenkis dimension): 二元分类器能够分类的训练样本的最大数目;









## 机器学习算法的决定因素

1. 降低训练误差 -> 欠拟合(underfitting)  
2. 缩小训练误差和测试误差间的差距 -> 过拟合(overfitting)

可以通过调整模型容量(capacity)控制模型偏向过拟合/欠拟合, 所谓模型容量是指模型拟合各种函数的能力，控制模型容量的方法有:

- 模型选择: 通过改变输入特征的数目和这些特征的参数以选择合适的假设空间(hypothesis)




## 参考资料  

[^1]: Yoshua Bengio:Deep Learning.  
[^2]: Mitchell. 1997  
