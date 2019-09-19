# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SpjobSpider(scrapy.Spider):
    name = 'spjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bc%5D%5B0%5D=1']
    

    def parse(self, response: HtmlResponse):
        # находим ссылку на следующую страницу
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()
        # возвращаем объет данной функции со ссылкой на следующую страницу
        yield response.follow(next_page, callback=self.parse)

        # список ссылок на ваканции
        vacancy = response.css("div.f-test-vacancy-item a:not([target='_self'])::attr(href)").extract()
        # обрабатываем список 
        for link in vacancy:
            yield response.follow(link, callback=self.vacansy_parse)
            print(link)
        
        


    def vacansy_parse(self, response: HtmlResponse):
        # разбираем страницу вакансии
        name = response.css('h1::text').extract_first()
        url = response.url
        company_name = response.css('a.icMQ_ h2::text').extract_first()

        sal = response.css('span.ZON4b span::text').extract()
        if len(sal)>0:
            salary = ''.join(sal)
        else:
            salary = response.css('span.ZON4b::text').extract_first()
        # отдаем готовый элемент для дальнейшего сохранения в паплайнах
        yield JobparserItem(name=name, company_name=company_name, salary=salary, url = url)
        print(f'{name}\n{salary}\n{company_name}\n{url}')

