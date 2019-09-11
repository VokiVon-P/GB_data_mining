import requests
import json

""" import requests
headers = {'User-agent': 'Mozilla/5.0',
                    'Authorization':'Basic cG9zdG1hbjpwYXNzd29yZA=='}
req = requests.get('https://postman-echo.com/basic-auth',headers=headers)
print('Заголовки: \n',  req.headers)
print('Ответ: \n',  req.text)

appid = 'b6907d289e10d714a6e88b30761fae22'
service = 'https://samples.openweathermap.org/data/2.5/weather'
req = requests.get(f'{service}?q=London,uk&appid={appid}')
data = json.loads(req.text)
print(f"В городе {data['name']} {data['main']['temp']} градусов по Кельвину")

 """