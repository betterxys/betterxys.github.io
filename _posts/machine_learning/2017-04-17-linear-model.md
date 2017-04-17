---
layout: post
title: 机器学习算法-线性模型
date: 2017-04-17
author: xiaoyongsheng
categories: Linux
tag: linux

---

* content
{: toc}

---

## 查看系统信息  

### cpu信息  

```shell
# 查看cpu个数
cat /proc/cpuinfo | grep "physical id" | uniq | wc -l

# 查看每个物理cpu的核数
cat /proc/cpuinfo | grep "cpu cores" | uniq

# 查看逻辑cpu个数
cat /proc/cpuinfo | grep "processor" | wc -l

# 查看cpu型号
cat /proc/cpuinfo | grep name
```

### 内存信息

```shell
cat /proc/meminfo

# 基于上述 /proc/meminfo进行显示，-t会显示Total， -g会以GB为单位  
free -t -g
```


### 磁盘空间

```shell
df -h  #据说有三板斧： df:磁盘 du：目录 fdisk：分区
```

## 参考资料  

1. http://www.cnblogs.com/emanlee/p/3587571.html  
2. https://my.oschina.net/hunterli/blog/140783  