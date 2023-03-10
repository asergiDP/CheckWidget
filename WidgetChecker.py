

import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup, builder, MarkupResemblesLocatorWarning
from dataclasses import dataclass, asdict
from widget_logger import WidgetLogger
from LocSize import get_widget_size_and_loc
from NetworkRequests import check_network_requests

from enum import Enum
import warnings
# warnings.filterwarnings("error")


from MappingMD import MappingIndividual, MappingFacility, AllowsBooking, ProfileType


# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

checks = []


UNIQUE_LINKS = set()
REMOVED_LINKS = set()
# REMOVED_LINKS = []

# class AllowsBooking(Enum):
#     OK = 'OK'
#     MAPPING_REVIEW = 'MAPPING REVIEW'
#     INVALID_URL = 'INVALID_URL'
#     INDIVIDUAL_PROFILE = 'INDIVIDUAL PROFILE'

class WidgetStatus(Enum):
    WIDGET_FOUND = 'Widget FOUND'
    WIDGET_NOT_FOUND = 'Widget NOT FOUND'
    WIDGET_INSTALLED = 'Widget INSTALLED'
    CONNECTION_ERROR = 'Connection refused - 403 ERROR'
    INDIVIDUAL_PROFILE = 'Widget FOUND - INDIVIDUAL PROFILE'


@dataclass
class CheckWidget:
    url: str = None
    position: str = None 
    page_found : str = None
    outcome: WidgetStatus = None
    allows_booking: str = None


'platform.docplanner.com/js/widget.js'


