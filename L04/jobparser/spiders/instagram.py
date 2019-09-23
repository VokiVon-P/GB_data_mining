# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode, urljoin
from copy import deepcopy
from jobparser.items import InstaItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    #получаем до 10 постов
    variables_base = {"first": 10}
    #variables_base = {'fetch_mutual': 'false', "include_reel": 'true', "first": 100}
    followers = {}
    posts = {}
    custom_settings = {
        'ITEM_PIPELINES': {
            'jobparser.pipelines.InstaParserPipeline': 400
        }
    }

    def __init__(self, user_links, login, pswrd, *args, **kwargs):
        self.user_links = user_links
        self.login = login
        self.pswrd = pswrd
        # поменял хэш на запрос постов
        self.query_hash = '58b6785bea111c67129decbe6a448951'
        #self.query_hash = 'c76146de99bb02f6415203be841dd25a'
        super().__init__(*args, *kwargs)

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            'https://www.instagram.com/accounts/login/ajax/',
            method='POST',
            callback=self.parse_users,
            formdata={'username': self.login, 'password': self.pswrd},
            headers={'X-CSRFToken': csrf_token}
        )

    def parse_users(self, response: HtmlResponse):
        j_body = json.loads(response.body)
        if j_body.get('authenticated'):
            for user in self.user_links:
                yield response.follow(urljoin(self.start_urls[0], user),
                                      callback=self.parse_user,
                                      cb_kwargs={'user': user})

    def parse_user(self, response: HtmlResponse, user):
        user_id = self.fetch_user_id(response.text, user)
        user_vars = deepcopy(self.variables_base)
        user_vars.update({'id': user_id})
        yield response.follow(self.make_graphql_url(user_vars),
                              #callback=self.parse_folowers,
                              callback=self.parse_posts,
                              cb_kwargs={'user_vars': user_vars, 'user': user})


    def fetch_csrf_token(self, text):
        """Используя регулярные выражения парсит переданную строку на наличие
        `csrf_token` и возвращет его."""
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        """Используя регулярные выражения парсит переданную строку на наличие
        `id` нужного пользователя и возвращет его."""
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')


    def make_graphql_url(self, user_vars):
        """Возвращает `url` для `graphql` запроса"""
        result = '{url}query_hash={hash}&{variables}'.format(
            url=self.graphql_url, hash=self.query_hash,
            variables=urlencode(user_vars)
        )
        return result

    #6ff3f5c474a240353993056428fb851e

    def get_posts_info(self, posts : list):
        """ выбираем только нужные данные из поста """
        result = {}
        for item in posts:
            node = item.get('node')
            post = {}
            post['id'] = node.get('id')
            post['display_url'] = node.get('display_url')
            post['is_video'] = node.get('is_video')
            post['owner'] = node.get('owner')
            post['shortcode'] = node.get('shortcode')
            post['caption'] = node.get('edge_media_to_caption').get('edges')[0].get('node').get('text')
            post['comment_users'] = [item.get('node').get('owner').get('username') for item in node.get('edge_media_to_comment').get('edges')]
            result[post['id']] = post
        return result
            


    def parse_posts(self, response: HtmlResponse, user_vars, user):
            data = json.loads(response.body)
            if not self.posts.get(user):
                self.posts[user] = {'posts': self.get_posts_info(data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')),
                                    'count': len(data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges'))
                                    }
            else:
                pass

            print(self.posts[user] ['posts'])
            yield InstaItem(name=user, posts=self.posts[user])
    

"""
    def parse_folowers(self, response: HtmlResponse, user_vars, user):
        data = json.loads(response.body)
        if not self.followers.get(user):
            self.followers[user] = {'followers': data.get('data').get('user').get('edge_followed_by').get('edges'),
                                    'count': data.get('data').get('user').get('edge_followed_by').get('count'),
                                    }
        else:
            self.followers[user]['followers'].extend(data.get('data').get('user').get('edge_followed_by').get('edges'))

        if data.get('data').get('user').get('edge_followed_by').get('page_info').get('has_next_page'):
            user_vars.update(
                {'after': data.get('data').get('user').get('edge_followed_by').get('page_info').get('end_cursor')})
            next_page = self.make_graphql_url(user_vars)

            yield response.follow(next_page, callback=self.parse_folowers,
                                  cb_kwargs={'user_vars': user_vars, 'user': user})

        if self.followers.get(user) and self.followers.get(user).get('count') == len(self.followers.get(user).get('followers')):
            pass

"""