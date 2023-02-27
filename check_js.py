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

driver = webdriver.Chrome(chrome_options=options)


# Go to the Google home page  
driver.get('https://www.nutrizionistavomero.com')  
time.sleep(5)

urls = []

# Access and print requests via the `requests` attribute  
for request in driver.requests:  
    if request.response:  
        print(  
            request.url,  
            request.response.status_code,  
            request.response.headers['Content-Type'])  
        urls.append(request.url)
        





[i for i in urls if 'docplanner' in i]