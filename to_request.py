import requests
from bs4 import BeautifulSoup as bs
import csv


CSV = 'cards.csv'
HOST = 'https://myfin.by'
URL = 'https://myfin.by/raschetnye-karty'
HEADERS = {
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='card-v2__top')
    cards =[]

    for item in items:
        cards.append(
            {
                'title': item.find('div', class_= 'card-v2__title').get_text(strip=True),
                'link_product': HOST + item.find('div', class_='card-v2__title').find('a').get('href'),
                'brand': item.find('div', class_='card-v2__info').find('span').get_text(),
                'card_image': item.find('div', class_= 'card-v2__img-card').find('img').get('data-url-img'),
            }
        )

    return cards

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название продукта', 'Ссылка на продукт', 'Банк', 'Изображение карты'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['brand'], item['card_image']])


def parser():
    PAGENATION = input('Укажите кол-во для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html= get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Парсинг страницы {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        pass
    else:
        print('Error')

parser()

