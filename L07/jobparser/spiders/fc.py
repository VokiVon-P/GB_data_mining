# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import HtmlResponse, Request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from jobparser.items import FacebookItem


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
        # при инициализации авторизуемся и передаем куки, после подгружаем себя же 
        if not self.is_init:
            self.fc_login()
            self.is_init = True
            yield Request(self.webdriver.current_url, cookies=self.webdriver.get_cookies(),callback=self.parse)
        else:
            yield response.follow(self.first_profile, callback=self.parse_page)
        

    def parse_page(self, response: HtmlResponse):
               
        # переходим на персональную страницу
        self.webdriver.get(response.url)
        # ссылка на картинки аватаров
        avatar_link = self.webdriver.find_element_by_xpath('//div[@id="fbTimelineHeadline"]//div[@class="photoContainer"]/div/a').get_attribute('href')
        # ссылка на инфо
        info_link  = self.webdriver.find_element_by_xpath('//a[@data-tab-key="about"]').get_attribute('href')
        # ссылка на списк друзей
        friends_link  = self.webdriver.find_element_by_xpath('//a[@data-tab-key="friends"]').get_attribute('href')

        """
        Секция обработки персональных данных
        """
        # получаем полное имя и фамилию
        item_full_name = self.webdriver.find_element_by_xpath('//span[@data-testid="profile_name_in_profile_page"]/a').text
         # переходим на инфо и получаем дату рождения если есть
        self.webdriver.get(info_link)
        contact_link = self.webdriver.find_element_by_xpath('//div[@data-testid="info_section_left_nav"]/a[@testid="nav_contact_basic"]').get_attribute('href')
        self.webdriver.get(contact_link)
        item_birthdate = None
        try:
            # получаю строку, разбиваю, беру дату и привожу ее чистый строковой вид
            item_birthdate = self.webdriver.find_element_by_xpath('//div[@id="pagelet_basic"]//ul/li').text.split('\n')[1][:-3]
            # далее можно попробовать заморочиться и перевести в datetime - но не в этот раз.
        except:
            pass

        """
        Секция обработки картинок с аватара
        <div id="fbTimelinePhotosContent" class="fbPhotosRedesignBorderOverlay">
            <div class="_1wzl" id="fbTimelinePhotosFlexgrid">
                <div style="width: 165.25905292479px; flex-grow: 1.0027855153203;" class="_vor focus_target _53s fbPhotoCurationControlWrapper child_is_active child_was_focused" data-fbid="807018239398984" id="u_0_2k">
                <i style="padding-bottom: 99.722222222222%;"></i>
                <a ajaxify="https://www.facebook.com/photo.php?fbid=807018239398984&amp;set=a.107327909368024&amp;type=3&amp;size=1040%2C1038" 
                href="https://www.facebook.com/photo.php?fbid=807018239398984&amp;set=a.107327909368024&amp;type=3&amp;size=1040%2C1038" rel="theater" id="u_0_2j"><img class="_pq3 img" src="https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif" alt="На изображении может находиться: один или несколько человек, океан, вода, на улице и природа" style="background-image: url('https\3a //scontent-arn2-2.xx.fbcdn.net/v/t1.0-0/p417x417/14141826_807018239398984_3251381103283133009_n.jpg?_nc_cat\3d 100\26 _nc_oc\3d AQkJBNdbb93guLRyilmuOJi6NZf8YQU2Ks3mrcCsf1fYgQu4xZ7E3H6ULJN0NngB0KI\26 _nc_ht\3d scontent-arn2-2.xx\26 oh\3d 5b59bdcdcd7a3abcf0f7ccfb13289900\26 oe\3d 5E230EBC');"></a><div class="_53d _53q"><div data-fbid="807018239398984" id="u_0_2v"><div class="_5gl-" id="u_0_2r"><a href="#" role="button" class="_5glz _53o _53b">Нравится</a><a href="#" role="button" class="_5glz _53p _53b">Не нравится</a><span class="_6ib"> · </span><a class="_5glz _s4z" role="button" href="#" id="u_0_2w">Комментировать</a><a class="_5gly _5glz" role="button" aria-label="Нравится: 6" href="#" id="u_0_2x"><div class="_53z"><div class="_4cn2 _4cn4" aria-label="6 likes"><div class="_29qi"><i class="img sp_4dN0mIj9BZd sx_d30747"></i></div><div class="_2ieq">6</div></div></div></a></div></div><img src="/images/photos/profile/gradient.png" class="_53l" alt=""></div></div><div style="width: 164.8px; flex-grow: 1;" class="_vor focus_target _53s fbPhotoCurationControlWrapper" data-fbid="677817588985717" id="u_0_2q"><i style="padding-bottom: 100%;"></i><a ajaxify="https://www.facebook.com/photo.php?fbid=677817588985717&amp;set=a.107327909368024&amp;type=3&amp;size=1440%2C1440" href="https://www.facebook.com/photo.php?fbid=677817588985717&amp;set=a.107327909368024&amp;type=3&amp;size=1440%2C1440" rel="theater" id="u_0_2p"><img class="_pq3 img" src="https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif" alt="На изображении может находиться: 1 человек" style="background-image: url('https\3a //scontent-arn2-2.xx.fbcdn.net/v/t1.0-0/p417x417/12242998_677817588985717_6240804416166156090_n.jpg?_nc_cat\3d 105\26 _nc_oc\3d AQnM9BOXDMakdVIiUJsBc8TFICmHl_krCmb32JTtS-lM_TRY6qZJzXg_pJNKg-P0Zj0\26 _nc_ht\3d scontent-arn2-2.xx\26 oh\3d 322b886b2293bff86a8f39d74fb41c55\26 oe\3d 5E31497D');"></a><div class="_53d _53q"><div data-fbid="677817588985717" id="u_0_2y"><div class="_5gl-" id="u_0_2s"><a href="#" role="button" class="_5glz _53o _53b">Нравится</a><a href="#" role="button" class="_5glz _53p _53b">Не нравится</a><span class="_6ib"> · </span><a class="_5glz _s4z" role="button" href="#" id="u_0_2z">Комментировать</a><a class="_5gly _5glz" role="button" aria-label="Нравится: 1" href="#" id="u_0_30"><div class="_53z"><div class="_4cn2 _4cn4" aria-label="1 likes"><div class="_29qi"><i class="img sp_4dN0mIj9BZd sx_d30747"></i></div><div class="_2ieq">1</div></div></div></a></div></div><img src="/images/photos/profile/gradient.png" class="_53l" alt=""></div></div><div style="width: 164.8px; flex-grow: 1;" class="_vor focus_target _53s fbPhotoCurationControlWrapper" data-fbid="667285610038915" id="u_0_2m"><i style="padding-bottom: 100%;"></i><a ajaxify="https://www.facebook.com/photo.php?fbid=667285610038915&amp;set=a.107327909368024&amp;type=3&amp;size=960%2C960" href="https://www.facebook.com/photo.php?fbid=667285610038915&amp;set=a.107327909368024&amp;type=3&amp;size=960%2C960" rel="theater" id="u_0_2l"><img class="_pq3 img" src="https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif" alt="На изображении может находиться: 2 человека" style="background-image: url('https\3a //scontent-arn2-2.xx.fbcdn.net/v/t1.0-0/p417x417/12122482_667285610038915_8136230970125921235_n.jpg?_nc_cat\3d 104\26 _nc_oc\3d AQkjhG9xtWUeLPTT-WVOGjcPL2iWU_HlDlesF15D6gQ50hbUaZldpLmWx8Ry9BzkLEw\26 _nc_ht\3d scontent-arn2-2.xx\26 oh\3d 3ecb141f5fac7f2db5b7e5be8af6a40b\26 oe\3d 5E2D7B56');"></a><div class="_53d _53q"><div data-fbid="667285610038915" id="u_0_31"><div class="_5gl-" id="u_0_2u"><a href="#" role="button" class="_5glz _53o _53b">Нравится</a><a href="#" role="button" class="_5glz _53p _53b">Не нравится</a><span class="_6ib"> · </span><a class="_5glz _s4z" role="button" href="#" id="u_0_32">Комментировать</a><a class="_5gly _5glz" role="button" aria-label="6 отметок «Нравится» и 1 комментарий" href="#" id="u_0_33"><div class="_53z"><div class="_4cn2 _4cn4" aria-label="6 likes"><div class="_29qi"><i class="img sp_4dN0mIj9BZd sx_d30747"></i></div><div class="_2ieq">6</div></div><div class="_4cn3 _4cn4" aria-label="1 comments"><div class="_29qj"><i class="img sp_4dN0mIj9BZd sx_8f33c1"></i></div><div class="_2ieq">1</div></div></div></a></div></div><img src="/images/photos/profile/gradient.png" class="_53l" alt=""></div></div><div style="width: 292.97777777778px; flex-grow: 1.7777777777778;" class="_vor focus_target _53s fbPhotoCurationControlWrapper" data-fbid="107327912701357" id="u_0_2o"><i style="padding-bottom: 56.25%;"></i><a ajaxify="https://www.facebook.com/photo.php?fbid=107327912701357&amp;set=a.107327909368024&amp;type=3&amp;size=2048%2C1153" href="https://www.facebook.com/photo.php?fbid=107327912701357&amp;set=a.107327909368024&amp;type=3&amp;size=2048%2C1153" rel="theater" id="u_0_2n"><img class="_pq3 img" src="https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif" alt="На изображении может находиться: 1 человек" style="background-image: url('https\3a //scontent-arn2-2.xx.fbcdn.net/v/t31.0-0/p417x417/288425_107327912701357_2963940_o.jpg?_nc_cat\3d 106\26 _nc_oc\3d AQncim4NrdLW6r6UIPX4A9LdAQ6xIqrb1DwDij48bD30RyFJTFMGJSFKQSARSNJXAx8\26 _nc_ht\3d scontent-arn2-2.xx\26 oh\3d b1e4add1ac4559364f55032b13194bf0\26 oe\3d 5E3A0652');"></a><div class="_53d _53q"><div data-fbid="107327912701357" id="u_0_34"><div class="_5gl-" id="u_0_2t"><a href="#" role="button" class="_5glz _53o _53b">Нравится</a><a href="#" role="button" class="_5glz _53p _53b">Не нравится</a><span class="_6ib"> · </span><a class="_5glz _s4z" role="button" href="#" id="u_0_35">Комментировать</a><a class="_5gly _5glz" role="button" href="#" id="u_0_36"></a></div></div><img src="/images/photos/profile/gradient.png" class="_53l" alt=""></div></div></div></div>

        '//div[@id="fbTimelinePhotosContent"]/div[@id="fbTimelinePhotosFlexgrid"]'                
        """
        item_photo_list = list()
        self.webdriver.get(avatar_link)
        # получим ссылку на альбом аватаров и перейдем
        path = '//div[@class="fbPhotoMediaTitle"]/span[@class="fbPhotoMediaTitleNoFullScreen"]/a'
        album_url = self.webdriver.find_element_by_xpath(path).get_attribute('href')
        self.webdriver.get(album_url)

        # обработаем альбом заходя на каждую фото и собирая ссылку
        path = '//div[@id="fbTimelinePhotosContent"]/div[@id="fbTimelinePhotosFlexgrid"]/div/a'
        tmp_list  = [itm.get_attribute('href') for itm in self.webdriver.find_elements_by_xpath(path)]

        for img_url in tmp_list:
            self.webdriver.get(img_url)
            time.sleep(1)
            img_src = self.webdriver.find_element_by_xpath('//img[@class="spotlight"]').get_attribute('src')
            item_photo_list.append(img_src)
            
        
        """
        Секция обработки список друзей
        """
        # переходим на список друзей
        self.webdriver.get(friends_link)

        # прокручиваем список
        body = self.webdriver.find_element_by_tag_name('body')
        _friend_list_item = '//div[@data-testid="friend_list_item"]/a'
        friends_len = len(self.webdriver.find_elements_by_xpath(
            _friend_list_item ))
        while True:
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
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
        item_friends_href_list = list(map(lambda x: x.get_attribute('href'), friends_list))
        #print(f'Друзей у {full_name}= ', len(href_list))

        # сохраняем в базу
        yield FacebookItem(
                            name = item_full_name, 
                            birthdate = item_birthdate,
                            photos = item_photo_list,
                            friends_count = friends_len,
                            friends = item_friends_href_list
                            )

        # и далее запускаем паучка рекурсивно по списку!
        for url in item_friends_href_list:
            yield response.follow(url, callback=self.parse_page)
