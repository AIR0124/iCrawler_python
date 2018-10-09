# -*- coding: utf-8 -*-
import hashlib
import os

from redis import ConnectionPool, StrictRedis
from scrapy.conf import settings
from scrapy.dupefilters import RFPDupeFilter
from w3lib.url import canonicalize_url


class UrlRedisFilter(RFPDupeFilter):
    """
    根据URL去重，实现增量抓取
    """
    def request_seen(self, request):
        self.dupefilter = UrlFiltration()

        if self.dupefilter.check_url(request.url):
            print(request.url + '已抓')
            return True

class UrlFiltration(object):
    def __init__(self):
        redis_config = {'host': settings.get('REDIS_HOST'), 'port': settings.get('REDIS_PORT'), 'db': 15}
        self.pool = ConnectionPool(**redis_config)
        self.redis = StrictRedis(connection_pool=self.pool)
        self.key = 'spider_redis_key'

    def url_md5(self, url):
        fp = hashlib.md5()
        fp.update(canonicalize_url(url).encode('utf-8'))    # 将URL规范化为标准形式以避免重复
        url_md5 = fp.hexdigest()
        return url_md5

    def check_url(self, url):
        md5 = self.url_md5(url)
        isExist = self.redis.sismember(self.key, md5)  # 判断URL是否在set中，不缓存URL信息，true已抓
        return isExist

    def add_url(self, url):
        md5 = self.url_md5(url)
        added = self.redis.sadd(self.key, md5)
        return added


