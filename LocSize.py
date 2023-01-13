
# from pyvirtualdisplay import Display

# display = Display(visible=0, size=(800, 600))
# display.start()



from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import chromedriver_binary


user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'

options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')
# options.add_argument('headless')
options.add_argument("--start-maximized")

driver = webdriver.Chrome(chrome_options=options)
driver.minimize_window()

wait = WebDriverWait(driver, 5)

def get_widget_size_and_loc(url, widget ):
    xp = f"//{widget[0][0].name}[contains(@href,'{widget[0][0]['href']}')]"
    xp = f"//*[contains(@href,'{widget[0][0]['href']}')]"
    xp_widget = "//*[contains(@src,'https://widgets.miodottore.it/')]"

    print(f"text is : {widget[0][0].text}")

    driver.get(url)
    try:
        widg = wait.until(EC.presence_of_element_located((By.XPATH, xp)))

        w, h= widg.size['width'], widg.size['height']
        x, y= widg.location['x'], widg.location['y']
        # d = {'text':widget[0][0].text}
        # widg.rect = widg.rect | d
        d = {'height': h, 'width': w, 'x': x, 'y': y, 'text':widget[0][0].text}
        # widg.rect['text'] = widget[0][0].text
        # print(widg.rect)
        print(d)
        return d
        # return (w,h), (x,y), widget[0][0].text
    except IndexError:

        widg = wait.until(EC.presence_of_element_located((By.XPATH, xp_widget)))
        w, h= widg.size['width'], widg.size['height']
        x, y= widg.location['x'], widg.location['y']
        d = {'height': h, 'width': w, 'x': x, 'y': y}
        print(d)
        return d
    except TimeoutException:
        # widg = wait.until(EC.presence_of_element_located((By.XPATH, xp_widget)))
        # # d = {'text':widget[0][0].text}
        # # widg.rect = widg.rect | d
        # w, h= widg.size['width'], widg.size['height']
        # x, y= widg.location['x'], widg.location['y']
        # d = {'height': h, 'width': w, 'x': x, 'y': y, 'text':widget[0][0].text}
        # print(d)
        # widg.rect['text'] = widget[0][0].text
        # print(widg.rect)
        d = {'height': None, 'width': None, 'x': None, 'y': None, 'text':None}

        return d
    except StaleElementReferenceException:
        d = {'height': None, 'width': None, 'x': None, 'y': None, 'text':None}


        # print('Page failed to LOAD')
        # pass

# url = 'https://www.centromedicomirandola.it/'
# url = 'https://www.nuovasaluscenter.it/'
# url = 'https://www.polimedicapinto.it/ '
# w = Website(url)
# # size, loc, tx =  get_widget_size_and_loc(url, w.widget)
# d = get_widget_size_and_loc(url, w.widget)

