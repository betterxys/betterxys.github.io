---
layout: post
title: linux-常用工具
date: 2017-08-28
author: xiaoyongsheng
categories: linux
tag: linux

---

* content
{: toc}

---

## 压缩文件

```
# .gz
gzip -d file.gz
```


## md5校验

```
md5sum day_* > criteomd5.md5
md5sum -c criteomd5.md5
```


## virtualenv[^1]

```shell
cd project_folder
virtualenv project_name
source project_name/bin/activate

pip freeze > requirements.txt
pip install -r requirements.txt
```

## tmux

>tmux所有自带命令都默认需要先按Ctrb+b，然后再键入对应的命令。  
Ctrl+b原意为send-prefix，即发送前缀信号。以下简写C-b  
tmux   # 运行 tmux -2 以256终端运行，exit命令退出  
C-b d  # 返回主 shell ， tmux 依旧在后台运行，里面的命令也保持运行状态  
tmux ls # 显示已有tmux会话（C-b s）  
tmux attach-session -t 数字 # 选择tmux  
tmux new-session -s session-name  
tmux kill-session -t session-name  
man tmux//显示  
C-b ?  // 显示快捷键帮助，退出按q  
C-b  "  // 模向分隔窗口  
C-b % // 纵向分隔窗口  
C-b 方向键//在各窗口间切换（注意与下一个命令的区别）  
C-b C-方向键 //调整分隔窗口大小，不要松开Ctrl  
C-b c//create， 生成一个新的窗口  
C-b n//next，移动到下一个窗口  
C-b p//previous，移动到前一个窗口  
C-b l//last，移动到最后使用的窗口  
C-b C-o  //调换窗口位置，当前窗口和上一个窗口互换。  
C-b o // 跳到下一个分隔窗口  
C-b 0~9 //选择几号窗口  
C-b q // 显示分隔窗口的编号  
C-b w // 以菜单方式显示及选择窗口  
C-b s // 以菜单方式显示和选择会话  
C-b t //显示时钟  
C-b & // 确认后退出 tmux  
C-b ! // 把当前窗口变为新窗口  
C-b 空格键  //采用下一个内置布局  
C-b [ 复制(空格开始)  
C-b ] 粘贴（回车结束）  
C-b ,　给当前窗口改名  
C-b Pgup/Pgdn 上下翻页[^3]  

## AWK

```
# 统计行列数目 [^4][^5]
$ awk -F ',' 'END{print "col:" NF "row:" NR}' ./merged_app_screen 
col:9row:2613

# 文本替换[^6]
$ awk   '{gsub(/root/,"good");print $0}' test
$ awk   '{gsub(/root/,"good");print > test}' test

# 匹配查找
$ awk '/tofind/' *.log | wc -l
```

## Reference
[^1]: 虚拟环境 — The Hitchhiker's Guide to Python. (2017). Pythonguidecn.readthedocs.io. Retrieved 21 August 2017, from http://pythonguidecn.readthedocs.io/zh/latest/dev/virtualenvs.html
[^2]: linux 工具——终端分屏与vim分屏 - 无限大地NLP_空木的专栏 - CSDN博客. (2017). Blog.csdn.net. Retrieved 22 August 2017, from http://blog.csdn.net/u010454729/article/details/49496381
[^3]: tmux/screen里面如何用鼠标滚轮来卷动窗口内容 - 巴蛮子 - 博客园. (2017). Cnblogs.com. Retrieved 28 August 2017, from http://www.cnblogs.com/bamanzi/archive/2012/08/17/mouse-wheel-in-tmux-screen.html
[^4]: linux awk命令详解 - ggjucheng - 博客园. (2017). Cnblogs.com. Retrieved 29 August 2017, from http://www.cnblogs.com/ggjucheng/archive/2013/01/13/2858470.html
[^5]: AWK 简明教程 | | 酷 壳 - CoolShell. (2013). 酷 壳 - CoolShell. Retrieved 29 August 2017, from https://coolshell.cn/articles/9070.html
[^6]: sed和awk的常用实例 - 无心出岫 - CSDN博客. (2017). Blog.csdn.net. Retrieved 29 August 2017, from http://blog.csdn.net/junjieguo/article/details/7525794