import requests
from bs4 import BeautifulSoup as bs

page_number =1
image_number = 0
url = 'https://zastavok.net'

n = int(input('Укажите кол-во для парсинга: '))
for page in range(n):
    responce = requests.get(f'{url}/{page_number}').text
    soup = bs(responce, 'lxml')
    block = soup.find('div', class_='block-photo')
    all_image = block.find_all('div', class_='short_full')

    for image in all_image:
        image_link = image.find('a').get('href')
        download_page = requests.get(f'{url}{image_link}').text  # получаем ссылку на страницу изображения

        download_soup = bs(download_page, 'lxml')
        download_block = download_soup.find('div', class_='image_data').find('div', class_='block_down')
        result_link = download_block.find('a').get('href')

        image_bytes = requests.get(f'{url}{result_link}').content

        # Сохранение изображений
        with open(f'images/{image_number}.jpg', 'wb') as file:
            file.write(image_bytes)

        image_number += 1
        print(f'Изображение {image_number}.jpg успешно скачано!')

    page_number +=1