class Website:

    def __init__(self, url: str, check_network:bool = False) -> None:
        if url.endswith(".html") == False:
            warnings.filterwarnings("error")
        global checks
        checks = []
        self.checks = []

        self.url = url
        if self.url.strip().startswith('http') == False:
            self.url = f"http://{url}"
            print(self.url)
        try:
            self.location = None
            # self.logger = WidgetLogger(url=self.url)
            self.response = requests.get(self.url, headers=headers)
            print(self.response)
            self.content = self.response.content
            self.soup = BeautifulSoup(self.content, 'html5lib')
            try:
                if len(self.soup.meta['content']) >0:
                    self.soup = self.handle_redirection()
                    print(f"Redirection to -> {self.url}")
            except KeyError:
                pass
            self.links = self.soup.find_all(href = True)

            # self.all_links = [i for i in self.links if urlparse(self.url).netloc.replace('www.','') in i['href'] and i['href'] != self.url]
            self.all_links = [self.clean_links(i) for i in self.links]
            self.all_links = [i for i in self.links if urlparse(self.url).netloc.replace('www.','') in i['href'] and i['href'] != self.url]


            self.all_widget = [self.soup.find_all(tag.name, {'href': tag['href']}) for tag in self.all_links]
            self.md = [i for i in self.links if 'miodottore.it' in i['href']]
            self.md = [*self.md, *[i for i in self.links if 'docplanner.it' in i['href']]]
            self.widget = [self.soup.find_all(tag.name, {'href': tag['href']}) for tag in self.md]
            self.outcome = CheckWidget(url = self.url, outcome= WidgetStatus.WIDGET_NOT_FOUND.value)
            self.all_widget = [i for i in self.all_widget if i[0]['href'].startswith('http')]
            self.all_widget = [i for i in self.all_widget if urlparse(i[0]['href']).netloc.replace('www.','') == urlparse(self.url).netloc.replace('www.','')]
            self.all_widget = [i for i in self.all_widget if i[0]['href'].endswith('.php') == False]
            self.all_widget = [i for i in self.all_widget if i[0]['href'].endswith('.xml') == False]
            self.all_widget = [i for i in self.all_widget if i[0]['href'].endswith('.jpeg') == False]
            self.all_widget = [i for i in self.all_widget if i[0]['href'].endswith('.jpg') == False]
            self.all_widget = [i for i in self.all_widget if i[0]['href'].endswith('.png') == False]
            self.all_widget = [i for i in self.all_widget if i[0]['href'].endswith('.pdf') == False]
            self.all_widget = [i for i in self.all_widget if i[0]['href'].endswith('.ttf') == False]
            self.all_widget = [i for i in self.all_widget if i[0]['href'].endswith('.woff') == False]
            self.all_widget = [i for i in self.all_widget if i[0]['href'].endswith('.gif') == False]



            self.all_widget = [i for i in self.all_widget if '.css' not in i[0]['href']]
            self.all_widget = [i for i in self.all_widget if 'wp-json' not in i[0]['href']]
            self.all_widget = [i for i in self.all_widget if 'wp-content' not in i[0]['href']]
            self.all_widget = [i for i in self.all_widget if '?share=' not in i[0]['href']]
            self.all_widget = [i for i in self.all_widget if '.ttf' not in i[0]['href']]
            self.all_widget = [i for i in self.all_widget if 'mailto:' not in i[0]['href']]
            self.all_widget = [i for i in self.all_widget if 'tel:' not in i[0]['href']]






            # warnings.filterwarnings("error")





            if check_network == True and len(self.md) <= 0 and 'platform.docplanner.com/js/widget.js' not in str(self.content) and 'docplanner-platform.com/js/widget.js' not in str(self.content):
                # warnings.resetwarnings()
                if check_network_requests(self.url) == True:
                    protocol = self.url.split('://')[0]
                    self.outcome = CheckWidget(url = f"{protocol}://{urlparse(self.url).netloc}", outcome = WidgetStatus.WIDGET_INSTALLED.value, position=None, page_found= 'HOMEPAGE')
                    checks = []

            # print(self.all_widget)

            
            if len(self.md)>0 :
                print(WidgetStatus.WIDGET_FOUND.value)
                print(f"MD is: {self.md}")
                self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.WIDGET_FOUND.value, position=self.widget_position(), page_found= 'HOMEPAGE')
                self.check_MD()
                print(f"OUTCOME is: {self.outcome}")
                self.location = get_widget_size_and_loc(self.url, self.widget)
                checks = []

            elif len(self.md)<=0 and ('platform.docplanner.com/js/widget.js' in str(self.content) or 'docplanner-platform.com/js/widget.js'in str(self.content)) and self.outcome.outcome != WidgetStatus.WIDGET_FOUND.value:

                print('JAVASCRIPT')
                self.outcome.url = self.url
                self.outcome.outcome =  WidgetStatus.WIDGET_INSTALLED.value
                self.outcome.page_found = 'HOMEPAGE'
                self.outcome.position = str(self.content).find('platform.docplanner.com/js/widget.js')/len(str(self.content))
                s = str(self.content)[str(self.content).find('https://www.miodottore.it/'):]
                url_md = s[:s.find('&')]
                # if url_md == '':
                #     s = str(self.content)[str(self.content).find('https://www.docplanner.it/'):]
                print(f"URL MD: {url_md}")
                self.check_MD(url_md)
                self.location = get_widget_size_and_loc(self.url, self.widget)
                checks = []


            elif len(self.md)<=0 and self.outcome.outcome != WidgetStatus.WIDGET_FOUND.value and self.outcome.outcome != WidgetStatus.WIDGET_INSTALLED.value:
                print('Checking pages')
                REMOVED_LINKS.add(self.url)

                # if len(checks)>0:
                # self.outcome.page_found = checks[0].url


                if len(self.all_widget) == 0:
                    return
                
                # if original:
                # page = None
                # REMOVED_LINKS = []
                for ww in self.all_widget:
                    # print(ww[0]['href'])
                    # print(ww[0]['href'] not in list(REMOVED_LINKS))
                    
                    # print(ww[0]['href'] not in REMOVED_LINKS)

                    if ww[0]['href'] not in list(REMOVED_LINKS):
                    # if w[0]['href'] not in REMOVED_LINKS:
                        # print(ww[0]['href'])
                        # REMOVED_LINKS.append(w[0]['href'])
                        # REMOVED_LINKS.add(w[0]['href'])
                        # print("removing links")
                        # print(REMOVED_LINKS)
                        page = self.check_one_link(ww[0]['href'])
                        # print(type(page))
                        # print(type(page) is Website)
                        # self.all_widget.remove(w[0]['href'])



                        # UNIQUE_LINKS.add(w[0]['href'])
                    # print(UNIQUE_LINKS)

                # page = self.check_all_links(list(UNIQUE_LINKS))

                # page = self.check_all_links(self.all_widget)

                        if type(page) is Website:
                        # if type(page) is Website and page.outcome.outcome == WidgetStatus.INDIVIDUAL_PROFILE.value or page.outcome.outcome == WidgetStatus.WIDGET_FOUND.value or page.outcome.outcome == WidgetStatus.WIDGET_INSTALLED.value:
                        
                            # REMOVED_LINKS.add(w[0]['href'])
                            print('EXITING')
                            # print(f"LINKS REMOVED: {REMOVED_LINKS}")
                            [REMOVED_LINKS.add(i[0]['href']) for i in self.all_widget if i[0]['href'] != page.outcome.url]
                            print(f"MAIN {page.outcome}") 
                            # checks = [page]
                            # checks.append(page)
                            # print([i.url for i in checks])
                            # self.location = page.location 
                            self.outcome.page_found = checks[0].url




                            # self.outcome.page_found = page.outcome.url
                            try:
                                self.outcome.page_found = checks[0].url
                            except:
                                pass
                            # check[0]


                            # self.all_widget.remove(w[0]['href'])


                            # self.outcome.page_found = w[0]['href']

                            # self.outcome.url = url
                            # self.outcome.outcome = page.outcome.outcome
                            # self.outcome.allows_booking = page.outcome.allows_booking
                            # self.outcome.position = page.outcome.position
                            # self.location = get_widget_size_and_loc(self.url, self.widget)
                            break
                        else:
                            # REMOVED_LINKS.add(w[0]['href'])
                            # if ww in self.all_widget:
                            self.all_widget.remove(ww)
                            # print(f"link to check:{len(self.all_widget)}")
                        #     self.outcome.url = self.url
                        #     self.outcome.outcome = WidgetStatus.WIDGET_NOT_FOUND.value
                        #     return 

            # elif all(i==None for i in asdict(CheckWidget).values()):
            #     if check_network_requests == True:
            #         self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.WIDGET_INSTALLED.value, position=None, page_found= 'HOMEPAGE')
            #     else:
            #         pass
            
        except requests.exceptions.ConnectionError as e:
            # self.logger.error("Exception occurred", exc_info=True)
            print(e)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except requests.exceptions.ContentDecodingError as e1:
            # self.logger.error("Exception occurred", exc_info = True)
            print(e1)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except requests.exceptions.InvalidSchema as e2:
            # self.logger.error("Exception occurred", exc_info = True)
            print(e2)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except requests.exceptions.ChunkedEncodingError as e3:
            # self.logger.error("Exception occurred", exc_info = True)
            print(e3)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except requests.exceptions.InvalidURL as e4:
            # self.logger.error("Exception occurred", exc_info = True)
            print(e4)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except RecursionError as e5:
            # self.logger.error("Exception occurred", exc_info = True)
            print(e5)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except builder.XMLParsedAsHTMLWarning as e6:
            # self.logger.error("XML file", exc_info = True)
            print(e6)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except MarkupResemblesLocatorWarning as e7:
            # self.logger.error("CSS file", exc_info = True)
            print(e7)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)




    def widget_position(self):
        position = []
        try:
            for widg in self.widget:
                position.append(str(self.soup.prettify()).replace('&amp;','&').find(widg[0]['href']))
                self.outcome.position = min(position)/ len(str(self.soup.prettify()))
            return min(position)/ len(str(self.soup.prettify()))
        except Exception as e:
            # self.logger.error("Exception occurred", exc_info=True)
            print(e)
            pass


    # @classmethod
    # def check_all_links(cls, links):
    #     for link in links:
    #         l = link[0]['href']
    #         print(f"link: {l}")
    #         w = Website(l)
    #         # print(w.outcome)
    #         # print(w.outcome.outcome == WidgetStatus.WIDGET_FOUND.value or w.outcome.outcome == WidgetStatus.INDIVIDUAL_PROFILE.value or w.outcome.outcome == WidgetStatus.WIDGET_INSTALLED.value)
    #         if w.outcome.outcome == WidgetStatus.WIDGET_FOUND.value or w.outcome.outcome == WidgetStatus.INDIVIDUAL_PROFILE.value or w.outcome.outcome == WidgetStatus.WIDGET_INSTALLED.value:

    #             print('BREAKING')
    #             print(f'OUTCOME: {w.outcome.outcome}')
    #             print(f'URL: {w.outcome.url}')
    #             return cls(url = w.outcome.url)


    # @classmethod
    def check_all_links(cls, links):
        for link in links:
            # l = link[0]['href']
            # UNIQUE_LINKS.add(l)
            print(f"link: {link}")
            REMOVED_LINKS.add(link)
            w = Website(link)
            # UNIQUE_LINKS.remove(link)

            # print(w.outcome)
            # print(w.outcome.outcome == WidgetStatus.WIDGET_FOUND.value or w.outcome.outcome == WidgetStatus.INDIVIDUAL_PROFILE.value or w.outcome.outcome == WidgetStatus.WIDGET_INSTALLED.value)
            if w.outcome.outcome == WidgetStatus.WIDGET_FOUND.value or w.outcome.outcome == WidgetStatus.INDIVIDUAL_PROFILE.value or w.outcome.outcome == WidgetStatus.WIDGET_INSTALLED.value:

                print('BREAKING')
                print(f'OUTCOME: {w.outcome.outcome}')
                print(f'URL: {w.outcome.url}')
                w.outcome.page_found = link
                REMOVED_LINKS.remove(link)
                return w
                # return cls(url = w.outcome.url)
            # else:
            #     print(f"Link removed: {link}")
            #     UNIQUE_LINKS.remove(link)


    # @classmethod
    def check_one_link(self, link):
        print(f"link: {link}")
        w = Website(link, True)
        if w.outcome.outcome == WidgetStatus.WIDGET_FOUND.value or w.outcome.outcome == WidgetStatus.INDIVIDUAL_PROFILE.value or w.outcome.outcome == WidgetStatus.WIDGET_INSTALLED.value:
            # REMOVED_LINKS.add(w.url)
            page = w
            # checks = []
            # [REMOVED_LINKS.add(i[0]['href']) for i in w.all_widget if i[0]['href'] != w.url]
            print('BREAKING')
            print(f'OUTCOME: {w.outcome.outcome}')
            print(f'URL: {w.outcome.url}')
            self.checks.append(w)
            checks.append(w)
            self.location = page.location 
            # self.outcome.page_found = page.outcome.url
            # checks = []
            # self.outcome.page_found = self.checks[0].url
            # checks = []

            # self.outcome.url = page.url
            protocol = page.url.split('://')[0]
            self.outcome.url = f"{protocol}://{urlparse(page.url).netloc}"
            self.outcome.outcome = page.outcome.outcome
            self.outcome.allows_booking = page.outcome.allows_booking
            self.outcome.position = page.outcome.position
            self.location = get_widget_size_and_loc(self.url, self.widget)
            w.outcome.page_found = link
            print(w.outcome)
            return w
        else:
            REMOVED_LINKS.add(link)
            return None

        # else:
        #     # if link in self.all_widget:
        #     self.all_widget.remove(link)
        #     print(f"link to check:{len(self.all_widget)}")
        # else:
        #     # REMOVED_LINKS.add(w[0]['href'])
        #     REMOVED_LINKS.add(link)
        #     # self.all_widget.remove(w[0]['href'])


        #     # self.all_widget.remove(link)
        #     w = None
        #     return w

            # return cls(url = w.outcome.url)


    def check_MD(self, url_md = None):
        try:

            if len(self.md)>0 and 'strutture' in self.md[0]['href']:
                self.outcome.allows_booking = MappingFacility(url = self.md[0]['href']).mapping.value

            if len(self.md)>0 and 'strutture' not in self.md[0]['href']:
                self.outcome.outcome = WidgetStatus.INDIVIDUAL_PROFILE.value
                self.outcome.allows_booking = MappingIndividual(url = self.md[0]['href']).mapping.value


            if url_md is not None and 'strutture' in url_md:
                self.outcome.allows_booking = MappingFacility(url = url_md).mapping.value

            if url_md is not None and 'strutture' not in url_md:
                self.outcome.outcome = WidgetStatus.INDIVIDUAL_PROFILE.value
                self.outcome.allows_booking = MappingIndividual(url = url_md).mapping.value

        except Exception as e:
                # self.logger.error("Exception occurred", exc_info=True)            
                pass
        

    def clean_links(self,link)->str:
        if urlparse(link['href']).netloc.replace('www.','') != '':
            return link
        else: 
            l = f"{urlparse(self.url).netloc.replace('www.','')}/{link['href']}".replace('///','/').replace('//','/')
            link['href'] = f"http://{l}"
            return link
    

    def handle_redirection(self)-> str:
        try:
            meta = self.soup.meta['content']
            redir = meta[meta.find('url='):].replace('ulr=','').replace('=','').replace('url','').strip()
            if urlparse(redir).netloc.replace('www.','') == urlparse(self.url).netloc.replace('www.',''):
                # return Website(redir)
                r = requests.get(redir, headers)
                if redir.endswith('.html'):
                    warnings.resetwarnings()
                return BeautifulSoup(r.content, 'html5lib')


            else:
                # return Website(f"{self.url}/{redir}".replace('//','/'))
                redir = f"{self.url}/{redir}".replace("https://","").replace("http://","").replace('//','/')
                r = requests.get(f"http://{redir}", headers)
                print(f"http://{redir}")
                if redir.endswith('.html'):
                    warnings.resetwarnings()
                return BeautifulSoup(r.content, 'html5lib')

        except Exception as e:
            print(f"Exception during redirection: {e}")
            pass

