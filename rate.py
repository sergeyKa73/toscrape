import requests
from bs4 import BeautifulSoup as bs

URL = 'https://myfin.by/bank/kursy_valjut_nbrb'
HEADERS = {
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

source = requests.get(URL, headers=HEADERS)
main_text  = source.text
soup = bs(main_text)

table = soup.find('table', attrs={'class': 'default-table'}).getText(separator=';')

print(table)

