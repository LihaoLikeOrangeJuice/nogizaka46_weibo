# 爬取nogizaka46在微博上的图片

## 简介

一共有15376张图片，所以我用到了MYSQL来存图片的网址

然后为了保证爬取的效率，所以需要用到代理IP，我选用了REDIS来管理代理IP池

## 使用方法

运行MYSQL和REDIS

在 run.py 同级目录下创建 cookie.txt 和 proxy.txt 文件

- 在 cookie.txt 中输入 cookie, cookie 为登陆微博后的 XSRF-TOKEN
- 在 proxy.txt 中输入代理IP的API提取链接

运行 run.py
