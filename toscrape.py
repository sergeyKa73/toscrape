import requests
from bs4 import BeautifulSoup as bs

HOST = 'http://books.toscrape.com/'
URL = 'http://books.toscrape.com/catalogue/page-1.html'
HEADERS = {
    'accept': 'image/avif,image/webp,*/*',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

#сбор данных со страницы
def get_books(html):
    soup = bs(html, 'html.parser')
    block = soup.find('ol', attrs={'class': 'row'})
    books = block.select('li')

    books_data = []
    for book in books:
        books_data.append(
            {
                'image': book.find('div', attrs={'class': 'image_container'}).find('img')['src'],
                'title': book.find('h3').find('a')['title'],
                'price': book.find('p', attrs={'class': 'price_color'}).text
            }
        )

    return books_data



def get_next_page(content):
    soup = bs(content, 'html.parser')
    block = soup.find('ul', attrs={'class': 'pager'}).find('li', attrs={'class': 'current'}).text
    len_page = []
    for i in block:
        if i.isdigit():
            len_page.append(int(i))
    return max(len_page)*10

    # поиск ссылки на  следующую страницу
    # try:
    #     next_page = 'http://books.toscrape.com/' + soup.find('li', attrs={'class': 'next'}).find('a')['href']
    #     print(next_page)
    #     return next_page
    # except:
    #     pass

html = get_html(URL).content


final_data = []
page_number = 1
url = 'http://books.toscrape.com/catalogue/page-1.html'
get_html = requests.get(url)
PAGENATION = get_next_page(html)

if get_html.status_code == 200:
    for  page in range(1, PAGENATION):
        books = get_books(get_html.content)
        print(f'получено{len(books)} с {page} страницы')
        final_data += books
else:
    pass



print(f'Данные спарсились {PAGENATION} страниц , {len(final_data)} книг')

