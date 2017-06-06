---
layout: post
title: linux下oracle安装教程
date:  2016-06-03
author: xiaoyongsheng
By: xiaoyongsheng
email: xiaoyongsheng@hotmail.com
categories: linux
tag: linux
---

* content
{:toc}

# 安装oracle安装过程中所需依赖包  #

1. 检查所需依赖文件是否已经安装

    `rpm -q binutils compat-libstdc++-33 elfutils-libelf elfutils-libelf-devel glibc glibc-common glibc-devel gcc- gcc-c++ libaio-devel libaio libgcc libstdc++ libstdc++-devel make sysstat unixODBC unixODBC-devel libXp pdksh`

2. 如有尚未安装的依赖包，可以通过 yum 安装
    
    `yum install <package_name>` 

    或者自行下载 rpm 包进行安装

	`rpm -ivh [-replacepkgs] <rpm_name>`

# 创建 oracle 组和用户账号 #

1. 创建用户和组  

	```bash
   groupadd oinstall  
   groupadd dba  
   useradd -m -g oinstall -G dba oracle  # -m 建立用户目录; -g 用户归属组; -G 用户同时属于其他指定组  
   id oracle  # 打印出真实生效的用户id和组id  
   passwd oracle
	```

2. 创建安装目录

	```bash
   mkdir -p /data/app/oracle
   chown -R oracle:oinstall /data/app/oracle
   chmod -R 777 /data/app/oracle
   mkdir -p /data/app/oraInventory
   chown -R oracle:oinstall /data/app/oraInventory
   chmod -R 777 /data/app/oraInventory
	```

# 参数配置 #

1. 配置内核参数 **/etc/sysctl.conf**

	```
   vi /etc/sysctl.conf  #向/etc/sysctl.conf追加如下内容`
   sysctl -p  #使sysctl生效
	```

	> **/etc/sysctl.conf的配置文件**
   kernel.shmmni = 4096
   kernel.sem = 250 32000 100 128
   fs.file-max = 6815744
   fs.aio-max-nr = 1048576
   net.core.rmem_default = 4194304
   net.core.rmem_max = 4194304
   net.core.wmem_default = 262144
   net.core.wmem_max = 1048576
   net.ipv4.ip_local_port_range = 9000 65500

2. **/etc/security/limits.conf** 中增加如下配置
	
	```
   oracle soft nproc 2047
   oracle hard nproc 16384
   oracle soft nofile 1024
   oracle hard nofile 65536
	```

3. **/etc/pam.d/login** 中增加如下配置

	```
   session required /lib64/security/pam_limits.so
   session requiredpam_limits.so
	```

4. **/etc/profile** 中增加如下配置

	```
   if [ \$USER = "oracle" ]; then 
       if [ \$SHELL = "/bin/ksh" ]; then
           ulimit -p 16384
           ulimit -n 65536
       else
           ulimit -u 16384 -n 65536
   fi
       umask 022
   fi
	```

5. **/etc/csh.login** 中增加如下配置

	```
   if ( \$USER == "oracle" ) then
       limit maxproc 16384
       limit descriptors 65536
       umask 022
   endif

	```

6. **/home/oracle/.bash_profile** 中增加如下环境变量

	```
   TMP=/tmp; export TMP
   TMPDIR=$TMP; export TMPDIR
   ORACLE_BASE=/data/app/oracle; export ORACLE_BASE
   ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1; export ORACLE_HOME
   ORACLE_SID=orcl; export ORACLE_SID
   ORACLE_UNQNAME=orcl; export ORACLE_UNQNAME
   ORACLE_TERM=xterm; export ORACLE_TERM
   PATH=/data/sbin:$PATH; export PATH
   PATH=$ORACLE_HOME/bin:$PATH; export PATH
   LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib; export LD_LIBRARY_PATH
   CLASSPATH=$ORACLE_HOME/JRE:$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib; export CLASSPATH
    
   if [ $USER = "oracle" ]; then
       if [ $SHELL = "/bin/ksh" ]; then
           ulimit -p 16384
           ulimit -n 65536
       else
           ulimit -u 16384 -n 65536
       fi
   fi
	```
	`source /home/oracle/.bash_profile`

7. 修改 **/etc/redhat-release** (*好像没有必要*)

	```
   Red Hat Enterprise Linux Server release 4 (Tikanga)  #将原本的6.2修改为4
	```

8. 修改 **/etc/hosts**（*好像没有必要*）

	```
   #安装机器的IP地址  安装机器主机名称  
   127.0.0.1 oracle localhost.localdomain localhost
   192.168.1.1 oracle localhost.localdomain localhost
   ::1 localhost6.localdomain6 localhost6
	```

9. 修改 **/etc/sysconfig/network**（*好像没有必要*）

	```
   NETWORKING=yes
   NETWORKING_IPV6=no
   HOSTNAME=localhost.localdomain
	```

&emsp;&emsp;注意： 在安装oracle数据库的时候要注意**/etc/hosts** 与 **/etc/sysconfig/network** 文件主机名的一致性，否则会在后面运行netca和dbca可能出现错误提示。

# 安装oracle #

1. 解压oracle安装文件到oracle用户目录

	```
   unzip p10404530_112030_Linux-x86-64_1of7.zip -d /home/oracle/
   unzip p10404530_112030_Linux-x86-64_2of7.zip -d /home/oracle/
	```

2. 设置xhost

	```
   su root  #切换到root用户执行以下步骤
   export DISPLAY=:0.0
   xhost +

   su oracle
   export LANG=en_US
   cd home/oracle/database
   ./runInstaller

	```