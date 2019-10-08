# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import HtmlResponse, Request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from jobparser.items import JobparserItem


class FcSpider(scrapy.Spider):
    name = 'facebook'
    allowed_domains = ['facebook.com']
    start_urls = ['http://facebook.com/']


    def __init__(self, user_link, login, pswrd, *args, **kwargs):
        self.webdriver = webdriver.Chrome()
        
        self.login = login
        self.pswrd = pswrd
        self.first_profile = user_link
        self.is_init = False
        super().__init__(*args, *kwargs)
        


    def init_request(self):
        self.fc_login()
        self.is_init = True
        yield Request(self.webdriver.current_url, cookies=self.webdriver.get_cookies(),callback=self.parse)

            


    def fc_login(self):
        """ авторизуемся и переходим на стартовый профиль """
        self.webdriver.get(self.start_urls[0])
        try:
            mail = self.webdriver.find_element_by_xpath('//input[@class="inputtext login_form_input_box"][@type ="email"][@name ="email"]')
            pswd = self.webdriver.find_element_by_xpath('//input[@class="inputtext login_form_input_box"][@type ="password"][@name ="pass"]')
            login_btn = self.webdriver.find_element_by_xpath('//label[@class="login_form_login_button uiButton uiButtonConfirm"]/input[@type ="submit"][@value ="Log In"]')
        except:
            mail = self.webdriver.find_element_by_xpath('//input[@type ="text"][@name ="email"]')
            pswd = self.webdriver.find_element_by_xpath('//input[@type ="password"][@name ="pass"]')
            login_btn = self.webdriver.find_element_by_xpath('//button[@name ="login"][@type ="submit"]')

        mail.send_keys(self.login)
        pswd.send_keys(self.pswrd)
        login_btn.click()
        #self.webdriver.get(self.first_profile)


    def parse(self, response: HtmlResponse):
        if not self.is_init:
            self.fc_login()
            self.is_init = True
            yield Request(self.webdriver.current_url, cookies=self.webdriver.get_cookies(),callback=self.parse)
        else:
        
        #self.webdriver.refresh()
        #self.webdriver.get(self.first_profile)
        
        #usr_name  = self.webdriver.find_element_by_xpath('//a[@data-tab-key="friends"][@href]')

            yield response.follow(self.first_profile, callback=self.parse_page)
        

    def parse_page(self, response: HtmlResponse):
               
        # переходим на список друзей
        self.webdriver.get(response.url)
        friends_link  = self.webdriver.find_element_by_xpath('//a[@data-tab-key="friends"]').get_attribute('href')
        full_name = self.webdriver.find_element_by_xpath('//span[@data-testid="profile_name_in_profile_page"]/a').text

        self.webdriver.get(friends_link)

        # прокручиваем список
        body = self.webdriver.find_element_by_tag_name('body')
        _friend_list_item = '//div[@data-testid="friend_list_item"]/a'
        friends_len = len(self.webdriver.find_elements_by_xpath(
            _friend_list_item ))
        while True:
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            tmp_len = len(self.webdriver.find_elements_by_xpath(
                _friend_list_item ))
            if friends_len == tmp_len:
                break
            friends_len = len(self.webdriver.find_elements_by_xpath(
                _friend_list_item ))
        # если открытых друзей нет - прекращаем обработку
        if friends_len == 0:
            return

        # получаем и обрабатываем список друзей
        friends_list = self.webdriver.find_elements_by_xpath(_friend_list_item )
        href_list = list(map(lambda x: x.get_attribute('href'), friends_list))
        #print(f'Друзей у {full_name}= ', len(href_list))

        # сохраняем в базу
        yield JobparserItem(name = full_name, salary = [f'Всего друзей = {friends_len}', href_list])
        # и далее запускаем паучка рекурсивно по списку!
        for url in href_list:
            yield response.follow(url, callback=self.parse_page)
