---
layout: post
title: 虚拟机设置静态IP 
date:  2016-05-31
author: xiaoyongsheng
By: xiaoyongsheng
email: xiaoyongsheng@hotmail.com  
categories: LittleBitch
tag: 虚拟机
---

* content
{:toc}

[本文参考自CSDN博客](http://blog.csdn.net/pangjiawei19/article/details/50905359)

-----

## windows -> network connections ##

- 设置本地连接的属性共享为允许，并在家庭网络连接中选择 VMnet8  
  
	![](http://i.imgur.com/Aq59JMA.png)  
          
- 配置VMnet8的网络属性，勾选VMware Bridge Protocol, 查看TCP/IPv4的属性；  
  
	- 我的 VMnet8 IP为 192.168.137.1
  
	![](http://i.imgur.com/oAv3phR.png)

## VMware -> edit -> virtual network editor ##

- 对 VMnet8 进行配置

	- 取消勾选 Use local dhcp server

	- 修改Sunet IP 和 Subnet Mask  

		- Subnet IP需要与宿主VMnet8的IP在同一地址段，可填写192.168.137.0

		- Subnet Mask应与VMnet8的子网掩码相同，即填写255.255.255.0  
	
	- NAT Settings 里面将Gateway IP设置为宿主计算机中 VMnet8 的 IP，即 192.168.137.1 

	![](http://i.imgur.com/aHa2fWj.png)

## 配置系统网络 ##

- 配置 /etc/sysconfig/network-scripts/ifcfg-eth0
	> IPADDR 填写你要设置的 ip 地址  
	> NETMASK 设置子网掩码，见前文配置  
	> ONBOOT 设为 yes 表示开机启动  
	> BOOTPROTO 设置为 static 表示静态 ip  
	> DNS1 配置为网关 IP 地址即可

	![](http://i.imgur.com/eQgQ5dv.png)

- 配置 /etc/sysconfig/network

	> 配置 GATEWAY 为网关IP地址

	![](http://i.imgur.com/OtBv1yz.png)

## 重启network ##

- 重启网络

	> service network restart	

    ![](http://i.imgur.com/tb4Gjll.png)

- 检测 IP

	> ifconfig
	
	![](http://i.imgur.com/74sRA9r.png)

&emsp;&emsp;可以看到我们的 IP 已经成功设置为 192.168.137.109，现在可以ping一下试试网络是否畅通，我的机器是不行的，随后又找到[相关解决方式](http://www.xpxt.net/xtjc/win8/04194953.html),发现我的配置是没有问题的，这个时候使出网关必杀技：**重启**

- 重启虚拟机

![](http://i.imgur.com/McTwn3H.png)

&emsp;&emsp;**well Done!**

## 物理机无法ping通虚拟机 ##

[参考资料](http://2358205.blog.51cto.com/2348205/1239132)

- 问题1：虚拟机可以 ping 通主机，但是主机无法 ping 通虚拟机

- 解决方案：

&emsp;&emsp;打开主机 network Connections, 找到 VMware Network Adapter VMnet8，将其重置为Enable即可.(先置为Disable,再置为Enable)