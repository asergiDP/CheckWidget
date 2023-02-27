
from seleniumwire import webdriver  # Import from seleniumwire  
import time
from selenium.webdriver.common.by import By
# from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import chromedriver_binary


user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'

options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')
options.add_argument('headless')
options.add_argument("--start-maximized")


def check_network_requests(url: str) -> bool:
    try:
        print("Checking all network requests")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        print("Loading page")
        time.sleep(5)
        urls = []
        for request in driver.requests:  
            if request.response: 
                urls.append(request.url)
        if len([i for i in urls if 'docplanner' in i]) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)   


# url = 'https://nutrizionistavomero.com'

# check_network_requests(url)