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


## 参考资料  

[^1]: 周志华.机器学习[M].清华大学出版社,2016.  
[^2]: 机器学习中的范数规则化之（一）L0、L1与L2范数:http://blog.csdn.net/zouxy09/article/details/24971995.  
