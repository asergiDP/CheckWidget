

import requests
from bs4 import BeautifulSoup

url = "https://www.igoroculista.com/"
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}


r = requests.get(url, headers)
r
c = r.content
soup = BeautifulSoup(r.content, 'html5lib')

type(soup.find_all('meta')[0])
dir(soup.find_all('meta')[0])

t = soup.find_all('meta')[0]
dir(t)
t.get('url')