# -*- coding: utf-8 -*-
import scrapy


class SpjobSpider(scrapy.Spider):
    name = 'spjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['http://superjob.ru/']

    def parse(self, response):
        pass
