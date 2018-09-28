# -*- coding: utf-8 -*-
import json
import scrapy

from iCrawler_python.items import LagouwangItem


class LagouwangSpider(scrapy.Spider):
    """
    拉勾网岗位信息爬虫
    """
    name = 'lagouwang'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com']

    def __init__(self, *args, **kwargs):
        super(LagouwangSpider, self).__init__(*args, **kwargs)
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': ' https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        }
        self.detail_headers = {
            'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        }
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        self.total_page = 0
        self.first = 'true'
        self.kd = '爬虫'
        self.pn = 1

    def start_requests(self):

        yield scrapy.FormRequest(
            url=self.url,
            headers=self.headers,
            formdata={
                'first': self.first,
                'kd': self.kd,
                'pn': str(self.pn)
            },
            callback=self.parse_list
        )

    def parse_list(self, response):
        """
        解析列表页
        :param response:
        :return:
        """
        data = json.loads(response.body)
        data_position = data['content']['positionResult']
        if not data_position:
            return
        data_results = data_position['result']
        for data_result in data_results:
            positionId = data_result['positionId']
            detailUrl = 'https://www.lagou.com/jobs/' + str(positionId) + '.html'
            companyFullName = data_result['companyFullName']
            salary = data_result['salary']
            city = data_result['city']
            district = data_result['district']
            workYear = data_result['workYear']
            education = data_result['education']
            industryField = data_result['industryField']
            companySize = data_result['companySize']
            positionName = data_result['positionName']
            publishDate = data_result['createTime']

            item = {
                'url': detailUrl,
                'companyFullName': companyFullName,
                'salary': salary,
                'city': city,
                'district': district,
                'workYear': workYear,
                'education': education,
                'industryField': industryField,
                'companySize': companySize,
                'positionName': positionName,
                'publishDate': publishDate,
                'keyword': '爬虫',
            }

            yield scrapy.Request(
                url=detailUrl,
                headers=self.detail_headers,
                callback=self.parse_detail,
                meta={'_gangwei_item': item}
            )


        # 下一页
        if (self.pn <= 31):
            self.pn += 1
            self.first = 'false'
            yield scrapy.FormRequest(
                url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
                headers=self.headers,
                formdata={
                    'first': self.first,
                    'kd': self.kd,
                    'pn': str(self.pn)
                },
                callback=self.parse_list
            )

    def parse_detail(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        document = ''
        item = response.meta['_gangwei_item']
        jobDescription = response.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()').extract()
        for i in range(len(jobDescription)):
            doc = jobDescription[i].replace('\xa0', '').replace(' ', '')
            if i == 1:
                document = doc
            else:
                document = document + '\n' + doc
        item['jobDescription'] = document
        lagouwangItem = LagouwangItem(item)
        yield lagouwangItem