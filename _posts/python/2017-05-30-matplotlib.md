---
layout: post
title: matplotlib当中的小技巧
date: 2017-05-30
author: xiaoyongsheng
categories: Python
tag: Python

---

* content
{: toc}

---

## 横坐标标签相关

```python
from matplotlib import dates
from matplotlib.ticker import  FormatStrFormatter 

# 横坐标日期格式
fig = plt.figure()
fig.autofmt_xdate()  # 简单的自动优化
ax = fig.add_subplot(1, 1, 1)
ax.plot(xdata, ydata, 'g-')
# 手动设置标签旋转, 注意顺序
ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m'))

#设置x轴标签文本的格式
fmt = FormatStrFormatter('%1.1f') 
ax.xaxis.set_major_formatter(fmt)

#去掉边框  
ax.spines['top'].set_visible(False)  
ax.spines['right'].set_visible(False)  

ax.set_title('title_name')
plt.tight_layout()
plt.savefig('test.png', dpi=200)
```


## 中文显示问题

```python
#coding:utf-8
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号
```


## 参考资料  

[^1]: 周志华.机器学习[M].清华大学出版社,2016.  
