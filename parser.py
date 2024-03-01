from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import asyncio
import os
from refresh_tasks import refresh_tasks

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
        btn = alert.find_element(By.TAG_NAME, 'button').click()
        time.sleep(1)
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
            step_bar = timeout_validate(browser, 'player-topbar__step-pins')

            await refresh_tasks(browser)

if __name__ == '__main__':
    load_dotenv()

    url = 'https://stepik.org/lesson/290248/step/1?unit=271724'

    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')

    parameters = {
        'email': email,
        'password': password,
        'url': url,
    }
        
    asyncio.run(main(parameters))