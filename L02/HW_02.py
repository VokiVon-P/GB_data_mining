
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import lxml
import time
import random

#mongo_url = 'mongodb://localhost:27017'

#USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 YaBrowser/19.9.0.1343 Yowser/2.5 Safari/537.36'


class AvitoFlatsParser:
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 YaBrowser/19.9.0.1343 Yowser/2.5 Safari/537.36'
    BASE_URL = 'https://www.avito.ru'

    def __init__(self):
        self._next_url = self.BASE_URL


    
    def parse(self, start_url):
        self._next_url = start_url
        while (self._next_url is not None):
            #self._prev_url = c_url
            #c_url = self._next_url
            ads_list = self.parse_page(self._next_url)
            #print(ads_list)
            self.save_to_mongo(ads_list)



    def req_ads(self, url):
        response = requests.get(url, headers={'User-Agent': self.USER_AGENT})
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            price = soup.body.findAll('span', attrs={'class': 'js-item-price', 'itemprop': 'price'})[0].attrs.get('content')
        except IndexError:
            price = None
        result = {'title': soup.head.title.text,
                'price': int(price) if price and price.isdigit else None,
                'url': response.url,
                'params': [tuple(itm.text.split(':')) for itm in
                            soup.body.findAll('li', attrs={'class': 'item-params-list-item'})]
                }
        return result


    def parse_page(self, page_url):
        response = requests.get(page_url, headers={'User-Agent': self.USER_AGENT}, proxies={'ip': 'port'})
        soup = BeautifulSoup(response.text, 'lxml')
        body = soup.html.body

        result = body.findAll('span', attrs={'data-marker': 'page-title/text'})
        #print(result)

        # находим указатель на следующую сраницу
        next_page = body.find('a', attrs={'class':'js-pagination-next'})
        if next_page is not None:
            self._next_url = f'{self.BASE_URL}{next_page.attrs.get("href")}'
        else:
            self._next_url = None
        
        
        ads = body.findAll('div', attrs={'class': ['item', 'item_table clearfix', 'js-catalog-item-enum', 'item-with-contact', 'js-item-extended']})
        urls = [f'{self.BASE_URL}{itm.find("a").attrs["href"]}' for itm in ads]
        return urls


        


    def save_to_mongo(self, urls: list):
        client = MongoClient('localhost', 27017)
        database = client.temp
        collection = database.avito
        for itm in urls:
            time.sleep(random.randint(1, 5))
            result = self.req_ads(itm)
            collection.insert_one(result)
            print('+', end='')

        print(f'\tСохранено {len(urls)} элементов!')
            
            

#


    
#url = 'https://www.avito.ru/zadonsk/kvartiry?cd=1'

url = 'https://www.avito.ru/sochi/kvartiry?cd=1&district=209'

parser = AvitoFlatsParser()
parser.parse(url)


#base_url = 'https://www.avito.ru'
#url = 'https://www.avito.ru/zadonsk/kvartiry?p=2&cd=1'


#url = 'https://www.avito.ru/zadonsk/kvartiry?p=2&cd=1'
'''
response = requests.get(url, headers={'User-Agent': USER_AGENT}, proxies={'ip': 'port'})
soup = BeautifulSoup(response.text, 'lxml')
body = soup.html.body
result = body.findAll('span', attrs={'data-marker': 'page-title/text'})
#div class="js-catalog_serp"  js-catalog_serp
next_page = body.find('a', attrs={'class':['pagination-page', 'js-pagination-nex']})
next_page_ulr = f'{base_url}{next_page.attrs.get("href")}'
#catalog-list js-catalog-list clearfix
#ads = body.findAll('div', attrs={'class': 'item item_table clearfix js-catalog-item-enum  item-with-contact js-item-extended'})
ads = body.findAll('div', attrs={'class': ['item', 'item_table clearfix', 'js-catalog-item-enum', 'item-with-contact', 'js-item-extended']})
urls = [f'{base_url}{itm.find("a").attrs["href"]}' for itm in ads]

collection = database.avito
# collection.insert_many(list(map(req_ads, urls)))

for itm in urls:
    time.sleep(random.randint(1, 5))
    result = req_ads(itm)
    collection.insert_one(result)

#
print(1)
'''