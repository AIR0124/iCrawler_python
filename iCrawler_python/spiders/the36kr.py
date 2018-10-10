# -*- coding: utf-8 -*-
import json
import re

import scrapy
from bs4 import BeautifulSoup

from iCrawler_python.items import NewsItem


class The36ke(scrapy.Spider):
    """
    36氪关键词搜索爬虫
    """
    name = 'the36kr'
    allowed_domains = ['36kr.com']
    start_urls = ['https://36kr.com']

    def __init__(self, *args, **kwargs):
        super(The36ke, self).__init__(*args, **kwargs)
        self.i = 1
        self.keyword = 'python'

    def start_requests(self):

        yield scrapy.Request(
            url='https://36kr.com/api//search/entity-search?page={0}&per_page=40&keyword={1}&entity_type=post&sort=date'.format(self.i, self.keyword),
            callback=self.parse_list
        )

    def parse_list(self, response):
        """
        解析列表页
        :param response:
        :return:
        """
        self.i += 1
        json_data = json.loads(response.body)
        json_items = json_data['data']['items']
        if not json_items:
            return
        for json_item in json_items:
            id = json_item['id']
            title = json_item['title']
            url = 'https://36kr.com/p/' + str(id) + '.html'

            item = {
                'title': title,
                'url': url,
                'message': self.keyword,
                'website_name': '36氪',
                'module_name': '36氪搜索'
            }

            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                meta={'_item': item}
            )

        # 下一页
        next_page_url = 'https://36kr.com/api//search/entity-search?page={0}&per_page=40&keyword={1}&entity_type=post&sort=date'.format(self.i, self.keyword)
        yield scrapy.Request(
            url=next_page_url,
            callback=self.parse_list
        )

    def parse_detail(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        item = response.meta['_item']
        body = response.text
        content = re.findall(r'var props=(.*?),locationnal=', body)
        json_content = json.loads(content[0])
        item['pub_date'] = json_content['detailArticle|post']['published_at']
        item['name'] = json_content['detailArticle|post']['user']['name']
        html_text = json_content['detailArticle|post']['content']
        html = BeautifulSoup(html_text, 'lxml')
        item['html'] = str(html)
        item['pure_text'] = html.text.strip()

        the36krItem = NewsItem(item)
        yield the36krItem

