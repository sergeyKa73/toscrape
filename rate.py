import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
import csv

URL = 'https://myfin.by/bank/kursy_valjut_nbrb'
user = fake_useragent.UserAgent().random
header = {'user-agent': user}
CSV = 'exchange.csv'


def get_html(url):
    r = requests.get(url, headers=header)
    if r.ok:  # 200  ## 403 404
        return r.text
    print(r.status_code)


def write_csv(data, path):
    with open(path, 'a') as file:
        header = ['name', 'cod', 'rate', 'rate_next', 'units', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()

        writer.writerow(data)


def get_page_content(html):
    soup = bs(html, 'lxml')
    table = soup.find('tbody').find_all('tr', class_='row body odd')
    for td in table:
        line = td.getText(separator=';')
        name = line.split(';')[0]
        link = 'https://myfin.by/' + td.find('a')['href']
        rate = line.split(';')[1]
        rate_next = line.split(';')[2]
        cod = line.split(';')[-2]
        units = line.split(';')[-1]

        data = {
            'name': name,
            'link': link,
            'rate': rate,
            'rate_next': rate_next,
            'cod': cod,
            'units': units
        }

        write_csv(data, CSV)


def main():
    get_page_content(get_html(URL))


if __name__ == '__main__':
    main()
