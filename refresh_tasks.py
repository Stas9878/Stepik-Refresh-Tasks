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
    for step in steps_a:
        #Номер step'а
        num_step = step.get_attribute('data-step-position')

        try:
            #Пробуем получить svg степа, если есть,то мы на уроке практики
            svg = step.find_element(By.TAG_NAME, 'svg')
            
            #Кликаем по иконке степа, чтобы перейти на след. степ
            step.click()

            time.sleep(2) #Иногда может потребоваться увеличение времени сна
            
            print(f'\t\tШаг #{num_step}', end=' - ')

            #Ждём когда появится блок с кнопкой
            div_btn = WebDriverWait(browser, timeout=15).until(
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
                #Если при сбросе задания не появляется модальное окно
                pass

            #Текущая страница
            print('Задание сброшено')   
            time.sleep(1)
            count_refresh += 1

        except NoSuchElementException as err:
            #Если нет кнопки 'Решить снова' то пропускаем степ

            #Если ошибка произошла не из-за того, что это шаг с теорией, значит это практика
            if 'svg' not in err.msg:
                    print('Задание не выполнено')
            continue

    #Возвращаем число шагов в уроке
    return count_refresh
