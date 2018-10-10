# iCrawler_python
icrawler_python爬虫是基于scrapy爬虫框架进行开发，对url进行md5加密处理存放到redis,在抓取过程中对已抓取过的url进行过滤实现增量抓取；建立user-agent池，每次请求会切换不同的user-agent；为确保ip代理的稳定性，使用阿布云动态ip代理，实现每次请求会切换不同的ip代理；实现重试机制，在抓取过程中对方服务器如果返回500、503、504、400、429、403错误会尝试重新请求一定的次数；抓取到的数据存储到mongo数据库保存。

###爬虫项目

#####doubangaofen.py    豆瓣高分电影爬虫

#####lagouwang.py       拉勾网爬虫

#####the36kr.py         36氪关键词搜索爬虫

#####toutiaohao.py      头条号爬虫

#####zhihu_user.py      知乎用户爬虫

#####zhihuhao.py        知乎号爬虫