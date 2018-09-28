# -*- coding: utf-8 -*-
import json
import re

import scrapy

from iCrawler_python.items import DoubangaofenItem


class DoubangaofenSpider(scrapy.Spider):
    """
    豆瓣高分电影爬虫
    """
    name = 'doubangaofen'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def __init__(self, *args, **kwargs):
        super(DoubangaofenSpider, self).__init__(*args, **kwargs)
        self.i = 0
        self.url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=豆瓣高分&sort=time&page_limit=20&page_start={0}'.format(self.i)

    def start_requests(self):

        yield scrapy.Request(
            url=self.url,
            callback=self.parse_list,
        )

    def parse_list(self, response):
        """
        解析列表页
        :param response:
        :return:
        """
        self.i += 20
        json_result = json.loads(response.body.decode('utf-8'))
        json_data = json_result['subjects']
        if not json_data:
            return
        for data in json_data:
            item = {}
            item['片名'] = data['title']
            item['url'] = data['url']
            item['评分'] = data['rate']
            detail_url = data['url']

            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={'_movie_item': item}
            )

        # 下一页
        next_page_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=豆瓣高分&sort=time&page_limit=20&page_start={0}'.format(self.i)
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
        item_movie = response.meta['_movie_item']
        item_movie['评价人数'] = response.xpath('//span[@property="v:votes"]/text()').extract_first()
        info = response.css('div.subject div#info').xpath('string(.)').extract_first()
        fields = [s.strip().replace(':', '') for s in response.css('div#info span.pl::text').extract()]
        values = [re.sub('\s+', '', s.strip()) for s in re.split('\s*(?:%s):\s*' % '|'.join(fields), info)][1:]
        item_movie.update(dict(zip(fields, values)))

        item = DoubangaofenItem()
        item['url'] = item_movie['url']
        item['title'] = item_movie['片名']
        if '导演' in item_movie:
            item['director'] = item_movie['导演']
        else:
            item['director'] = ''
        if '编剧' in item_movie:
            item['writer'] = item_movie['编剧']
        else:
            item['writer'] = ''
        if '类型' in item_movie:
            item['type'] = item_movie['类型']
        else:
            item['type'] = ''
        if '语言' in item_movie:
            item['language'] = item_movie['语言']
        else:
            item['language'] = ''
        if '制片国家/地区' in item_movie:
            item['district'] = item_movie['制片国家/地区']
        else:
            item['district'] = u''
        if u'上映日期' in item_movie:
            item['release_date'] = item_movie[u'上映日期']
        else:
            item['release_date'] = ''
        if '片长' in item_movie:
            item['time_long'] = item_movie['片长']
        else:
            item['time_long'] = ''
        item['douban_grade'] = item_movie['评分']
        item['rating_people_num'] = item_movie['评价人数']
        doubangaofen_item = DoubangaofenItem(item)

        yield doubangaofen_item