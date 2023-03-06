
import logging
from urllib.parse import urlparse

    
def WidgetLogger(url) -> None:
    
    name = urlparse(url).netloc
    banned_cahr = ['//','\\',':','"']
    name = [name.replace(char, '') for char in banned_cahr][0]
    # name = name.replace('//','')
    # name = name.replace('\\','')
    # name = name.replace(':','')
    # name = name.replace('"','')


    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(f"logs/{name}.log")
    # c_handler.setLevel(logging.DEBUG)
    # f_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s', datefmt= '%d-%m-%Y %H:%M:%S')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s',datefmt= '%d-%m-%Y %H:%M:%S')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    # for handler in logger.handlers[:]:
    #     logger.removeHandler(handler)
    #     handler.close()
    return logger 

logger = WidgetLogger(url= 'https://google.com')
logger.debug("cazzo")
logger.error("cazzo")
logger.info("info")
logger.error("info")


# logger = logging.getLogger(__name__)


# c_handler = logging.StreamHandler()
# f_handler = logging.FileHandler("widget.log")
# c_handler.setLevel(logging.WARNING)
# f_handler.setLevel(logging.ERROR)


# c_format = logging.Formatter('%(name)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s', datefmt= '%d-%m-%Y %H:%M:%S')
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s',datefmt= '%d-%m-%Y %H:%M:%S')
# c_handler.setFormatter(c_format)
# f_handler.setFormatter(f_format)

# logger.addHandler(c_handler)
# logger.addHandler(f_handler)