# w = Website("https://nuoviequilibri.com/")
# w = Website("https://www.baldinottipsicologo.it")
# w = Website("www.baldinottipsicologo.it")
# w = Website("https://www.spalla.it")
# w = Website("https://www.federicobaranzini.it")
# w = Website("http://www.nutrirsi-irenegranucci.it/")
# w = Website("https://www.an-fisio-osteo-spine.it/")

# w = Website("https://www.cesareiacopino.it/")
# w = Website("https://www.nutrizionistavomero.com/", True)

# w = Website("https://www.cesareiacopino.it/contatti/", True)
# w = Website("https://www.cesareiacopino.it/", True)

# w = Website("https://www.psicoterapeutagiareimonica.it/",True)
# w = Website("https://www.dottlucabello.com/", True)
# w = Website("https://www.nutrizionistavomero.com/", True)
# w = Website("https://gennaroiapicca.it", True)

# w = Website(url = "https://psicoterapeuta-antinori.it", check_network= True)

# w = Website(url = "https://www.valerioavinoosteopata.it/", check_network= True)

# w = Website(url= "https://www.baldinottipsicologo.it", check_network= True)
# w = Website(url= "http://www.psicologasilviabaresi.it/", check_network= True)
# w = Website(url = "https://www.igoroculista.com/site", check_network= True)
# w = Website(url = "http://www.fernandomaxia.it/", check_network= True)
# w = Website(url = "http://www.ambulatoriomedicodellafilanda.it/", check_network= True)


