# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubangaofenItem(scrapy.Item):
    """
    豆瓣高分电影
    """
    title = scrapy.Field()              # 电影名称
    url = scrapy.Field()                # 详情页URL
    director = scrapy.Field()           # 导演
    writer = scrapy.Field()             # 编剧
    actor = scrapy.Field()              # 演员
    type = scrapy.Field()               # 电影类型
    district = scrapy.Field()           # 地区
    language = scrapy.Field()           # 语言
    release_date = scrapy.Field()       # 上映日期
    time_long = scrapy.Field()          # 片长
    douban_grade = scrapy.Field()       # 豆瓣评分
    rating_people_num = scrapy.Field()  # 评价人数

class LagouwangItem(scrapy.Item):
    """
    拉勾网岗位信息
    """
    keyword = scrapy.Field()
    url = scrapy.Field()                # 详情页URL
    companyFullName = scrapy.Field()    # 公司名称
    salary = scrapy.Field()             # 薪水
    city = scrapy.Field()               # 城市
    district = scrapy.Field()           # 区域
    workYear = scrapy.Field()           # 工作时间
    education = scrapy.Field()          # 教育背景
    industryField = scrapy.Field()      # 公司所属领域
    companySize = scrapy.Field()        # 公司规模
    positionName = scrapy.Field()       # 岗位名称
    publishDate = scrapy.Field()        # 发布时间
    jobDescription = scrapy.Field()     # 职位描述

class NewsItem(scrapy.Item):
    """
    文章类
    """
    zhihuhao = scrapy.Field()           # 知乎号
    title = scrapy.Field()              # 标题
    url = scrapy.Field()                # 正文URL
    pub_date = scrapy.Field()           # 发布时间
    html = scrapy.Field()               # 正文html
    pure_text = scrapy.Field()          # 正文文本
    name = scrapy.Field()               # 知乎号名称
