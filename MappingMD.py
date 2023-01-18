import requests
from bs4 import BeautifulSoup
from enum import Enum
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

headers_md = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

class AllowsBooking(Enum):
    OK = 'OK'
    MAPPING_REVIEW = 'MAPPING REVIEW'
    INVALID_URL = 'INVALID URL'
    INDIVIDUAL_PROFILE = 'INDIVIDUAL PROFILE'

class ProfileType(Enum):
    INDIVIDUAL = 'DOCTOR_ID'
    FACILITY = 'FACILITY_ID'


@dataclass
class MappingMD:
    bookable: AllowsBooking

class MappingMD(ABC):

    def __init__(self, url: str, profile_type: ProfileType) -> None:
        self.url_md = url
        self.profile_type = profile_type
        self.r = requests.get(url= self.url_md, headers=headers_md)
        self.soup = BeautifulSoup(self.r.content, 'html5lib')
        self.md_id = self.get_id()
        self.mapping = AllowsBooking.MAPPING_REVIEW

    def get_id(self) -> str:
        match self.profile_type:
            case ProfileType.INDIVIDUAL:
                idx_start = str(self.r.content).find(ProfileType.INDIVIDUAL.value)
                idx_end = idx_start + str(self.r.content)[idx_start:].find(',')
                return ''.join([i for i in str(self.r.content)[idx_start:idx_end].split(':')[1].strip() if i.isdigit()])
            case ProfileType.FACILITY:
                idx_start = str(self.r.content).find(ProfileType.FACILITY.value)
                idx_end = idx_start + str(self.r.content)[idx_start:].find(',')
                return ''.join([i for i in str(self.r.content)[idx_start:idx_end].split(':')[1].strip() if i.isdigit()])

    @abstractmethod
    def check_MD(self):
        pass


class MappingIndividual(MappingMD):
    
    def __init__(self, url) -> None:
        super().__init__(url, profile_type = ProfileType.INDIVIDUAL)
        self.tk = self.get_access_token()
        self.address_id = self.get_address_id()
        self.mapping = self.check_MD()

    def get_access_token(self):
        idx_start_tk = str(self.r.content).find('ACCESS_TOKEN')
        idx_end_tk = idx_start_tk + str(self.r.content)[idx_start_tk:].find(',')
        return f"Bearer {''.join([i for i in str(self.r.content)[idx_start_tk:idx_end_tk].split(':')[1].strip()])}".replace('\\','').replace("'","")
    
    def get_address_id(self):
        divs = self.soup.select('div[data-address-id]')
        address_id = [div['data-address-id'] for div in divs]
        return address_id

    def check_MD(self):
        try:
            for address in self.address_id:
                api = f'https://www.miodottore.it/api/v3/doctors/{self.md_id}/addresses/{address}/services/calendar'
                headers_api = headers_md | {"authorization": self.tk}
                c = requests.get(url = api, cookies = self.r.cookies.get_dict(), headers=headers_api)
                print(c.status_code)
                print(c.json())
                if c.status_code == 200 and len(c.json()) >0:
                    return AllowsBooking.OK
                else:
                    return AllowsBooking.MAPPING_REVIEW
        except Exception as e:
            print(e)
            return AllowsBooking.INVALID_URL


class MappingFacility(MappingMD):

    def __init__(self, url):
        super().__init__(url, profile_type = ProfileType.FACILITY)
        self.mapping = self.check_MD()

    def check_MD(self):
        try:
            api = f"https://www.miodottore.it/ajax/facility/{self.md_id}/pricing"
            r = requests.get(api, headers_md)
            d = r.json()
            if '404 Questa pagina non esiste' in str(r.content):
                return AllowsBooking.INVALID_URL
            elif len(d['doctors']) >0:
                return AllowsBooking.OK
            elif len(d['doctors'])==0:
                return AllowsBooking.MAPPING_REVIEW
        except Exception as e:
            print(e)
            return AllowsBooking.INVALID_URL