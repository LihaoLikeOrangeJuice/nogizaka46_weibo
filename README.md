# 爬取乃木坂46官方微博上的图片

## 安装依赖

```shell
conda install redis-py
conda install mysql-connector-python
```

## 简介

一共有15376张图片，所以我用到了MYSQL来存图片的网址

然后为了保证爬取的效率，所以需要用到代理IP，我选用了REDIS来管理代理IP池

代理用的站大爷，用的账号密码认证模式

## 使用方法

运行MYSQL和REDIS

在 nogizaka46_weibo.py 同级目录下创建 cookie.txt, proxy.txt, password.txt, account_number.txt文件

- 在 cookie.txt 中输入 cookie, cookie 为登陆微博后的 XSRF-TOKEN
- 在 proxy.txt 中输入代理IP的API提取链接
- 在 password.txt中输入代理的实例ID
- 在 account_number.txt中输入代理的密码

运行 nogizaka46_weibo.py
