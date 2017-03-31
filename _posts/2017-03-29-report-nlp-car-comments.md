---
layout: post
title: 读书报告-社会化情境下用户在线评论数据挖掘模型构建研究
date: 2017-03-29
author: xiaoyongsheng
categories: NLP BookReport
tag: 文本挖掘

---

* content
{: toc}

阅读文献：姜霖. 社会信息化情境下用户在线评论数据挖掘模型构建研究——以汽车行业负面观点评论自动抽取系统为例[J]. 情报科学, 2016 (8): 143-147 170.  
关键词：观点评论挖掘
---

## 1. 引言

- 观点评论的信息功能：
    1. 透露事物的自在信息，即事物自我显示的信息；  
    2. 揭示事物的本质信息；  
    3. 期待信息反馈；  

- 评论信息挖掘的研究意义：
    1. 从信息的角度：当今网络环境信息量巨大，在许多情况下尤其是博客和论坛当中，大量文本中仅有极少部分文字才是真正具有实际意义的；  
    2. 从应用的角度：数据分析能力越强，对决策的支持能力就越强，负面评论的挖掘可以及时提供舆情预警，最大程度的减少损失；  

## 2. 中文网络评论观点抽取现状

- 对新闻报道的褒贬分类研究  
    Tsou B K Y, Yuen R W M, Kwong O Y, et al. Polarity classification of celebrity coverage in the Chinese press[C]//Proceedings of International Conference on Intelligence Analysis. 2005.  

- BBS热门话题挖掘  
    邱立坤, 龙志祎, 钟华, 等. 层次化话题发现与跟踪方法及系统实现[J]. 廣西師範大學學報 (自然科學版), 2007, 25(2): 157-160.  
    邱立坤, 程葳, 龙志稀. 面向 BBS 的话题挖掘初探 [C][J]. 自然语言理解与大规模内容计算. 北京: 清华大学出版社, 2005: 401-407.  

- 汽车论坛评论挖掘系统  
    姚天昉, 聂青阳, 李建超, 等. 一个用于汉语汽车评论的意见挖掘系统 [C][C]//中文信息处理前沿进展-中国中文信息学会二十五周年学术会议论文集. 北京: 清华大学出版社, 2006: 260-281.  

作者研究的重点是：***语义极性分析*** 和***观点抽取***；  
本文的创新之处是：通过Google的label propagation算法进行词极性分类；  

## 3. 系统模型构建

数据来源：爬虫获取汽车论坛和新浪微博中有关汽车的用户评论；  
技术：自然语言处理；  
目标：构建汽车行业负面观点评论的自动抽取系统；  

```flow  
st=>start: Start
e=>end
op=>operation: My Operation
cond=>condition: Yes or No?

st->op-cond
cond(yes)->e
cond(no)->op
```


---
## 参考文献
【1】姜霖. 社会信息化情境下用户在线评论数据挖掘模型构建研究——以汽车行业负面观点评论自动抽取系统为例[J]. 情报科学, 2016 (8): 143-147 170.  
【2】Tsou B K Y, Yuen R W M, Kwong O Y, et al. Polarity classification of celebrity coverage in the Chinese press[C][J]//Proceedings of International Conference on Intelligence Analysis. 2005.  
【3】邱立坤, 龙志祎, 钟华, 等. 层次化话题发现与跟踪方法及系统实现[J]. 廣西師範大學學報 (自然科學版), 2007, 25(2): 157-160.   
【4】邱立坤, 程葳, 龙志稀. 面向 BBS 的话题挖掘初探 [C]. 自然语言理解与大规模内容计算. 北京: 清华大学出版社, 2005: 401-407.  
【5】姚天昉, 聂青阳, 李建超, 等. 一个用于汉语汽车评论的意见挖掘系统 [C][C]//中文信息处理前沿进展-中国中文信息学会二十五周年学术会议论文集. 北京: 清华大学出版社, 2006: 260-281.  
