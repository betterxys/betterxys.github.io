---
layout: post
title: 文献引用格式汇总
date:  2018-01-04
author: xiaoyongsheng
By: xiaoyongsheng
email: xiaoyongsheng@hotmail.com  
categories: Others
tag: latex
---

* content
{:toc}


##  写作动机

毕业论文写作过程中，为了避免大量的格式调整，所以采用latex来进行写作，写作过程中学习到很多，但未曾记录。本人论文采用前辈们的模板进行撰写，但如今学院格式审查过程中发现有些格式依旧不符合要求，在此进行记录并解决。


## 问题汇总

- 封面页标题应采用“小二仿宋加粗”，原模板采用黑体加粗；
- 评审页标题同样应该采用“仿宋加粗”，原模板未加粗；
- 英文评审页标题下划线应同样长，原模型以下划线的形式存在；
- 独创性声明需要3份（暂时不管）;
- 摘要/目录等中间间隔一个空格，原模板有两个；
- ABSTRACT页眉应采用Abstract,原模板全部大写；
- 目录缩进两个字节，原文4个；
- 目录行间距采用单倍行距，原本双倍；
- 图目录/表目录每项都应如“图 1.1”,原文为“1.1”;
- 公式的段前距过大，需要缩小；
- 章节标题段前距过大，需要缩小；
- 图片内部间距不应过大（与模板无关，本人出自美观考虑自行做图导致的问题）；
- 章节标题需要加粗；
- 参考文献要求不同；

##  解决方案

###  仿宋加粗问题

作者仔细查看了相关资料和本人电脑（ubuntu）中的配置信息，Linux系统支持的中文字体并不丰富，所以本人将win的字体全部拷贝到linux下，但经查看，仿宋字体并没有加粗的设置，也就是说该字体天然不支持加粗操作，可能也是由于这个原因，模板中的`\bfseries`操作未能达到加粗效果，本人采用的解决方案是通过伪加粗的方式对仿宋进行加粗。

```
% 添加加粗仿宋
\setCJKfamilyfont{fs}[AutoFakeBold=3]{FangSong} 
\newcommand{\fs}{\CJKfamily{fs}}
```

采用该方式需要实现确认系统中是否有字体`FangSong`, `AutoFakeBold`就是伪加粗，其至可自行调节；


###  公式行间距

```
{\setlength\abovedisplayskip{1pt plus 3pt minus 7pt} 
\setlength\belowdisplayskip{1pt plus 3pt minus 7pt} 
\begin{align}\label{eq:ctr_form}
\text{历史点击率} = \frac{\text{总点击次数}}{\text{总展示次数}} \times 100%
\end{align}
}
```

这是一种较为简单直接的方式实现段前和段后间距设置, `align`内是公式内容，`displayskip`是段前段后间距。


###  空格

```
\@namedef{ZJU@spaceChar}{\hspace{1em}}
```

通过这种方式定义空格就是将一个单位的空格`\hspace{1em}`赋值给变量`\ZJU@spaceChar`，后续可以使用该变量进行设置；

###  大写

`\MakeUppercase`是本文使用的大写转换命令，找到并注释掉即可； 

### 目录

#### 缩进

```
\renewcommand*\l@section{\@dottedtocline{1}{1em}{2.1em}}
\renewcommand*\l@subsection{\@dottedtocline{2}{2em}{3em}}
\renewcommand*\l@subsubsection{\@dottedtocline{3}{6em}{3.8em}}
```

上述`\@dottedtocline`的第二个参数是控制该目录缩进位置，第三个参数控制用以显示页数的box的宽度；


#### 行间距

```
\linespread{1.2}\selectfont
```

设置目录时通过上述命令即可控制行间距，本文1.2为单倍行距，1.7为双倍行距；

#### 图表


```
% 图目录
\renewcommand\listoffigures{%
    \if@openright\cleardoublepage\else\clearpage\fi%
    \chapter{\listfigurename}
    \let\oldnumberline\numberline
    \renewcommand{\numberline}{\figurename~\oldnumberline}%
    \@starttoc{lof}}

\renewcommand*\l@figure{
    \linespread{1.2}\selectfont 
    \@dottedtocline{1}{0\p@}{2.3em}
    }
```

以图目录为例， 先将原有的图序号`numberline`赋值给`lodnumberline`，再将`oldnumberline`和`\figurename`（即‘图’）拼接起来作为新的`numberline`参与到目录项即可；


###  参考文献

参考文献本文采用南京大学胡海星制作的GB/T 7714-2005规范的BibTex([项目主页在此](http://haixing-hu.github.io/nju-thesis/)); 
但是该规范与学院要求不符，所以改用清华薛瑞尼提供的参考文献样式([项目主页在此](https://github.com/xueruini/thuthesis)); 