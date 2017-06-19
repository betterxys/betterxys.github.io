---
layout: post
title: 爬虫-模拟登陆 
date:  2016-06-19
author: xiaoyongsheng
By: xiaoyongsheng
email: xiaoyongsheng@hotmail.com  
categories: Information_Intergration
tag: 爬虫
---

* content
{:toc}

  
## 页面准备 ##

1. 输入网址并由此进入登陆界面 ： http://***.***.***.***/Login.aspx

2. 登陆进入登陆后界面，此操作使用chrome的 "**检查**" 打开,得到如下信息：  

   >   **General**  
   >   Request URL: http://***.***.***.***/Login.aspx  
   >   Request Method:POST  
   >   Status Code:200 OK  
   >   Remote Address:***.***.***.***:80
  
   >  **Response Headers**  
   >  Cache-Control:private  
   >  Content-Length:10729  
   >  Content-Type:text/html; charset=utf-8  
   >  Date:Wed, 15 Jun 2016 00:40 :34 GMT  
   >  Server:Microsoft-IIS/6.0  
   >  X-AspNet-Version:2.0.50727  
   >  X-Powered-By:ASP.NET  
     
   >  **Request Headers**  
   >  Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8  
   >  Accept-Encoding:gzip, deflate  
   >  Accept-Language:zh-CN,zh;q=0.8  
   >  Cache-Control:max-age=0  
   >  Connection:keep-alive  
   >  Content-Length:470  
   >  Content-Type:application/x-www-form-urlencoded  
   >  Cookie:ASP.NET_SessionId=hgrn0v55k5muviipntt1h155  
   >  Host:***.***.***.***  
   >  Origin: http://***.***.***.***  
   >  Referer: http://***.***.***.***/Login.aspx  
   >  Upgrade-Insecure-Requests:1  
   >  User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36  

   >  **From Data**  
   >  \__EVENTTARGET:  
   >  \__EVENTARGUMENT:  
   >  \__VIEWSTATE:/wEPDwUKLTc4MzY5NjY5Nw9kFgICAw9kFgICFw8PFgIeBFRleHRlZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgUFCHJidG5EZXB0BQtyYnRuVGVhY2hlcgULcmJ0blRlYWNoZXIFC3JidG5TdHVkZW50BQtyYnRuU3R1ZGVudA1gZKqG2kk6EvC2qWLlC7HHx7io  
   >  \__EVENTVALIDATION:/wEWCAKR+7KNDQKvruq2CALSxeCRDwLI0oXWBQKjndD0AwKViOj6BgL+jNCfDwKT+PmaCMChSLI3uc0DzHYNhu/SeMa6TuKo  
   >  UserName:######  
   >  Password:######  
   >  userType:rbtnStudent  
   >  LoginButton:登 陆  

## 代码完成 ##  

   &emsp;&emsp;接下来需要进行代码的编写：  

   ```python
import urllib
import urllib.request
import urllib.parse
import http.cookiejar


PostUrl = "http://***.***.***.***/Login.aspx"
cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
UserName = ######
Password = ######

PostData = {
'__EVENTTARGET' = '',
'__EVENTARGUMENT' = '',
'__VIEWSTATE' = '/wEPDwUKLTc4MzY5NjY5Nw9kFgICAw9kFgICFw8PFgIeBFRleHRlZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgUFCHJidG5EZXB0BQtyYnRuVGVhY2hlcgULcmJ0blRlYWNoZXIFC3JidG5TdHVkZW50BQtyYnRuU3R1ZGVudA1gZKqG2kk6EvC2qWLlC7HHx7io',
'__EVENTVALIDATION' = '/wEWCAKR+7KNDQKvruq2CALSxeCRDwLI0oXWBQKjndD0AwKViOj6BgL+jNCfDwKT+PmaCMChSLI3uc0DzHYNhu/SeMa6TuKo',
'UserName' = '######',
'Password' = '######',
'userType' = 'rbtnStudent',
'LoginButton' = '登 陆'}

headers = {'Accept' = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding' = 'gzip, deflate',
'Accept-Language' = 'zh-CN,zh;q=0.8',
'Cache-Control' = 'max-age=0',
'Connection' = 'keep-alive',
'Content-Length' = '470',
'Content-Type' = 'application/x-www-form-urlencoded',
'Cookie' = 'ASP.NET_SessionId=hgrn0v55k5muviipntt1h155',
'Host' = '***.***.***.***',
'Origin' = 'http://***.***.***.***',
'Referer' = 'http://***.***.***.***/Login.aspx',
'Upgrade-Insecure-Requests' = '1',
'User-Agent' = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}

data = urllib.parse.urlencode(PostData).encode()
request = urllib.request.Request(PostUrl, data, headers)

try:
    response = opener.open(request)
	result = response.read()
    print(result)
except urllib.request.HTTPError as e:
    print(e)
   ```

