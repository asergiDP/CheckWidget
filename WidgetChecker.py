

import re
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from widget_logger import WidgetLogger
from LocSize import get_widget_size_and_loc
from enum import Enum

from MappingMD import MappingIndividual, MappingFacility, AllowsBooking, ProfileType


# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}






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

    def __init__(self, url: str) -> None:
        self.url = url
        try:
            self.location = None
            self.logger = WidgetLogger(url=self.url)
            self.response = requests.get(self.url, headers=headers)
            print(self.response)
            self.content = self.response.content
            self.soup = BeautifulSoup(self.content, 'html5lib')
            self.links = self.soup.find_all(href = True)
            self.all_links = [i for i in self.links if self.url in i['href'] and i['href'] != self.url]
            self.all_widget = [self.soup.find_all(tag.name, {'href': tag['href']}) for tag in self.all_links]
            self.md = [i for i in self.links if 'www.miodottore.it' in i['href']]
            self.widget = [self.soup.find_all(tag.name, {'href': tag['href']}) for tag in self.md]
            self.outcome = CheckWidget()
            
            if len(self.md)>0 :
                print(WidgetStatus.WIDGET_FOUND.value)
                print(f"MD is: {self.md}")
                self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.WIDGET_FOUND.value, position=self.widget_position(), page_found= 'HOMEPAGE')
                self.check_MD()
                print(f"OUTCOME is: {self.outcome}")
                self.location = get_widget_size_and_loc(self.url, self.widget)

            elif len(self.md)<=0 and 'platform.docplanner.com/js/widget.js' in str(self.content) and self.outcome.outcome != WidgetStatus.WIDGET_FOUND.value:
                print('JAVASCRIPT')
                self.outcome.url = self.url
                self.outcome.outcome =  WidgetStatus.WIDGET_INSTALLED.value
                self.outcome.page_found = 'HOMEPAGE'
                self.outcome.position = str(self.content).find('platform.docplanner.com/js/widget.js')/len(str(self.content))
                s = str(self.content)[str(self.content).find('https://www.miodottore.it/'):]
                url_md = s[:s.find('&')]
                print(f"URL MD: {url_md}")
                self.check_MD(url_md)
                self.location = get_widget_size_and_loc(self.url, self.widget)


            elif len(self.md)<=0 and self.outcome.outcome != WidgetStatus.WIDGET_FOUND.value:
                print('Checking pages')
                page = self.check_all_links(self.all_widget)

                if type(page) is Website:
                    print(f"MAIN {page.outcome}") 
                    self.location = page.location 
                    self.outcome.page_found = page.outcome.page_found
                    self.outcome.url = url
                    self.outcome.outcome = page.outcome.outcome
                    self.outcome.allows_booking = page.outcome.allows_booking
                    self.outcome.position = page.outcome.position
                    self.location = get_widget_size_and_loc(self.url, self.widget)
                else:
                    self.outcome.url = self.url
                    self.outcome.outcome = WidgetStatus.WIDGET_NOT_FOUND.value

            
        except requests.exceptions.ConnectionError as e:
            self.logger.error("Exception occurred", exc_info=True)
            print(e)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except requests.exceptions.ContentDecodingError as e1:
            self.logger.error("Exception occurred", exc_info = True)
            print(e1)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except requests.exceptions.InvalidSchema as e2:
            self.logger.error("Exception occurred", exc_info = True)
            print(e2)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)
        except requests.exceptions.ChunkedEncodingError as e3:
            self.logger.error("Exception occurred", exc_info = True)
            print(e3)
            self.outcome = CheckWidget(url = self.url,outcome = WidgetStatus.CONNECTION_ERROR.value)



    def widget_position(self):
        position = []
        try:
            for widg in self.widget:
                position.append(str(self.soup.prettify()).replace('&amp;','&').find(widg[0]['href']))
                self.outcome.position = min(position)/ len(str(self.soup.prettify()))
            return min(position)/ len(str(self.soup.prettify()))
        except Exception as e:
            self.logger.error("Exception occurred", exc_info=True)
            print(e)
            pass


    @classmethod
    def check_all_links(cls, links):
        for link in links:
            l = link[0]['href']
            print(f"link: {l}")
            w = Website(l)

            if w.outcome.outcome == WidgetStatus.WIDGET_FOUND.value:
                print(f'OUTCOME: {w.outcome.outcome}')
                print(f'URL: {w.outcome.url}')
                return cls(url = w.outcome.url)

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
                self.logger.error("Exception occurred", exc_info=True)            
                pass

