# -*- coding: utf-8 -*-

# Scrapy settings for iCrawler_python project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging.config

BOT_NAME = 'iCrawler_python'

SPIDER_MODULES = ['iCrawler_python.spiders']
NEWSPIDER_MODULE = 'iCrawler_python.spiders'


logger = logging.getLogger(__name__)

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.5
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.3
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 60
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'iCrawler_python.middlewares.UserAgentMiddleware': 98,                    # UA机制

    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'iCrawler_python.middlewares.SpiderRetryMiddleware': 97,                  # 重试机制

    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'iCrawler_python.middlewares.ProxyMiddleware': 99,                        # 代理机制
}

ITEM_PIPELINES = {
    'iCrawler_python.pipelines.IcrawlerPipeline': 125,
    'iCrawler_python.pipelines.UrlFilterPipeline': 300
}

# mongo config
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'Data'
MONGODB_USERNAME = ""
MONGODB_PASSWORD = ""

# mongo collection
DOUBANGAOFEN_MOVIE_COLLECTION = 'doubangaofen_movie'
LAGOUWANG_GANGWEIXINXI_COLLECTION = 'lagouwang_gangweixinxi'
NEWS_COLLECTION = 'news'

# redis config
DUPEFILTER_CLASS = 'iCrawler_python.url_filter.UrlRedisFilter'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 503, 504, 400, 429, 403]
RETRY_TIMES = 5
RETRY_PRIORITY_ADJUST = 0
