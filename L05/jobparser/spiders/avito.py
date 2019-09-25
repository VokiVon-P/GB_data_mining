# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    #start_urls = ['https://www.avito.ru/rossiya/vakansii?q=python']
    start_urls = ['https://www.avito.ru/rossiya/vakansii']
    
    
    

    def parse(self, response):
        """ - собираем urls простых и вип вакансий  
            - если есть следующая страница - вызываем себя для нее
            - вызываем разбор вакансии для каждого собранного url 
        """
        vacancy_urls = response.xpath('//a[contains(@class, "item-description-title-link")]/@href').extract()
        vip_urls = response.xpath('//div[contains(@class, "serp-vips")]//a[@class="description-title-link js-item-link"]/@href').extract()
        page_urls = vacancy_urls + vip_urls

        next_page = response.xpath('//div[contains(@class, "pagination-nav clearfix")]/a[@class="pagination-page js-pagination-next"]/@href').extract_first()
        print(page_urls)
        yield response.follow(next_page, callback=self.parse)
        
        for vac in page_urls:
            yield response.follow(vac, callback=self.parse_vacancy)
        


    def parse_vacancy(self, response: HtmlResponse):
        _tmp_cur = {'₽': 'RUB', '$': 'USD'}
        name = response.xpath("//div[@class='title-info-main']/h1/span[@class='title-info-title-text']/text()").extract_first()
        
        _tmp_values = response.xpath("//div[@class='_3MVeX']/span[contains(@class, '_3mfro')]/span/text()").extract()
        v_tmp = [int(itm.replace('\xa0', '')) for itm in _tmp_values[:-1] if itm.replace('\xa0', '').isdigit()]
        salary = {'currency': (lambda x: _tmp_cur[x] if x and x in _tmp_cur else None)(
            _tmp_values[-1]) if _tmp_values else None,
                  'min_value': v_tmp[0] if v_tmp else None,
                  'max_value': v_tmp[1] if v_tmp and len(v_tmp) > 1 else None,
                  }

        yield JobparserItem(name=name, salary=salary)

        
