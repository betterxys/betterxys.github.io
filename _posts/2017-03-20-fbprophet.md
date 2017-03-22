---
layout: post
title: 时间序列开源工具-fbprophet
date:  2017-03-20
author: xiaoyongsheng
By: xiaoyongsheng
email: xiaoyongsheng@hotmail.com  
categories: Statistical_Learning
tag: 时间序列

---

* content
{:toc}

参考文章：Sean J.Taylor, Ben letham (facebook)：https://research.fb.com/prophet-forecasting-at-scale/

----

fbprophet是2017年2月23日由facebook[开源](https://github.com/facebookincubator/prophet)的专门用于解决时间序列预测问题的开源库，提供了python和R两种接口，笔者亲自尝试了一番，使用简单且表现极其优秀，但文档不全，这个问题随着接触prophet的朋友越来越多会不断完善。本文将以fb的[研究报告](https://research.fb.com/prophet-forecasting-at-scale/)为基础对其实现原理进行简要描述。  

## Prophet存在的意义
在业务预测的实践当中往往会面临两个问题：  
   1. 全自动的预测技术通常较为表现较为一般且不够灵活；  
   2. 能够提供足够精确的预测分析的专业分析师人员短缺；

Prophet不仅能够解决上述两个问题，更是将重点放到了“forecasting at scale”的“scale”之上：  
 1. 计算：能够非常简便的实现众多时间序列**并行**预测；
 2. 存储：可以存储到关系型数据库(Mysql)或者数据仓库(Hive)当中；  

## Prophet主要针对的对象
 1. 时间序列历史数据：有一定数量的以小时/天/周等为观测周期的历史数据；
 2. 受季节性影响：如每周有类似波动，或每到每年的固定时间都会有类似波动产生；
 3. 节假日：受节假日影响的时间序列（prophet可以导入不规则周期的重要节假日）；
 4. 有限异常值：缺失值或者异常值数量应当保持在合理范围内；
 5. 趋势变化：存在长期趋势（线性或者非线性）；

## Prophet的优势
1. 操作简单  
 Prophet的默认设置对于绝大部分的时序预测问题已经有了足够好的表现，但是如果你对其表现仍不满意，那么即便你是一个没有任何统计学背景的小白，也依然可以简单地通过调整prophet提供的接口参数来继续提升prophet的准确率直至你满意为止。  

2. python开源库  
 时间序列预测方法开源库基本都是R语言的开源库（如下三个都是及其经典的时间序列预测开源项目），很少有python的开源库，如今Facebook的Prophet弥补了这个不足，同时提供python和R接口。
 - Rob Hyndman的R语言开源库：forecast：http://robjhyndman.com/software/forecast/   
 
  > 【论文】Hyndman R J, Khandakar Y. Automatic time series for forecasting: the forecast package for R[R]. Monash University, Department of Econometrics and Business Statistics, 2007.  
 - Google的R语言开源库：CausalImpact：https://google.github.io/CausalImpact/  
 
  > 【论文】Brodersen K H, Gallusser F, Koehler J, et al. Inferring causal impact using Bayesian structural time-series models[J]. The Annals of Applied Statistics, 2015, 9(1): 247-274.  

 - Twitter的R语言开源库：AnomalyDetection：https://github.com/twitter/AnomalyDetection  

  > 【博客】https://blog.twitter.com/2015/introducing-practical-and-robust-anomaly-detection-in-a-time-series

3. 合理、精准的预测  
 提供了ARIMA、指数平滑等众多时间序列的预测方法以供选择；

4. 简易、灵活的预测方法  
 - 提供季节性平滑参数以适应周期性影响；  
 - 提供趋势性平滑参数以适应历史走势影响；
 - 为增长曲线提供“capacities”参数作为上下限约束条件；  
 - 可以指定节假日，如黑色星期五、感恩节、the Super Bowl（橄榄球比赛）；

## Prophet工作原理
 Prophet采用的是统计学中的加法模型（Additive Model, AM）<sup>[1][2]</sup>，主要考虑四方面因素的影响：
 1. 分段的linear/logistic趋势： Prophet自动检测数据中各段分割点；
 2. 季节性影响-年： 采用傅里叶级数<sup>[3]</sup>建模；
 3. 季节性影响-周： 采用虚拟变量法<sup>[4][5]</sup>(虚拟变量为0/1以决定是否对输出产生影响)；
 4. 重要节假日：可由用户自定义；

## 其它
1. Prophet可以画出总体趋势（trend）、一年内的趋势(yearly trend)、一周的趋势(weekly trend)来更加直观、更加灵活的调节每个组成成分的模型以达到改进模型性能的目的。

## 参考文献
[1] Friedman J H, Stuetzle W. Projection pursuit regression[J]. Journal of the American statistical Association, 1981, 76(376): 817-823.  
[2] Additive model. (2016, November 18). In Wikipedia, The Free Encyclopedia. Retrieved 03:06, March 20, 2017, from https://en.wikipedia.org/w/index.php?title=Additive_model&oldid=750292281  
[3] Fourier series. (2017, January 30). In Wikipedia, The Free Encyclopedia. Retrieved 03:16, March 20, 2017, from https://en.wikipedia.org/w/index.php?title=Fourier_series&oldid=762814082  
[4] Dummy variable (statistics). (2016, December 5). In Wikipedia, The Free Encyclopedia. Retrieved 03:20, March 20, 2017, from https://en.wikipedia.org/w/index.php?title=Dummy_variable_(statistics)&oldid=753174921  
[5] Skrivanek S. The use of dummy variables in regression analysis[J]. More Steam, LLC, 2009.
