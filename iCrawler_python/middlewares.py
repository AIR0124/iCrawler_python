# -*- coding: utf-8 -*-
import base64
import logging
import random
import uuid

from scrapy.conf import settings
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.http import HtmlResponse
from scrapy.utils.response import response_status_message

from iCrawler_python.settings import RETRY_HTTP_CODES, PROXY_SIZE, PROXY_MAX_USED_TIME
from iCrawler_python.settings import logger
from iCrawler_python.user_agent import agents


class UserAgentMiddleware(object):
    """
    切换User-Agent
    """
    def process_request(self, request, spider):
        # 如果已经设置了ua,则不需要重新设置
        exists_UA = request.headers.get('User-Agent')
        if not exists_UA:
            agent = random.choice(agents)
            # print("当前使用User-Agent是：" + agent)
            request.headers['User-Agent'] = agent


class SpiderRetryMiddleware(RetryMiddleware):
    """
    重试机制
    """
    def __init__(self, settings):
        super(SpiderRetryMiddleware, self).__init__(settings)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in RETRY_HTTP_CODES:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider):

        current_retry_times = request.meta.get('retry_times', 0)
        if str(reason).find('429') > -1:
            request.meta['retry_times'] = current_retry_times - 1
            logger.debug('Found proxy 429 status')
        return super(SpiderRetryMiddleware, self)._retry(request, reason, spider)


class ProxyMiddleware(object):
    """
    代理机制
    """
    def process_request(self, request, spider):
        userPass = 'H566QY611P76191D:8308510CA0847A5D'
        proxyAuth = 'Basic ' + base64.urlsafe_b64encode(bytes(userPass, 'ascii')).decode('utf8')
        request.meta['proxy'] = settings.get('proxyServer')
        request.headers['Proxy-Authorization'] = proxyAuth
        spider.logger.debug('The {0} Use AbuProxy'.format(request.url))
