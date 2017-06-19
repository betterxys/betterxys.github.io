---
layout: post
title: LjungBox统计量两种实现方式 
date:  2017-02-17
author: xiaoyongsheng
By: xiaoyongsheng
email: xiaoyongsheng@hotmail.com  
categories: Statistical_Learning
tag: 时间序列
---

* content
{:toc}

Here are 2 different way to realize Ljung Box test<sup>[1][2][[3]](https://en.wikipedia.org/wiki/Ljung%E2%80%93Box_test)</sup>:
    
## 1. statsmodels.stats.diagnostic.acorr_ljungbox<sup>[[5]](http://statsmodels.sourceforge.net/0.6.0/generated/statsmodels.stats.diagnostic.acorr_ljungbox.html "[5]")</sup> ##

    from statsmodels.stats.diagnostic import acorr_ljungbox
 
	data = ***
	acorr_ljungbox(data, lags=None, boxpirece=False)  #lags is the largest lag to report


## 2. pypr.stattest.ljungbox<sup>[[4]](http://pypr.sourceforge.net/stattest.html)</sup> ##

	from pypr.stattest.jungbox import *
	h, pV, Q, cV = lbqtest(x, range(1, 20), alpha=0.1)

　problem "no module named ljungbox" occured when import pypr.stattest, find out the package files in 'Lib/site-packages/pypr/stattest', find out that all these files lying silently here:

![lbfile](http://i.imgur.com/LlQ7T1X.png)

　The truth is only one:

	__init__.py

	from ljungbox import *
	from model_select import *

　it should be:


	__init__.py

	from .ljungbox import *
	from .model_select import *

　and now all fix!


# [References] #

1. Box G E P, Pierce D A. Distribution of residual autocorrelations in autoregressive-integrated moving average time series models[J]. Journal of the American statistical Association, 1970, 65(332): 1509-1526.
2. Ljung G M, Box G E P. On a measure of lack of fit in time series models[J]. Biometrika, 1978: 297-303.
3. https://en.wikipedia.org/wiki/Ljung%E2%80%93Box_test
4. http://pypr.sourceforge.net/stattest.html
5. http://statsmodels.sourceforge.net/0.6.0/generated/statsmodels.stats.diagnostic.acorr_ljungbox.html
