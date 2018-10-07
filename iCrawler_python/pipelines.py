# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.crawler import logger

from iCrawler_python.item_processors.news_item_processor import process_news_item
from iCrawler_python.items import DoubangaofenItem, NewsItem, LagouwangItem
from iCrawler_python.url_filter import UrlFiltration


class IcrawlerPipeline(object):
    doubangaofen_movie = settings.get('DOUBANGAOFEN_MOVIE_COLLECTION')
    lagouwang_gangweixinxi = settings.get('LAGOUWANG_GANGWEIXINXI_COLLECTION')
    news = settings.get('NEWS_COLLECTION')

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        db = self.client[self.mongo_db]
        self.doubangaofen_movie_collection = db[self.doubangaofen_movie]
        self.lagouwang_collection = db[self.lagouwang_gangweixinxi]
        self.news_collection = db[self.news]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """
        判断item的类型，并作相应的处理，再入数据库
        """
        if isinstance(item, DoubangaofenItem):
            try:
                self.doubangaofen_movie_collection.insert(dict(item))
            except Exception as e:
                logger.exception(str(e))
        elif isinstance(item, LagouwangItem):
            try:
                self.lagouwang_collection.insert(dict(item))
            except Exception as e:
                logger.exception(str(e))
        elif isinstance(item, NewsItem):
            try:
                process_news_item(item)
                self.news_collection.insert(dict(item))
            except Exception as e:
                logger.exception(str(e))
        return item


class UrlFilterPipeline(object):
    """
    将已爬取的URL放入redis
    """
    def __init__(self):
        self.dupefilter = UrlFiltration()

    def process_item(self, item, spider):
        self.dupefilter.add_url(item['url'])
        return item
