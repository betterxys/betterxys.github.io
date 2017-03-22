---
layout: post
title: 虚拟机设置网络连接 
date:  2016-05-31
author: xiaoyongsheng
By: xiaoyongsheng
email: xiaoyongsheng@hotmail.com  
categories: LittleBitch
tag: 虚拟机
---

* content
{:toc}

# 总体思路 #
[参考自科学网博客](http://blog.sciencenet.cn/blog-430991-507041.html)  
&emsp;&emsp;将宿主计算机的物理网卡与VMnet8共享，VMnet8充当路由器，而VM中的虚拟计算机通过DHCP自动获得在某一个IP段内的IP地址，这些虚拟机都通过路由器(VMnet8)连接的IP与物理网卡上的Internet连接。

## windows -> network connections ##

- 设置本地连接的属性共享为允许，并在家庭网络连接中选择 VMnet8  
  
	![](http://i.imgur.com/Aq59JMA.png)  
          
- 配置VMnet8的网络属性，勾选VMware Bridge Protocol, 查看TCP/IPv4的属性；  
  
	- 我的 VMnet8 IP为 192.168.137.1
  
	![](http://i.imgur.com/oAv3phR.png)
  
## VM WorkStation -> Edit -> Virtual Network Editor ##

- 打开 VM WorkStation -> Edit -> Virtual Network Editor，选择VMnet8，勾选

	- Connect a host virtual network adapter to this network

	- Use local DHCP service to distribute IP address to VMs
	
- 修改Subnet IP 和 Subnet Mask  

	- Subnet IP需要与宿主VMnet8的IP在同一地址段，可填写192.168.137.0

	- Subnet Mask应与VMnet8的子网掩码相同，即填写255.255.255.0  

    ![](http://i.imgur.com/1FXbwDS.png)

- 设置 NAT Settings

	- NAT Settings 里面将Gateway IP设置为宿主计算机中VMnet8的IP，即192.168.137.1  

	- DHCP Settings 里面设置  

		> Start IP address = 192.168.137.0  
		  End IP address = 192.168.137.255

- 测试一下是否网络已经畅通

	- ping www.baidu.com
	
	- 如果还是不行：
	
		> vi /etc/sysconfig/network-scripts/ifcfg-eth0  
		  设置 bootproto = "dhcp"  
	      保存退出，然后再 ping www.baidu.com  
	      ok,done! 
