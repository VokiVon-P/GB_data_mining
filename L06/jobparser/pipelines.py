# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from database.base import VacancyDB
from database.models import Vacancy
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy
        # self.sql_db = VacancyDB('sqlite:///vacancy.sqlite')

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        # db_item = Vacancy(name=item.get('name'), spider=spider.name, salary=item.get('salary'))
        # self.sql_db.add_salary(db_item)
        return item


class AvitoPhotosPipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
         if item.get('photos'):
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError:
                    pass

    def item_completed(self, results, item, info):
        # обрабатываем данные по фото
        if results:
            item['photos'] = [itm for ok, itm in results if ok]
            
        # обрабатываем данные по параметрам
        params = item.get('params')
        if params is not None:
            for itm in params:
                # приводим к чистым единичным строкам
                p_val = params.get(itm).strip().replace('\xa0м²','')
                # попытка приведения к числу
                try:
                    if p_val.isnumeric():
                        if p_val.isdecimal():
                            p_val = int(p_val)
                        else:
                            p_val = float(p_val)
                except:
                    pass
                #print(p_val)
                # записываем обработанное значение обратно в словарь
                params[itm] = p_val 

        return item
