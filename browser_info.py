import requests
import fake_useragent
from bs4 import BeautifulSoup as bs

user = fake_useragent.UserAgent().random
header = {'user-agent': user}

url = 'https://browser-info.ru/'
responce = requests.get(url, headers=header).text
soup = bs(responce, 'lxml')
block = soup.find('div', id ='tool_padding')

#JS
block_js = block.find('div', id="javascript_check")
status_js = block_js.find_all('span')[1].text
res_js = f'javascript: {status_js}'

#Flash
block_flash = block.find('div', id="flash_version")
status_js = block_flash.find_all('span')[1].text
res_flash = f'flash: {status_js}'

#User-agent
block_user = block.find('div', id="user_agent").text
res_user = f'flash: {block_user}'

print(res_js)
print(res_flash)
print(res_user)






