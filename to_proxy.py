import requests
import multiprocessing

#функция обработчик
def handler(proxy):
    url = 'http://icanhazip.com/'

    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }

    try:
        responce = requests.get(url, proxies=proxies, timeout=2).text
        print(f'IP: {responce}')
    except:
        print('Прокси не валидный!')


with open('proxy') as file:
    proxy_base = ''.join(file.read()).strip().split('\n')

with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
    process.map(handler, proxy_base)
