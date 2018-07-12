---
layout: post
title: 实名认证调研
date:  2018-07-12
author: xiaoyongsheng
By: xiaoyongsheng
email: xiaoyongsheng@hotmail.com  
categories: Others
---

* content
{:toc}

## 身份证号解析

身份证号[^6]主要分为两种：15位（1999年之前）、18位（1999年之后）；18位第二代身份证号编码规则如下：

- 6位地址码；
- 7位出生日期：15位的是YYMMDD，18位的是YYYYMMDD；
- 3位顺序码：同一地址码区域范围内，对同年同月同日生的人按序编号，奇数分配给男性，偶数分配给女性；
- 1位校验码；

## 实名认证调研

### 主要目的

实名认证的目的[^1][^5]：

1. 确保是用户本人的真实操作，降低平台风险；
2. 出于监管需要，发生恶意攻击时监管机构和平台方有据可循；
3. 保障用户资产和信息安全，维护自身权利，防止被他人恶意注册；

### 当前矛盾

校验信息越多，用户的真实性和准确性越高；但过程繁琐用户体验差，信任感低；

### 实现方式

实名认证的实现方式总体上可以分为两类：面对面认证和远程认证。远程认证的常见方式包括：

1. 姓名+身份证号：通过公安系统（公安部 “[全国公民身份证号码查询服务中心](http://www.nciic.com.cn/framework/gongzuo/gchcpofhhfilbbnnldnjnnnkpcfpcodb.jsp)” [^2]等）进行验证；
2. 姓名+身份证号+手机号：通过运营商进行验证；
3. **姓名+身份证号+活体人脸识别**：验证姓名、身份证号是否相符，验证活体人脸是否与身份证照片相符[^7]；
4. 人工视频审核：开启摄像头、回答客服问题、手持身份证照片（招行自助办卡）；
5. 随机付款：用户提供姓名、账户，平台随机小额转账，用户回填金额；
6. **绑定银行卡**：验证姓名、身份证号、卡号、预留手机号，向预留手机号发送验证信息即可；

### 相关风险

1. 手机验证码：手机丢失可能导致恶意交易；
2. 手机号：存在副卡等情况，持卡人和手机号拥有者不是同一人；
3. 姓名+身份证号：无法保证是本人操作，无法判断是否人证合一（网络上有大批量低价贩卖手持身份证照片甚至身份证原件的黑渠道[^3]）；
4. 人工审核：成本高、效率低、体验差；

### 推荐方式

最可靠的两种方式：绑定银行卡、人脸识别+身份证号+姓名验证；

**绑定银行卡**：验证姓名、身份证号、卡号、预留手机号，向预留手机号发送验证信息即可；

**姓名+身份证号+活体人脸识别**：验证姓名、身份证号是否相符，验证活体人脸是否与身份证照片相符；



## Reference

[^1]: *聊聊常见的实名认证*. (2018). *简书*. Retrieved 12 July 2018, from https://www.jianshu.com/p/cd4ac184f751
[^2]: 全国公民身份证号码查询服务中心. (2018). Nciic.com.cn. Retrieved 12 July 2018, from http://www.nciic.com.cn/framework/gongzuo/ilkjbckkhfilbbnnldnjnnnkpcfpcodb.jsp
[^3]: *一张照片让你背负现金贷的债，你还在随意发验证照吗？*. (2018). *Xw.qq.com*. Retrieved 12 July 2018, from https://xw.qq.com/cmsid/20180413A0QWIE00
[^4]: 芝麻信用商家服务平台(2018). *B.zmxy.com.cn*. Retrieved 12 July 2018, from https://b.zmxy.com.cn/technology/technicalAuths.htm
[^5]: *干货丨互联网常见实名认证方式介绍 | 人人都是产品经理*. (2018). *Woshipm.com*. Retrieved 12 July 2018, from http://www.woshipm.com/pmd/351836.html
[^6]: *干货丨身份证号码编码规则及其应用 | 人人都是产品经理*. (2018). *Woshipm.com*. Retrieved 12 July 2018, from http://www.woshipm.com/pmd/350196.html
[^7]: *未绑定快捷支付，手机上通过支付宝进行实名认证的流程 (2018). Cshall.alipay.com*. Retrieved 12 July 2018, from https://cshall.alipay.com/lab/help_detail.htm?help_id=559829
