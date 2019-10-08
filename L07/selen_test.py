from selenium import webdriver
from selenium.webdriver.common.keys import Keys

user_1 = 'https://www.facebook.com/denise.dente.5'
user_2 = 'https://www.facebook.com/profile.php?id=100009326603148'
user_3 = 'https://www.facebook.com/salvador.bathory'

fox_driver = webdriver.Chrome()
fox_driver.get('https://facebook.com')

mail = fox_driver.find_element_by_xpath('//input[@class="inputtext login_form_input_box"][@type ="email"][@name ="email"]')
if mail is None:
    mail = fox_driver.find_element_by_xpath('//input[@type ="text"][@name ="email"]')

mail.send_keys('pan.heap@gmail.com')
pswd = fox_driver.find_element_by_xpath('//input[@class="inputtext login_form_input_box"][@type ="password"][@name ="pass"]')
if pswd is None:
    pswd = fox_driver.find_element_by_xpath('//input[@type ="password"][@name ="pass"]')
pswd.send_keys('quy-vy-cy-bo')

login_btn = fox_driver.find_element_by_xpath('//label[@class="login_form_login_button uiButton uiButtonConfirm"]/input[@type ="submit"][@value ="Log In"]')
login_btn.click()


# <button value="1" class="_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy" name="login" type="submit">Log In</button>
fox_driver.get(user_1)
pass