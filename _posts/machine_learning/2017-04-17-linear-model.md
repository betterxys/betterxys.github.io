---
layout: post
title: 机器学习算法-线性模型
date: 2017-04-17
author: xiaoyongsheng
categories: Machine_Learning
tag: 机器学习

---

* content
{: toc}

---

## 线性回归

testadsfsfasfs

$$
\begin{align*}
  & \phi(x,y) = \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right)
  = \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j) = \\
  & (x_1, \ldots, x_n) \left( \begin{array}{ccc}
      \phi(e_1, e_1) & \cdots & \phi(e_1, e_n) \\
      \vdots & \ddots & \vdots \\
      \phi(e_n, e_1) & \cdots & \phi(e_n, e_n)
    \end{array} \right)
  \left( \begin{array}{c}
      y_1 \\
      \vdots \\
      y_n
    \end{array} \right)
\end{align*}
$$

This is [a link](http://rubyforge.org) to a page.
A [link](../test "local URI") can also have a title.
And [spaces](link with spaces.html)!

This is a [link](http://example.com){:hreflang="de"}

test[^1].


The next paragraph contains a link and some text.

[Room 100]\: There you should find everything you need!

[Room 100]: link_to_room_100.html

[^1]: Some *crazy* footnote definition.

[^footnote]:
    > Blockquotes can be in a footnote.

        as well as code blocks

    or, naturally, simple paragraphs.

[^other-note]:       no code block here (spaces are stripped away)

[^codeblock-note]:
        this is now a code block (8 spaces indentation)


* list item one

* list item two

* list one
^
* list two

This is a [reference style link][linkid] to a page. And [this]
[linkid] is also a link. As is [this][] and [THIS]. 

[linkid]: www.google.com




这是怎么了

The following is a math block:

$$ 5 + 5 $$

But next comes a paragraph with an inline math statement:

\$$ 5 + 5 $$


不是把， 为什么现实不出俩了


## 参考资料  

[^1]: 周志华.机器学习[M].清华大学出版社,2016.  
