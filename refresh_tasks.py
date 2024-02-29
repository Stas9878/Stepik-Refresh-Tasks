from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

async def refresh_tasks(browser):
    #Находим блоки div всех степов
    steps_a = browser.find_element(By.CLASS_NAME, 'player-topbar__step-pins').find_elements(By.XPATH, ".//div[contains(@class, 'm-step-pin ember-view player__step-pin')]")

    #Обход всех степов
    for step in steps_a:
        try:
            #Пробуем получить svg степа, если есть,то мы на уроке практики
            svg = step.find_element(By.TAG_NAME, 'svg')
            #Кликаем по иконке степа, чтобы перейти на след. степ
            step.click()

            time.sleep(2)

            div_btn = WebDriverWait(browser, timeout=10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'attempt__actions'))
            )
            div_btn.find_element(By.TAG_NAME, 'button').click()

            time.sleep(1)
            #Текущая страница
            print(browser.current_url)

        except:
            #Если на уроке теории, или нет кнопки 'Решить снова' то пропускаем степ
            continue
            

