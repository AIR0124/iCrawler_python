# -*- coding: utf-8 -*-
import json
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup

from iCrawler_python.items import WZItem


class ZhihuhaoSpider(scrapy.Spider):
    """
    知乎号专栏文章爬虫
    """
    name = 'zhihuhao'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com']

    def __init__(self, *args, **kwargs):
        super(ZhihuhaoSpider, self).__init__(*args, **kwargs)
        # 专栏文章请求头
        self.headers_zhuanlan = {
            'Host': 'zhuanlan.zhihu.com',
        }
        kwargs['message'] = '{"keyword": "qiong-you-jin-nang"}'    # test
        self.message = json.loads(kwargs.get('message'))
        self.keyword = self.message.get('keyword', '')
        self.i = 0

    def start_requests(self):

        yield scrapy.Request(
            url='https://www.zhihu.com/api/v4/members/{0}/articles?offset={1}&limit=20'.format(self.keyword, self.i),
            callback=self.parse_list,
        )

    def parse_list(self, response):
        """
        解析列表页
        :param response:
        :return:
        """
        self.i += 20
        json_result = json.loads(response.body)
        json_data = json_result['data']
        if not json_data:
            return
        for json_target in json_data:
            detail_url = json_target['url']
            name = json_target['author']['name']
            item = {
                'url': detail_url,
                'name': name,
                'module_name': self.keyword,
            }

            yield scrapy.Request(
                url=detail_url,
                headers=self.headers_zhuanlan,
                callback=self.parse_detail,
                meta={
                    '_item': item
                }
            )

        # 下一页
        next_page_url = 'https://www.zhihu.com/api/v4/members/{0}/articles?offset={1}&limit=20'.format(self.keyword, self.i),
        next_page_url = next_page_url[0]
        yield scrapy.Request(
            url=next_page_url,
            callback=self.parse_list,
        )

    def parse_detail(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        item = response.meta['_item']
        item['title'] = response.xpath('//h1/text()').extract_first()
        document = BeautifulSoup(response.body, 'lxml')
        divs = document.select('div.RichText')
        if divs:
            content = ''
            for div in divs:
                div_str = str(div)
                if len(div_str) > len(content):
                    content = div_str
        else:
            return
        document = BeautifulSoup(content, 'lxml')

        # 删除noscript标签
        noscripts = document.select('figure noscript')
        if noscripts:
            for noscript in noscripts:
                noscript.extract()
        # 判断src属性值，如果不是jpg格式就进行替换src属性值
        imgs = document.select('img')
        if imgs:
            for img in imgs:
                try:
                    data_original = img.get('data-original')
                    src = img.get('src')
                    data_actualsrc = img.get('data-actualsrc')
                    if src:
                        if '.jpg' in src:
                            continue
                        elif data_original and src:
                            img['src'] = data_original
                        elif not data_original and data_actualsrc:
                            img['src'] = data_actualsrc
                    elif not src and data_actualsrc:
                        img['src'] = data_actualsrc
                except Exception as e:
                    continue

        pure_text = document.text.strip()
        time = response.xpath('//*[@class="PostIndex-author"]')
        date = time.xpath('div[@class="HoverTitle"]/@data-hover-title').extract_first()
        if date:
            item['pub_date'] = str(datetime.strptime(date, '%a, %b %d, %Y %I:%M %p'))
        else:
            date = response.xpath('//span/@data-tooltip').extract_first()
            pub_time = date.replace('发布于 ', '')
            item['pub_date'] = pub_time + ':00'

        item['html'] = str(document)
        item['pure_text'] = pure_text

        fp = open('D:\source_code\GitHub\iCrawler_python\iCrawler_python\spider_html\\' + str(item['title']) + '.html', 'wb')
        fp.write(bytes(item['html'], encoding='utf8'))
        fp.close()

        zhihuhao_item = WZItem(item)
        yield zhihuhao_item