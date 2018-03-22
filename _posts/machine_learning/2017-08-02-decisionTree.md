---
layout: post
title: 机器学习算法之决策树
date: 2017-08-02
author: xiaoyongsheng
categories: Machine_Learning
tag: 机器学习

---

* content
{: toc}

---
## 写在前面
>碍于时间关系，本文不再对各算法发表的paper进行标注，仅对本文所参考的文献来源进行标注; 

决策树(decision tree)无疑是机器学习领域最为经典的模型之一，本文意在回顾决策树算法的基本流程及其关键点，需要明确以下几点：

- 决策树算法的优缺点机器适用场景
- 决策树的基本流程
- 决策树的种类及各种类之间的区别

## 决策树的大事记
李航[^2]在其统计学习方法的决策树一章认为决策书学习的主要思量来源于以下三个方面：

- 1984年Breiman等提出 CART(classification and regression tree)
- 1986年Quinlan提出 ID3
- 1993年提出 C4.5

## 决策树的优缺点

> [sklearn doc](http://scikit-learn.org/stable/modules/tree.html)[^3]:  
>Some advantages of decision trees are:
- Simple to understand and to interpret. Trees can be visualised.
- Requires little data preparation. Other techniques often require data normalisation, dummy variables need to be created and blank values to be removed. Note however that this module does not support missing values.
- The cost of using the tree (i.e., predicting data) is logarithmic in the number of data points used to train the tree.
- Able to handle both numerical and categorical data. Other techniques are usually specialised in analysing datasets that have only one type of variable. See algorithms for more information.
- Able to handle multi-output problems.
- Uses a white box model. If a given situation is observable in a model, the explanation for the condition is easily explained by boolean logic. By contrast, in a black box model (e.g., in an artificial neural network), results may be more difficult to interpret.
- Possible to validate a model using statistical tests. That makes it possible to account for the reliability of the model.
- Performs well even if its assumptions are somewhat violated by the true model from which the data were generated.
>
>The disadvantages of decision trees include:
- Decision-tree learners can create over-complex trees that do not generalise the data well. This is called overfitting. Mechanisms such as pruning (not currently supported), setting the minimum number of samples required at a leaf node or setting the maximum depth of the tree are necessary to avoid this problem.
- Decision trees can be unstable because small variations in the data might result in a completely different tree being generated. This problem is mitigated by using decision trees within an ensemble.
- The problem of learning an optimal decision tree is known to be NP-complete under several aspects of optimality and even for simple concepts. Consequently, practical decision-tree learning algorithms are based on heuristic algorithms such as the greedy algorithm where locally optimal decisions are made at each node. Such algorithms cannot guarantee to return the globally optimal decision tree. This can be mitigated by training multiple trees in an ensemble learner, where the features and samples are randomly sampled with replacement.
- There are concepts that are hard to learn because decision trees do not express them easily, such as XOR, parity or multiplexer problems.
- Decision tree learners create biased trees if some classes dominate. It is therefore recommended to balance the dataset prior to fitting with the decision tree.


### 优点

- 白箱模型，具备可读性
- 较短时间对较大数据源作出可行且效果良好的结果，训练代价是log(n)
- 可以同时接受连续型和离散型特征，需要极少的数据预处理过程
- 可以使用统计检验方法算出其模型置信度


### 缺点

- 容易过拟合
- 不稳定，数据的微小变动会引起模型产生比较大的变化
- 树的生成过程是贪婪的，只能找到局部最优
- 有些逻辑难以表示，如异或等
- 对数据分布有一定要求，数据分布不平衡会有比较大的问题

## 决策树建模流程
主要包括特征的选择和模型的选择两部分，其中模型的选择又可分为模型的局部选择和模型的全局选择，分别对应于决策树的生成过程和剪枝过程[^2]。
### 特征选择
不同的算法使用不同的评判依据进行特征选择，主要包括一下三种：

#### 信息增益（**ID3**）  

信息论中熵(entropy)表示随机变量的不确定性：

$$H(X)=\sum_{i=1}^{n}p_i log{p_i}$$


令\\(H(D)\\)表示集合D的熵， \\(H(D\|A)\\) 表示特征A给定条件下D的条件熵，则特征A对数据集D的信息增益可以表示为：

$$g(D, A) = H(D) - H(D|A)$$

这种方法存在一定的问题：偏向于取值多的特征

#### 信息增益率（**C4.5**）  

$$ H_A(D) = - \sum_{i=1}^n \frac {|D_i|} {|D|} \log \frac {|D_i|} {|D|}$$

$$ g_R(D, A) = \frac {g(D, A)} {H_A(D)} $$

其中， n是A的特征取值个数。

#### 基尼系数（**CART**）  
Gini系数又称Gini不纯度，就像字面意思一样，描述的是一个集合的不纯度，若集合D有K个不同的类别，则D的GIni系数就是:

$$Gini(D) = 1 - \sum_{k=1}^{K}p_k^2$$

选定特征A后，特征A下的基尼系数定义为:

$$Gini(D, A) = \sum_{i=1}^n p_i Gini(D_i)$$


### 决策树的生成

- ID3和C4.5生成算法
    - **多叉树**
    
    - 算法停止条件
        - 特征的信息增益小于预定阈值
        - 没有特征可以选择
        
- CART生成算法

    - 递归构建**二叉决策树**

    - 根据Gini系数选择**最优特征**以及**最优切分点**

    - 算法停止条件
    	- 结点样本数小于预定阈值
    	- 样本集的Gini系数小于预定阈值
    	- 没有更多特征

### 决策树的剪枝
决策树的剪枝过程是全局优化的过程，其优化目标包括：

 - 减小损失函数
 
 - 降低模型复杂度
 
 树 T 的叶节点个数为 \|T\| , 叶节点 t 有\\(N_t\\)个样本点, \\(H_t(T)\\) 为叶节点 t   上的经验熵其损失函数可以定义为：
 
 $$C_\alpha(T) = \sum_{t=1}^{|T|} {N_t H_t(T)} + \alpha|T| $$

第一项是模型对训练数据的预测误差，第二项代表模型的复杂度，参数 \\(\alpha >= 0\\) 控制两者之间的影响

## 参考文献  

[^1]: 周志华.机器学习[M].清华大学出版社,2016.  
[^2]: 李航. "统计学习方法." 清华大学出版社, 北京 (2012).
[^3]: Decision Trees — scikit-learn 0.18.2 documentation. (2017). Scikit-learn.org. Retrieved 5 August 2017, from http://scikit-learn.org/stable/modules/tree.html