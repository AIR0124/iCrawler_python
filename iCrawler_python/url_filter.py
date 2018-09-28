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

        # 根据Request对象, 生成一个请求的指纹字符串
        # fp = self.request_fingerprint(request)
        # if fp in self.fingerprints:
        #     return True
        # self.fingerprints.add(fp)
        # if self.file:
        #     self.file.writer(fp + os.linesep)

class UrlFiltration(object):
    def __init__(self):
        redis_config = {'host': settings.get('REDIS_HOST'), 'port': settings.get('REDIS_PORT'), 'db': 15}
        self.pool = ConnectionPool(**redis_config)
        self.redis = StrictRedis(connection_pool=self.pool)
        self.key = 'spider_redis_key'

    def url_sha1(self, url):
        fp = hashlib.sha1()
        fp.update(canonicalize_url(url).encode('utf-8'))    # 将URL规范化为标准形式以避免重复
        url_sha1 = fp.hexdigest()
        return url_sha1

    def check_url(self, url):
        sha1 = self.url_sha1(url)
        isExist = self.redis.sismember(self.key, sha1)  # 判断URL是否在set中，不缓存URL信息
        return isExist

    def add_url(self, url):
        sha1 = self.url_sha1(url)
        added = self.redis.sadd(self.key, sha1)
        return added


