

import requests
from bs4 import BeautifulSoup

url = "https://www.igoroculista.com/"
url = "http://silvialiberati.it"
url = "http://www.insufflazionipolitzer.com"
url = "http://silvialiberati.it/content/Home_Page.html"
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}


r = requests.get(url, headers, allow_redirects= True)
# r
c = r.content
soup = BeautifulSoup(r.content, 'lxml')

type(soup.find_all('meta')[0])
dir(soup.find_all('meta')[0])

t = soup.find_all('meta')[0]
dir(t)
t.get('url')

soup.find_all(url=True)

dir(soup.meta)

soup.meta["content"]


igor_redir = '0; url=https://www.igoroculista.com/site/'
silvia_liberat = '0;url= content/Home_Page.html'


def handle_redirection(url: str , s: str)-> str:
    try:
        redir = s[s.find('url='):].replace('url=','').replace('=','').strip()
        if redir.startswith('http') == True:
            return redir
        else:
            return f"{url}/{redir}".replace('//','/')
    except Exception as e:
        print(e)
        pass 

handle_redirection("http://silvialiberati.it", '0;url= content/Home_Page.html')
handle_redirection("https://www.igoroculista.com/", '0; url=https://www.igoroculista.com/site/')
