---
layout: post
title: survey-explainable Machine Learning Algorithms
date: 2018-11-16
author: xiaoyongsheng
categories: recommendation
tag: recommendation

---

* content
{: toc}

---

## 可解释的推荐方式

| 解释方式     | 解释                  |
|:-------------|:----------------------|
| itemBased-CF | 你曾买过相似的物品    |
| userBased-CF | 和你类似的人还买了... |
| 基于规则     | 大家还购买了...       |
|              |                       |

## 推荐系统历史

| 推荐算法                     | 可解释性机理                                         | 缺点                           |
|:-----------------------------|:-----------------------------------------------------|:-------------------------------|
| content-based                | 基于item属性进行推荐，推荐理由可以显式的给出item属性 | 生成item属性耗费大量时间       |
| userBased-CF                 | 使用一组item评分向量代表一个user                     | 可解释性差于contentBased       |
| itemBased-CF                 | 使用一组user评分向量代表一个item                     | 可解释性差于contentBased       |
| latent Factor Models(LFM/MF) | 基于latent fator进行预测                             | 适用于评分模型，但是可解释性差 |


## 概念

- model-based explainable recommendation: 推荐算法以可解释的方式同时给出推荐列表和推荐理由；
  - model: LDA(latent dirichlet allocation) / EFM(Explicit Factor Model) / ...
  - 备注： 深度学习的黑盒模式导致可解释性更差；
-
## 分类

### 按照生成理由的类型

1. 文本
2. 图像

### 按照生成理由的模型

1. matrix fatorization
2. topic modeling
3. graph-based
4. deep Learning
5. knowledgge-Graph
6. association rules
7. post-hoc Models

## 展现形式

| 类型                 | 详情                                                                                                                                                                          |
|:---------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| user-based           | 根据用户的反馈（显式/隐式）向用户推荐和他相似的人群喜欢的内容，最好是直接展示用户熟识的一度关系的喜好                                                                         |
| item-based           | 根据用户喜欢过的物品向其推荐相似物品                                                                                                                                          |
| content-based        | 基于用户行为和物品属性进行推荐，（比如通过雷达图表示出物品属性和多个用户的偏好进行直观展示；或者使用用户的基础信息进行推荐，如年龄、性别、职业等：80%的同龄人买了这件商品；） |
| textual explanations |                                                                                                                                                                               |
| visual explanations  |                                                                                                                                                                               |
| social explanations  |                                                                                                                                                                               |
| hybrid explanations  |                                                                                                                                                                               |
