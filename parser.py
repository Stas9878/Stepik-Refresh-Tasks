from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import asyncio
import aiohttp
import os





async def main(parameters):
        with Chrome() as browser:
            browser.get('https://stepik.org/catalog?auth=login')
            alert = WebDriverWait(browser, 10).until(
                 EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog-inner'))
            )


if __name__ == '__main__':
    load_dotenv()

    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')

    url = 'https://stepik.org/course/179694/syllabus'
    timeout = 10

    parameters = {
        'email': email,
        'password': password,
        'url': url,
        'timeout': timeout
    }
        
    asyncio.run(main(parameters))