---
layout: post
title: 面试题目 
date:  2017-06-26
author: xiaoyongsheng
categories: interview
tag: 面试
---

* content
{:toc}

---

## 0626

### 上台阶

一个楼梯共有n阶，每次只能上一阶或者两阶，问共有多少种方式走完整段楼梯？  

- 解题思路  
 这是一个递归的思路，因为当剩余台阶大于等于2阶时，都会面临两个选择：下1阶或者2阶，代码如下：  

 ```python
def upstairs(n):
    if n > 0:
        print('steps:{0}\tposibilities:{1}'.format(n, step(n)))
    else:
        print('sorry! illegal input!')


def step(n):
    """step by step like the pace of the devil.
    
    Params:
        n:   total steps.

    Return:
        count of posibilities.
    """
    if n == 2:
        return 2
    elif n == 1:
        return 1
    elif n == 0:
        return 0
    elif n > 2:
        return step(n-1) + step(n-2)

if __name__ == '__main__':
    for i in range(10):
        upstairs(i)
 ```
 - 原始思路  
 很少面试，也很少涉及面试的时候写代码这种事情，所以，当时思路是这样的：  

 > 将本题转换为数学题：  
 > $$1 * a + 2 * b = n$$  
 > 其中，a代表了下1阶台阶的次数，b代表了下2阶台阶的次数，n代表台阶总数；  
 > 在给定n的情况下，会有多组（a,b）的值，(a,b)的个数就是本题“组合”数；
 > 而具体有多少种方案就是各个“组合”的“排列”值的总和；
 >
 > 这样实现起来的时候首先需要求多组(a,b)，然后把a个1,b个2转换为list，再求每个list所有的可能“排列”，计算复杂，占用空间巨大，扯到蛋了。
 >


