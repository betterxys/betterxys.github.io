---
layout: post
title: 使用RNN之LSTM进行时序预测
date: 2017-03-24
By: xiaoyongsheng
categories: Machine_Learning
tag: TensorFlow

---  

* content
{: toc}

# 本文目标  
对于时间序列的预测是金融、经济等等领域广泛的需求，本文以一组价格数据为例对该组价格时序采用LSTM进行预测，以观察其效果。  
[所有代码以及示例数据在此](https://github.com/betterxys/tensorflow-lstm-regression)

# 数据概述  
本例数据如下表所示：  

  | t | s  
---|---|---  
 0|2013-12-13|1087.50  
 1|2013-12-20|1453.33  
 2|2013-12-27|1630.00  
 3|2014-01-03|1675.00  
...|...|...  
148|2016-10-14|671.37  

其中，t代表的日期，s代表的是该日期对应的价格。显然日期字段记录的日期并非连续日期，两两间隔七日，这是由于该价格本身的性质决定的，该价格仅在每周五更新，所以导致所有有效记录日期均为周五。历史价格共有149条记录，从2013年12月13日开始不间断记录至2016年10月14日截止，其时序图如下：

![时序图](https://github.com/betterxys/tensorflow-lstm-regression/tree/master/figures/sequence.png)

本例数据是一个典型的时间序列问题，常用的解决方案是采用**时间序列分析方法**，笔者在另一篇[博文](https://betterxys.github.io/2017/03/20/fbprophet/)介绍的facebook开源工具fbprophet就是采用时间序列分析方法对此类时间序列问题进行预测的典型代表。而本文将采用神经网络当中的RNN对时间序列进行预测，后续会将fbprophet和RNN的结果进行对比。

# RNN简介
RNN（Recurrent Neural Networks）是神经网络的一种，常用于语音和文本序列的分析，其优势在于引进了过去数据对现在的影响，而LSTM（Long Short Term Memory networks）是RNN的一个变种，RNN对于过去很久的事情没有很好的记忆效果，而LSTM就是用来解决这个问题的，因此称之为长短期记忆模型。  
如果有时间，后续会补充RNN的知识，暂时先推荐一篇博文[Understanding LSTM Networks](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)，这篇文章是tensorflow官方推荐的RNN入门文章并给予极高评价，简单直观，值得一读。

# 参考文献  
【1】 Mourad Mourafiq. Sequence prediction using recurrent neural networks(LSTM) with TensorFlow: http://mourafiq.com/2016/05/15/predicting-sequences-using-rnn-in-tensorflow.html, 2016.05.15  
【2】 Colah. Understanding LSTM Networks: http://colah.github.io/posts/2015-08-Understanding-LSTMs/, 2015.08.27
