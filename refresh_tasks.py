from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import time

async def refresh_tasks(browser):
    #Количество сброшенных заданий
    count_refresh = 0

    #Находим зелёные(пройденные) блоки div всех степов
    steps_a = browser.find_element(By.CLASS_NAME, 'player-topbar__step-pins').find_elements(By.CSS_SELECTOR, '.m-step-pin[data-is-passed]')

    #Обход всех степов
    for num, step in enumerate(steps_a, 1):
        print(f'\t\tШаг #{num}', end=' - ')
        try:
            #Пробуем получить svg степа, если есть,то мы на уроке практики
            svg = step.find_element(By.TAG_NAME, 'svg')
            
            #Кликаем по иконке степа, чтобы перейти на след. степ
            step.click()

            time.sleep(2) #Иногда может потребоваться увеличение времени сна
            
            #Ждём когда появится блок с кнопкой
            div_btn = WebDriverWait(browser, timeout=10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'attempt__actions'))
            )
        
            #Нажимаем на кнопку сброса задания
            div_btn.find_element(By.CSS_SELECTOR, "button[class='again-btn white']").click()

            try:
                time.sleep(1)

                #Если при сбросе задание появляется модальное окно
                alert = browser.find_element(By.CSS_SELECTOR, "footer[class='modal-popup__footer ember-view']")

                time.sleep(1)

                #Подтверждаем сброс в модальном окне
                alert_btn = alert.find_element(By.TAG_NAME, 'button').click()

            except NoSuchElementException as err:
                #Если при сбросе задание не появляется модальное окно
                pass    
                   
            time.sleep(1)
            count_refresh += 1
            #Текущая страница
            print('Задание сброшено')

        except NoSuchElementException as err:
            #Если на уроке теории, или нет кнопки 'Решить снова' то пропускаем степ
            if 'svg' in err.msg:
                print('Это теория')
            else:
                print('Это невыполненное задание')
            
            continue

    if not steps_a:
        print(f'\t\tНет пройденных шагов в данном уроке')

    #Отступ от предыдущей секции
    print()
    
    #Возвращаем число шагов в уроке
    return count_refresh
