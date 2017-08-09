---
layout: post
title: 数据结构之二叉搜索树
date: 2017-08-02
author: xiaoyongsheng
categories: DataStrure
tag: 数据结构

---

* content
{: toc}

---


## 思路整理

本题考察目标在于对数据结构尤其是二叉搜索树的理解，所以首先需要明确二叉搜索树的概念，定义树的结构，实现一棵二叉搜索树，完成树的遍历，最终检验构造出的树是否满足二叉搜索树的要求。

## 基本概念
这里总结一些基本的二叉树类型 [^6] [^7] [^8]:

- 完全二叉树: 除最后一层其余层都是最大节点数，最后一层的叶子节点也都是从左往右紧密排列的; 
  
- 搜索二叉树(binary search tree)：左子树的值小于根节点; 右子树的值大于根节点; 左右子树都是BST;

- 平衡二叉树：左右两个子树的高度差不超过1, 并且左右子树均为碰横二叉树;

## 构造二叉树
二叉树是一种抽象的数据结构，需要自行构造：

```python
class node:
    """implement a binary search tree"""

    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key
```
## 构造二叉搜索树
如题，本文的目标是将一个已排序的数组转换为BST，我们采取递归的方式进行，原本的想法是按顺序逐个往二叉树当中塞，但如此一来会导致这棵树向一个链表一样，一路向右不回头，也就失去了树存在的意义，当然可以通过每插入一个数值重新调整一下二叉树经过旋转使其保持平衡二叉树的模样，但如此以来就会太过复杂，所以从列表的中间开始，以(0+len(list)-1)//2为根节点，其左子节点为其左侧的值，右子节点为其右侧的值，递归进行此操作，可以O(n)的复杂度实现从排序数组到BST的过程[^3] [^9]。
    
```python
def sortedlist2bst(ary, start, end):
    """change a sorted list to binary search tree."""
    if start > end:
        return None
    else:
        mid = (start + end) // 2
        tree = node(ary[mid])
        tree.left = sortedlist2bst(ary, start, mid - 1)
        tree.right = sortedlist2bst(ary, mid + 1, end)
        return tree
```

## 二叉树的遍历
但凡涉及到树的结构，遍历总是绕不过去的，所以本文总结如下四种树的遍历方式[^1] [^4]，其中，前序、中序、后序均属于深度优先，可以采用递归实现，层序遍历采用队列的方式实现：

- 前序遍历: root -> left -> right
- 中序遍历: left -> root -> right 
- 后序遍历: left -> right -> root
- 层序遍历: 从上到下每层从左向右输出


```python
preod = list()
inod = list()
postod = list()
levelod = list()

def preorder(rst):
    if rst:
    preod.append(rst.value)
    preorder(rst.left)
    preorder(rst.right)

def inorder(rst):
    if rst:
        inorder(rst.left)
        inod.append(rst.value)
        inorder(rst.right)

def postorder(rst):
    if rst:
        postorder(rst.left)
        postorder(rst.right)
        postod.append(rst.value)

def levelorder(rst):
    tmp = [rst]
    while tmp:
        node = tmp.pop(0)
        levelod.append(node.value)
        if node.left:
            tmp.append(node.left)
        if node.right:
            tmp.append(node.right)
    return levelod
```
    
    
## 判断一棵树是否是搜索二叉树

较为高效，以O(n)复杂度判断一棵二叉树[^2]是否是BST主要有两个思路：

- 根据BST的性质进行判断：
    - 根节点的值 > 左子树值
    - 根节点的值 < 右子树值

```python
def check_bst(tre, min_value, max_value):
    """Check if a binary tree is a binary search tree."""
    if tre is None:
        return True
    if tre.value < min_value or tre.value > max_value:
        return False
    if check_bst(tre.left, min_value, tre.value) and check_bst(tre.right, tre.value, max_value):
        return True
```

- 根据中序排列后的列表是否为递增序列

```python
def check_bst_2(rst, tmp=-np.inf):
    '''check if an binary tree is BST or not with another method'''
    def check_inorder(rst):
        if rst:
            inorder(rst.left)
            nonlocal tmp
            if tmp >= rst.value:
                return False
            tmp = rst.value
            inorder(rst.right)
    check_inorder(rst)
    return True
```

    
## Reference
[^1]: 数据结构（六）——二叉树 前序、中序、后序、层次遍历及非递归实现 查找、统计个数、比较、求深度的递归实现 - 阿修罗道 - CSDN博客. (2017). Blog.csdn.net. Retrieved 2 August 2017, from http://blog.csdn.net/fansongy/article/details/6798278
[^2]: A program to check if a binary tree is BST or not - GeeksforGeeks. (2009). GeeksforGeeks. Retrieved 2 August 2017, from http://www.geeksforgeeks.org/a-program-to-check-if-a-binary-tree-is-bst-or-not/
[^3]: Sorted Array to Balanced BST - GeeksforGeeks. (2012). GeeksforGeeks. Retrieved 2 August 2017, from http://www.geeksforgeeks.org/sorted-array-to-balanced-bst/
[^4]: Tree Traversals (Inorder, Preorder and Postorder) - GeeksforGeeks. (2009). GeeksforGeeks. Retrieved 2 August 2017, from http://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/
[^5]: python实现二叉树和它的七种遍历 - 九茶 - CSDN博客. (2017). Blog.csdn.net. Retrieved 2 August 2017, from http://blog.csdn.net/bone_ace/article/details/46718683
[^6]: [Data Structure] 数据结构中各种树 - Poll的笔记 - 博客园. (2017). Cnblogs.com. Retrieved 2 August 2017, from http://www.cnblogs.com/maybe2030/p/4732377.html
[^7]: 二元搜尋樹. (2017). Zh.wikipedia.org. Retrieved 2 August 2017, from https://zh.wikipedia.org/wiki/%E4%BA%8C%E5%85%83%E6%90%9C%E5%B0%8B%E6%A8%B9
[^8]: 数据结构 - 树. (2017). 简书. Retrieved 2 August 2017, from http://www.jianshu.com/p/45661b029292
[^9]: Search Tree Implementation — Problem Solving with Algorithms and Data Structures. (2017). Interactivepython.org. Retrieved 2 August 2017, from http://interactivepython.org/runestone/static/pythonds/Trees/SearchTreeImplementation.html