# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/vakansii?q=python']
    #start_urls = ['https://www.avito.ru/rossiya/vakansii']
    
    
    

    def parse(self, response):
        """ - собираем urls простых и вип вакансий  
            - если есть следующая страница - вызываем себя для нее
            - вызываем разбор вакансии для каждого собранного url 
        """
        vacancy_urls = response.xpath('//a[contains(@class, "item-description-title-link")]/@href').extract()
        vip_urls = response.xpath('//div[contains(@class, "serp-vips")]//a[@class="description-title-link js-item-link"]/@href').extract()
        page_urls = vacancy_urls + vip_urls

        next_page = response.xpath('//div[contains(@class, "pagination-nav clearfix")]/a[@class="pagination-page js-pagination-next"]/@href').extract_first()
       
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        # пройдемся по всем вакансиям в списке
        for vac in page_urls:
            yield response.follow(vac, callback=self.parse_vacancy)
        


    def parse_vacancy(self, response: HtmlResponse):
        #_tmp_cur = {'₽': 'RUB', '$': 'USD'}
        # получим название вакансии
        name = response.xpath("//div[@class='title-info-main']/h1/span[@class='title-info-title-text']/text()").extract_first()
        # значение храниться в оттрибуте content в нужном нам виде
        _tmp_values = response.xpath("//div[@class='price-value price-value_side-card']//span[contains(@class, 'js-item-price')]/@content").extract_first()
        # название валюты можно получить прямо из атрибута - не нужно преобразований
        _tmp_currenvcy = response.xpath("//div[@class='price-value price-value_side-card']//span[contains(@class, 'price-value-prices-list-item-currency_sign')]/@content").extract_first()
        min_value = int(_tmp_values) if _tmp_values and _tmp_values.isdigit() else None
                
        salary = {'currency': _tmp_currenvcy,
                  'min_value': min_value,
                  'max_value': None
                  }

        yield JobparserItem(name=name, salary=salary)

        