程序执行之后，打印出来的还是登陆界面，所以，进入调试过程：

## request-response机制了解 ##

- ### 分析代码，整理代码流程 ###

   ```python
result = response.read()
response = opener.open(request)
request = urllib.request.Request(PostUrl, data, headers)  # PostUrl,headers手动指定
data = urllib.parse.urlencode(PostData).encode()  # PostData手动指定
   ```

	1. #### 分析 urllib.parse.urllencode() ####
	
	   > urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus)  
	   > 
	   > Convert a mapping object or a sequence of two-element tuples, which may contain str or bytes objects, to a “percent-encoded” **string**. If the resultant string is to be used as a data for POST operation with urlopen() function, then it should be properly encoded to bytes, otherwise it would result in a TypeError.
	   > 
	   > **当输出被用于urlopen时，必须将输出转换为bytes格**  
	   
	   &emsp;&emsp;`urllib.parse.urlencode(PostData)`的类型是`str`,所以需要使用`encode()`来将`data`转换为`bytes`格式;  
	
	   > data = UserName=######&LoginButton=%E7%99%BB+%E9%99%86&userType=rbtnStudent&Password=######
	   > type(data) = bytes
	
	   &emsp;&emsp;此时，data的值如上所示，应该是可以满足要求的。
	
	2. #### 分析 urllib.request.Request(PostUrl, data, headers) #### 
	
	   `class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)` 
	   This class is an abstraction of a URL request.
	
	   > ***data***
	   > data must be a bytes object specifying additional data to send to the server, or None if no such data is needed. Currently HTTP requests are the only ones that use data; the HTTP request will be a POST instead of a GET when the data parameter is provided. data should be a buffer in the standard application/x-www-form-urlencoded format.
	
	   > ***headers***
	   > headers should be a dictionary, and will be treated as if add_header() was called with each key and value as arguments.This is often used to “spoof” the User-Agent header, which is used by a browser to identify itself – some HTTP servers only allow requests coming from common browsers as opposed to scripts. 
	
	   > ***origin_req_host*** 
	   > origin_req_host should be the request-host of the origin transaction, as defined by RFC 2965. It defaults to http.cookiejar.request_host(self). This is the host name or IP address of the original request that was initiated by the user.
	
	   > ***unvrifiable***
	   >unverifiable should indicate whether the request is unverifiable, as defined by RFC 2965. It defaults to False. An unverifiable request is one whose URL the user did not have the option to approve. 
	
	   > ***method***
	   > method should be a string that indicates the HTTP request method that will be used (e.g. 'HEAD'). If provided, its value is stored in the method attribute and is used by get_method(). 
	
	   最为关键的应该就是 url/data/headers 这三项：
	   
	   &emsp;&emsp;url 是登陆界面的 url；
	   &emsp;&emsp;data 由 parse.urlencode().encode()生成的 bytes 来指定；
	   &emsp;&emsp;headers 是根据浏览器当中的 Request Headers 来确定的；
	
	   &emsp;&emsp;那么问题来了，这三项都符合，那究竟是哪里出了问题？这个时候拐回代码段，发现还有一部分代码被我们忽略掉了：
	
	```python
	cookie = http.cookiejar.CookieJar()
	handler = urllib.request.HTTPCookieProcessor(cookie)
	opener = urllib.request.build_opener(handler)
	```

