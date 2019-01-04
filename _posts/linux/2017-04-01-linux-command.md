---
layout: post
title: linux-常见问题
date: 2017-08-28
author: xiaoyongsheng
categories: linux
tag: linux

---

* content
{: toc}

---

## 文件

### 批量修改文件名

```
rename 's/^af/AFM/' af*
```

## 查看系统信息[^1][^2]  

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

## 安装与解压

### 安装问题
- dpkg 安装存在依赖问题

```
apt-get -f -y install
```

### 解压问题
- zip 解压中文乱码

```
unzip -O gbk *.zip
```

## ssh相关问题

### ubuntu终端登录ssh
- ubuntu 终端登录 ssh
ubuntu登录ssh可以通过命令``` ssh username@ip```进行登录，为避免每次重复输入用户名和ip，可以```touch ~/.ssh/config```，并在该文件当中添加配置文件即可。

```shell
# ~/.ssh/config
Host alias
	User username
	Hostname ip
$ source ~/.ssh/config
$ ssh alias
```

### github 与 gitlab
- github 与 gitlab ssh key冲突的问题
生成两对名称不同的密钥，并添加~/.ssh/config文件，从中配置特定域名走特定渠道，参考[^3][^4]

- gitlab clone 非master分支代码[^5]
```shell
git clone git@gitlab.xxx.git
git branch -a # 查看所有分支
git checkout $branchname
```

### github配置


```shell
ssh-keygen -t rsa -b 4096 -C "betterxys@gmail.com" -f id_rsa.github
pbcopy < ~/.ssh/id_rsa.github.pub

# paste to github config

git clone git@github.com:betterxys/betterxys.github.io.git
git remote add origin git@github.com:betterxys/betterxys.github.io.git
git push origin master

# vi ./ssh/config
Host github.com
  Preferredauthentications publickey
  IdentityFile ~/.ssh/id_rsa.github
```


## 参考资料  

[^1]: http://www.cnblogs.com/emanlee/p/3587571.html  
[^2]: https://my.oschina.net/hunterli/blog/140783  
[^3]:  gitlab/github 多账户下设置 ssh keys - 前端微言 - SegmentFault. (2017). Segmentfault.com. Retrieved 18 August 2017, from https://segmentfault.com/a/1190000002994742
[^4]: xirong/my-git. (2017). GitHub. Retrieved 18 August 2017, from https://github.com/xirong/my-git/blob/master/use-gitlab-github-together.md
[^5]: Git 如何 clone 非 master 分支的代码. (2017). Gaohaoyang.github.io. Retrieved 18 August 2017, from https://gaohaoyang.github.io/2016/07/07/git-clone-not-master-branch/