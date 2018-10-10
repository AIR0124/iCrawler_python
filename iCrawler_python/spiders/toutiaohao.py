# -*- coding: utf-8 -*-
import hashlib
import json
import math
import time
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup

from iCrawler_python.items import NewsItem
from iCrawler_python.settings import logger


class ToutiaohaoSpider(scrapy.Spider):
    """
    头条号m站爬虫
    """
    name = 'toutiaohao'
    allowed_domains = ['toutiao.com']
    start_urls = ['http://m.toutiao.com/profile/{0}/']
    api_url = 'https://www.toutiao.com/pgc/ma/?page_type=1&max_behot_time={0}&uid={1}&media_id={2}&output=json&is_json=1&count=20&from=user_profile_app&version=2&as={3}&cp={4}'
    detail_url = 'https://m.toutiao.com/i{0}/info/?i={0}'
    max_retry_times = 15

    def __init__(self, *args, **kwargs):

        super(ToutiaohaoSpider, self).__init__(*args, **kwargs)
        self.message = {
            'keyword': '50413226082'
        }
        self.keyword = self.message.get('keyword', '')
        self.req_headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        }
        self.pages = 10
        self.time_format = u"%Y-%m-%d %H:%M:%S"

    def start_requests(self):
        """
        程序入口
        :param self:
        :return:
        """
        curr_page = 1
        if not self.keyword:
            logger.info('Message has no user_id')
            return
        user_id = self.keyword
        url = self.start_urls[0].format(user_id)
        meta_dict = {
            'url': url,
            'curr_page': curr_page,
            'user_id': user_id
        }

        yield scrapy.Request(
            url=url,
            callback=self.handle_user_profile_page,
            meta=meta_dict,
            headers=self.req_headers
        )

    def handle_user_profile_page(self, response):
        url = response.meta.get('url')
        curr_page = response.meta.get('curr_page')
        user_id = response.meta.get('user_id')
        logger.info('Getting %s toutiaohao user profile data' % url)

        response_text = response.text
        start_index = response_text.find('mediaId = ')
        end_index = response_text.find(',', start_index)
        user_mid = response_text[start_index + 10: end_index]\
            .replace('\'', '').replace(' ', '')
        url = self._generate_url(user_id=user_id, user_mid=user_mid)
        meta_dict = {
            'url': url,
            'curr_page': curr_page,
            'user_id': user_id,
            'user_mid': user_mid
        }
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta=meta_dict,
            headers=self.req_headers,
            dont_filter=True
        )

    def parse(self, response):
        url = response.meta.get('url')
        curr_page = response.meta.get('curr_page')
        user_id = response.meta.get('user_id')
        user_mid = response.meta.get('user_mid')
        retry_times = response.meta.get('_retry_times')
        if not retry_times:
            retry_times = 0
        next_behot_time = None
        has_more = 0
        response_text = response.body.decode()
        if response_text.find('jsonp4(') > -1:
            response_text = response_text[7:]
        if response_text.endswith(')'):
            response_text = response_text[0:len(response_text)-1]
        json_data = json.loads(response_text)
        if json_data.get('next') and json_data.get('next').get('max_behot_time'):
            next_behot_time = json_data.get('next').get('max_behot_time')  # 错误时=0
        if json_data.get('has_more'):
            has_more = int(json_data.get('has_more'))
        logger.info('Processing toutiaohao %s page %s' % (user_id, curr_page))
        data_list = json_data.get('data')
        # 请求详情信息
        for row in data_list:
            item = {
                'title': row.get('title'),
                'url': 'http://toutiao.com/group/{0}/'.format(row.get('str_item_id')),
                'pub_date': datetime.fromtimestamp(int(row.get('publish_time'))).strftime(self.time_format),
                'website_name': '今日头条',
                'module_name': '头条号',
                'message': self.keyword,
                'name': row.get('source'),
            }
            item_id = row.get('str_item_id')
            detail_page_url = self.detail_url.format(item_id)
            detail_meta = {
                'item': item,
                'url': detail_page_url
            }

            yield scrapy.Request(
                url=detail_page_url,
                callback=self.parse_detail,
                meta=detail_meta,
                headers=self.req_headers
            )

        # 下一页
        if has_more == 1 and next_behot_time and next_behot_time != u'0':
            if curr_page + 1 > self.pages:
                return
            next_url = self._generate_url(user_id=user_id, user_mid=user_mid,
                                          next_behot_time=next_behot_time)
            meta_dict = {
                'url': next_url,
                'curr_page': curr_page + 1,
                'user_id': user_id,
                'user_mid': user_mid
            }
            yield response.follow(
                url=next_url,
                callback=self.parse,
                meta=meta_dict,
                headers=self.req_headers
            )
        else:
            # 重试
            if retry_times < self.max_retry_times:
                meta_dict = {
                    'url': url,
                    'curr_page': curr_page,
                    'user_id': user_id,
                    'user_mid': user_mid,
                    '_retry_times': retry_times + 1
                }
                logger.debug("Retry toutiao list - %s, %s" % (str(retry_times+1), url))

                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta=meta_dict,
                    headers=self.req_headers,
                    dont_filter=True
                )
            else:
                logger.debug("No next page found - %s, %s " % (str(has_more), str(next_behot_time)))

    def parse_detail(self, response):
        detail_page_url = response.meta['url']
        item = response.meta['item']
        detail_html = response.text
        resp_json = json.loads(detail_html)
        item['html'] = resp_json['data']['content']
        soup = BeautifulSoup(item['html'], 'lxml')
        item['pure_text'] = soup.get_text(separator='\n', strip=True)
        item['url'] = detail_page_url

        toutiao_news_item = NewsItem(item)
        yield toutiao_news_item

    def _generate_as_cp(self):
        as_val = '479BB4B7254C150'
        cp_val = '7E0AC8874BB0985'
        t = int(math.floor(time.time()))
        e = str(hex(t)).upper()[2:]  # 删除16禁止开头
        str_t = str(t).encode(encoding='utf-8')
        md5 = hashlib.md5()
        md5.update(str_t)
        t_md5 = md5.hexdigest()
        i = t_md5.upper()   # 将小写字母转为大写字母
        if len(e) == 8:
            a = i[0:5]
            n = i[-5:]
            o = ""
            for r in range(0, 5):
                o += a[r:r + 1] + e[r:r + 1]
            l = ""
            for s in range(0, 5):
                l += e[s + 3:s + 4] + n[s:s + 1]
            as_val = "A1" + o + e[-3:]
            cp_val = e[0:3] + l + "E1"
        return as_val, cp_val

    def _generate_url(self, user_id, user_mid, next_behot_time=None):
        """
        产生一个url
        :param user_id:
        :param next_behot_time:
        :return:
        """
        if not next_behot_time:
            next_behot_time = ""
        as_val, cp_val = self._generate_as_cp()
        url = self.api_url.format(next_behot_time, user_id, user_mid, as_val, cp_val)
        logger.debug(u'Generate url - {0}'.format(url))
        return url
