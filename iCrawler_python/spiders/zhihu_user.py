# -*- coding: utf-8 -*-
import scrapy
import json

from iCrawler_python.items import ZhihuUserItem


class Zhihu_User_Spider(scrapy.Spider):
    """
    知乎用户信息爬虫
    """
    name = 'zhihu_user'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 用户信息接口
    user_info_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    # 他关注的用户接口
    following_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    following_query = 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,collapsed_by,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics'
    # 粉丝用户接口
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    start_user = 'qiong-you-jin-nang'

    def __init__(self, *args, **kwargs):
        super(Zhihu_User_Spider, self).__init__(*args, **kwargs)

    def start_requests(self):
        # 请求用户信息
        yield scrapy.Request(
            url=self.user_info_url.format(user=self.start_user, include=self.user_query),
            callback=self.parse_user_info
        )
        # 请求他关注的用户
        yield scrapy.Request(
            url=self.following_url.format(user=self.start_user, include=self.following_query, offset=0, limit=20),
            callback=self.get_following_info
        )
        # 请求粉丝用户
        yield scrapy.Request(
            url=self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20),
            callback=self.get_followers_info
        )

    def parse_user_info(self, response):
        """
        解析用户信息
        :param response:
        :return:
        """
        item = ZhihuUserItem()
        result = json.loads(response.text)
        url_token = result.get('url_token')

        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)

        item['url'] = response.url
        zhihuuseritem = item
        yield zhihuuseritem

        yield scrapy.Request(
            url=self.following_url.format(user=url_token, include=self.following_query, offset=0, limit=20),
            callback=self.get_following_info
        )

        yield scrapy.Request(
            url=self.followers_url.format(user=url_token, include=self.followers_query, offset=0, limit=20),
            callback=self.get_followers_info
        )

    def get_following_info(self, response):
        """
        获取他关注的用户的url_token并请求他关注的用户的信息
        :param response:
        :return:
        """
        result = json.loads(response.text)
        if 'data' in result.keys():
            data = result.get('data')
            for user in data:
                url_token = user.get('url_token')
                url = self.user_info_url.format(user=url_token, include=self.user_query)

                yield scrapy.Request(
                    url=url,
                    callback=self.parse_user_info
                )
        # 判断是否有下一页
        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            next_url = result.get('paging').get('next')

            yield scrapy.Request(
                url=next_url,
                callback=self.get_following_info
            )

    def get_followers_info(self, response):
        """
        获取粉丝用户的url_token并请求粉丝用户的信息
        :param response:
        :return:
        """
        result = json.loads(response.text)

        if 'data' in result.keys():
            data = result.get('data')
            for user in data:
                url_token = user.get('url_token')
                url = self.user_info_url.format(user=url_token, include=self.user_query)

                yield scrapy.Request(
                    url=url,
                    callback=self.parse_user_info,
                )

        # 判断是否有下一页
        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            next_url = result.get('paging').get('next')

            yield scrapy.Request(
                url=next_url,
                callback=self.get_followers_info
            )
