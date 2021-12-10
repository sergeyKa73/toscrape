import requests
from bs4 import BeautifulSoup as bs

get_html = requests.get('http://books.toscrape.com/')
if get_html.status_code == 200:
    html = get_html.content

    soup =bs(html, 'html.parser')
    sections = soup.select('section')
    section = sections[0]
    books_block = section.select_one('ol[class=row]')
    books = books_block.select('li')

    books_data = []
    for book in books:
        image = 'http://books.toscrape.com/' + book.find('div', attrs={'class': 'image_container'}).find('img')['src']
        title = book.find('h3').find('a')['title']
        price = book.find('p', attrs={'class': 'price_color'}).text

        book_dict = {
            'image': image,
            'title': title,
            'price': price
        }

        books_data.append(book_dict)

    print(books_data[3])
