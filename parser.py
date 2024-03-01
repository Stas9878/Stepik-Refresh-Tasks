from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from refresh_tasks import refresh_tasks
from api import get_sections_api
import time
import asyncio
import os


def timeout_validate(browser, class_name):
    try:
        result = WebDriverWait(browser, timeout=15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
        return result
    except:
        raise Exception('Произошла ошибка поиска элемента, попробуйте увеличить timeout')

def authenticated_stepik(alert, email, password):
    print('Вход в аккаунт с указанными учётными данными..')
    try:
        #Ищем поле для ввода почты
        add_login = alert.find_element(By.ID, 'id_login_email').send_keys(email)

        #Ищем поле для ввода пароля
        add_password = alert.find_element(By.ID, 'id_login_password').send_keys(password)

        #Ищем кнопку для отправки формы и кликаем
        btn = alert.find_element(By.TAG_NAME, 'button').click()

        time.sleep(1)
        
        print('Вход выполнен успешно')
        print('_______________________\n')
        return True
    
    except:
        raise Exception('Произошла ошибка авторизации, попробуйте снова')

async def main(parameters):
        print('\nНачинаем обход курса..')
        print('_______________________\n')
        with Chrome() as browser:
            browser.get('https://stepik.org/catalog?auth=login')
            #Ожидаем отображения модального окна авторизации
            alert = timeout_validate(browser, 'modal-dialog-inner')

            #Входим в свою учётную запись
            auth = authenticated_stepik(alert, 
                                 parameters['email'], 
                                 parameters['password'])
            
            #Достаём объект курса (словарь)
            course = await parameters['course']
            #Достаём все section
            dict_course = [i for i in course['sections']]

            counter_tasks = 0            
            for d in dict_course:
                #Достаём название текущей section
                section = [key for key in d.keys()][0]

                #Индекс - '_', чтобы сделать нужный срез числа
                index = section.index('_')
                print(f'Секция - {section[:index]} ({section})')
            
                #Достаём все ссылки на step'ы в конкретной section
                lessons_url = d[section]['lessons_url']
                for num, url in enumerate(lessons_url, 1):
                    #Переходим к целевому уроку
                    browser.get(url)
                    #Ожидаем отображения тела урока
                    step_bar = timeout_validate(browser, 'lesson__player')

                    print(f'\tУрок #{num}')

                    #Ожидаем сброс заданий на этом уроке
                    num_of_refresh = await refresh_tasks(browser)
                    if num_of_refresh == 0:
                        print(f'\t\tНет заданий для сброса')
                    else:
                        print(f'\t\tСброшено заданий в этом уроке - {num_of_refresh}')
                    
                    #Отступ от предыдущей секции
                    print()

                    counter_tasks += num_of_refresh
            print('_______________________\n')
            print('Сброс заданий окончен')
            print(f'Всего сброшено заданий {counter_tasks}')
                    
                    
if __name__ == '__main__':
    load_dotenv()
    
    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')

    try:
        course = get_sections_api(int(input('\nВведите ID курса: \n')))

    except KeyError:
        print('_______________________\n')
        print('Указанного курса не сущесвует или он скрыт')
        exit()

    parameters = {
        'email': email,
        'password': password,
        'course': course,
    }
        
    asyncio.run(main(parameters))