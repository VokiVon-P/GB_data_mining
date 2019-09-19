# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

"""
class SpjobSpider(scrapy.Spider):
    name = 'spjob'
    allowed_domains = ['superjob.ru']
    #start_urls = ['http://superjob.ru/']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        print(1)
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        yield JobparserItem(name='A', company_name='B', salary='C')

"""

class SpjobSpider(scrapy.Spider):
    name = 'spjob'
    allowed_domains = ['superjob.ru']
    #start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bc%5D%5B0%5D=1']
    

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        #vacancy = response.css('div.f-test-vacancy-item not(span.f-test-text-vacancy-item-company-name) a::attr(href)').extract()
        vacancy = response.css("div.f-test-vacancy-item a:not([target='_self'])::attr(href)").extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacansy_parse)
            print(link)
        
        


    def vacansy_parse(self, response: HtmlResponse):
        #name = response.css('div.vacancy-title h1.header::text').extract_first() response.css('h1.s1nFK::text').extract_first()
        name = response.css('h1::text').extract_first()
        #company_name = response.css('a.vacancy-company-name span::text').extract_first().strip() response.css('div.Ghoh2 a.icMQ_ h2::text').extract_first()
        company_name = response.css('a.icMQ_ h2::text').extract_first()
        #icMQ_ f-test-link-Federalnoe_gosudarstvennoe_nauchnoe_uchrezhdenie_Centr_informacionnyh_tehnologij_i_sistem_organov_ispolnitelnoj_vlasti_ _2JivQ
        #salary = response.css('div.vacancy-title p.vacancy-salary::text').extract_first()
        sal = response.css('span.ZON4b span::text').extract()
        if len(sal)>0:
            salary = ''.join(sal)
            #salary.replace('\xa0', ' ')
        else:
            salary = response.css('span.ZON4b::text').extract_first()
        yield JobparserItem(name=name, company_name=company_name, salary=salary)
        print(f'{name}\n{salary}\n{company_name}')

"""
    def parse(self, response: HtmlResponse):
        print(1)
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        company_name = response.css('a.vacancy-company-name span::text').extract_first().strip()
        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract_first()

        yield JobparserItem(name=name, company_name=company_name, salary=salary)
"""