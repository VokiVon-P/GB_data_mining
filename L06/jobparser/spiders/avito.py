# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from jobparser.items import AvitoRealEstate
from scrapy.loader.processors import MapCompose, TakeFirst


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/komnaty']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)
        pass

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoRealEstate(), response=response)
        loader.add_xpath('photos',
                         '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')
        # используем вложенный лоадер для разбора параметров жилья
        param_loader = loader.nested_xpath('//div[contains(@class, "item-params")]/ul')
        # получим ключи и сразу их почистим
        p_keys = list(map(lambda x: x.replace(': ', ''), param_loader.get_xpath('//li[@class = "item-params-list-item"]/span[@class = "item-params-label"]/text()')))
        # получим значения - очистку и конвертацию будем делать на этапе паплайна
        p_values = param_loader.get_xpath('//li[@class = "item-params-list-item"]/text()[2]')
        # p_values = list(map(lambda k: k.replace('\xa0м²',''), map(lambda x: x.strip(), p_values)))
        # p_values = list(map(lambda k: k.replace('\xa0м²',''), map(str.strip, p_values)))
        # создадим словарь с параметрами
        params = dict(zip(p_keys, p_values))
        
        param_loader.add_value('params', params) 
        

        #param_loader.add_xpath('p_vals', '//li[@class = "item-params-list-item"]/text()')

        # _tmp_values = response.xpath('//div[contains(@class, "item-params")]/ul//li[@class = "item-params-list-item"]/span/text()').extract()
        # loader.add_xpath('params','//div[contains(@class, "item-params")]//ul[contains(@class, "item-params-list-item")]')
        # response.xpath('//div[contains(@class, "item-params")]/ul//li/span')
        yield loader.load_item()