- ### 继续整理 cookie 产生机制 ###

	`class http.cookiejar.CookieJar(policy=None)` 
	 > policy is an object implementing the CookiePolicy interface.
	 > The CookieJar class stores HTTP cookies. It **extracts cookies from HTTP requests**, and **returns them in HTTP responses**. CookieJar instances automatically expire contained cookies when necessary. Subclasses are also responsible for storing and retrieving cookies from a file or database.
  
   `class urllib.request.HTTPCookieProcessor(cookiejar=None)` 
     > A class to handle HTTP Cookies.
	 > HTTPCookieProcessor instances have one attribute:
	 > HTTPCookieProcessor.cookiejar(The http.cookiejar.CookieJar in which cookies are stored.)

   `urllib.request.build_opener([handler, ...])` 
	 > Return an OpenerDirector instance, which chains the handlers in the order given. handlers can be either instances of BaseHandler, or subclasses of BaseHandler (in which case it must be possible to call the constructor without any parameters). Instances of the following classes will be in front of the handlers, unless the handlers contain them, instances of them or subclasses of them: ProxyHandler (if proxy settings are detected), UnknownHandler, HTTPHandler, HTTPDefaultErrorHandler, HTTPRedirectHandler, FTPHandler, FileHandler, HTTPErrorProcessor.
	
	 > If the Python installation has SSL support (i.e., if the ssl module can be imported), HTTPSHandler will also be added.

## 分析错误原因 ##

   &emsp;&emsp;使用fiddler来抓捕程序发出的request和response.
	
   

- **p-request**
	```
POST http://***.***.***.***/Login.aspx HTTP/1.1
Accept-Encoding: identity
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: http://***.***.***.***/Login.aspx
Content-Length: 100
Connection: close
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36
Host: ***.***.***.***
Accept-Language: zh-CN,zh;q=0.8
UserName=######&userType=rbtnStudent&LoginButton=%25E7%2599%25BB%2B%25E9%2599%2586&Password=######
```


- **web-request**
	```
POST http://***.***.***.***/Login.aspx HTTP/1.1
Host: ***.***.***.***
Connection: keep-alive
Content-Length: 470
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: http://***.***.***.***
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Referer: http://***.***.***.***/Login.aspx
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: ASP.NET_SessionId=3arhgnyvjehpve554tftgb32

__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKLTc4MzY5NjY5Nw9kFgICAw9kFgICFw8PFgIeBFRleHRlZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgUFCHJidG5EZXB0BQtyYnRuVGVhY2hlcgULcmJ0blRlYWNoZXIFC3JidG5TdHVkZW50BQtyYnRuU3R1ZGVudA1gZKqG2kk6EvC2qWLlC7HHx7io&__EVENTVALIDATION=%2FwEWCAKR%2B7KNDQKvruq2CALSxeCRDwLI0oXWBQKjndD0AwKViOj6BgL%2BjNCfDwKT%2BPmaCMChSLI3uc0DzHYNhu%2FSeMa6TuKo&UserName=######&Password=######&userType=rbtnStudent&LoginButton=%E7%99%BB+%E9%99%86
```

- **p-response**

	```
HTTP/1.1 200 OK
Connection: close
Date: Sun, 19 Jun 2016 03:11:42 GMT
Server: Microsoft-IIS/6.0
X-Powered-By: ASP.NET
X-AspNet-Version: 2.0.50727
Cache-Control: private
Content-Type: text/html; charset=utf-8
Content-Length: 7990
********web页面*******
```

- **web-response**
	```
HTTP/1.1 200 OK
Date: Sun, 19 Jun 2016 03:27:56 GMT
Server: Microsoft-IIS/6.0
X-Powered-By: ASP.NET
X-AspNet-Version: 2.0.50727
Cache-Control: private
Content-Type: text/html; charset=utf-8
Content-Length: 10729
****web页面****
```

    问题应该主要是出在了request上面，经过对比发现,p-request存在以下问题：
> Accept-Encoding: identity  ***# gzip, deflate***
> Connection: close  ***# keep-alive***
> Content-Length: 100  ***# 470***
> User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36
> ***# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36***
> cookie缺失  ***# Cookie: ASP.NET_SessionId=3arhgnyvjehpve554tftgb32***
> LoginButton=%25E7%2599%25BB%2B%25E9%2599%2586&
> ***# %E7%99%BB+%E9%99%86***

    经过修改cookie，loginbutton,uer-agent都已经解决，剩下的就是：
	
	- Accept-Encoding = gzip,deflate
	- Connection = keep-alive
	- Content-Length = 470