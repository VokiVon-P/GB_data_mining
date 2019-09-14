import requests
import json
from auth_voki import GIT_VOKI_PSWD


def write_json(data, file_name):
# записывает данные в файл формата json 
# data - словарь 
    _fname = file_name
    try:
        with open(_fname, 'w') as f_n:
            json.dump(data, f_n, indent=4) #sort_keys=True, 

    except Exception as err:
            print(f"Ошибка записи файла { _fname}\n", err)                    

### Задание 1

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 YaBrowser/19.9.0.1343 Yowser/2.5 Safari/537.36'}
URL_service = 'https://api.github.com'
URL_coomand = '/users/VokiVon-P/repos'
file_name = 'out/repositories.json'



resp = requests.get(f'{URL_service}{URL_coomand}', headers=headers)
data = json.loads(resp.text)
write_json(data, file_name)
print(f"JSON файл {file_name} успешно записан")     

### Задание 2
# будем использовать для тестирования тот же GitHub

URL_coomand = '/user'
file_name = 'out/auth_answer.json'

url_login = 'vokivon.p@gmail.com'
url_pswd = GIT_VOKI_PSWD
auth_info = (url_login, url_pswd)


resp = requests.get(f'{URL_service}{URL_coomand}', headers=headers, auth = auth_info)
data = json.loads(resp.text)
write_json(data, file_name)
print(f"JSON файл {file_name} c параметрами пользователя успешно записан")  

