---
layout: post
title: 机器学习-模型评估与选择
date: 2017-06-02
author: xiaoyongsheng
categories: Machine_Learning
tag: 机器学习

---

* content
{: toc}

---

## 1 评估方法  

所谓评估方法就是将样本集拆分为训练集和测试集以评估其泛化误差。常见手段包括留出法(hold out)、交叉验证(cross validation)和自助法(bootstrapping)三种方式，其中**留出法和交叉验证法适用于大样本，自助法适用于小样本**[^1]。  

**分层抽样**: 保留类别比例的抽样方法，适用于留出法和交叉验证；

### 1.1 留出法  

将数据集拆分为训练集和测试集两个互斥子集；通常多次划分、重复试验取均值。

### 1.2 交叉验证法  

将样本集划分为k个互斥的大小相似的子集，每次取其中之一作为测试集，其余作为训练集，取k轮均值作为最终结果。

### 1.3 自助法  

给定大小为m的数据集D,有放回采样m次得到训练集，未被采样的样本作为测试集，测试集约占总体的0.368。

$$  
\lim_{x\to\infty} (1-\frac {1} {m})^m \rightarrow \frac {1} {e} \approx 0.368
$$

## 2 性能度量

### 2.1 回归-性能度量

评价指标|公式
----|-----
Absolute Error|$$ae_i = \hat{y_i} - y_i$$
Relative Error|$$re_i = \frac {\hat{y_i} - y_i} {y_i}$$
Mean Absolute Error|$$mae = \frac {1} {n} \sum_{i=1}^{n} \|ae_i\|$$
Mean Square Error|$$mse = \frac{1}{n} \sum_{i=1}^{n} (ae_i)^2 $$
Root Mean Square Error|$$rmse = \sqrt{mse} $$
Mean Absolute Percentage Error|$$mape = \frac{1}{n} \sum_{i=1}^{n} \|re_i\| $$

### 2.2 分类-性能度量

#### 2.2.1 confusion matrix

| | $$ \hat{y}=Positive $$ | $$ \hat{y}=Negative $$
------------|--------------------|--------------------
$$ y=Positive $$| TP | FN
$$ y=Negative $$| FP | TN

#### 2.2.2 Precision-Recall

$$ Precision: P = \frac {TP}{TP+FP} $$  

$$ Recall: R = \frac {TP}{TP+FN} $$  

$$ F1: \frac{1}{F_1} = \frac{1}{2} (\frac{1}{P} + \frac{1}{R})$$  

$$ F_\beta: \frac{1}{F_\beta} = \frac{1}{1+\beta^2} (\frac{1}{P} + \frac{\beta^2}{R})$$


- 对于$$F_\beta$$而言, 当\beta>1时更偏好recall, 反之亦然;  

- $$F_1$$是$$F_\beta$$的一种特殊情况，当$$\beta=1$$时，$$F_\beta$$=$$F_1$$;  

## 3 模型选择策略

模型选择的策略包括两个方面：
 - 经验风险最小化(empirical risk minimization)  

  $$min \frac{1}{N} \sum_{i=1}^{N}L(y_i, f(x_i)) $$  

  所谓经验风险最小化,是指损失函数的值越小越好;  

 - 结构风险最小化(structural risk minimization)  

  $$min \frac{1}{N} \sum_{i=1}^{N}L(y_i, f(x_i)) + \lambda J(f) $$  

  结构风险最小化, 就是正则化(regularization), 正则化项代表的是模型的复杂度, 损失函数和复杂度同时小才是真的好!  

正则化项[^2]一般包括三种：

 - $$L_0$$ ： 非零分量的个数; 更倾向于稀疏(期望系数为0);  
 - $$L_1$$ ： 各分量元素绝对值之和; 倾向于稀疏(期望系数为零);   
 - $$L_2$$ ： 各分量平方和的平方根; 倾向于各分量取值均衡(期望系数尽量小,但非零),非零分量个数尽量稠密;


## 4 算法的适用场景

算法不说千千万万也差不多了，那么到底什么时候采用什么算法才会有比较好的结果呢？这个当然没有定论，但肯定是值得探讨的。

### 4.1 没有免费的午餐

在接触机器学习之初，我的导师曾经跟我说过，你没办法说哪个模型最好，只有最适合你这份数据的，此后，我又接触到"no freee lunch"[^2][^3]这种说法，简单来说就是模型的最终期望性能与算法无关！所以我心目中对此也好不怀疑，是骡子是马，拉出来溜溜就行了，所有能用的算法都跑一遍，哪个表现好，就用哪个呗，让事实说话不是更有说服力嘛！  
但在经历了这么多的面试之后，我的这种想法有些变化了，以上说法其实是指单纯的对比这些算法那个好哪个差是没有意义的，但不同的数据必然会有更合适的算法存在，所以本节要总结前人的经验。

### 4.2 不同场景的适用算法

不同的数据会有不同的适用算法，所以需要对数据有所区分，图像、声音等富文本文件必然是采用深度学习无疑，CNN和RNN才是他们的主战场，本节只讨论结构化数据。结构化的数据以二维表的形式存在，分为行和列，所以可供划分的依据有：行的数量、列的数量、列的数据属性、预测目标等，scikit-learn给出了一张辅助选择的路线图。

![](/styles/images/1708/ml_map.png)

sk-learn的这张图是这么划分的:

- 样本集低于50条样本，请回家好好睡一觉；
- 分类：
    + 小样本
        * 优先使用Linear-SVC
        * 其次考虑 naive bayes(文本)、KNN
        * 最终是SVC和Ensemble Classifier
    + 大样本
        * 优先使用SGD Classifier(线性模型的一种)
        * 其次考虑kernel approximation(特征转换的方式，更像是降维？)
- 聚类
    + 半监督
        * 大样本 
            - MiniBatch Kmeans
        * 小样本 
            - 优先考虑Kmeans
            - Spectral Cluster / GMM
    + 无监督
        * 大样本
            - 臣妾做不到啊
        * 小样本
            - MeanShift
            - VBGMM
- 回归：
    + 大样本
        * SGD Regressor
    + 小样本
        * 维度较少
            - Lasso / ElasticNet
        * 维度较多
            - RidgeRegression / SVR(linear)
            - EnsembleRegressors / SVR(RBF)
- 降维：
    + PCA
    + 大样本
        * kernel approximation
    + 小样本
        * Isomap / Spectral Embedding
        * LLE


## 参考资料  

[^1]: 周志华.机器学习[M].清华大学出版社,2016.  
[^2]: 机器学习中的范数规则化之（一）L0、L1与L2范数:http://blog.csdn.net/zouxy09/article/details/24971995.  
[^3]: No free lunch theorem. (2017). En.wikipedia.org. Retrieved 4 August 2017, from https://en.wikipedia.org/wiki/No_free_lunch_theorem
[^4]: Choosing the right estimator — scikit-learn 0.18.2 documentation. (2017). Scikit-learn.org. Retrieved 4 August 2017, from http://scikit-learn.org/stable/tutorial/machine_learning_map/index.html