######## REDIRECTION
# w = Website(url = "https://www.igoroculista.com/", check_network= True)
# w = Website(url = "http://silvialiberati.it", check_network= True)
# w = Website(url = "http://www.insufflazionipolitzer.com", check_network=True)




# print(w.outcome)
# urlparse(w.outcome.url).netloc


# url = "https://www.baldinottipsicologo.it"
# url = "www.baldinottipsicologo.it"

# if url.strip().startswith('http') == False:
#     url = f"https://{url}"

# w.outcome


# w.all_links = [i for i in w.links if w.url in i['href'] and i['href'] != w.url]

# # w = Website("http://www.psicoterapeuta-pescara.it/")

# [i for i in w.links if w.url in i['href']]
# [i['href'] for i in w.links]

# from urllib.parse import urlparse

# o = urlparse("https://nuoviequilibri.com/")





# 'https://www.nuoviequilibri.com/covid-19-oltre-il-virus-la-lontanza-da-casa/' in list(REMOVED_LINKS)  # when does it get removed
# 'https://www.nuoviequilibri.com/feed/' in list(REMOVED_LINKS)




# not_rem = [i[0]['href'] for i in w.all_widget if i[0]['href'] not in list(REMOVED_LINKS)]
# len(not_rem)
# REMOVED_LINKS
# len(list(REMOVED_LINKS))

# [i.url for i in checks]

# w.soup.meta['content']