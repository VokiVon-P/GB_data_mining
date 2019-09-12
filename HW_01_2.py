
import requests
import json

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 YaBrowser/19.9.0.1343 Yowser/2.5 Safari/537.36'
            , 'Authorization':'Basic cG9zdG1hbjpwYXNzd29yZA=='
}

URL_service = 'https://postman-echo.com'
URL_coomand = '/basic-auth'

req = requests.get(f'{URL_service}{URL_coomand}',headers=headers)
print('Заголовки: \n',  req.headers)
print('Ответ: \n',  req.text)

 