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

## 0705

### 判断二叉搜索树

> 本题是在Boss直聘看到的，有家创业公司（小库科技， 建筑AI）直接把题目贴出来，说有答案请联系我，还挺有个性的。

以复杂度O(n)判定一棵树是否为二叉搜索树。

- 原始思路  
首先，既然要判定是否是二叉搜索树，我得先构造一棵树，所以第一步要学学如何构造二叉树，然后再去琢磨如何判定。


```python

def isbst(node, min, max):
    if node is None:
        return True
    return isbst(left_node, min, node) && isbst(right_node, node, max)

```

## 0712  

### 字典排序

> 给定一组dict, 其中key是str类型, value是float型，请根据value的大小对key进行排序

- 原始思路
 将key和value拆分为两个list,对list进行排序，排序进行的同时对key进行排序：

  - 首先实现排序算法，以快排为例：

  ```python
  def qs(input_list):
      return quick_sort(input_list, 0, len(input_list)-1)

  def quick_sort(lst, left, right):
      if left >= right:
          return lst
      else:
          key = left
          lp = left
          rp = right
          while lp < rp:
              while lst[rp] >= lst[key] and lp < rp:
                  rp = rp - 1
              while lst[lp] <= lst[key] and lp < rp:
                  lp = lp + 1
              print(lst, lp, rp, key)
              lst[lp], lst[rp] = lst[rp], lst[lp]
          lst[left], lst[lp] = lst[lp], lst[left]
          lst = quick_sort(lst, left, lp)
          lst = quick_sort(lst, rp+1, right)
          return lst
  ```

  - 其次，按照原本思路，根据key值或者value值对dict items进行排序：

  ```python
  def qs_dict(input_dict, rv=False):
      return dict_quick_sort(input_dict.items(), 0, len(input_dict)-1, rv=rv)

  def dict_quick_sort(lst_dict, left, right, rv=False):
      """ if rv = False, output items ordered with key;
      if rv = True, return items ordered with values;
      """
      if left >= right:
          return lst_dict
      elif rv == True:
          lst = [j for i,j in lst_dict]
      else:
          lst = [i for i,j in lst_dict]
      key = left
      lp = left
      rp = right
      while lp < rp:
          while lst[rp] >= lst[key] and lp < rp:
              rp = rp - 1
          while lst[lp] <= lst[key] and lp < rp:
              lp = lp + 1
          print(lst_dict, lp, rp, key)
          lst_dict[lp], lst_dict[rp] = lst_dict[rp], lst_dict[lp]
      lst_dict[left], lst_dict[lp] = lst_dict[lp], lst_dict[left]
      lst_dict = dict_quick_sort(lst_dict, left, lp, rv=rv)
      lst_dict = dict_quick_sort(lst_dict, rp+1, right, rv=rv)
      return lst_dict
  ```

- 反思

  其实，最开始的想法是dict自己有没有类似这种排序方法, 可惜好像并没有，
  但是意外之喜是python内建函数sorted其实可以简单的实现这个功能：

   ```python
  sorted(input_dict.items(), key = lambda d: d[0])  # 按照key进行排序
  sorted(input_dict.items(), key = lambda d: d[1])  # 按照value进行排序
   ```
