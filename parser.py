from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import asyncio
import aiohttp
import os

def timeout_validate(browser, class_name):
    try:
        result = WebDriverWait(browser, timeout=10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
        return result
    except:
        raise Exception('Произошла ошибка поиска элемента, попробуйте увеличить timeout')

def authenticated_stepik(alert, email, password):
    try:
        add_login = alert.find_element(By.ID, 'id_login_email').send_keys(email)
        add_password = alert.find_element(By.ID, 'id_login_password').send_keys(password)
        time.sleep(1)
        btn = alert.find_element(By.TAG_NAME, 'button').click()
        time.sleep(2)
        return True
    except:
        raise Exception('Произошла ошибка авторизации, попробуйте снова')

async def main(parameters):
        with Chrome() as browser:
            browser.get('https://stepik.org/catalog?auth=login')
            #Ожидаем отображения модального окна авторизации
            alert = timeout_validate(browser, 'modal-dialog-inner')

            #Входим в свою учётную запись
            auth = authenticated_stepik(alert, 
                                 parameters['email'], 
                                 parameters['password'])
            
            #Переходим к целевому курсу
            browser.get(parameters['url'])
            #Ожидаем отображения тела урока
            sidebar = timeout_validate(browser, 'lesson-modern__wrapper')

if __name__ == '__main__':
    load_dotenv()

    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')

    url = 'https://stepik.org/lesson/1044812/step/1?unit=1053384'

    parameters = {
        'email': email,
        'password': password,
        'url': url,
    }
        
    asyncio.run(main(parameters))