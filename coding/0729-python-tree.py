import numpy as np


class node:
    """implement a binary search tree"""

    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key


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


def check_bst(tre, min_value, max_value):
    """Check if a binary tree is a binary search tree."""
    if tre is None:
        return True
    if tre.value < min_value or tre.value > max_value:
        return False
    if check_bst(tre.left, min_value, tre.value) and check_bst(tre.right, tre.value, max_value):
        return True


def check_bst_2(rst, tmp=-np.inf):

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

levelod = list()


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


preod = list()
inod = list()
postod = list()
ary = [1, 2, 3, 4, 5, 6, 7, 8]
rst = sortedlist2bst(ary, 0, len(ary) - 1)

preorder(rst)
inorder(rst)
postorder(rst)
levelorder(rst)
print(preod, inod, postod, levelod)
print(check_bst(rst, -np.inf, np.inf))
print(check_bst_2(rst))
