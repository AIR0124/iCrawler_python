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
    website_name = scrapy.Field()       # 来源
    message = scrapy.Field()            # 消息体
    title = scrapy.Field()              # 标题
    url = scrapy.Field()                # 正文URL
    pub_date = scrapy.Field()           # 发布时间
    html = scrapy.Field()               # 正文html
    pure_text = scrapy.Field()          # 正文文本
    name = scrapy.Field()               # 作者
    module_name = scrapy.Field()

class ZhihuUserItem(scrapy.Item):
    """
    知乎用户
    """
    answer_count = scrapy.Field()               # 回答数
    articles_count = scrapy.Field()             # 文章数
    badge = scrapy.Field()                      # 成就
    columns_count = scrapy.Field()              # 专栏数
    commercial_question_count = scrapy.Field()  # 提问数
    description = scrapy.Field()                # 描述
    educations = scrapy.Field()                 # 教育
    employments = scrapy.Field()                # 职业
    favorite_count = scrapy.Field()             # 收藏数
    favorited_count = scrapy.Field()            # 被收藏数
    follower_count = scrapy.Field()             # 粉丝数
    following_columns_count = scrapy.Field()    # 关注专栏的数量
    following_count = scrapy.Field()            # 他关注用户数量
    following_favlists_count = scrapy.Field()   # 他关注的收藏夹数量
    following_question_count = scrapy.Field()   # 他关注的问题数量
    following_topic_count = scrapy.Field()      # 他关注的话题数量
    gender = scrapy.Field()                     # 性别
    headline = scrapy.Field()
    hosted_live_count = scrapy.Field()          # 举办的live数量
    id = scrapy.Field()
    locations = scrapy.Field()                  # 地址
    logs_count = scrapy.Field()                 # 参与公共编辑次数
    marked_answers_count = scrapy.Field()       # 知乎收录的回答数量
    marked_answers_text = scrapy.Field()        # 知乎收录在的地址
    name = scrapy.Field()                       # 用户名
    participated_live_count = scrapy.Field()    # 参与live的数量
    pins_count = scrapy.Field()                 # 用户想法次数
    question_count = scrapy.Field()             # 提问次数
    thank_from_count = scrapy.Field()
    thank_to_count = scrapy.Field()
    thanked_count = scrapy.Field()              # 获得感谢次数
    type = scrapy.Field()
    url = scrapy.Field()
    url_token = scrapy.Field()
    user_type = scrapy.Field()
