import requests
from bs4 import BeautifulSoup as bs

#сбор данных со страницы
def get_books(content):
    soup =bs(content, 'html.parser')
    block = soup.find('ol', attrs={'class': 'row'})
    books = block.select('li')

    books_data = []
    for book in books:
        image = book.find('div', attrs={'class': 'image_container'}).find('img')['src']
        title = book.find('h3').find('a')['title']
        price = book.find('p', attrs={'class': 'price_color'}).text

        book_dict = {
            'image': image,
            'title': title,
            'price': price
        }
        books_data.append(book_dict)
    return books_data


#поиск ссылки на  следующую страницу
def get_next_page(content):
    soup = bs(content, 'html.parser')
    try:
        next_page = 'http://books.toscrape.com/' + soup.find('li', attrs={'class': 'next'}).find('a')['href']
        return next_page
    except:
        pass

final_data = []
page_number = 1
url = 'http://books.toscrape.com/catalogue/page-1.html'
get_html = requests.get(url)

if get_html.status_code == 200:
    while True:
        books = get_books(get_html.content)
        print(f'получено{len(books)} с {page_number} страницы')
        final_data += books

        next_page = get_next_page(get_html.content)
        if next_page:
            page_number += 1
            get_html = requests.get(next_page)
            if get_html.status_code == 200:
                print(f'начинаеи парсить {page_number}')
            else:
                pass

print(f'Данные спарсились {page_number} страниц , {len(final_data)} книг')


